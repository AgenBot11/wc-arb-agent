"""Scan demo or live odds snapshots for surebets and middles."""

from core.arbitrage import OutcomeOdds, find_surebets
from core.middle import MiddleLeg, find_middle_opportunities
from scraper.aggregate import get_all_snapshots
from scraper.base import OddsSnapshot


def _scan_snapshots(
    snapshots: list[OddsSnapshot],
    bankroll: float,
    min_profit_pct: float,
) -> tuple[list, list]:
    surebets = []
    middles = []

    for snapshot in snapshots:
        for market in ("1x2",):
            selections: dict[str, OutcomeOdds] = {}
            for platform in snapshot.platforms:
                for m in platform.markets:
                    if m.market == market:
                        key = m.selection
                        if key not in selections or m.odds > selections[key].odds:
                            selections[key] = OutcomeOdds(
                                label=key,
                                platform=platform.platform,
                                odds=m.odds,
                            )
            if len(selections) >= 2:
                opp = find_surebets(
                    match=snapshot.match,
                    market=market,
                    outcomes=list(selections.values()),
                    bankroll=bankroll,
                    min_profit_pct=min_profit_pct,
                )
                if opp:
                    surebets.append(opp)

        favorites = []
        underdogs = []
        for platform in snapshot.platforms:
            for m in platform.markets:
                if m.market == "asian_handicap" and m.handicap is not None:
                    if m.handicap < 0:
                        favorites.append(
                            MiddleLeg(platform.platform, m.selection, m.handicap, m.odds)
                        )
                    elif m.handicap > 0:
                        underdogs.append(
                            MiddleLeg(platform.platform, m.selection, m.handicap, m.odds)
                        )
        if favorites and underdogs:
            middles.extend(
                find_middle_opportunities(snapshot.match, favorites, underdogs, bankroll)
            )

    return surebets, middles


def scan_surebets(
    bankroll: float = 7.0,
    min_profit_pct: float = 0.0,
    source: str = "demo",
) -> list:
    snapshots, _ = get_all_snapshots(source)
    surebets, _ = _scan_snapshots(snapshots, bankroll, min_profit_pct)
    return surebets


def scan_middles(bankroll: float = 7.0, source: str = "demo") -> list:
    snapshots, _ = get_all_snapshots(source)
    _, middles = _scan_snapshots(snapshots, bankroll, 0.0)
    return middles


def scan_all(
    bankroll: float = 7.0,
    min_profit_pct: float = 0.0,
    source: str = "demo",
) -> tuple[list, list, dict]:
    snapshots, meta = get_all_snapshots(source)
    surebets, middles = _scan_snapshots(snapshots, bankroll, min_profit_pct)
    meta["snapshot_count"] = len(snapshots)
    return surebets, middles, meta