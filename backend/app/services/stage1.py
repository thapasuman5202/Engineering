"""Service functions for Stage 1 variant generation."""

from app.models.stage import StageResult
from app.ai_agents.negotiator import negotiator


def run() -> StageResult:
    """Generate combinatorial design variants.

    Returns:
        StageResult: Details about the produced design variants.
    """

    variants = negotiator.generate_variants()
    return StageResult(stage=1, status="variants generated", data={"variants": variants})
