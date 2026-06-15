from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class OutcomeOdds:
    label: str
    platform: str
    odds: float


@dataclass(frozen=True)
class SurebetOpportunity:
    match: str
    market: str
    outcomes: tuple[OutcomeOdds, ...]
    margin: float
    profit_pct: float
    stakes: dict[str, float]
    guaranteed_profit: float


def implied_probability(odds: float) -> float:
    if odds <= 1.0:
        raise ValueError(f"Invalid odds: {odds}")
    return 1.0 / odds


def calculate_margin(odds_list: Iterable[float]) -> float:
    total = sum(implied_probability(o) for o in odds_list)
    return 1.0 - total


def calculate_stakes_for_surebet(
    outcomes: list[OutcomeOdds], bankroll: float
) -> dict[str, float]:
    inv_sum = sum(implied_probability(o.odds) for o in outcomes)
    stakes: dict[str, float] = {}
    for o in outcomes:
        key = f"{o.platform}:{o.label}"
        stakes[key] = round(bankroll * implied_probability(o.odds) / inv_sum, 4)
    return stakes


def find_surebets(
    match: str,
    market: str,
    outcomes: list[OutcomeOdds],
    bankroll: float = 100.0,
    min_profit_pct: float = 0.1,
) -> SurebetOpportunity | None:
    if len(outcomes) < 2:
        return None

    margin = calculate_margin(o.odds for o in outcomes)
    profit_pct = margin * 100

    if profit_pct < min_profit_pct:
        return None

    stakes = calculate_stakes_for_surebet(outcomes, bankroll)
    min_return = min(stakes[k] * o.odds for k, o in zip(stakes, outcomes))
    guaranteed_profit = round(min_return - bankroll, 4)

    return SurebetOpportunity(
        match=match,
        market=market,
        outcomes=tuple(outcomes),
        margin=round(margin, 6),
        profit_pct=round(profit_pct, 4),
        stakes=stakes,
        guaranteed_profit=guaranteed_profit,
    )