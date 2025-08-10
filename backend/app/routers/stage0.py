from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage0

router = APIRouter(prefix="/stage0", tags=["Stage 0"])

@router.get("", response_model=StageResult)
def run():
    return stage0.run()
