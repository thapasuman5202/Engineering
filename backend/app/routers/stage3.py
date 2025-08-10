from fastapi import APIRouter
from app.services import stage3

router = APIRouter(prefix="/stage3", tags=["Stage 3"])

@router.get("")
def run():
    return stage3.run()
