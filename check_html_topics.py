import re
import urllib.request
import xml.etree.ElementTree as ET

sitemap_xml = urllib.request.urlopen("https://community.erx.vn/sitemap.xml", timeout=15).read().decode("utf-8")
locs = [el.text.strip() for el in ET.fromstring(sitemap_xml).iter() if el.tag.endswith("loc") and "/forum/chu-de/" in (el.text or "")]

print(f"Total topic URLs in sitemap: {len(locs)}")
html_topics = []
for u in locs:
    page = urllib.request.urlopen(u, timeout=15).read().decode("utf-8", errors="ignore")
    att_links = re.findall(r'href=["\'](/api/community/attachments/\d+[^"\']*)["\'][^>]*>(.*?)</a>', page, flags=re.I | re.S)
    body_m = re.search(r'<article>(.*?)</article>', page, flags=re.I | re.S)
    body_txt = re.sub(r"<[^>]+>", " ", body_m.group(1)).strip() if body_m else ""
    body_txt = re.sub(r"\s+", " ", body_txt)
    if att_links or ".html" in page:
        html_topics.append((u, len(body_txt), att_links))

print(f"Topics with attachment links: {len(html_topics)}")
for u, blen, links in html_topics:
    print(f"  - {u} (body text len: {blen}): {links}")
