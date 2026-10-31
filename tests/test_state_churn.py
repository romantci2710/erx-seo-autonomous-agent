# -*- coding: utf-8 -*-
"""State files must not be rewritten (and so must not show up in git) when only timestamps changed."""
import json

from muse_seo_daemon import save_json_state

VOLATILE = ("last_checked", "last_watch_run")


def _data(ts, title="A"):
    return {"last_watch_run": ts, "url_registry": {"https://x/": {"title": title, "last_checked": ts, "issues": []}}}


def test_timestamp_only_change_does_not_rewrite_the_file(tmp_path):
    p = tmp_path / "state.json"
    assert save_json_state(p, _data("t1"), ignore_keys=VOLATILE) is True   # first write
    before = p.read_text(encoding="utf-8")
    assert save_json_state(p, _data("t2"), ignore_keys=VOLATILE) is False  # only timestamps differ
    assert p.read_text(encoding="utf-8") == before


def test_real_change_rewrites_including_fresh_timestamps(tmp_path):
    p = tmp_path / "state.json"
    save_json_state(p, _data("t1"), ignore_keys=VOLATILE)
    assert save_json_state(p, _data("t2", title="B"), ignore_keys=VOLATILE) is True
    saved = json.loads(p.read_text(encoding="utf-8"))
    assert saved["url_registry"]["https://x/"]["title"] == "B" and saved["last_watch_run"] == "t2"


def test_default_behaviour_is_unchanged_and_tolerates_corrupt_files(tmp_path):
    p = tmp_path / "s.json"
    assert save_json_state(p, {"a": 1}) is True
    assert save_json_state(p, {"a": 1}) is True  # no ignore_keys: always writes
    p.write_text("not json", encoding="utf-8")
    assert save_json_state(p, {"a": 1}, ignore_keys=VOLATILE) is True
    assert json.loads(p.read_text(encoding="utf-8")) == {"a": 1}
