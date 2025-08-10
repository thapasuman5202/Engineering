from typing import Any, Dict
from fastapi import APIRouter
from app.services import stage9

router = APIRouter(prefix="/stage9", tags=["Stage 9"])


@router.post("/tuning")
def tuning(payload: Dict[str, Any]):
    return stage9.tuning(payload)


@router.get("/wellness")
def wellness():
    return stage9.wellness()
