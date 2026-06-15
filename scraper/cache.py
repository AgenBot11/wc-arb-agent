"""Simple JSON file cache to reduce API quota usage."""

from __future__ import annotations

import json
import time
from hashlib import md5
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"


def _cache_path(key: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{md5(key.encode()).hexdigest()}.json"


def _read_payload(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def get_cached(key: str, ttl_sec: int = 90) -> dict | list | None:
    payload = _read_payload(_cache_path(key))
    if payload is None:
        return None
    if time.time() - payload.get("_ts", 0) > ttl_sec:
        return None
    return payload.get("data")


def get_cached_stale(key: str, max_age_sec: int = 3600) -> tuple[dict | list | None, int | None]:
    """Return cached data even if TTL expired, up to max_age_sec."""
    payload = _read_payload(_cache_path(key))
    if payload is None:
        return None, None
    age = int(time.time() - payload.get("_ts", 0))
    if age > max_age_sec:
        return None, None
    return payload.get("data"), age


def set_cached(key: str, data: dict | list) -> None:
    path = _cache_path(key)
    path.write_text(
        json.dumps({"_ts": time.time(), "data": data}, ensure_ascii=False),
        encoding="utf-8",
    )