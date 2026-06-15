"""
Auto bet executor via Playwright.

Enable with: python cli.py autopilot --enable
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class BetOrder:
    platform: str
    match: str
    market: str
    selection: str
    odds: float
    stake: float


class BetExecutor:
    def __init__(self, auto_execute: bool = False, dry_run: bool = True):
        self.auto_execute = auto_execute
        self.dry_run = dry_run

    async def place_order(self, order: BetOrder) -> dict:
        if self.dry_run or not self.auto_execute:
            return {
                "status": "dry_run",
                "order": order,
                "message": "Logged only. Enable: python cli.py autopilot --enable",
            }

        from executor.playwright_runner import place_order_via_playwright

        return await place_order_via_playwright(order, headless=True)

    async def place_arbitrage_pair(self, orders: list[BetOrder]) -> list[dict]:
        sorted_orders = sorted(orders, key=lambda o: o.odds)
        results = []
        for order in sorted_orders:
            results.append(await self.place_order(order))
        return results


def order_to_dict(order: BetOrder) -> dict:
    return asdict(order)