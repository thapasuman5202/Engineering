from __future__ import annotations

from time import sleep

from . import celery_app


@celery_app.task(name="workers.export.export")
def export(payload: dict) -> dict:
    """Simulate an export step."""
    data = payload
    sleep(1)
    data["exported"] = True
    return data
