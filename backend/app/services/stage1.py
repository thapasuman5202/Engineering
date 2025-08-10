from app.models.stage import StageResult
from app.ai_agents.negotiator import negotiator


def run() -> StageResult:
    variants = negotiator.generate_variants()
    return StageResult(stage=1, status="variants generated", data={"variants": variants})
