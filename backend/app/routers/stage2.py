"""API router for Stage 2 analysis endpoints."""

from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage2

router = APIRouter(prefix="/stage2", tags=["Stage 2"])


@router.get("", response_model=StageResult)
def run() -> StageResult:
    """Execute stage 2 analysis.

    Returns:
        StageResult: Simulated analysis outcome.
    """

    return stage2.run()
