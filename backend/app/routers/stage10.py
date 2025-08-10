"""API router for Stage 10 revenue and resilience endpoints."""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.models.stage import StageResult
from app.services.stage10 import Stage10Service

router = APIRouter(prefix="/stage10", tags=["Stage 10"])


@router.post("/revenue", response_model=StageResult)
def revenue(
    payload: Dict[str, Any],
    service: Stage10Service = Depends(Stage10Service),
) -> StageResult:
    """Record revenue information.

    Args:
        payload: Revenue details to log.
        service: Stage 10 business logic provider.

    Returns:
        StageResult: Count of revenue records stored.
    """

    return service.revenue(payload)


@router.get("/resilience", response_model=StageResult)
def resilience(service: Stage10Service = Depends(Stage10Service)) -> StageResult:
    """Retrieve resilience metrics.

    Args:
        service: Stage 10 business logic provider.

    Returns:
        StageResult: Current resilience metrics.
    """

    return service.resilience()
