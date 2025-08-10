from typing import Any, Dict
from fastapi import APIRouter, Depends
from app.services.stage11 import Stage11Service

router = APIRouter(prefix="/stage11", tags=["Stage 11"])


@router.post("/salvage")
def salvage(
    payload: Dict[str, Any],
    service: Stage11Service = Depends(Stage11Service),
):
    return service.salvage(payload)


@router.get("/match")
def match(service: Stage11Service = Depends(Stage11Service)):
    return service.match()
