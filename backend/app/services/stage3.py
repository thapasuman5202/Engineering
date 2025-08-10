from app.models.stage import StageResult


def run() -> StageResult:
    return StageResult(stage=3, status="optimization complete", data={"best_score": 0.9})
