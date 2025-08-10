from fastapi import APIRouter
from app.services import stage5

router = APIRouter(prefix="/stage5", tags=["Stage 5"])

@router.get("")
def run():
    return stage5.run()
