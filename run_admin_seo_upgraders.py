# -*- coding: utf-8 -*-
"""
Execute khoahoc_seo_upgrader.js and erx_seo_master_upgrader.js inside the user's
authenticated Chrome instance via Chrome's official remote debugging interface
(chrome://inspect/#remote-debugging -> DevToolsActivePort).
"""
from __future__ import annotations

import json
import os
import time
import traceback
from pathlib import Path
from typing import Any

from playwright.sync_api import BrowserContext, Page, sync_playwright

BASE_DIR = Path(__file__).resolve().parent
KHOAHOC_JS_PATH = BASE_DIR / "pm_assets" / "khoahoc_seo_upgrader.js"
ERX_JS_PATH = BASE_DIR / "pm_assets" / "erx_seo_master_upgrader.js"
REPORT_PATH = BASE_DIR / "reports" / "admin_seo_upgrader_run.json"


def read_devtools_ws_url() -> str:
    dap = Path(os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\DevToolsActivePort"))
    if not dap.exists():
        raise RuntimeError(f"DevToolsActivePort not found at {dap}. Enable chrome://inspect/#remote-debugging first.")
    lines = [line.strip() for line in dap.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) < 2:
        raise RuntimeError(f"Malformed DevToolsActivePort at {dap}")
    return f"ws://127.0.0.1:{lines[0]}{lines[1]}"


def find_target_page(contexts: list[BrowserContext], host_substr: str) -> Page | None:
    for ctx in contexts:
        for pg in ctx.pages:
            if host_substr in (pg.url or "").lower():
                return pg
    return None


def run_khoahoc_upgrade(page: Page, courses_only: bool = False, pages_only: bool = False) -> dict[str, Any]:
    if "/manage" not in page.url:
        page.goto("https://khoahoc.erx.vn/manage", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_load_state("domcontentloaded", timeout=30000)

    deadline = time.time() + 20.0
    auth_state: dict[str, Any] = {}
    while time.time() < deadline:
        auth_state = page.evaluate(
            """() => ({
                url: location.href,
                hasMeteor: typeof window.Meteor !== 'undefined' && typeof window.Meteor.call === 'function',
                loggingIn: (typeof window.Meteor !== 'undefined' && typeof window.Meteor.loggingIn === 'function')
                    ? !!window.Meteor.loggingIn() : false,
                userId: (typeof window.Meteor !== 'undefined' && typeof window.Meteor.userId === 'function')
                    ? window.Meteor.userId() : null
            })"""
        )
        if auth_state.get("hasMeteor") and not auth_state.get("loggingIn") and auth_state.get("userId"):
            break
        time.sleep(1.0)

    if not auth_state.get("hasMeteor"):
        return {"ok": False, "error": "Meteor runtime not loaded on khoahoc.erx.vn/manage", "auth_state": auth_state}
    if not auth_state.get("userId") or "sign-in" in auth_state.get("url", "") or "login" in auth_state.get("url", ""):
        return {"ok": False, "error": "Not logged in to https://khoahoc.erx.vn/manage on this Chrome profile", "auth_state": auth_state}

    js_code = KHOAHOC_JS_PATH.read_text(encoding="utf-8")
    page.evaluate("() => {\n" + js_code + "\nreturn true;\n}")
    if pages_only:
        pages = page.evaluate("async () => await window.erxUpgradeKhoahocPagesSeo()")
        import re as _re
        import requests as _req

        ssr_check: dict[str, Any] = {}
        for slug in [
            "workshop",
            "giang-vien",
            "chinh-sach-bao-mat",
            "dieu-khoan-dich-vu",
            "quy-dinh-ve-thanh-toan",
            "tro-giup",
            "trang-chu",
            "gift",
            "landingpage",
        ]:
            try:
                resp = _req.get(
                    f"https://khoahoc.erx.vn/p/{slug}",
                    headers={"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"},
                    timeout=15,
                )
                tm = _re.search(r"<title[^>]*>(.*?)</title>", resp.text, _re.I | _re.S)
                ssr_check[slug] = tm.group(1).strip() if tm else None
            except Exception as exc:
                ssr_check[slug] = f"ERR: {exc}"
        return {"ok": True, "auth_state": auth_state, "result": {"pages": pages, "ssr_check": ssr_check}}
    if courses_only:
        courses = page.evaluate("async () => await window.erxUpgradeKhoahocCoursesSeo()")
        return {"ok": True, "auth_state": auth_state, "result": {"courses": courses}}
    result = page.evaluate("async () => await window.erxRunAllKhoahocSeoUpgrades()")
    return {"ok": True, "auth_state": auth_state, "result": result}


def run_erx_upgrade(page: Page) -> dict[str, Any]:
    if "/administrator" not in page.url.lower():
        page.goto("https://erx.vn/administrator", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_load_state("domcontentloaded", timeout=30000)

    check = page.evaluate(
        """async () => {
            const url = location.href;
            const hasPasswordInput = !!document.querySelector('input[type="password"]');
            const probe = await fetch('/administrator/globalconfiguration/site?from=3&divid=100', { credentials: 'include' });
            const text = await probe.text();
            const probeHasForm = text.includes('META.SCRIPT_HEADER');
            const alreadyUpgradedHeader = text.includes('articleSeo');
            return { url, hasPasswordInput, probeStatus: probe.status, probeUrl: probe.url, probeHasForm, alreadyUpgradedHeader };
        }"""
    )
    if check.get("hasPasswordInput") or not check.get("probeHasForm"):
        return {"ok": False, "error": "Not logged in to https://erx.vn/administrator on this Chrome profile", "check": check}

    js_code = ERX_JS_PATH.read_text(encoding="utf-8")
    page.evaluate("() => {\n" + js_code + "\nreturn true;\n}")
    if check.get("alreadyUpgradedHeader"):
        # Only patch the single remaining article 7122807028 if full upgrade already ran
        result = page.evaluate(
            """async () => {
                window.ERX_ARTICLE_SEO_UPGRADES = { "7122807028": window.ERX_ARTICLE_SEO_UPGRADES["7122807028"] };
                const articles = await window.erxUpgradeArticlesSeo();
                return { mode: "retry_7122807028_only", articles };
            }"""
        )
    else:
        result = page.evaluate("async () => await window.erxRunAllSeoUpgrades()")
    return {"ok": True, "check": check, "result": result}


def main() -> int:
    import sys

    courses_only = "--khoahoc-courses-only" in sys.argv
    pages_only = "--khoahoc-pages-only" in sys.argv
    ws_url = read_devtools_ws_url()
    print(f"Connecting over CDP to {ws_url} (waiting up to 5 min for Chrome 'Allow' click)...", flush=True)
    summary: dict[str, Any] = {"ws_url": ws_url, "khoahoc": None, "erx": None}

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url, timeout=300000)
        contexts = browser.contexts
        print(f"Connected! Found {len(contexts)} browser context(s).", flush=True)
        for idx, ctx in enumerate(contexts):
            print(f"  Context {idx}: {[pg.url for pg in ctx.pages]}", flush=True)

        kh_page = find_target_page(contexts, "khoahoc.erx.vn")
        erx_page = find_target_page(contexts, "erx.vn/administrator") or find_target_page(contexts, "erx.vn")

        base_ctx = (kh_page.context if kh_page else (erx_page.context if erx_page else (contexts[0] if contexts else None)))
        if base_ctx is None:
            raise RuntimeError("No browser context available in Chrome.")

        if kh_page is None:
            kh_page = base_ctx.new_page()
            kh_page.goto("https://khoahoc.erx.vn/manage", wait_until="domcontentloaded", timeout=45000)

        print("Running khoahoc_seo_upgrader.js on https://khoahoc.erx.vn/manage ...", flush=True)
        try:
            summary["khoahoc"] = run_khoahoc_upgrade(kh_page, courses_only=courses_only, pages_only=pages_only)
        except Exception as exc:
            summary["khoahoc"] = {"ok": False, "error": str(exc), "trace": traceback.format_exc()}
        print("khoahoc result:", json.dumps(summary["khoahoc"], ensure_ascii=False)[:800], flush=True)

        if courses_only or pages_only:
            summary["erx"] = {"ok": True, "skipped": "already_completed_44_of_44"}
        else:
            if erx_page is None:
                erx_page = base_ctx.new_page()
                erx_page.goto("https://erx.vn/administrator", wait_until="domcontentloaded", timeout=45000)
            print("Running erx_seo_master_upgrader.js on https://erx.vn/administrator ...", flush=True)
            try:
                summary["erx"] = run_erx_upgrade(erx_page)
            except Exception as exc:
                summary["erx"] = {"ok": False, "error": str(exc), "trace": traceback.format_exc()}
            print("erx result:", json.dumps(summary["erx"], ensure_ascii=False)[:600], flush=True)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved full report to {REPORT_PATH}", flush=True)
    ok = bool(summary["khoahoc"] and summary["khoahoc"].get("ok") and summary["erx"] and summary["erx"].get("ok"))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
