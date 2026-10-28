# -*- coding: utf-8 -*-
import json
import re
import sys
import urllib.request
import html as html_lib

sys.stdout.reconfigure(encoding='utf-8')

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")

# 1. Check style.min.css for img-block-0 and img-content and modid-109690
css = fetch("https://erx.vn/Styles/blue/style.min.css?v=1.7")
print("=== CSS RULES FOR img-block / img-content / list-block ===")
for m in re.finditer(r'([^{}]*(?:img-block|img-content|list-block|modid-109690)[^{}]*\{[^{}]*\})', css, re.I):
    print(" ", re.sub(r'\s+', ' ', m.group(1).strip()))

# 2. Check body of /hoi-thao.html
ht = fetch("https://erx.vn/hoi-thao.html")
b_idx = ht.find("<body")
ht_body = ht[b_idx:]
print("\n=== HOI THAO BODY CARD HTML ===")
idx_card = ht_body.find("TẠI SAO AND/OR")
if idx_card != -1:
    print(ht_body[max(0, idx_card-800):idx_card+1200])

print("\n=== ALL HOI THAO ITEMS ===")
for m in re.finditer(r'<a[^>]*href="([^"]*-(\d+)\.html)"[^>]*>\s*<h\d[^>]*>([\s\S]*?)</h\d>', ht_body, re.I):
    print(f"  {m.group(2)} | {html_lib.unescape(re.sub(r'<[^>]+>', '', m.group(3))).strip()} | {m.group(1)}")

# 3. Check all category listing pages to find any article titles with uppercase words
pages = [
    "/kien-thuc.html", "/mau-file-quan-ly-excel.html", "/excel-function.html",
    "/excel-vba.html", "/dashboard-automated-report.html", "/sql-in-excel.html",
    "/excel-365.html", "/power-bi.html", "/supply-chain-management.html",
    "/logistics-management.html", "/procurement-management.html",
    "/planning-management.html", "/warehouse-management.html",
    "/python-for-supply-chain.html", "/project-management.html", "/phan-mem.html"
]
seen = {}
for p in pages:
    try:
        ph = fetch("https://erx.vn" + p)
        pb = ph[ph.find("<body"):]
        for m in re.finditer(r'<a[^>]*href="([^"]*-(\d+)\.html)"[^>]*>\s*<h3[^>]*>([\s\S]*?)</h3>', pb, re.I):
            nid = m.group(2)
            title = html_lib.unescape(re.sub(r'<[^>]+>', '', m.group(3))).strip()
            seen[nid] = (title, m.group(1))
    except Exception as e:
        pass

print(f"\n=== ALL {len(seen)} VISIBLE ARTICLE TITLES ACROSS LISTING PAGES ===")
for nid, (title, url) in sorted(seen.items()):
    print(f"  {nid} | {title}")
