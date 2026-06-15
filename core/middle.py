from dataclasses import dataclass


@dataclass(frozen=True)
class MiddleLeg:
    platform: str
    selection: str
    handicap: float
    odds: float


@dataclass(frozen=True)
class MiddleOpportunity:
    match: str
    leg_a: MiddleLeg
    leg_b: MiddleLeg
    middle_scores: tuple[str, ...]
    stake_a: float
    stake_b: float
    middle_profit: float
    worst_case_loss: float


def _payout(stake: float, odds: float) -> float:
    return stake * odds


def _ah_result(goals_diff: int, handicap: float, stake: float, odds: float) -> float:
    """
    Asian handicap settlement for a single leg.
    goals_diff: backing team margin (positive = backing team wins by more)
    handicap: line on the backed side (e.g. -1.0 means team must win by 1+)
    """
    adjusted = goals_diff + handicap
    if adjusted > 0.25:
        return _payout(stake, odds)
    if adjusted == 0.25:
        return stake + (stake * (odds - 1) / 2)
    if adjusted == 0:
        return stake
    if adjusted == -0.25:
        return stake / 2
    return 0.0


def analyze_middle(
    match: str,
    leg_a: MiddleLeg,
    leg_b: MiddleLeg,
    total_stake: float = 7.0,
) -> MiddleOpportunity:
    """
    Classic middle: back Team -1.0 on platform A, opponent +1.5 on platform B.
    Middle hits when favorite wins by exactly 1 goal.
    """
    stake_a = round(total_stake * 0.5, 4)
    stake_b = round(total_stake - stake_a, 4)

    # favorite wins by exactly 1: leg_a half-win, leg_b full win
    middle_a = stake_a + (stake_a * (leg_a.odds - 1) / 2)
    middle_b = _payout(stake_b, leg_b.odds)
    middle_profit = round(middle_a + middle_b - total_stake, 4)

    # favorite wins by 2+
    win_big_a = _payout(stake_a, leg_a.odds)
    win_big = round(win_big_a - stake_b, 4)

    # draw or underdog win
    lose_a = 0.0
    win_b = _payout(stake_b, leg_b.odds)
    draw_loss = round(lose_a + win_b - total_stake, 4)

    worst_case = min(middle_profit, win_big, draw_loss)

    return MiddleOpportunity(
        match=match,
        leg_a=leg_a,
        leg_b=leg_b,
        middle_scores=("1-0", "2-1", "3-2"),
        stake_a=stake_a,
        stake_b=stake_b,
        middle_profit=middle_profit,
        worst_case_loss=worst_case,
    )


def find_middle_opportunities(
    match: str,
    favorites: list[MiddleLeg],
    underdogs: list[MiddleLeg],
    total_stake: float = 7.0,
    min_middle_profit: float = 0.5,
) -> list[MiddleOpportunity]:
    results: list[MiddleOpportunity] = []
    for fav in favorites:
        for dog in underdogs:
            if fav.platform == dog.platform:
                continue
            opp = analyze_middle(match, fav, dog, total_stake)
            if opp.middle_profit >= min_middle_profit:
                results.append(opp)
    return sorted(results, key=lambda x: x.middle_profit, reverse=True)