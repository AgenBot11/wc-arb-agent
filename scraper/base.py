from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class MarketOdds:
    market: str
    selection: str
    odds: float
    handicap: float | None = None


@dataclass
class PlatformOdds:
    platform: str
    match: str
    markets: list[MarketOdds] = field(default_factory=list)
    scraped_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class OddsSnapshot:
    match: str
    platforms: list[PlatformOdds] = field(default_factory=list)

    def best_odds(self, market: str, selection: str) -> tuple[str, float] | None:
        best_platform = None
        best_odds = 0.0
        for p in self.platforms:
            for m in p.markets:
                if m.market == market and m.selection == selection and m.odds > best_odds:
                    best_odds = m.odds
                    best_platform = p.platform
        if best_platform is None:
            return None
        return best_platform, best_odds