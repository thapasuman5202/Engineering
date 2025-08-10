from fastapi import APIRouter
from app.services import stage1

router = APIRouter(prefix="/stage1", tags=["Stage 1"])

@router.get("")
def run():
    return stage1.run()
