from typing import Any, Dict, List
from app.models.stage import StageResult

tuning_events: List[Dict[str, Any]] = []
wellness_state: Dict[str, Any] = {"status": "nominal"}


def tuning(data: Dict[str, Any]) -> StageResult:
    tuning_events.append(data)
    return StageResult(stage=9, status="tuning received", data={"count": len(tuning_events)})


def wellness() -> StageResult:
    return StageResult(stage=9, status="wellness status", data=wellness_state)
