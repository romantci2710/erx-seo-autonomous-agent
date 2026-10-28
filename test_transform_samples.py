# -*- coding: utf-8 -*-
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open(r'D:\GIT\SEO Tool\pm_assets\sitemap_articles_audit.json', encoding='utf-8'))

for nid in ["7123687467", "7123702834", "7123694822", "7123673148"]:
    for d in data:
        if d.get("nid") == nid:
            ft = d["ft_html"]
            idx = ft.find('<div class="txtr">')
            if idx != -1:
                ft = ft[:idx]
            ft_short = re.sub(r'data:image/[^"]+', 'DATA_IMG', ft)
            print("=" * 80)
            print(nid, d["url"])
            print(ft_short)
            break
