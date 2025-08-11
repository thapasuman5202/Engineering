from __future__ import annotations

from time import sleep

from . import celery_app


@celery_app.task(name="workers.massing.massing")
def massing(payload: dict) -> dict:
    """Simulate a massing step."""
    data = payload
    sleep(1)
    data["massing"] = True
    return data
