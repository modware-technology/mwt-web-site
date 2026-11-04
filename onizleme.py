"""Yerel önizleme sunucusu: Cloudflare Pages gibi temiz adresleri açar.

/hizmetler → hizmetler.html, /blog/ → blog/index.html; bulunamayan adreste en yakın üst klasördeki
404.html (404 durumuyla): /en/olmayan → en/404.html, /olmayan → 404.html.
Kullanım: python onizleme.py <site-klasörü> [port]   (varsayılan port 8765)
"""
import functools
import http.server
import os
import sys

KOK = os.path.abspath(sys.argv[1])
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8765


def en_yakin_404(yol):
    parcalar = [p for p in yol.split("/")[:-1] if p not in ("", ".", "..")]
    while parcalar and not os.path.isfile(os.path.join(KOK, *parcalar, "404.html")):
        parcalar.pop()
    return os.path.join(KOK, *parcalar, "404.html")


class Isleyici(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        yol, ayir, sorgu = self.path.partition("?")
        yol = yol.split("#", 1)[0]
        tam = self.translate_path(yol)
        if not os.path.exists(tam) and os.path.isfile(tam + ".html"):
            self.path = yol + ".html" + (ayir + sorgu)
        elif not os.path.exists(tam):
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            veri = open(en_yakin_404(yol), "rb").read()
            self.send_header("Content-Length", str(len(veri)))
            self.end_headers()
            self.wfile.write(veri)
            return None
        return super().send_head()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"http://127.0.0.1:{PORT}/  ({KOK})")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), functools.partial(Isleyici, directory=KOK)).serve_forever()
