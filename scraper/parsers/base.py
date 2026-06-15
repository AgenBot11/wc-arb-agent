"""Shared odds parsing utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedMarket:
    market: str
    selection: str
    odds: float
    handicap: float | None = None


_ODDS_RE = re.compile(r"\b(\d+\.\d{2})\b")


def extract_decimal_odds(text: str) -> list[float]:
    return [float(m) for m in _ODDS_RE.findall(text) if 1.01 <= float(m) <= 50.0]


def parse_page_odds(platform: str, body_text: str) -> list[ParsedMarket]:
    from scraper.parsers.cloudbet import parse_cloudbet_odds
    from scraper.parsers.stake import parse_stake_odds

    parsers = {"stake": parse_stake_odds, "cloudbet": parse_cloudbet_odds}
    fn = parsers.get(platform)
    if not fn:
        return []
    return fn(body_text)