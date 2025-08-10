from app.models.stage import StageResult


def run() -> StageResult:
    data = {"message": "context ingested"}
    return StageResult(stage=0, status="context ingested", data=data)
