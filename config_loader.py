"""Load config.yaml with environment variable overrides."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config.example.yaml"
USER_CONFIG = ROOT / "config.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as e:
        raise ImportError("Install pyyaml: pip install pyyaml") from e
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}


def load_config() -> dict[str, Any]:
    data = _load_yaml(DEFAULT_CONFIG)
    user = _load_yaml(USER_CONFIG)
    _deep_merge(data, user)
    _apply_env_overrides(data)
    return data


def _deep_merge(base: dict, override: dict) -> None:
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def _apply_env_overrides(cfg: dict[str, Any]) -> None:
    affiliate = cfg.setdefault("affiliate", {})
    for platform in ("stake", "cloudbet", "bcgame"):
        env_ref = os.getenv(f"WC_ARB_{platform.upper()}_REF")
        env_url = os.getenv(f"WC_ARB_{platform.upper()}_URL")
        if env_ref or env_url:
            entry = affiliate.setdefault(platform, {})
            if env_ref:
                entry["ref_code"] = env_ref
            if env_url:
                entry["url"] = env_url

    api_key = os.getenv("WC_ARB_API_FOOTBALL_KEY")
    if api_key:
        cfg.setdefault("api_football", {})["key"] = api_key

    odds_key = os.getenv("WC_ARB_THE_ODDS_API_KEY")
    if odds_key:
        cfg.setdefault("the_odds_api", {})["key"] = odds_key


def _is_configured(value: str) -> bool:
    if not value:
        return False
    upper = value.upper()
    return "YOUR_" not in upper and "PLACEHOLDER" not in upper


def ensure_user_config() -> Path:
    """Create config.yaml from example if missing — zero manual file setup."""
    if not USER_CONFIG.exists() and DEFAULT_CONFIG.exists():
        USER_CONFIG.write_text(DEFAULT_CONFIG.read_text(encoding="utf-8"), encoding="utf-8")
    return USER_CONFIG


def config_status() -> dict[str, bool]:
    cfg = load_config()
    aff = cfg.get("affiliate", {})
    return {
        "config_yaml": USER_CONFIG.exists(),
        "stake_affiliate": _is_configured(str(aff.get("stake", {}).get("ref_code", ""))),
        "cloudbet_affiliate": _is_configured(str(aff.get("cloudbet", {}).get("ref_code", ""))),
        "bcgame_affiliate": _is_configured(str(aff.get("bcgame", {}).get("ref_code", ""))),
        "api_football": _is_configured(str(cfg.get("api_football", {}).get("key", ""))),
        "the_odds_api": _is_configured(str(cfg.get("the_odds_api", {}).get("key", ""))),
    }