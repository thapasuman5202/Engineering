"""Service functions for Stage 6 fabrication scheduling."""

from app.models.stage import StageResult


def run() -> StageResult:
    """Schedule fabrication for stage 6.

    Returns:
        StageResult: Details about the fabrication plan.
    """

    return StageResult(stage=6, status="fabrication scheduled", data={"robots": 3})
