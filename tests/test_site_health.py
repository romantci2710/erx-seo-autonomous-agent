# -*- coding: utf-8 -*-
"""Site-level health: security headers, soft 404, compression, UA parity, placeholder tags."""
import datetime as dt

from muse_seo_daemon import (
    GOOGLEBOT_UA,
    USER_AGENT,
    audit_advisory_seo,
    check_security_headers,
    check_site_health,
    extract_page_seo_signals,
    site_health_due,
)

GOOD_HEADERS = {
    "strict-transport-security": "max-age=31536000; includeSubDomains",
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
}


def _resp(status=200, headers=None, text="", wire_bytes=None):
    return {
        "ok": status < 400,
        "status": status,
        "headers": {k.lower(): v for k, v in (headers or {}).items()},
        "text": text,
        "wire_bytes": len(text.encode("utf-8")) if wire_bytes is None else wire_bytes,
    }


PAGE = "<html><head><title>Trang chủ ERX</title></head><body><h1>Trang chủ</h1>%s</body></html>"
PLATFORM = {"id": "t", "domain": "t.erx.vn", "base_url": "https://t.erx.vn/"}


def make_fetch(home=None, probe=None, googlebot=None):
    """Fake fetcher: probe URL -> probe, UA Googlebot -> googlebot, else home."""
    home = home or _resp(headers={**GOOD_HEADERS, "content-encoding": "gzip", "content-type": "text/html"}, text=PAGE % "x")

    def fetch(url, user_agent=USER_AGENT, timeout=15):
        if "__seo-probe-" in url:
            return probe or _resp(404, {"content-type": "text/html"}, "nf")
        if user_agent == GOOGLEBOT_UA and googlebot is not None:
            return googlebot
        return home

    return fetch


# ---- security headers ----

def test_security_headers_missing_and_good():
    assert check_security_headers({}) == ["MISSING_HSTS", "MISSING_NOSNIFF", "MISSING_REFERRER_POLICY"]
    assert check_security_headers(GOOD_HEADERS) == []


def test_security_headers_malformed_values_are_flagged():
    bad = {**GOOD_HEADERS, "strict-transport-security": ": max-age=31536000", "x-content-type-options": ": nosniff"}
    flags = check_security_headers(bad)
    assert "MALFORMED_HSTS" in flags
    assert "MISSING_NOSNIFF" in flags


# ---- site health ----

def test_site_health_clean_site_has_no_flags():
    result = check_site_health(PLATFORM, fetch=make_fetch())
    assert result["flags"] == []
    assert "checked_at" in result


def test_soft_404_and_non_html_404():
    soft = check_site_health(PLATFORM, fetch=make_fetch(probe=_resp(200, {"content-type": "text/html"}, "shell")))
    assert "SOFT_404" in soft["flags"]
    json404 = check_site_health(
        PLATFORM, fetch=make_fetch(probe=_resp(404, {"content-type": "application/json"}, "{}"))
    )
    assert "NON_HTML_404" in json404["flags"]
    gone = check_site_health(PLATFORM, fetch=make_fetch(probe=_resp(410, {"content-type": "text/html"}, "gone")))
    assert not {"SOFT_404", "NON_HTML_404"} & set(gone["flags"])


def test_uncompressed_large_html_is_flagged_but_small_is_not():
    big = _resp(headers={**GOOD_HEADERS, "content-type": "text/html"}, text=PAGE % "x", wire_bytes=975_000)
    assert any(f.startswith("HTML_NOT_COMPRESSED") for f in check_site_health(PLATFORM, fetch=make_fetch(home=big))["flags"])
    small = _resp(headers={**GOOD_HEADERS, "content-type": "text/html"}, text=PAGE % "x", wire_bytes=20_000)
    assert not any(f.startswith("HTML_NOT_COMPRESSED") for f in check_site_health(PLATFORM, fetch=make_fetch(home=small))["flags"])


def test_user_agent_parity_detects_empty_shell_for_normal_browsers():
    shell = _resp(headers={**GOOD_HEADERS, "content-encoding": "gzip"}, text="<html><head></head><body><div id='root'></div></body></html>")
    full = _resp(headers={**GOOD_HEADERS, "content-encoding": "gzip"}, text=PAGE % ("<p>nội dung</p>" * 50))
    result = check_site_health(PLATFORM, fetch=make_fetch(home=shell, googlebot=full))
    assert "UA_CONTENT_MISMATCH" in result["flags"]


def test_user_agent_parity_ok_when_identical():
    page = _resp(headers={**GOOD_HEADERS, "content-encoding": "gzip"}, text=PAGE % "x")
    assert "UA_CONTENT_MISMATCH" not in check_site_health(PLATFORM, fetch=make_fetch(home=page, googlebot=page))["flags"]


def test_unreachable_homepage():
    def fetch(url, user_agent=USER_AGENT, timeout=15):
        return {"ok": False, "status": 0, "headers": {}, "text": "", "wire_bytes": 0}

    assert "HOMEPAGE_UNREACHABLE" in check_site_health(PLATFORM, fetch=fetch)["flags"]


def test_site_health_due_respects_ttl():
    now = dt.datetime(2026, 10, 30, 12, 0, tzinfo=dt.timezone.utc)
    assert site_health_due(None, now)
    assert not site_health_due({"checked_at": (now - dt.timedelta(hours=1)).isoformat()}, now)
    assert site_health_due({"checked_at": (now - dt.timedelta(hours=7)).isoformat()}, now)
    assert site_health_due({"checked_at": "garbage"}, now)


# ---- placeholder tags (literal "undefined" etc.) ----

def _sig(title="Tiêu đề hợp lệ cho trang này", desc="Mô tả hợp lệ " * 8, h1="Tiêu đề chính"):
    html_text = (
        f'<html><head><title>{title}</title><meta name="description" content="{desc}" />'
        f'<link rel="canonical" href="https://erx.vn/" /></head><body><h1>{h1}</h1></body></html>'
    )
    return extract_page_seo_signals(html_text, "https://erx.vn/")


def test_undefined_placeholder_in_tags_is_flagged():
    sig = _sig(title="undefined", desc="undefined", h1="undefined")
    flags = audit_advisory_seo(sig, "khoahoc.erx.vn")
    assert any(f.startswith("UNDEFINED_PLACEHOLDER") and "title" in f and "h1" in f for f in flags)


def test_legitimate_use_of_null_or_undefined_in_a_longer_title_is_not_flagged():
    sig = _sig(title="Xử lý giá trị null và undefined trong SQL và JavaScript")
    assert not any(f.startswith("UNDEFINED_PLACEHOLDER") for f in audit_advisory_seo(sig, "erx.vn"))
