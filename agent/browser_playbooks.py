"""Browser takeover playbooks for Agent-driven odds scraping and assisted betting."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class BrowserStep:
    action: str
    target: str
    value: str = ""
    notes: str = ""


@dataclass(frozen=True)
class BrowserPlaybook:
    id: str
    name: str
    platform: str
    description: str
    compatible_agents: list[str] = field(default_factory=list)
    steps: list[BrowserStep] = field(default_factory=list)
    safety: str = ""


PLAYBOOKS: dict[str, BrowserPlaybook] = {
    "stake_login": BrowserPlaybook(
        id="stake_login",
        name="Stake 登录并保存会话",
        platform="stake",
        description="打开 Stake，用户手动登录一次，Playwright 保存 cookie 到 .sessions/",
        compatible_agents=["grok", "playwright", "browser-use", "computer-use"],
        steps=[
            BrowserStep("navigate", "https://stake.com", notes="使用用户默认浏览器或 Playwright 有头模式"),
            BrowserStep("wait", "user", notes="用户完成登录（含 2FA）"),
            BrowserStep("save_session", ".sessions/stake_state.json", notes="Playwright storage_state"),
        ],
        safety="不自动输入密码；仅保存用户已登录的会话",
    ),
    "stake_scrape_odds": BrowserPlaybook(
        id="stake_scrape_odds",
        name="Stake 比赛赔率抓取",
        platform="stake",
        description="从 Stake 比赛页提取 1x2 与亚盘赔率文本",
        compatible_agents=["grok", "playwright", "browser-use", "computer-use"],
        steps=[
            BrowserStep("navigate", "{match_url}", notes="用户或 scan 结果提供的比赛 URL"),
            BrowserStep("wait", "networkidle", notes="等待盘口加载"),
            BrowserStep("extract", "main", notes="读取页面赔率区域文本；优先找 1x2、Asian Handicap"),
            BrowserStep("parse", "odds_json", notes="整理为 home/draw/away 与 handicap 行"),
            BrowserStep("return", "wc_arb", notes="回传给套利计算或 wc_arb_agent"),
        ],
        safety="只读页面，不下注",
    ),
    "cloudbet_login": BrowserPlaybook(
        id="cloudbet_login",
        name="Cloudbet 登录并保存会话",
        platform="cloudbet",
        description="Cloudbet 登录态保存",
        compatible_agents=["grok", "playwright", "browser-use"],
        steps=[
            BrowserStep("navigate", "https://cloudbet.com/en/auth/login"),
            BrowserStep("wait", "user", notes="用户手动登录"),
            BrowserStep("save_session", ".sessions/cloudbet_state.json"),
        ],
        safety="不自动输入密码",
    ),
    "cloudbet_scrape_odds": BrowserPlaybook(
        id="cloudbet_scrape_odds",
        name="Cloudbet 比赛赔率抓取",
        platform="cloudbet",
        description="从 Cloudbet 比赛页提取赔率",
        compatible_agents=["grok", "playwright", "browser-use", "computer-use"],
        steps=[
            BrowserStep("navigate", "{match_url}"),
            BrowserStep("wait", "networkidle"),
            BrowserStep("extract", "betting_markets", notes="Moneyline + Asian Handicap + Totals"),
            BrowserStep("parse", "odds_json"),
            BrowserStep("return", "wc_arb"),
        ],
        safety="只读页面，不下注",
    ),
    "compare_platforms": BrowserPlaybook(
        id="compare_platforms",
        name="双平台对照套利",
        platform="multi",
        description="同时打开 Stake 与 Cloudbet 同场比赛，人工或 Agent 对照盘口",
        compatible_agents=["grok", "computer-use", "browser-use"],
        steps=[
            BrowserStep("open_tab", "stake", "{stake_match_url}"),
            BrowserStep("open_tab", "cloudbet", "{cloudbet_match_url}"),
            BrowserStep("extract", "both", notes="分别读取两边赔率"),
            BrowserStep("compute", "surebet_middle", notes="用 core/arbitrage 逻辑或 wc_arb_scan 对比"),
        ],
        safety="只读；下单走 assisted_bet",
    ),
    "assisted_bet": BrowserPlaybook(
        id="assisted_bet",
        name="辅助填单（人工确认下注）",
        platform="multi",
        description="Agent 填入盘口、金额，用户自己点 Confirm",
        compatible_agents=["grok", "playwright", "browser-use"],
        steps=[
            BrowserStep("navigate", "{platform_bet_url}"),
            BrowserStep("click", "{selection}", notes="选择盘口"),
            BrowserStep("type", "stake_input", "{stake_usdt}", notes="填入 USDT 金额"),
            BrowserStep("screenshot", "bet_slip", notes="截图给用户确认"),
            BrowserStep("wait", "user_confirm", notes="**禁止** Agent 点击 Submit/Confirm"),
        ],
        safety="auto_execute 必须为 false；永远人工确认",
    ),
}


def list_playbooks() -> list[BrowserPlaybook]:
    return list(PLAYBOOKS.values())


def get_playbook(scenario_id: str) -> BrowserPlaybook | None:
    return PLAYBOOKS.get(scenario_id)


def format_playbook_markdown(playbook: BrowserPlaybook) -> str:
    lines = [
        f"# {playbook.name}",
        f"Platform: {playbook.platform}",
        f"Agents: {', '.join(playbook.compatible_agents)}",
        "",
        playbook.description,
        "",
        f"Safety: {playbook.safety}",
        "",
        "## Steps",
    ]
    for i, step in enumerate(playbook.steps, 1):
        lines.append(f"{i}. **{step.action}** `{step.target}`")
        if step.value:
            lines.append(f"   - value: {step.value}")
        if step.notes:
            lines.append(f"   - {step.notes}")
    return "\n".join(lines)


def format_playbook_json(playbook: BrowserPlaybook) -> str:
    return json.dumps(asdict(playbook), ensure_ascii=False, indent=2)