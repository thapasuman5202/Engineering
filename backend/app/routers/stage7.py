from fastapi import APIRouter
from app.services import stage7

router = APIRouter(prefix="/stage7", tags=["Stage 7"])

@router.get("")
def run():
    return stage7.run()
