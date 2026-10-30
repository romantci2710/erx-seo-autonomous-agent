# -*- coding: utf-8 -*-
"""Meta-description fitting, advisory page audit and keyword quality filter."""
from muse_seo_daemon import (
    audit_advisory_seo,
    audit_single_page_seo,
    build_keyword_seo_package,
    evaluate_and_select_keywords,
    extract_page_seo_signals,
    fit_meta_description,
    is_low_quality_keyword,
    load_config,
    now_vn,
    synthesize_remediation_for_page,
)

REAL_KEYWORDS = [
    "sơ đồ gantt online",
    "công cụ dịch pdf chuyên ngành",
    "tạo báo cáo chuyên nghiệp bằng ai",
    "phân tích chi phí mua hàng spend analysis",
    "khóa học mua hàng thực chiến procurement",
    "khóa học phân tích dữ liệu chuỗi cung ứng",
    "dịch file pdf giữ nguyên định dạng",
    "soạn thảo hợp đồng bằng ai",
    "tiêu chí đánh giá nhà cung cấp",
    "truy vấn sql trong excel",
    "khóa học excel 365 nâng cao cho doanh nghiệp",
    "phần mềm lập tiến độ dự án",
    "viết báo cáo quản trị tự động",
    "phân tích dữ liệu power bi dax",
    "đào tạo mua hàng thực chiến hands on procurement",
]


# ---- 1. meta description: no hard cut, varied openers ----

def test_fit_meta_description_never_appends_ellipsis_or_cuts_mid_word():
    short = "Mô tả ngắn gọn."
    assert fit_meta_description(short) == short
    out = fit_meta_description(("Từ " * 80).strip())
    assert len(out) <= 160
    assert not out.endswith(("...", "…"))
    assert out.endswith(".")
    assert len(fit_meta_description("a" * 400, limit=160)) <= 160


def test_fit_meta_description_drops_dangling_connector():
    text = "Hướng dẫn chi tiết cách quản lý " + "dự án " * 20 + "và"
    out = fit_meta_description(text, limit=60)
    assert len(out) <= 60
    assert not out.rstrip(".").endswith((" và", " với", " cho", " của"))


def test_package_meta_descriptions_are_clean_and_varied():
    cfg = load_config()
    openers = set()
    for i, kw in enumerate(REAL_KEYWORDS):
        platform = cfg["platforms"][i % len(cfg["platforms"])]
        cand = {
            "keyword": kw,
            "target_url": platform["base_url"],
            "intent": "x",
            "priority_score": 80,
            "coverage_status": "UNCOVERED_HIGH_OPPORTUNITY",
            "target_outrank_words": 1500,
        }
        meta = build_keyword_seo_package(cand, platform, [])["recommended_meta_description"]
        assert 145 <= len(meta) <= 160, (kw, len(meta), meta)
        assert not meta.endswith(("...", "…")), meta
        assert kw.lower() in meta.lower(), (kw, meta)
        openers.add(meta[:12])
    assert len(openers) >= 3


def test_remediation_meta_description_has_no_ellipsis():
    sig = {
        "url": "https://erx.vn/x-7123456789.html",
        "title": "Một tiêu đề đủ dài để không bị bổ sung hậu tố thương hiệu | ERX",
        "meta_description": "",
        "h2": [
            "Phân tích chi tiết hệ thống quản trị chuỗi cung ứng hiện đại cho doanh nghiệp sản xuất",
            "Quy trình lựa chọn và đánh giá nhà cung cấp theo tiêu chí đa chiều",
            "Kiểm soát chi phí mua hàng bằng phân tích spend analysis chuyên sâu",
        ],
    }
    meta = synthesize_remediation_for_page(sig, "erx.vn", ["MISSING_META_DESCRIPTION"])[
        "recommended_meta_description"
    ]
    assert len(meta) <= 160
    assert not meta.endswith(("...", "…"))


# ---- 2. page audit: title length, H1, twitter card, image dimensions ----

GOOD_HEAD = (
    "<title>Tiêu đề trang chủ vừa đủ dài để đạt chuẩn SEO | ERX</title>"
    '<meta name="description" content="' + "Mô tả đủ dài. " * 8 + '" />'
    '<link rel="canonical" href="https://erx.vn/" />'
    '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization"}</script>'
)
H1_OK = "<h1>Tiêu đề chính</h1>"


def _page(head=GOOD_HEAD, body=H1_OK):
    return extract_page_seo_signals(f"<html><head>{head}</head><body>{body}</body></html>", "https://erx.vn/")


def test_audit_flags_long_title():
    long_title = "ERX - Trung tâm đào tạo thực chiến phân tích dữ liệu & quản lý chuỗi cung ứng"
    sig = _page(head=f"<title>{long_title}</title>")
    assert any(i.startswith("LONG_TITLE") for i in audit_advisory_seo(sig, "erx.vn"))
    assert not any(i.startswith("LONG_TITLE") for i in audit_advisory_seo(_page(), "erx.vn"))


def test_audit_flags_h1_without_text():
    logo_only = _page(body='<h1><img src="/l.png" alt="logo"/></h1>')
    assert "EMPTY_H1" in audit_advisory_seo(logo_only, "erx.vn")
    no_h1 = _page(body="<h2>Chỉ có H2</h2>")
    assert "MISSING_H1" in audit_advisory_seo(no_h1, "erx.vn")
    advisories = audit_advisory_seo(_page(), "erx.vn")
    assert "EMPTY_H1" not in advisories and "MISSING_H1" not in advisories


def test_audit_flags_empty_twitter_card_only_when_tag_present_but_empty():
    empty = _page(head=GOOD_HEAD + '<meta name="twitter:card" content="" />')
    filled = _page(head=GOOD_HEAD + '<meta name="twitter:card" content="summary_large_image" />')
    assert "EMPTY_TWITTER_CARD" in audit_advisory_seo(empty, "erx.vn")
    assert "EMPTY_TWITTER_CARD" not in audit_advisory_seo(_page(), "erx.vn")
    assert "EMPTY_TWITTER_CARD" not in audit_advisory_seo(filled, "erx.vn")


def test_audit_flags_images_missing_dimensions():
    bad = "".join(f'<img src="/{i}.png" alt="a"/>' for i in range(4))
    good = "".join(f'<img src="/{i}.png" alt="a" width="10" height="10"/>' for i in range(4))
    sig = _page(body=H1_OK + bad)
    assert sig["img_total"] == 4 and sig["img_missing_dims"] == 4
    assert any(i.startswith("IMAGES_MISSING_DIMENSIONS") for i in audit_advisory_seo(sig, "erx.vn"))
    assert not any(
        i.startswith("IMAGES_MISSING_DIMENSIONS") for i in audit_advisory_seo(_page(body=H1_OK + good), "erx.vn")
    )


def test_advisories_do_not_change_blocking_issues_or_fingerprint():
    plain = _page()
    with_imgs = _page(body=H1_OK + '<img src="/a.png"/>')
    assert audit_single_page_seo(with_imgs, "erx.vn") == []
    assert plain["fingerprint"] == with_imgs["fingerprint"]


# ---- 3. keyword quality filter ----

def _select(discovered, history=None, top_n=1):
    platform = load_config()["platforms"][0]
    return evaluate_and_select_keywords(
        platform=platform,
        discovered_keywords=discovered,
        live_platform_pages=[
            {"url": platform["base_url"], "title": "", "meta_description": "", "h1": [], "h2": []}
        ],
        competitor_signals=[],
        seo_state={"optimized_keywords": history or {}},
        top_n=top_n,
    )


def test_keyword_filter_rejects_leading_filler_words():
    assert is_low_quality_keyword("về sơ đồ gantt online")
    assert is_low_quality_keyword("của phần mềm quản lý dự án")
    assert not is_low_quality_keyword("sơ đồ gantt online")


def test_keyword_filter_detects_near_duplicates_of_recent_history():
    pid = load_config()["platforms"][0]["id"]
    recent = now_vn().isoformat()

    history = {f"{pid}::tiêu chí đánh giá nhà cung cấp": recent}
    out = _select(["7 tiêu chí đánh giá nhà cung cấp", "lập tiến độ dự án bằng gantt"], history, top_n=2)
    kws = [c["keyword"] for c in out]
    assert "7 tiêu chí đánh giá nhà cung cấp" not in kws
    assert "lập tiến độ dự án bằng gantt" in kws

    history = {f"{pid}::dịch file pdf giữ nguyên định dạng": recent}
    out = _select(["dịch file pdf giữ nguyên định dạng free", "tạo sơ đồ gantt từ excel"], history, top_n=2)
    assert "dịch file pdf giữ nguyên định dạng free" not in [c["keyword"] for c in out]


def test_keyword_filter_dedups_within_a_single_selection():
    out = _select(["sơ đồ gantt online", "sơ đồ gantt online free", "về sơ đồ gantt online"], top_n=3)
    assert [c["keyword"] for c in out] == ["sơ đồ gantt online"]


def test_meta_description_length_holds_for_all_templates_domains_and_keyword_lengths():
    from muse_seo_daemon import META_DESCRIPTION_TEMPLATES, compose_meta_description

    words = "dịch tài liệu pdf chuyên ngành bằng công cụ ai cho doanh nghiệp sản xuất vừa và nhỏ".split()
    domains = [p["domain"] for p in load_config()["platforms"]]
    checked = 0
    for core, clauses in META_DESCRIPTION_TEMPLATES:
        for domain in domains:
            for n in range(2, 12):
                kw = " ".join(words[:n])
                if not 10 <= len(kw) <= 60:
                    continue
                fmt = {"kw": kw, "Kw": kw[:1].upper() + kw[1:], "d": domain}
                meta = compose_meta_description(core.format(**fmt), tuple(c.format(**fmt) for c in clauses))
                assert 145 <= len(meta) <= 160, (core, domain, kw, len(meta), meta)
                assert not meta.endswith(("...", "…"))
                checked += 1
    assert checked > 200
