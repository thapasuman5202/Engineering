from typing import Any, Dict
from fastapi import APIRouter
from app.services import stage8

router = APIRouter(prefix="/stage8", tags=["Stage 8"])


@router.post("/telemetry")
def telemetry(payload: Dict[str, Any]):
    return stage8.telemetry(payload)


@router.get("/plan")
def plan():
    return stage8.plan()
