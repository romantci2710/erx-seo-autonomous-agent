# -*- coding: utf-8 -*-
"""
Deep SEO Audit of https://community.erx.vn/ across all 89 Sitemap URLs:
Checks HTTP status, <title>, <meta name="description">, <link rel="canonical">,
<h1>/<h2>, SSR text length, JSON-LD Schema, OpenGraph tags, and duplicate/short/missing metadata.
"""
import json
import re
import sys
import html as html_lib
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding="utf-8")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.getcode(), resp.read().decode("utf-8", "ignore")

code_rb, rb_txt = fetch("https://community.erx.vn/robots.txt")
print("=== ROBOTS.TXT ===")
print(rb_txt.strip())

code_sm, sm_xml = fetch("https://community.erx.vn/sitemap.xml")
urls = re.findall(r"<loc>(.*?)</loc>", sm_xml)
print(f"\n=== SITEMAP.XML ({len(urls)} URLs) ===")

def audit_url(u):
    try:
        code, raw = fetch(u)
        m_t = re.search(r"<title>(.*?)</title>", raw, re.I | re.S)
        title = html_lib.unescape(m_t.group(1).strip()) if m_t else ""

        m_d = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', raw, re.I | re.S)
        if not m_d:
            m_d = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', raw, re.I | re.S)
        desc = html_lib.unescape(m_d.group(1).strip()) if m_d else ""

        m_c = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', raw, re.I)
        if not m_c:
            m_c = re.search(r'<link\s+href=["\'](.*?)["\']\s+rel=["\']canonical["\']', raw, re.I)
        canonical = m_c.group(1).strip() if m_c else ""

        m_robots = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', raw, re.I)
        robots = m_robots.group(1).strip() if m_robots else ""

        m_og_img = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']', raw, re.I)
        if not m_og_img:
            m_og_img = re.search(r'<meta\s+content=["\'](.*?)["\']\s+property=["\']og:image["\']', raw, re.I)
        og_img = m_og_img.group(1).strip() if m_og_img else ""

        h1s = [html_lib.unescape(re.sub(r"<[^>]+>", " ", x)).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>", raw, re.I | re.S)]
        h2s = [html_lib.unescape(re.sub(r"<[^>]+>", " ", x)).strip() for x in re.findall(r"<h2[^>]*>(.*?)</h2>", raw, re.I | re.S)]

        lds = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', raw, re.I | re.S)
        ld_types = []
        for b in lds:
            try:
                obj = json.loads(b.strip())
                if isinstance(obj, list):
                    ld_types.extend([x.get("@type") for x in obj if isinstance(x, dict) and x.get("@type")])
                elif isinstance(obj, dict):
                    if "@graph" in obj:
                        ld_types.extend([x.get("@type") for x in obj["@graph"] if isinstance(x, dict)])
                    elif "@type" in obj:
                        ld_types.append(obj.get("@type"))
            except Exception as e:
                ld_types.append(f"INVALID_JSON({e})")

        # Visible body text (strip script and style)
        body_match = re.search(r"<body[^>]*>(.*?)</body>", raw, re.I | re.S)
        body_html = body_match.group(1) if body_match else raw
        clean_body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body_html, flags=re.I | re.S)
        clean_text = html_lib.unescape(re.sub(r"<[^>]+>", " ", clean_body))
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        internal_links = len(re.findall(r'<a\s+[^>]*href=["\'](?:/|https://community\.erx\.vn/)', body_html, re.I))

        return {
            "url": u,
            "code": code,
            "title": title,
            "tlen": len(title),
            "desc": desc,
            "dlen": len(desc),
            "canonical": canonical,
            "robots": robots,
            "og_img": og_img,
            "h1_cnt": len(h1s),
            "h1s": h1s,
            "h2_cnt": len(h2s),
            "ld_cnt": len(lds),
            "ld_types": ld_types,
            "body_chars": len(clean_text),
            "internal_links": internal_links,
            "text_preview": clean_text[:180]
        }
    except Exception as e:
        return {"url": u, "error": str(e)}

with ThreadPoolExecutor(max_workers=12) as ex:
    results = list(ex.map(audit_url, urls))

errors = [r for r in results if "error" in r or r.get("code") != 200]
print(f"HTTP 200 OK: {len(results) - len(errors)} / {len(results)} | Errors: {len(errors)}")
for e in errors:
    print("  ERR:", e)

valid = [r for r in results if "error" not in r]

# Group by route pattern
def classify(u):
    path = u.replace("https://community.erx.vn", "")
    if path in ("", "/"): return "1_home"
    if path in ("/forum/", "/tuyen-dung/", "/khoa-hoc/"): return "2_hub:" + path
    if path.startswith("/forum/chu-de/"): return "4_topic"
    if path.startswith("/forum/"): return "3_category"
    if path.startswith("/tuyen-dung/"): return "5_job"
    if path.startswith("/khoa-hoc/"): return "6_course"
    if path.startswith("/doanh-nghiep/"): return "7_company"
    if path.startswith("/thanh-vien/"): return "8_member"
    return "9_other"

by_group = {}
for r in valid:
    g = classify(r["url"])
    by_group.setdefault(g, []).append(r)

print("\n=== SUMMARY BY PAGE TYPE ===")
for g in sorted(by_group.keys()):
    items = by_group[g]
    sample = items[0]
    avg_chars = sum(x["body_chars"] for x in items) // len(items)
    avg_links = sum(x["internal_links"] for x in items) // len(items)
    short_t = sum(1 for x in items if x["tlen"] < 40)
    short_d = sum(1 for x in items if x["dlen"] < 100)
    no_h1 = sum(1 for x in items if x["h1_cnt"] == 0)
    no_ld = sum(1 for x in items if x["ld_cnt"] == 0)
    print(f"\n[{g}] Count={len(items)} | AvgBodyChars={avg_chars} | AvgLinks={avg_links} | ShortTitle(<40)={short_t} | ShortDesc(<100)={short_d} | NoH1={no_h1} | NoSchema={no_ld}")
    print(f"  Sample URL      : {sample['url']}")
    print(f"  Sample Title({sample['tlen']}): {sample['title']}")
    print(f"  Sample Desc({sample['dlen']}) : {sample['desc'][:140]}")
    print(f"  Sample Canonical: {sample['canonical']} | OG_Img: {sample['og_img']}")
    print(f"  Sample H1s      : {sample['h1s']} | H2s={sample['h2_cnt']} | Schema={sample['ld_types']}")
    print(f"  Sample Text     : {sample['text_preview']}")

# Check duplicate titles & descriptions
from collections import Counter
t_counts = Counter(x["title"] for x in valid)
d_counts = Counter(x["desc"] for x in valid)
print("\n=== DUPLICATE TITLES ===")
for t, cnt in t_counts.items():
    if cnt > 1:
        print(f"  ({cnt}x) {t}")
        for x in valid:
            if x["title"] == t:
                print(f"       -> {x['url']}")

print("\n=== DUPLICATE DESCRIPTIONS ===")
for d, cnt in d_counts.items():
    if cnt > 1:
        print(f"  ({cnt}x) {d[:100]}...")
        for x in valid:
            if x["desc"] == d:
                print(f"       -> {x['url']}")

print("\n=== SHORT OR LONG TITLES (<45 or >75 chars) ===")
for x in valid:
    if x["tlen"] < 45 or x["tlen"] > 75:
        print(f"  [{x['tlen']:3d}c] {x['url'].replace('https://community.erx.vn','')} -> {x['title']}")

print("\n=== SHORT OR GENERIC DESCRIPTIONS (<110 chars) ===")
for x in valid:
    if x["dlen"] < 110:
        print(f"  [{x['dlen']:3d}c] {x['url'].replace('https://community.erx.vn','')} -> {x['desc']}")

with open(r"D:\GIT\SEO Tool\pm_assets\community_seo_audit.json", "w", encoding="utf-8") as f:
    json.dump(valid, f, ensure_ascii=False, indent=2)
