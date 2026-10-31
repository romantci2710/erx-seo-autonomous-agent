# -*- coding: utf-8 -*-
"""
Google Search Console client for the ERX SEO daemon (standard library only).

Credentials: a `authorized_user` file, i.e. the output of
    gcloud auth application-default login --scopes="https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform"
located via GSC_CREDENTIALS_FILE or the default gcloud ADC path. Service-account files are not
supported here (JWT signing needs a crypto library the daemon does not depend on).

The module never raises on network/credential problems: callers get None / [] and decide what to do.
"""
from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger("muse_seo_daemon.gsc")

TOKEN_URL = "https://oauth2.googleapis.com/token"
API_BASE = "https://searchconsole.googleapis.com/webmasters/v3"
HttpPost = Callable[[str, bytes, dict[str, str]], dict[str, Any]]


def default_http_post(url: str, data: bytes, headers: dict[str, str]) -> dict[str, Any]:
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", "replace")[:300]
        except Exception:
            detail = ""
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc


def default_credentials_path() -> str:
    env = os.environ.get("GSC_CREDENTIALS_FILE", "").strip()
    if env:
        return env
    config_dir = os.environ.get("CLOUDSDK_CONFIG", "").strip()
    if not config_dir:
        appdata = os.environ.get("APPDATA", "").strip()
        config_dir = str(Path(appdata) / "gcloud") if appdata else str(Path.home() / ".config" / "gcloud")
    return str(Path(config_dir) / "application_default_credentials.json")


def load_credentials(path: str | None = None) -> dict[str, Any] | None:
    try:
        data = json.loads(Path(path or default_credentials_path()).read_text(encoding="utf-8"))
    except Exception:
        return None
    if data.get("type") != "authorized_user" or not data.get("refresh_token"):
        return None
    return data


def get_access_token(creds: dict[str, Any], http_post: HttpPost = default_http_post) -> str | None:
    body = urllib.parse.urlencode(
        {
            "client_id": creds["client_id"],
            "client_secret": creds["client_secret"],
            "refresh_token": creds["refresh_token"],
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    try:
        out = http_post(TOKEN_URL, body, {"Content-Type": "application/x-www-form-urlencoded"})
    except Exception as exc:
        logger.warning("GSC token refresh failed: %s", exc)
        return None
    return out.get("access_token")


def fetch_rows(
    property_url: str,
    start: str,
    end: str,
    dimensions: list[str],
    token: str,
    http_post: HttpPost = default_http_post,
    row_limit: int = 25000,
    max_rows: int = 100000,
    quota_project: str | None = None,
) -> list[dict[str, Any]]:
    url = f"{API_BASE}/sites/{urllib.parse.quote(property_url, safe='')}/searchAnalytics/query"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if quota_project:  # user credentials need the project whose API quota is used
        headers["X-Goog-User-Project"] = quota_project
    rows: list[dict[str, Any]] = []
    start_row = 0
    while len(rows) < max_rows:
        body = json.dumps(
            {"startDate": start, "endDate": end, "dimensions": dimensions, "rowLimit": row_limit, "startRow": start_row}
        ).encode("utf-8")
        try:
            page = http_post(url, body, headers).get("rows", [])
        except Exception as exc:
            logger.warning("GSC query failed for %s: %s", property_url, exc)
            return rows
        rows.extend(page)
        if len(page) < row_limit:
            break
        start_row += row_limit
    return rows


# ---------------------------------------------------------------------------
# Analysis helpers (pure functions over API rows)
# ---------------------------------------------------------------------------

def host_of(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.lower()


def filter_rows_by_host(rows: list[dict[str, Any]], host: str | None) -> list[dict[str, Any]]:
    if not host:
        return rows
    return [r for r in rows if host_of(r["keys"][0]) == host]


def striking_distance(
    rows: list[dict[str, Any]], min_impr: int = 50, pos_min: float = 4.0, pos_max: float = 20.0
) -> list[dict[str, Any]]:
    """Queries that already rank close to page one but get few clicks (keys = [..., query])."""
    out = [
        {
            "query": r["keys"][-1],
            "page": r["keys"][0] if len(r["keys"]) > 1 else "",
            "impressions": r["impressions"],
            "clicks": r["clicks"],
            "position": round(r["position"], 1),
        }
        for r in rows
        if r["impressions"] >= min_impr and pos_min <= r["position"] <= pos_max
    ]
    return sorted(out, key=lambda o: -o["impressions"])


def low_ctr_pages(
    rows: list[dict[str, Any]],
    min_impr: int = 500,
    max_ctr: float = 0.02,
    max_pos: float = 9.0,
    target_ctr: float = 0.04,
) -> list[dict[str, Any]]:
    """Pages that rank well but whose snippet gets few clicks. potential_gain is a rough estimate."""
    out = []
    for r in rows:
        impr = r["impressions"]
        ctr = r["clicks"] / impr if impr else 0.0
        if impr >= min_impr and ctr < max_ctr and r["position"] <= max_pos:
            out.append(
                {
                    "url": r["keys"][0],
                    "impressions": impr,
                    "clicks": r["clicks"],
                    "ctr": round(ctr * 100, 2),
                    "position": round(r["position"], 1),
                    "potential_gain": max(0, int(impr * target_ctr - r["clicks"])),
                }
            )
    return sorted(out, key=lambda o: -o["potential_gain"])


def real_query_impressions(keyword: str, queries: dict[str, int]) -> int:
    """Impressions of real queries that contain (nearly) all meaningful tokens of `keyword`."""
    tokens = [t for t in keyword.lower().split() if len(t) > 2]
    if not tokens:
        return 0
    # Short keywords must match fully; longer ones may miss one token.
    need = len(tokens) if len(tokens) <= 3 else len(tokens) - 1
    return sum(i for q, i in queries.items() if sum(t in q.lower() for t in tokens) >= need)


# ---------------------------------------------------------------------------
# Collection and reporting
# ---------------------------------------------------------------------------

def collect_platform_data(
    platforms: list[dict[str, Any]],
    start: str,
    end: str,
    token: str,
    http_post: HttpPost = default_http_post,
    quota_project: str | None = None,
) -> dict[str, dict[str, Any]]:
    """One fetch per distinct Search Console property, then split rows per platform by host."""
    cache: dict[str, dict[str, list[dict[str, Any]]]] = {}
    result: dict[str, dict[str, Any]] = {}
    for p in platforms:
        prop = p.get("gsc_property")
        if not prop:
            continue
        if prop not in cache:
            cache[prop] = {
                "pages": fetch_rows(prop, start, end, ["page"], token, http_post, quota_project=quota_project),
                "page_queries": fetch_rows(
                    prop, start, end, ["page", "query"], token, http_post, quota_project=quota_project
                ),
            }
        # A domain property covers every subdomain, so rows are always split by the platform's domain.
        host = p["domain"]
        result[p["id"]] = {
            "domain": p["domain"],
            "property": prop,
            "pages": filter_rows_by_host(cache[prop]["pages"], host),
            "page_queries": filter_rows_by_host(cache[prop]["page_queries"], host),
        }
    return result


def queries_by_impressions(platform_data: dict[str, Any]) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in platform_data.get("page_queries", []):
        q = r["keys"][-1]
        out[q] = out.get(q, 0) + r["impressions"]
    return out


def write_opportunity_report(path: Path, data: dict[str, dict[str, Any]], start: str, end: str) -> None:
    lines = [
        "# Cơ hội từ Google Search Console",
        f"- **Khoảng thời gian:** `{start}` → `{end}`",
        "- Số 'ước tính thêm click' là ước lượng thô theo CTR mục tiêu 4%, không phải dự báo.",
        "",
    ]
    for pid, d in data.items():
        pages = d.get("pages", [])
        clicks = sum(r["clicks"] for r in pages)
        impr = sum(r["impressions"] for r in pages)
        lines += [f"## {pid} (`{d.get('domain', '')}`)", "", f"- Click: **{clicks}**, hiển thị: **{impr}**, trang có dữ liệu: **{len(pages)}**", ""]
        lp = low_ctr_pages(pages)[:10]
        if lp:
            lines += ["### Trang xếp hạng tốt nhưng ít click (CTR thấp)", "",
                      "| URL | Hiển thị | Click | CTR % | Vị trí | Ước tính thêm click |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
            lines += [f"| {o['url']} | {o['impressions']} | {o['clicks']} | {o['ctr']} | {o['position']} | +{o['potential_gain']} |" for o in lp]
            lines.append("")
        sd = striking_distance(d.get("page_queries", []))[:15]
        if sd:
            lines += ["### Truy vấn sát trang một (vị trí 4–20)", "",
                      "| Truy vấn | Hiển thị | Click | Vị trí | Trang |", "| --- | ---: | ---: | ---: | --- |"]
            lines += [f"| {o['query']} | {o['impressions']} | {o['clicks']} | {o['position']} | {o['page']} |" for o in sd]
            lines.append("")
        if not lp and not sd:
            lines += ["Chưa có cơ hội đáng kể (dữ liệu còn ít).", ""]
    Path(path).write_text("\n".join(lines), encoding="utf-8")
