# -*- coding: utf-8 -*-
"""Alerts: notify only when site-health flags change or an experiment regresses."""
import json

import alerts as a


# ---- diffing flags ----

def test_diff_flags_ignores_first_observation():
    assert a.diff_flags(None, ["SOFT_404"]) is None


def test_diff_flags_reports_added_and_cleared():
    d = a.diff_flags(["SOFT_404", "MISSING_HSTS"], ["MISSING_HSTS", "MALFORMED_HSTS"])
    assert d == {"added": ["MALFORMED_HSTS"], "cleared": ["SOFT_404"]}


def test_diff_flags_ignores_size_changes_inside_parentheses():
    assert a.diff_flags(["HTML_NOT_COMPRESSED (952 KB)"], ["HTML_NOT_COMPRESSED (975 KB)"]) is None


def test_diff_flags_none_when_equal():
    assert a.diff_flags(["A", "B"], ["B", "A"]) is None


# ---- message ----

def test_format_message_lists_events():
    events = [
        {"type": "site_health", "platform": "khoahoc", "domain": "khoahoc.erx.vn", "added": ["SOFT_404"], "cleared": ["MISSING_HSTS"]},
        {"type": "experiment_regressed", "id": "exp-1", "url": "https://erx.vn/a", "days": 14},
    ]
    text = a.format_message(events)
    assert "khoahoc.erx.vn" in text and "SOFT_404" in text and "MISSING_HSTS" in text
    assert "exp-1" in text and "https://erx.vn/a" in text
    assert a.format_message([]) == ""


# ---- sending ----

class Recorder:
    def __init__(self, fail=False):
        self.calls, self.fail = [], fail

    def __call__(self, url, data, headers):
        self.calls.append((url, json.loads(data.decode()), headers))
        if self.fail:
            raise OSError("down")
        return 200


def test_send_without_configuration_does_nothing():
    rec = Recorder()
    assert a.send("hello", env={}, http_post=rec) == []
    assert rec.calls == []


def test_send_slack_discord_generic_and_telegram_payloads():
    rec = Recorder()
    channels = a.send("hello", env={
        "ALERT_WEBHOOK_URL": "https://hooks.example/x", "ALERT_WEBHOOK_FORMAT": "discord",
        "ALERT_TELEGRAM_BOT_TOKEN": "TOK", "ALERT_TELEGRAM_CHAT_ID": "42"}, http_post=rec)
    assert channels == ["webhook", "telegram"]
    assert rec.calls[0][1] == {"content": "hello"}
    assert rec.calls[1][0] == "https://api.telegram.org/botTOK/sendMessage"
    assert rec.calls[1][1] == {"chat_id": "42", "text": "hello"}
    rec2 = Recorder()
    a.send("hello", env={"ALERT_WEBHOOK_URL": "https://hooks.example/x"}, http_post=rec2)
    assert rec2.calls[0][1] == {"text": "hello"}  # slack is the default
    rec3 = Recorder()
    a.send("hello", env={"ALERT_WEBHOOK_URL": "https://hooks.example/x", "ALERT_WEBHOOK_FORMAT": "generic"}, http_post=rec3)
    assert rec3.calls[0][1] == {"message": "hello"}


def test_send_never_raises_and_reports_only_successful_channels():
    assert a.send("hello", env={"ALERT_WEBHOOK_URL": "https://h/x"}, http_post=Recorder(fail=True)) == []


def test_send_rejects_non_https_webhook():
    rec = Recorder()
    assert a.send("hello", env={"ALERT_WEBHOOK_URL": "http://insecure.example/x"}, http_post=rec) == []
    assert rec.calls == []


# ---- daemon integration ----

def test_site_health_events_come_from_flag_changes(monkeypatch):
    import muse_seo_daemon as d

    prev = {"khoahoc": {"flags": ["SOFT_404"]}, "erx-main": {"flags": ["A"]}}
    curr = [
        {"platform_id": "khoahoc", "domain": "khoahoc.erx.vn", "flags": ["SOFT_404", "MALFORMED_HSTS"]},
        {"platform_id": "erx-main", "domain": "erx.vn", "flags": ["A"]},
        {"platform_id": "community", "domain": "community.erx.vn", "flags": ["X"]},  # first observation
    ]
    events = d.site_health_events(prev, curr)
    assert events == [{"type": "site_health", "platform": "khoahoc", "domain": "khoahoc.erx.vn",
                       "added": ["MALFORMED_HSTS"], "cleared": []}]
