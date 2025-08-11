from __future__ import annotations

from typing import Any, Dict, Literal, Optional
from uuid import UUID

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

