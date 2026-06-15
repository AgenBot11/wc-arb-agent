"""Aggregate odds from demo + live API sources."""

from __future__ import annotations

from scraper.base import OddsSnapshot
from scraper.demo_data import get_demo_world_cup_odds
from scraper.the_odds_api import fetch_live_odds


def get_all_snapshots(source: str = "all") -> tuple[list[OddsSnapshot], dict]:
    """
    source: demo | live | all
    Returns (snapshots, meta)
    """
    meta = {"demo_count": 0, "live_count": 0, "sources": []}
    snapshots: list[OddsSnapshot] = []

    if source in ("demo", "all"):
        demo = get_demo_world_cup_odds()
        snapshots.extend(demo)
        meta["demo_count"] = len(demo)
        meta["sources"].append("demo")

    if source in ("live", "all"):
        live = fetch_live_odds()
        snapshots.extend(live)
        meta["live_count"] = len(live)
        if live:
            meta["sources"].append("the_odds_api")
        elif source == "live":
            meta["live_error"] = "No live odds — add the_odds_api.key to config.yaml"

    return snapshots, meta