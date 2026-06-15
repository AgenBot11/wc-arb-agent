#!/usr/bin/env python3
"""MCP server — Grok Build calls these tools directly, zero manual CLI."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

from config_loader import config_status, ensure_user_config
from mcp.server.fastmcp import FastMCP
from registration import format_missing_links_compact, format_registration_json

mcp = FastMCP("wc-arb-agent")
ensure_user_config()


def _py(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(ROOT / "cli.py"), *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return result.stdout or result.stderr


def _with_missing_links(output: str) -> str:
    block = format_missing_links_compact(config_status())
    return output + block if block else output


@mcp.tool()
def wc_arb_scan(bankroll: float = 7.0, live: bool = True) -> str:
    """Scan for surebets and Asian handicap middles. Set live=true for real API odds."""
    args = ["scan", "--bankroll", str(bankroll)]
    if live:
        args.append("--all")
    else:
        args.append("--demo")
    return _with_missing_links(_py(*args))


@mcp.tool()
def wc_arb_fixtures() -> str:
    """List today's live World Cup fixtures (needs API-Football key in config.yaml)."""
    return _with_missing_links(_py("fixtures"))


@mcp.tool()
def wc_arb_agent(text: str, minute: int = 0) -> str:
    """Analyze live commentary text and return Agent trading signals."""
    args = ["agent", "--text", text]
    if minute:
        args.extend(["--minute", str(minute)])
    return _py(*args)


@mcp.tool()
def wc_arb_status() -> str:
    """Show config status and direct registration URLs for anything still missing."""
    return _py("status")


@mcp.tool()
def wc_arb_setup() -> str:
    """One-shot setup: create config.yaml and show what is still missing."""
    return _with_missing_links(_py("setup"))


@mcp.tool()
def wc_arb_registration_links(missing_only: bool = True) -> str:
    """Return registration URLs. Default: only items user still needs to register."""
    args = ["register"]
    if missing_only:
        args.append("--missing")
    args.append("--json")
    return _py(*args)


@mcp.tool()
def wc_arb_affiliate() -> str:
    """Show configured affiliate signup links for Stake, Cloudbet, BC.Game."""
    return _with_missing_links(_py("affiliate"))


@mcp.tool()
def wc_arb_init(skip_playwright: bool = False) -> str:
    """Full auto-init: install deps, create config, print registration links."""
    args = ["init"]
    if skip_playwright:
        args.append("--skip-playwright")
    return _with_missing_links(_py(*args))


@mcp.tool()
def wc_arb_onboard(skip_playwright: bool = False) -> str:
    """Zero-touch onboarding: init + status + missing registration links in one call."""
    args = ["onboard"]
    if skip_playwright:
        args.append("--skip-playwright")
    return _with_missing_links(_py(*args))


@mcp.tool()
def wc_arb_browser_playbook(scenario: str = "stake_scrape_odds") -> str:
    """Return Agent browser takeover steps for odds scraping or assisted betting. No API quota used."""
    return _py("browser", "--scenario", scenario)


@mcp.tool()
def wc_arb_browser_list() -> str:
    """List all browser takeover scenarios (Playwright / Grok / browser-use compatible)."""
    return _py("browser", "--list")


@mcp.tool()
def wc_arb_browser_scrape(platform: str, match_url: str) -> str:
    """Scrape match odds from Stake or Cloudbet via Playwright (uses saved .sessions/ login if any)."""
    return _py("browser", "--scenario", f"{platform}_scrape_odds", "--run", "scrape", "--platform", platform, "--url", match_url)


@mcp.tool()
def wc_arb_login(platform: str) -> str:
    """Open browser for user to log in to stake or cloudbet once; saves session for autopilot."""
    return _py("login", "--platform", platform)


@mcp.tool()
def wc_arb_autopilot_enable(dry_run: bool = False) -> str:
    """One-time opt-in: enable auto_execute in config.yaml for real bets."""
    args = ["autopilot", "--enable"]
    if dry_run:
        args.append("--dry-run")
    return _py(*args)


@mcp.tool()
def wc_arb_autopilot_check() -> str:
    """Check if login sessions and auto_execute are ready for autonomous betting."""
    return _py("autopilot", "--check")


@mcp.tool()
def wc_arb_autopilot(bankroll: float = 7.0, preview: bool = False) -> str:
    """Autonomous scan + place bets on Stake/Cloudbet. Requires login + autopilot --enable first."""
    if preview:
        return _py("autopilot", "--preview", "--bankroll", str(bankroll))
    return _py("autopilot", "--bankroll", str(bankroll))


@mcp.tool()
def wc_arb_go() -> str:
    """Full user journey: onboard → check readiness → guide login/enable → run autopilot if ready."""
    parts = [
        _py("onboard"),
        "\n--- READINESS ---\n",
        _py("autopilot", "--check"),
        "\n--- INSTRUCTIONS ---\n",
        "If missing_sessions: call wc_arb_login for each platform.\n"
        "If need_enable: call wc_arb_autopilot_enable.\n"
        "When ready: call wc_arb_autopilot.\n"
        "Docs: docs/AUTOPILOT.md",
    ]
    check = _py("autopilot", "--check")
    if '"ready": true' in check.replace(" ", ""):
        parts.append("\n--- AUTO RUN ---\n")
        parts.append(_py("autopilot", "--preview"))
    return "\n".join(parts)


if __name__ == "__main__":
    mcp.run()