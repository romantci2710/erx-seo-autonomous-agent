import urllib.request
import re
import json
from concurrent.futures import ThreadPoolExecutor

with open(r'D:\GIT\SEO Tool\pm_assets\sitemap_articles_audit.json', encoding='utf-8') as f:
    data = json.load(f)

urls = []
for d in data:
    u = d.get('url', '')
    if re.search(r'-712\d+\.html$', u) and u not in urls:
        urls.append(u)

# Also add all 8 cluster PM articles if not in audit
pm_html = urllib.request.urlopen('https://erx.vn/project-management.html').read().decode('utf-8', 'ignore')
for m in re.finditer(r'href=["\'](https://erx\.vn/[^"\']+-712\d+\.html|/[^"\']+-712\d+\.html)["\']', pm_html):
    u = m.group(1) if m.group(1).startswith('http') else 'https://erx.vn' + m.group(1)
    if u not in urls:
        urls.append(u)

print(f"Total 712* blog article URLs: {len(urls)}")

def check_url(u):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        raw = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
        nid = re.search(r'-(\d+)\.html$', u).group(1)
        t = re.findall(r'<title>(.*?)</title>', raw, re.S)
        t = t[0].strip() if t else ''
        d = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', raw, re.I)
        d = d[0].strip() if d else ''
        return {'nid': nid, 'url': u, 'title': t, 'tlen': len(t), 'desc': d, 'dlen': len(d)}
    except Exception as e:
        return {'nid': '', 'url': u, 'error': str(e)}

with ThreadPoolExecutor(max_workers=16) as ex:
    results = list(ex.map(check_url, urls))

errors = [r for r in results if 'error' in r]
valid = [r for r in results if 'error' not in r]
short_t = [r for r in valid if r['tlen'] < 45]
bad_d = [r for r in valid if r['dlen'] < 100]

print(f"Valid: {len(valid)}, Errors: {len(errors)}")
print(f"Articles with <title> < 45 chars: {len(short_t)}")
for r in sorted(short_t, key=lambda x: x['tlen']):
    print(f"  {r['nid']} ({r['tlen']:2d}c): {r['title']}  |  {r['url'].split('/')[-1]}")
print(f"Articles with <meta description> < 100 chars: {len(bad_d)}")
for r in bad_d:
    print(f"  {r['nid']} ({r['dlen']:2d}c): {r['desc']}")

with open(r'D:\GIT\SEO Tool\pm_assets\live_119_articles_seo.json', 'w', encoding='utf-8') as f:
    json.dump({'valid': valid, 'errors': errors, 'all_urls': [r['url'] for r in valid]}, f, ensure_ascii=False, indent=2)
