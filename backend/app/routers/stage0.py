"""API router for Stage 0 context ingestion endpoints."""

from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage0

router = APIRouter(prefix="/stage0", tags=["Stage 0"])


@router.get("", response_model=StageResult)
def run() -> StageResult:
    """Ingest initial context for the workflow.

    Returns:
        StageResult: Outcome of the ingestion step.
    """

    return stage0.run()
