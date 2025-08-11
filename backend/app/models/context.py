from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal
from uuid import uuid4
from datetime import datetime


class LatLon(BaseModel):
    lat: float
    lon: float


class UQNumber(BaseModel):
    value: float
    ci95_low: float
    ci95_high: float
    source: str


class ClimateScen(BaseModel):
    heatwave_days: UQNumber
    flood_return_yr: UQNumber


class RiskScores(BaseModel):
    flood_0_100: int
    quake_0_100: int
    heat_0_100: int
    pollution_0_100: int


class ZoningDrift(BaseModel):
    p_change_1y: float
    p_upzone_3y: float
    label_1y: Literal["no_change", "upzone", "downzone"]
    explain: str


class DataQuality(BaseModel):
    online: bool
    sources: List[str]
    notes: str


class Lineage(BaseModel):
    source_id: str
    license: str
    transform: str


class PrivacyReport(BaseModel):
    pii_found: bool
    fields: List[str] = []


class SubsurfaceStub(BaseModel):
    utility_density_hint: Literal["low", "medium", "high"]
    void_risk_hint: Literal["low", "medium", "high"]
    voxels_overview: Optional[Dict[str, int]] = None  # {"occupied":X,"empty":Y}


class ExplainItem(BaseModel):
    feature: str
    why: str


class AuditBlock(BaseModel):
    inputs_hash: str
    duration_ms: int
    version: str


class Stage0Request(BaseModel):
    site_name: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    radius_m: int = 500
    boundary_geojson: Optional[dict] = None
    brief: Optional[str] = None
    online: bool = False
    scenarios: List[str] = ["baseline"]
    horizon_years: int = 30


class SiteContext(BaseModel):
    context_id: str = Field(default_factory=lambda: str(uuid4()))
    site_name: str
    centroid: LatLon
    bbox: List[float]  # [minLon, minLat, maxLon, maxLat]
    boundary_geojson: Optional[dict]
    climate: Dict[str, UQNumber]  # avg_temp_c, annual_rain_mm, hdd, cdd, wind_index
    climate_scenarios: Dict[str, ClimateScen]
    environment: Dict[str, UQNumber]  # elev_m_mean, slope_deg_mean, greenspace_pct, water_pct
    mobility: Dict[str, UQNumber]  # road_km_per_km2, intersection_density, transit_stops, walkability_0_100
    socio_econ: Dict[str, UQNumber]  # pop_density_km2, median_income_index, gentrification_risk_0_1
    constraints: List[str]
    zoning_hint: Optional[str]
    zoning_drift_pred: ZoningDrift
    risk_scores: RiskScores
    design_objectives_suggested: List[str]
    subsurface: SubsurfaceStub
    data_quality: DataQuality
    lineage: Dict[str, Lineage]
    privacy_report: PrivacyReport
    explain: List[ExplainItem]
    audit: AuditBlock
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
