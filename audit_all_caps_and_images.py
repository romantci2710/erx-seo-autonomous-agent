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

# 1. Inspect homepage HTML for inline uppercase, module titles, footer modules, and image blocks
home_html = fetch("https://erx.vn/")
print("=== 1. INLINE text-transform: uppercase ON HOMEPAGE ===")
for m in re.finditer(r'.{0,120}uppercase.{0,120}', home_html, re.I):
    print("  ", m.group(0).strip())

print("\n=== 2. FOOTER MODULES ON HOMEPAGE ===")
idx_ft = home_html.find("dv-footer-top")
if idx_ft != -1:
    print(home_html[idx_ft:idx_ft+6000])

# 2. Inspect CSS files for text-transform: uppercase and .img-block rules
css_urls = re.findall(r'href=["\']([^"\']+\.css[^"\']*)["\']', home_html, re.I)
print("\n=== 3. CSS FILES ON ERX.VN ===")
for cu in css_urls:
    if any(k in cu.lower() for k in ["bootstrap", "font-awesome", "owl", "animate", "aos"]):
        continue
    full_cu = "https://erx.vn" + cu if cu.startswith("/") else cu
    try:
        css_txt = fetch(full_cu)
        up_rules = re.findall(r'([^{}]+\{[^{}]*text-transform\s*:\s*uppercase[^{}]*\})', css_txt, re.I)
        img_rules = re.findall(r'([^{}]*img-block[^{}]*\{[^{}]*\})', css_txt, re.I)
        print(f"CSS: {cu} | uppercase rules: {len(up_rules)} | img-block rules: {len(img_rules)}")
        for r in up_rules:
            print("  [UPPERCASE RULE]", re.sub(r'\s+', ' ', r.strip()))
        for r in img_rules[:15]:
            print("  [IMG-BLOCK RULE]", re.sub(r'\s+', ' ', r.strip()))
    except Exception as e:
        print(f"CSS error {cu}: {e}")

# 3. Inspect /hoi-thao.html, /dao-tao-doanh-nghiep.html, /phan-mem.html
for page_slug in ["/hoi-thao.html", "/dao-tao-doanh-nghiep.html", "/phan-mem.html", "/kien-thuc.html"]:
    p_html = fetch("https://erx.vn" + page_slug)
    titles = [html_lib.unescape(re.sub(r'<[^>]+>', '', t)).strip() for t in re.findall(r'<h[1-4][^>]*>([\s\S]*?)</h[1-4]>', p_html, re.I)]
    print(f"\n=== PAGE {page_slug} HEADINGS ===")
    for t in titles:
        print("  -", t)
