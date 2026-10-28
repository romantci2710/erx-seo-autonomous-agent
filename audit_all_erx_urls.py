import urllib.request
import re
import json

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.getcode(), resp.read().decode('utf-8', 'ignore')

extra_menus = [
    'https://erx.vn/excel-function.html',
    'https://erx.vn/excel-365.html',
    'https://erx.vn/cuoc-thi-supply-chain-data-analysis-challenge.html',
    'https://erx.vn/lien-he0.html',
    'https://erx.vn/gioi-thieu.html',
    'https://erx.vn/tro-thanh-giang-vien-cung-erx.html',
    'https://erx.vn/thong-tin-tuyen-sinh.html',
    'https://erx.vn/tin-quan-trong.html',
]

print("=== EXTRA MENU PAGES ===")
for u in extra_menus:
    try:
        code, html = fetch(u)
        t = re.findall(r'<title>(.*?)</title>', html, re.S)
        t = t[0].strip() if t else ''
        d = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
        d = d[0].strip() if d else ''
        h1s = [re.sub(r'<[^>]+>', '', h).strip() for h in re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)]
        print(f"- {u.replace('https://erx.vn', '')}: Title({len(t)}c)='{t}' | Desc({len(d)}c)='{d[:80]}' | H1s={h1s}")
    except Exception as e:
        print(f"- {u}: ERROR {e}")

print("\n=== CHECK JSON-LD ON HOMEPAGE, CATEGORY, ARTICLE, WORKSHOP ===")
for label, u in [
    ('Homepage', 'https://erx.vn/'),
    ('Category PM', 'https://erx.vn/project-management.html'),
    ('Article PM', 'https://erx.vn/quan-tri-du-an-theo-chuan-pmbok-8-tong-quan-nguyen-tac-va-quy-trinh-7124047589.html'),
    ('Article Legacy', 'https://erx.vn/expand-excel-365-erx-vietnam-7123806948.html'),
    ('Workshop', 'https://erx.vn/tai-sao-and-or-khong-spill-4-giai-phap-thay-the-trong-excel-moi-8315644.html'),
]:
    _, html = fetch(u)
    lds = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.I | re.S)
    print(f"  {label} ({u}): {len(lds)} JSON-LD block(s)")
    for i, b in enumerate(lds):
        clean_b = re.sub(r'\s+', ' ', b).strip()
        print(f"    [{i}] {clean_b[:220]}...")

print("\n=== CHECK ALL 107 LEGACY ARTICLES IN erx_all_107_articles_raw.json FOR SEO METRICS ===")
with open(r'D:\GIT\SEO Tool\erx_all_107_articles_raw.json', 'r', encoding='utf-8') as f:
    arts = json.load(f)

short_titles = []
long_titles = []
short_meta_titles = []
missing_meta_keys = []
for a in arts:
    nid = a.get('nid')
    title = (a.get('title') or '').strip()
    mtitle = (a.get('metaTitle') or '').strip()
    mdesc = (a.get('metaDesc') or '').strip()
    mkey = (a.get('metaKey') or '').strip()
    eff_title = mtitle if mtitle else title
    if len(eff_title) < 35:
        short_titles.append((nid, eff_title, title))
    elif len(eff_title) > 75:
        long_titles.append((nid, eff_title, title))
    if not mkey:
        missing_meta_keys.append(nid)

print(f"Articles with effective <title> < 35 chars: {len(short_titles)}")
for x in short_titles[:15]:
    print("  SHORT:", x)
print(f"Articles with effective <title> > 75 chars: {len(long_titles)}")
for x in long_titles[:10]:
    print("  LONG :", x)
print(f"Articles with empty META_KEY: {len(missing_meta_keys)}")
