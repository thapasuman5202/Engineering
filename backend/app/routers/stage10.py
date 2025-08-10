from typing import Any, Dict
from fastapi import APIRouter
from app.services import stage10

router = APIRouter(prefix="/stage10", tags=["Stage 10"])


@router.post("/revenue")
def revenue(payload: Dict[str, Any]):
    return stage10.revenue(payload)


@router.get("/resilience")
def resilience():
    return stage10.resilience()
