from __future__ import annotations

from time import sleep

from . import celery_app


@celery_app.task(name="workers.render.render")
def render(payload: dict | None = None) -> dict:
    """Simulate a render step."""
    data = payload or {}
    sleep(1)
    data["rendered"] = True
    return data
