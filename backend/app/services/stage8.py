from typing import Any, Dict, List
from app.models.stage import StageResult

telemetry_log: List[Dict[str, Any]] = []
current_plan: Dict[str, Any] = {"tasks": []}


def telemetry(data: Dict[str, Any]) -> StageResult:
    telemetry_log.append(data)
    return StageResult(stage=8, status="telemetry received", data={"count": len(telemetry_log)})


def plan() -> StageResult:
    return StageResult(stage=8, status="current plan", data=current_plan)


def scheduler_stub() -> None:
    pass
