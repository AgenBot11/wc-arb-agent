"""All registration URLs — single source of truth."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RegistrationItem:
    id: str
    name: str
    url: str
    category: str
    purpose: str
    required: bool
    eta: str
    config_key: str = ""


REGISTRATIONS: list[RegistrationItem] = [
    RegistrationItem(
        "stake_affiliate",
        "Stake Affiliate（返利）",
        "https://stake.com/affiliate",
        "money",
        "申请推荐码 → 填入 config.yaml affiliate.stake.ref_code",
        True,
        "1-3 天",
        "stake_affiliate",
    ),
    RegistrationItem(
        "cloudbet_affiliate",
        "Cloudbet Affiliates（返利）",
        "https://www.cloudbet.com/affiliates",
        "money",
        "申请推荐码 → affiliate.cloudbet.ref_code",
        True,
        "1-2 天",
        "cloudbet_affiliate",
    ),
    RegistrationItem(
        "bcgame_affiliate",
        "BC.Game Affiliate（返利，可选）",
        "https://bc.game/affiliate",
        "money",
        "部分地区无法注册可跳过；有码后填 affiliate.bcgame.ref_code",
        False,
        "较快",
        "bcgame_affiliate",
    ),
    RegistrationItem(
        "the_odds_api",
        "The-Odds-API（实时赔率）",
        "https://the-odds-api.com/#get-access",
        "data",
        "必须用自己的 Key（BYOK）→ the_odds_api.key，禁止共用额度",
        True,
        "5 分钟",
        "the_odds_api",
    ),
    RegistrationItem(
        "api_football",
        "API-Football（赛程/事件，可选）",
        "https://dashboard.api-football.com/register",
        "data",
        "注册后复制 API Key 即可，无需找「世界杯专用接口」— 工具自动按联赛筛选",
        False,
        "5 分钟",
        "api_football",
    ),
    RegistrationItem(
        "stake_signup",
        "Stake 开户（用户用）",
        "https://stake.com/?c=YOUR_STAKE_CODE",
        "platform",
        "你的返利链接，拿到码后替换",
        False,
        "即时",
        "",
    ),
    RegistrationItem(
        "cloudbet_signup",
        "Cloudbet 开户（用户用）",
        "https://cloudbet.com/en/auth/sign-up",
        "platform",
        "你的返利链接",
        False,
        "即时",
        "",
    ),
    RegistrationItem(
        "github_repo",
        "GitHub 仓库",
        "https://github.com/AgenBot11/wc-arb-agent",
        "promo",
        "已完成",
        False,
        "—",
        "",
    ),
    RegistrationItem(
        "grok_plugin",
        "Grok 安装插件",
        "https://github.com/AgenBot11/wc-arb-agent#quick-start",
        "promo",
        "grok plugin install AgenBot11/wc-arb-agent --trust",
        False,
        "即时",
        "",
    ),
    RegistrationItem(
        "xai_marketplace",
        "xAI Plugin Marketplace PR",
        "https://github.com/xai-org/plugin-marketplace",
        "promo",
        "可选：申请上架官方市场",
        False,
        "数天",
        "",
    ),
]

_BY_CONFIG_KEY = {r.config_key: r for r in REGISTRATIONS if r.config_key}


def registration_url_for(config_key: str, fallback: str = "") -> str:
    item = _BY_CONFIG_KEY.get(config_key)
    return item.url if item else fallback


def get_missing_registrations(status: dict[str, bool]) -> list[RegistrationItem]:
    """Return required registration items not yet configured."""
    missing: list[RegistrationItem] = []
    for key, item in _BY_CONFIG_KEY.items():
        if item.required and not status.get(key, False):
            missing.append(item)
    return missing


def format_missing_links_compact(status: dict[str, bool]) -> str:
    """One-block paste for Grok to hand user — only what's still missing."""
    missing = get_missing_registrations(status)
    if not missing:
        return ""
    lines = ["\n--- 还需注册（直接点链接） ---"]
    for item in missing:
        lines.append(f"• {item.name} (~{item.eta}): {item.url}")
        lines.append(f"  {item.purpose}")
    return "\n".join(lines)


def format_registration_markdown() -> str:
    lines = ["# 注册链接一览\n"]
    for cat, title in [
        ("money", "## 赚钱必做"),
        ("data", "## 数据必做"),
        ("platform", "## 平台开户"),
        ("promo", "## 推广可选"),
    ]:
        items = [r for r in REGISTRATIONS if r.category == cat]
        if not items:
            continue
        lines.append(title)
        for item in items:
            req = "**必做**" if item.required else "可选"
            lines.append(f"- {item.name} ({req}, ~{item.eta})")
            lines.append(f"  - 链接: {item.url}")
            lines.append(f"  - 用途: {item.purpose}")
        lines.append("")
    return "\n".join(lines)


def format_registration_json(status: dict[str, bool] | None = None) -> str:
    payload = {
        "all": [asdict(r) for r in REGISTRATIONS],
        "missing": [asdict(r) for r in get_missing_registrations(status or {})],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)