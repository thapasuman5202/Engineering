"""API router for Stage 7 permitting endpoints."""

from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage7

router = APIRouter(prefix="/stage7", tags=["Stage 7"])


@router.get("", response_model=StageResult)
def run() -> StageResult:
    """Submit permitting information for stage 7.

    Returns:
        StageResult: Permit status information.
    """

    return stage7.run()
