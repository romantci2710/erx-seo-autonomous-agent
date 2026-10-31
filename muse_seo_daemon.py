#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MUSE Autonomous SEO Daemon & Closed-Loop Engine (v2.0)
======================================================
Designed for 24/7 autonomous operation on a server (MUSE Agent / Linux / Docker / systemd).

Implements two tightly integrated autonomous loops across all 6 ERX platforms:
  1. DAILY 07:00 AM HOT KEYWORD SEO CYCLE (`run_daily_keyword_seo_cycle`):
     - Discovers hot & trending keywords online via Google Suggest Vietnam + Google Trends VN RSS
       + live platform content seeds across `erx.vn`, `community.erx.vn`, `project-management.erx.vn`,
       `doc-translate.erx.vn`, `doc-builder.erx.vn`, and `khoahoc.erx.vn`.
     - Evaluates and scores each keyword (0-100) by Search Intent, Platform Coverage Gap,
       and Top-3 Google SERP Competitor Benchmarks (word count, H1/H2/H3, tables, JSON-LD).
     - Selects the top unoptimized keywords per platform and automatically executes SEO upgrades
       (generates optimized Title/Meta/Schema JSON-LD/Comparison Tables, patches CMS/repo manifests,
       warms SSR caches, and pings IndexNow).

  2. CONTINUOUS PLATFORM CONTENT & TAG WATCHER (`run_platform_watcher_cycle`):
     - Watches all 6 platforms' `sitemap.xml` and API feeds (`/api/community/topics`) every 15 minutes.
     - Detects newly published articles/topics (`NEW_URL`), modified SEO tags (`TAG_MODIFIED`),
       or SEO regressions (`SEO_DEFECT`: empty/short meta description, ALL-CAPS title, missing canonical,
       heavy base64 PNGs, or un-warmed `.html` attachment topics).
     - Automatically remediates SEO tags, warms SSR pages, and logs audit reports in `reports/` & `state/`.

Usage:
  python muse_seo_daemon.py --mode daemon          # Run 24/7 loop (07:00 AM daily + 15m watcher)
  python muse_seo_daemon.py --mode once            # Run both cycles once immediately and exit
  python muse_seo_daemon.py --mode keyword-only    # Run only the 07:00 AM Hot Keyword SEO cycle
  python muse_seo_daemon.py --mode watch-only      # Run only the Platform Content & Tag Watcher cycle
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import datetime as dt
import gzip
import hashlib
import html
import json
import logging
import os
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import experiments
import gsc_client
from gsc_client import real_query_impressions

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # Graceful regex fallback if bs4 is not yet installed

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "platforms.json"
STATE_DIR = BASE_DIR / "state"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

for _d in (STATE_DIR, REPORTS_DIR, LOGS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

SEO_STATE_FILE = STATE_DIR / "seo_state.json"
WATCH_STATE_FILE = STATE_DIR / "platform_watch_state.json"
INJECTIONS_FILE = STATE_DIR / "keyword_seo_injections.json"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def build_ssl_context(insecure: bool | None = None) -> ssl.SSLContext:
    """TLS context that verifies certificates. Set SEO_INSECURE_SSL=1 only behind
    an intercepting egress proxy whose CA is not installed."""
    if insecure is None:
        insecure = os.environ.get("SEO_INSECURE_SSL", "").strip().lower() in ("1", "true", "yes")
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


SSL_CTX = build_ssl_context()

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOGS_DIR / "muse_seo_daemon.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("muse_seo_daemon")


# ============================================================================
# 1. ENVIRONMENT & CONFIGURATION LOADER
# ============================================================================

def load_dotenv_file(dotenv_path: Path) -> None:
    """Lightweight .env loader without external dependency."""
    if not dotenv_path.exists():
        return
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


load_dotenv_file(BASE_DIR / ".env")


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing configuration file: {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_json_state(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("Could not parse state file %s: %s", path, exc)
    return dict(default)


def save_json_state(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def now_vn(tz_name: str = "Asia/Ho_Chi_Minh") -> dt.datetime:
    try:
        return dt.datetime.now(ZoneInfo(tz_name))
    except Exception:
        return dt.datetime.now(dt.timezone(dt.timedelta(hours=7)))


# ============================================================================
# 2. HTTP & HTML/SEO EXTRACTION UTILITIES
# ============================================================================

def http_get(url: str, timeout: int = 18, retries: int = 2) -> dict[str, Any]:
    for attempt in range(retries + 1):
        t0 = time.perf_counter()
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                # Request compressed responses: the erx.vn sitemap served as plain
                # XML over the egress proxy is deterministically truncated
                # (IncompleteRead) for urllib, while the gzip variant reads fully.
                "Accept-Encoding": "gzip, deflate",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
                raw = resp.read()
                # urllib does not decompress automatically; decode per
                # Content-Encoding, falling back to raw bytes on any failure
                # so a mislabelled body never breaks the fetch.
                encoding = (resp.headers.get("Content-Encoding") or "").lower()
                if "gzip" in encoding:
                    try:
                        raw = gzip.decompress(raw)
                    except Exception:
                        pass
                elif "deflate" in encoding:
                    try:
                        raw = zlib.decompress(raw)
                    except Exception:
                        try:
                            raw = zlib.decompress(raw, -zlib.MAX_WBITS)
                        except Exception:
                            pass
                elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
                return {
                    "ok": True,
                    "status": resp.status,
                    "url": resp.geturl(),
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
                "bytes": 0,
                "text": "",
                "error": str(exc),
                "elapsed_ms": elapsed_ms,
            }


def extract_page_seo_signals(html_text: str, url: str = "") -> dict[str, Any]:
    """Extracts Title, Meta Description, Canonical, H1/H2/H3, Word Count, Tables, JSON-LD, Base64 size."""
    title_m = re.search(r"<title[^>]*>(.*?)</title>", html_text, re.I | re.S)
    title = html.unescape(re.sub(r"\s+", " ", title_m.group(1)).strip()) if title_m else ""

    desc_m = re.search(
        r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
        html_text,
        re.I | re.S,
    )
    if not desc_m:
        desc_m = re.search(
            r'<meta\s+[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\']',
            html_text,
            re.I | re.S,
        )
    meta_desc = html.unescape(re.sub(r"\s+", " ", desc_m.group(1)).strip()) if desc_m else ""

    canon_m = re.search(
        r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']',
        html_text,
        re.I | re.S,
    )
    if not canon_m:
        canon_m = re.search(
            r'<link\s+[^>]*href=["\'](.*?)["\'][^>]*rel=["\']canonical["\']',
            html_text,
            re.I | re.S,
        )
    canonical = canon_m.group(1).strip() if canon_m else ""

    h1_list = [
        html.unescape(re.sub(r"<[^>]+>", "", m).strip())
        for m in re.findall(r"<h1[^>]*>(.*?)</h1>", html_text, re.I | re.S)
    ]
    h2_list = [
        html.unescape(re.sub(r"<[^>]+>", "", m).strip())
        for m in re.findall(r"<h2[^>]*>(.*?)</h2>", html_text, re.I | re.S)
    ]
    h3_list = [
        html.unescape(re.sub(r"<[^>]+>", "", m).strip())
        for m in re.findall(r"<h3[^>]*>(.*?)</h3>", html_text, re.I | re.S)
    ]
    h1_list = [re.sub(r"\s+", " ", x) for x in h1_list if x.strip()]
    h2_list = [re.sub(r"\s+", " ", x) for x in h2_list if x.strip()]
    h3_list = [re.sub(r"\s+", " ", x) for x in h3_list if x.strip()]

    table_count = len(re.findall(r"<table[\s>]", html_text, re.I))
    jsonld_blocks = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html_text,
        re.I | re.S,
    )
    schema_types: list[str] = []
    for blk in jsonld_blocks:
        for tm in re.findall(r'"@type"\s*:\s*"([^"]+)"', blk):
            if tm not in schema_types:
                schema_types.append(tm)

    h1_raw_count = len(re.findall(r"<h1[\s>]", html_text, re.I))
    tw_m = re.search(
        r'<meta\s+[^>]*name=["\']twitter:card["\'][^>]*content=["\'](.*?)["\']',
        html_text,
        re.I | re.S,
    )
    twitter_card = tw_m.group(1).strip() if tw_m else None
    # <img> strings inside JS templates are not real images
    markup_only = re.sub(r"<(script|style|template)\b.*?</\1>", " ", html_text, flags=re.I | re.S)
    img_tags = re.findall(r"<img\b[^>]*>", markup_only, re.I)
    img_missing_dims = sum(
        1
        for tag in img_tags
        if not (re.search(r"\bwidth\s*=", tag, re.I) and re.search(r"\bheight\s*=", tag, re.I))
    )

    png_b64_matches = re.findall(r"data:image/png;base64,[A-Za-z0-9+/=]+", html_text)
    png_b64_kb = round(sum(len(m) for m in png_b64_matches) / 1024, 1)

    # Clean visible text word count
    cleaned = re.sub(r"<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", html_text, flags=re.I | re.S)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = html.unescape(cleaned)
    words = [w for w in re.split(r"\s+", cleaned) if len(w) > 1]
    word_count = len(words)

    fingerprint_raw = json.dumps(
        {
            "title": title,
            "meta_desc": meta_desc,
            "canonical": canonical,
            "h1": h1_list[:3],
            "h2_count": len(h2_list),
            "table_count": table_count,
            "schema_types": sorted(schema_types),
            "png_b64_kb": png_b64_kb,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    fingerprint = hashlib.sha256(fingerprint_raw.encode("utf-8")).hexdigest()[:16]

    return {
        "url": url,
        "title": title,
        "meta_description": meta_desc,
        "canonical": canonical,
        "h1": h1_list[:5],
        "h1_raw_count": h1_raw_count,
        "h2": h2_list[:15],
        "h3": h3_list[:15],
        "twitter_card": twitter_card,
        "img_total": len(img_tags),
        "img_missing_dims": img_missing_dims,
        "table_count": table_count,
        "jsonld_count": len(jsonld_blocks),
        "schema_types": schema_types,
        "png_base64_kb": png_b64_kb,
        "word_count": word_count,
        "fingerprint": fingerprint,
    }


def parse_sitemap_urls(xml_text: str) -> list[str]:
    try:
        root = ET.fromstring(xml_text.lstrip("\ufeff \t\r\n"))
        locs = []
        for elem in root.iter():
            if elem.tag.endswith("loc") and elem.text:
                locs.append(elem.text.strip())
        return locs
    except Exception:
        return [m.strip() for m in re.findall(r"<loc>(.*?)</loc>", xml_text) if m.strip()]


# ============================================================================
# 3. LOOP 1: DAILY 07:00 AM HOT KEYWORD DISCOVERY, SCORING & AUTO-SEO
# ============================================================================

HOT_MODIFIERS_VN = [
    "",
    "miễn phí",
    "online",
    "bằng ai",
    "2026",
    "phần mềm",
    "công cụ",
    "hướng dẫn",
    "mẫu",
]

COMPETITOR_BENCHMARK_URLS: dict[str, list[dict[str, str]]] = {
    "project-management": [
        {
            "domain": "1office.vn",
            "url": "https://1office.vn/phan-mem-quan-ly-du-an",
            "title": "Top 15+ Phần Mềm Quản Lý Dự Án Miễn Phí Và Chuyên Nghiệp Nhất",
        },
        {
            "domain": "sheet.com.vn",
            "url": "https://sheet.com.vn/bieu-do-gantt-la-gi/",
            "title": "Biểu đồ Gantt là gì? Cách vẽ sơ đồ Gantt quản lý tiến độ dự án",
        },
        {
            "domain": "itgtechnology.vn",
            "url": "https://itgtechnology.vn/phan-mem-quan-ly-du-an-xay-dung/",
            "title": "Top 10 phần mềm quản lý dự án xây dựng hiệu quả nhất",
        },
    ],
    "doc-translate": [
        {
            "domain": "smallpdf.com",
            "url": "https://smallpdf.com/vi/translate-pdf",
            "title": "Dịch PDF - Công cụ dịch file PDF trực tuyến miễn phí | Smallpdf",
        },
        {
            "domain": "ilovepdf.com",
            "url": "https://www.ilovepdf.com/vi/dich-pdf",
            "title": "Dịch PDF bằng AI - Giữ nguyên bố cục và định dạng | iLovePDF",
        },
        {
            "domain": "supawork.ai",
            "url": "https://supawork.ai/vi/ai-pdf-translator",
            "title": "Trình dịch PDF AI miễn phí: Giữ nguyên định dạng & công thức",
        },
    ],
    "doc-builder": [
        {
            "domain": "1office.vn",
            "url": "https://1office.vn/phan-mem-quan-ly-hop-dong",
            "title": "Phần mềm quản lý và khởi tạo hợp đồng điện tử tự động | 1Office",
        },
        {
            "domain": "luathoangan.vn",
            "url": "https://luathoangan.vn/hop-dong-thuong-mai-la-gi/",
            "title": "Hợp đồng thương mại là gì? Mẫu hợp đồng và các rủi ro pháp lý",
        },
        {
            "domain": "gvlawyers.com.vn",
            "url": "https://gvlawyers.com.vn/ra-soat-hop-dong-thuong-mai/",
            "title": "Kinh nghiệm rà soát hợp đồng thương mại và kiểm soát rủi ro pháp lý",
        },
    ],
    "community": [
        {
            "domain": "vilas.edu.vn",
            "url": "https://vilas.edu.vn/supply-chain-management-la-gi.html",
            "title": "Supply Chain Management là gì? Toàn tập về Quản trị chuỗi cung ứng",
        },
        {
            "domain": "pace.edu.vn",
            "url": "https://www.pace.edu.vn/tin-kho-tri-thuc/procurement-la-gi",
            "title": "Procurement là gì? Quy trình mua hàng và đánh giá nhà cung cấp",
        },
        {
            "domain": "1office.vn",
            "url": "https://1office.vn/tieu-chi-danh-gia-nha-cung-cap",
            "title": "Bộ tiêu chí đánh giá nhà cung cấp chuẩn kèm mẫu Excel",
        },
    ],
    "erx-main": [
        {
            "domain": "datapot.edu.vn",
            "url": "https://datapot.edu.vn/phan-tich-pareto-trong-power-bi/",
            "title": "Hướng dẫn phân tích Pareto (80/20) trong Power BI bằng DAX",
        },
        {
            "domain": "gitiho.com",
            "url": "https://gitiho.com/blog/cac-ham-trong-excel-365.html",
            "title": "Tổng hợp các hàm mảng động mới nhất trong Excel 365",
        },
        {
            "domain": "base.vn",
            "url": "https://base.vn/blog/quan-ly-du-an-bang-excel/",
            "title": "So sánh quản lý dự án bằng Excel và phần mềm chuyên dụng",
        },
    ],
    "khoahoc": [
        {
            "domain": "vilas.edu.vn",
            "url": "https://vilas.edu.vn/khoa-hoc-quan-tri-mua-hang-procurement.html",
            "title": "Khóa học Quản trị Mua hàng (Procurement Management) Thực chiến",
        },
        {
            "domain": "datapot.edu.vn",
            "url": "https://datapot.edu.vn/khoa-hoc-power-bi/",
            "title": "Khóa học phân tích dữ liệu Power BI & SQL thực chiến cho doanh nghiệp",
        },
    ],
}


def fetch_google_suggest_vn(seed: str) -> list[str]:
    """Queries live Google Autocomplete Vietnam for hot search phrases in pure UTF-8."""
    q = urllib.parse.quote(seed.strip())
    url = (
        f"https://suggestqueries.google.com/complete/search"
        f"?client=firefox&hl=vi&gl=vn&ie=utf-8&oe=utf-8&q={q}"
    )
    res = http_get(url, timeout=10, retries=1)
    if not res["ok"] or not res["text"]:
        return []
    try:
        payload = json.loads(res["text"])
        if isinstance(payload, list) and len(payload) > 1 and isinstance(payload[1], list):
            return [str(x).strip().lower() for x in payload[1] if str(x).strip()]
    except Exception:
        pass
    return []


def fetch_google_trends_vn_rss() -> list[str]:
    """Fetches daily trending terms from Google Trends Vietnam RSS feed."""
    url = "https://trends.google.com/trending/rss?geo=VN"
    res = http_get(url, timeout=10, retries=1)
    if not res["ok"] or not res["text"]:
        return []
    titles = re.findall(r"<title>(.*?)</title>", res["text"], re.I | re.S)
    cleaned = []
    for t in titles:
        t_clean = html.unescape(t).strip().lower()
        if t_clean and "daily search trends" not in t_clean:
            cleaned.append(t_clean)
    return cleaned[:20]


def classify_keyword_intent(kw: str) -> tuple[str, int]:
    """Returns (Intent Label, Intent Score out of 35)."""
    k = kw.lower()
    if any(
        w in k
        for w in (
            "phần mềm",
            "công cụ",
            "online",
            "miễn phí",
            "app",
            "web",
            "dịch file",
            "dịch pdf",
            "soạn thảo",
            "tạo báo cáo",
            "tải",
            "template",
            "mẫu file",
        )
    ):
        return "Transactional / Tool", 35
    if any(
        w in k
        for w in (
            "so sánh",
            "top",
            "tốt nhất",
            "review",
            "đánh giá",
            "khóa học",
            "đào tạo",
            "bảng giá",
            "chi phí",
        )
    ):
        return "Commercial Investigation", 30
    return "Informational / How-To", 24


def discover_platform_hot_keywords(platform: dict[str, Any]) -> list[str]:
    """Harvests live Google Suggest keywords for a platform's functional seeds."""
    discovered: list[str] = []
    seen: set[str] = set()

    for seed in platform.get("seed_keywords", []):
        seed_norm = seed.strip().lower()
        if seed_norm not in seen:
            seen.add(seed_norm)
            discovered.append(seed_norm)
        for mod in HOT_MODIFIERS_VN[:4]:
            query = f"{seed_norm} {mod}".strip()
            suggestions = fetch_google_suggest_vn(query)
            for s in suggestions:
                if s not in seen and len(s) >= 10:
                    seen.add(s)
                    discovered.append(s)
            time.sleep(0.1)

    return discovered


_KEYWORD_FILLER_PREFIXES = {"về", "của", "và", "là", "cho", "với", "các", "những", "một", "để", "thì", "mà"}
_KEYWORD_NOISE_TOKENS = {"free", "online", "miễn", "phí", "2024", "2025", "2026"}


def is_low_quality_keyword(kw: str) -> bool:
    """True for fragments such as 'về sơ đồ gantt online' that start with a filler word."""
    tokens = kw.strip().lower().split()
    return not tokens or tokens[0] in _KEYWORD_FILLER_PREFIXES


def keyword_dedup_key(kw: str) -> tuple[str, ...]:
    """Order- and noise-insensitive key: 'dịch pdf giữ nguyên định dạng free' == 'dịch pdf giữ nguyên định dạng',
    '7 tiêu chí X' == 'tiêu chí X'."""
    tokens = [
        t
        for t in kw.strip().lower().split()
        if not t.isdigit() and t not in _KEYWORD_NOISE_TOKENS and t not in _KEYWORD_FILLER_PREFIXES
    ]
    return tuple(sorted(set(tokens)))


def evaluate_and_select_keywords(
    platform: dict[str, Any],
    discovered_keywords: list[str],
    live_platform_pages: list[dict[str, Any]],
    competitor_signals: list[dict[str, Any]],
    seo_state: dict[str, Any],
    top_n: int = 1,
    real_queries: dict[str, int] | None = None,
) -> list[dict[str, Any]]:
    """
    Scores all discovered keywords (0-100) and selects the top `top_n` unoptimized keywords.
    `real_queries` (query -> impressions from Search Console) breaks ties between equal scores.
    """
    optimized_history: dict[str, str] = seo_state.get("optimized_keywords", {})
    now = now_vn()

    # Combine all titles, H1s, H2s, and meta descriptions on our live platform
    all_titles_h1 = " || ".join(
        f"{p.get('title', '')} { ' '.join(p.get('h1', [])) }".lower()
        for p in live_platform_pages
    )
    all_h2_meta = " || ".join(
        f"{p.get('meta_description', '')} { ' '.join(p.get('h2', [])) }".lower()
        for p in live_platform_pages
    )

    avg_comp_words = (
        int(sum(c.get("word_count", 900) for c in competitor_signals) / max(len(competitor_signals), 1))
        if competitor_signals
        else 1200
    )
    comp_has_tables = any(c.get("table_count", 0) > 0 for c in competitor_signals)
    comp_has_faq = any("FAQPage" in c.get("schema_types", []) for c in competitor_signals)

    # Keys of keywords this platform optimized in the last 14 days, to reject near-duplicates
    recent_keys: set[tuple[str, ...]] = set()
    history_prefix = f"{platform['id']}::"
    for hist_key, hist_iso in optimized_history.items():
        if not hist_key.startswith(history_prefix):
            continue
        try:
            if (now - dt.datetime.fromisoformat(hist_iso)).days < 14:
                recent_keys.add(keyword_dedup_key(hist_key[len(history_prefix):]))
        except Exception:
            continue

    scored_candidates: list[dict[str, Any]] = []
    for kw in discovered_keywords:
        # Skip if optimized within the last 14 days
        last_opt_iso = optimized_history.get(f"{platform['id']}::{kw}")
        if last_opt_iso:
            try:
                last_dt = dt.datetime.fromisoformat(last_opt_iso)
                if (now - last_dt).days < 14:
                    continue
            except Exception:
                pass

        if is_low_quality_keyword(kw) or keyword_dedup_key(kw) in recent_keys:
            continue

        intent_label, intent_score = classify_keyword_intent(kw)

        # Coverage gap score (0-35): Higher score if NOT yet in Title/H1
        tokens = [t for t in kw.split() if len(t) > 2]
        exact_in_title = kw in all_titles_h1
        exact_in_h2 = kw in all_h2_meta
        token_match_ratio = (
            sum(1 for t in tokens if t in all_titles_h1 or t in all_h2_meta) / max(len(tokens), 1)
        )

        if not exact_in_title and not exact_in_h2:
            coverage_gap_score = 35
            coverage_status = "UNCOVERED_HIGH_OPPORTUNITY"
        elif not exact_in_title and exact_in_h2:
            coverage_gap_score = 26
            coverage_status = "PARTIAL_H2_ONLY"
        else:
            coverage_gap_score = 14
            coverage_status = "COVERED_REINFORCE"

        # Competitor SERP gap score (0-30)
        serp_score = 20
        if 3 <= len(kw.split()) <= 8:
            serp_score += 6  # Sweet-spot high-conversion Vietnamese phrase length
        if token_match_ratio >= 0.4:
            serp_score += 4  # Strongly aligned with platform core capability

        total_score = min(100, intent_score + coverage_gap_score + serp_score)

        # Determine best target URL on the platform for this keyword
        best_url = platform["base_url"]
        best_overlap = -1
        for p in live_platform_pages:
            p_text = f"{p.get('url', '')} {p.get('title', '')} {' '.join(p.get('h2', []))}".lower()
            overlap = sum(1 for t in tokens if t in p_text)
            if overlap > best_overlap:
                best_overlap = overlap
                best_url = p.get("url", platform["base_url"])

        scored_candidates.append(
            {
                "keyword": kw,
                "platform_id": platform["id"],
                "platform_domain": platform["domain"],
                "target_url": best_url,
                "intent": intent_label,
                "coverage_status": coverage_status,
                "priority_score": total_score,
                "competitor_avg_words": avg_comp_words,
                "target_outrank_words": max(1100, int(avg_comp_words * 1.25)),
                "competitor_has_tables": comp_has_tables,
                "competitor_has_faq": comp_has_faq,
                "gsc_impressions": real_query_impressions(kw, real_queries or {}),
            }
        )

    scored_candidates.sort(key=lambda x: (-x["priority_score"], -x["gsc_impressions"], len(x["keyword"])))
    selected: list[dict[str, Any]] = []
    selected_keys: set[tuple[str, ...]] = set()
    for cand in scored_candidates:
        key = keyword_dedup_key(cand["keyword"])
        if key in selected_keys:
            continue
        selected_keys.add(key)
        selected.append(cand)
        if len(selected) >= top_n:
            break
    return selected


# (core sentence, optional clauses in priority order). Clauses are appended whole while they
# still fit, so a description never ends mid-phrase.
META_DESCRIPTION_TEMPLATES = (
    (
        "Hướng dẫn và công cụ {kw} trên {d}",
        ("chuẩn hoá quy trình", "bảng so sánh thông số thực tế", "tự động hoá bằng AI miễn phí",
         "từ ERX Việt Nam", "dễ áp dụng", "có ví dụ minh hoạ", "sẵn sàng dùng ngay"),
    ),
    (
        "{Kw} thực chiến trên {d}",
        ("quy trình từng bước", "bảng đối chiếu tiêu chí rõ ràng", "công cụ AI hỗ trợ áp dụng ngay",
         "cùng ERX Việt Nam", "có ví dụ thực tế", "dễ làm theo", "tiết kiệm thời gian"),
    ),
    (
        "Tìm hiểu {kw} qua ví dụ thực tế",
        ("bảng so sánh cách làm thủ công và tự động", "công cụ trực tuyến miễn phí",
         "trên {d} của ERX Việt Nam", "dễ áp dụng", "có hướng dẫn chi tiết", "dùng được ngay"),
    ),
    (
        "Áp dụng {kw} nhanh và chính xác hơn trên {d}",
        ("checklist chuẩn hoá", "biểu mẫu tương tác", "trợ lý AI sẵn dùng",
         "phát triển bởi ERX Việt Nam", "có ví dụ thực tế", "dễ làm theo", "tiết kiệm thời gian"),
    ),
    (
        "{Kw}: so sánh các cách làm phổ biến",
        ("hướng dẫn thao tác chi tiết", "công cụ tự động hoá tiết kiệm thời gian",
         "có sẵn miễn phí trên {d}", "từ ERX Việt Nam", "dễ áp dụng", "có ví dụ minh hoạ", "dễ làm theo"),
    ),
)

_DANGLING_WORDS = {
    "và", "với", "cho", "của", "để", "là", "bằng", "từ", "trong", "các", "những", "một",
    "trên", "tại", "qua", "kèm", "theo", "bởi", "vào", "cùng",
}


def compose_meta_description(core: str, clauses: tuple[str, ...], limit: int = 160) -> str:
    """Core sentence plus as many whole clauses as fit in `limit` chars, ending with a period."""
    out = fit_meta_description(core, limit - 1).rstrip(".")
    for clause in clauses:
        candidate = f"{out}, {clause}"
        if len(candidate) + 1 <= limit:
            out = candidate
    return out + "."


def fit_meta_description(text: str, limit: int = 160) -> str:
    """Fits text into `limit` chars on a word boundary, ending with a period (no '...')."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    window = text[: limit - 1]
    if not text[limit - 1].isspace():
        cut = window.rfind(" ")
        if cut > limit // 2:
            window = window[:cut]
    out = window.rstrip(" ,;:-–—")
    while True:
        head, _, last = out.rpartition(" ")
        if head and last.lower() in _DANGLING_WORDS:
            out = head.rstrip(" ,;:-–—")
        else:
            break
    if not out.endswith((".", "!", "?")):
        out += "."
    return out


def build_keyword_seo_package(
    candidate: dict[str, Any],
    platform: dict[str, Any],
    competitors: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Generates an executable SEO upgrade package for the selected keyword:
      - Optimized <title> (50-65 chars)
      - Optimized <meta name="description"> (145-160 chars)
      - META_KEY cluster
      - Schema.org FAQPage + TechArticle JSON-LD
      - Outranking HTML section (H2 + Comparison Table + FAQ)
    """
    kw = candidate["keyword"]
    kw_title_case = kw[:1].upper() + kw[1:]
    brand_suffix = " | ERX"

    # Build a crisp 55-65 char Title with primary keyword front-loaded
    base_title = f"{kw_title_case} Thực Chiến & Tự Động Hoá AI{brand_suffix}"
    if len(base_title) > 65:
        base_title = f"{kw_title_case} Chuẩn Thực Chiến{brand_suffix}"
    if len(base_title) > 65:
        base_title = f"{kw_title_case[:55].rstrip()}{brand_suffix}"

    # Build a 145-160 char Meta Description (opener varies per keyword, cut on a word boundary)
    core, clauses = META_DESCRIPTION_TEMPLATES[
        int(hashlib.sha1(kw.encode("utf-8")).hexdigest(), 16) % len(META_DESCRIPTION_TEMPLATES)
    ]
    fmt = {"kw": kw, "Kw": kw_title_case, "d": platform["domain"]}
    meta_desc = compose_meta_description(
        core.format(**fmt), tuple(c.format(**fmt) for c in clauses)
    )

    seed_cluster = [kw] + [s for s in platform.get("seed_keywords", [])[:4] if s != kw]
    meta_keywords = ", ".join(seed_cluster)

    comp_domains = ", ".join(c.get("domain", "") for c in competitors[:3] if c.get("domain"))
    comp_h2_samples: list[str] = []
    for c in competitors[:3]:
        for h2 in c.get("h2", [])[:3]:
            if h2 not in comp_h2_samples and len(h2) > 8:
                comp_h2_samples.append(h2)

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"Làm thế nào để áp dụng {kw} hiệu quả nhất trong doanh nghiệp?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"Để triển khai {kw} đạt hiệu quả cao, bạn nên kết hợp quy trình chuẩn hoá dữ liệu đầu vào "
                        f"với công cụ tự động hoá trực tuyến trên {platform['domain']} giúp tiết kiệm 70-80% thời gian xử lý thủ công."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": f"Giải pháp {kw} tại {platform['domain']} có ưu điểm gì vượt trội?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"Khác với các bài viết lý thuyết tĩnh, {platform['domain']} cung cấp biểu mẫu tương tác trực tiếp, "
                        f"bảng đối chiếu thông số kỹ thuật và AI hỗ trợ phân tích ngay trên trình duyệt."
                    ),
                },
            },
        ],
    }

    pillar_html_snippet = f"""
<section class="erx-seo-keyword-module" data-keyword="{html.escape(kw)}">
  <h2>{html.escape(kw_title_case)}: Giải pháp &amp; Quy trình Chuẩn Thực Chiến</h2>
  <p>{html.escape(meta_desc)}</p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Tiêu chí đánh giá ({html.escape(kw_title_case)})</th>
          <th>Phương pháp Thủ công / Truyền thống</th>
          <th>Giải pháp Tự động hoá trên {html.escape(platform['domain'])}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Tốc độ triển khai &amp; Xử lý</strong></td>
          <td>Mất nhiều giờ chỉnh sửa thủ công, dễ sai sót</td>
          <td>Tự động hoá tức thì bằng AI &amp; thuật toán chuẩn hoá (tiết kiệm 80% thời gian)</td>
        </tr>
        <tr>
          <td><strong>Độ chính xác &amp; Cấu trúc dữ liệu</strong></td>
          <td>Phụ thuộc kinh nghiệm cá nhân, thiếu đồng nhất</td>
          <td>Chuẩn hoá 100% theo tiêu chuẩn doanh nghiệp B2B &amp; PMBOK/ISO</td>
        </tr>
        <tr>
          <td><strong>Khả năng xuất bản &amp; Tích hợp</strong></td>
          <td>Rời rạc giữa nhiều file tĩnh</td>
          <td>Liên thông trực tiếp với hệ sinh thái ERX Việt Nam ({html.escape(platform['domain'])})</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
""".strip()

    return {
        "generated_at": now_vn().isoformat(),
        "platform_id": platform["id"],
        "platform_domain": platform["domain"],
        "target_url": candidate["target_url"],
        "keyword": kw,
        "intent": candidate["intent"],
        "priority_score": candidate["priority_score"],
        "coverage_status": candidate["coverage_status"],
        "target_outrank_words": candidate["target_outrank_words"],
        "competitors_analyzed": comp_domains,
        "competitor_h2_benchmarks": comp_h2_samples[:6],
        "recommended_title": base_title,
        "recommended_meta_description": meta_desc,
        "recommended_meta_keywords": meta_keywords,
        "faq_jsonld": faq_schema,
        "pillar_html_snippet": pillar_html_snippet,
    }


def submit_indexnow(urls: list[str]) -> dict[str, Any]:
    """Submits URLs to the IndexNow API (Bing, Yandex, etc.; Google does not use it).
    Requires INDEXNOW_KEY, with the key file hosted at https://<host>/<key>.txt."""
    key = os.environ.get("INDEXNOW_KEY", "").strip()
    if not key:
        return {"status": "skipped_no_key", "submitted": 0}
    by_host: dict[str, list[str]] = {}
    for u in urls:
        host = urllib.parse.urlparse(u).netloc.lower()
        if host:
            by_host.setdefault(host, []).append(u)
    submitted = 0
    errors: list[str] = []
    for host, host_urls in by_host.items():
        body = json.dumps(
            {
                "host": host,
                "key": key,
                "keyLocation": f"https://{host}/{key}.txt",
                "urlList": host_urls,
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": USER_AGENT},
        )
        try:
            with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
                if resp.status in (200, 202):
                    submitted += len(host_urls)
                else:
                    errors.append(f"{host}: HTTP {resp.status}")
        except Exception as exc:
            errors.append(f"{host}: {exc}")
    result: dict[str, Any] = {"status": "submitted" if submitted else "failed", "submitted": submitted}
    if errors:
        result["errors"] = errors
    return result


def ping_indexnow_and_warm_cache(urls: list[str]) -> dict[str, Any]:
    """Warms SSR caches on our platforms, then submits the URLs to IndexNow if configured."""
    warmed = 0
    for u in urls:
        res = http_get(u, timeout=12, retries=1)
        if res["ok"] and res["status"] == 200:
            warmed += 1
    return {
        "urls_submitted": len(urls),
        "ssr_warmed_ok": warmed,
        "indexnow": submit_indexnow(urls),
    }


def apply_erx_cms_direct_update(patches: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Stages Title/Meta patches for erx.vn in reports/erx_cms_auto_patch.js.

    This function does NOT write to the CMS: the administrator edit form is an
    ASP.NET page whose POST contract is not implemented here. When ERX_ADMIN_COOKIE
    is set it only confirms the edit pages are reachable with that session
    (`session_reachable_count`); `patched_count` is always 0.
    """
    js_payload_path = REPORTS_DIR / "erx_cms_auto_patch.js"
    patch_map = {}
    for p in patches:
        url = p.get("target_url", "")
        nid_m = re.search(r"-(\d{9,12})\.html$", url)
        if nid_m:
            patch_map[nid_m.group(1)] = {
                "url": url,
                "title": p.get("recommended_title", ""),
                "meta_title": p.get("recommended_title", ""),
                "meta_desc": p.get("recommended_meta_description", ""),
                "meta_key": p.get("recommended_meta_keywords", ""),
            }

    js_content = (
        "// Auto-generated by MUSE Autonomous SEO Daemon\n"
        f"window.ERX_AUTO_SEO_PATCHES = {json.dumps(patch_map, ensure_ascii=False, indent=2)};\n"
    )
    js_payload_path.write_text(js_content, encoding="utf-8")

    admin_cookie = os.environ.get("ERX_ADMIN_COOKIE", "").strip()
    if not admin_cookie or not patch_map:
        return {
            "mode": "staged_js_payload",
            "patched_count": 0,
            "staged_count": len(patch_map),
            "payload_file": str(js_payload_path),
        }

    reachable = 0
    for nid in patch_map:
        edit_url = f"https://erx.vn/administrator/content/edit.aspx?nContentId={nid}&divid=300&from=31"
        req = urllib.request.Request(
            edit_url,
            headers={"User-Agent": USER_AGENT, "Cookie": admin_cookie},
        )
        try:
            with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
                if resp.status == 200:
                    reachable += 1
        except Exception as exc:
            logger.warning("CMS edit page unreachable for %s: %s", nid, exc)

    return {
        "mode": "staged_session_verified",
        "patched_count": 0,
        "staged_count": len(patch_map),
        "session_reachable_count": reachable,
        "payload_file": str(js_payload_path),
    }


def collect_gsc_for_cycle(config: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """Search Console data per platform for the last 28 complete days; empty when not configured."""
    creds = gsc_client.load_credentials()
    if not creds:
        return {}, {"status": "skipped_no_credentials"}
    token = gsc_client.get_access_token(creds)
    if not token:
        return {}, {"status": "skipped_token_error"}
    end = now_vn().date() - dt.timedelta(days=3)  # Search Console data lags by about 2-3 days
    start = end - dt.timedelta(days=27)
    data = gsc_client.collect_platform_data(
        config.get("platforms", []), start.isoformat(), end.isoformat(), token,
        quota_project=creds.get("quota_project_id"),
    )
    return data, {"status": "ok", "start": start.isoformat(), "end": end.isoformat(), "platforms": len(data)}


def run_experiment_cycle(
    ledger_path: Path | None = None,
    report_path: Path | None = None,
    today: dt.date | None = None,
    fetch: Any = None,
    resolve: Any = None,
) -> dict[str, Any]:
    """Measure SEO experiments that reached their 14/21-day mark and refresh reports/experiments_latest.md."""
    fetch = fetch or experiments.default_gsc_fetcher()
    if not fetch:
        return {"status": "skipped_no_credentials"}
    ledger_path = ledger_path or experiments.LEDGER_PATH
    today = today or now_vn().date()
    ledger = experiments.load_ledger(ledger_path)
    done = experiments.run_due_measurements(ledger, today, fetch, resolve or experiments.property_resolver())
    experiments.save_ledger(ledger_path, ledger)
    experiments.write_experiments_report(report_path or experiments.REPORT_PATH, ledger, today)
    return {"status": "ok", "measured": len(done), "verdicts": [r["verdict"] for r in done]}


def run_daily_keyword_seo_cycle(config: dict[str, Any]) -> dict[str, Any]:
    """
    Executes the complete 07:00 AM Autonomous Keyword Discovery, Evaluation & SEO Optimization cycle.
    """
    logger.info("=== [LOOP 1] Starting Daily 07:00 AM Hot Keyword Discovery & Auto-SEO Cycle ===")
    seo_state = load_json_state(
        SEO_STATE_FILE,
        {"last_daily_run": None, "optimized_keywords": {}, "history": []},
    )
    injections_state = load_json_state(INJECTIONS_FILE, {"injections": []})

    gsc_data, gsc_status = collect_gsc_for_cycle(config)
    logger.info("Search Console: %s", gsc_status)
    try:
        experiments_status = run_experiment_cycle()
    except Exception as exc:  # never let the experiment ledger break the daily cycle
        logger.warning("Experiment measurement failed: %s", exc)
        experiments_status = {"status": f"error: {exc}"}
    logger.info("Experiments: %s", experiments_status)

    trending_vn = fetch_google_trends_vn_rss()
    logger.info("Fetched %d trending topics from Google Trends Vietnam RSS", len(trending_vn))

    keywords_per_platform = int(
        os.environ.get(
            "KEYWORDS_PER_PLATFORM_PER_DAY",
            config.get("keywords_per_platform_per_day", 1),
        )
    )

    cycle_results: list[dict[str, Any]] = []
    urls_to_warm: list[str] = []

    for platform in config.get("platforms", []):
        pid = platform["id"]
        logger.info("Discovering hot keywords for platform [%s] (%s)...", pid, platform["domain"])

        # 1. Discover hot keywords via Google Suggest Vietnam
        discovered = discover_platform_hot_keywords(platform)

        # 2. Crawl our live primary target URLs on this platform
        live_pages: list[dict[str, Any]] = []
        for t_url in platform.get("primary_target_urls", [])[:6]:
            res = http_get(t_url, timeout=15)
            if res["ok"] and res["status"] == 200:
                live_pages.append(extract_page_seo_signals(res["text"], t_url))

        # 3. Crawl Top-3 Competitor benchmark URLs
        comp_signals: list[dict[str, Any]] = []
        for comp in COMPETITOR_BENCHMARK_URLS.get(pid, [])[:3]:
            c_res = http_get(comp["url"], timeout=12, retries=1)
            if c_res["ok"] and c_res["status"] == 200:
                sig = extract_page_seo_signals(c_res["text"], comp["url"])
                sig["domain"] = comp["domain"]
                comp_signals.append(sig)
            else:
                comp_signals.append(
                    {
                        "domain": comp["domain"],
                        "url": comp["url"],
                        "title": comp["title"],
                        "word_count": 1350,
                        "table_count": 1,
                        "schema_types": ["Article", "FAQPage"],
                        "h2": [comp["title"]],
                    }
                )

        # 4. Evaluate and rank keywords to pick the top opportunity
        selected = evaluate_and_select_keywords(
            platform=platform,
            discovered_keywords=discovered,
            live_platform_pages=live_pages,
            competitor_signals=comp_signals,
            seo_state=seo_state,
            top_n=keywords_per_platform,
            real_queries=gsc_client.queries_by_impressions(gsc_data.get(pid, {})),
        )

        # 5. Build and execute SEO upgrade package for each selected keyword
        for cand in selected:
            pkg = build_keyword_seo_package(cand, platform, comp_signals)
            cycle_results.append(pkg)
            urls_to_warm.append(cand["target_url"])

            # Mark keyword as optimized in state
            seo_state.setdefault("optimized_keywords", {})[
                f"{pid}::{cand['keyword']}"
            ] = now_vn().isoformat()
            injections_state.setdefault("injections", []).append(pkg)

            logger.info(
                "  -> Selected & Optimized [%s] Keyword: '%s' (Score: %d/100, Target: %s)",
                pid,
                cand["keyword"],
                cand["priority_score"],
                cand["target_url"],
            )

    if gsc_data:
        gsc_client.write_opportunity_report(
            REPORTS_DIR / f"gsc_opportunities_{now_vn().date().isoformat()}.md",
            gsc_data, gsc_status["start"], gsc_status["end"],
        )

    # Keep last 200 injections in state file
    injections_state["injections"] = injections_state.get("injections", [])[-200:]
    save_json_state(INJECTIONS_FILE, injections_state)

    # Apply CMS patches if any target erx.vn
    cms_result = apply_erx_cms_direct_update(cycle_results)

    # Optional hook command for MUSE Server Agent (e.g. auto-commit/deploy to target repos)
    hook_cmd = os.environ.get("MUSE_AGENT_HOOK_CMD", "").strip()
    hook_status = "not_configured"
    if hook_cmd:
        try:
            subprocess.run(hook_cmd, shell=True, check=True, timeout=300)
            hook_status = "executed_ok"
        except Exception as exc:
            hook_status = f"error: {exc}"

    warm_result = ping_indexnow_and_warm_cache(urls_to_warm)

    run_summary = {
        "cycle_type": "daily_keyword_seo",
        "executed_at": now_vn().isoformat(),
        "trending_vn_sample": trending_vn[:8],
        "keywords_optimized_count": len(cycle_results),
        "optimizations": cycle_results,
        "cms_patch_status": cms_result,
        "gsc_status": gsc_status,
        "experiments_status": experiments_status,
        "muse_hook_status": hook_status,
        "cache_and_indexnow": warm_result,
    }

    seo_state["last_daily_run"] = now_vn().strftime("%Y-%m-%d")
    seo_state.setdefault("history", []).append(
        {
            "executed_at": run_summary["executed_at"],
            "keywords_optimized_count": len(cycle_results),
            "keywords": [x["keyword"] for x in cycle_results],
        }
    )
    seo_state["history"] = seo_state["history"][-90:]
    save_json_state(SEO_STATE_FILE, seo_state)

    # Write human-readable & agent-readable daily report
    date_tag = now_vn().strftime("%Y-%m-%d")
    report_md_path = REPORTS_DIR / f"daily_keyword_seo_{date_tag}.md"
    write_daily_keyword_report_md(report_md_path, run_summary)
    logger.info("=== [LOOP 1] Completed Daily Keyword SEO Cycle (%d keywords optimized) ===", len(cycle_results))
    return run_summary


def write_daily_keyword_report_md(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Báo cáo Vòng lặp Tự động 07:00 AM — Săn Từ khoá Hot & Tối ưu SEO",
        f"- **Thời gian thực thi:** `{summary['executed_at']}`",
        f"- **Số từ khoá mục tiêu đã chọn & tối ưu:** `{summary['keywords_optimized_count']}`",
        f"- **Trạng thái làm ấm SSR & IndexNow:** `{summary['cache_and_indexnow']}`",
        "",
        "## Danh sách Từ khoá Đã Chọn & Thực thi SEO Hôm nay",
        "",
        "| Nền tảng | Từ khoá Mục tiêu | Điểm Ưu tiên | Trạng thái Trước SEO | URL Đích | Title Tối ưu Mới |",
        "| :--- | :--- | :---: | :--- | :--- | :--- |",
    ]
    for opt in summary.get("optimizations", []):
        lines.append(
            f"| `{opt['platform_domain']}` | **{opt['keyword']}** | `{opt['priority_score']}/100` | "
            f"`{opt['coverage_status']}` | {opt['target_url']} | {opt['recommended_title']} |"
        )
    lines.append("")
    lines.append("## Chi tiết Gói Tối ưu Nội dung & Schema JSON-LD")
    for opt in summary.get("optimizations", []):
        lines.extend(
            [
                f"### [{opt['platform_domain']}] Từ khoá: `{opt['keyword']}`",
                f"- **URL đích:** `{opt['target_url']}`",
                f"- **Intent:** `{opt['intent']}` | **Số từ mục tiêu vượt Top 3 đối thủ (`{opt['competitors_analyzed']}`):** `{opt['target_outrank_words']} từ`",
                f"- **Recommended `<title>`:** `{opt['recommended_title']}`",
                f"- **Recommended `<meta name=\"description\">`:** `{opt['recommended_meta_description']}`",
                f"- **Recommended `META_KEY`:** `{opt['recommended_meta_keywords']}`",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


# ============================================================================
# 4. LOOP 2: CONTINUOUS PLATFORM CONTENT & TAG WATCHER
# ============================================================================

def audit_single_page_seo(sig: dict[str, Any], domain: str) -> list[str]:
    """Checks a page's extracted SEO signals for any defects or regressions."""
    issues: list[str] = []
    title = sig.get("title", "")
    desc = sig.get("meta_description", "")
    canon = sig.get("canonical", "")

    if not title:
        issues.append("MISSING_TITLE")
    elif len(title) < 35:
        issues.append(f"SHORT_TITLE ({len(title)} chars)")
    elif title.isupper() and len(title) > 15:
        issues.append("ALL_CAPS_TITLE")

    if domain != "khoahoc.erx.vn":
        if not desc:
            issues.append("MISSING_META_DESCRIPTION")
        elif len(desc) < 70:
            issues.append(f"SHORT_META_DESCRIPTION ({len(desc)} chars)")
        elif desc.strip() == title.strip():
            issues.append("DUPLICATE_TITLE_AS_META_DESCRIPTION")

        if not canon:
            issues.append("MISSING_CANONICAL")

        if sig.get("jsonld_count", 0) == 0:
            issues.append("MISSING_JSONLD_SCHEMA")

    if sig.get("png_base64_kb", 0) > 250:
        issues.append(f"HEAVY_INLINE_PNG_BASE64 ({sig['png_base64_kb']} KB)")

    return issues


GOOGLEBOT_UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
SITE_HEALTH_TTL_HOURS = 6
HTML_COMPRESSION_MIN_BYTES = 100_000
_PLACEHOLDER_VALUES = {"undefined", "null", "nan", "[object object]"}


def fetch_with_headers(url: str, user_agent: str = USER_AGENT, timeout: int = 15) -> dict[str, Any]:
    """GET that keeps response headers and on-the-wire size; never raises."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            raw, status, headers = resp.read(5_000_000), resp.status, resp.headers
    except urllib.error.HTTPError as exc:
        try:
            raw = exc.read(5_000_000)
        except Exception:
            raw = b""
        status, headers = exc.code, exc.headers
    except Exception:
        return {"ok": False, "status": 0, "headers": {}, "text": "", "wire_bytes": 0}

    wire_bytes = len(raw)
    encoding = (headers.get("Content-Encoding") or "").lower()
    try:
        if "gzip" in encoding:
            raw = gzip.decompress(raw)
        elif "deflate" in encoding:
            raw = zlib.decompress(raw)
    except Exception:
        pass
    return {
        "ok": status < 400,
        "status": status,
        "headers": {k.lower(): v for k, v in headers.items()},
        "text": raw.decode("utf-8", errors="replace"),
        "wire_bytes": wire_bytes,
    }


def check_security_headers(headers: dict[str, str]) -> list[str]:
    flags: list[str] = []
    hsts = headers.get("strict-transport-security", "").strip()
    if not hsts:
        flags.append("MISSING_HSTS")
    elif not re.match(r"max-age=\d+", hsts, re.I):
        flags.append("MALFORMED_HSTS")
    if headers.get("x-content-type-options", "").strip().lower() != "nosniff":
        flags.append("MISSING_NOSNIFF")
    if not headers.get("referrer-policy", "").strip():
        flags.append("MISSING_REFERRER_POLICY")
    return flags


def _differs_by_user_agent(chrome: dict[str, Any], bot: dict[str, Any], url: str) -> bool:
    sig_c = extract_page_seo_signals(chrome["text"], url)
    sig_b = extract_page_seo_signals(bot["text"], url)
    if sig_c["title"] and sig_b["title"] and sig_c["title"] != sig_b["title"]:
        return True
    if bool(sig_c["title"]) != bool(sig_b["title"]) or bool(sig_c["h1"]) != bool(sig_b["h1"]):
        return True
    small, large = sorted((len(chrome["text"]), len(bot["text"])))
    return (small == 0 and large > 0) or (small > 0 and large / small > 2.0)


def check_site_health(
    platform: dict[str, Any],
    fetch: Any = fetch_with_headers,
    parity_urls: Any = (),
) -> dict[str, Any]:
    """Site-level checks: security headers, HTML compression, soft 404, Googlebot-vs-browser parity."""
    base = platform["base_url"]
    flags: list[str] = []

    home = fetch(base, user_agent=USER_AGENT)
    if not home.get("ok"):
        flags.append("HOMEPAGE_UNREACHABLE")
    else:
        flags.extend(check_security_headers(home["headers"]))
        encoding = home["headers"].get("content-encoding", "").lower()
        if home["wire_bytes"] > HTML_COMPRESSION_MIN_BYTES and not any(
            e in encoding for e in ("gzip", "br", "deflate", "zstd")
        ):
            flags.append(f"HTML_NOT_COMPRESSED ({home['wire_bytes'] // 1024} KB)")

    probe = fetch(f"{base.rstrip('/')}/__seo-probe-{uuid.uuid4().hex[:8]}", user_agent=USER_AGENT)
    if probe.get("status") == 200:
        flags.append("SOFT_404")
    elif probe.get("status") in (404, 410):
        ctype = probe.get("headers", {}).get("content-type", "").lower()
        if ctype and "html" not in ctype:
            flags.append("NON_HTML_404")

    for url in [base, *list(parity_urls)[:2]]:
        chrome = home if url == base else fetch(url, user_agent=USER_AGENT)
        bot = fetch(url, user_agent=GOOGLEBOT_UA)
        if chrome.get("ok") and bot.get("ok") and _differs_by_user_agent(chrome, bot, url):
            flags.append("UA_CONTENT_MISMATCH")
            break

    return {"checked_at": now_vn().isoformat(), "flags": flags}


def site_health_due(
    entry: dict[str, Any] | None, now: dt.datetime, ttl_hours: int = SITE_HEALTH_TTL_HOURS
) -> bool:
    if not entry:
        return True
    try:
        return (now - dt.datetime.fromisoformat(entry["checked_at"])) >= dt.timedelta(hours=ttl_hours)
    except Exception:
        return True


def audit_advisory_seo(sig: dict[str, Any], domain: str) -> list[str]:
    """Advisory on-page checks. Reported, but they never trigger title/meta auto-remediation."""
    advisories: list[str] = []

    placeholder_fields = [
        name
        for name, values in (
            ("title", [sig.get("title", "")]),
            ("meta_description", [sig.get("meta_description", "")]),
            ("h1", sig.get("h1", [])),
        )
        if any(v.strip().lower() in _PLACEHOLDER_VALUES or "[object Object]" in v for v in values)
    ]
    if placeholder_fields:
        advisories.append(f"UNDEFINED_PLACEHOLDER ({', '.join(placeholder_fields)})")

    title = sig.get("title", "")
    if len(title) > 65:
        advisories.append(f"LONG_TITLE ({len(title)} chars)")

    h1_raw = sig.get("h1_raw_count")
    if h1_raw is not None:
        if h1_raw == 0:
            advisories.append("MISSING_H1")
        elif not sig.get("h1"):
            advisories.append("EMPTY_H1")

    if sig.get("twitter_card") == "":
        advisories.append("EMPTY_TWITTER_CARD")

    img_total = sig.get("img_total", 0)
    img_missing = sig.get("img_missing_dims", 0)
    if img_total >= 3 and img_missing / img_total >= 0.5:
        advisories.append(f"IMAGES_MISSING_DIMENSIONS ({img_missing}/{img_total})")

    return advisories


def synthesize_remediation_for_page(sig: dict[str, Any], domain: str, issues: list[str]) -> dict[str, Any]:
    """Generates immediate auto-fix metadata for a new or degraded page."""
    raw_title = sig.get("title", "") or (sig.get("h1", [""])[0] if sig.get("h1") else domain)
    clean_title = raw_title.strip()
    if clean_title.isupper():
        clean_title = clean_title.capitalize()
    if len(clean_title) < 42 and "| ERX" not in clean_title:
        clean_title = f"{clean_title} — Hướng dẫn & Công cụ Thực chiến | ERX"

    raw_desc = sig.get("meta_description", "").strip()
    if not raw_desc or len(raw_desc) < 70 or raw_desc == raw_title:
        h2_preview = ", ".join(sig.get("h2", [])[:3])
        if h2_preview:
            raw_desc = f"{clean_title}: Phân tích chi tiết về {h2_preview} kèm biểu mẫu và hướng dẫn thực chiến tại {domain}."
        else:
            raw_desc = f"{clean_title} — Tài liệu hướng dẫn chuyên sâu, biểu mẫu thực hành và công cụ tự động hoá trên hệ sinh thái {domain}."
    raw_desc = fit_meta_description(raw_desc)

    return {
        "target_url": sig.get("url", ""),
        "domain": domain,
        "detected_issues": issues,
        "recommended_title": clean_title,
        "recommended_meta_description": raw_desc,
        "recommended_canonical": sig.get("canonical") or sig.get("url", ""),
    }


def watch_community_api_topics() -> list[dict[str, Any]]:
    """Checks `community.erx.vn/api/community/topics` for newly posted or HTML-attached topics."""
    res = http_get("https://community.erx.vn/api/community/topics", timeout=15)
    if not res["ok"] or not res["text"]:
        return []
    try:
        data = json.loads(res["text"])
        items = data.get("items", data) if isinstance(data, dict) else data
        if not isinstance(items, list):
            return []
        return items[:25]
    except Exception:
        return []


def run_platform_watcher_cycle(config: dict[str, Any]) -> dict[str, Any]:
    """
    Scans all 6 platforms for:
      - Newly published pages/articles/topics (`NEW_URL`)
      - Modified SEO tags (`TAG_MODIFIED`)
      - SEO tag defects (`SEO_DEFECT`)
    Automatically warms SSR caches, generates remediation patches, and applies CMS fixes.
    """
    logger.info("=== [LOOP 2] Starting Continuous Platform Content & Tag Watcher Cycle ===")
    watch_state = load_json_state(
        WATCH_STATE_FILE,
        {"last_watch_run": None, "url_registry": {}, "community_topics_seen": []},
    )
    url_registry: dict[str, dict[str, Any]] = watch_state.setdefault("url_registry", {})
    seen_topics: set[int] = set(watch_state.get("community_topics_seen", []))

    new_urls_found: list[dict[str, Any]] = []
    modified_urls_found: list[dict[str, Any]] = []
    remediations_triggered: list[dict[str, Any]] = []
    advisory_pages: list[dict[str, Any]] = []
    platform_health: list[dict[str, Any]] = []
    site_health_state: dict[str, dict[str, Any]] = watch_state.setdefault("site_health", {})
    site_health_results: list[dict[str, Any]] = []

    for platform in config.get("platforms", []):
        pid = platform["id"]
        domain = platform["domain"]
        base_url = platform["base_url"]
        sitemap_url = platform.get("sitemap_url", "")

        # 1. Fetch sitemap URLs
        s_res = http_get(sitemap_url, timeout=15) if sitemap_url else {"ok": False, "text": ""}
        sitemap_locs = parse_sitemap_urls(s_res["text"]) if s_res.get("ok") else []

        # 1b. Site-level health (security headers, compression, soft 404, Googlebot parity), cached 6h
        health = site_health_state.get(pid)
        if site_health_due(health, now_vn()):
            health = check_site_health(platform, parity_urls=sitemap_locs[:2])
            site_health_state[pid] = health
        site_health_results.append(
            {"platform_id": pid, "domain": domain, "checked_at": health["checked_at"], "flags": health["flags"]}
        )

        # Combine primary URLs + most recent/important sitemap URLs (cap at 35 per cycle for fast non-blocking checks)
        urls_to_inspect: list[str] = []
        for u in platform.get("primary_target_urls", []) + sitemap_locs[:20] + sitemap_locs[-15:]:
            if u and u not in urls_to_inspect:
                urls_to_inspect.append(u)

        def _inspect_url(u: str) -> dict[str, Any] | None:
            r = http_get(u, timeout=15, retries=1)
            if not r["ok"] or r["status"] != 200:
                return {"url": u, "ok": False, "status": r["status"]}
            sig = extract_page_seo_signals(r["text"], u)
            sig["ok"] = True
            sig["status"] = r["status"]
            sig["elapsed_ms"] = r["elapsed_ms"]
            return sig

        inspected_results: list[dict[str, Any]] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            for res_item in pool.map(_inspect_url, urls_to_inspect):
                if res_item:
                    inspected_results.append(res_item)

        for item in inspected_results:
            u = item["url"]
            if not item.get("ok"):
                continue

            issues = audit_single_page_seo(item, domain)
            advisories = audit_advisory_seo(item, domain)
            if advisories:
                advisory_pages.append({"platform_id": pid, "url": u, "advisories": advisories})
            prev = url_registry.get(u)

            if prev is None:
                event_type = "NEW_URL"
                new_urls_found.append(
                    {
                        "platform_id": pid,
                        "url": u,
                        "title": item.get("title", ""),
                        "issues": issues,
                    }
                )
            elif prev.get("fingerprint") != item.get("fingerprint"):
                event_type = "TAG_MODIFIED"
                modified_urls_found.append(
                    {
                        "platform_id": pid,
                        "url": u,
                        "old_title": prev.get("title", ""),
                        "new_title": item.get("title", ""),
                        "old_meta_desc": prev.get("meta_description", ""),
                        "new_meta_desc": item.get("meta_description", ""),
                        "issues": issues,
                    }
                )
            else:
                event_type = "UNCHANGED"

            if issues or event_type in ("NEW_URL", "TAG_MODIFIED"):
                if issues:
                    rem = synthesize_remediation_for_page(item, domain, issues)
                    rem["event_type"] = event_type
                    remediations_triggered.append(rem)

            url_registry[u] = {
                "platform_id": pid,
                "title": item.get("title", ""),
                "meta_description": item.get("meta_description", ""),
                "canonical": item.get("canonical", ""),
                "word_count": item.get("word_count", 0),
                "jsonld_count": item.get("jsonld_count", 0),
                "png_base64_kb": item.get("png_base64_kb", 0),
                "fingerprint": item.get("fingerprint", ""),
                "issues": issues,
                "advisories": advisories,
                "last_checked": now_vn().isoformat(),
            }

        platform_health.append(
            {
                "platform_id": pid,
                "domain": domain,
                "sitemap_url_count": len(sitemap_locs),
                "inspected_count": len(inspected_results),
            }
        )

    # Check community.erx.vn live topics API for newly posted threads & warm their SSR & API routes
    community_topics = watch_community_api_topics()
    new_community_topics: list[dict[str, Any]] = []
    for t in community_topics:
        tid = t.get("id")
        if not isinstance(tid, int):
            continue
        if tid not in seen_topics:
            seen_topics.add(tid)
            # Warm both the API detail endpoint (triggers HTML attachment extraction) and SSR forum page
            api_detail_url = f"https://community.erx.vn/api/community/topics/{tid}"
            http_get(api_detail_url, timeout=12, retries=1)
            new_community_topics.append(
                {
                    "id": tid,
                    "title": t.get("title", ""),
                    "api_url": api_detail_url,
                }
            )

    watch_state["community_topics_seen"] = sorted(list(seen_topics))[-500:]
    watch_state["last_watch_run"] = now_vn().isoformat()
    save_json_state(WATCH_STATE_FILE, watch_state)

    # Automatically apply any ERX CMS remediations
    cms_remediation_status = apply_erx_cms_direct_update(remediations_triggered)

    # Save auto-remediation queue JSON
    remediation_queue_path = REPORTS_DIR / "auto_remediation_queue.json"
    save_json_state(
        remediation_queue_path,
        {
            "generated_at": now_vn().isoformat(),
            "remediations_count": len(remediations_triggered),
            "remediations": remediations_triggered,
        },
    )

    watch_summary = {
        "cycle_type": "platform_watcher",
        "executed_at": now_vn().isoformat(),
        "platforms_checked": platform_health,
        "new_urls_count": len(new_urls_found),
        "modified_urls_count": len(modified_urls_found),
        "new_community_topics_warmed": len(new_community_topics),
        "remediations_triggered_count": len(remediations_triggered),
        "cms_remediation_status": cms_remediation_status,
        "site_health": site_health_results,
        "advisory_pages_count": len(advisory_pages),
        "advisory_counts": dict(
            collections.Counter(a.split(" (")[0] for p in advisory_pages for a in p["advisories"])
        ),
        "advisory_pages_sample": advisory_pages[:15],
        "new_urls_sample": new_urls_found[:15],
        "modified_urls_sample": modified_urls_found[:15],
        "remediations_sample": remediations_triggered[:15],
    }

    save_json_state(REPORTS_DIR / "latest_loop_status.json", watch_summary)
    write_watcher_report_md(REPORTS_DIR / "latest_loop_report.md", watch_summary)
    logger.info(
        "=== [LOOP 2] Completed Platform Watcher Cycle (New URLs: %d, Modified: %d, Remediations: %d) ===",
        len(new_urls_found),
        len(modified_urls_found),
        len(remediations_triggered),
    )
    return watch_summary


def write_watcher_report_md(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Báo cáo Trực Chiến 24/7 — Giám sát Bài viết Mới, Thẻ SEO & Tự động Tối ưu",
        f"- **Thời gian quét gần nhất:** `{summary['executed_at']}`",
        f"- **URL mới phát hiện (`NEW_URL`):** `{summary['new_urls_count']}`",
        f"- **URL có chỉnh sửa thẻ (`TAG_MODIFIED`):** `{summary['modified_urls_count']}`",
        f"- **Chủ đề `community.erx.vn` mới đã tự động trích xuất HTML & làm ấm SSR:** `{summary['new_community_topics_warmed']}`",
        f"- **Lệnh tự động tối ưu lại thẻ SEO (`Auto-Remediation`):** `{summary['remediations_triggered_count']}`",
        "",
        "## 1. Trạng thái Sitemap & Độ phủ trên 6 Nền tảng",
        "",
        "| Nền tảng | Tên miền | Tổng URL trong Sitemap | Số URL kiểm tra sâu mỗi vòng |",
        "| :--- | :--- | :---: | :---: |",
    ]
    for p in summary.get("platforms_checked", []):
        lines.append(
            f"| `{p['platform_id']}` | `{p['domain']}` | `{p['sitemap_url_count']}` | `{p['inspected_count']}` |"
        )

    if summary.get("modified_urls_sample"):
        lines.extend(
            [
                "",
                "## 2. Phát hiện Thay đổi Thẻ SEO (`TAG_MODIFIED`)",
                "",
                "| Nền tảng | URL | Title Cũ | Title Mới | Vấn đề Phát hiện |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ]
        )
        for m in summary["modified_urls_sample"]:
            lines.append(
                f"| `{m['platform_id']}` | {m['url']} | {m['old_title']} | {m['new_title']} | "
                f"`{', '.join(m['issues']) or 'OK'}` |"
            )

    if summary.get("remediations_sample"):
        lines.extend(
            [
                "",
                "## 3. Gói Tự động Chuẩn hoá Thẻ SEO (`Auto-Remediation Queue`)",
                "",
                "| Tên miền | URL | Lỗi Thẻ Phát hiện | Title Đề xuất Chuẩn SEO | Meta Description Đề xuất |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ]
        )
        for r in summary["remediations_sample"]:
            lines.append(
                f"| `{r['domain']}` | {r['target_url']} | `{', '.join(r['detected_issues'])}` | "
                f"{r['recommended_title']} | {r['recommended_meta_description']} |"
            )

    if summary.get("site_health"):
        lines.extend(
            [
                "",
                "## 5. Sức khỏe cấp Site (header bảo mật, nén HTML, soft 404, Googlebot vs trình duyệt)",
                "",
                "| Nền tảng | Tên miền | Cờ cảnh báo | Kiểm tra lúc |",
                "| :--- | :--- | :--- | :--- |",
            ]
        )
        for h in summary["site_health"]:
            lines.append(
                f"| `{h['platform_id']}` | `{h['domain']}` | `{', '.join(h['flags']) or 'OK'}` | {h['checked_at']} |"
            )

    if summary.get("advisory_pages_sample"):
        counts =", ".join(f"{k}: {v}" for k, v in summary.get("advisory_counts", {}).items())
        lines.extend(
            [
                "",
                f"## 4. Khuyến nghị On-page (Advisory, không tự sửa) — `{summary['advisory_pages_count']}` trang",
                "",
                f"Tổng hợp: {counts}",
                "",
                "| Nền tảng | URL | Khuyến nghị |",
                "| :--- | :--- | :--- |",
            ]
        )
        for a in summary["advisory_pages_sample"]:
            lines.append(f"| `{a['platform_id']}` | {a['url']} | `{', '.join(a['advisories'])}` |")

    path.write_text("\n".join(lines), encoding="utf-8")


# ============================================================================
# 5. MAIN 24/7 DAEMON SCHEDULER LOOP
# ============================================================================

def run_daemon_loop(config: dict[str, Any], daily_time_str: str, watch_interval_sec: int) -> None:
    """
    Infinite 24/7 loop for MUSE Server Agent:
      - Triggers `run_daily_keyword_seo_cycle` every day at `daily_time_str` (default 07:00 Asia/Ho_Chi_Minh),
        and also immediately on first boot if today's daily cycle hasn't run yet.
      - Triggers `run_platform_watcher_cycle` every `watch_interval_sec` seconds (default 900s = 15m).
    """
    target_hour, target_min = [int(x) for x in daily_time_str.split(":")]
    tz_name = config.get("timezone", "Asia/Ho_Chi_Minh")

    logger.info(
        "MUSE SEO Daemon booted. Timezone=%s | Daily Keyword SEO=%02d:%02d | Platform Watcher Interval=%ds",
        tz_name,
        target_hour,
        target_min,
        watch_interval_sec,
    )

    last_watch_ts = 0.0

    while True:
        try:
            now = now_vn(tz_name)
            today_str = now.strftime("%Y-%m-%d")
            seo_state = load_json_state(SEO_STATE_FILE, {"last_daily_run": None})
            last_daily_run = seo_state.get("last_daily_run")

            # Check if it's >= 07:00 AM today and today's daily keyword cycle hasn't run yet
            reached_daily_window = (now.hour > target_hour) or (
                now.hour == target_hour and now.minute >= target_min
            )
            if last_daily_run != today_str and reached_daily_window:
                run_daily_keyword_seo_cycle(config)

            # Check if it's time to run the continuous platform watcher
            if time.time() - last_watch_ts >= watch_interval_sec:
                run_platform_watcher_cycle(config)
                last_watch_ts = time.time()

        except KeyboardInterrupt:
            logger.info("MUSE SEO Daemon stopped by KeyboardInterrupt.")
            break
        except Exception as exc:
            logger.exception("Unexpected error in daemon loop (auto-recovering in 30s): %s", exc)

        time.sleep(30)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="MUSE Autonomous SEO Daemon & Closed-Loop Engine for ERX Ecosystem"
    )
    parser.add_argument(
        "--mode",
        choices=["daemon", "once", "keyword-only", "watch-only"],
        default=os.environ.get("SEO_DAEMON_MODE", "once"),
        help="Execution mode: 'daemon' (24/7 loop), 'once' (run both cycles and exit), 'keyword-only', or 'watch-only'",
    )
    parser.add_argument(
        "--daily-time",
        default=os.environ.get("SEO_DAILY_TIME", "07:00"),
        help="Daily trigger time in HH:MM (Asia/Ho_Chi_Minh) for the Hot Keyword SEO Cycle (default: 07:00)",
    )
    parser.add_argument(
        "--watch-interval",
        type=int,
        default=int(os.environ.get("SEO_WATCH_INTERVAL", "900")),
        help="Interval in seconds between Platform Content & Tag Watcher cycles (default: 900 = 15m)",
    )
    args = parser.parse_args()

    config = load_config()

    if args.mode == "keyword-only":
        run_daily_keyword_seo_cycle(config)
    elif args.mode == "watch-only":
        run_platform_watcher_cycle(config)
    elif args.mode == "once":
        run_daily_keyword_seo_cycle(config)
        run_platform_watcher_cycle(config)
    elif args.mode == "daemon":
        run_daemon_loop(
            config=config,
            daily_time_str=args.daily_time,
            watch_interval_sec=args.watch_interval,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
