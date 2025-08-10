from typing import Any, Dict, List

from app.models.stage import StageResult


class Stage10Service:
    """Encapsulates mutable state for Stage 10 operations."""

    def __init__(self) -> None:
        self.revenue_records: List[Dict[str, Any]] = []
        self.resilience_metrics: Dict[str, Any] = {"score": 0}

    def revenue(self, data: Dict[str, Any]) -> StageResult:
        """Record revenue information and return current count."""
        self.revenue_records.append(data)
        return StageResult(
            stage=10,
            status="revenue recorded",
            data={"count": len(self.revenue_records)},
        )

    def resilience(self) -> StageResult:
        """Return resilience metrics."""
        return StageResult(stage=10, status="resilience metrics", data=self.resilience_metrics)


service = Stage10Service()


def revenue(data: Dict[str, Any]) -> StageResult:
    return service.revenue(data)


def resilience() -> StageResult:
    return service.resilience()


def reset_state() -> None:
    """Reset service state for testing purposes."""
    global service
    service = Stage10Service()
