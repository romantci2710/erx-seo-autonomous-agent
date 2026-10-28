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
