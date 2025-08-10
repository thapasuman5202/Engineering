from typing import Any, Dict
from fastapi import APIRouter
from app.services import stage11

router = APIRouter(prefix="/stage11", tags=["Stage 11"])


@router.post("/salvage")
def salvage(payload: Dict[str, Any]):
    return stage11.salvage(payload)


@router.get("/match")
def match():
    return stage11.match()
