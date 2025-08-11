"""Stage 0 ultra context router."""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Dict, Optional

from ..models.context import SiteContext, Stage0Request
from ..services.stage0_context import (
    CTX_CACHE,
    build_site_context,
    validate_boundary,
    parse_upload,
    apply_patch,
    run_counterfactual,
    policy_watch,
)

router = APIRouter(prefix="/stage0", tags=["Stage0"])


@router.post("/context/build", response_model=SiteContext)
async def build_context(req: Stage0Request) -> SiteContext:
    """Build a deterministic SiteContext."""
    return build_site_context(req)


class BoundaryRequest(BaseModel):
    boundary_geojson: dict


@router.post("/context/validate")
async def validate_ctx(req: BoundaryRequest) -> Dict:
    """Validate boundary geometry."""
    return validate_boundary(req.boundary_geojson)


@router.post("/context/upload")
async def upload_boundary(file: UploadFile = File(...)) -> Dict:
    """Parse an uploaded boundary file."""
    boundary = parse_upload(file)
    return {"boundary_geojson": boundary}


@router.get("/context/{context_id}", response_model=SiteContext)
async def get_context(context_id: str) -> SiteContext:
    """Retrieve a cached context by id."""
    ctx = CTX_CACHE.get(context_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="Context not found")
    return ctx


@router.get("/sources")
async def list_sources() -> Dict:
    """List available data sources."""
    return {"online_default": False, "adapters": ["offline_synthetic_v2", "osm_stub", "cmip_stub"]}


class ResolveRequest(BaseModel):
    context_id: str
    patch: Dict


@router.post("/resolve", response_model=SiteContext)
async def resolve_context(req: ResolveRequest) -> SiteContext:
    """Apply human patch overrides to a context."""
    ctx = CTX_CACHE.get(req.context_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="Context not found")
    return apply_patch(ctx, req.patch)


class CounterfactualRequest(BaseModel):
    context_id: str
    delta: Dict[str, float]


@router.post("/counterfactual")
async def counterfactual(req: CounterfactualRequest) -> Dict:
    """Run a simple counterfactual analysis."""
    ctx = CTX_CACHE.get(req.context_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="Context not found")
    before = ctx
    after = run_counterfactual(ctx, req.delta)
    deltas = {k: getattr(after.risk_scores, k) - getattr(before.risk_scores, k) for k in after.risk_scores.model_fields}
    return {"before": before, "after": after, "deltas": deltas}


class PolicyWatchRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None


@router.post("/policy/watch")
async def policy_watch_ep(req: PolicyWatchRequest) -> Dict:
    """Estimate zoning change probability from policy text."""
    return policy_watch(req.text, req.url)
