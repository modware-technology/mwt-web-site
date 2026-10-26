import os, re, sys, json, html
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote, parse_qs
site = sys.argv[1]
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","source","track","wbr","path","circle","rect","polyline","line"}
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.st = []; s.err = []; s.ids = []; s.refs = []; s.meta = {}; s.title = ""; s.intitle = False; s.ld = []; s.inld = False; s.h1 = 0
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.append(a["id"])
        for k in ("href", "src"):
            if k in a: s.refs.append(a[k])
        if t == "meta":
            s.meta[a.get("name") or a.get("property") or a.get("charset", "")] = a.get("content")
        if t == "link" and a.get("rel") == "canonical": s.meta["canonical"] = a.get("href")
        if t == "title": s.intitle = True
        if t == "h1": s.h1 += 1
        if t == "script" and a.get("type") == "application/ld+json": s.inld = True
        if t not in VOID: s.st.append((t, s.getpos()[0]))
    def handle_startendtag(s, t, a): pass
    def handle_endtag(s, t):
        if t in VOID: return
        if t == "title": s.intitle = False
        if t == "script": s.inld = False
        if not s.st or s.st[-1][0] != t:
            s.err.append(f"satır {s.getpos()[0]}: </{t}> beklenmedik (açık: {s.st[-1] if s.st else None})")
            for i in range(len(s.st) - 1, -1, -1):
                if s.st[i][0] == t: del s.st[i:]; break
        else: s.st.pop()
    def handle_data(s, d):
        if s.intitle: s.title += d
        if s.inld: s.ld.append(d)
sayfalar = ["index.html", "urunler.html", "hakkimizda.html", "teklif.html", "404.html", "hizmetler.html",
            "elektronik-kart-tasarimi.html", "pcb-uretimi.html", "gomulu-yazilim.html", "tasarim-incelemesi.html", "prototip-ar-ge.html"]
if os.path.isdir(os.path.join(site, "blog")):
    sayfalar += ["blog/index.html"] + sorted(f"blog/{f}" for f in os.listdir(os.path.join(site, "blog")) if f.endswith(".html") and f != "index.html")
teklif = open(os.path.join(site, "teklif.html"), encoding="utf-8").read()
secenek = set(html.unescape(v) for v in re.findall(r'<option value="([^"]*)"', teklif))
sorun = []; basliklar = {}
for fn in sayfalar:
    s = open(os.path.join(site, fn), encoding="utf-8").read()
    p = P(); p.feed(s)
    if p.err: sorun += [f"{fn}: {x}" for x in p.err[:3]]
    if p.st: sorun.append(f"{fn}: kapanmamış {p.st[:3]}")
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup: sorun.append(f"{fn}: tekrarlanan id {dup}")
    if p.h1 != 1: sorun.append(f"{fn}: h1 sayısı {p.h1}")
    for blok in p.ld:
        try: json.loads(blok)
        except Exception as ex: sorun.append(f"{fn}: JSON-LD hatası {ex}")
    for r in p.refs:
        u = urlparse(r)
        if u.scheme in ("http", "https", "mailto") or r.startswith("#") or not u.path: continue
        yol = unquote(u.path).lstrip("/")
        if "/" in fn and not u.path.startswith("/"):
            sorun.append(f"{fn}: alt klasörde göreli bağlantı {r}")
        if yol.endswith("/"): yol += "index.html"
        if not os.path.exists(os.path.join(site, yol)): sorun.append(f"{fn}: eksik hedef {r}")
        if yol == "teklif.html" and u.query:
            v = parse_qs(u.query).get("urun", [None])[0]
            if v not in secenek: sorun.append(f"{fn}: teklif seçeneği yok: {v}")
    t = html.unescape(p.title.strip()); d = p.meta.get("description") or ""
    basliklar[fn] = t
    if fn != "404.html":
        print(f"{fn:30s} başlık {len(t):3d} · açıklama {len(d):3d} · canonical {p.meta.get('canonical')} · og:image {'var' if p.meta.get('og:image') else 'YOK'} · JSON-LD {len(p.ld)}")
if len(set(basliklar.values())) != len(basliklar): sorun.append("tekrarlanan başlık")
sm = open(os.path.join(site, "sitemap.xml"), encoding="utf-8").read()
for loc in re.findall(r"<loc>https://modwaretechnology\.com/([^<]*)</loc>", sm):
    f = "index.html" if loc == "" else (loc + "index.html" if loc.endswith("/") else loc + ".html")
    if not os.path.exists(os.path.join(site, f)): sorun.append(f"sitemap: dosya yok {loc}")
print("site haritası adres sayısı:", sm.count("<loc>"))
print("\nSORUN YOK" if not sorun else "\n".join(["SORUNLAR:"] + sorun))