# AGENTS.md — Operational Playbook for MUSE Server Agent

This repository (`erx-seo-autonomous-agent`) is a self-contained **24/7 Autonomous SEO Loop Engine** for the entire `*.erx.vn` ecosystem:
1. `https://erx.vn` (Main Portal & Technical Blog)
2. `https://community.erx.vn` (Supply Chain, Procurement & AI Forum — repo: `romantci2710/scm-com`)
3. `https://project-management.erx.vn` (AI Project Gantt Planner PMBOK 8 — repo: `romantci2710/Gantt-Planner3.4.3`)
4. `https://doc-translate.erx.vn` (AI PDF & LaTeX Translator — repo: `romantci2710/Translator_Machine`)
5. `https://doc-builder.erx.vn` (AI Contract, Report & Legal Audit — repo: `romantci2710/build_document`)
6. `https://khoahoc.erx.vn` (ERX E-Learning Academy)

---

## 1. The Two Autonomous Loops

### Loop 1: Daily `07:00 AM` (Asia/Ho_Chi_Minh) Hot Keyword Discovery, Scoring & Auto-SEO
Every day at `07:00 AM`, `muse_seo_daemon.py` executes `run_daily_keyword_seo_cycle()`:
1. **Online Keyword Harvesting:** Queries live **Google Suggest / Autocomplete Vietnam** (`hl=vi&gl=vn`) with functional seeds and hot modifiers (`miễn phí`, `online`, `bằng ai`, `2026`, `phần mềm`, `công cụ`, `hướng dẫn`, `mẫu`) + **Google Trends Vietnam RSS** (`geo=VN`).
2. **Competitor SERP Evaluation & Opportunity Scoring (`0–100`):**
   - Crawls live pages on our 6 platforms and compares them against Top-3 organic competitors (`1office.vn`, `base.vn`, `smallpdf.com`, `ilovepdf.com`, `supawork.ai`, `luathoangan.vn`, `vilas.edu.vn`, `datapot.edu.vn`, etc.).
   - Scores every keyword by **Search Intent (35 pts)** + **Platform Coverage Gap (35 pts)** + **SERP Outranking Feasibility (30 pts)**.
   - Filters out keywords already optimized within the last 14 days (`state/seo_state.json`).
3. **Automated SEO Execution:**
   - Selects the highest-scoring unoptimized keyword for each platform.
   - Generates optimized `<title>` (50–65 chars), `<meta name="description">` (145–160 chars), `META_KEY`, **Schema.org `FAQPage` JSON-LD**, and an **Outranking Comparison `<table>` HTML snippet**.
   - Pushes updates to `erx.vn/administrator` (if `ERX_ADMIN_COOKIE` is set), syncs keyword manifests to sibling repos via `muse_repo_auto_deployer.py`, warms SSR caches, and writes `reports/daily_keyword_seo_YYYY-MM-DD.md`.

### Loop 2: Continuous `15-Minute` Platform Content & Tag Watcher
Every `15 minutes` (`900 seconds`), `muse_seo_daemon.py` executes `run_platform_watcher_cycle()`:
1. Fetches `sitemap.xml` across all 6 platforms + `/api/community/topics` on `community.erx.vn`.
2. Computes a SHA-256 fingerprint of each page's `<title>`, `<meta name="description">`, `<link rel="canonical">`, `<h1>`, `<h2>`, `<table>` count, `application/ld+json` schemas, and inline base64 PNG weight.
3. Detects:
   - **`NEW_URL`:** Newly published blog articles, forum topics, or landing pages.
   - **`TAG_MODIFIED`:** Any manual or CMS edit to `<title>`, `<meta name="description">`, or `<link rel="canonical">`.
   - **`SEO_DEFECT`:** Missing/short/duplicate meta description, ALL-CAPS title, missing canonical, missing JSON-LD, or heavy inline base64 PNGs (`>250 KB`).
4. **Immediate Auto-Remediation:**
   - Synthesizes compliant SEO tags in `reports/auto_remediation_queue.json` & `reports/erx_cms_auto_patch.js`.
   - Warms `/api/community/topics/{id}` and `/forum/chu-de/{slug}-{id}` on `community.erx.vn` so newly uploaded `.html` attachments have their semantic text (`<h2>, <h3>, <p>, <ul>, <table>`) extracted and cached for Googlebot immediately.

---

## 2. How MUSE Agent Should Run This Repository on the Server

### Option A: Docker Compose (Recommended for 24/7 Server Deployment)
```bash
cp .env.example .env
docker compose up -d --build
docker compose logs -f
```

### Option B: Direct Python Daemon / Systemd Service
```bash
pip install -r requirements.txt
python3 muse_seo_daemon.py --mode daemon --daily-time 07:00 --watch-interval 900
```

### Option C: Single-Pass Execution (For Agent Tool Calls or External Cron)
```bash
# Run both Loop 1 (Keyword Discovery & Auto-SEO) and Loop 2 (Platform Watcher) once:
python3 muse_seo_daemon.py --mode once

# Run only Loop 1 (07:00 AM Hot Keyword SEO Cycle):
python3 muse_seo_daemon.py --mode keyword-only

# Run only Loop 2 (15-Minute Platform Content & Tag Watcher):
python3 muse_seo_daemon.py --mode watch-only

# Sync generated keyword manifests to sibling Git repositories:
python3 muse_repo_auto_deployer.py
```

---

## 3. Key Output Files for MUSE Agent Inspection
- `state/seo_state.json`: Persistent history of all daily runs and optimized keywords.
- `state/platform_watch_state.json`: SHA-256 fingerprint registry of all monitored URLs and community topics.
- `state/keyword_seo_injections.json`: Full structured payloads (`<title>`, `<meta description>`, `FAQPage` JSON-LD, comparison `<table>` HTML) for every selected keyword.
- `reports/latest_loop_status.json` & `reports/latest_loop_report.md`: Latest 15-minute watcher status and detected tag modifications.
- `reports/daily_keyword_seo_YYYY-MM-DD.md`: Daily 07:00 AM keyword research & auto-SEO execution report.
- `reports/auto_remediation_queue.json`: Actionable queue of pages needing immediate tag remediation.
