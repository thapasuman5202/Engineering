from __future__ import annotations

import os
from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "workers",
    broker=redis_url,
    backend=redis_url,
    include=["workers.render", "workers.massing", "workers.export"],
)

celery_app.conf.task_routes = {
    "workers.render.*": {"queue": "render"},
    "workers.massing.*": {"queue": "massing"},
    "workers.export.*": {"queue": "export"},
}

__all__ = ["celery_app"]
