import os, re, sys, json, html
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote, parse_qs
site = sys.argv[1]
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","source","track","wbr","path","circle","rect","polyline","line"}
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.st = []; s.err = []; s.ids = []; s.refs = []; s.meta = {}; s.title = ""; s.intitle = False; s.ld = []; s.inld = False; s.h1 = 0
        s.lang = None; s.alt = {}; s.dugme = None; s.metin = []; s.kod = 0
    def handle_starttag(s, t, a):
        a = dict(a)
        if t == "html": s.lang = a.get("lang")
        if "id" in a: s.ids.append(a["id"])
        for k in ("href", "src"):
            if k in a: s.refs.append(a[k])
        if t == "meta":
            s.meta[a.get("name") or a.get("property") or a.get("charset", "")] = a.get("content")
        if t == "link" and a.get("rel") == "canonical": s.meta["canonical"] = a.get("href")
        if t == "link" and a.get("rel") == "alternate" and a.get("hreflang"): s.alt[a["hreflang"]] = a.get("href")
        if t == "a" and "lang-switch" in (a.get("class") or ""): s.dugme = a.get("href")
        if t in ("script", "style", "pre", "code"): s.kod += 1
        if t == "title": s.intitle = True
        if t == "h1": s.h1 += 1
        if t == "script" and a.get("type") == "application/ld+json": s.inld = True
        for k in ("alt", "aria-label", "title", "placeholder"):
            if a.get(k): s.metin.append(a[k])
        if t not in VOID: s.st.append((t, s.getpos()[0]))
    def handle_startendtag(s, t, a): pass
    def handle_endtag(s, t):
        if t in VOID: return
        if t == "title": s.intitle = False
        if t == "script": s.inld = False
        if t in ("script", "style", "pre", "code"): s.kod = max(0, s.kod - 1)
        if not s.st or s.st[-1][0] != t:
            s.err.append(f"satır {s.getpos()[0]}: </{t}> beklenmedik (açık: {s.st[-1] if s.st else None})")
            for i in range(len(s.st) - 1, -1, -1):
                if s.st[i][0] == t: del s.st[i:]; break
        else: s.st.pop()
    def handle_data(s, d):
        if s.intitle: s.title += d
        if s.inld: s.ld.append(d)
        if not s.kod: s.metin.append(d)
sayfalar = ["index.html", "urunler.html", "hakkimizda.html", "teklif.html", "404.html", "hizmetler.html",
            "elektronik-kart-tasarimi.html", "pcb-uretimi.html", "gomulu-yazilim.html", "tasarim-incelemesi.html", "prototip-ar-ge.html"]
if os.path.isdir(os.path.join(site, "blog")):
    sayfalar += ["blog/index.html"] + sorted(f"blog/{f}" for f in os.listdir(os.path.join(site, "blog")) if f.endswith(".html") and f != "index.html")
# İngilizce sayfalar (/en/): klasördeki bütün sayfalar
for kok, _, dosyalar in os.walk(os.path.join(site, "en")):
    sayfalar += sorted(os.path.relpath(os.path.join(kok, f), site).replace("\\", "/") for f in dosyalar if f.endswith(".html"))
def secenekler(fn):
    return set(html.unescape(v) for v in re.findall(r'<option value="([^"]*)"', open(os.path.join(site, fn), encoding="utf-8").read()))
secenek = {"teklif.html": secenekler("teklif.html")}
if os.path.exists(os.path.join(site, "en", "quote.html")): secenek["en/quote.html"] = secenekler("en/quote.html")
IZINLI = {"İzmit", "Kocaeli", "Türkiye", "Türkiye's", "Türkçe"}   # İngilizce sayfada kalabilecek Türkçe harfli kelimeler
AYNI_OLABILIR = {"3D model (STEP):"}   # iki dilde de aynı yazılan ifadeler
sorun = []; basliklar = {}; diller = {}; metinler = {}; esler = {}
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
        if u.path.endswith(".html"):
            sorun.append(f"{fn}: uzantılı iç bağlantı {r} (temiz adres kullanın: /sayfa)")
        yol = unquote(u.path).lstrip("/")
        if "/" in fn and not u.path.startswith("/"):
            sorun.append(f"{fn}: alt klasörde göreli bağlantı {r}")
        if yol == "": yol = "index.html"
        elif yol.endswith("/"): yol += "index.html"
        elif not os.path.splitext(yol)[1]: yol += ".html"  # temiz adres: /hizmetler → hizmetler.html
        if not os.path.exists(os.path.join(site, yol)): sorun.append(f"{fn}: eksik hedef {r}")
        if yol in secenek and u.query:
            v = parse_qs(u.query).get("urun", [None])[0]
            if v not in secenek[yol]: sorun.append(f"{fn}: teklif seçeneği yok: {v} ({yol})")
    t = html.unescape(p.title.strip()); d = p.meta.get("description") or ""
    basliklar[fn] = t
    beklenen_dil = "en" if fn.startswith("en/") else "tr"
    if p.lang != beklenen_dil: sorun.append(f"{fn}: html lang {p.lang} (beklenen {beklenen_dil})")
    if not p.dugme: sorun.append(f"{fn}: dil düğmesi yok")
    elif p.alt and "https://modwaretechnology.com" + p.dugme != p.alt.get("tr" if beklenen_dil == "en" else "en"):
        sorun.append(f"{fn}: dil düğmesi {p.dugme} karşı dildeki eşine gitmiyor")
    if beklenen_dil == "en":
        kalan = sorted({w for x in p.metin for w in re.findall(r"[\w'’]+", x) if re.search(r"[çğıöşüÇĞÖŞÜ]", w)} - IZINLI)
        if kalan: sorun.append(f"{fn}: İngilizce sayfada Türkçe kelimeler {kalan[:8]}")
        esler[fn] = p.alt.get("tr") or "404.html"
    # Çeviri denetimi için: en az iki kelimeli ve küçük harfli kelime içeren metinler (marka, kod, sayı değil)
    metinler[fn] = {" ".join(x.split()) for x in p.metin if len(x.split()) >= 2 and re.search(r"\b[a-zçğıöşü]{3,}\b", x)}
    if not fn.endswith("404.html"):
        diller[p.meta.get("canonical")] = (fn, p.alt)
        if set(p.alt) != {"tr", "en", "x-default"}: sorun.append(f"{fn}: hreflang eksik {sorted(p.alt)}")
        elif p.alt[beklenen_dil] != p.meta.get("canonical"): sorun.append(f"{fn}: hreflang {beklenen_dil} canonical değil")
        print(f"{fn:42s} başlık {len(t):3d} · açıklama {len(d):3d} · canonical {p.meta.get('canonical')} · og:image {'var' if p.meta.get('og:image') else 'YOK'} · JSON-LD {len(p.ld)}")
# hreflang karşılıklı olmalı: her dil karşılığı aynı üçlüyü taşır
for url, (fn, alt) in diller.items():
    for h, hedef in alt.items():
        if hedef not in diller: sorun.append(f"{fn}: hreflang {h} hedefi üretilmemiş {hedef}"); continue
        if diller[hedef][1] != alt: sorun.append(f"{fn}: hreflang karşılıklı değil ({h} → {diller[hedef][0]})")
print("dil eşleri:", sum(1 for _, a in diller.values() if a), "sayfa")
# Çevrilmemiş metin: İngilizce sayfada Türkçe eşiyle birebir aynı kalan cümleler (Türkçe harf içermese de yakalanır)
for fn, karsi_url in esler.items():
    tr_fn = diller[karsi_url][0] if karsi_url in diller else karsi_url
    ayni = (metinler[fn] & metinler.get(tr_fn, set())) - AYNI_OLABILIR
    if ayni: sorun.append(f"{fn}: Türkçe eşiyle ({tr_fn}) aynı kalan metin {sorted(ayni)[:5]}")
if len(set(basliklar.values())) != len(basliklar): sorun.append("tekrarlanan başlık")
sm = open(os.path.join(site, "sitemap.xml"), encoding="utf-8").read()
def dosya(loc):
    return "index.html" if loc == "" else (loc + "index.html" if loc.endswith("/") else loc + ".html")
sm_loc = re.findall(r"<loc>https://modwaretechnology\.com/([^<]*)</loc>", sm)
for loc in sm_loc:
    if not os.path.exists(os.path.join(site, dosya(loc))): sorun.append(f"sitemap: dosya yok {loc}")
print("site haritası adres sayısı:", sm.count("<loc>"))
llms_yol = os.path.join(site, "llms.txt")
if os.path.exists(llms_yol):
    lt = open(llms_yol, encoding="utf-8").read()
    if not lt.startswith("# "): sorun.append("llms.txt: ilk satır '# Başlık' değil")
    ll = re.findall(r"\]\(https://modwaretechnology\.com/([^)]*)\)", lt)
    for loc in ll:
        if not os.path.exists(os.path.join(site, dosya(loc))): sorun.append(f"llms.txt: dosya yok {loc}")
    eksik = set(sm_loc) - set(ll) - {""}
    if eksik: sorun.append(f"llms.txt: site haritasındaki sayfalar eksik {sorted(eksik)}")
    print("llms.txt sayfa sayısı:", len(ll))
else:
    sorun.append("llms.txt yok")
print("\nSORUN YOK" if not sorun else "\n".join(["SORUNLAR:"] + sorun))