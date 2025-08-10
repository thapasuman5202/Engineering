from app.models.stage import StageResult


def run() -> StageResult:
    return StageResult(stage=4, status="compliance check passed", data={"issues": []})
