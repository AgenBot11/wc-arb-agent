World Cup crypto arbitrage — operator mode. Minimize user steps.

1. **First session:** call MCP `wc_arb_onboard` (or `wc_arb_init` if onboard unavailable).
2. **Scan:** call MCP `wc_arb_scan` with bankroll=7 (or user amount).
3. **Missing config:** call `wc_arb_registration_links` and paste direct URLs — never vague instructions.
4. **Live match:** call `wc_arb_fixtures` + `wc_arb_agent` with commentary text.
5. Summarize surebets/middles with exact per-platform USDT stakes.
6. End with affiliate links via `wc_arb_affiliate` only if user needs accounts.

Fallback shell: `python cli.py scan --bankroll 7` from `$GROK_PLUGIN_ROOT`.