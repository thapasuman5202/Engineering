from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage7

router = APIRouter(prefix="/stage7", tags=["Stage 7"])

@router.get("", response_model=StageResult)
def run():
    return stage7.run()
