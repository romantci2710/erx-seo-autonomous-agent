# -*- coding: utf-8 -*-
import json
import re
import sys
import html as html_lib

sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open(r'D:\GIT\SEO Tool\pm_assets\sitemap_articles_audit.json', encoding='utf-8'))

pm_ids = {
    "7124047589", "7124054453", "7124068075", "7124079199",
    "7124088613", "7124095185", "7124108707", "7124156882"
}

legacy = {}
for d in data:
    nid = d.get('nid', '')
    if not nid.startswith('712') or nid in pm_ids:
        continue
    ft = d['ft_html']
    idx = ft.find('<div class="txtr">')
    if idx != -1:
        ft = ft[:idx]
    ft_no_style = re.sub(r'<style[^>]*>.*?</style>', '', ft, flags=re.S | re.I)
    clean_txt = html_lib.unescape(re.sub(r'<[^>]+>', ' ', ft_no_style))
    clean_txt = re.sub(r'\s+', ' ', clean_txt).strip()
    d['clean_txt'] = clean_txt
    d['clean_len'] = len(clean_txt)
    legacy[nid] = d

print(f"Total unique legacy 712* articles: {len(legacy)}")
for nid, d in sorted(legacy.items(), key=lambda x: x[1]['clean_len']):
    slug = d['url'].split('/')[-1]
    print(f"{nid} | clean_len={d['clean_len']:5d} | intro_len={d['intro_len']:4d} | {slug}")
    print(f"   INTRO: {d['intro_text'][:140]!r}")
    print(f"   BODY : {d['clean_txt'][:200]!r}")
