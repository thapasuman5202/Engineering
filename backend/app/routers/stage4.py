"""API router for Stage 4 compliance endpoints."""

from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage4

router = APIRouter(prefix="/stage4", tags=["Stage 4"])


@router.get("", response_model=StageResult)
def run() -> StageResult:
    """Run compliance checks for stage 4.

    Returns:
        StageResult: Compliance evaluation results.
    """

    return stage4.run()
