from fastapi import APIRouter

from app.models.stage import StageResult
from app.services import stage5

router = APIRouter(prefix="/stage5", tags=["Stage 5"])

@router.get("", response_model=StageResult)
def run():
    return stage5.run()
