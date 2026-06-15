"""
Affiliate link manager.

Links are NOT encrypted — they are public tracking IDs, not secrets.
Open-source encryption would be security theater (the key ships in the repo).

Instead:
  - Real codes live in config.yaml (gitignored) or environment variables
  - Source code only contains placeholders
  - Each fork maintainer uses their own codes
"""

from __future__ import annotations

from dataclasses import dataclass

from config_loader import load_config


@dataclass(frozen=True)
class AffiliateLink:
    platform: str
    ref_code: str
    url: str
    commission_note: str
    configured: bool


def get_affiliate_links() -> list[AffiliateLink]:
    cfg = load_config()
    links: list[AffiliateLink] = []
    for platform, data in cfg.get("affiliate", {}).items():
        if not isinstance(data, dict):
            continue
        ref = str(data.get("ref_code", ""))
        configured = bool(ref) and "YOUR_" not in ref
        links.append(
            AffiliateLink(
                platform=platform,
                ref_code=ref if configured else "(not configured)",
                url=str(data.get("url", "")),
                commission_note=str(data.get("commission", "")),
                configured=configured,
            )
        )
    return links


def format_affiliate_banner() -> str:
    lines = ["", "── Platform signup (affiliate) ──"]
    any_configured = False
    for link in get_affiliate_links():
        if link.configured:
            any_configured = True
            lines.append(f"  {link.platform}: {link.url}")
        elif link.platform == "bcgame" and not link.url:
            lines.append(f"  {link.platform}: skipped (optional)")
        else:
            lines.append(f"  {link.platform}: run `python cli.py setup` to configure")
    if not any_configured:
        lines.append("  Tip: copy config.example.yaml → config.yaml and add your ref codes")
    return "\n".join(lines)