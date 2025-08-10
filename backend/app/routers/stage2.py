from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage2

router = APIRouter(prefix="/stage2", tags=["Stage 2"])

@router.get("", response_model=StageResult)
def run():
    return stage2.run()
