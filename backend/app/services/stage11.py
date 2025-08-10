from typing import Any, Dict, List

from app.models.stage import StageResult


class Stage11Service:
    """Encapsulates mutable state for Stage 11 operations."""

    def __init__(self) -> None:
        self.salvage_reports: List[Dict[str, Any]] = []
        self.match_state: Dict[str, Any] = {"matches": []}

    def salvage(self, data: Dict[str, Any]) -> StageResult:
        """Record salvage information and return current count."""
        self.salvage_reports.append(data)
        return StageResult(
            stage=11,
            status="salvage recorded",
            data={"count": len(self.salvage_reports)},
        )

    def match(self) -> StageResult:
        """Return current match state."""
        return StageResult(stage=11, status="match info", data=self.match_state)


service = Stage11Service()


def salvage(data: Dict[str, Any]) -> StageResult:
    return service.salvage(data)


def match() -> StageResult:
    return service.match()


def reset_state() -> None:
    """Reset service state for testing purposes."""
    global service
    service = Stage11Service()
