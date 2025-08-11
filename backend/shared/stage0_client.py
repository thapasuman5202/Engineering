"""Client for retrieving Stage0 site context."""

from __future__ import annotations

import os
import httpx

from app.models.context import SiteContext

STAGE0_API_URL = os.getenv("STAGE0_API_URL", "").rstrip("/")


def fetch_context(project_id: str) -> SiteContext:
    """Fetch context from the Stage0 API for the given project id."""
    if not STAGE0_API_URL:
        raise RuntimeError("STAGE0_API_URL not set")
    url = f"{STAGE0_API_URL}/projects/{project_id}/context"
    resp = httpx.get(url, timeout=10.0)
    resp.raise_for_status()
    data = resp.json()
    return SiteContext.model_validate(data)
