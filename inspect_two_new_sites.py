#!/usr/bin/env python3
import re
import ssl
import urllib.request

ctx = ssl.create_default_context()
for domain in ["https://doc-translate.erx.vn", "https://doc-builder.erx.vn"]:
    print("=== " + domain + " ===")
    for path in ["/", "/robots.txt", "/sitemap.xml"]:
        url = domain + path
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
                body = r.read().decode("utf-8", errors="replace")
                print(
                    f"{url} -> {r.status} ({len(body)} chars, Content-Type: {r.headers.get('Content-Type')})"
                )
                if path != "/":
                    print(body[:600])
                else:
                    for label, pat in [
                        ("title", r"<title[^>]*>.*?</title>"),
                        ("meta", r"<meta[^>]+>"),
                        ("canonical", r"<link[^>]+rel=[\"']canonical[\"'][^>]*>"),
                        ("jsonld", r"<script[^>]+application/ld\+json[^>]*>.*?</script>"),
                        ("h1", r"<h1[^>]*>.*?</h1>"),
                    ]:
                        matches = re.findall(pat, body, re.I | re.S)
                        print(f"  {label}: {len(matches)} matches -> {matches[:6]}")
        except Exception as e:
            print(f"{url} -> ERROR: {e}")
