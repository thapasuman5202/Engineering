"""Service functions for Stage 0 context generation."""

from app.models.stage import StageResult
from app.models.context import Stage0Request, LatLon
from .stage0_context import build_site_context


def run(lat: float = 0.0, lon: float = 0.0) -> StageResult:
    """Build the site context used to initialise the workflow."""

    req = Stage0Request(location=LatLon(lat=lat, lon=lon))
    ctx = build_site_context(req)
    return StageResult(stage=0, status="context built", data=ctx.model_dump())
