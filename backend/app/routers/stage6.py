from fastapi import APIRouter
from app.services import stage6

router = APIRouter(prefix="/stage6", tags=["Stage 6"])

@router.get("")
def run():
    return stage6.run()
