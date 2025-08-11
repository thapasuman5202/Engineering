"""Simple Redis-backed caching helpers."""

from __future__ import annotations

import os
import random
import time
from typing import Optional

try:
    import redis  # type: ignore
except Exception:  # pragma: no cover
    redis = None  # type: ignore

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

if redis is not None:  # pragma: no branch
    try:
        _redis = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        _redis.ping()
    except Exception:  # pragma: no cover
        _redis = None
else:  # pragma: no cover
    _redis = None

_memory_cache: dict[str, tuple[str, float]] = {}


def get(key: str) -> Optional[str]:
    """Retrieve a cached string value, if present and not expired."""
    if _redis is not None:
        try:
            return _redis.get(key)
        except Exception:  # pragma: no cover
            return None
    val = _memory_cache.get(key)
    if not val:
        return None
    data, exp = val
    if exp < time.time():
        _memory_cache.pop(key, None)
        return None
    return data


def set(key: str, value: str, ttl: Optional[int] = None) -> None:
    """Store a string value with a TTL between 15 and 60 minutes."""
    ttl = ttl or random.randint(900, 3600)
    if _redis is not None:
        try:
            _redis.setex(key, ttl, value)
            return
        except Exception:  # pragma: no cover
            pass
    _memory_cache[key] = (value, time.time() + ttl)
