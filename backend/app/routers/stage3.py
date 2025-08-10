"""API router for Stage 3 optimization endpoints."""

from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage3

router = APIRouter(prefix="/stage3", tags=["Stage 3"])


@router.get("", response_model=StageResult)
def run() -> StageResult:
    """Perform stage 3 optimization.

    Returns:
        StageResult: Optimization summary.
    """

    return stage3.run()
