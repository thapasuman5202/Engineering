"""Service functions for Stage 0 context ingestion."""

from app.models.stage import StageResult


def run() -> StageResult:
    """Ingest initial context for the workflow.

    Returns:
        StageResult: Outcome of the ingestion step with a status message.
    """

    data = {"message": "context ingested"}
    return StageResult(stage=0, status="context ingested", data=data)
