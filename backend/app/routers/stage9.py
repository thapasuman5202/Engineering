from typing import Any, Dict
from fastapi import APIRouter, Depends
from app.services.stage9 import Stage9Service

router = APIRouter(prefix="/stage9", tags=["Stage 9"])


@router.post("/tuning")
def tuning(
    payload: Dict[str, Any],
    service: Stage9Service = Depends(Stage9Service),
):
    return service.tuning(payload)


@router.get("/wellness")
def wellness(service: Stage9Service = Depends(Stage9Service)):
    return service.wellness()
