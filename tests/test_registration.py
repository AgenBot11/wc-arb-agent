from registration import (
    format_missing_links_compact,
    get_missing_registrations,
    registration_url_for,
)


def test_registration_url_for():
    assert "the-odds-api.com" in registration_url_for("the_odds_api")
    assert registration_url_for("nonexistent", "https://example.com") == "https://example.com"


def test_get_missing_registrations():
    status = {
        "stake_affiliate": False,
        "cloudbet_affiliate": True,
        "bcgame_affiliate": False,
        "api_football": False,
        "the_odds_api": True,
    }
    missing = get_missing_registrations(status)
    ids = {m.id for m in missing}
    assert "stake_affiliate" in ids
    assert "api_football" in ids
    assert "cloudbet_affiliate" not in ids


def test_format_missing_links_compact():
    partial = {"the_odds_api": False, "stake_affiliate": True}
    text = format_missing_links_compact(partial)
    assert "the-odds-api.com" in text

    all_done = {
        "stake_affiliate": True,
        "cloudbet_affiliate": True,
        "bcgame_affiliate": True,
        "api_football": True,
        "the_odds_api": True,
    }
    assert format_missing_links_compact(all_done) == ""