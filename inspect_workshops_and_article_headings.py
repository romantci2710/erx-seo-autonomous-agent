# -*- coding: utf-8 -*-
import json
import re
import sys
import urllib.request
import html as html_lib
from PIL import Image
import io

sys.stdout.reconfigure(encoding='utf-8')

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")

# 1. Inspect all workshop items on /hoi-thao.html
ht = fetch("https://erx.vn/hoi-thao.html")
ht_body = ht[ht.find("<body"):]
print("=== ALL WORKSHOP ITEMS ON /hoi-thao.html ===")
for m in re.finditer(r'<h3 class="title">\s*<a href="([^"]*-(\d+)\.html)">([\s\S]*?)</a>\s*</h3>', ht_body, re.I):
    url, wid, title = m.group(1), m.group(2), html_lib.unescape(re.sub(r'<[^>]+>', '', m.group(3))).strip()
    print(f"  {wid} | {title} | {url}")

# Check if there are more workshop items loaded via AJAX or page 2
print("\n=== CHECKING HOMEPAGE THUMBNAILS IN modid-109690 ===")
home = fetch("https://erx.vn/")
home_mod = home[home.find("devide_mod_109690"):home.find("slide_owncousor_40569")]
for m in re.finditer(r'<a href="([^"]*-(\d+)\.html)"[^>]*class="img-block-0"[^>]*>\s*<img[^>]*src="([^"]+)"', home_mod, re.I):
    url, nid, img_src = m.group(1), m.group(2), m.group(3)
    try:
        encoded_src = urllib.parse.quote(img_src, safe=":/?=&[]()")
        req = urllib.request.Request(encoded_src, headers={"User-Agent": "Mozilla/5.0"})
        raw_img = urllib.request.urlopen(req, timeout=15).read()
        im = Image.open(io.BytesIO(raw_img))
        print(f"  {nid} | {im.size[0]:4d}x{im.size[1]:4d} (ratio={im.size[0]/im.size[1]:.2f}) | {img_src}")
    except Exception as e:
        print(f"  {nid} | ERROR {e} | {img_src}")
