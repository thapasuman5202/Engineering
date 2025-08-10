from fastapi import APIRouter
from app.services import stage0

router = APIRouter(prefix="/stage0", tags=["Stage 0"])

@router.get("")
def run():
    return stage0.run()
