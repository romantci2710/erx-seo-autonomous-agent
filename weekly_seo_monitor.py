#!/usr/bin/env python3
"""
ERX Ecosystem — Weekly Automated SEO Auditor & Monitor
Monitors all 5 ERX domains across the 3 Google Search Console properties:
  1. https://erx.vn/
  2. https://khoahoc.erx.vn/
  3. https://doc-translate.erx.vn/
  4. https://community.erx.vn/
  5. https://project-management.erx.vn/

Checks:
  - Uptime, HTTP status, TTFB (detects Railway sleeping or 502/503 errors)
  - robots.txt and sitemap.xml validity & URL counts
  - On-page SEO tags (<title>, <meta name="description">, <link rel="canonical">, JSON-LD)
  - Scans recent/top articles in erx.vn/sitemap.xml for:
      * Empty <meta name="description">
      * ALL-CAPS <title> or duplicate <meta name="description">
      * Uncompressed inline data:image/png;base64 payloads (>300 KB)
  - Verifies critical 301 redirects on erx.vn
"""

from __future__ import annotations

import concurrent.futures
import datetime as dt
import html
import json
import re
import ssl
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (compatible; ERX-SEO-Monitor/1.0; +https://erx.vn)"
SSL_CTX = ssl.create_default_context()

SITES = [
    {
        "name": "erx.vn (Main Portal & Blog)",
        "gsc_property": "sc-domain:erx.vn",
        "base_url": "https://erx.vn/",
        "robots_url": "https://erx.vn/robots.txt",
        "sitemap_url": "https://erx.vn/sitemap.xml",
        "expect_canonical": True,
    },
    {
        "name": "khoahoc.erx.vn (Hoola LMS)",
        "gsc_property": "sc-domain:erx.vn",
        "base_url": "https://khoahoc.erx.vn/",
        "robots_url": "https://khoahoc.erx.vn/robots.txt",
        "sitemap_url": "https://khoahoc.erx.vn/sitemap.xml",
        "expect_canonical": False,  # Meteor/Vue SPA sets meta via client runtime
    },
    {
        "name": "doc-translate.erx.vn (AI PDF Translator)",
        "gsc_property": "sc-domain:doc-translate.erx.vn",
        "base_url": "https://doc-translate.erx.vn/",
        "robots_url": "https://doc-translate.erx.vn/robots.txt",
        "sitemap_url": "https://doc-translate.erx.vn/sitemap.xml",
        "expect_canonical": True,
    },
    {
        "name": "doc-builder.erx.vn (AI Doc Builder & Audit)",
        "gsc_property": "sc-domain:doc-builder.erx.vn",
        "base_url": "https://doc-builder.erx.vn/",
        "robots_url": "https://doc-builder.erx.vn/robots.txt",
        "sitemap_url": "https://doc-builder.erx.vn/sitemap.xml",
        "expect_canonical": True,
    },
    {
        "name": "community.erx.vn (Supply Chain Community)",
        "gsc_property": "https://community.erx.vn/",
        "base_url": "https://community.erx.vn/",
        "robots_url": "https://community.erx.vn/robots.txt",
        "sitemap_url": "https://community.erx.vn/sitemap.xml",
        "expect_canonical": True,
    },
    {
        "name": "project-management.erx.vn (AI Gantt Planner)",
        "gsc_property": "sc-domain:project-management.erx.vn",
        "base_url": "https://project-management.erx.vn/",
        "robots_url": "https://project-management.erx.vn/robots.txt",
        "sitemap_url": "https://project-management.erx.vn/sitemap.xml",
        "expect_canonical": True,
    },
]

SAMPLE_REDIRECT_CHECKS = [
    (
        "https://erx.vn/tong-hop-du-lieu-tu-nhieu-",
        "https://erx.vn/tong-hop-du-lieu-tu-nhieu-sheet-trong-cung-1-file-bang-ham-vstack-7123653300.html",
    ),
    (
        "https://erx.vn/sql-in-excel-level-01-data-analysis-automated-reports-dashboard-90302334.html",
        "https://erx.vn/sql-in-excel.html",
    ),
    (
        "https://erx.vn/khoa-hoc-chuyen-vien-mua-hang-hands-on-procurement-905837736.html",
        "https://erx.vn/procurement-management.html",
    ),
]


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_url(url: str, timeout: int = 20, follow_redirects: bool = True, retries: int = 2) -> dict[str, Any]:
    for attempt in range(retries + 1):
        t0 = time.perf_counter()
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        opener = (
            urllib.request.build_opener(urllib.request.HTTPSHandler(context=SSL_CTX))
            if follow_redirects
            else urllib.request.build_opener(
                urllib.request.HTTPSHandler(context=SSL_CTX), NoRedirectHandler()
            )
        )
        try:
            with opener.open(req, timeout=timeout) as resp:
                raw = resp.read()
                elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
                return {
                    "ok": True,
                    "status": resp.status,
                    "url": resp.geturl(),
                    "headers": {k.lower(): v for k, v in resp.headers.items()},
                    "bytes": len(raw),
                    "text": raw.decode("utf-8", errors="replace"),
                    "elapsed_ms": elapsed_ms,
                }
        except urllib.error.HTTPError as exc:
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
            return {
                "ok": False,
                "status": exc.code,
                "url": url,
                "headers": {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {},
                "bytes": 0,
                "text": "",
                "elapsed_ms": elapsed_ms,
            }
        except Exception as exc:
            if attempt < retries:
                time.sleep(0.5 * (attempt + 1))
                continue
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
            return {
                "ok": False,
                "status": 0,
                "url": url,
                "headers": {},
                "bytes": 0,
                "text": "",
                "error": str(exc),
                "elapsed_ms": elapsed_ms,
            }


def parse_html_seo(html_text: str) -> dict[str, Any]:
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html_text, re.I | re.S)
    title = html.unescape(title_match.group(1).strip()) if title_match else ""

    desc_match = re.search(
        r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
        html_text,
        re.I | re.S,
    )
    if not desc_match:
        desc_match = re.search(
            r'<meta\s+[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\']',
            html_text,
            re.I | re.S,
        )
    meta_desc = html.unescape(desc_match.group(1).strip()) if desc_match else ""

    canon_match = re.search(
        r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']',
        html_text,
        re.I | re.S,
    )
    if not canon_match:
        canon_match = re.search(
            r'<link\s+[^>]*href=["\'](.*?)["\'][^>]*rel=["\']canonical["\']',
            html_text,
            re.I | re.S,
        )
    canonical = canon_match.group(1).strip() if canon_match else ""

    jsonld_count = len(
        re.findall(r'<script[^>]*type=["\']application/ld\+json["\']', html_text, re.I)
    )
    png_b64_matches = re.findall(r"data:image/png;base64,[A-Za-z0-9+/=]+", html_text)
    png_b64_bytes = sum(len(m) for m in png_b64_matches)

    return {
        "title": title,
        "meta_description": meta_desc,
        "canonical": canonical,
        "jsonld_count": jsonld_count,
        "png_base64_count": len(png_b64_matches),
        "png_base64_kb": round(png_b64_bytes / 1024, 1),
    }


def extract_sitemap_locs(xml_text: str) -> list[str]:
    try:
        root = ET.fromstring(xml_text.lstrip("\ufeff \t\r\n"))
        locs = []
        for elem in root.iter():
            if elem.tag.endswith("loc") and elem.text:
                locs.append(elem.text.strip())
        return locs
    except Exception:
        return re.findall(r"<loc>(.*?)</loc>", xml_text)


def run_audit() -> dict[str, Any]:
    now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report: dict[str, Any] = {
        "generated_at": now_str,
        "sites": [],
        "erx_article_alerts": [],
        "redirect_checks": [],
        "action_items": [],
    }

    for site in SITES:
        res = fetch_url(site["base_url"])
        seo = parse_html_seo(res["text"]) if res["ok"] else {}
        robots_ok = None
        if site["robots_url"]:
            r_res = fetch_url(site["robots_url"])
            robots_ok = r_res["ok"] and "user-agent" in r_res["text"].lower()

        sitemap_count = None
        sitemap_locs: list[str] = []
        if site["sitemap_url"]:
            s_res = fetch_url(site["sitemap_url"])
            if s_res["ok"]:
                sitemap_locs = extract_sitemap_locs(s_res["text"])
                sitemap_count = len(sitemap_locs)

        issues: list[str] = []
        if not res["ok"] or res["status"] != 200:
            issues.append(f"HTTP status {res['status']} on {site['base_url']}")
        if res["elapsed_ms"] > 5000:
            issues.append(f"Slow response ({res['elapsed_ms']} ms)")
        if site["expect_canonical"] and not seo.get("canonical"):
            issues.append("Missing <link rel='canonical'>")
        if site["expect_canonical"] and not seo.get("meta_description"):
            issues.append("Missing <meta name='description'>")
        if site["robots_url"] and not robots_ok:
            issues.append("Invalid or missing robots.txt")
        if site["sitemap_url"] and not sitemap_count:
            issues.append("Empty or unreachable sitemap.xml")

        site_entry = {
            "name": site["name"],
            "gsc_property": site["gsc_property"],
            "base_url": site["base_url"],
            "status": res["status"],
            "elapsed_ms": res["elapsed_ms"],
            "html_kb": round(res["bytes"] / 1024, 1),
            "title": seo.get("title", ""),
            "meta_description_len": len(seo.get("meta_description", "")),
            "canonical": seo.get("canonical", ""),
            "jsonld_count": seo.get("jsonld_count", 0),
            "robots_ok": robots_ok,
            "sitemap_url_count": sitemap_count,
            "issues": issues,
        }
        report["sites"].append(site_entry)
        for iss in issues:
            report["action_items"].append(f"[{site['name']}] {iss}")

        # Scan all articles in erx.vn/sitemap.xml in parallel for missing meta description or heavy PNG base64
        if site["base_url"] == "https://erx.vn/" and sitemap_locs:
            article_urls = [u for u in sitemap_locs if re.search(r"-\d{9,12}\.html$", u)]

            def _check_article(art_url: str) -> dict[str, Any] | None:
                a_res = fetch_url(art_url, timeout=15)
                if not a_res["ok"]:
                    return {"url": art_url, "html_kb": 0, "issues": [f"HTTP {a_res['status']}"]}
                a_seo = parse_html_seo(a_res["text"])
                art_issues = []
                if not a_seo["meta_description"]:
                    art_issues.append("Empty <meta name='description'>")
                elif a_seo["meta_description"] == a_seo["title"] and (
                    a_seo["title"].isupper() or len(a_seo["meta_description"]) < 90
                ):
                    art_issues.append("Duplicate/ALL-CAPS <meta name='description'>")
                if a_seo["png_base64_kb"] > 300:
                    art_issues.append(
                        f"Uncompressed inline PNG Base64 ({a_seo['png_base64_count']} imgs, {a_seo['png_base64_kb']} KB)"
                    )
                if art_issues:
                    return {
                        "url": art_url,
                        "title": a_seo["title"],
                        "html_kb": round(a_res["bytes"] / 1024, 1),
                        "png_base64_kb": a_seo["png_base64_kb"],
                        "png_base64_count": a_seo["png_base64_count"],
                        "issues": art_issues,
                    }
                return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                for res_item in pool.map(_check_article, article_urls):
                    if res_item:
                        report["erx_article_alerts"].append(res_item)

            report["erx_article_alerts"].sort(
                key=lambda x: x.get("html_kb", 0), reverse=True
            )

        # Scan all URLs in community.erx.vn, doc-translate.erx.vn, and doc-builder.erx.vn sitemaps
        if site["base_url"] in (
            "https://community.erx.vn/",
            "https://doc-translate.erx.vn/",
            "https://doc-builder.erx.vn/",
        ) and sitemap_locs:
            def _check_comm_url(c_url: str) -> str | None:
                c_res = fetch_url(c_url, timeout=15)
                if not c_res["ok"] or c_res["status"] != 200:
                    return f"{c_url}: HTTP {c_res['status']}"
                c_seo = parse_html_seo(c_res["text"])
                t_len = len(c_seo["title"])
                d_len = len(c_seo["meta_description"])
                if t_len < 45 or t_len > 75:
                    return f"{c_url}: <title> length {t_len} outside 45-75 chars"
                if d_len < 110:
                    return f"{c_url}: <meta description> length {d_len} < 110 chars"
                if not c_seo["canonical"]:
                    return f"{c_url}: Missing canonical link"
                if c_seo["jsonld_count"] < 1:
                    return f"{c_url}: Missing JSON-LD structured data"
                if "Chưa có chủ đề nào." in c_res["text"]:
                    return f"{c_url}: Empty category ('Chưa có chủ đề nào.')"
                return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                for c_issue in pool.map(_check_comm_url, sitemap_locs):
                    if c_issue:
                        site_entry["issues"].append(c_issue)
                        report["action_items"].append(f"[{site['name']}] {c_issue}")

    for src, expected_dest in SAMPLE_REDIRECT_CHECKS:
        r_check = fetch_url(src, follow_redirects=False)
        loc = r_check["headers"].get("location", "")
        ok = r_check["status"] == 301 and loc == expected_dest
        report["redirect_checks"].append(
            {
                "source": src,
                "status": r_check["status"],
                "location": loc,
                "expected": expected_dest,
                "ok": ok,
            }
        )
        if not ok:
            report["action_items"].append(
                f"[Redirect Failure] {src} returned {r_check['status']} -> {loc}"
            )

    return report


def write_reports(report: dict[str, Any]) -> tuple[Path, Path]:
    date_tag = dt.datetime.now().strftime("%Y-%m-%d")
    json_path = REPORTS_DIR / "latest_seo_report.json"
    md_path = REPORTS_DIR / f"weekly_seo_report_{date_tag}.md"
    latest_md_path = REPORTS_DIR / "latest_seo_report.md"

    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# Báo cáo Giám sát SEO Định kỳ Hệ sinh thái ERX ({report['generated_at']})",
        "",
        "## 1. Trạng thái Sức khỏe 6 Website (5 Google Search Console Properties)",
        "",
        "| Website | HTTP | Phản hồi | Dung lượng HTML | Canonical | Robots.txt | Sitemap URLs | Trạng thái |",
        "|---|---:|---:|---:|---|---|---:|---|",
    ]
    for s in report["sites"]:
        status_badge = "✅ OK" if not s["issues"] else "⚠️ " + "; ".join(s["issues"])
        canon_badge = "✅" if s["canonical"] else ("➖ SPA" if "khoahoc" in s["base_url"] else "❌")
        rob_badge = "✅" if s["robots_ok"] else ("➖" if s["robots_ok"] is None else "❌")
        sm_count = str(s["sitemap_url_count"]) if s["sitemap_url_count"] is not None else "➖"
        lines.append(
            f"| **{s['name']}** | `{s['status']}` | `{s['elapsed_ms']} ms` | `{s['html_kb']} KB` | {canon_badge} | {rob_badge} | `{sm_count}` | {status_badge} |"
        )

    lines.extend(
        [
            "",
            "## 2. Kiểm tra 301 Redirect trên `erx.vn`",
            "",
            "| URL Nguồn | Mã HTTP | Đích Chuyển hướng | Kết quả |",
            "|---|---:|---|---|",
        ]
    )
    for rc in report["redirect_checks"]:
        badge = "✅ Chuẩn" if rc["ok"] else "❌ Lỗi"
        lines.append(f"| `{rc['source']}` | `{rc['status']}` | `{rc['location']}` | {badge} |")

    lines.extend(
        [
            "",
            "## 3. Các bài viết trên `erx.vn` cần tối ưu thêm (`Meta Description` / Nén ảnh Base64 WebP)",
            "",
        ]
    )
    if not report["erx_article_alerts"]:
        lines.append("- ✅ Toàn bộ 15 bài viết kiểm tra trong Sitemap đều đã đạt chuẩn!")
    else:
        lines.append("| URL Bài viết | Dung lượng HTML | Hạng mục cần tự động tối ưu trên `erx.vn/administrator` |")
        lines.append("|---|---:|---|")
        for alert in report["erx_article_alerts"]:
            iss_str = ", ".join(alert.get("issues", [alert.get("issue", "")]))
            lines.append(f"| `{alert['url']}` | `{alert.get('html_kb', 0)} KB` | {iss_str} |")

    md_content = "\n".join(lines) + "\n"
    md_path.write_text(md_content, encoding="utf-8")
    latest_md_path.write_text(md_content, encoding="utf-8")
    return json_path, md_path


if __name__ == "__main__":
    audit_data = run_audit()
    j_file, m_file = write_reports(audit_data)
    print(f"Saved JSON report: {j_file}")
    print(f"Saved Markdown report: {m_file}")
    print(f"Sites checked: {len(audit_data['sites'])}, Action items: {len(audit_data['action_items'])}, Article alerts: {len(audit_data['erx_article_alerts'])}")
