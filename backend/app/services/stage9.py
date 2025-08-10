from typing import Any, Dict, List

from app.models.stage import StageResult


class Stage9Service:
    """Encapsulates mutable state for Stage 9 operations."""

    def __init__(self) -> None:
        self.tuning_events: List[Dict[str, Any]] = []
        self.wellness_state: Dict[str, Any] = {"status": "nominal"}

    def tuning(self, data: Dict[str, Any]) -> StageResult:
        """Record a tuning event and return current count."""
        self.tuning_events.append(data)
        return StageResult(
            stage=9,
            status="tuning received",
            data={"count": len(self.tuning_events)},
        )

    def wellness(self) -> StageResult:
        """Return current wellness status."""
        return StageResult(stage=9, status="wellness status", data=self.wellness_state)


service = Stage9Service()


def tuning(data: Dict[str, Any]) -> StageResult:
    return service.tuning(data)


def wellness() -> StageResult:
    return service.wellness()


def reset_state() -> None:
    """Reset service state for testing purposes."""
    global service
    service = Stage9Service()
