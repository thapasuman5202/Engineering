from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage1

router = APIRouter(prefix="/stage1", tags=["Stage 1"])

@router.get("", response_model=StageResult)
def run():
    return stage1.run()
