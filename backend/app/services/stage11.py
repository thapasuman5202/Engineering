from typing import Any, Dict, List
from app.models.stage import StageResult

salvage_reports: List[Dict[str, Any]] = []
match_state: Dict[str, Any] = {"matches": []}


def salvage(data: Dict[str, Any]) -> StageResult:
    salvage_reports.append(data)
    return StageResult(stage=11, status="salvage recorded", data={"count": len(salvage_reports)})


def match() -> StageResult:
    return StageResult(stage=11, status="match info", data=match_state)
