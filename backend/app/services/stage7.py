"""Service functions for Stage 7 permitting."""

from app.models.stage import StageResult


def run() -> StageResult:
    """Submit permitting information for stage 7.

    Returns:
        StageResult: Current permit status.
    """

    return StageResult(stage=7, status="permit submitted", data={"approved": False})
