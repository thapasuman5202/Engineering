from fastapi import APIRouter
from app.services import stage4

router = APIRouter(prefix="/stage4", tags=["Stage 4"])

@router.get("")
def run():
    return stage4.run()
