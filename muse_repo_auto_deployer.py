#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MUSE Auto-Deployer & Git Synchronizer (`muse_repo_auto_deployer.py`)
====================================================================
Called automatically by `muse_seo_daemon.py` (or directly by the MUSE Server Agent)
after each 07:00 AM Keyword SEO Cycle or Platform Watcher Cycle.

Responsibilities:
  1. Synchronizes the latest `state/` and `reports/` snapshots.
  2. Exports platform-specific dynamic SEO keyword & FAQ JSON manifests into target repos
     if local clones exist (`Gantt-Planner3.4.3`, `PDFMathTranslate-3`/`Translator_Machine`,
     `Build document`/`build_document`, `Supply_chain_community`/`scm-com`).
  3. Optionally commits & pushes updates when `AUTO_GIT_COMMIT=true` is set in `.env`.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "platforms.json"
INJECTIONS_FILE = BASE_DIR / "state" / "keyword_seo_injections.json"
REPORTS_DIR = BASE_DIR / "reports"

logger = logging.getLogger("muse_repo_auto_deployer")


def find_local_repo(candidates: list[str]) -> Path | None:
    for cand in candidates:
        p = Path(cand)
        if not p.is_absolute():
            p = (BASE_DIR / cand).resolve()
        if p.exists() and (p / ".git").exists():
            return p
    return None


def sync_injections_to_platform_repos() -> dict[str, Any]:
    if not CONFIG_PATH.exists() or not INJECTIONS_FILE.exists():
        return {"synced_repos": [], "status": "missing_config_or_injections"}

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    injections_data = json.loads(INJECTIONS_FILE.read_text(encoding="utf-8"))
    injections = injections_data.get("injections", [])

    synced_repos: list[dict[str, Any]] = []
    auto_commit = os.environ.get("AUTO_GIT_COMMIT", "false").lower() in ("1", "true", "yes")

    for platform in config.get("platforms", []):
        pid = platform["id"]
        repo_dir = find_local_repo(platform.get("local_repo_candidates", []))
        if not repo_dir:
            continue

        platform_injections = [x for x in injections if x.get("platform_id") == pid]
        if not platform_injections:
            continue

        # Write latest dynamic keyword & FAQ enrichment manifest into the repo's public/seo directory if present
        target_manifest_dir = repo_dir / "public"
        if not target_manifest_dir.exists():
            target_manifest_dir = repo_dir / "frontend" / "public"
        if not target_manifest_dir.exists():
            target_manifest_dir = repo_dir / "reports"
        if not target_manifest_dir.exists():
            continue

        manifest_path = target_manifest_dir / "erx-auto-seo-keywords.json"
        manifest_payload = {
            "platform_id": pid,
            "domain": platform["domain"],
            "keyword_count": len(platform_injections),
            "keywords": platform_injections[-30:],
        }
        manifest_path.write_text(
            json.dumps(manifest_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        committed = False
        if auto_commit:
            try:
                subprocess.run(
                    ["git", "add", str(manifest_path.relative_to(repo_dir))],
                    cwd=str(repo_dir),
                    check=True,
                    capture_output=True,
                )
                diff_proc = subprocess.run(
                    ["git", "status", "--porcelain", str(manifest_path.relative_to(repo_dir))],
                    cwd=str(repo_dir),
                    capture_output=True,
                    text=True,
                )
                if diff_proc.stdout.strip():
                    subprocess.run(
                        ["git", "commit", "-m", f"chore(seo): auto-update keyword manifest for {platform['domain']}"],
                        cwd=str(repo_dir),
                        check=True,
                        capture_output=True,
                    )
                    committed = True
            except Exception as exc:
                logger.warning("Auto-commit skipped for %s: %s", repo_dir, exc)

        synced_repos.append(
            {
                "platform_id": pid,
                "repo_path": str(repo_dir),
                "manifest_path": str(manifest_path),
                "keywords_synced": len(platform_injections[-30:]),
                "auto_committed": committed,
            }
        )

    return {"status": "ok", "synced_repos": synced_repos}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    res = sync_injections_to_platform_repos()
    print(json.dumps(res, ensure_ascii=False, indent=2))
