# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open(r'D:\GIT\SEO Tool\pm_assets\sitemap_articles_audit.json', encoding='utf-8'))
targets = {"7123687467", "7123702834", "7123694822", "7123673148", "7122399614", "7122417941"}
for d in data:
    if d.get('nid') in targets:
        ft = d['ft_html']
        idx = ft.find('<div class="txtr">')
        if idx != -1:
            ft = ft[:idx]
        print("=" * 80)
        print(d['nid'], d['url'])
        print("INTRO:", repr(d['intro_text']))
        print("FT_HTML:")
        print(ft[:3500])
