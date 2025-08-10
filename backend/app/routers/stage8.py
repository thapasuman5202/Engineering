from typing import Any, Dict
from fastapi import APIRouter, Depends
from app.services.stage8 import Stage8Service

router = APIRouter(prefix="/stage8", tags=["Stage 8"])


@router.post("/telemetry")
def telemetry(
    payload: Dict[str, Any],
    service: Stage8Service = Depends(Stage8Service),
):
    return service.telemetry(payload)


@router.get("/plan")
def plan(service: Stage8Service = Depends(Stage8Service)):
    return service.plan()
