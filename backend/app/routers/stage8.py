"""API router for Stage 8 telemetry and planning endpoints."""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.models.stage import StageResult
from app.services.stage8 import Stage8Service

router = APIRouter(prefix="/stage8", tags=["Stage 8"])


@router.post("/telemetry", response_model=StageResult)
def telemetry(
    payload: Dict[str, Any],
    service: Stage8Service = Depends(Stage8Service),
) -> StageResult:
    """Record telemetry information.

    Args:
        payload: Sensor readings or status updates.
        service: Stage 8 business logic provider.

    Returns:
        StageResult: Count of telemetry entries stored.

    Example:
        >>> client.post("/stage8/telemetry", json={"temp": 70})
    """

    return service.telemetry(payload)


@router.get("/plan", response_model=StageResult)
def plan(service: Stage8Service = Depends(Stage8Service)) -> StageResult:
    """Retrieve the current execution plan.

    Args:
        service: Stage 8 business logic provider.

    Returns:
        StageResult: Scheduled tasks for Stage 8.
    """

    return service.plan()
