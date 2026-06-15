from executor.autopilot import middle_to_orders, pick_best_opportunity, readiness_check
from executor.platform_urls import cloudbet_match_url, parse_match, stake_match_url


def test_parse_match():
    assert parse_match("France vs Senegal") == ("France", "Senegal")


def test_platform_urls():
    assert "stake.com" in stake_match_url("France vs Senegal")
    assert "cloudbet.com" in cloudbet_match_url("France vs Senegal")


def test_pick_demo_middle():
    pick = pick_best_opportunity(bankroll=7.0, source="demo", platforms=["stake", "cloudbet"])
    assert pick["type"] in ("middle", "surebet", "none")
    if pick["type"] == "middle":
        assert len(pick["orders"]) == 2
        platforms = {o.platform for o in pick["orders"]}
        assert platforms <= {"stake", "cloudbet"}


def test_middle_to_orders():
    pick = pick_best_opportunity(bankroll=7.0, source="demo", platforms=["stake", "cloudbet"])
    if pick["type"] != "middle":
        return
    orders = middle_to_orders(pick["opportunity"])
    assert orders[0].stake + orders[1].stake == 7.0


def test_readiness_check_keys():
    r = readiness_check()
    assert "sessions" in r
    assert "ready" in r