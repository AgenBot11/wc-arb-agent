#!/usr/bin/env python3
"""WC Arb Agent CLI — scan, analyze, and plan cross-platform arbitrage."""

import argparse
import json
import sys

from agent.commentary import CommentaryAnalyzer, CommentaryEvent, EventType
from scanner import scan_middles, scan_surebets


def cmd_scan(args):
    print("=" * 60)
    print("WC ARB AGENT — Opportunity Scanner")
    print("=" * 60)

    surebets = scan_surebets(bankroll=args.bankroll, min_profit_pct=args.min_profit)
    middles = scan_middles(bankroll=args.bankroll)

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
        print("  Tip: Middles are more common than surebets on World Cup matches.")

    return 0


def cmd_agent(args):
    analyzer = CommentaryAnalyzer()
    events = [
        CommentaryEvent(23, EventType.GOAL, "France", "Mbappe scores!", "1-0"),
        CommentaryEvent(45, EventType.PRESSURE, "Senegal", "Senegal pressing hard"),
    ]
    if args.text:
        events.append(analyzer.parse_event(67, args.text))

    signals = analyzer.analyze(events, {"totals_over_25": 2.15})
    print(json.dumps([s.__dict__ for s in signals], indent=2))
    return 0


def cmd_affiliate(args):
    from pathlib import Path

    path = Path(__file__).parent / "config.yaml"
    if not path.exists():
        print("Copy config.example.yaml → config.yaml and add your referral codes.")
        return 1
    print(f"Config found: {path}")
    print("Affiliate links will be injected into README and CLI output.")
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
    scan_p.set_defaults(func=cmd_scan)

    agent_p = sub.add_parser("agent", help="Analyze live commentary text")
    agent_p.add_argument("--text", type=str, default="", help="Live commentary line")
    agent_p.set_defaults(func=cmd_agent)

    aff_p = sub.add_parser("affiliate", help="Check affiliate config")
    aff_p.set_defaults(func=cmd_affiliate)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()