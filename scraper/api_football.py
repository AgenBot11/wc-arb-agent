"""Live fixtures and events from API-Football with cache + stale fallback."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from config_loader import load_config
from registration import registration_url_for
from scraper.cache import get_cached, get_cached_stale, set_cached

FIXTURES_TTL = 300
STALE_MAX_AGE = 7200


@dataclass
class LiveFixture:
    fixture_id: int
    match: str
    status: str
    minute: int
    score: str
    league: str


def fetch_live_fixtures(league_id: int = 1) -> tuple[list[LiveFixture], dict]:
    """league_id=1 is World Cup in API-Football; adjust per season."""
    meta: dict = {"source": "api_football", "cached": False, "stale": False, "errors": []}
    cfg = load_config()
    api_key = cfg.get("api_football", {}).get("key", "")
    base = cfg.get("api_football", {}).get("base_url", "https://v3.football.api-sports.io")
    if not api_key or "YOUR_" in api_key.upper():
        meta["errors"].append(
            "Missing api_football.key (optional) — register: "
            f"{registration_url_for('api_football', 'https://dashboard.api-football.com/register')} "
            "→ login → copy API Key from dashboard (no separate World Cup product)"
        )
        return [], meta

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    cache_key = f"fixtures_{today}_{league_id}"

    cached = get_cached(cache_key, ttl_sec=FIXTURES_TTL)
    if cached is not None:
        meta["cached"] = True
        return _parse_fixtures(cached), meta

    try:
        import httpx
    except ImportError:
        meta["errors"].append("Install httpx: pip install httpx")
        return _stale_fixtures(cache_key, meta)

    headers = {"x-apisports-key": api_key}
    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(
                f"{base}/fixtures",
                headers=headers,
                params={"date": today, "timezone": "UTC"},
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        meta["errors"].append(str(e))
        return _stale_fixtures(cache_key, meta)

    response = data.get("response", [])
    set_cached(cache_key, response)
    meta["fixture_count"] = len(response)
    return _parse_fixtures(response), meta


def _stale_fixtures(cache_key: str, meta: dict) -> tuple[list[LiveFixture], dict]:
    stale_data, age = get_cached_stale(cache_key, max_age_sec=STALE_MAX_AGE)
    if stale_data:
        meta["stale"] = True
        meta["stale_age_sec"] = age
        meta["errors"].append(f"API unavailable — using stale cache ({age}s old)")
        return _parse_fixtures(stale_data), meta
    return [], meta


def _parse_fixtures(response: list) -> list[LiveFixture]:
    fixtures: list[LiveFixture] = []
    for item in response:
        fix = item.get("fixture", {})
        teams = item.get("teams", {})
        goals = item.get("goals", {})
        status = fix.get("status", {})
        home = teams.get("home", {}).get("name", "")
        away = teams.get("away", {}).get("name", "")
        fixtures.append(
            LiveFixture(
                fixture_id=fix.get("id", 0),
                match=f"{home} vs {away}",
                status=status.get("long", ""),
                minute=int(status.get("elapsed") or 0),
                score=f"{goals.get('home', 0)}-{goals.get('away', 0)}",
                league=item.get("league", {}).get("name", ""),
            )
        )
    return fixtures


def fetch_fixture_events(fixture_id: int) -> list[dict]:
    cfg = load_config()
    api_key = cfg.get("api_football", {}).get("key", "")
    base = cfg.get("api_football", {}).get("base_url", "https://v3.football.api-sports.io")
    if not api_key or "YOUR_" in api_key.upper():
        return []

    cache_key = f"fixture_events_{fixture_id}"
    cached = get_cached(cache_key, ttl_sec=60)
    if cached is not None:
        return cached

    try:
        import httpx
    except ImportError:
        return []

    headers = {"x-apisports-key": api_key}
    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(
                f"{base}/fixtures/events",
                headers=headers,
                params={"fixture": fixture_id},
            )
            resp.raise_for_status()
            events = resp.json().get("response", [])
            set_cached(cache_key, events)
            return events
    except Exception:
        stale, _ = get_cached_stale(cache_key, max_age_sec=STALE_MAX_AGE)
        return stale if isinstance(stale, list) else []