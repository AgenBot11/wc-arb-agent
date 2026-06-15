Zero-touch first-time setup.

1. Call MCP `wc_arb_onboard` (preferred) or `wc_arb_init`.
2. Call `wc_arb_status` to see what's still missing.
3. For each missing item, call `wc_arb_registration_links` and paste URLs directly.
4. User registers → pastes API keys in chat → you save to config.yaml or tell them env vars.
5. Then call `wc_arb_scan` — no further manual steps.

Fallback: `python cli.py onboard` from `$GROK_PLUGIN_ROOT`.