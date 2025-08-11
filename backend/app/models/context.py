from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


class LatLon(BaseModel):
    """Simple latitude / longitude pair."""

    lat: float
    lon: float


class UQNumber(BaseModel):
    """Numeric value with optional uncertainty and unit."""

    value: float
    uncertainty: Optional[float] = None
    unit: Optional[str] = None


class ClimateScen(str, Enum):
    """Climate scenario identifiers."""

    HISTORICAL = "historical"
    SSP126 = "ssp1_2.6"
    SSP245 = "ssp2_4.5"
    SSP585 = "ssp5_8.5"


class RiskScores(BaseModel):
    """Collection of risk related scores."""

    exposure: Optional[float] = None
    damage: Optional[float] = None
    score: Optional[float] = None


class ZoningDrift(BaseModel):
    """Represents drift or deviation in zoning predictions."""

    compliant: bool = True
    message: Optional[str] = None


class DataQuality(BaseModel):
    """Metadata describing data quality metrics."""

    completeness: Optional[float] = None
    accuracy: Optional[float] = None
    source: Optional[str] = None


class Lineage(BaseModel):
    """Track provenance of data used in analysis."""

    source: str
    retrieved: Optional[str] = None
    notes: Optional[str] = None


class PrivacyReport(BaseModel):
    """Information about privacy considerations for a dataset."""

    contains_pii: bool = False
    comments: Optional[str] = None


class SubsurfaceStub(BaseModel):
    """Placeholder for subsurface analysis results."""

    message: str = "No subsurface data available."


class ExplainItem(BaseModel):
    """One explanatory item for model output."""

    feature: str
    value: Optional[Union[float, int, str]] = None
    explanation: Optional[str] = None


class AuditBlock(BaseModel):
    """Set of explanatory items with optional versioning."""

    items: List[ExplainItem] = []
    version: Optional[str] = None


class Stage0Request(BaseModel):
    """Input request structure for stage 0 processing."""

    location: LatLon
    climate_scenario: Optional[ClimateScen] = ClimateScen.HISTORICAL
    lineage: Optional[Lineage] = None


class SiteContext(BaseModel):
    """Aggregated context for a site including risk and metadata."""

    request: Stage0Request
    risk: Optional[RiskScores] = None
    zoning: Optional[ZoningDrift] = None
    data_quality: Optional[DataQuality] = None
    privacy: Optional[PrivacyReport] = None
    audit: Optional[AuditBlock] = None
    subsurface: Optional[SubsurfaceStub] = None
