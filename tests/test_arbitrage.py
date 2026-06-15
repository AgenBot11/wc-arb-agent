import pytest

from core.arbitrage import OutcomeOdds, calculate_margin, find_surebets
from core.middle import MiddleLeg, analyze_middle
from core.stakes import calculate_stakes


def test_calculate_margin_no_arb():
    margin = calculate_margin([1.90, 3.40, 4.75])
    assert margin < 0


def test_surebet_detected():
    outcomes = [
        OutcomeOdds("Home", "stake", 2.10),
        OutcomeOdds("Draw", "cloudbet", 3.60),
        OutcomeOdds("Away", "bcgame", 4.50),
    ]
    opp = find_surebets("Test vs Match", "1x2", outcomes, bankroll=100, min_profit_pct=0.1)
    assert opp is not None
    assert opp.profit_pct > 0
    assert abs(sum(opp.stakes.values()) - 100) < 0.01


def test_middle_one_goal_win():
    opp = analyze_middle(
        "France vs Senegal",
        MiddleLeg("stake", "France -1.0", -1.0, 1.90),
        MiddleLeg("cloudbet", "Senegal +1.5", 1.5, 1.95),
        total_stake=7.0,
    )
    assert opp.middle_profit > 0
    assert opp.stake_a + opp.stake_b == 7.0


def test_stake_plans_sum_to_bankroll():
    legs = [("stake", "France", 1.90), ("cloudbet", "Senegal +1.5", 1.95)]
    plans = calculate_stakes(legs, bankroll=7.0)
    assert abs(sum(p.stake for p in plans) - 7.0) < 0.01