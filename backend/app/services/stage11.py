from typing import Any, Dict, List
from app.models.stage import StageResult


class Stage11Service:
    def __init__(self) -> None:
        self.salvage_reports: List[Dict[str, Any]] = []
        self.match_state: Dict[str, Any] = {"matches": []}

    def salvage(self, data: Dict[str, Any]) -> StageResult:
        self.salvage_reports.append(data)
        return StageResult(
            stage=11,
            status="salvage recorded",
            data={"count": len(self.salvage_reports)},
        )

    def match(self) -> StageResult:
        return StageResult(stage=11, status="match info", data=self.match_state)
