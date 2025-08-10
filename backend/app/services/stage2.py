"""Service functions for Stage 2 analysis simulation."""

from app.models.stage import StageResult


def run() -> StageResult:
    """Simulate analysis for stage 2.

    Returns:
        StageResult: Simulated analysis outcome.
    """

    return StageResult(stage=2, status="analysis complete", data={"result": "simulated"})
