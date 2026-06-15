"""
Semi-auto / auto bet executor via Playwright.

SAFETY: auto_execute defaults to False. Enable only after manual testing.
"""

from __future__ import annotations

from dataclasses import dataclass


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
                "message": "Bet logged but not placed. Set auto_execute=True to enable.",
            }

        # Platform-specific bet slip automation goes here
        return {
            "status": "not_implemented",
            "order": order,
            "message": "Add platform bet-slip selectors in executor/parsers/",
        }

    async def place_arbitrage_pair(self, orders: list[BetOrder]) -> list[dict]:
        # Place harder side first (industry standard)
        sorted_orders = sorted(orders, key=lambda o: o.odds)
        results = []
        for order in sorted_orders:
            results.append(await self.place_order(order))
        return results