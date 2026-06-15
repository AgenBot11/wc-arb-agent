---
name: wc-arb
description: >
  World Cup crypto sportsbook arbitrage agent. MCP: wc_arb_scan, wc_arb_onboard,
  wc_arb_browser_playbook, wc_arb_registration_links. BYOK API keys required.
  Browser takeover for Stake/Cloudbet without API quota.
---

# WC Arb Agent — Grok Operator Mode

**Minimize user actions.** Run MCP tools yourself.

## Critical: BYOK (Bring Your Own Key)

- **Never** use or share the maintainer's API keys
- Each user registers **their own** [The-Odds-API](https://the-odds-api.com/#get-access) key
- Quota is per account (~500 credits/month) — shared keys die in days
- Tell users: paste **their** key into `config.yaml` or env `WC_ARB_THE_ODDS_API_KEY`
- Full policy: `docs/API_KEYS.md`

If user has no API key: run `wc_arb_scan` with `live=false` (demo) **or** `wc_arb_browser_playbook` for real Stake/Cloudbet odds.

## Zero-touch workflow

| Step | Tool |
|------|------|
| First time | `wc_arb_onboard` |
| Scan | `wc_arb_scan` (live=true only if user has own key) |
| No API key | `wc_arb_browser_playbook` + execute steps in browser |
| Missing config | `wc_arb_registration_links` → paste URLs |
| Fixtures | `wc_arb_fixtures` (optional API-Football) |
| Commentary | `wc_arb_agent` |

## Browser takeover (no API quota)

| Tool | Use |
|------|-----|
| `wc_arb_browser_list` | List scenarios |
| `wc_arb_browser_playbook` | Steps for Grok/computer-use agent |
| `wc_arb_browser_scrape` | Playwright scrape if session exists |

Scenarios: `stake_scrape_odds`, `cloudbet_scrape_odds`, `compare_platforms`, `assisted_bet`  
`assisted_bet` — fill slip only, **never** click Confirm.

## Registration URLs

| What | URL |
|------|-----|
| The-Odds-API | https://the-odds-api.com/#get-access |
| API-Football (optional) | https://dashboard.api-football.com/register |
| Stake Affiliate | https://stake.com/affiliate |
| Cloudbet Affiliate | https://www.cloudbet.com/affiliates |

## Output rules

- Exact platform, market, odds, USDT stake
- Prioritize middles over surebets
- Remind users BYOK when discussing live scan
- Use `wc_arb_affiliate` for signup links, never hardcode