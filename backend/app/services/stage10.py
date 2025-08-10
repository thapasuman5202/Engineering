from typing import Any, Dict, List
from app.models.stage import StageResult

revenue_records: List[Dict[str, Any]] = []
resilience_metrics: Dict[str, Any] = {"score": 0}


def revenue(data: Dict[str, Any]) -> StageResult:
    revenue_records.append(data)
    return StageResult(stage=10, status="revenue recorded", data={"count": len(revenue_records)})


def resilience() -> StageResult:
    return StageResult(stage=10, status="resilience metrics", data=resilience_metrics)
