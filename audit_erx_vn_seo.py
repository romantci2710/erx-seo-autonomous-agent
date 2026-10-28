import urllib.request
import urllib.parse
import re
import json
import xml.etree.ElementTree as ET

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.getcode(), resp.read().decode('utf-8', 'ignore'), dict(resp.info())

print("=== 1. CHECK SITEMAP.XML & ROBOTS.TXT ===")
for path in ['/robots.txt', '/sitemap.xml', '/Media/files/sitemap-project-management.txt', '/Media/files/sitemap-erx-all.txt']:
    try:
        code, body, hdrs = fetch('https://erx.vn' + path)
        print(f"{path}: HTTP {code}, len={len(body)}, content-type={hdrs.get('Content-Type')}")
        if path == '/robots.txt':
            print("robots.txt:\n" + body[:600])
        elif path == '/sitemap.xml':
            urls = re.findall(r'<loc>(.*?)</loc>', body)
            print(f"sitemap.xml URL count: {len(urls)}")
            pm_urls = [u for u in urls if '71240475' in u or 'project-management' in u]
            print(f"sitemap.xml PM URLs: {len(pm_urls)} -> {pm_urls[:5]}")
            bad_urls = [u for u in urls if '#.html' in u or 'http://' in u]
            print(f"sitemap.xml bad URLs: {bad_urls[:10]}")
    except Exception as e:
        print(f"{path}: ERROR {e}")

print("\n=== 2. CHECK KEY CATEGORY / MENU PAGES META, H1, CANONICAL, SCHEMA ===")
key_pages = [
    'https://erx.vn/',
    'https://erx.vn/dao-tao-doanh-nghiep.html',
    'https://erx.vn/hoi-thao.html',
    'https://erx.vn/kien-thuc.html',
    'https://erx.vn/mau-file-quan-ly-excel.html',
    'https://erx.vn/excel-functions.html',
    'https://erx.vn/excel-vba.html',
    'https://erx.vn/dashboard-automated-report.html',
    'https://erx.vn/sql-in-excel.html',
    'https://erx.vn/cac-ham-excel-365.html',
    'https://erx.vn/power-bi.html',
    'https://erx.vn/supply-chain-management.html',
    'https://erx.vn/logistics-management.html',
    'https://erx.vn/procurement-management.html',
    'https://erx.vn/planning-management.html',
    'https://erx.vn/warehouse-management.html',
    'https://erx.vn/python-for-supply-chain.html',
    'https://erx.vn/project-management.html',
    'https://erx.vn/phan-mem.html',
    'https://erx.vn/hop-tac-viec-lam.html',
    'https://erx.vn/lien-he.html',
]

for url in key_pages:
    try:
        code, html, _ = fetch(url)
        title = re.findall(r'<title>(.*?)</title>', html, re.S)
        title = title[0].strip() if title else ''
        desc = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
        desc = desc[0].strip() if desc else ''
        canon = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.I)
        canon = canon[0].strip() if canon else ''
        h1s = [re.sub(r'<[^>]+>', '', h).strip() for h in re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)]
        ld_json = len(re.findall(r'application/ld\+json', html, re.I))
        print(f"- {url.replace('https://erx.vn', '') or '/'}:")
        print(f"    Title ({len(title)}c): {title}")
        print(f"    Desc  ({len(desc)}c): {desc[:100]}{'...' if len(desc)>100 else ''}")
        print(f"    Canon: {canon} | H1s: {h1s} | JSON-LD count: {ld_json}")
    except Exception as e:
        print(f"- {url}: ERROR {e}")
