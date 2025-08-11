from app.ai_agents.orchestrator import run_generation
from app.models import Weights


def test_run_generation_returns_ranked_variants():
    weights = Weights()
    variants = run_generation(5, weights)
    assert len(variants) == 5
    scores = [v.score["composite"] for v in variants]
    assert scores == sorted(scores, reverse=True)
