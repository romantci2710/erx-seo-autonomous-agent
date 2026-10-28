# -*- coding: utf-8 -*-
"""
Local CORS + Private-Network HTTP server on 127.0.0.1:8765
Serves /bundle.json containing the 4 Pillar Articles + 12 images (WebP & JPG base64)
so the browser agent on https://erx.vn/administrator can upload all 12 images via CKFinder
and publish all 4 Pillar Articles in 1 shot.
"""
import os
import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler

ASSET_DIR = r"D:\GIT\SEO Tool\pm_assets"

def build_bundle():
    with open(os.path.join(ASSET_DIR, "pillar_articles_clean.json"), "r", encoding="utf-8") as f:
        articles = json.load(f)
    images_b64 = {}
    for art in articles:
        for img_info in art["images"]:
            fname = img_info["file"]
            fpath = os.path.join(ASSET_DIR, fname)
            with open(fpath, "rb") as imgf:
                images_b64[fname] = base64.b64encode(imgf.read()).decode("ascii")
            img_info["upload_name"] = fname.replace(".jpg", "_light.jpg")
    return json.dumps({"articles": articles, "images": images_b64}, ensure_ascii=False).encode("utf-8")

BUNDLE_BYTES = build_bundle()

class Handler(BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/bundle.json"):
            self.send_response(200)
            self._send_cors()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(BUNDLE_BYTES)))
            self.end_headers()
            self.wfile.write(BUNDLE_BYTES)
        else:
            self.send_response(200)
            self._send_cors()
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    print(f"Serving bundle ({len(BUNDLE_BYTES)/1024:.1f} KB) on http://127.0.0.1:8765/bundle.json")
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
