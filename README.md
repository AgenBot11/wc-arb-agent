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
git clone https://github.com/YOUR_USERNAME/wc-arb-agent.git
cd wc-arb-agent
pip install -r requirements.txt
playwright install chromium

# Scan demo World Cup odds for opportunities
python cli.py scan --bankroll 7

# Analyze live commentary text
python cli.py agent --text "Red card shown to Senegal defender"
```

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
cp config.example.yaml config.yaml
# Edit affiliate codes and API keys
```

**Safety defaults:**
- `auto_execute: false` — never auto-bet without explicit opt-in
- `dry_run: true` — log orders only

---

## Roadmap

- [x] Surebet calculator
- [x] Middle detector
- [x] Commentary Agent (rule-based)
- [x] Playwright scraper scaffold
- [x] Dry-run bet executor
- [ ] Stake / Cloudbet DOM parsers
- [ ] API-Football live feed
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