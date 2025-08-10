from app.models.stage import StageResult


def run() -> StageResult:
    return StageResult(stage=2, status="analysis complete", data={"result": "simulated"})
