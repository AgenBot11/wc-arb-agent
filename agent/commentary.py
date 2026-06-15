from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    GOAL = "goal"
    RED_CARD = "red_card"
    YELLOW_CARD = "yellow_card"
    SUBSTITUTION = "substitution"
    VAR = "var"
    KICKOFF = "kickoff"
    HALFTIME = "halftime"
    FULLTIME = "fulltime"
    PRESSURE = "pressure"
    UNKNOWN = "unknown"


@dataclass
class CommentaryEvent:
    minute: int
    event_type: EventType
    team: str
    text: str
    score: str | None = None


@dataclass
class AgentSignal:
    action: str
    reason: str
    confidence: float
    suggested_markets: list[str]


class CommentaryAnalyzer:
    """Rule-based Agent layer. Swap for LLM API in production."""

    KEYWORDS = {
        EventType.GOAL: ["goal", "scores", "进球", "破门"],
        EventType.RED_CARD: ["red card", "sent off", "红牌"],
        EventType.YELLOW_CARD: ["yellow card", "黄牌"],
        EventType.VAR: ["var", "video review"],
        EventType.PRESSURE: ["pressing", "dangerous", "chance", "威胁"],
    }

    def parse_event(self, minute: int, text: str, team: str = "") -> CommentaryEvent:
        lower = text.lower()
        event_type = EventType.UNKNOWN
        for et, words in self.KEYWORDS.items():
            if any(w in lower for w in words):
                event_type = et
                break
        return CommentaryEvent(minute=minute, event_type=event_type, team=team, text=text)

    def analyze(self, events: list[CommentaryEvent], current_odds: dict) -> list[AgentSignal]:
        signals: list[AgentSignal] = []
        score = "0-0"
        for e in events:
            if e.score:
                score = e.score

        last = events[-1] if events else None
        if not last:
            return signals

        if last.event_type == EventType.GOAL:
            parts = score.split("-")
            if len(parts) == 2:
                diff = abs(int(parts[0]) - int(parts[1]))
                if diff == 1:
                    signals.append(
                        AgentSignal(
                            action="MIDDLE_ALERT",
                            reason=f"Score {score} — 1-goal lead, middle window open",
                            confidence=0.75,
                            suggested_markets=["asian_handicap_middle", "lock_profit"],
                        )
                    )
                elif diff >= 2:
                    signals.append(
                        AgentSignal(
                            action="HOLD",
                            reason=f"Score {score} — favorite pulling away",
                            confidence=0.8,
                            suggested_markets=[],
                        )
                    )

        if last.event_type == EventType.RED_CARD:
            signals.append(
                AgentSignal(
                    action="LIVE_VALUE",
                    reason="Red card shifts live odds — scan for arb",
                    confidence=0.7,
                    suggested_markets=["1x2", "asian_handicap", "totals"],
                )
            )

        if last.event_type == EventType.PRESSURE and current_odds.get("totals_over_25", 0) > 2.1:
            signals.append(
                AgentSignal(
                    action="WATCH",
                    reason="High pressure + over odds drifting",
                    confidence=0.55,
                    suggested_markets=["totals_over_25"],
                )
            )

        return signals