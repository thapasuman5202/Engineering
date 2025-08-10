from typing import Any, Dict
from fastapi import APIRouter, Depends
from app.services.stage10 import Stage10Service

router = APIRouter(prefix="/stage10", tags=["Stage 10"])


@router.post("/revenue")
def revenue(
    payload: Dict[str, Any],
    service: Stage10Service = Depends(Stage10Service),
):
    return service.revenue(payload)


@router.get("/resilience")
def resilience(service: Stage10Service = Depends(Stage10Service)):
    return service.resilience()
