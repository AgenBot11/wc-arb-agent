# Completeness Roadmap — v0.2.0

## Done (ready to promote)

- [x] Surebet + middle math engine
- [x] Demo World Cup odds scanner
- [x] The-Odds-API live odds integration (`scan --live`, `scan --all`)
- [x] API-Football fixtures + events (`fixtures`, `agent --fixture-id`)
- [x] Affiliate manager (config.yaml, env vars — no encryption)
- [x] CLI: setup, status, affiliate, scan, agent, fixtures
- [x] Grok Build plugin (skill + /wc-arb command)
- [x] Unit tests (7 passing)
- [x] Registration checklist doc

## In progress (before X launch)

- [ ] Your real affiliate codes in config.yaml
- [ ] The-Odds-API free key (enables live scan)
- [ ] API-Football free key (enables live fixtures)
- [ ] 1 screenshot/GIF of `python cli.py scan` for README

## v0.3.0 (next sprint)

- [ ] Playwright Stake DOM parser (real crypto book odds)
- [ ] Playwright Cloudbet DOM parser
- [ ] BC.Game parser
- [ ] Auto-bet executor (opt-in, dry-run default)
- [ ] Chrome extension popup UI

## Publish gate

**Do NOT post on X until:**

1. `python cli.py affiliate` shows at least 1 `[OK]` platform
2. `python cli.py scan --all` returns live snapshots OR clear demo + live fallback message
3. README has install GIF/screenshot