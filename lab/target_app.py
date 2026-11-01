#!/usr/bin/env python3
"""mythos-lab — the self-owned vulnerable-by-design target for the worked
engagement (and for trying the arsenal safely).

Run:    python3 lab/target_app.py [port]
Everything it serves is synthetic. The AUTH story is a self-owned lab
declaration: it IS the authorizing artifact recorded in scope.csv.
"""
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

JS = b"""// mythos-lab bundle
const API_KEY = "MYTHOS-CANARY-lab-013";
// routes served by the console:
//   /api/v0/debug  (retired but still mounted, ops banner)
async function loadMetrics() {
  return fetch('/api/v2/admin/metrics', {headers: {'X-Session': API_KEY}});
}
async function listUsers()   { return fetch('/api/v1/users'); }
async function getInvoice() { return fetch('/api/v1/invoices?ref=LAB-0001'); }
"""

OPENAPI = {
    "openapi": "3.0.0",
    "info": {"title": "mythos-lab API", "version": "2.0.0"},
    "paths": {
        "/api/v1/users": {"get": {"summary": "public user list",
                                  "responses": {"200": {}}}},
        "/api/v1/invoices": {"get": {"summary": "invoice lookup",
                                     "responses": {"200": {}}}},
        "/api/v2/admin/metrics": {"get": {"summary": "console metrics",
                                          "security": [{"sessionKey": []}],
                                          "responses": {"401": {}}}},
        "/api/v2/admin/export": {"get": {"summary": "console export",
                                         "security": [{"sessionKey": []}],
                                         "responses": {"401": {}}}},
    },
}

HTML = b"""<!doctype html>
<html><head><title>mythos-lab</title><script src="/app.js"></script></head>
<body><h1>mythos-lab</h1>
<!-- admin console coming soon -->
<a href="/about">About</a> <a href="/pricing">Pricing</a>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "mythos-lab/1.0"

    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        route = {
            "/": (200, HTML, "text/html"),
            "/app.js": (200, JS, "application/javascript"),
            "/robots.txt": (200, b"User-agent: *\nDisallow: /admin\n"
                                 b"Disallow: /backup\n", "text/plain"),
            "/sitemap.xml": (200, b"<?xml version=\"1.0\"?>"
                                   b"<urlset><url><loc>/</loc></url>"
                                   b"<url><loc>/about</loc></url>"
                                   b"<url><loc>/pricing</loc></url>"
                                   b"</urlset>", "application/xml"),
            "/about": (200, b"<html><body>about mythos-lab</body></html>",
                       "text/html"),
            "/pricing": (200, b"<html><body>pricing</body></html>",
                         "text/html"),
            "/admin": (307, b"", "text/html"),
            "/login": (200, b"<html><body>login</body></html>", "text/html"),
            "/backup.zip": (200, b"PK-lab-archive-synthetic", "application/zip"),
            "/.env.example": (200, b"LAB_MODE=1\nLAB_SECRET=", "text/plain"),
            "/antique-page": (200, b"<html><body>Page not found</body>"
                                   b"</html>", "text/html"),
            "/api/v0/debug": (200, b'{"debug": true, "banner": "mythos-lab '
                                   b'debug console", "lab_only": true}',
                              "application/json"),
            "/api/v1/users": (200, b'[{"id": 1, "name": "lab-user-a"},'
                                   b'{"id": 2, "name": "lab-user-b"}]',
                              "application/json"),
        }.get(self.path)
        if route is None and self.path == "/openapi.json":
            return self._send(200, json.dumps(OPENAPI, indent=1).encode(),
                              "application/json")
        if route is None and self.path == "/api/v2/admin/metrics":
            if self.headers.get("X-Session") == "MYTHOS-CANARY-lab-013":
                return self._send(200, b'{"uptime": 42}', "application/json")
            return self._send(401, b'{"error": "session required"}',
                              "application/json")
        if route is None:
            body = b'{"error": "not found", "path": "' + \
                self.path.encode() + b'"}'
            return self._send(404, body, "application/json")
        code, body, ctype = route
        if code == 307:
            self.send_response(307)
            self.send_header("Location", "/login")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self._send(code, body, ctype)

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        self.rfile.read(length)
        self._send(404, b'{"error": "not found"}', "application/json")

    def log_message(self, fmt, *args):  # quiet
        pass


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8477
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("mythos-lab listening on 127.0.0.1:%d (self-owned synthetic "
          "target)" % port)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
