# Completeness Roadmap — v0.6.0

## Done (autonomous betting MVP)

- [x] Surebet + middle math
- [x] Demo + The-Odds-API live scan
- [x] Stake / Cloudbet Playwright bet executors
- [x] Autopilot: scan → pick → place (`autopilot --enable`)
- [x] Login session save (`login --platform`)
- [x] Grok MCP: `wc_arb_go`, `wc_arb_autopilot`, `wc_arb_login`
- [x] BYOK docs + browser playbooks
- [x] 19 unit tests

## User journey (target)

1. `grok plugin install AgenBot11/wc-arb-agent --trust`
2. `wc_arb_onboard`
3. `wc_arb_login` × 2 (Stake, Cloudbet)
4. `wc_arb_autopilot_enable`
5. `wc_arb_autopilot` — done

## Remaining (polish)

- [ ] README demo GIF
- [ ] DOM selector hardening per site A/B tests
- [ ] `scan --watch` loop
- [ ] Chrome extension UI
- [ ] BC.Game (optional platform)

## Publish gate for X

1. `affiliate` shows `[OK]` — user has Stake + Cloudbet
2. `autopilot --preview` returns a middle/surebet
3. Screenshot of scan or autopilot preview in README