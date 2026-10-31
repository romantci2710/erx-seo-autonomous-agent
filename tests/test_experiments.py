# -*- coding: utf-8 -*-
"""Experiment ledger: record SEO changes and measure them 14/21 days later from Search Console."""
import datetime as dt
import json

import experiments as ex

URL = "https://erx.vn/ham-textsplit.html"
D = dt.date(2026, 10, 31)


def _row(url, clicks, impressions, position):
    return {"keys": [url], "clicks": clicks, "impressions": impressions,
            "ctr": clicks / impressions if impressions else 0, "position": position}


def _baseline(clicks=89, impressions=9513, position=5.2, days=28):
    return {"start": "2026-10-01", "end": "2026-10-28", "days": days, "clicks": clicks,
            "impressions": impressions, "ctr": clicks / impressions, "position": position}


# ---- summarising rows ----

def test_summarize_rows_filters_by_url_and_weights_position_by_impressions():
    rows = [_row(URL, 10, 100, 4.0), _row(URL, 10, 300, 8.0), _row("https://erx.vn/other", 99, 999, 1.0)]
    s = ex.summarize_rows(rows, URL)
    assert (s["clicks"], s["impressions"]) == (20, 400)
    assert s["position"] == 7.0  # (4*100 + 8*300) / 400
    assert s["ctr"] == 0.05
    assert ex.summarize_rows([], URL) is None


def test_baseline_window_ends_before_the_change_with_gsc_lag():
    assert ex.baseline_window(D) == (dt.date(2026, 10, 1), dt.date(2026, 10, 28))


# ---- ledger ----

def test_ledger_roundtrip_and_ids(tmp_path):
    path = tmp_path / "experiments.json"
    ledger = ex.load_ledger(path)
    assert ledger == {"experiments": []}
    a = ex.add_experiment(ledger, url=URL, change_date=D, kind="title+meta",
                          old={"title": "a"}, new={"title": "b"}, baseline=_baseline())
    b = ex.add_experiment(ledger, url=URL + "2", change_date=D, kind="title", old={}, new={}, baseline=None)
    assert a["id"] == "exp-20261031-001" and b["id"] == "exp-20261031-002"
    ex.save_ledger(path, ledger)
    assert ex.load_ledger(path)["experiments"][0]["url"] == URL
    path.write_text("broken", encoding="utf-8")
    assert ex.load_ledger(path) == {"experiments": []}


# ---- when to measure ----

def test_due_measurements_wait_for_gsc_lag():
    ledger = {"experiments": []}
    e = ex.add_experiment(ledger, url=URL, change_date=D, kind="title", old={}, new={}, baseline=_baseline())
    assert ex.due_measurements(ledger, dt.date(2026, 11, 16)) == []          # 14 days + 3 lag not reached
    assert [(x["id"], n) for x, n in ex.due_measurements(ledger, dt.date(2026, 11, 17))] == [(e["id"], 14)]
    assert [n for _, n in ex.due_measurements(ledger, dt.date(2026, 11, 24))] == [14, 21]


def test_measurement_window_starts_the_day_after_the_change():
    assert ex.measurement_window(D, 14) == (dt.date(2026, 11, 1), dt.date(2026, 11, 14))
    assert ex.measurement_window(D, 21) == (dt.date(2026, 11, 1), dt.date(2026, 11, 21))


# ---- evaluating ----

def test_compute_result_uses_per_day_rates_and_flags_improvement():
    post = {"days": 14, "clicks": 140, "impressions": 4800, "ctr": 140 / 4800, "position": 5.0}
    r = ex.compute_result(_baseline(), post)
    assert round(r["baseline_clicks_per_day"], 2) == round(89 / 28, 2)
    assert round(r["post_clicks_per_day"], 2) == 10.0
    assert r["clicks_per_day_change_pct"] > 100
    assert r["verdict"] == "improved"


def test_compute_result_verdicts():
    base = _baseline()
    neutral = ex.compute_result(base, {"days": 14, "clicks": 45, "impressions": 4700, "ctr": 45 / 4700, "position": 5.3})
    assert neutral["verdict"] == "neutral"
    worse = ex.compute_result(base, {"days": 14, "clicks": 20, "impressions": 4700, "ctr": 20 / 4700, "position": 5.3})
    assert worse["verdict"] == "regressed"
    rank_drop = ex.compute_result(base, {"days": 14, "clicks": 45, "impressions": 4700, "ctr": 45 / 4700, "position": 8.0})
    assert rank_drop["verdict"] == "regressed"
    few = ex.compute_result(base, {"days": 14, "clicks": 1, "impressions": 50, "ctr": 0.02, "position": 5.0})
    assert few["verdict"] == "insufficient_data"
    assert ex.compute_result(None, {"days": 14, "clicks": 9, "impressions": 900, "ctr": 0.01, "position": 5})["verdict"] == "insufficient_data"


# ---- running due measurements ----

def test_run_due_measurements_fetches_window_once_and_never_remeasures():
    ledger = {"experiments": []}
    e = ex.add_experiment(ledger, url=URL, change_date=D, kind="title", old={}, new={}, baseline=_baseline())
    calls = []

    def fetch(prop, start, end):
        calls.append((prop, start, end))
        return [_row(URL, 140, 4800, 5.0)]

    prop = lambda url: "sc-domain:erx.vn"
    done = ex.run_due_measurements(ledger, dt.date(2026, 11, 17), fetch, prop)
    assert len(done) == 1 and calls == [("sc-domain:erx.vn", "2026-11-01", "2026-11-14")]
    assert e["measurements"]["14"]["verdict"] == "improved"
    assert ex.run_due_measurements(ledger, dt.date(2026, 11, 17), fetch, prop) == []   # already measured
    assert len(calls) == 1


def test_run_due_measurements_skips_unknown_property_and_empty_data():
    ledger = {"experiments": []}
    ex.add_experiment(ledger, url=URL, change_date=D, kind="title", old={}, new={}, baseline=_baseline())
    assert ex.run_due_measurements(ledger, dt.date(2026, 11, 17), lambda *a: [], lambda u: None) == []
    done = ex.run_due_measurements(ledger, dt.date(2026, 11, 17), lambda *a: [], lambda u: "sc-domain:erx.vn")
    assert done[0]["verdict"] == "insufficient_data"  # no rows for the URL in the window


# ---- report and CLI ----

def test_report_lists_experiments_and_results(tmp_path):
    ledger = {"experiments": []}
    e = ex.add_experiment(ledger, url=URL, change_date=D, kind="title+meta",
                          old={"title": "Tiêu đề cũ"}, new={"title": "Tiêu đề mới"}, baseline=_baseline())
    ex.run_due_measurements(ledger, dt.date(2026, 11, 17), lambda *a: [_row(URL, 140, 4800, 5.0)], lambda u: "p")
    out = tmp_path / "r.md"
    ex.write_experiments_report(out, ledger, dt.date(2026, 11, 17))
    text = out.read_text(encoding="utf-8")
    assert e["id"] in text and URL in text and "Tiêu đề cũ" in text and "Tiêu đề mới" in text
    assert "improved" in text and "tương quan" in text.lower()


def test_cli_add_records_experiment_with_fetched_baseline(tmp_path):
    path = tmp_path / "experiments.json"
    seen = {}

    def fetch(prop, start, end):
        seen["window"] = (prop, start, end)
        return [_row(URL, 89, 9513, 5.2)]

    rc = ex.main(["add", "--url", URL, "--date", "2026-10-31", "--old-title", "cũ", "--new-title", "mới",
                  "--note", "TEXTSPLIT"], ledger_path=path, fetch_page_rows=fetch, resolve_property=lambda u: "sc-domain:erx.vn")
    assert rc == 0
    data = json.loads(path.read_text(encoding="utf-8"))["experiments"][0]
    assert seen["window"] == ("sc-domain:erx.vn", "2026-10-01", "2026-10-28")
    assert data["baseline"]["clicks"] == 89 and data["old"]["title"] == "cũ" and data["new"]["title"] == "mới"
    assert data["kind"] == "title" and data["note"] == "TEXTSPLIT"


# ---- daemon integration ----

def test_daemon_experiment_cycle_measures_due_items_and_writes_report(tmp_path):
    import muse_seo_daemon as d

    ledger_path = tmp_path / "experiments.json"
    report_path = tmp_path / "experiments_latest.md"
    ledger = ex.load_ledger(ledger_path)
    ex.add_experiment(ledger, url=URL, change_date=D, kind="title", old={"title": "a"}, new={"title": "b"}, baseline=_baseline())
    ex.save_ledger(ledger_path, ledger)

    out = d.run_experiment_cycle(
        ledger_path=ledger_path, report_path=report_path, today=dt.date(2026, 11, 17),
        fetch=lambda prop, start, end: [_row(URL, 140, 4800, 5.0)], resolve=lambda url: "sc-domain:erx.vn",
    )
    assert out == {"status": "ok", "measured": 1, "verdicts": ["improved"]}
    assert ex.load_ledger(ledger_path)["experiments"][0]["measurements"]["14"]["verdict"] == "improved"
    assert URL in report_path.read_text(encoding="utf-8")


def test_daemon_experiment_cycle_skips_without_credentials(tmp_path, monkeypatch):
    import muse_seo_daemon as d

    monkeypatch.setattr(ex, "default_gsc_fetcher", lambda: None)
    out = d.run_experiment_cycle(ledger_path=tmp_path / "e.json", report_path=tmp_path / "r.md", today=D)
    assert out == {"status": "skipped_no_credentials"}
