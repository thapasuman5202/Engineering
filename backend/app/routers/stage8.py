from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.models.stage import StageResult
from app.services.stage8 import Stage8Service

router = APIRouter(prefix="/stage8", tags=["Stage 8"])


@router.post("/telemetry", response_model=StageResult)
def telemetry(
    payload: Dict[str, Any],
    service: Stage8Service = Depends(Stage8Service),
):
    return service.telemetry(payload)


@router.get("/plan", response_model=StageResult)
def plan(service: Stage8Service = Depends(Stage8Service)):
    return service.plan()
