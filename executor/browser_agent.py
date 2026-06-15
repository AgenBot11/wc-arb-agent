"""Execute browser playbooks via Playwright or optional browser-use."""

from __future__ import annotations

import json
from dataclasses import asdict

from agent.browser_playbooks import BrowserPlaybook, get_playbook


async def run_playwright_scrape(platform: str, match_url: str, headless: bool = True) -> dict:
    from scraper.playwright_odds import scrape_platform

    return await scrape_platform(platform, match_url, headless=headless)


async def run_playwright_login(platform: str, login_url: str, headless: bool = False) -> dict:
    """Headful login — user completes auth, session saved."""
    try:
        from playwright.async_api import async_playwright
    except ImportError as e:
        raise ImportError("pip install playwright && playwright install chromium") from e

    from scraper.playwright_odds import save_session

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(login_url, wait_until="domcontentloaded", timeout=60000)
        if not headless:
            await page.wait_for_timeout(120_000)
        await save_session(platform, context)
        await browser.close()
    return {"status": "ok", "platform": platform, "session": f".sessions/{platform}_state.json"}


async def run_browser_use_agent(scenario: str, match_url: str) -> dict:
    """Optional browser-use integration when installed."""
    playbook = get_playbook(scenario)
    if not playbook:
        return {"status": "error", "message": f"Unknown scenario: {scenario}"}

    try:
        from browser_use import Agent  # type: ignore
        from langchain_openai import ChatOpenAI  # type: ignore
    except ImportError:
        return {
            "status": "not_installed",
            "message": "pip install browser-use langchain-openai",
            "playbook": asdict(playbook),
        }

    task = (
        f"Follow this playbook for {playbook.name}: "
        f"{json.dumps(asdict(playbook), ensure_ascii=False)}. "
        f"Match URL: {match_url}. Extract odds only, do not place bets."
    )
    agent = Agent(task=task, llm=ChatOpenAI(model="gpt-4o-mini"))
    result = await agent.run()
    return {"status": "ok", "scenario": scenario, "result": str(result)}


def playbook_for_agent(scenario: str) -> dict:
    pb = get_playbook(scenario)
    if not pb:
        return {"error": f"Unknown scenario. Available: {list_playbook_ids()}"}
    return asdict(pb)


def list_playbook_ids() -> list[str]:
    from agent.browser_playbooks import PLAYBOOKS

    return list(PLAYBOOKS.keys())