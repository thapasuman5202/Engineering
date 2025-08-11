from __future__ import annotations

from time import perf_counter
from math import sin, cos, pi
import hashlib, json, random
from typing import Dict, List, Optional

from shapely.geometry import shape, Polygon, mapping

from ..models.context import (
    AuditBlock,
    ClimateScen,
    DataQuality,
    ExplainItem,
    LatLon,
    Lineage,
    PrivacyReport,
    RiskScores,
    SiteContext,
    Stage0Request,
    SubsurfaceStub,
    ZoningDrift,
    UQNumber,
)


CTX_CACHE: Dict[str, SiteContext] = {}


def _seed(lat: float, lon: float) -> random.Random:
    key = f"{round(lat,5)},{round(lon,5)}"
    h = hashlib.sha256(key.encode()).hexdigest()
    seed = int(h[:16], 16)
    return random.Random(seed)


def _with_uq(x: float, src: str, band: float = 0.15) -> UQNumber:
    low = x * (1 - band)
    high = x * (1 + band)
    return UQNumber(value=x, ci95_low=max(0.0, low), ci95_high=max(low, high), source=src)


def _buffer_circle_geojson(lat: float, lon: float, radius_m: int) -> dict:
    segments = 64
    dlat = radius_m / 111320.0
    dlon = radius_m / (111320.0 * max(0.0001, cos(lat * pi / 180)))
    points = []
    for i in range(segments):
        ang = 2 * pi * i / segments
        points.append([
            lon + dlon * cos(ang),
            lat + dlat * sin(ang),
        ])
    points.append(points[0])
    return {"type": "Polygon", "coordinates": [points]}


def _bbox_from_geojson(gj: dict) -> List[float]:
    geom = shape(gj)
    minx, miny, maxx, maxy = geom.bounds
    return [minx, miny, maxx, maxy]


def _wind_index_from_lat(lat: float) -> float:
    return (cos(lat * pi / 180) + 1) / 2


def _synthetic_climate(r: random.Random, lat: float, lon: float) -> Dict[str, UQNumber]:
    jitter = r.uniform(-1, 1)
    avg_temp_c = 30 - abs(lat) / 3 + jitter
    rain_jitter = r.uniform(-50, 50)
    annual_rain_mm = 1200 + 400 * sin(lat * pi / 180) + rain_jitter
    hdd = max(0.0, 2000 - avg_temp_c * 50)
    cdd = max(0.0, avg_temp_c * 40 - 400)
    wind_index = _wind_index_from_lat(lat)
    return {
        "avg_temp_c": _with_uq(avg_temp_c, "climate"),
        "annual_rain_mm": _with_uq(annual_rain_mm, "climate"),
        "hdd": _with_uq(hdd, "climate"),
        "cdd": _with_uq(cdd, "climate"),
        "wind_index": _with_uq(wind_index, "climate"),
    }


def _synthetic_environment(r: random.Random) -> Dict[str, UQNumber]:
    elev = r.uniform(0, 2500)
    slope = r.uniform(0, 15)
    greenspace = r.uniform(0.05, 0.6)
    water = r.uniform(0.0, 0.1)
    return {
        "elev_m_mean": _with_uq(elev, "env"),
        "slope_deg_mean": _with_uq(slope, "env"),
        "greenspace_pct": _with_uq(greenspace, "env"),
        "water_pct": _with_uq(water, "env"),
    }


def _synthetic_mobility(r: random.Random) -> Dict[str, UQNumber]:
    road = r.uniform(1, 10)
    inter = r.uniform(20, 200)
    transit = r.uniform(0, 30)
    walk = max(0.0, min(100.0, road * 5 + inter / 2))
    return {
        "road_km_per_km2": _with_uq(road, "mob"),
        "intersection_density": _with_uq(inter, "mob"),
        "transit_stops": _with_uq(transit, "mob"),
        "walkability_0_100": _with_uq(walk, "mob"),
    }


def _synthetic_socio(r: random.Random, mobility: Dict[str, UQNumber]) -> Dict[str, UQNumber]:
    pop = r.uniform(500, 20000)
    income = r.uniform(0.3, 0.9)
    pop_norm = (pop - 500) / 19500
    walk = mobility["walkability_0_100"].value / 100
    gent = max(0.0, min(1.0, (walk + pop_norm) / 2))
    return {
        "pop_density_km2": _with_uq(pop, "socio"),
        "median_income_index": _with_uq(income, "socio"),
        "gentrification_risk_0_1": _with_uq(gent, "socio"),
    }


def _derive_constraints_and_zoning(mobility: Dict[str, UQNumber], socio: Dict[str, UQNumber]) -> tuple[List[str], str]:
    pop = socio["pop_density_km2"].value
    walk = mobility["walkability_0_100"].value
    constraints: List[str] = []
    zoning = "R1"
    if pop > 10000 and walk > 70:
        zoning = "MU3"
        constraints = ["setback 5m", "max_height 30m"]
    elif pop > 5000 and walk > 60:
        zoning = "MU2"
        constraints = ["setback 3m", "max_height 20m"]
    return constraints, zoning


def _scenario_pack(r: random.Random, base_climate: Dict[str, UQNumber], scenarios: List[str]) -> Dict[str, ClimateScen]:
    avg_temp = base_climate["avg_temp_c"].value
    heat_base = max(1.0, avg_temp)
    flood_base = max(5.0, 100 - base_climate["annual_rain_mm"].value / 50)
    res: Dict[str, ClimateScen] = {}
    for scen in scenarios:
        if scen == "baseline":
            heat = heat_base
            flood = flood_base
        elif scen == "RCP4.5":
            heat = heat_base * 1.4
            flood = flood_base * 0.9
        elif scen == "RCP8.5":
            heat = heat_base * 1.9
            flood = flood_base * 0.75
        else:
            continue
        res[scen] = ClimateScen(
            heatwave_days=_with_uq(heat, "scenario"),
            flood_return_yr=_with_uq(flood, "scenario"),
        )
    return res


def _risk_scores(climate: Dict[str, UQNumber], environment: Dict[str, UQNumber]) -> RiskScores:
    flood = int(min(100, environment["water_pct"].value * 800))
    heat = int(min(100, climate["avg_temp_c"].value * 3 - environment["greenspace_pct"].value * 50))
    quake = 50
    pollution = int(min(100, 60 - environment["greenspace_pct"].value * 50))
    return RiskScores(flood_0_100=flood, quake_0_100=quake, heat_0_100=heat, pollution_0_100=pollution)


def _zoning_drift(brief: str, mobility: Dict[str, UQNumber], socio: Dict[str, UQNumber]) -> ZoningDrift:
    walk = mobility["walkability_0_100"].value
    p_change = 0.05
    p_upzone = 0.1
    label = "no_change"
    explain = "stable"
    if "mixed-use" in brief.lower() and walk > 70:
        p_upzone = 0.3
        explain = "mixed-use interest with good walkability"
    return ZoningDrift(p_change_1y=p_change, p_upzone_3y=p_upzone, label_1y=label, explain=explain)


def _design_objectives(brief: str, risk: RiskScores) -> List[str]:
    objs: List[str] = []
    if risk.heat_0_100 > 40:
        objs.append("maximize natural cooling days")
    if "mixed-use" in brief.lower():
        objs.append("integrate mixed-use zoning")
    return objs


def _explain(fields: Dict[str, float]) -> List[ExplainItem]:
    items = []
    if "walkability" in fields:
        items.append(ExplainItem(feature="walkability", why="high walkability supports transit"))
    if "zoning_hint" in fields:
        items.append(ExplainItem(feature="zoning_hint", why=f"zoning suggested {fields['zoning_hint']}"))
    if "greenspace_pct" in fields:
        items.append(ExplainItem(feature="greenspace_pct", why="greenspace moderates heat/pollution"))
    return items


def _audit_hash(request_json: dict) -> str:
    data = json.dumps(request_json, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()


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


def build_site_context(req: Stage0Request) -> SiteContext:
    t0 = perf_counter()
    assert (req.boundary_geojson is not None) or (req.lat is not None and req.lon is not None), "Provide lat/lon or boundary_geojson"

    if req.boundary_geojson is None:
        boundary = _buffer_circle_geojson(req.lat, req.lon, req.radius_m)
    else:
        boundary = req.boundary_geojson
    bbox = _bbox_from_geojson(boundary)

    rnd = _seed(req.lat or (bbox[1] + bbox[3]) / 2, req.lon or (bbox[0] + bbox[2]) / 2)

    climate = _synthetic_climate(rnd, req.lat or 0.0, req.lon or 0.0)
    environment = _synthetic_environment(rnd)
    mobility = _synthetic_mobility(rnd)
    socio = _synthetic_socio(rnd, mobility)

    constraints, zoning_hint = _derive_constraints_and_zoning(mobility, socio)
    scen = _scenario_pack(rnd, climate, req.scenarios)
    risks = _risk_scores(climate, environment)
    zoning_drift = _zoning_drift(req.brief or "", mobility, socio)
    objectives = _design_objectives(req.brief or "", risks)

    dq = DataQuality(
        online=req.online,
        sources=["offline_synthetic_v2"] if not req.online else ["offline_synthetic_v2", "online_stubs"],
        notes="deterministic proxies" if not req.online else "deterministic proxies (online flagged)",
    )
    lineage = {
        "climate": Lineage(source_id="syn-v2", license="MIT-like", transform="latlon-seeded"),
        "environment": Lineage(source_id="syn-v2", license="MIT-like", transform="seeded-noise"),
        "mobility": Lineage(source_id="syn-v2", license="MIT-like", transform="derived"),
        "socio_econ": Lineage(source_id="syn-v2", license="MIT-like", transform="derived"),
    }
    privacy = PrivacyReport(pii_found=False, fields=[])

    centroid = LatLon(lat=(req.lat if req.lat is not None else (bbox[1] + bbox[3]) / 2),
                      lon=(req.lon if req.lon is not None else (bbox[0] + bbox[2]) / 2))

    subsurface = SubsurfaceStub(
        utility_density_hint="medium" if mobility["intersection_density"].value > 70 else "low",
        void_risk_hint="low",
        voxels_overview={"occupied": int(rnd.uniform(100, 200)), "empty": int(rnd.uniform(400, 600))},
    )

    explain = _explain({
        "walkability": mobility["walkability_0_100"].value,
        "zoning_hint": zoning_hint,
        "greenspace_pct": environment["greenspace_pct"].value,
    })
    inputs_hash = _audit_hash(json.loads(Stage0Request.model_dump_json(req)))
    duration_ms = int((perf_counter() - t0) * 1000)

    ctx = SiteContext(
        site_name=req.site_name,
        centroid=centroid,
        bbox=bbox,
        boundary_geojson=boundary,
        climate=climate,
        climate_scenarios=scen,
        environment=environment,
        mobility=mobility,
        socio_econ=socio,
        constraints=constraints,
        zoning_hint=zoning_hint,
        zoning_drift_pred=zoning_drift,
        risk_scores=risks,
        design_objectives_suggested=objectives,
        subsurface=subsurface,
        data_quality=dq,
        lineage=lineage,
        privacy_report=privacy,
        explain=explain,
        audit=AuditBlock(inputs_hash=inputs_hash, duration_ms=duration_ms, version="stage0-ultra-0.3.0"),
    )

    CTX_CACHE[ctx.context_id] = ctx
    return ctx

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
    new_ctx.design_objectives_suggested = _design_objectives("", new_ctx.risk_scores)
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
