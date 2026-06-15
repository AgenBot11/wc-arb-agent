"""Fetch World Cup odds from The-Odds-API (optional live source)."""

from __future__ import annotations

from config_loader import load_config
from scraper.base import MarketOdds, OddsSnapshot, PlatformOdds


SPORT = "soccer_fifa_world_cup"
REGIONS = "eu,uk,us"
MARKETS = "h2h,spreads,totals"


def fetch_live_odds() -> list[OddsSnapshot]:
    cfg = load_config()
    api_key = cfg.get("the_odds_api", {}).get("key", "")
    if not api_key or "YOUR_" in api_key:
        return []

    try:
        import httpx
    except ImportError:
        return []

    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"
    params = {"apiKey": api_key, "regions": REGIONS, "markets": MARKETS, "oddsFormat": "decimal"}

    with httpx.Client(timeout=30) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        events = resp.json()

    snapshots: list[OddsSnapshot] = []
    for event in events:
        home = event.get("home_team", "")
        away = event.get("away_team", "")
        match_name = f"{home} vs {away}"
        platform_map: dict[str, list[MarketOdds]] = {}

        for bookmaker in event.get("bookmakers", []):
            platform = _normalize_platform(bookmaker.get("key", bookmaker.get("title", "unknown")))
            markets: list[MarketOdds] = []
            for market in bookmaker.get("markets", []):
                key = market.get("key", "")
                for outcome in market.get("outcomes", []):
                    name = outcome.get("name", "")
                    price = float(outcome.get("price", 0))
                    point = outcome.get("point")
                    if price <= 1:
                        continue
                    if key == "h2h":
                        markets.append(MarketOdds("1x2", name, price))
                    elif key == "spreads" and point is not None:
                        label = f"{name} {point:+.1f}"
                        markets.append(MarketOdds("asian_handicap", label, price, float(point)))
                    elif key == "totals" and point is not None:
                        side = "Over" if "Over" in name or name.lower() == "over" else "Under"
                        markets.append(MarketOdds("totals", f"{side} {point}", price))
            if markets:
                platform_map.setdefault(platform, []).extend(markets)

        platforms = [
            PlatformOdds(platform=p, match=match_name, markets=ms)
            for p, ms in platform_map.items()
        ]
        if len(platforms) >= 2:
            snapshots.append(OddsSnapshot(match=match_name, platforms=platforms))

    return snapshots


def _normalize_platform(name: str) -> str:
    lower = name.lower().replace(" ", "")
    aliases = {
        "stake": "stake",
        "cloudbet": "cloudbet",
        "bcgame": "bcgame",
        "bet365": "bet365",
        "pinnacle": "pinnacle",
        "draftkings": "draftkings",
        "fanduel": "fanduel",
    }
    for key, val in aliases.items():
        if key in lower:
            return val
    return lower[:24] or "unknown"