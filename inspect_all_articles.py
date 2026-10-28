# -*- coding: utf-8 -*-
import urllib.request
import re
import json
import sys
import html as html_lib
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')

xml = urllib.request.urlopen('https://erx.vn/sitemap.xml').read().decode('utf-8', 'ignore')
urls = re.findall(r'<loc>(https://erx\.vn/[^<]+-\d+\.html)</loc>', xml)

# Also crawl all 19 category listing pages to make sure we don't miss any article not yet in sitemap.xml
cat_pages = [
    "https://erx.vn/kien-thuc.html",
    "https://erx.vn/excel-functions.html",
    "https://erx.vn/cac-ham-excel-365.html",
    "https://erx.vn/excel-vba.html",
    "https://erx.vn/sql.html",
    "https://erx.vn/power-bi.html",
    "https://erx.vn/dashboard-automated-report.html",
    "https://erx.vn/python-for-supply-chain.html",
    "https://erx.vn/supply-chain-management.html",
    "https://erx.vn/procurement-management.html",
    "https://erx.vn/planning-management.html",
    "https://erx.vn/inventory-management.html",
    "https://erx.vn/logistics-management.html",
    "https://erx.vn/mau-file-quan-ly-excel.html",
    "https://erx.vn/project-management.html",
    "https://erx.vn/cau-chuyen-thanh-cong.html",
    "https://erx.vn/su-kien.html",
]

for cp in cat_pages:
    try:
        chtml = urllib.request.urlopen(cp, timeout=10).read().decode('utf-8', 'ignore')
        found = re.findall(r'href=["\'](https://erx\.vn/[^"\']+-\d+\.html|/[^"\']+-\d+\.html)["\']', chtml)
        for f in found:
            full = f if f.startswith('http') else 'https://erx.vn' + f
            if full not in urls:
                urls.append(full)
    except Exception:
        pass

print(f"Total unique article URLs discovered: {len(urls)}")

def fetch_info(u):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        raw = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
        m_id = re.search(r'-(\d+)\.html$', u)
        nid = m_id.group(1) if m_id else ''
        is_article = 'ct-article-detail' in raw
        m_h1 = re.search(r'<div class="title-content">\s*<h1>(.*?)</h1>', raw, re.S | re.I)
        h1 = html_lib.unescape(re.sub(r'<[^>]+>', '', m_h1.group(1)).strip()) if m_h1 else ''
        m_bc = re.findall(r'<ul class="breadcrumb">.*?</ul>', raw, re.S | re.I)
        bc_text = ""
        if m_bc:
            bc_links = re.findall(r'<a[^>]*>(.*?)</a>', m_bc[0], re.S | re.I)
            bc_text = " > ".join(html_lib.unescape(re.sub(r'<[^>]+>', '', x).strip()) for x in bc_links)
        m_intro = re.search(r'<h2 class="div-intro-content">(.*?)</h2>', raw, re.S | re.I)
        intro_html = m_intro.group(1).strip() if m_intro else ''
        intro_text = html_lib.unescape(re.sub(r'<[^>]+>', ' ', intro_html))
        intro_text = re.sub(r'\s+', ' ', intro_text).strip()
        m_desc = re.search(r'<meta name="description" content="([^"]*)"', raw, re.I)
        desc = html_lib.unescape(m_desc.group(1).strip()) if m_desc else ''
        m_ft = re.search(r'<div class="full-text">(.*?)</div>\s*<div class="author-content">', raw, re.S | re.I)
        ft_html = m_ft.group(1).strip() if m_ft else ''
        ft_text = html_lib.unescape(re.sub(r'<[^>]+>', ' ', ft_html))
        ft_text = re.sub(r'\s+', ' ', ft_text).strip()
        h2_cnt = len(re.findall(r'<h2\b', ft_html, re.I))
        h3_cnt = len(re.findall(r'<h3\b', ft_html, re.I))
        code_cnt = len(re.findall(r'<(?:code|pre)\b', ft_html, re.I))
        raw_formulas = len(re.findall(r'(?:^|>|\s)=[A-Z]{2,}[A-Z0-9_.]*\s*\(', ft_html))
        return {
            'url': u,
            'nid': nid,
            'is_article': is_article,
            'breadcrumb': bc_text,
            'h1': h1,
            'intro_len': len(intro_text),
            'intro_text': intro_text,
            'intro_html': intro_html,
            'desc': desc,
            'ft_text_len': len(ft_text),
            'ft_html': ft_html,
            'h2': h2_cnt,
            'h3': h3_cnt,
            'code': code_cnt,
            'raw_formulas': raw_formulas
        }
    except Exception as e:
        return {'url': u, 'error': str(e)}

with ThreadPoolExecutor(max_workers=12) as ex:
    res = list(ex.map(fetch_info, urls))

articles = [r for r in res if r.get('is_article')]
print(f"Total crawled: {len(res)}, Blog articles (ct-article-detail): {len(articles)}")
empty_intro = [a for a in articles if a['intro_len'] < 50]
no_h2 = [a for a in articles if a['h2'] == 0]
has_raw_formula = [a for a in articles if a['raw_formulas'] > 0 and a['code'] == 0]
short_ft = [a for a in articles if a['ft_text_len'] < 1500]
print(f"Empty/short intro (<50 chars): {len(empty_intro)}")
print(f"No H2 headings in body: {len(no_h2)}")
print(f"Has raw Excel formulas without <code>/<pre>: {len(has_raw_formula)}")
print(f"Short body text (<1500 chars): {len(short_ft)}")

out_path = r'D:\GIT\SEO Tool\pm_assets\sitemap_articles_audit.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("Saved full audit to", out_path)
