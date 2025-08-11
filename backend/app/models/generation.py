from __future__ import annotations

from typing import Any, Dict, Literal, Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel


class Weights(BaseModel):
    aesthetic: float = 0.25
    sustainability: float = 0.25
    cost: float = 0.20
    accessibility: float = 0.15
    emotion: float = 0.15


class VariantAsset(BaseModel):
    type: Literal['render', 'model', 'pdf', 'json']
    path: str
    signed_url: Optional[str] = None


class VariantOut(BaseModel):
    id: UUID
    label: str
    metadata: Dict[str, Any] | None = None
    score: Dict[str, float] | None = None
    rank: int
    assets: list[VariantAsset] = []


class GenerateRequest(BaseModel):
    n: int = 3
    weights: Weights = Weights()


class JobStatus(str, Enum):
    queued = "queued"
    completed = "completed"
    failed = "failed"


class JobOut(BaseModel):
    id: UUID
    status: JobStatus
    variants: list[VariantOut] | None = None
    error: Optional[str] = None


class JobEvent(BaseModel):
    type: Literal["status", "variant"]
    data: Dict[str, Any]


class FeedbackIn(BaseModel):
    rating: int
    comment: Optional[str] = None

