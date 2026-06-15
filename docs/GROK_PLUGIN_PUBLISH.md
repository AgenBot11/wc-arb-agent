# Publish as Grok Build Plugin

## Can we? Yes.

Grok Build plugins bundle skills + commands + optional MCP/hooks.
This repo is already structured as a plugin:

```
wc-arb-agent/
├── .grok-plugin/plugin.json    # manifest
├── skills/wc-arb/SKILL.md      # auto-invoked agent skill
├── commands/wc-arb.md          # /wc-arb slash command
├── cli.py                      # underlying tooling
└── core/ scraper/ agent/       # open-source engine
```

## Install locally (test)

```bash
grok plugin install ./wc-arb-agent --trust
grok plugin enable wc-arb-agent
```

Or from GitHub after push:

```bash
grok plugin install AgenBot11/wc-arb-agent --trust
```

## Publish to official xAI Marketplace

1. Push repo to GitHub (public)
2. Open PR to https://github.com/xai-org/plugin-marketplace
3. Add entry to `.grok-plugin/marketplace.json`:

```json
{
  "name": "wc-arb-agent",
  "description": "World Cup crypto sportsbook arbitrage — surebets, middles, live commentary agent.",
  "category": "finance",
  "keywords": ["arbitrage", "world-cup", "stake", "usdt", "sports-betting"],
  "domains": ["stake.com", "cloudbet.com", "bc.game"],
  "source": {
    "source": "url",
    "url": "https://github.com/AgenBot11/wc-arb-agent.git",
    "sha": "PASTE_40_CHAR_COMMIT_SHA"
  },
  "homepage": "https://github.com/AgenBot11/wc-arb-agent"
}
```

4. Pin SHA: `git ls-remote https://github.com/AgenBot11/wc-arb-agent.git HEAD`
5. Wait for xAI review + code-owner approval

**Note:** Gambling plugins may face extra scrutiny. Keep disclaimer prominent.

## X promotion angle (Grok Build plugin)

Better hook than "random GitHub repo":

```
We built a Grok Build plugin for World Cup arbitrage 🏆

Install in one line:
grok plugin install AgenBot11/wc-arb-agent --trust

Then just type: /wc-arb

→ Scans Stake + Cloudbet for middles
→ Calculates exact USDT stakes
→ AI reads live commentary

Free & open source. Built for @grok Build.

#GrokBuild #WorldCup2026 #SportsArbitrage
```

Tag @grok @xai — plugin marketplace launches get more reach than standalone repos.

## Monetization inside plugin

- README + skill output includes affiliate links (config.yaml)
- Plugin is free; revenue = platform referral commissions
- Do NOT charge for plugin while using affiliate links (trust issue)