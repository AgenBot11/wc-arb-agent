"""Parse Cloudbet sports page text into structured odds."""

from __future__ import annotations

import re

from scraper.parsers.base import ParsedMarket

_AH_RE = re.compile(r"([A-Za-z][A-Za-z\s\.]+?)\s+([+-]?\d+\.?\d*)\s+(\d+\.\d{2})")
_ML_RE = re.compile(r"(Home|Away|Draw|[A-Za-z]{3,})\s+(\d+\.\d{2})")


def parse_cloudbet_odds(body_text: str) -> list[ParsedMarket]:
    markets: list[ParsedMarket] = []
    seen: set[str] = set()

    for m in _AH_RE.finditer(body_text):
        team, line, odds = m.group(1).strip(), float(m.group(2)), float(m.group(3))
        if odds <= 1.0:
            continue
        label = f"{team} {line:+.1f}"
        key = f"ah:{label}"
        if key not in seen:
            seen.add(key)
            markets.append(ParsedMarket("asian_handicap", label, odds, line))

    for m in _ML_RE.finditer(body_text):
        name, odds = m.group(1).strip(), float(m.group(2))
        if odds <= 1.0:
            continue
        key = f"1x2:{name}"
        if key not in seen:
            seen.add(key)
            markets.append(ParsedMarket("1x2", name, odds))

    return markets