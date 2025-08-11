from __future__ import annotations

import json
from typing import Dict, List, Optional

from shapely.geometry import Polygon, shape

from app.models.context import RiskScores, SiteContext, Stage0Request, UQNumber
from shared.cache import get as cache_get, set as cache_set
from shared.stage0_client import fetch_context

# In-memory map of context_id -> SiteContext for quick lookups and mutations
CTX_CACHE: Dict[str, SiteContext] = {}


def build_site_context(req: Stage0Request) -> SiteContext:
    """Fetch a site context using the Stage0 adapter with Redis caching."""
    project_id = req.site_name
    key = f"stage0:context:{project_id}"
    cached = cache_get(key)
    if cached:
        ctx = SiteContext.model_validate_json(cached)
        CTX_CACHE[ctx.context_id] = ctx
        return ctx

    ctx = fetch_context(project_id)
    cache_set(key, ctx.model_dump_json())
    CTX_CACHE[ctx.context_id] = ctx
    return ctx


def validate_boundary(boundary_geojson: dict) -> dict:
    errors: List[str] = []
    try:
        geom = shape(boundary_geojson)
        if not isinstance(geom, Polygon):
            raise ValueError("geometry must be polygon-like")
        if not geom.is_valid:
            errors.append("self-intersection")
    except Exception as exc:
        errors.append(str(exc))
    return {"valid": not errors, "errors": errors}


def parse_upload(file) -> dict:
    if file is None:
        raise ValueError("no file provided")
    data = file.file.read()
    try:
        return json.loads(data)
    except Exception:
        raise ValueError("unsupported file type")


# --- Counterfactual helpers retained from mock implementation ---


def _with_uq(x: float, src: str, band: float = 0.15) -> UQNumber:
    low = x * (1 - band)
    high = x * (1 + band)
    return UQNumber(
        value=x, ci95_low=max(0.0, low), ci95_high=max(low, high), source=src
    )


def _risk_scores(
    climate: Dict[str, UQNumber], environment: Dict[str, UQNumber]
) -> RiskScores:
    flood = int(min(100, environment["water_pct"].value * 800))
    heat = int(
        min(
            100,
            climate["avg_temp_c"].value * 3 - environment["greenspace_pct"].value * 50,
        )
    )
    quake = 50
    pollution = int(min(100, 60 - environment["greenspace_pct"].value * 50))
    return RiskScores(
        flood_0_100=flood, quake_0_100=quake, heat_0_100=heat, pollution_0_100=pollution
    )


def apply_patch(ctx: SiteContext, patch: dict) -> SiteContext:
    for key, val in patch.items():
        setattr(ctx, key, val)
    for ln in ctx.lineage.values():
        ln.transform += "+ human_override"
    CTX_CACHE[ctx.context_id] = ctx
    return ctx


def run_counterfactual(ctx: SiteContext, delta: Dict[str, float]) -> SiteContext:
    new_ctx = ctx.model_copy(deep=True)
    for key, val in delta.items():
        if key in new_ctx.environment:
            base = new_ctx.environment[key].value + val
            new_ctx.environment[key] = _with_uq(base, new_ctx.environment[key].source)
    new_ctx.risk_scores = _risk_scores(new_ctx.climate, new_ctx.environment)
    new_ctx.design_objectives_suggested = ctx.design_objectives_suggested
    return new_ctx


def policy_watch(text: Optional[str], url: Optional[str]) -> Dict:
    prob = 0.1
    topics: List[str] = []
    txt = (text or "").lower()
    for k in ["upzone", "tod", "density bonus"]:
        if k in txt:
            prob += 0.2
            topics.append(k)
    for k in ["overlay", "heritage"]:
        if k in txt:
            prob -= 0.1
            topics.append(k)
    prob = max(0.0, min(1.0, prob))
    citations = [url] if url else []
    explain = "keywords detected" if topics else "baseline probability"
    return {
        "zoning_change_prob_0_1": prob,
        "topics": topics,
        "citations": citations,
        "explain": explain,
    }
