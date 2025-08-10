"""API router for Stage 11 salvage and matching endpoints."""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.models.stage import StageResult
from app.services.stage11 import Stage11Service

router = APIRouter(prefix="/stage11", tags=["Stage 11"])


@router.post("/salvage", response_model=StageResult)
def salvage(
    payload: Dict[str, Any],
    service: Stage11Service = Depends(Stage11Service),
) -> StageResult:
    """Record a salvage report.

    Args:
        payload: Details about recovered components.
        service: Stage 11 business logic provider.

    Returns:
        StageResult: Count of salvage reports stored.
    """

    return service.salvage(payload)


@router.get("/match", response_model=StageResult)
def match(service: Stage11Service = Depends(Stage11Service)) -> StageResult:
    """Retrieve current matching information.

    Args:
        service: Stage 11 business logic provider.

    Returns:
        StageResult: Match data for salvaged parts.
    """

    return service.match()
