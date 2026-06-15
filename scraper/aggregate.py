"""Aggregate odds from demo + live API sources with smart merge."""

from __future__ import annotations

from scraper.base import OddsSnapshot, PlatformOdds
from scraper.demo_data import get_demo_world_cup_odds
from scraper.the_odds_api import fetch_live_odds


def _norm_match(name: str) -> str:
    return name.lower().replace("  ", " ").strip()


def _merge_snapshots(base: list[OddsSnapshot], extra: list[OddsSnapshot]) -> list[OddsSnapshot]:
    index: dict[str, OddsSnapshot] = {_norm_match(s.match): s for s in base}
    for snap in extra:
        key = _norm_match(snap.match)
        if key not in index:
            index[key] = snap
            continue
        existing = index[key]
        known = {p.platform for p in existing.platforms}
        for p in snap.platforms:
            if p.platform not in known:
                existing.platforms.append(p)
                known.add(p.platform)
    return list(index.values())


def get_all_snapshots(source: str = "all") -> tuple[list[OddsSnapshot], dict]:
    meta: dict = {"demo_count": 0, "live_count": 0, "sources": [], "live_meta": {}}
    snapshots: list[OddsSnapshot] = []

    if source in ("demo", "all"):
        demo = get_demo_world_cup_odds()
        snapshots = demo.copy()
        meta["demo_count"] = len(demo)
        meta["sources"].append("demo")

    if source in ("live", "all"):
        live, live_meta = fetch_live_odds()
        meta["live_meta"] = live_meta
        meta["live_count"] = len(live)
        if live:
            meta["sources"].append("the_odds_api")
            if source == "all":
                snapshots = _merge_snapshots(snapshots, live)
            else:
                snapshots = live
        elif source == "live":
            meta["live_error"] = live_meta.get("errors", ["No live odds"])[0]

    meta["snapshot_count"] = len(snapshots)
    return snapshots, meta