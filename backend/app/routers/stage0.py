"""API router for Stage 0 context and resolution endpoints."""

from __future__ import annotations

from typing import Dict, List
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.context import SiteContext, Stage0Request
from app.services.stage0_context import build_site_context

router = APIRouter(prefix="/stage0", tags=["Stage 0"])

# In-memory store for built contexts
_CONTEXTS: Dict[str, SiteContext] = {}


class BuildContextResponse(BaseModel):
    """Response payload for :func:`build_context`."""

    context_id: str
    context: SiteContext


class ValidateContextRequest(BaseModel):
    """Request body for :func:`validate_context`."""

    context: SiteContext


class ValidateContextResponse(BaseModel):
    """Validation outcome returned by :func:`validate_context`."""

    valid: bool
    errors: List[str] = []


class UploadContextRequest(BaseModel):
    """Request body for :func:`upload_context`."""

    context_id: str


class UploadContextResponse(BaseModel):
    """Result returned by :func:`upload_context`."""

    uploaded: bool


class ResolveRequest(BaseModel):
    """Request model for :func:`resolve`."""

    query: str


class ResolveResponse(BaseModel):
    """Resolution result for :func:`resolve`."""

    result: str


class CounterfactualRequest(BaseModel):
    """Request payload for :func:`counterfactual`."""

    scenario: str


class CounterfactualResponse(BaseModel):
    """Response payload for :func:`counterfactual`."""

    description: str


class PolicyWatchRequest(BaseModel):
    """Request model for :func:`policy_watch`."""

    policy_id: str


class PolicyWatchResponse(BaseModel):
    """Response model for :func:`policy_watch`."""

    status: str


@router.post("/context/build", response_model=BuildContextResponse)
def build_context(req: Stage0Request) -> BuildContextResponse:
    """Build and cache a synthetic site context."""

    ctx = build_site_context(req)
    context_id = uuid4().hex
    _CONTEXTS[context_id] = ctx
    return BuildContextResponse(context_id=context_id, context=ctx)


@router.post("/context/validate", response_model=ValidateContextResponse)
def validate_context(req: ValidateContextRequest) -> ValidateContextResponse:
    """Validate a site context for completeness."""

    # This demo always considers the context valid.
    return ValidateContextResponse(valid=True)


@router.post("/context/upload", response_model=UploadContextResponse)
def upload_context(req: UploadContextRequest) -> UploadContextResponse:
    """Upload a previously built context."""

    if req.context_id not in _CONTEXTS:
        raise HTTPException(status_code=404, detail="Context not found")
    return UploadContextResponse(uploaded=True)


@router.get("/context/{context_id}", response_model=SiteContext)
def get_context(context_id: str) -> SiteContext:
    """Retrieve a cached context by its identifier."""

    ctx = _CONTEXTS.get(context_id)
    if ctx is None:
        raise HTTPException(status_code=404, detail="Context not found")
    return ctx


@router.get("/sources", response_model=List[str])
def list_sources() -> List[str]:
    """List data sources used for context generation."""

    return ["synthetic-data"]


@router.post("/resolve", response_model=ResolveResponse)
def resolve(req: ResolveRequest) -> ResolveResponse:
    """Resolve a free form query against the context."""

    return ResolveResponse(result=f"resolved: {req.query}")


@router.post("/counterfactual", response_model=CounterfactualResponse)
def counterfactual(req: CounterfactualRequest) -> CounterfactualResponse:
    """Generate a simple counterfactual analysis."""

    return CounterfactualResponse(description=f"counterfactual for {req.scenario}")


@router.post("/policy/watch", response_model=PolicyWatchResponse)
def policy_watch(req: PolicyWatchRequest) -> PolicyWatchResponse:
    """Register a policy watch on the given identifier."""

    return PolicyWatchResponse(status=f"watching {req.policy_id}")
