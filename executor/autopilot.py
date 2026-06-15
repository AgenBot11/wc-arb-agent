"""Autonomous scan → verify → bet pipeline."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from config_loader import load_config
from core.arbitrage import OutcomeOdds
from core.middle import MiddleOpportunity
from executor.browser_bet import BetExecutor, BetOrder
from executor.session import has_session, missing_sessions
from scanner import scan_all

ROOT = Path(__file__).resolve().parent.parent
BETS_DIR = ROOT / ".sessions" / "bets"


def _configured_platforms() -> list[str]:
    return list(load_config().get("platforms", ["stake", "cloudbet"]))


def readiness_check() -> dict:
    cfg = load_config()
    platforms = _configured_platforms()
    bot = cfg.get("bot", {})
    return {
        "platforms": platforms,
        "sessions": {p: has_session(p) for p in platforms},
        "missing_sessions": missing_sessions(platforms),
        "auto_execute": bool(bot.get("auto_execute", False)),
        "dry_run": bool(bot.get("dry_run", True)),
        "ready": bool(bot.get("auto_execute")) and not missing_sessions(platforms),
    }


def pick_best_opportunity(
    bankroll: float,
    min_profit: float = 0.0,
    source: str = "all",
    platforms: list[str] | None = None,
) -> dict:
    """Pick best middle or surebet limited to user's platforms."""
    platforms = platforms or _configured_platforms()
    surebets, middles, meta = scan_all(bankroll=bankroll, min_profit_pct=min_profit, source=source)

    filtered_middles = [
        m
        for m in middles
        if m.leg_a.platform in platforms and m.leg_b.platform in platforms
    ]
    if filtered_middles:
        best = filtered_middles[0]
        return {
            "type": "middle",
            "opportunity": best,
            "orders": middle_to_orders(best),
            "meta": meta,
        }

    filtered_surebets = [
        s
        for s in surebets
        if all(o.platform in platforms for o in s.outcomes)
    ]
    if filtered_surebets:
        best = max(filtered_surebets, key=lambda s: s.profit_pct)
        orders = []
        for o in best.outcomes:
            key = f"{o.platform}:{o.label}"
            orders.append(
                BetOrder(
                    platform=o.platform,
                    match=best.match,
                    market=best.market,
                    selection=o.label,
                    odds=o.odds,
                    stake=best.stakes[key],
                )
            )
        return {
            "type": "surebet",
            "opportunity": best,
            "orders": orders,
            "meta": meta,
        }

    return {"type": "none", "opportunity": None, "orders": [], "meta": meta}


def middle_to_orders(middle: MiddleOpportunity) -> list[BetOrder]:
    return [
        BetOrder(
            platform=middle.leg_a.platform,
            match=middle.match,
            market="asian_handicap",
            selection=middle.leg_a.selection,
            odds=middle.leg_a.odds,
            stake=middle.stake_a,
        ),
        BetOrder(
            platform=middle.leg_b.platform,
            match=middle.match,
            market="asian_handicap",
            selection=middle.leg_b.selection,
            odds=middle.leg_b.odds,
            stake=middle.stake_b,
        ),
    ]


async def run_autopilot(
    bankroll: float = 7.0,
    source: str = "all",
    force: bool = False,
    headless: bool = True,
) -> dict:
    cfg = load_config()
    bot = cfg.get("bot", {})
    auto_execute = bool(bot.get("auto_execute", False))
    dry_run = bool(bot.get("dry_run", True))

    readiness = readiness_check()
    report: dict = {
        "readiness": readiness,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": [],
    }

    if readiness["missing_sessions"]:
        report["status"] = "need_login"
        report["message"] = f"Login required: {readiness['missing_sessions']}. Run: python cli.py login --platform stake"
        return report

    if not auto_execute and not force:
        report["status"] = "need_enable"
        report["message"] = "Run: python cli.py autopilot --enable  (one-time opt-in for real bets)"
        return report

    pick = pick_best_opportunity(bankroll=bankroll, source=source)
    report["pick"] = {
        "type": pick["type"],
        "match": getattr(pick.get("opportunity"), "match", None),
    }

    if pick["type"] == "none":
        report["status"] = "no_opportunity"
        report["message"] = "No arbitrage on your platforms right now"
        return report

    executor = BetExecutor(auto_execute=auto_execute or force, dry_run=dry_run and not force)

    orders: list[BetOrder] = pick["orders"]
    sorted_orders = sorted(orders, key=lambda o: o.odds)

    for order in sorted_orders:
        if dry_run and not force:
            result = await executor.place_order(order)
        else:
            from executor.playwright_runner import place_order_via_playwright

            result = await place_order_via_playwright(order, headless=headless)
        report["results"].append(_serialize_result(result))

    placed = [r for r in report["results"] if r.get("status") == "placed"]
    report["status"] = "placed" if len(placed) == len(orders) else "partial"
    report["message"] = f"{len(placed)}/{len(orders)} legs placed"

    log_path = BETS_DIR / f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    BETS_DIR.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    report["log"] = str(log_path)
    return report


def _serialize_result(result: dict) -> dict:
    out = dict(result)
    if "order" in out and hasattr(out["order"], "__dataclass_fields__"):
        out["order"] = asdict(out["order"])
    return out


def enable_auto_execute(dry_run: bool = False) -> dict:
    """Flip config.yaml bot.auto_execute = true."""
    import yaml

    from config_loader import USER_CONFIG, ensure_user_config

    ensure_user_config()
    data = yaml.safe_load(USER_CONFIG.read_text(encoding="utf-8")) or {}
    bot = data.setdefault("bot", {})
    bot["auto_execute"] = True
    bot["dry_run"] = dry_run
    USER_CONFIG.write_text(yaml.dump(data, allow_unicode=True, default_flow_style=False), encoding="utf-8")
    return {"auto_execute": True, "dry_run": dry_run, "config": str(USER_CONFIG)}