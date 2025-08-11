from __future__ import annotations

import uuid
import asyncio
import json
from typing import Dict, List

import jwt
from celery import Celery, chain
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sse_starlette.sse import EventSourceResponse

from app.core.config import settings
from app.models import (
    FeedbackIn,
    GenerateRequest,
    JobEvent,
    JobOut,
    JobStatus,
    VariantOut,
)

router = APIRouter(prefix="/v1", tags=["v1"])

security = HTTPBearer()

celery_app = Celery("workers", broker=settings.redis_url, backend=settings.redis_url)

JOBS: Dict[str, AsyncResult] = {}
VARIANTS: Dict[str, VariantOut] = {}
FEEDBACK: Dict[str, List[FeedbackIn]] = {}


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    token = credentials.credentials
    try:
        return jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=401, detail="Invalid token") from exc


@router.post("/generate", response_model=JobOut)
async def generate(
    req: GenerateRequest, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> JobOut:
    verify_token(credentials)
    workflow = chain(
        celery_app.signature("workers.render.render"),
        celery_app.signature("workers.massing.massing"),
        celery_app.signature("workers.export.export"),
    )
    result = workflow.apply_async()
    job_id = uuid.UUID(result.id)
    JOBS[str(job_id)] = result
    return JobOut(id=job_id, status=JobStatus.queued)


@router.get("/jobs/{job_id}", response_model=JobOut)
async def get_job(
    job_id: uuid.UUID, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> JobOut:
    verify_token(credentials)
    result = JOBS.get(str(job_id)) or AsyncResult(str(job_id), app=celery_app)
    state = result.state
    status_map = {
        "PENDING": JobStatus.queued,
        "STARTED": JobStatus.running,
        "SUCCESS": JobStatus.completed,
        "FAILURE": JobStatus.failed,
    }
    status = status_map.get(state, JobStatus.queued)
    variants = result.result if state == "SUCCESS" else None
    error = str(result.result) if state == "FAILURE" else None
    return JobOut(id=job_id, status=status, variants=variants, error=error)


@router.websocket("/jobs/{job_id}/events")
async def job_events(websocket: WebSocket, job_id: uuid.UUID, token: str):
    try:
        jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except Exception:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    result = AsyncResult(str(job_id), app=celery_app)
    status_map = {
        "PENDING": JobStatus.queued,
        "STARTED": JobStatus.running,
        "SUCCESS": JobStatus.completed,
        "FAILURE": JobStatus.failed,
    }
    prev_state: str | None = None
    while True:
        state = result.state
        status = status_map.get(state, JobStatus.queued)
        if state != prev_state:
            await websocket.send_json(
                JobEvent(type="status", data={"status": status}).model_dump()
            )
            prev_state = state
        if state in ("SUCCESS", "FAILURE"):
            break
        await asyncio.sleep(1)
    await websocket.close()


@router.get("/jobs/{job_id}/events-sse")
async def job_events_sse(job_id: uuid.UUID, token: str):
    try:
        jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    async def event_generator():
        result = AsyncResult(str(job_id), app=celery_app)
        status_map = {
            "PENDING": JobStatus.queued,
            "STARTED": JobStatus.running,
            "SUCCESS": JobStatus.completed,
            "FAILURE": JobStatus.failed,
        }
        prev_state: str | None = None
        while True:
            state = result.state
            status = status_map.get(state, JobStatus.queued)
            if state != prev_state:
                yield {
                    "event": "status",
                    "data": json.dumps({"status": status}),
                }
                prev_state = state
            if state in ("SUCCESS", "FAILURE"):
                break
            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())


@router.get("/variants/{variant_id}", response_model=VariantOut)
async def get_variant(
    variant_id: uuid.UUID, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> VariantOut:
    verify_token(credentials)
    variant = VARIANTS.get(str(variant_id))
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant


@router.post("/feedback/{variant_id}")
async def submit_feedback(
    variant_id: uuid.UUID,
    fb: FeedbackIn,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, str]:
    verify_token(credentials)
    if str(variant_id) not in VARIANTS:
        raise HTTPException(status_code=404, detail="Variant not found")
    FEEDBACK.setdefault(str(variant_id), []).append(fb)
    return {"status": "ok"}
