import urllib.request
import re
import json

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.getcode(), resp.read().decode('utf-8', 'ignore')

_, home_html = fetch('https://erx.vn/')
nav_links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', home_html, re.S)
print("=== NAVBAR LINKS ON HOMEPAGE ===")
seen_nav = set()
for href, txt in nav_links:
    clean_txt = re.sub(r'<[^>]+>', '', txt).strip()
    if ('erx.vn' in href or href.startswith('/')) and href not in seen_nav and len(seen_nav) < 35:
        seen_nav.add(href)
        print(f"  {clean_txt:35s} -> {href}")

print("\n=== CHECK WORKSHOP DETAIL PAGES (/hoi-thao.html) ===")
_, ht_html = fetch('https://erx.vn/hoi-thao.html')
ws_links = []
for m in re.finditer(r'<a[^>]+href=["\'](https://erx\.vn/[^"\']+-831\d+\.html)["\']', ht_html):
    u = m.group(1)
    if u not in ws_links:
        ws_links.append(u)

print(f"Found {len(ws_links)} Workshop detail URLs on /hoi-thao.html")
for u in ws_links[:6]:
    _, whtml = fetch(u)
    t = re.findall(r'<title>(.*?)</title>', whtml, re.S)
    t = t[0].strip() if t else ''
    d = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', whtml, re.I)
    d = d[0].strip() if d else ''
    h1s = [re.sub(r'<[^>]+>', '', h).strip() for h in re.findall(r'<h1[^>]*>(.*?)</h1>', whtml, re.I | re.S)]
    print(f"  {u.split('/')[-1]}:")
    print(f"    Title: {t}")
    print(f"    Desc : {d[:100]}")
    print(f"    H1s  : {h1s}")

print("\n=== CHECK SITEMAP.XML CONTENTS ===")
_, sm_xml = fetch('https://erx.vn/sitemap.xml')
sm_urls = re.findall(r'<loc>(.*?)</loc>', sm_xml)
print(f"Total URLs in /sitemap.xml: {len(sm_urls)}")
articles_in_sm = [u for u in sm_urls if re.search(r'-712\d+\.html$', u)]
workshops_in_sm = [u for u in sm_urls if re.search(r'-831\d+\.html$', u)]
others_in_sm = [u for u in sm_urls if u not in articles_in_sm and u not in workshops_in_sm]
print(f"  Articles (712*) in /sitemap.xml: {len(articles_in_sm)}")
print(f"  Workshops (831*) in /sitemap.xml: {len(workshops_in_sm)}")
print(f"  Other pages in /sitemap.xml ({len(others_in_sm)}): {others_in_sm}")

print("\n=== CHECK SAMPLE BLOG ARTICLES (LEGACY & PM) META, H1, SCHEMA ===")
sample_articles = [
    'https://erx.vn/quan-tri-du-an-theo-chuan-pmbok-8-tong-quan-nguyen-tac-va-quy-trinh-7124047589.html',
    'https://erx.vn/expand-excel-365-erx-vietnam-7123806948.html',
    'https://erx.vn/layout-theo-quy-tac-abc-trong-cau-hinh-he-thong-kho-hang-7124011913.html',
    'https://erx.vn/loai-bo-cac-dau-cach-thua-so-32-va-so-160-trong-excel-7122246032.html',
]
for u in sample_articles:
    _, ahtml = fetch(u)
    t = re.findall(r'<title>(.*?)</title>', ahtml, re.S)
    t = t[0].strip() if t else ''
    d = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', ahtml, re.I)
    d = d[0].strip() if d else ''
    h1s = [re.sub(r'<[^>]+>', '', h).strip() for h in re.findall(r'<h1[^>]*>(.*?)</h1>', ahtml, re.I | re.S)]
    ld = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', ahtml, re.I | re.S)
    print(f"  {u.split('/')[-1]}:")
    print(f"    Title ({len(t)}c): {t}")
    print(f"    Desc  ({len(d)}c): {d[:110]}")
    print(f"    H1s: {h1s} | JSON-LD blocks: {len(ld)}")
