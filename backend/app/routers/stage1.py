"""API router for Stage 1 variant generation endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.models import StageResult, Weights
from app.services import stage1

router = APIRouter(prefix="/stage1", tags=["Stage 1"])


class GenerateRequest(BaseModel):
    n_variants: int = 3
    weights: Weights | None = None


@router.post("/generate", response_model=StageResult)
def generate(req: GenerateRequest) -> StageResult:
    """Generate design variants for stage 1."""

    return stage1.run(req.n_variants, req.weights)
