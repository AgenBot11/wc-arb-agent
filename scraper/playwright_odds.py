"""
Playwright-based odds scraper for crypto sportsbooks.

Usage:
  1. Copy config.example.yaml → config.yaml
  2. Log in manually once; cookies are saved to .sessions/
  3. python -m scraper.playwright_odds --match "France vs Senegal"

Supported platforms (extensible):
  - stake
  - cloudbet
  - bcgame
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SESSION_DIR = Path(__file__).resolve().parent.parent / ".sessions"


async def save_session(platform: str, context) -> None:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    path = SESSION_DIR / f"{platform}_state.json"
    await context.storage_state(path=str(path))
    print(f"Session saved: {path}")


async def load_session(platform: str, browser):
    path = SESSION_DIR / f"{platform}_state.json"
    if path.exists():
        return await browser.new_context(storage_state=str(path))
    return await browser.new_context()


async def scrape_platform(platform: str, match_url: str, headless: bool = True) -> dict:
    try:
        from playwright.async_api import async_playwright
    except ImportError as e:
        raise ImportError("Install playwright: pip install playwright && playwright install") from e

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await load_session(platform, browser)
        page = await context.new_page()
        await page.goto(match_url, wait_until="domcontentloaded", timeout=60000)

        title = await page.title()
        body_text = await page.inner_text("body")
        from scraper.parsers.base import parse_page_odds

        markets = parse_page_odds(platform, body_text)

        await browser.close()
        return {
            "platform": platform,
            "title": title,
            "url": match_url,
            "markets": [{"market": m.market, "selection": m.selection, "odds": m.odds, "handicap": m.handicap} for m in markets],
            "market_count": len(markets),
        }


def main():
    parser = argparse.ArgumentParser(description="Scrape odds via Playwright")
    parser.add_argument("--platform", required=True, choices=["stake", "cloudbet", "bcgame"])
    parser.add_argument("--url", required=True, help="Match page URL")
    parser.add_argument("--headless", action="store_true", default=True)
    args = parser.parse_args()

    import asyncio

    result = asyncio.run(scrape_platform(args.platform, args.url, args.headless))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()