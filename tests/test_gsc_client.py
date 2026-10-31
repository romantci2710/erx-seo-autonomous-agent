# -*- coding: utf-8 -*-
"""Search Console client (stdlib only) and opportunity logic."""
import json
import urllib.parse

import gsc_client as g
from muse_seo_daemon import evaluate_and_select_keywords, load_config


def _row(keys, clicks, impressions, position):
    return {"keys": keys, "clicks": clicks, "impressions": impressions,
            "ctr": clicks / impressions if impressions else 0, "position": position}


# ---- credentials ----

def test_load_credentials_accepts_authorized_user_only(tmp_path):
    ok = tmp_path / "adc.json"
    ok.write_text(json.dumps({"type": "authorized_user", "client_id": "c", "client_secret": "s", "refresh_token": "r"}))
    assert g.load_credentials(str(ok))["refresh_token"] == "r"
    sa = tmp_path / "sa.json"
    sa.write_text(json.dumps({"type": "service_account"}))
    assert g.load_credentials(str(sa)) is None
    assert g.load_credentials(str(tmp_path / "missing.json")) is None
    bad = tmp_path / "bad.json"
    bad.write_text("not json")
    assert g.load_credentials(str(bad)) is None


def test_get_access_token_posts_refresh_grant():
    seen = {}

    def post(url, data, headers):
        seen["url"], seen["data"] = url, dict(urllib.parse.parse_qsl(data.decode()))
        return {"access_token": "tok", "expires_in": 3600}

    creds = {"client_id": "c", "client_secret": "s", "refresh_token": "r"}
    assert g.get_access_token(creds, http_post=post) == "tok"
    assert seen["url"] == "https://oauth2.googleapis.com/token"
    assert seen["data"] == {"client_id": "c", "client_secret": "s", "refresh_token": "r", "grant_type": "refresh_token"}


def test_get_access_token_returns_none_on_failure():
    def post(url, data, headers):
        raise OSError("down")

    assert g.get_access_token({"client_id": "c", "client_secret": "s", "refresh_token": "r"}, http_post=post) is None


# ---- querying ----

def test_fetch_rows_paginates_until_short_page_and_encodes_property():
    calls = []

    def post(url, data, headers):
        body = json.loads(data.decode())
        calls.append((url, body, headers))
        start = body["startRow"]
        return {"rows": [_row(["k%d" % i], 1, 10, 5.0) for i in range(start, start + (3 if start == 0 else 1))]}

    rows = g.fetch_rows("sc-domain:erx.vn", "2026-10-01", "2026-10-28", ["page"], "tok", http_post=post, row_limit=3)
    assert len(rows) == 4
    assert [c[1]["startRow"] for c in calls] == [0, 3]
    assert calls[0][0].endswith("/sites/sc-domain%3Aerx.vn/searchAnalytics/query")
    assert calls[0][2]["Authorization"] == "Bearer tok"
    assert calls[0][1]["dimensions"] == ["page"]


def test_fetch_rows_returns_empty_on_error():
    def post(url, data, headers):
        raise OSError("boom")

    assert g.fetch_rows("p", "a", "b", ["page"], "tok", http_post=post) == []


# ---- opportunity logic ----

def test_host_of_and_filter_rows_by_host():
    assert g.host_of("https://khoahoc.erx.vn/course/x") == "khoahoc.erx.vn"
    rows = [_row(["https://erx.vn/a", "q1"], 1, 10, 5), _row(["https://khoahoc.erx.vn/b", "q2"], 1, 10, 5)]
    assert [r["keys"][1] for r in g.filter_rows_by_host(rows, "khoahoc.erx.vn")] == ["q2"]
    assert len(g.filter_rows_by_host(rows, None)) == 2


def test_striking_distance_keeps_queries_in_position_window_sorted_by_impressions():
    rows = [
        _row(["p", "high-impr"], 5, 300, 6.0),
        _row(["p", "already-top"], 50, 400, 1.5),
        _row(["p", "too-low"], 0, 500, 40.0),
        _row(["p", "small"], 0, 10, 8.0),
        _row(["p", "mid"], 1, 120, 12.0),
    ]
    out = g.striking_distance(rows)
    assert [o["query"] for o in out] == ["high-impr", "mid"]


def test_low_ctr_pages_estimates_gain_at_target_ctr():
    rows = [
        _row(["https://erx.vn/a"], 84, 8710, 5.1),     # CTR 0.96%
        _row(["https://erx.vn/b"], 200, 2000, 5.0),    # CTR 10% fine
        _row(["https://erx.vn/c"], 1, 100, 5.0),       # too few impressions
    ]
    out = g.low_ctr_pages(rows)
    assert [o["url"] for o in out] == ["https://erx.vn/a"]
    assert out[0]["potential_gain"] == int(8710 * 0.04 - 84)


def test_real_query_impressions_matches_tokens():
    queries = {"hàm tách ký tự trong excel": 193, "hàm vstack trong excel": 85}
    assert g.real_query_impressions("hàm tách ký tự excel", queries) == 193
    assert g.real_query_impressions("khóa học procurement", queries) == 0


# ---- daemon integration: real demand breaks ties between equally scored keywords ----

def test_keyword_selection_prefers_keywords_with_real_search_demand():
    platform = load_config()["platforms"][0]
    pages = [{"url": platform["base_url"], "title": "", "meta_description": "", "h1": [], "h2": []}]
    discovered = ["dự báo nhu cầu bằng excel", "lập tiến độ dự án bằng gantt"]
    base = dict(platform=platform, discovered_keywords=discovered, live_platform_pages=pages,
                competitor_signals=[], seo_state={"optimized_keywords": {}}, top_n=2)
    plain = evaluate_and_select_keywords(**base)
    boosted = evaluate_and_select_keywords(**base, real_queries={"lập tiến độ dự án bằng gantt chart": 400})
    assert boosted[0]["keyword"] == "lập tiến độ dự án bằng gantt"
    assert boosted[0]["gsc_impressions"] == 400
    assert all("gsc_impressions" in c for c in plain)


def test_opportunity_report_markdown_lists_pages_and_queries(tmp_path):
    data = {"erx-main": {
        "domain": "erx.vn", "property": "sc-domain:erx.vn",
        "pages": [_row(["https://erx.vn/a"], 84, 8710, 5.1)],
        "page_queries": [_row(["https://erx.vn/a", "hàm tách ký tự"], 1, 193, 4.7)],
    }}
    path = tmp_path / "r.md"
    g.write_opportunity_report(path, data, "2026-10-01", "2026-10-28")
    text = path.read_text(encoding="utf-8")
    assert "https://erx.vn/a" in text and "hàm tách ký tự" in text and "8710" in text


def test_fetch_rows_sends_quota_project_header_when_given():
    seen = {}

    def post(url, data, headers):
        seen.update(headers)
        return {"rows": []}

    g.fetch_rows("p", "a", "b", ["page"], "tok", http_post=post, quota_project="my-proj")
    assert seen["X-Goog-User-Project"] == "my-proj"
    seen.clear()
    g.fetch_rows("p", "a", "b", ["page"], "tok", http_post=post)
    assert "X-Goog-User-Project" not in seen


def test_collect_platform_data_passes_quota_project_and_splits_by_host():
    calls = []

    def post(url, data, headers):
        calls.append(headers.get("X-Goog-User-Project"))
        dims = json.loads(data.decode())["dimensions"]
        rows = [_row(["https://erx.vn/a"] + (["q"] if "query" in dims else []), 1, 10, 5),
                _row(["https://khoahoc.erx.vn/b"] + (["q"] if "query" in dims else []), 2, 20, 6)]
        return {"rows": rows}

    plats = [{"id": "erx-main", "domain": "erx.vn", "gsc_property": "sc-domain:erx.vn"},
             {"id": "khoahoc", "domain": "khoahoc.erx.vn", "gsc_property": "sc-domain:erx.vn"}]
    out = g.collect_platform_data(plats, "2026-10-01", "2026-10-28", "tok", http_post=post, quota_project="proj")
    assert set(calls) == {"proj"} and len(calls) == 2  # one property, two dimension sets
    assert [r["keys"][0] for r in out["erx-main"]["pages"]] == ["https://erx.vn/a"]
    assert [r["keys"][0] for r in out["khoahoc"]["pages"]] == ["https://khoahoc.erx.vn/b"]


def test_default_http_post_error_message_includes_response_body(monkeypatch):
    import io
    import urllib.error

    def fake_urlopen(req, timeout=0):
        raise urllib.error.HTTPError("u", 403, "Forbidden", {}, io.BytesIO(b'{"error":{"message":"API disabled"}}'))

    monkeypatch.setattr(g.urllib.request, "urlopen", fake_urlopen)
    try:
        g.default_http_post("https://x", b"", {})
        assert False, "expected an error"
    except RuntimeError as exc:
        assert "403" in str(exc) and "API disabled" in str(exc)
