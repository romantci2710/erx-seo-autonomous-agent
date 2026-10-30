# -*- coding: utf-8 -*-
import json
from pathlib import Path

from muse_seo_daemon import (
    audit_single_page_seo,
    build_keyword_seo_package,
    classify_keyword_intent,
    evaluate_and_select_keywords,
    extract_page_seo_signals,
    load_config,
    synthesize_remediation_for_page,
)


def test_config_loads_all_six_platforms():
    cfg = load_config()
    platforms = cfg.get("platforms", [])
    assert len(platforms) == 6
    ids = {p["id"] for p in platforms}
    assert {
        "project-management",
        "doc-translate",
        "doc-builder",
        "community",
        "erx-main",
        "khoahoc",
    } == ids


def test_extract_page_seo_signals_and_audit():
    sample_html = """
    <html>
      <head>
        <title>Phần mềm Quản lý Dự án &amp; Sơ đồ Gantt Online Miễn Phí | ERX</title>
        <meta name="description" content="Giải pháp quản lý dự án trực tuyến chuẩn PMBOK 8 với sơ đồ Gantt, WBS và Earned Value Management (EVM) tự động hoá bằng AI từ ERX Việt Nam." />
        <link rel="canonical" href="https://project-management.erx.vn/phan-mem-quan-ly-du-an" />
        <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage"}</script>
      </head>
      <body>
        <h1>Phần mềm Quản lý Dự án Chuẩn PMBOK 8</h1>
        <h2>Tính năng Sơ đồ Gantt Online</h2>
        <table><tr><td>A</td><td>B</td></tr></table>
      </body>
    </html>
    """
    sig = extract_page_seo_signals(
        sample_html, "https://project-management.erx.vn/phan-mem-quan-ly-du-an"
    )
    assert "Phần mềm Quản lý Dự án" in sig["title"]
    assert sig["table_count"] == 1
    assert "FAQPage" in sig["schema_types"]
    issues = audit_single_page_seo(sig, "project-management.erx.vn")
    assert issues == []


def test_audit_detects_defects_and_synthesizes_remediation():
    bad_html = "<html><head><title>SHORT TITLE</title></head><body><h1>Quản lý chi phí mua hàng</h1></body></html>"
    sig = extract_page_seo_signals(bad_html, "https://erx.vn/test-article-7123456789.html")
    issues = audit_single_page_seo(sig, "erx.vn")
    assert any("SHORT_TITLE" in x for x in issues)
    assert "MISSING_META_DESCRIPTION" in issues
    assert "MISSING_CANONICAL" in issues

    rem = synthesize_remediation_for_page(sig, "erx.vn", issues)
    assert len(rem["recommended_title"]) >= 35
    assert 70 <= len(rem["recommended_meta_description"]) <= 160


def test_evaluate_and_select_keywords_and_package():
    cfg = load_config()
    pm_platform = cfg["platforms"][0]
    discovered = [
        "phần mềm quản lý dự án xây dựng miễn phí",
        "cách vẽ sơ đồ gantt online",
    ]
    live_pages = [
        {
            "url": "https://project-management.erx.vn/",
            "title": "AI Project Gantt Planner",
            "meta_description": "Gantt Planner",
            "h1": ["AI Project Gantt Planner"],
            "h2": ["WBS & Gantt"],
        }
    ]
    comp_signals = [
        {"domain": "1office.vn", "word_count": 1500, "table_count": 1, "schema_types": ["FAQPage"], "h2": ["Phần mềm quản lý dự án là gì?"]}
    ]
    selected = evaluate_and_select_keywords(
        platform=pm_platform,
        discovered_keywords=discovered,
        live_platform_pages=live_pages,
        competitor_signals=comp_signals,
        seo_state={"optimized_keywords": {}},
        top_n=1,
    )
    assert len(selected) == 1
    cand = selected[0]
    assert cand["priority_score"] >= 70

    pkg = build_keyword_seo_package(cand, pm_platform, comp_signals)
    assert pkg["keyword"] == cand["keyword"]
    assert len(pkg["recommended_title"]) <= 65
    assert len(pkg["recommended_meta_description"]) <= 160
    assert pkg["faq_jsonld"]["@type"] == "FAQPage"
    assert "<table" in pkg["pillar_html_snippet"]


# ---- honesty of CMS / IndexNow reporting and TLS verification ----

def test_ssl_context_verifies_certificates_by_default():
    import ssl
    from muse_seo_daemon import build_ssl_context

    ctx = build_ssl_context(insecure=False)
    assert ctx.verify_mode == ssl.CERT_REQUIRED
    assert ctx.check_hostname is True


def test_ssl_context_insecure_is_explicit_opt_in():
    import ssl
    from muse_seo_daemon import build_ssl_context

    ctx = build_ssl_context(insecure=True)
    assert ctx.verify_mode == ssl.CERT_NONE


def test_cms_update_with_cookie_never_claims_patched(monkeypatch, tmp_path):
    import muse_seo_daemon as d

    monkeypatch.setattr(d, "REPORTS_DIR", tmp_path)
    monkeypatch.setenv("ERX_ADMIN_COOKIE", "session=abc")
    calls = []

    class FakeResp:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(req, timeout=0, context=None):
        calls.append((req.get_method(), req.full_url))
        return FakeResp()

    monkeypatch.setattr(d.urllib.request, "urlopen", fake_urlopen)
    patches = [{
        "target_url": "https://erx.vn/bai-viet-123456789012.html",
        "recommended_title": "T",
        "recommended_meta_description": "D",
        "recommended_meta_keywords": "K",
    }]
    result = d.apply_erx_cms_direct_update(patches)

    assert result["patched_count"] == 0
    assert result["mode"] == "staged_session_verified"
    assert result["session_reachable_count"] == 1
    assert all(m == "GET" for m, _ in calls)


def test_cms_update_without_cookie_is_staged(monkeypatch, tmp_path):
    import muse_seo_daemon as d

    monkeypatch.setattr(d, "REPORTS_DIR", tmp_path)
    monkeypatch.delenv("ERX_ADMIN_COOKIE", raising=False)
    result = d.apply_erx_cms_direct_update([])
    assert result["mode"] == "staged_js_payload"
    assert result["patched_count"] == 0


def test_indexnow_skipped_without_key(monkeypatch):
    import muse_seo_daemon as d

    monkeypatch.delenv("INDEXNOW_KEY", raising=False)
    monkeypatch.setattr(d, "http_get", lambda *a, **k: {"ok": True, "status": 200})
    out = d.ping_indexnow_and_warm_cache(["https://erx.vn/a"])
    assert out["indexnow"]["status"] == "skipped_no_key"
    assert out["ssr_warmed_ok"] == 1


def test_indexnow_posts_grouped_by_host_when_key_set(monkeypatch):
    import muse_seo_daemon as d

    monkeypatch.setenv("INDEXNOW_KEY", "k" * 16)
    monkeypatch.setattr(d, "http_get", lambda *a, **k: {"ok": True, "status": 200})
    posted = []

    class FakeResp:
        status = 202

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(req, timeout=0, context=None):
        posted.append((req.get_method(), json.loads(req.data.decode("utf-8"))))
        return FakeResp()

    monkeypatch.setattr(d.urllib.request, "urlopen", fake_urlopen)
    out = d.ping_indexnow_and_warm_cache(
        ["https://erx.vn/a", "https://erx.vn/b", "https://community.erx.vn/c"]
    )
    hosts = {p["host"]: p["urlList"] for _, p in posted}
    assert hosts == {
        "erx.vn": ["https://erx.vn/a", "https://erx.vn/b"],
        "community.erx.vn": ["https://community.erx.vn/c"],
    }
    assert all(m == "POST" for m, _ in posted)
    assert out["indexnow"]["status"] == "submitted"
