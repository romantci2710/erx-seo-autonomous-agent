# -*- coding: utf-8 -*-
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")

pages = [
    "/", "/kien-thuc.html", "/mau-file-quan-ly-excel.html", "/excel-function.html",
    "/excel-vba.html", "/dashboard-automated-report.html", "/sql-in-excel.html",
    "/excel-365.html", "/power-bi.html", "/supply-chain-management.html",
    "/logistics-management.html", "/procurement-management.html",
    "/planning-management.html", "/warehouse-management.html",
    "/python-for-supply-chain.html", "/project-management.html", "/phan-mem.html"
]

missing_thumbs = []
total_cards = 0
for p in pages:
    html = fetch("https://erx.vn" + p)
    body = html[html.find("<body"):]
    cards = re.findall(r'<li class="list-block"[\s\S]*?</li>', body, re.I)
    for c in cards:
        total_cards += 1
        m_link = re.search(r'href="([^"]*-(\d+)\.html)"', c)
        m_img = re.search(r'<img[^>]*src="([^"]+)"', c)
        if m_link and (not m_img or "no-image" in m_img.group(1).lower() or not m_img.group(1).strip()):
            missing_thumbs.append((p, m_link.group(2), m_link.group(1)))

print(f"Total cards checked across {len(pages)} pages: {total_cards}")
print(f"Cards missing thumbnails: {len(missing_thumbs)}")
for item in missing_thumbs:
    print("  MISSING:", item)
