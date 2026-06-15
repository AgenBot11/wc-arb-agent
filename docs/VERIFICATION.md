# Verification Guide — 怎么验证这套东西能跑

## Level 1: Math (no network, 30 seconds)

```bash
cd wc-arb-agent
python cli.py scan --bankroll 7
```

**Pass criteria:**
- `[MIDDLES] Found >= 1` on demo data
- Each middle shows stake_a, stake_b, middle_profit, worst_case_loss
- No Python exceptions

```bash
python cli.py agent --text "Red card for Senegal defender"
```

**Pass criteria:**
- JSON output with `action`, `reason`, `confidence`

---

## Level 2: Grok Plugin (1 minute)

```bash
grok plugin validate .
grok plugin install ./wc-arb-agent --trust
grok inspect
```

**Pass criteria:**
- `grok plugin validate` exits 0
- `grok inspect` shows skill `wc-arb` and command `wc-arb`
- In Grok TUI: `/wc-arb` or `/skills wc-arb` works

---

## Level 3: Playwright scraper (needs network + login)

```bash
pip install playwright && playwright install chromium
# Manual login once, save session — see scraper/playwright_odds.py
python -m scraper.playwright_odds --platform stake --url "MATCH_URL"
```

**Pass criteria:**
- Returns JSON with platform, title, url
- Session file created in `.sessions/`

**Human required:** first login to each platform.

---

## Level 4: Live odds accuracy (manual cross-check)

1. Open Stake + Cloudbet in browser for same match
2. Note France -1.0 and Senegal +1.5 odds
3. Compare with scanner output
4. **Pass:** odds within 0.05 of live market

---

## Level 5: Paper trade (full flow, no money)

1. Scanner finds middle
2. Record predicted stakes
3. Watch match result
4. Calculate actual P&L manually
5. **Pass:** middle score (1-goal win) matches predicted profit formula

---

## Level 6: Real money (7U test)

1. Deploy exact stakes from scanner
2. Screenshot both bet slips
3. Compare settlement vs prediction
4. **Pass:** worst_case_loss bound holds

---

## Automated tests

```bash
python -m pytest -q
```

**Pass criteria:** all tests green (arbitrage, middle, config, cache, autopilot, playbooks).