from app.models.stage import StageResult


def run() -> StageResult:
    return StageResult(stage=7, status="permit submitted", data={"approved": False})
