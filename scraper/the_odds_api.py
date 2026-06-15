"""Fetch World Cup odds from The-Odds-API with cache, retry, and parallel sports."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from config_loader import load_config
from registration import registration_url_for
from scraper.base import MarketOdds, OddsSnapshot, PlatformOdds
from scraper.cache import get_cached, get_cached_stale, set_cached

SPORT_KEYS = [
    "soccer_fifa_world_cup",
    "soccer_fifa_world_cup_qualification_concaf",
]
REGIONS = "eu,uk,us,au"
MARKETS = "h2h,spreads,totals"
CACHE_TTL = 90
STALE_MAX_AGE = 3600


def _fetch_sport(client, api_key: str, sport: str) -> tuple[str, list, str | None, str | None]:
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "apiKey": api_key,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": "decimal",
    }
    last_err = None
    for attempt in range(3):
        try:
            resp = client.get(url, params=params)
            credits = resp.headers.get("x-requests-remaining")
            if resp.status_code == 404:
                return sport, [], credits, None
            resp.raise_for_status()
            return sport, resp.json(), credits, None
        except Exception as e:
            last_err = str(e)
            if attempt == 2:
                return sport, [], None, last_err
    return sport, [], None, last_err


def fetch_live_odds(use_cache: bool = True) -> tuple[list[OddsSnapshot], dict]:
    meta: dict = {"source": "the_odds_api", "cached": False, "stale": False, "errors": []}
    cfg = load_config()
    api_key = cfg.get("the_odds_api", {}).get("key", "")
    if not api_key or "YOUR_" in api_key.upper():
        meta["errors"].append(
            f"Missing the_odds_api.key — register: {registration_url_for('the_odds_api', 'https://the-odds-api.com/#get-access')}"
        )
        return [], meta

    cache_key = f"odds_merged_{'_'.join(SPORT_KEYS)}_{REGIONS}"
    if use_cache:
        cached = get_cached(cache_key, ttl_sec=CACHE_TTL)
        if cached is not None:
            meta["cached"] = True
            return _parse_events(cached), meta

    try:
        import httpx
    except ImportError:
        meta["errors"].append("Install httpx: pip install httpx")
        return _stale_fallback(cache_key, meta)

    all_events: list = []
    credits_remaining = None
    sports_hit: list[str] = []

    with httpx.Client(timeout=30) as client:
        with ThreadPoolExecutor(max_workers=len(SPORT_KEYS)) as pool:
            futures = {
                pool.submit(_fetch_sport, client, api_key, sport): sport for sport in SPORT_KEYS
            }
            for future in as_completed(futures):
                sport, events, credits, err = future.result()
                if credits:
                    credits_remaining = credits
                if err:
                    meta["errors"].append(f"{sport}: {err}")
                if events:
                    sports_hit.append(sport)
                    all_events.extend(events)

    if all_events:
        set_cached(cache_key, all_events)
        meta["sport"] = ",".join(sports_hit)
        meta["credits_remaining"] = credits_remaining
        meta["event_count"] = len(all_events)
        return _parse_events(all_events), meta

    return _stale_fallback(cache_key, meta)


def _stale_fallback(cache_key: str, meta: dict) -> tuple[list[OddsSnapshot], dict]:
    stale_data, age = get_cached_stale(cache_key, max_age_sec=STALE_MAX_AGE)
    if stale_data:
        meta["stale"] = True
        meta["stale_age_sec"] = age
        meta["errors"].append(f"API unavailable — using stale cache ({age}s old)")
        return _parse_events(stale_data), meta
    if not meta["errors"]:
        meta["errors"].append("No live odds returned")
    return [], meta


def _parse_events(events: list) -> list[OddsSnapshot]:
    snapshots: list[OddsSnapshot] = []
    seen_matches: set[str] = set()

    for event in events:
        home = event.get("home_team", "")
        away = event.get("away_team", "")
        match_name = f"{home} vs {away}"
        norm = match_name.lower()
        if norm in seen_matches:
            continue

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
                        side = "Over" if name.lower() in ("over", "o") else "Under"
                        markets.append(MarketOdds("totals", f"{side} {point}", price))
            if markets:
                platform_map.setdefault(platform, []).extend(markets)

        platforms = [
            PlatformOdds(platform=p, match=match_name, markets=ms)
            for p, ms in platform_map.items()
        ]
        if len(platforms) >= 2:
            snapshots.append(OddsSnapshot(match=match_name, platforms=platforms))
            seen_matches.add(norm)
    return snapshots


def _normalize_platform(name: str) -> str:
    lower = name.lower().replace(" ", "").replace("_", "")
    aliases = {
        "stake": "stake",
        "cloudbet": "cloudbet",
        "bcgame": "bcgame",
        "bet365": "bet365",
        "pinnacle": "pinnacle",
        "draftkings": "draftkings",
        "fanduel": "fanduel",
        "williamhill": "williamhill",
        "betfair": "betfair",
        "unibet": "unibet",
    }
    for key, val in aliases.items():
        if key in lower:
            return val
    return lower[:24] or "unknown"