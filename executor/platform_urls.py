"""Build platform match URLs from team names."""

from __future__ import annotations

import re
from urllib.parse import quote


def _slug(team: str) -> str:
    s = team.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def parse_match(match: str) -> tuple[str, str]:
    for sep in (" vs ", " v ", " - "):
        if sep in match:
            a, b = match.split(sep, 1)
            return a.strip(), b.strip()
    raise ValueError(f"Cannot parse match: {match}")


def stake_match_url(match: str) -> str:
    home, away = parse_match(match)
    q = quote(f"{home} {away}")
    return f"https://stake.com/sports/soccer/international/world-cup?search={q}"


def cloudbet_match_url(match: str) -> str:
    home, away = parse_match(match)
    q = quote(f"{home} vs {away}")
    return f"https://cloudbet.com/en/sports/soccer?search={q}"


def platform_match_url(platform: str, match: str) -> str:
    builders = {
        "stake": stake_match_url,
        "cloudbet": cloudbet_match_url,
    }
    fn = builders.get(platform)
    if not fn:
        raise ValueError(f"No URL builder for platform: {platform}")
    return fn(match)