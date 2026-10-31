# -*- coding: utf-8 -*-
"""
SEO experiment ledger (standard library only).

Every change to a live page (title, meta description...) is recorded in state/experiments.json with the
old/new values and a Search Console baseline. After 14 and 21 days the daemon measures the page again and
compares clicks/impressions per day, CTR and position. Results are correlational, not proof of cause.

CLI:
    python experiments.py add --url URL --old-title "..." --new-title "..." [--old-meta "..." --new-meta "..."]
                              [--date YYYY-MM-DD] [--note "..."]
    python experiments.py measure      # measure everything that is due and rewrite the report
    python experiments.py list
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Callable

import gsc_client

BASE_DIR = Path(__file__).resolve().parent
LEDGER_PATH = BASE_DIR / "state" / "experiments.json"
REPORT_PATH = BASE_DIR / "reports" / "experiments_latest.md"
CONFIG_PATH = BASE_DIR / "config" / "platforms.json"

GSC_LAG_DAYS = 3          # Search Console data trails real time by about 2-3 days
BASELINE_DAYS = 28
MEASURE_DAYS = (14, 21)
MIN_IMPRESSIONS = 200     # below this the post-change window is too small to judge
IMPROVED_CLICKS_PCT = 20.0
REGRESSED_CLICKS_PCT = -20.0
REGRESSED_POSITION_DELTA = 2.0  # average position worse by this many places
FetchRows = Callable[[str, str, str], list[dict[str, Any]]]
ResolveProperty = Callable[[str], "str | None"]


# ---------------------------------------------------------------------------
# Ledger persistence
# ---------------------------------------------------------------------------

def load_ledger(path: Path = LEDGER_PATH) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("experiments"), list):
            return data
    except Exception:
        pass
    return {"experiments": []}


def save_ledger(path: Path, ledger: dict[str, Any]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add_experiment(
    ledger: dict[str, Any],
    *,
    url: str,
    change_date: dt.date,
    kind: str,
    old: dict[str, Any],
    new: dict[str, Any],
    baseline: dict[str, Any] | None,
    note: str = "",
) -> dict[str, Any]:
    prefix = f"exp-{change_date:%Y%m%d}-"
    seq = sum(1 for e in ledger["experiments"] if e["id"].startswith(prefix)) + 1
    exp = {
        "id": f"{prefix}{seq:03d}",
        "url": url,
        "date": change_date.isoformat(),
        "kind": kind,
        "old": old,
        "new": new,
        "baseline": baseline,
        "note": note,
        "status": "pending",
        "measurements": {},
    }
    ledger["experiments"].append(exp)
    return exp


# ---------------------------------------------------------------------------
# Windows and measurement
# ---------------------------------------------------------------------------

def baseline_window(change_date: dt.date) -> tuple[dt.date, dt.date]:
    """28 complete days that end before the change (accounting for the Search Console lag)."""
    end = change_date - dt.timedelta(days=GSC_LAG_DAYS)
    return end - dt.timedelta(days=BASELINE_DAYS - 1), end


def measurement_window(change_date: dt.date, days: int) -> tuple[dt.date, dt.date]:
    return change_date + dt.timedelta(days=1), change_date + dt.timedelta(days=days)


def summarize_rows(rows: list[dict[str, Any]], url: str) -> dict[str, Any] | None:
    mine = [r for r in rows if r["keys"][0] == url]
    if not mine:
        return None
    clicks = sum(r["clicks"] for r in mine)
    impressions = sum(r["impressions"] for r in mine)
    position = sum(r["position"] * r["impressions"] for r in mine) / impressions if impressions else 0.0
    return {
        "clicks": clicks,
        "impressions": impressions,
        "ctr": clicks / impressions if impressions else 0.0,
        "position": round(position, 2),
    }


def due_measurements(ledger: dict[str, Any], today: dt.date) -> list[tuple[dict[str, Any], int]]:
    available_until = today - dt.timedelta(days=GSC_LAG_DAYS)
    due = []
    for exp in ledger["experiments"]:
        change = dt.date.fromisoformat(exp["date"])
        for days in MEASURE_DAYS:
            if str(days) not in exp["measurements"] and available_until >= change + dt.timedelta(days=days):
                due.append((exp, days))
    return due


def _pct(new: float, old: float) -> float | None:
    return round((new - old) / old * 100, 1) if old else None


def compute_result(baseline: dict[str, Any] | None, post: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "post_clicks_per_day": round(post["clicks"] / post["days"], 2),
        "post_impressions_per_day": round(post["impressions"] / post["days"], 1),
        "post_ctr": post["ctr"],
        "post_position": post["position"],
    }
    if not baseline or post["impressions"] < MIN_IMPRESSIONS:
        result["verdict"] = "insufficient_data"
        return result
    base_cpd = baseline["clicks"] / baseline["days"]
    base_ipd = baseline["impressions"] / baseline["days"]
    result.update(
        {
            "baseline_clicks_per_day": round(base_cpd, 2),
            "baseline_impressions_per_day": round(base_ipd, 1),
            "baseline_ctr": baseline["ctr"],
            "baseline_position": baseline["position"],
            "clicks_per_day_change_pct": _pct(result["post_clicks_per_day"], base_cpd),
            "impressions_per_day_change_pct": _pct(result["post_impressions_per_day"], base_ipd),
            "ctr_change_pct": _pct(post["ctr"], baseline["ctr"]),
            "position_delta": round(post["position"] - baseline["position"], 2),  # positive = worse rank
        }
    )
    change = result["clicks_per_day_change_pct"]
    if result["position_delta"] >= REGRESSED_POSITION_DELTA or (change is not None and change <= REGRESSED_CLICKS_PCT):
        result["verdict"] = "regressed"
    elif change is None:
        result["verdict"] = "improved" if result["post_clicks_per_day"] >= 1 else "neutral"
    elif change >= IMPROVED_CLICKS_PCT:
        result["verdict"] = "improved"
    else:
        result["verdict"] = "neutral"
    return result


def run_due_measurements(
    ledger: dict[str, Any], today: dt.date, fetch_page_rows: FetchRows, resolve_property: ResolveProperty
) -> list[dict[str, Any]]:
    done = []
    for exp, days in due_measurements(ledger, today):
        prop = resolve_property(exp["url"])
        if not prop:
            continue
        change = dt.date.fromisoformat(exp["date"])
        start, end = measurement_window(change, days)
        rows = fetch_page_rows(prop, start.isoformat(), end.isoformat())
        post = summarize_rows(rows, exp["url"]) or {"clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0}
        post["days"] = days
        result = compute_result(exp.get("baseline"), post)
        exp["measurements"][str(days)] = {
            **result,
            "measured_on": today.isoformat(),
            "window": [start.isoformat(), end.isoformat()],
        }
        exp["status"] = "measured" if all(str(d) in exp["measurements"] for d in MEASURE_DAYS) else "partial"
        done.append({"id": exp["id"], "url": exp["url"], "days": days, **result})
    return done


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def _fmt(value: Any, suffix: str = "") -> str:
    return "-" if value is None else f"{value}{suffix}"


def write_experiments_report(path: Path, ledger: dict[str, Any], today: dt.date) -> None:
    lines = [
        "# Sổ thí nghiệm SEO",
        f"- **Cập nhật:** `{today.isoformat()}`",
        "- So sánh theo **tốc độ mỗi ngày** (click, hiển thị) giữa 28 ngày trước khi đổi và cửa sổ sau khi đổi.",
        "- Kết quả chỉ là tương quan, không phải bằng chứng nhân quả: cập nhật thuật toán của Google, mùa vụ hay thay đổi khác có thể trùng thời gian.",
        "",
    ]
    if not ledger["experiments"]:
        lines.append("Chưa có thí nghiệm nào. Dùng `python experiments.py add ...` để ghi nhận thay đổi.")
    for exp in ledger["experiments"]:
        base = exp.get("baseline")
        lines += [f"## {exp['id']} — {exp['url']}", "",
                  f"- Ngày đổi: **{exp['date']}**, loại: `{exp['kind']}`, trạng thái: `{exp['status']}`"]
        if exp.get("note"):
            lines.append(f"- Ghi chú: {exp['note']}")
        for key in ("title", "meta_description"):
            if exp["old"].get(key) or exp["new"].get(key):
                lines += [f"- {key} cũ: {exp['old'].get(key, '')}", f"- {key} mới: {exp['new'].get(key, '')}"]
        if base:
            lines.append(
                f"- Số liệu nền ({base['start']} → {base['end']}): {base['clicks']} click, {base['impressions']} hiển thị, "
                f"CTR {base['ctr'] * 100:.2f}%, vị trí {base['position']}"
            )
        else:
            lines.append("- Chưa có số liệu nền.")
        lines += ["", "| Sau | Cửa sổ | Click/ngày | Hiển thị/ngày | CTR | Vị trí | Δ click/ngày | Δ vị trí | Nhận xét |",
                  "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
        for days in MEASURE_DAYS:
            m = exp["measurements"].get(str(days))
            if not m:
                lines.append(f"| {days} ngày | chưa đến hạn | | | | | | | |")
                continue
            lines.append(
                f"| {days} ngày | {m['window'][0]} → {m['window'][1]} | {m['post_clicks_per_day']} | "
                f"{m['post_impressions_per_day']} | {m['post_ctr'] * 100:.2f}% | {m['post_position']} | "
                f"{_fmt(m.get('clicks_per_day_change_pct'), '%')} | {_fmt(m.get('position_delta'))} | `{m['verdict']}` |"
            )
        lines.append("")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Search Console wiring and CLI
# ---------------------------------------------------------------------------

def property_resolver(config_path: Path = CONFIG_PATH) -> ResolveProperty:
    try:
        platforms = json.loads(Path(config_path).read_text(encoding="utf-8")).get("platforms", [])
    except Exception:
        platforms = []
    by_domain = {p["domain"]: p.get("gsc_property") for p in platforms}
    return lambda url: by_domain.get(urllib.parse.urlparse(url).netloc.lower())


def default_gsc_fetcher() -> FetchRows | None:
    """Fetch page-level Search Console rows, or None when credentials are not available."""
    creds = gsc_client.load_credentials()
    token = gsc_client.get_access_token(creds) if creds else None
    if not token:
        return None
    quota = creds.get("quota_project_id")
    return lambda prop, start, end: gsc_client.fetch_rows(prop, start, end, ["page"], token, quota_project=quota)


def _baseline_for(url: str, change_date: dt.date, fetch: FetchRows | None, resolve: ResolveProperty) -> dict[str, Any] | None:
    prop = resolve(url)
    if not (prop and fetch):
        return None
    start, end = baseline_window(change_date)
    summary = summarize_rows(fetch(prop, start.isoformat(), end.isoformat()), url)
    if not summary:
        return None
    return {"start": start.isoformat(), "end": end.isoformat(), "days": BASELINE_DAYS, **summary}


def main(
    argv: list[str] | None = None,
    ledger_path: Path = LEDGER_PATH,
    fetch_page_rows: FetchRows | None = None,
    resolve_property: ResolveProperty | None = None,
) -> int:
    ap = argparse.ArgumentParser(description="SEO experiment ledger")
    sub = ap.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add", help="record a change to a live page")
    add.add_argument("--url", required=True)
    add.add_argument("--date", default=None, help="change date, default today")
    add.add_argument("--old-title")
    add.add_argument("--new-title")
    add.add_argument("--old-meta")
    add.add_argument("--new-meta")
    add.add_argument("--note", default="")
    sub.add_parser("measure", help="measure experiments that are due")
    sub.add_parser("list", help="print the ledger")
    args = ap.parse_args(argv)

    resolve = resolve_property or property_resolver()
    ledger = load_ledger(ledger_path)
    today = dt.date.today()

    if args.cmd == "add":
        change_date = dt.date.fromisoformat(args.date) if args.date else today
        old = {k: v for k, v in (("title", args.old_title), ("meta_description", args.old_meta)) if v}
        new = {k: v for k, v in (("title", args.new_title), ("meta_description", args.new_meta)) if v}
        has_title = bool(args.new_title or args.old_title)
        has_meta = bool(args.new_meta or args.old_meta)
        kind = "title+meta" if has_title and has_meta else "title" if has_title else "meta" if has_meta else "other"
        fetch = fetch_page_rows or default_gsc_fetcher()
        baseline = _baseline_for(args.url, change_date, fetch, resolve)
        if baseline is None:
            print("Cảnh báo: chưa lấy được số liệu nền từ Search Console; thí nghiệm sẽ ở trạng thái thiếu dữ liệu.", file=sys.stderr)
        exp = add_experiment(ledger, url=args.url, change_date=change_date, kind=kind, old=old, new=new,
                             baseline=baseline, note=args.note)
        save_ledger(ledger_path, ledger)
        print(f"Đã ghi {exp['id']}")
        return 0

    if args.cmd == "measure":
        fetch = fetch_page_rows or default_gsc_fetcher()
        if not fetch:
            print("Không có thông tin xác thực Search Console.", file=sys.stderr)
            return 1
        done = run_due_measurements(ledger, today, fetch, resolve)
        save_ledger(ledger_path, ledger)
        write_experiments_report(REPORT_PATH, ledger, today)
        print(f"Đã đo {len(done)} lần đo.")
        return 0

    for exp in ledger["experiments"]:
        print(exp["id"], exp["date"], exp["status"], exp["url"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
