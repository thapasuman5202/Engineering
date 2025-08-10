from app.models.stage import StageResult


def run() -> StageResult:
    return StageResult(stage=6, status="fabrication scheduled", data={"robots": 3})
