"""API router for Stage 1 variant generation endpoints."""

from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage1

router = APIRouter(prefix="/stage1", tags=["Stage 1"])


@router.get("", response_model=StageResult)
def run() -> StageResult:
    """Generate design variants for stage 1.

    Returns:
        StageResult: Summary of generated variants.
    """

    return stage1.run()
