"""Platform bet placement via Playwright."""

from __future__ import annotations

from executor.browser_bet import BetOrder
from executor.parsers.cloudbet_bet import place_cloudbet_bet
from executor.parsers.stake_bet import place_stake_bet


async def place_platform_bet(page, order: BetOrder, screenshot_dir) -> dict:
    placers = {
        "stake": place_stake_bet,
        "cloudbet": place_cloudbet_bet,
    }
    fn = placers.get(order.platform)
    if not fn:
        return {"status": "error", "message": f"Unsupported platform: {order.platform}"}
    return await fn(page, order, screenshot_dir)