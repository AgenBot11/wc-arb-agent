"""Live fixtures and events from API-Football."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from config_loader import load_config


@dataclass
class LiveFixture:
    fixture_id: int
    match: str
    status: str
    minute: int
    score: str
    league: str


def fetch_live_fixtures(league_id: int = 1) -> list[LiveFixture]:
    """league_id=1 is World Cup in API-Football; adjust per season."""
    cfg = load_config()
    api_key = cfg.get("api_football", {}).get("key", "")
    base = cfg.get("api_football", {}).get("base_url", "https://v3.football.api-sports.io")
    if not api_key or "YOUR_" in api_key:
        return []

    try:
        import httpx
    except ImportError:
        return []

    headers = {"x-apisports-key": api_key}
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    with httpx.Client(timeout=30) as client:
        resp = client.get(
            f"{base}/fixtures",
            headers=headers,
            params={"date": today, "timezone": "UTC"},
        )
        resp.raise_for_status()
        data = resp.json()

    fixtures: list[LiveFixture] = []
    for item in data.get("response", []):
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
    if not api_key or "YOUR_" in api_key:
        return []

    try:
        import httpx
    except ImportError:
        return []

    headers = {"x-apisports-key": api_key}
    with httpx.Client(timeout=30) as client:
        resp = client.get(
            f"{base}/fixtures/events",
            headers=headers,
            params={"fixture": fixture_id},
        )
        resp.raise_for_status()
        return resp.json().get("response", [])