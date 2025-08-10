from fastapi import APIRouter
from app.services import stage2

router = APIRouter(prefix="/stage2", tags=["Stage 2"])

@router.get("")
def run():
    return stage2.run()
