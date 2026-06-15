import time

from scraper.cache import get_cached, get_cached_stale, set_cached


def test_cache_and_stale_fallback(tmp_path, monkeypatch):
    monkeypatch.setattr("scraper.cache.CACHE_DIR", tmp_path)
    set_cached("test_key", [{"a": 1}])
    assert get_cached("test_key", ttl_sec=90) == [{"a": 1}]

    # Simulate expired but still within stale window
    path = tmp_path / list(tmp_path.iterdir())[0].name
    import json

    payload = json.loads(path.read_text())
    payload["_ts"] = time.time() - 200
    path.write_text(json.dumps(payload))

    assert get_cached("test_key", ttl_sec=90) is None
    stale, age = get_cached_stale("test_key", max_age_sec=3600)
    assert stale == [{"a": 1}]
    assert age is not None and age >= 200