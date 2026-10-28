# -*- coding: utf-8 -*-
import json
import re
import sys
import html as html_lib

sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open(r"D:\GIT\SEO Tool\pm_assets\sitemap_articles_audit.json", encoding="utf-8"))

ALLOWED_UPPER = {
    "EXCEL", "SQL", "VBA", "DAX", "BI", "AI", "ERP", "SAP", "MRP", "TCO", "ABC",
    "WBS", "CPM", "EVM", "EMV", "RACI", "PMBOK", "P2P", "SCM", "KPI", "ROI",
    "NPV", "IRR", "SLA", "HS", "API", "MRO", "YTD", "IIF", "ADO", "ADODB", "UDF",
    "HTML", "CSS", "CSV", "XML", "JSON", "PDF", "URL", "HTTP", "HTTPS", "UI", "UX",
    "IT", "HR", "PR", "PO", "GRN", "RFQ", "RFP", "BOQ", "BOM", "COGS", "JIT", "VRP",
    "EDA", "ETL", "SSAS", "OLAP", "IDE", "OS", "PC", "RAM", "CPU", "GPU", "ROM",
    "FIFO", "FEFO", "LIFO", "SWOT", "SMART", "PDCA", "OKR", "CRM", "WMS", "TMS",
    "3PL", "4PL", "B2B", "B2C", "USD", "VND", "S&OP", "FP&A", "R&D", "M&A", "Q&A",
    "3D", "2D", "TOP", "SCAN", "LAMBDA", "FILTER", "TRIM", "SUBSTITUTE", "CHAR",
    "SUM", "SUMIFS", "COUNTIFS", "VLOOKUP", "XLOOKUP", "HLOOKUP", "INDEX", "MATCH",
    "OFFSET", "CHOOSE", "CHOOSEROWS", "CHOOSECOLS", "TAKE", "DROP", "EXPAND",
    "VSTACK", "HSTACK", "TOCOL", "TOROW", "WRAPROWS", "WRAPCOLS", "TEXTSPLIT",
    "TEXTBEFORE", "TEXTAFTER", "LET", "UNIQUE", "SORT", "SORTBY", "SEQUENCE",
    "SUBTOTAL", "AGGREGATE", "EOMONTH", "GROUPBY", "HYPERLINK", "SUMPRODUCT",
    "WHERE", "GROUP", "BY", "HAVING", "ORDER", "SELECT", "FROM", "JOIN", "LEFT",
    "RIGHT", "INNER", "FULL", "UNION", "ALL", "ALLSELECTED", "INSERT", "UPDATE",
    "DELETE", "CREATE", "ALTER", "CALCULATE", "RANKX", "DIVIDE", "CALENDAR",
    "CALENDARAUTO", "VAR", "RETURN", "IF", "AND", "OR", "NOT", "IN", "LIKE",
    "BETWEEN", "IS", "NULL", "TRUE", "FALSE", "II", "III", "IV", "VI", "VII", "VIII", "IX"
}

print("=== CHECKING ALL H1/H2/H3/STRONG IN SITEMAP_ARTICLES_AUDIT.JSON FOR ALL-CAPS VIETNAMESE ===")
for d in data:
    nid = d.get("nid", "")
    ft = d.get("ft_html", "")
    idx = ft.find('<div class="txtr">')
    if idx != -1:
        ft = ft[:idx]
    for m in re.finditer(r'<(h[1-4]|strong|b)[^>]*>([\s\S]*?)</\1>', ft, re.I):
        tag, inner = m.group(1), html_lib.unescape(re.sub(r'<[^>]+>', ' ', m.group(2))).strip()
        inner = re.sub(r'\s+', ' ', inner)
        if len(inner) < 8 or inner.startswith("="):
            continue
        words = [re.sub(r'[^A-ZÀ-Ỹa-zà-ỹ0-9&-]', '', w) for w in inner.split()]
        words = [w for w in words if len(w) >= 2 and any(c.isalpha() for c in w)]
        if len(words) >= 3:
            upper_vn = [w for w in words if w.isupper() and w not in ALLOWED_UPPER]
            if len(upper_vn) >= 3 and len(upper_vn) / len(words) >= 0.5:
                print(f"  {nid} | <{tag}> {inner[:100]}")
