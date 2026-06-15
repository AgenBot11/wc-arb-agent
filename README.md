# WC Arb Agent

**AI-powered cross-platform sports arbitrage toolkit for the 2026 World Cup.**

Free, open-source, and built for crypto sportsbooks (Stake, Cloudbet, BC.Game).  
Scan surebets, detect Asian handicap middles, analyze live commentary, and plan automated bets.

> Sell shovels, not gold. This tool is free — we earn through platform referral programs when you sign up via our links.

---

## Why This Exists

Most arbitrage bots on GitHub only support US sportsbooks (FanDuel, DraftKings).  
**WC Arb Agent** fills the gap:

| Feature | WC Arb Agent | Typical OSS bots |
|---------|--------------|------------------|
| Crypto bookmakers (USDT) | Yes | Rare |
| Asian handicap middles | Yes | Rare |
| Live commentary Agent | Yes | No |
| Playwright auto-bet scaffold | Yes | Partial |
| World Cup 2026 focus | Yes | No |

---

## Quick Start

```bash
git clone https://github.com/AgenBot11/wc-arb-agent.git
cd wc-arb-agent
pip install -r requirements.txt
playwright install chromium

python cli.py setup          # your own config.yaml (never commit)
python cli.py scan --bankroll 7   # demo + live if you added YOUR API key

# Analyze live commentary text
python cli.py agent --text "Red card shown to Senegal defender"
```

**Grok plugin:** `grok plugin install AgenBot11/wc-arb-agent --trust`

### Autonomous betting (3 steps after install)

```bash
python cli.py login --platform stake      # log in once in browser
python cli.py login --platform cloudbet
python cli.py autopilot --enable          # one-time opt-in
python cli.py autopilot                   # scan + place bets
```

In Grok: `wc_arb_go` → `wc_arb_autopilot`  
Guide: [docs/AUTOPILOT.md](docs/AUTOPILOT.md)

---

## API Keys — Bring Your Own (BYOK)

**Each user must register their own API keys.** The project does not ship shared keys.

| Why | Detail |
|-----|--------|
| Quota | The-Odds-API ~500 credits/month per account |
| Security | Shared keys get exhausted in days when used by all users |
| Setup | Copy `config.example.yaml` → `config.yaml`, paste **your** keys |

Register: [The-Odds-API](https://the-odds-api.com/#get-access) · [API-Football](https://dashboard.api-football.com/register) (optional)

Full policy: [docs/API_KEYS.md](docs/API_KEYS.md)

---

## Agent Browser Takeover (no API quota)

For **Stake / Cloudbet real odds** or when API credits run low, use Agent browser playbooks:

```bash
python cli.py browser --list
python cli.py browser --scenario stake_scrape_odds
python cli.py browser --scenario stake_login --run login --platform stake
```

Works with Grok browser, Playwright, or optional [browser-use](https://github.com/browser-use/browser-use).  
Guide: [docs/BROWSER_AGENT.md](docs/BROWSER_AGENT.md)

---

## What It Finds

### 1. Surebets (risk-free arbitrage)

When combined implied probability < 100%, profit is guaranteed:

```
Profit % = (1 - Σ(1/odds)) × 100
```

### 2. Middles (Asian handicap)

Exploit line differences across platforms. Example:

| Platform | Bet | Odds |
|----------|-----|------|
| Stake | France -1.0 | 1.90 |
| Cloudbet | Senegal +1.5 | 1.95 |

If France wins by **exactly 1 goal** → **both sides pay**. That's the middle.

### 3. Agent signals (live commentary)

Feed live text → get action signals:

```bash
python cli.py agent --text "GOAL France 1-0 in the 23rd minute"
```

---

## Project Structure

```
wc-arb-agent/
├── core/           # Arbitrage + middle math (open source)
├── scraper/        # Playwright odds scraping
├── agent/          # Live commentary analyzer
├── executor/       # Auto-bet executor (dry-run by default)
├── cli.py          # Main entry point
└── config.example.yaml
```

---

## Supported Platforms

Register through our referral links to support the project:

| Platform | USDT | Referral |
|----------|------|----------|
| **Stake** | TRC-20 | [Sign up →](https://stake.com/?c=YOUR_CODE) |
| **Cloudbet** | TRC-20 | [Sign up →](https://cloudbet.com/en/auth/sign-up?referrer=YOUR_CODE) |
| **BC.Game** | Multi-chain | [Sign up →](https://bc.game/?i=YOUR_CODE) |

Replace `YOUR_CODE` with codes from `config.yaml` after copying `config.example.yaml`.

---

## Configuration

```bash
python cli.py setup   # creates config.yaml from example
# Fill in YOUR affiliate codes and YOUR API keys — never commit config.yaml
```

**Safety defaults:**
- `auto_execute: false` — never auto-bet without explicit opt-in
- `dry_run: true` — log orders only

---

## Roadmap

- [x] Surebet calculator
- [x] Middle detector
- [x] Commentary Agent (rule-based)
- [x] Playwright scraper + parsers
- [x] Autopilot bet executor (opt-in `--enable`)
- [x] Agent browser playbooks (Grok / Playwright / browser-use)
- [x] BYOK API key documentation
- [ ] DOM selector hardening (site updates)
- [ ] API-Football live feed (optional)
- [ ] Chrome extension UI
- [ ] LLM-powered Agent layer

---

## Disclaimer

**For educational and entertainment purposes only.**

- Gambling laws vary by jurisdiction. Comply with your local laws.
- Arbitrage is not risk-free in practice (odds movement, bet delays, account limits).
- Authors are not responsible for financial losses.
- Check each platform's Terms of Service before using automation.

---

## Contributing

PRs welcome. Priority areas:
1. Platform-specific odds parsers (Stake, Cloudbet, BC.Game)
2. Live commentary API integrations
3. Tests for arbitrage math

---

## License

MIT — free to use, modify, and distribute.

---

**Star this repo if it helps you. Share on X with `#WorldCup2026 #SportsArbitrage #CryptoBetting`**