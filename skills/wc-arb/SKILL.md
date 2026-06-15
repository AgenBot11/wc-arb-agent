---
name: wc-arb
description: >
  World Cup crypto arbitrage with autonomous betting. MCP: wc_arb_go, wc_arb_autopilot,
  wc_arb_login, wc_arb_scan. User installs plugin, logs in once, then auto bets.
---

# WC Arb Agent — Autonomous Operator

**Goal:** After install + one-time login, user says「执行套利」→ you run bets without asking them to click.

## Full autonomous flow

| Order | Tool | Notes |
|-------|------|-------|
| 1 | `wc_arb_onboard` | deps + config |
| 2 | `wc_arb_login("stake")` | user logs in browser once |
| 3 | `wc_arb_login("cloudbet")` | same |
| 4 | `wc_arb_autopilot_enable` | user must agree to real money |
| 5 | `wc_arb_autopilot(preview=true)` | show pick first |
| 6 | `wc_arb_autopilot` | scan + place bets |

Shortcut: `wc_arb_go` — runs checks and guides missing steps.

## BYOK

Users need **their own** The-Odds-API key for live scan. See `docs/API_KEYS.md`.

## When user says「帮我下注」「执行套利」

1. `wc_arb_autopilot_check`
2. Fix blockers (login / enable) via tools above
3. `wc_arb_autopilot(preview=true)` → explain match + stakes
4. `wc_arb_autopilot` → execute
5. Report `.sessions/bets/` screenshots + log path

## Rules

- Exact USDT stakes per platform
- Prioritize middles over surebets
- Harder leg (lower odds) first
- If partial failure, show screenshot paths
- `wc_arb_affiliate` for signup links only