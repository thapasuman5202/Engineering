from __future__ import annotations

import uuid
from typing import Dict, List

import jwt
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.ai_agents.orchestrator import run_generation
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

JOBS: Dict[str, JobOut] = {}
VARIANTS: Dict[str, VariantOut] = {}
FEEDBACK: Dict[str, List[FeedbackIn]] = {}


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    token = credentials.credentials
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=401, detail="Invalid token") from exc


@router.post("/generate", response_model=JobOut)
async def generate(req: GenerateRequest, credentials: HTTPAuthorizationCredentials = Depends(security)) -> JobOut:
    verify_token(credentials)
    variants = run_generation(req.n, req.weights)
    job_id = uuid.uuid4()
    for v in variants:
        VARIANTS[str(v.id)] = v
    job = JobOut(id=job_id, status=JobStatus.completed, variants=variants)
    JOBS[str(job_id)] = job
    return job


@router.get("/jobs/{job_id}", response_model=JobOut)
async def get_job(job_id: uuid.UUID, credentials: HTTPAuthorizationCredentials = Depends(security)) -> JobOut:
    verify_token(credentials)
    job = JOBS.get(str(job_id))
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.websocket("/jobs/{job_id}/events")
async def job_events(websocket: WebSocket, job_id: uuid.UUID, token: str):
    try:
        jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except Exception:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    job = JOBS.get(str(job_id))
    if not job:
        await websocket.close(code=1008)
        return
    await websocket.send_json(JobEvent(type="status", data={"status": job.status}).model_dump())
    for variant in job.variants or []:
        await websocket.send_json(JobEvent(type="variant", data=variant.model_dump()).model_dump())
    await websocket.close()


@router.get("/variants/{variant_id}", response_model=VariantOut)
async def get_variant(variant_id: uuid.UUID, credentials: HTTPAuthorizationCredentials = Depends(security)) -> VariantOut:
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
