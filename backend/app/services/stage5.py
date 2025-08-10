from app.models.stage import StageResult


def run() -> StageResult:
    return StageResult(stage=5, status="procurement complete", data={"contracts": []})
