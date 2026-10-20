#!/usr/bin/env python3
"""Server locale che imita GitHub Pages: /servizi -> servizi.html, / -> index.html, pagine mancanti -> 404.html.
Uso: python3 anteprima.py 4231 [cartella]"""
import http.server, os, sys
porta = int(sys.argv[1]) if len(sys.argv) > 1 else 4231
if len(sys.argv) > 2: os.chdir(sys.argv[2])
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = super().translate_path(path.split("?")[0].split("#")[0])
        if not os.path.exists(p) and os.path.exists(p + ".html"): return p + ".html"
        return p
    def send_error(self, code, message=None, explain=None):
        if code == 404 and os.path.exists("404.html"):
            corpo = open("404.html", "rb").read()
            self.send_response(404); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo))); self.end_headers(); self.wfile.write(corpo); return
        super().send_error(code, message, explain)
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", porta), H).serve_forever()
