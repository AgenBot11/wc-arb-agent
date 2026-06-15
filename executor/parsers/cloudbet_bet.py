"""Cloudbet bet slip automation."""

from __future__ import annotations

import re
from pathlib import Path

from executor.browser_bet import BetOrder

_SUBMIT_TEXTS = ("Place bet", "Place Bet", "Confirm bet", "Confirm", "Bet now")
_STAKE_SELECTORS = (
    'input[type="number"]',
    'input[placeholder*="Stake"]',
    'input[data-testid*="stake"]',
)


async def _click_selection(page, selection: str) -> bool:
    tokens = [t for t in re.split(r"\s+", selection) if len(t) > 1]
    for token in tokens[:3]:
        try:
            loc = page.get_by_text(token, exact=False).first
            if await loc.count() > 0:
                await loc.click(timeout=5000)
                return True
        except Exception:
            continue
    return False


async def _fill_stake(page, stake: float) -> bool:
    for sel in _STAKE_SELECTORS:
        try:
            loc = page.locator(sel).first
            if await loc.count() > 0:
                await loc.fill(str(round(stake, 2)), timeout=5000)
                return True
        except Exception:
            continue
    return False


async def _submit(page) -> bool:
    for text in _SUBMIT_TEXTS:
        try:
            btn = page.get_by_role("button", name=text).first
            if await btn.count() > 0:
                await btn.click(timeout=8000)
                return True
        except Exception:
            continue
    return False


async def place_cloudbet_bet(page, order: BetOrder, screenshot_dir: Path) -> dict:
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    if not await _click_selection(page, order.selection):
        await page.screenshot(path=str(screenshot_dir / "cloudbet_select_fail.png"))
        return {"status": "error", "step": "select", "message": f"Could not find: {order.selection}"}

    await page.wait_for_timeout(800)
    if not await _fill_stake(page, order.stake):
        await page.screenshot(path=str(screenshot_dir / "cloudbet_stake_fail.png"))
        return {"status": "error", "step": "stake", "message": "Could not fill stake input"}

    await page.screenshot(path=str(screenshot_dir / "cloudbet_presubmit.png"))
    if not await _submit(page):
        return {"status": "error", "step": "submit", "message": "Could not click Place Bet"}

    await page.wait_for_timeout(2000)
    await page.screenshot(path=str(screenshot_dir / "cloudbet_postsubmit.png"))
    return {"status": "placed", "platform": "cloudbet", "order": order}