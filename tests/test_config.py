import os

from affiliate import get_affiliate_links
from config_loader import load_config


def test_load_config_has_affiliate_section():
    cfg = load_config()
    assert "affiliate" in cfg
    assert "stake" in cfg["affiliate"]


def test_affiliate_placeholder_not_configured():
    links = get_affiliate_links()
    stake = next(l for l in links if l.platform == "stake")
    assert stake.configured is False or stake.ref_code != "(not configured)"


def test_env_override_ref(monkeypatch):
    monkeypatch.setenv("WC_ARB_STAKE_REF", "testref123")
    cfg = load_config()
    assert cfg["affiliate"]["stake"]["ref_code"] == "testref123"