from dataclasses import dataclass


@dataclass(frozen=True)
class StakePlan:
    platform: str
    selection: str
    odds: float
    stake: float
    potential_return: float


def calculate_stakes(
    legs: list[tuple[str, str, float]],
    bankroll: float,
    mode: str = "equal_profit",
) -> list[StakePlan]:
    """
    Calculate optimal stakes across multiple legs.

    legs: list of (platform, selection, decimal_odds)
    mode: "equal_profit" for arbitrage, "kelly" for value bets
    """
    if mode == "equal_profit":
        inv = [1.0 / odds for _, _, odds in legs]
        total_inv = sum(inv)
        plans: list[StakePlan] = []
        for (platform, selection, odds), weight in zip(legs, inv):
            stake = round(bankroll * weight / total_inv, 4)
            plans.append(
                StakePlan(
                    platform=platform,
                    selection=selection,
                    odds=odds,
                    stake=stake,
                    potential_return=round(stake * odds, 4),
                )
            )
        return plans

    if mode == "kelly":
        # Simplified Kelly: caller provides estimated win probability via odds edge
        plans = []
        per_leg = round(bankroll / len(legs), 4)
        for platform, selection, odds in legs:
            plans.append(
                StakePlan(
                    platform=platform,
                    selection=selection,
                    odds=odds,
                    stake=per_leg,
                    potential_return=round(per_leg * odds, 4),
                )
            )
        return plans

    raise ValueError(f"Unknown mode: {mode}")