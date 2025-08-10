"""API router for Stage 9 tuning and wellness endpoints."""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.models.stage import StageResult
from app.services.stage9 import Stage9Service

router = APIRouter(prefix="/stage9", tags=["Stage 9"])


@router.post("/tuning", response_model=StageResult)
def tuning(
    payload: Dict[str, Any],
    service: Stage9Service = Depends(Stage9Service),
) -> StageResult:
    """Record a tuning event.

    Args:
        payload: Parameters adjusted during tuning.
        service: Stage 9 business logic provider.

    Returns:
        StageResult: Count of tuning events recorded.

    Example:
        >>> client.post("/stage9/tuning", json={"gain": 1.2})
    """

    return service.tuning(payload)


@router.get("/wellness", response_model=StageResult)
def wellness(service: Stage9Service = Depends(Stage9Service)) -> StageResult:
    """Retrieve system wellness information.

    Args:
        service: Stage 9 business logic provider.

    Returns:
        StageResult: Current wellness summary.
    """

    return service.wellness()
