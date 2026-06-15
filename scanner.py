"""Scan demo or live odds snapshots for surebets and middles."""

from core.arbitrage import OutcomeOdds, find_surebets
from core.middle import MiddleLeg, find_middle_opportunities
from scraper.demo_data import get_demo_world_cup_odds


def scan_surebets(bankroll: float = 7.0, min_profit_pct: float = 0.0) -> list:
    opportunities = []
    for snapshot in get_demo_world_cup_odds():
        for market in ("1x2",):
            selections = {}
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
                    opportunities.append(opp)
    return opportunities


def scan_middles(bankroll: float = 7.0) -> list:
    opportunities = []
    for snapshot in get_demo_world_cup_odds():
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
            opportunities.extend(
                find_middle_opportunities(snapshot.match, favorites, underdogs, bankroll)
            )
    return opportunities