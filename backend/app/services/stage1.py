from app.models.stage import StageResult
from app.ai_agents.negotiator import negotiator


def run() -> StageResult:
    """Execute stage 1 by generating combinatorial design variants."""
    variants = negotiator.generate_variants()
    return StageResult(stage=1, status="variants generated", data={"variants": variants})
