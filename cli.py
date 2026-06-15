#!/usr/bin/env python3
"""WC Arb Agent CLI — scan, analyze, and plan cross-platform arbitrage."""

import argparse
import json
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

from affiliate import format_affiliate_banner, get_affiliate_links
from agent.commentary import CommentaryAnalyzer, CommentaryEvent, EventType
from config_loader import USER_CONFIG, config_status, ensure_user_config, load_config
from registration import (
    REGISTRATIONS,
    format_missing_links_compact,
    format_registration_json,
    format_registration_markdown,
    get_missing_registrations,
)
from scanner import scan_all

ROOT = Path(__file__).parent


def _append_missing_links() -> None:
    block = format_missing_links_compact(config_status())
    if block:
        print(block)


def cmd_scan(args):
    if args.demo:
        source = "demo"
    elif args.live:
        source = "live"
    else:
        source = "all"

    surebets, middles, meta = scan_all(
        bankroll=args.bankroll,
        min_profit_pct=args.min_profit,
        source=source,
    )

    print("=" * 60)
    print("WC ARB AGENT — Opportunity Scanner")
    print("=" * 60)
    print(f"Source: {source} | Snapshots: {meta.get('snapshot_count', 0)} | {meta.get('sources', [])}")

    live_meta = meta.get("live_meta", {})
    if live_meta.get("cached"):
        print("Live odds: cached (90s TTL)")
    if live_meta.get("stale"):
        print(f"Live odds: stale cache ({live_meta.get('stale_age_sec', '?')}s old)")
    if live_meta.get("credits_remaining"):
        print(f"API credits remaining: {live_meta['credits_remaining']}")
    for err in live_meta.get("errors", []):
        print(f"Note: {err}")
    if meta.get("live_error"):
        print(f"Note: {meta['live_error']}")

    print(f"\n[SUREBETS] Found {len(surebets)}")
    for opp in surebets:
        print(f"\n  Match: {opp.match} | Market: {opp.market}")
        print(f"  Profit: {opp.profit_pct:.2f}% | Guaranteed: +{opp.guaranteed_profit}U")
        for outcome in opp.outcomes:
            key = f"{outcome.platform}:{outcome.label}"
            print(f"    → {key} @ {outcome.odds} → stake {opp.stakes[key]}U")

    print(f"\n[MIDDLES] Found {len(middles)}")
    for opp in middles:
        print(f"\n  Match: {opp.match}")
        print(f"    A: {opp.leg_a.platform} {opp.leg_a.selection} @ {opp.leg_a.odds} → {opp.stake_a}U")
        print(f"    B: {opp.leg_b.platform} {opp.leg_b.selection} @ {opp.leg_b.odds} → {opp.stake_b}U")
        print(f"    Middle scores: {', '.join(opp.middle_scores)}")
        print(f"    Middle profit: +{opp.middle_profit}U | Worst case: {opp.worst_case_loss}U")

    if not surebets and not middles:
        print("\n  No opportunities yet.")

    print(format_affiliate_banner())
    _append_missing_links()
    return 0


def cmd_agent(args):
    analyzer = CommentaryAnalyzer()
    events: list[CommentaryEvent] = []

    if args.fixture_id:
        from scraper.api_football import fetch_fixture_events

        for ev in fetch_fixture_events(args.fixture_id):
            minute = ev.get("time", {}).get("elapsed", 0) or 0
            team = ev.get("team", {}).get("name", "")
            detail = ev.get("detail", "")
            events.append(analyzer.parse_event(minute, f"{detail} {ev.get('type', '')}", team))

    if args.text:
        events.append(analyzer.parse_event(args.minute, args.text))

    if not events:
        events = [
            CommentaryEvent(23, EventType.GOAL, "France", "Mbappe scores!", "1-0"),
            CommentaryEvent(45, EventType.PRESSURE, "Senegal", "Senegal pressing hard"),
        ]

    signals = analyzer.analyze(events, {"totals_over_25": 2.15})
    print(json.dumps([s.__dict__ for s in signals], indent=2, default=str))
    return 0


def cmd_affiliate(args):
    links = get_affiliate_links()
    print("Affiliate configuration:\n")
    for link in links:
        status = "OK" if link.configured else "MISSING"
        print(f"  [{status}] {link.platform}")
        print(f"         ref: {link.ref_code}")
        print(f"         url: {link.url}")
        if link.commission_note:
            print(f"         note: {link.commission_note}")
        print()
    _append_missing_links()
    return 0


def cmd_register(args):
    status = config_status()
    if args.missing:
        missing = get_missing_registrations(status)
        if not missing:
            print("All required registrations configured.")
            return 0
        print("# 还需注册\n")
        for item in missing:
            print(f"- {item.name} (~{item.eta})")
            print(f"  {item.url}")
            print(f"  {item.purpose}\n")
        if args.json:
            print(format_registration_json(status))
        if args.open:
            for item in missing:
                print(f"Opening: {item.url}")
                webbrowser.open(item.url)
        return 0

    print(format_registration_markdown())
    if args.json:
        print("\n" + format_registration_json(status))
    if args.open:
        for item in REGISTRATIONS:
            if item.required:
                print(f"Opening: {item.url}")
                webbrowser.open(item.url)
    return 0


def cmd_setup(args):
    ensure_user_config()
    print(f"Config ready: {USER_CONFIG}")
    return cmd_register(argparse.Namespace(missing=True, open=False, json=False))


def cmd_init(args):
    print("=== WC Arb Agent — One-shot Init ===\n")

    print("[1/4] Installing Python dependencies...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt"), "-q"],
        check=False,
    )

    if not args.skip_playwright:
        print("[2/4] Installing Playwright Chromium...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)
    else:
        print("[2/4] Skipped Playwright")

    print("[3/4] Creating config.yaml...")
    ensure_user_config()

    status = config_status()
    print("[4/4] Configuration status:")
    print(json.dumps(status, indent=2))

    missing = get_missing_registrations(status)
    if missing:
        print("\n--- 还需注册（直接点链接） ---")
        for item in missing:
            print(f"  → {item.name}: {item.url}")
    else:
        print("\nAll required keys configured.")

    print("\nDone. In Grok: /wc-arb-scan or MCP wc_arb_scan")
    print("Quick test: python cli.py scan")
    return 0


def cmd_fixtures(args):
    from scraper.api_football import fetch_live_fixtures

    fixtures, meta = fetch_live_fixtures()
    for err in meta.get("errors", []):
        print(f"Note: {err}")
    if meta.get("cached"):
        print("Fixtures: cached (5min TTL)")
    if not fixtures:
        _append_missing_links()
        return 1
    for f in fixtures:
        print(f"  [{f.status} {f.minute}'] {f.match} {f.score} (id={f.fixture_id})")
    return 0


def cmd_status(args):
    print(json.dumps(config_status(), indent=2))
    cfg = load_config()
    print(f"\nPlatforms: {cfg.get('platforms', [])}")
    _append_missing_links()
    return 0


def cmd_onboard(args):
    """Zero-touch: init + status + missing links in one shot."""
    cmd_init(argparse.Namespace(skip_playwright=args.skip_playwright))
    print("\n" + "=" * 40)
    cmd_status(argparse.Namespace())
    return 0


def main():
    ensure_user_config()

    parser = argparse.ArgumentParser(prog="wc-arb-agent")
    sub = parser.add_subparsers(dest="command", required=True)

    scan_p = sub.add_parser("scan", help="Scan opportunities (default: demo+live)")
    scan_p.add_argument("--bankroll", type=float, default=7.0)
    scan_p.add_argument("--min-profit", type=float, default=0.0, dest="min_profit")
    scan_p.add_argument("--demo", action="store_true", help="Demo data only")
    scan_p.add_argument("--live", action="store_true", help="Live API only")
    scan_p.set_defaults(func=cmd_scan)

    agent_p = sub.add_parser("agent", help="Analyze live commentary")
    agent_p.add_argument("--text", type=str, default="")
    agent_p.add_argument("--minute", type=int, default=67)
    agent_p.add_argument("--fixture-id", type=int, default=0)
    agent_p.set_defaults(func=cmd_agent)

    reg_p = sub.add_parser("register", help="Registration links")
    reg_p.add_argument("--open", action="store_true", help="Open links in browser")
    reg_p.add_argument("--missing", action="store_true", help="Only show unconfigured items")
    reg_p.add_argument("--json", action="store_true", help="Also output JSON")
    reg_p.set_defaults(func=cmd_register)

    init_p = sub.add_parser("init", help="One-shot: deps + config + links")
    init_p.add_argument("--skip-playwright", action="store_true")
    init_p.set_defaults(func=cmd_init)

    onboard_p = sub.add_parser("onboard", help="Full zero-touch setup")
    onboard_p.add_argument("--skip-playwright", action="store_true")
    onboard_p.set_defaults(func=cmd_onboard)

    sub.add_parser("affiliate", help="Affiliate status").set_defaults(func=cmd_affiliate)
    sub.add_parser("setup", help="Create config + show links").set_defaults(func=cmd_setup)
    sub.add_parser("fixtures", help="Live fixtures").set_defaults(func=cmd_fixtures)
    sub.add_parser("status", help="Config status").set_defaults(func=cmd_status)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()