# -*- coding: utf-8 -*-
import json
import re
import sys
import html as html_lib

sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open(r'D:\GIT\SEO Tool\pm_assets\sitemap_articles_audit.json', encoding='utf-8'))

# Exclude the new PM articles (7124047589+) and non-712* items
pm_ids = {
    "7124047589", "7124054453", "7124068075", "7124079199",
    "7124088613", "7124095185", "7124108707", "7124156882"
}

legacy = {}
for d in data:
    nid = d.get('nid', '')
    if not nid.startswith('712') or nid in pm_ids:
        continue
    # Extract title from URL slug or ft_html if h1 was missed
    url = d['url']
    slug = url.split('/')[-1].rsplit('-', 1)[0]
    legacy[nid] = d

print(f"Total unique legacy 712* articles to inspect: {len(legacy)}")
for nid, d in sorted(legacy.items(), key=lambda x: int(x[0])):
    slug = d['url'].split('/')[-1]
    print(f"{nid} | intro={d['intro_len']:4d} | ft={d['ft_text_len']:6d} | h2={d['h2']:2d} | f={d['raw_formulas']:2d} | {slug}")
    if d['intro_len'] < 160 or d['intro_len'] > 500:
        print(f"   [INTRO FIX NEEDED] cur_intro={d['intro_text'][:100]!r} | desc={d['desc'][:100]!r}")
