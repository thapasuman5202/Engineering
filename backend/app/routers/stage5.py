"""API router for Stage 5 procurement endpoints."""

from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage5

router = APIRouter(prefix="/stage5", tags=["Stage 5"])


@router.get("", response_model=StageResult)
def run() -> StageResult:
    """Handle procurement actions for stage 5.

    Returns:
        StageResult: Procurement summary.
    """

    return stage5.run()
