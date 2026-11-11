# -*- coding: utf-8 -*-
"""Tests for build_khoahoc_seo_upgrader.py and its generated Hoola Admin Console upgrader."""
import json
import re
import subprocess
import sys
from pathlib import Path

from build_khoahoc_seo_upgrader import (
    KHOAHOC_COURSES_SEO,
    KHOAHOC_HOME_SEO,
    KHOAHOC_INSTRUCTORS_SEO,
    KHOAHOC_PAGES_SEO,
    lookup_khoahoc_curated_seo,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_JS = ROOT / "pm_assets" / "khoahoc_seo_upgrader.js"


def test_all_khoahoc_curated_titles_and_descriptions_fit_bounds():
    entries = {
        "home": KHOAHOC_HOME_SEO,
        **KHOAHOC_COURSES_SEO,
        **KHOAHOC_PAGES_SEO,
        **KHOAHOC_INSTRUCTORS_SEO,
    }
    assert len(entries) == 29
    bad_titles = {k: len(v["title"]) for k, v in entries.items() if not (50 <= len(v["title"]) <= 65)}
    bad_descs = {k: len(v["meta_desc"]) for k, v in entries.items() if not (140 <= len(v["meta_desc"]) <= 160)}
    assert bad_titles == {}
    assert bad_descs == {}


def test_lookup_khoahoc_curated_seo_resolves_all_url_types():
    assert lookup_khoahoc_curated_seo("https://khoahoc.erx.vn/")["title"] == KHOAHOC_HOME_SEO["title"]
    assert lookup_khoahoc_curated_seo("https://khoahoc.erx.vn/course/master-vba")["title"] == KHOAHOC_COURSES_SEO["master-vba"]["title"]
    assert lookup_khoahoc_curated_seo("https://khoahoc.erx.vn/p/giang-vien")["title"] == KHOAHOC_PAGES_SEO["giang-vien"]["title"]
    assert lookup_khoahoc_curated_seo("https://khoahoc.erx.vn/instructor/nguyen-minh-ngoc")["title"] == KHOAHOC_INSTRUCTORS_SEO["nguyen-minh-ngoc"]["title"]
    assert lookup_khoahoc_curated_seo("https://khoahoc.erx.vn/unknown") is None


def test_khoahoc_upgrader_script_builds_and_exposes_meteor_methods():
    subprocess.run([sys.executable, str(ROOT / "build_khoahoc_seo_upgrader.py")], check=True, cwd=ROOT, capture_output=True)
    text = OUT_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.ERX_KHOAHOC_SEO_PAYLOAD = (\{.*?\n\});\n", text, re.S)
    assert m
    payload = json.loads(m.group(1))
    assert len(payload["courses"]) == 15
    assert len(payload["pages"]) == 10
    assert len(payload["instructors"]) == 3
    for method_name in (
        "Settings.methods.updateAppSetting",
        "Pages.methods.updateChildPageGrapeJS",
        "Courses.methods.updateCourseInfoGeneral",
        "Courses.methods.updateCourseDescription",
        "Instructors.methods.updateInstructor",
        "window.erxRunAllKhoahocSeoUpgrades",
    ):
        assert method_name in text

