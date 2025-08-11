"""Utility helpers for building a synthetic site context for Stage 0.

This module exposes a :func:`build_site_context` factory which generates a
:class:`~app.models.context.SiteContext` instance populated with deterministic
pseudo–random data.  The goal of the helpers is not to be scientifically
accurate but to provide stable and easily testable structures that mimic what a
real implementation could look like.

The module maintains a simple in–memory cache so repeated requests for the same
site do not need to rebuild the context.
"""

from __future__ import annotations

from random import Random
from typing import Dict

from app.models.context import (
    AuditBlock,
    ClimateScen,
    DataQuality,
    ExplainItem,
    LatLon,
    PrivacyReport,
    RiskScores,
    SiteContext,
    Stage0Request,
    SubsurfaceStub,
    ZoningDrift,
    UQNumber,
)

# ---------------------------------------------------------------------------
# Module level cache --------------------------------------------------------
# ---------------------------------------------------------------------------

# Keyed by ``"{lat},{lon}:{scenario}"``
CTX_CACHE: Dict[str, SiteContext] = {}


# ---------------------------------------------------------------------------
# Helper utilities ----------------------------------------------------------
# ---------------------------------------------------------------------------

def _seed(location: LatLon) -> Random:
    """Create a deterministic random generator based on location.

    Parameters
    ----------
    location:
        Geographic coordinates used for seeding.  Small rounding is performed so
        that nearby values still produce stable seeds.
    """

    seed_val = hash((round(location.lat, 4), round(location.lon, 4)))
    return Random(seed_val)


def _with_uq(rng: Random, value: float, rel_uncertainty: float = 0.05, unit: str | None = None) -> UQNumber:
    """Return ``value`` packaged with a simple relative uncertainty.

    A small amount of variability is added using the provided random generator
    to keep the function deterministic for a given seed.
    """

    jitter = 1 + (rng.random() - 0.5) * rel_uncertainty
    val = value * jitter
    return UQNumber(value=val, uncertainty=abs(val) * rel_uncertainty, unit=unit)


def _synthetic_climate(rng: Random, scen: ClimateScen) -> RiskScores:
    """Generate fake climate risk scores.

    The numbers are purely illustrative and depend on the selected scenario.
    """

    base = rng.uniform(0, 1)
    scen_mult = {
        ClimateScen.HISTORICAL: 1.0,
        ClimateScen.SSP126: 1.1,
        ClimateScen.SSP245: 1.3,
        ClimateScen.SSP585: 1.8,
    }[scen]
    exposure = _with_uq(rng, base * scen_mult, 0.1).value
    damage = _with_uq(rng, base * scen_mult * 0.6, 0.1).value
    score = (exposure + damage) / 2
    return RiskScores(exposure=exposure, damage=damage, score=score)


def _synthetic_zoning(rng: Random) -> ZoningDrift:
    compliant = rng.random() > 0.1
    msg = None if compliant else "Potential zoning variance required"
    return ZoningDrift(compliant=compliant, message=msg)


def _synthetic_data_quality(rng: Random) -> DataQuality:
    return DataQuality(
        completeness=_with_uq(rng, rng.uniform(0.7, 1.0), 0.02).value,
        accuracy=_with_uq(rng, rng.uniform(0.7, 1.0), 0.02).value,
        source="synthetic",
    )


def _synthetic_privacy(rng: Random) -> PrivacyReport:
    contains_pii = rng.random() < 0.05
    comment = None if not contains_pii else "Synthetic PII for demonstration"
    return PrivacyReport(contains_pii=contains_pii, comments=comment)


def _synthetic_audit(req: Stage0Request, rng: Random) -> AuditBlock:
    items = [
        ExplainItem(feature="lat", value=req.location.lat, explanation="Provided by request"),
        ExplainItem(feature="lon", value=req.location.lon, explanation="Provided by request"),
    ]
    return AuditBlock(items=items, version="0.1")


def _synthetic_subsurface(_: Random) -> SubsurfaceStub:
    # Currently just return a default message; placeholder for future models.
    return SubsurfaceStub()


# ---------------------------------------------------------------------------
# Public API ----------------------------------------------------------------
# ---------------------------------------------------------------------------

def build_site_context(req: Stage0Request) -> SiteContext:
    """Build a :class:`SiteContext` for ``req``.

    The function checks an in-memory cache keyed by location and scenario.  If a
    cached value exists it is returned, otherwise a new context is generated and
    stored.
    """

    key = f"{req.location.lat:.4f},{req.location.lon:.4f}:{req.climate_scenario}"
    cached = CTX_CACHE.get(key)
    if cached is not None:
        return cached

    rng = _seed(req.location)
    ctx = SiteContext(
        request=req,
        risk=_synthetic_climate(rng, req.climate_scenario),
        zoning=_synthetic_zoning(rng),
        data_quality=_synthetic_data_quality(rng),
        privacy=_synthetic_privacy(rng),
        audit=_synthetic_audit(req, rng),
        subsurface=_synthetic_subsurface(rng),
    )

    CTX_CACHE[key] = ctx
    return ctx

