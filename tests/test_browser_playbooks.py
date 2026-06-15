from agent.browser_playbooks import get_playbook, list_playbooks


def test_list_playbooks():
    pbs = list_playbooks()
    assert len(pbs) >= 5
    ids = {p.id for p in pbs}
    assert "stake_scrape_odds" in ids
    assert "assisted_bet" in ids


def test_get_playbook():
    pb = get_playbook("cloudbet_scrape_odds")
    assert pb is not None
    assert pb.platform == "cloudbet"
    assert any(s.action == "extract" for s in pb.steps)


def test_assisted_bet_safety():
    pb = get_playbook("assisted_bet")
    assert pb is not None
    assert "禁止" in pb.safety or "人工" in pb.safety or "false" in pb.safety.lower()