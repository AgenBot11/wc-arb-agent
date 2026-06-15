"""Playwright session management for platform login state."""

from __future__ import annotations

from pathlib import Path

SESSION_DIR = Path(__file__).resolve().parent.parent / ".sessions"

LOGIN_URLS = {
    "stake": "https://stake.com",
    "cloudbet": "https://cloudbet.com/en/auth/login",
}


def session_path(platform: str) -> Path:
    return SESSION_DIR / f"{platform}_state.json"


def has_session(platform: str) -> bool:
    return session_path(platform).exists()


def missing_sessions(platforms: list[str]) -> list[str]:
    return [p for p in platforms if not has_session(p)]


def ensure_session_dir() -> Path:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    return SESSION_DIR