#!/usr/bin/env python3
"""WC Arb Agent CLI — scan, analyze, and plan cross-platform arbitrage."""

import argparse
import json
import shutil
import sys
from pathlib import Path

from affiliate import format_affiliate_banner, get_affiliate_links
from agent.commentary import CommentaryAnalyzer, CommentaryEvent, EventType
from config_loader import USER_CONFIG, config_status, load_config
from scanner import scan_all

ROOT = Path(__file__).parent


def cmd_scan(args):
    source = "live" if args.live else ("all" if args.all_sources else "demo")
    surebets, middles, meta = scan_all(
        bankroll=args.bankroll,
        min_profit_pct=args.min_profit,
        source=source,
    )

    print("=" * 60)
    print("WC ARB AGENT — Opportunity Scanner")
    print("=" * 60)
    print(f"Source: {source} | Snapshots: {meta.get('snapshot_count', 0)} | {meta.get('sources', [])}")
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
        print("\n  No opportunities at current thresholds.")

    print(format_affiliate_banner())
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
    print("Links are loaded from config.yaml (gitignored) or WC_ARB_*_REF env vars.")
    print("Do NOT commit real ref codes to GitHub.")
    return 0


def cmd_setup(args):
    example = ROOT / "config.example.yaml"
    if not USER_CONFIG.exists():
        shutil.copy(example, USER_CONFIG)
        print(f"Created {USER_CONFIG}")
    else:
        print(f"Already exists: {USER_CONFIG}")

    print("\n=== Registration checklist ===\n")
    checklist = [
        ("GitHub", "https://github.com", "Done — repo published"),
        ("Stake Affiliate", "https://stake.com/affiliate", "Apply → paste ref in config.yaml"),
        ("Cloudbet Affiliate", "https://www.cloudbet.com/affiliates", "Apply → paste ref"),
        ("BC.Game Affiliate", "https://bc.game/affiliate", "Apply → paste ref"),
        ("The-Odds-API", "https://the-odds-api.com", "Free key → the_odds_api.key"),
        ("API-Football", "https://www.api-football.com", "Free key → api_football.key"),
        ("X / Twitter", "https://x.com", "For promotion posts"),
    ]
    for name, url, note in checklist:
        print(f"  [ ] {name}")
        print(f"      {url}")
        print(f"      {note}\n")

    status = config_status()
    print("Current config status:")
    for k, v in status.items():
        print(f"  {k}: {'yes' if v else 'no'}")
    return 0


def cmd_fixtures(args):
    from scraper.api_football import fetch_live_fixtures

    fixtures = fetch_live_fixtures()
    if not fixtures:
        print("No live fixtures. Add api_football.key to config.yaml")
        print("Get free key: https://www.api-football.com")
        return 1
    for f in fixtures:
        print(f"  [{f.status} {f.minute}'] {f.match} {f.score} (id={f.fixture_id})")
    return 0


def cmd_status(args):
    print(json.dumps(config_status(), indent=2))
    cfg = load_config()
    print(f"\nPlatforms enabled: {cfg.get('platforms', [])}")
    print(f"Auto execute: {cfg.get('bot', {}).get('auto_execute', False)}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="wc-arb-agent",
        description="AI-powered World Cup cross-platform arbitrage toolkit",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    scan_p = sub.add_parser("scan", help="Scan for surebets and middles")
    scan_p.add_argument("--bankroll", type=float, default=7.0)
    scan_p.add_argument("--min-profit", type=float, default=0.0, dest="min_profit")
    scan_p.add_argument("--live", action="store_true", help="Use The-Odds-API only")
    scan_p.add_argument("--all", action="store_true", dest="all_sources", help="Demo + live")
    scan_p.set_defaults(func=cmd_scan)

    agent_p = sub.add_parser("agent", help="Analyze live commentary")
    agent_p.add_argument("--text", type=str, default="")
    agent_p.add_argument("--minute", type=int, default=67)
    agent_p.add_argument("--fixture-id", type=int, default=0)
    agent_p.set_defaults(func=cmd_agent)

    sub.add_parser("affiliate", help="Show affiliate link status").set_defaults(func=cmd_affiliate)
    sub.add_parser("setup", help="Create config.yaml + registration checklist").set_defaults(func=cmd_setup)
    sub.add_parser("fixtures", help="List today's live fixtures (API-Football)").set_defaults(func=cmd_fixtures)
    sub.add_parser("status", help="Show configuration status").set_defaults(func=cmd_status)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()