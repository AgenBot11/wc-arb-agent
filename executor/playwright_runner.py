"""Playwright bet placement runner."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from executor.browser_bet import BetOrder
from executor.platform_urls import platform_match_url

ROOT = Path(__file__).resolve().parent.parent
BETS_DIR = ROOT / ".sessions" / "bets"


async def place_order_via_playwright(order: BetOrder, headless: bool = True) -> dict:
    from playwright.async_api import async_playwright

    from executor.parsers.base import place_platform_bet
    from scraper.playwright_odds import load_session

    url = platform_match_url(order.platform, order.match)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    shot_dir = BETS_DIR / f"{order.platform}_{ts}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await load_session(order.platform, browser)
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=90000)
        await page.wait_for_timeout(3000)
        result = await place_platform_bet(page, order, shot_dir)
        result["url"] = url
        await browser.close()
    return result