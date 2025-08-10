from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage6

router = APIRouter(prefix="/stage6", tags=["Stage 6"])

@router.get("", response_model=StageResult)
def run():
    return stage6.run()
