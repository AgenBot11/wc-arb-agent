"""Demo odds for testing without live platform access."""

from .base import MarketOdds, OddsSnapshot, PlatformOdds


def get_demo_world_cup_odds() -> list[OddsSnapshot]:
    return [
        OddsSnapshot(
            match="France vs Senegal",
            platforms=[
                PlatformOdds(
                    platform="stake",
                    match="France vs Senegal",
                    markets=[
                        MarketOdds("1x2", "France", 1.48),
                        MarketOdds("1x2", "Draw", 4.50),
                        MarketOdds("1x2", "Senegal", 7.20),
                        MarketOdds("asian_handicap", "France -1.0", 1.90, -1.0),
                        MarketOdds("totals", "Over 2.5", 2.00),
                        MarketOdds("totals", "Under 2.5", 1.85),
                    ],
                ),
                PlatformOdds(
                    platform="cloudbet",
                    match="France vs Senegal",
                    markets=[
                        MarketOdds("1x2", "France", 1.45),
                        MarketOdds("1x2", "Draw", 4.60),
                        MarketOdds("1x2", "Senegal", 7.50),
                        MarketOdds("asian_handicap", "Senegal +1.5", 1.95, 1.5),
                        MarketOdds("totals", "Over 2.5", 1.95),
                        MarketOdds("totals", "Under 2.5", 1.90),
                    ],
                ),
            ],
        ),
        OddsSnapshot(
            match="Iraq vs Norway",
            platforms=[
                PlatformOdds(
                    platform="stake",
                    match="Iraq vs Norway",
                    markets=[
                        MarketOdds("1x2", "Norway", 1.22),
                        MarketOdds("1x2", "Draw", 6.50),
                        MarketOdds("1x2", "Iraq", 13.00),
                        MarketOdds("asian_handicap", "Norway -1.0", 1.85, -1.0),
                        MarketOdds("totals", "Under 2.5", 1.80),
                    ],
                ),
                PlatformOdds(
                    platform="cloudbet",
                    match="Iraq vs Norway",
                    markets=[
                        MarketOdds("1x2", "Norway", 1.20),
                        MarketOdds("1x2", "Draw", 7.00),
                        MarketOdds("1x2", "Iraq", 12.00),
                        MarketOdds("asian_handicap", "Iraq +1.5", 2.00, 1.5),
                        MarketOdds("totals", "Under 2.5", 1.85),
                    ],
                ),
            ],
        ),
    ]