# -*- coding: utf-8 -*-
import json
import re
import sys
import urllib.request
import html as html_lib

sys.stdout.reconfigure(encoding='utf-8')

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")

home_html = fetch("https://erx.vn/")

# 1. Find all inline <style> blocks on homepage
print("=== INLINE STYLES ON HOMEPAGE ===")
for i, m in enumerate(re.finditer(r'<style[^>]*>([\s\S]*?)</style>', home_html, re.I)):
    st = m.group(1).strip()
    if "img-block" in st or "109690" in st or "uppercase" in st or "list-block" in st:
        print(f"--- Style #{i} ---")
        print(st[:2500])

# 2. Find all footer module IDs
print("\n=== ALL MODULE DIVS ON HOMEPAGE ===")
for m in re.finditer(r'<div class="([^"]*modid-\d+[^"]*)"', home_html):
    print(" ", m.group(1))

# 3. Check all workshop links and IDs on /hoi-thao.html (page 1 & 2)
hoithao_html = fetch("https://erx.vn/hoi-thao.html")
print("\n=== WORKSHOP ITEMS ON /hoi-thao.html ===")
for m in re.finditer(r'href="([^"]*-(\d{10})\.html)"[^>]*>\s*<h3[^>]*>([\s\S]*?)</h3>', hoithao_html, re.I):
    url, nid, title = m.group(1), m.group(2), html_lib.unescape(re.sub(r'<[^>]+>', '', m.group(3))).strip()
    print(f"  {nid} | {title} | {url}")

# Also check how /hoi-thao.html renders items
idx_ht = hoithao_html.find("list-block")
if idx_ht != -1:
    print("\n=== SAMPLE HOI THAO ITEM HTML ===")
    print(hoithao_html[max(0, idx_ht-200):idx_ht+1500])

# 4. Check all 107 legacy blog titles from sitemap_articles_audit.json for uppercase words
data = json.load(open(r"D:\GIT\SEO Tool\pm_assets\sitemap_articles_audit.json", encoding="utf-8"))
print("\n=== BLOG ARTICLES WITH UPPERCASE PHRASES IN TITLE ===")
for d in data:
    t = d.get("title", "")
    # Remove " - ERX.VN" or similar suffix
    # Check if there are Vietnamese uppercase words of length >= 2 that are not standard acronyms
    words = t.split()
    upper_words = [w for w in words if len(w) >= 2 and w.isupper() and not re.match(r'^(EXCEL|SQL|VBA|DAX|BI|AI|ERP|SAP|MRP|TCO|ABC|WBS|CPM|EVM|EMV|RACI|PMBOK|P2P|SCM|KPI|ROI|NPV|IRR|SLA|HS|API|MRO|YTD|IIF|ADO|ADODB|UDF|HTML|CSS|CSV|XML|JSON|PDF|URL|HTTP|HTTPS|UI|UX|IT|HR|PR|PO|GRN|RFQ|RFP|BOQ|BOM|COGS|JIT|VRP|EDA|ETL|SSAS|OLAP|IDE|OS|PC|RAM|CPU|GPU|ROM|LAN|WAN|WIFI|QR|BARCODE|FIFO|FEFO|LIFO|SWOT|SMART|PDCA|OKR|CRM|WMS|TMS|OMS|IMS|APS|MES|PLM|SRM|VMI|3PL|4PL|B2B|B2C|C2C|G2B|USD|VND|EUR|JPY|CNY|GBP|S&OP|FP&A|R&D|M&A|Q&A|P&L|A-Z|0-9|3D|2D|1-CLICK|TOP|N|SCAN|LAMBDA|FILTER|TRIM|SUBSTITUTE|CHAR|SUM|SUMIFS|COUNTIFS|VLOOKUP|XLOOKUP|HLOOKUP|INDEX|MATCH|OFFSET|CHOOSE|CHOOSEROWS|CHOOSECOLS|TAKE|DROP|EXPAND|VSTACK|HSTACK|TOCOL|TOROW|WRAPROWS|WRAPCOLS|TEXTSPLIT|TEXTBEFORE|TEXTAFTER|LET|UNIQUE|SORT|SORTBY|SEQUENCE|SUBTOTAL|AGGREGATE|EOMONTH|GROUPBY|HYPERLINK|SUMPRODUCT|MERGE|CELLS|TABLE|SEARCH|BOX|CHECK|PARETO|CHART|PIVOT|WILDCARDS|WHERE|GROUP|BY|HAVING|ORDER|SELECT|FROM|JOIN|LEFT|RIGHT|INNER|FULL|UNION|ALL|ALLSELECTED|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|CALCULATE|RANKX|DIVIDE|CALENDAR|CALENDARAUTO|VAR|RETURN|IF|AND|OR|NOT|IN|LIKE|BETWEEN|IS|NULL|TRUE|FALSE)$', re.sub(r'[^A-ZÀ-Ỹ0-9&-]', '', w))]
    if upper_words:
        print(f"  {d.get('nid')} | {t} | upper={upper_words}")
