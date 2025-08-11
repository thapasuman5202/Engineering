"""Service functions for Stage 1 variant generation."""

from app.models import StageResult, Weights
from app.ai_agents.orchestrator import run_generation


def run(n_variants: int = 3, weights: Weights | None = None) -> StageResult:
    """Generate design variants using simple agent orchestration."""

    weights = weights or Weights()
    variants = run_generation(n_variants, weights)
    data = {"variants": [v.model_dump() for v in variants]}
    return StageResult(stage=1, status="variants generated", data=data)
