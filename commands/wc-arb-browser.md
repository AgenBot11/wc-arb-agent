Use Agent browser takeover when API quota is low or Stake/Cloudbet real odds needed.

1. Call `wc_arb_browser_list` to see scenarios.
2. Call `wc_arb_browser_playbook` with scenario e.g. `stake_scrape_odds` or `compare_platforms`.
3. Execute steps via Grok browser / computer-use — read odds only unless `assisted_bet`.
4. For `assisted_bet`: fill stake, user clicks Confirm — never auto-submit.
5. Remind user: API keys must be their own (docs/API_KEYS.md).

Fallback: `python cli.py browser --scenario stake_scrape_odds`