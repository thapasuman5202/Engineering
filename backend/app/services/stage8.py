from typing import Any, Dict, List

from app.models.stage import StageResult


class Stage8Service:
    """Encapsulates mutable state for Stage 8 operations."""

    def __init__(self) -> None:
        self.telemetry_log: List[Dict[str, Any]] = []
        self.current_plan: Dict[str, Any] = {"tasks": []}

    def telemetry(self, data: Dict[str, Any]) -> StageResult:
        """Record telemetry data and return count of entries."""
        self.telemetry_log.append(data)
        return StageResult(
            stage=8,
            status="telemetry received",
            data={"count": len(self.telemetry_log)},
        )

    def plan(self) -> StageResult:
        """Return the current plan state."""
        return StageResult(stage=8, status="current plan", data=self.current_plan)


service = Stage8Service()


def telemetry(data: Dict[str, Any]) -> StageResult:
    return service.telemetry(data)


def plan() -> StageResult:
    return service.plan()


def reset_state() -> None:
    """Reset the service state for testing purposes."""
    global service
    service = Stage8Service()


def scheduler_stub() -> None:
    pass
