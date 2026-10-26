"""modwaretechnology.com — arama motoru görünürlüğü.

Mevcut sayfaların görünüşüne dokunmadan: sekme başlıkları, açıklamalar, canonical, paylaşım önizlemesi,
yapılandırılmış veri, robots.txt, sitemap.xml. Her hizmet için sitenin aynı bileşenleriyle ayrı bir sayfa.
Kullanım: python seo_uret.py <site-klasörü>
"""
import html
import json
import math
import os
import re
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_yazilar import YAZILAR  # noqa: E402

SITE = sys.argv[1]
ALAN = "https://modwaretechnology.com"
OG_IMG = f"{ALAN}/assets/og/modware-og.png"
TARIH = "2026-10-26"
ORG_ID = f"{ALAN}/#org"


def e(s):
    return html.escape(s, quote=True)


def oku(fn):
    raw = open(os.path.join(SITE, fn), "rb").read().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    return raw.replace("\r\n", "\n"), nl


def yaz(fn, s, nl="\r\n"):
    yol = os.path.join(SITE, fn)
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    open(yol, "wb").write(s.replace("\n", nl).encode("utf-8"))


# ---------------------------------------------------------------- başlık yazımı
# Başlıklarda her kelime büyük harfle başlar; TDK'ya göre "ve, ile, ya da, veya, de/da, ki" ve soru eki "mi" küçük kalır.
KUCUK_KALIR = {"ve", "ile", "ya", "da", "de", "veya", "ki"}
SORU_EKI = re.compile(r"m[ıiuü](?:y[ıiuü][mz]|s[ıiuü]n(?:[ıiuü]z)?|d[ıiuü]r(?:l[ae]r)?)?")
BOSLUK_VARLIK = {"&nbsp;", "&#160;", "&#xa0;"}


def _buyut(kelime, ilk):
    m = re.match(r"(\W*)([^\W\d_])(.*)", kelime, re.S)
    if not m:
        return kelime
    on, harf, kalan = m.groups()
    # Zaten büyük harfle başlayan (PCB, STM32) ya da içinde büyük harf olan (mA, kHz) kelimeye dokunulmaz
    if not harf.islower() or any(c.isupper() for c in kalan):
        return kelime
    kok = re.sub(r"\W+$", "", harf + kalan)
    if not ilk and (kok in KUCUK_KALIR or SORU_EKI.fullmatch(kok)):
        return kelime
    return on + {"i": "İ", "ı": "I"}.get(harf, harf.upper()) + kalan


def _baslik_ic(ic):
    cikti, bas, ilk = [], True, True
    for p in re.split(r"(<[^>]+>|&[#\w]+;|\s+|/)", ic):
        if not p:
            continue
        if p.startswith("<"):
            bas = bas or bool(re.match(r"<br\b", p, re.I))
        elif p.isspace() or p == "/" or p in BOSLUK_VARLIK:
            bas = True
        elif p.startswith("&") and p.endswith(";"):
            # Açılış tırnağından sonra kelime büyür; kesme işaretinden (&#x27;) sonraki ek küçük kalır
            bas = p in ("&quot;", "&#34;")
        else:
            if bas:
                p = _buyut(p, ilk)
                ilk = False
            bas = False
        cikti.append(p)
    return "".join(cikti)


def basliklar(s):
    s = re.sub(r"(<(h[1-3])\b[^>]*>)(.*?)(</\2>)",
               lambda m: m.group(1) + _baslik_ic(m.group(3)) + m.group(4), s, flags=re.S)
    return re.sub(r'(<legend class="q-legend"[^>]*>)(.*?)(</legend>)',
                  lambda m: m.group(1) + _baslik_ic(m.group(2)) + m.group(3), s, flags=re.S)


# ---------------------------------------------------------------- temiz adresler
# Site içi bağlantılar uzantısız ve kökten başlar: hizmetler.html → /hizmetler, index.html → /,
# blog/index.html → /blog/. Cloudflare Pages .html adreslerini her tıklamada ayrıca yönlendirir;
# temiz adres doğrudan açılır ve Google'a bildirilen (canonical) adresle aynıdır.
def temiz_url(s):
    def cevir(m):
        yol, ek = m.group(2).lstrip("/"), m.group(3) or ""
        yeni = "/" + (yol[:-len("index.html")] if yol.endswith("index.html") else yol[:-len(".html")])
        return f'{m.group(1)}="{yeni}{ek}"'
    return re.sub(r'\b(href)="(?!https?:|mailto:|tel:|#|//)(/?[a-z0-9/_-]+\.html)([?#][^"]*)?"', cevir, s)


def son_isle(s):
    return temiz_url(basliklar(s))


# ---------------------------------------------------------------- ikonlar (24×24, çizgi)
IKON = {
    "chip": '<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M9.5 3v4M14.5 3v4M9.5 17v4M14.5 17v4M3 9.5h4M3 14.5h4M17 9.5h4M17 14.5h4"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "box": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "code": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
    "bolt": '<path d="M13 2L5 13.5h6L10 22l8-11.5h-6z"/>',
    "flask": '<path d="M9.5 3h5M10.5 3v6.2L5.2 18.4A1.8 1.8 0 0 0 6.8 21h10.4a1.8 1.8 0 0 0 1.6-2.6L13.5 9.2V3"/><path d="M7.5 15h9"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "gauge": '<path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4-6"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "cycle": '<path d="M20 12a8 8 0 0 1-14 5.3"/><path d="M4 12a8 8 0 0 1 14-5.3"/><path d="M18 3v4h-4"/><path d="M6 21v-4h4"/>',
    "wave": '<path d="M2 12h4l3-7 5 14 3-7h5"/>',
    "list": '<path d="M10 6h10M10 12h10M10 18h10"/><path d="M4 6l1.2 1.2L7.5 5M4 12l1.2 1.2L7.5 11M4 18l1.2 1.2L7.5 17"/>',
    "thermo": '<path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0z"/><path d="M12 9v7"/>',
    "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
}

# ---------------------------------------------------------------- hizmetler
# urun: teklif formundaki seçenek değeri (form ?urun= ile o seçenek seçili açılır)
HIZMETLER = [
    dict(slug="elektronik-kart-tasarimi", ad="Elektronik kart ve donanım tasarımı", ikon="chip", urun="Özel donanım tasarımı",
         ozet="Gereksinimden şematiğe, PCB tasarımından prototipe: kontrol, güç, sensör ve haberleşme kartları."),
    dict(slug="pcb-uretimi", ad="PCB üretimi", ikon="box", urun="PCB üretimi",
         ozet="Dosya kontrolünden teslimata; prototip ve küçük seri baskı devre kart üretimi."),
    dict(slug="gomulu-yazilim", ad="Gömülü yazılım geliştirme", ikon="code", urun="Gömülü yazılım",
         ozet="Donanımınıza özel, sahada güvenilir çalışan gömülü yazılım: sıfırdan geliştirme ya da mevcut yazılımın iyileştirilmesi."),
    dict(slug="tasarim-incelemesi", ad="Tasarım incelemesi", ikon="eye", urun="Tasarım incelemesi",
         ozet="Şematik ve PCB'nizi üretime göndermeden önce inceler, hataları ve riskleri raporlarız."),
    dict(slug="prototip-ar-ge", ad="Prototip ve Ar-Ge", ikon="flask", urun="Özel donanım tasarımı",
         ozet="Fikirden çalışan prototipe, prototipten üretime; test planı ve dokümantasyon."),
]
H = {h["slug"]: h for h in HIZMETLER}

SAYFALAR = {
    "elektronik-kart-tasarimi": dict(
        title="Elektronik Kart, Donanım ve PCB Tasarımı | ModWare Technology",
        desc="Elektronik kart, donanım ve PCB tasarımı: gereksinimden şematiğe, çok katmanlı PCB'den prototipe tek ekip. DFM kontrolü ve üretim dosyaları. İzmit, Kocaeli.",
        eyebrow="Hizmet · Donanım ve PCB tasarımı",
        h1="Elektronik kart, donanım ve PCB tasarımı",
        lede="Fikrinizi çalışan bir elektronik karta dönüştürüyoruz: gereksinimleri birlikte çıkarıyor, şematiği ve çok katmanlı PCB'yi tasarlıyor, prototipi test edip üretime hazırlıyoruz. Elinizde şematik varsa yalnızca PCB tasarımını da üstleniyoruz.",
        kapsam_baslik="Hangi kartları tasarlıyoruz?",
        kapsam=[
            ("chip", "Mikrodenetleyicili kontrol kartları", "STM32 tabanlı kontrol ve arayüz kartları: ekran, enkoder, tuş, LED ve kalıcı olay kaydı."),
            ("bolt", "Güç kartları", "12–48 V DC sistemler için buck ve buck-boost dönüştürücüler, eFuse, ters kutup koruması ve güç dağıtımı."),
            ("gauge", "Ölçüm ve sensör kartları", "Akım, gerilim, sıcaklık ve basınç ölçümü; sinyal koşullandırma ve kalibrasyona uygun tasarım."),
            ("wave", "Haberleşme kartları", "RS-485 (Modbus RTU), izoleli USB, LoRa, I²C, SPI ve UART arayüzleri."),
            ("layers", "Modüler sistemler", "Taşıyıcı kart ve takılabilir modül mimarisi; kartlar arası bağlantı ve mekanik uyum."),
            ("shield", "Sahaya dayanıklı tasarım", "Ters bağlantı, kısa devre, aşırı gerilim ve ESD korumaları; EMC/EMI'yi baştan düşünen yerleşim."),
        ],
        kapsam2=dict(eyebrow="PCB tasarımı", baslik="PCB tasarımında neleri ele alıyoruz?", kartlar=[
            ("layers", "Çok katmanlı kartlar", "Katman sayısını kartın ihtiyacına göre belirler, katman yapısını ve toprak düzlemlerini sinyal bütünlüğüne göre planlarız."),
            ("bolt", "Yüksek akım ve gerilim", "Güç yolları için bakır döküm, akım kapasitesi ve IPC-2221'e göre gerilim aralıkları."),
            ("wave", "Gürültü ve EMC", "Anahtarlama döngülerini küçük tutan yerleşim; analog, dijital ve güç bölgelerinin ayrılması."),
            ("chip", "İnce adımlı entegreler", "0,5 mm adımlı QFN ve TSSOP paketler, termal pedler ve via yerleşimi."),
            ("list", "Üretilebilirlik (DFM)", "Üretim kurallarına uygun iz, aralık ve via ölçüleri; tasarım kuralı denetimi (DRC)."),
            ("box", "Mekanik uyum", "Kutu, konnektör ve montaj deliği konumları; 3D modelle yükseklik ve çakışma kontrolü."),
        ]),
        surec_baslik="Fikirden üretime dört adım",
        surec=[
            ("Gereksinimler", "Kartın ne yapacağını, nerede çalışacağını ve kaç adet üretileceğini birlikte netleştiririz."),
            ("Şematik ve hesap", "Parça seçimi, güç ve ısı hesapları, gerekirse simülasyon; şematiği adım adım onayınıza sunarız."),
            ("PCB ve prototip", "Çok katmanlı PCB yerleşimi, üretim dosyaları ve prototip kartların testi."),
            ("Üretime geçiş", "Maliyet ve tedarik kontrolü, montaj ve test dokümanları; seri üretime hazır paket."),
        ],
        teslim=[
            ("doc", "Tasarım dosyaları", "Şematik ve PCB tasarım dosyaları, kütüphane parçalarıyla birlikte."),
            ("box", "Üretim paketi", "Gerber, delik, malzeme listesi (BOM) ve dizgi (CPL) dosyaları, montaj çizimi."),
            ("list", "Tasarım raporu", "Hesaplar, parça seçim gerekçeleri, test planı ve açık riskler."),
        ],
        sss=[
            ("Elimde yalnızca fikir var, başlayabilir miyiz?", "Evet. Keşif aşamasında ihtiyaçları birlikte yazıya döker, teknik gereksinimleri çıkarırız; tasarım bu belgeyle başlar."),
            ("Mevcut kartımızı geliştirebilir misiniz?", "Evet. Şematik ve PCB'nizi inceleyip revizyon, maliyet düşürme, parça değişimi ya da yeni özellik ekleme yapabiliriz."),
            ("Yalnızca PCB tasarımı yaptırabilir miyim?", "Evet. Şematiğinizi inceler, eksik ya da riskli noktaları raporlar, ardından PCB yerleşimine başlarız. Katman sayısını akım, gürültü ve maliyete göre birlikte belirleriz."),
            ("Tasarım ne kadar sürer?", "Kapsama göre değişir. Teklifte işi aşamalara böler, her aşamanın süresini ve teslimatını ayrı yazarız."),
            ("Dosyalar ve gizlilik nasıl olur?", "Şematik ve PCB tasarım dosyalarını, üretim dosyalarıyla birlikte teslim ederiz. Gizlilik ve fikri mülkiyet koşulları proje başında yazılı olarak belirlenir."),
        ],
        cta="Kartınızı birlikte tasarlayalım.",
    ),
    "pcb-uretimi": dict(
        title="PCB Üretimi | Prototip ve Küçük Seri Baskı Devre – ModWare Technology",
        desc="PCB üretimi hizmeti: dosya kontrolünden teslimata baskı devre kart üretimi. DFM kontrolü, katman yapısı ve yüzey kaplama seçimi, prototip ve küçük seri. İzmit, Kocaeli.",
        eyebrow="Hizmet · PCB üretimi",
        h1="PCB üretimi",
        lede="Prototipten küçük seriye baskı devre kartlarınızın üretimini üstleniyoruz: dosyalarınızı kontrol ediyor, doğru üretim seçeneklerini belirliyor, süreci baştan sona takip edip kartlarınızı teslim ediyoruz.",
        kapsam_baslik="Üretimde neleri üstleniyoruz?",
        kapsam=[
            ("list", "Dosya kontrolü (DFM)", "Gerber ve delik dosyalarınızı üretimden önce kontrol eder, sorunları üretime girmeden düzeltiriz."),
            ("layers", "Doğru üretim seçenekleri", "Katman yapısı, bakır kalınlığı ve yüzey kaplamayı (HASL, ENIG) işe ve bütçeye göre seçeriz."),
            ("box", "Uçtan uca süreç", "Teklif, üretim takibi ve teslimat tek elden; tek muhatabınız biziz."),
            ("cycle", "Prototipten küçük seriye", "Birkaç adet prototiple başlayıp tasarım doğrulandıktan sonra adetleri artırırız."),
            ("doc", "Kolay tekrar üretim", "Doğrulanmış dosyaları ve üretim ayarlarını saklar, bir sonraki siparişi aynı ayarlarla tekrarlarız."),
            ("chip", "Tasarımla birlikte", "Kartın tasarımı da bizdeyse dosyalar üretime hazır çıkar; tasarım ve üretim tek elden yürür."),
        ],
        surec_baslik="Dosyadan teslimata",
        surec=[
            ("Dosyalar", "Kendi tasarımınızın dosyalarını gönderin ya da tasarımı bizimle yapın."),
            ("Kontrol ve teklif", "DFM kontrolü ve üretim seçenekleriyle maliyeti ve süreyi çıkarırız."),
            ("Üretim", "Onayınızla üretimi başlatır, süreci baştan sona takip ederiz."),
            ("Teslim", "Kartlarınızı teslim eder, bir sonraki sipariş için doğrulanmış dosya paketini veririz."),
        ],
        teslim=[
            ("box", "Üretilmiş PCB'ler", "Kararlaştırılan adette ve seçeneklerle üretilmiş baskı devre kartları."),
            ("list", "Üretim öncesi kontrol notu", "DFM kontrolünde bulunan sorunlar ve yapılan düzeltmeler."),
            ("doc", "Tekrar sipariş paketi", "Bir sonraki üretim için doğrulanmış dosyalar ve üretim ayarları."),
        ],
        sss=[
            ("Az adet ürettirebilir miyim?", "Evet. Prototip için birkaç adetle başlayabilir, tasarım doğrulandıktan sonra küçük seriye geçebilirsiniz."),
            ("Tasarımım başka yerde yapıldı, yalnızca üretim isteyebilir miyim?", "Evet. Dosyalarınızı üretimden önce kontrol eder, gereken düzeltmeleri önerir ve üretimi üstleniriz."),
            ("Yüzey kaplama ve katman yapısı neden önemli?", "İnce adımlı entegrelerde düz yüzey (ENIG) lehimlemeyi kolaylaştırır; katman yapısı ise gürültüyü ve ısıyı etkiler. Seçimi işe göre birlikte yaparız."),
            ("Üretim ne kadar sürer?", "Adede ve seçeneklere göre değişir; teklifte üretim ve teslimat süresini ayrıca belirtiriz."),
        ],
        cta="PCB'nizi birlikte üretelim.",
    ),
    "gomulu-yazilim": dict(
        title="Gömülü Yazılım Geliştirme | STM32 Firmware – ModWare Technology",
        desc="Gömülü yazılım geliştirme: mikrodenetleyicili ürünler için sıfırdan firmware ya da mevcut yazılımın iyileştirilmesi. STM32, Modbus RTU, RS-485, USB ve LoRa. İzmit, Kocaeli.",
        eyebrow="Hizmet · Gömülü yazılım",
        h1="Gömülü yazılım geliştirme",
        lede="Mikrodenetleyicili ürünleriniz için gömülü yazılımı, donanımı tasarlayan ekiple birlikte geliştiriyoruz. Yeni ürününüz için sıfırdan yazıyor, mevcut yazılımınızın hatalarını gideriyor ve ona yeni özellikler kazandırıyoruz.",
        kapsam_baslik="Gömülü yazılımda neler yapıyoruz?",
        kapsam=[
            ("chip", "STM32 firmware", "STM32 mikrodenetleyiciler için çevre birimi sürücüleri, zamanlayıcılar, ADC/DAC ve düşük güç modları."),
            ("wave", "Haberleşme protokolleri", "Modbus RTU, RS-485, UART, I²C, SPI, USB ve LoRa; PC, PLC ve SCADA bağlantısı."),
            ("shield", "Arıza ve güvenlik mantığı", "Watchdog, açılış öz testleri, arıza kayıtları ve güvenli kapanma senaryoları."),
            ("gauge", "Ölçüm ve kontrol", "Sensör okuma, filtreleme, kalibrasyon katsayıları ve kapalı çevrim kontrol."),
            ("eye", "Kullanıcı arayüzü", "Ekran, enkoder, tuş ve LED ile sahada izleme ve ayar menüleri."),
            ("cycle", "Mevcut yazılımın geliştirilmesi", "Var olan yazılımınızdaki hataları giderir, yeni özellik ekler ya da yazılımı yeni donanıma taşırız."),
        ],
        surec_baslik="Mimariden teslime",
        surec=[
            ("Mimari", "Görevleri, zamanlamayı, haberleşmeyi ve arıza senaryolarını belirleriz."),
            ("Sürücüler", "Donanım katmanı ve çevre birimleri; kart gelir gelmez temel testler."),
            ("Uygulama", "İş mantığı, haberleşme ve arayüz; ara sürümlerle onayınıza sunarız."),
            ("Test ve teslim", "Senaryo testleri, yüklenebilir yazılım ve kullanım dokümanı."),
        ],
        teslim=[
            ("list", "Test sonuçları", "Senaryo testlerinin sonuçları ve sürüm notları."),
            ("box", "Yüklenebilir yazılım", "Derlenmiş yazılım ve karta yükleme talimatı."),
            ("doc", "Haberleşme dokümanı", "Kullanım kılavuzu ve örneğin Modbus kayıt tablosu."),
        ],
        sss=[
            ("Yalnızca yazılım için çalışabilir miyiz?", "Evet. Mevcut kartınız için yazılım geliştirebilir ya da var olan yazılımı iyileştirebiliriz."),
            ("Hangi mikrodenetleyicilerle çalışıyorsunuz?", "Ağırlıklı olarak STM32 ailesiyle çalışıyoruz; projenin ihtiyacına göre başka aileleri de değerlendiririz."),
            ("Kaynak kod bize teslim edilir mi?", "Standart teslimatımız yüklenebilir yazılım ve kullanım dokümanıdır. Kaynak kodun teslimi ve lisans koşulları projeye göre ayrıca belirlenir."),
            ("PLC ya da SCADA ile haberleşebilir mi?", "Evet. Modbus RTU (RS-485) gibi endüstriyel protokollerle PLC, SCADA ve PC yazılımlarına bağlanır."),
        ],
        cta="Kartınızın yazılımını birlikte yazalım.",
    ),
    "tasarim-incelemesi": dict(
        title="Şematik ve PCB Tasarım İncelemesi, Üretim Öncesi Kontrol | ModWare",
        desc="Kartınızı üretime göndermeden önce şematik ve PCB tasarımınızı inceliyoruz: hatalar, riskler, üretilebilirlik ve maliyet için önceliklendirilmiş rapor. İzmit, Kocaeli.",
        eyebrow="Hizmet · Tasarım incelemesi",
        h1="Şematik ve PCB tasarım incelemesi",
        lede="Kartınızı üretime göndermeden önce şematik ve PCB tasarımınızı ikinci bir göz olarak inceliyoruz. Hataları, riskleri ve iyileştirme önerilerini önceliklendirilmiş bir raporla teslim ediyor, düzeltmelerde destek oluyoruz.",
        kapsam_baslik="Neleri inceliyoruz?",
        kapsam=[
            ("chip", "Şematik kontrolü", "Bağlantı hataları, eksik pull-up ve pull-down dirençleri, yanlış değerler, pin uyumsuzlukları ve elektriksel kurallar."),
            ("bolt", "Güç ve koruma", "Gerilim, akım ve ısı payları; ters bağlantı, kısa devre ve aşırı gerilim korumaları."),
            ("layers", "PCB yerleşimi", "Akım yolları, toprak düzlemi, anahtarlama döngüleri, iz genişlikleri ve gerilim aralıkları."),
            ("list", "Üretilebilirlik (DFM)", "Üretim kuralları, via ve ped ölçüleri, yüzey kaplama ve katman yapısı seçimi."),
            ("box", "Parça ve maliyet", "Bulunması zor ya da riskli parçalar, muadil önerileri ve maliyet düşürme fırsatları."),
            ("doc", "Dosya tutarlılığı", "Malzeme listesi, üretim dosyaları ve montaj çizimlerinin şematikle uyumu."),
        ],
        surec_baslik="Dosyadan rapora",
        surec=[
            ("Dosyalar", "Şematik ve PCB dosyalarınızı ya da PDF ve Gerber çıktılarını gönderin."),
            ("Kapsam ve teklif", "Kartın amacını ve sizi endişelendiren noktaları konuşur, inceleme kapsamını ve süresini belirleriz."),
            ("İnceleme", "Şematik, PCB ve üretim dosyalarını kontrol listesi ve hesaplarla inceleriz."),
            ("Rapor ve destek", "Bulguları önem sırasına göre raporlar, düzeltmeleri birlikte gözden geçiririz."),
        ],
        teslim=[
            ("list", "Önceliklendirilmiş bulgu raporu", "Her bulgu için konum, risk ve önerilen düzeltme; kritikten öneriye sıralı."),
            ("doc", "İşaretli çıktılar", "Sorunlu noktaları işaretlenmiş şematik ve PCB görüntüleri."),
            ("eye", "Değerlendirme görüşmesi", "Raporu birlikte gözden geçirdiğimiz kısa bir toplantı."),
        ],
        sss=[
            ("Hangi dosyaları göndermem gerekiyor?", "Şematik ve PCB dosyaları en iyisidir; yoksa şematiğin PDF'i, Gerber dosyaları ve malzeme listesiyle de inceleme yapabiliriz."),
            ("Kartı sizin tasarlamış olmanız gerekiyor mu?", "Hayır. Başka bir ekibin ya da kendi ekibinizin tasarımını inceleriz; isterseniz düzeltmeleri de biz yaparız."),
            ("İnceleme ne kadar sürer?", "Kartın büyüklüğüne ve kapsamına göre değişir; teklifte süreyi ve teslim tarihini belirtiriz."),
            ("Dosyalarımın gizliliği nasıl korunur?", "Dosyalarınızı yalnızca inceleme için kullanırız; isterseniz incelemeden önce gizlilik sözleşmesi imzalarız."),
        ],
        cta="Kartınızı üretime göndermeden inceleyelim.",
    ),
    "prototip-ar-ge": dict(
        title="Prototip Geliştirme ve Elektronik Ar-Ge | Kocaeli – ModWare Technology",
        desc="Elektronik ürün Ar-Ge'si ve prototip geliştirme: fikirden çalışan prototipe, prototipten üretime. Gereksinim, tasarım, test planı ve dokümantasyon tek ekipte. İzmit, Kocaeli.",
        eyebrow="Hizmet · Ar-Ge",
        h1="Prototip geliştirme ve elektronik Ar-Ge",
        lede="Yeni bir elektronik ürün fikrini çalışan ve üretilebilir bir prototipe dönüştürüyoruz. Donanımı, gömülü yazılımı ve mekaniği aynı ekipte yürütüyor, her aşamayı ölçülebilir teslimatlarla belgeliyoruz.",
        kapsam_baslik="Ar-Ge'de neleri üstleniyoruz?",
        kapsam=[
            ("flask", "Fizibilite ve kavram kanıtı", "Fikrin teknik olarak yapılabilirliğini hızlı bir kavram kanıtıyla (POC) deneriz."),
            ("list", "Gereksinim ve mimari", "Ürünün ne yapacağını, sınırlarını ve kartlar arası arayüzleri belgeye dökeriz."),
            ("chip", "Donanım ve yazılım", "Elektronik kart, gömülü yazılım ve gerekirse PC arayüzü."),
            ("box", "Mekanik ve kutu", "Kart yerleşimi, kutu, konnektör ve ısı yönetimi; makine mühendisliğiyle birlikte."),
            ("gauge", "Test planı ve doğrulama", "Her gereksinim için ölçüm yöntemi ve kabul kriteri; prototip testleri."),
            ("cycle", "Üretime geçiş", "Maliyet düşürme, tedarik, montaj ve test dokümanları."),
        ],
        surec_baslik="Ölçülebilir teslimatlarla dört aşama",
        surec=[
            ("Keşif ve kapsam", "İhtiyaçları ve başarı kriterlerini netleştirir, teknik gereksinimleri çıkarırız."),
            ("Tasarım ve doğrulama", "Şematik, PCB ve yazılım mimarisi; hesap ve ara teslimlerle doğrulama."),
            ("Prototip ve test", "Prototipi üretir, test planına göre ölçer ve iyileştiririz."),
            ("Üretime geçiş", "Üretilebilirlik, tedarik ve test süreçleri; dokümantasyon."),
        ],
        teslim=[
            ("doc", "Gereksinim ve tasarım belgeleri", "Ürünün tanımı, mimarisi, hesapları ve kararların gerekçeleri."),
            ("chip", "Çalışan prototip", "Donanımı ve yazılımıyla test edilebilir prototip."),
            ("list", "Test planı ve sonuçları", "Ölçüm yöntemleri, kabul kriterleri ve sonuç raporu."),
        ],
        sss=[
            ("Fikrim henüz net değil, nereden başlamalıyım?", "Bir keşif görüşmesiyle başlarız; ihtiyacı, kullanım koşullarını ve hedef maliyeti birlikte netleştiririz."),
            ("Prototip kaç aşamada çıkar?", "Genellikle bir kavram kanıtı ve ardından bir ya da iki prototip revizyonu; her aşamanın sonunda öğrendiklerimizi raporlarız."),
            ("Seri üretime nasıl geçeriz?", "Prototip doğrulandıktan sonra maliyet, tedarik ve test süreçlerini düzenler; üretim dosyalarını ve montaj talimatlarını hazırlarız."),
        ],
        cta="Fikrinizi prototipe dönüştürelim.",
    ),
}

HUB = dict(
    title="Hizmetler: Elektronik Tasarım, PCB ve Gömülü Yazılım | ModWare",
    desc="Elektronik kart ve donanım tasarımı, PCB tasarımı ve üretimi, gömülü yazılım, tasarım incelemesi, prototip ve Ar-Ge. İzmit, Kocaeli'den Türkiye geneline.",
    eyebrow="Hizmetler",
    h1="Elektronik tasarımdan üretime",
    lede="Bir elektronik ürünün ihtiyaç duyduğu her adımı tek ekipte topluyoruz. İhtiyacınıza en yakın hizmeti seçin ya da projenizi doğrudan anlatın.",
)

# ---------------------------------------------------------------- sekme ikonu
# Google arama sonuçları SVG ikonu kullanmaz (PNG, ICO vb. ister; 48 px'ten büyük önerilir).
# Bu yüzden SVG'nin yanında 192 px PNG de bildirilir; kök dizindeki favicon.ico yedektir.
def ikon_blok(s):
    m = re.search(r'  <!-- Sekme ikonu -->\n(?:  <(?:link rel="(?:icon|apple-touch-icon)"|meta name="theme-color")[^\n]*\n)+', s)
    assert m, "sekme ikonu bloğu bulunamadı"
    on = "/" if 'href="/assets/favicon.svg"' in m.group(0) else ""  # 404 sayfası mutlak yol kullanır
    blok = ("  <!-- Sekme ikonu -->\n"
            f'  <link rel="icon" href="{on}assets/favicon.svg" type="image/svg+xml">\n'
            f'  <link rel="icon" href="{on}assets/favicon-32.png" sizes="32x32" type="image/png">\n'
            f'  <link rel="icon" href="{on}assets/favicon-192.png" sizes="192x192" type="image/png">\n'
            f'  <link rel="apple-touch-icon" href="{on}assets/apple-touch-icon.png">\n'
            '  <meta name="theme-color" content="#0a0f1c">\n')
    return s[:m.start()] + blok + s[m.end():]


# ---------------------------------------------------------------- menüde Blog bağlantısı (Hakkımızda'dan sonra)
def menu_blok(s):
    if 'data-nav="blog"' in s:
        return s
    m = re.search(r'( *)<li><a class="nav-link" href="(/?)hakkimizda\.html" data-nav="hakkimizda">Hakkımızda</a></li>\n', s)
    assert m, "menüde Hakkımızda bağlantısı bulunamadı"
    girinti, on = m.group(1), m.group(2)
    return s[:m.end()] + f'{girinti}<li><a class="nav-link" href="{on}blog/index.html" data-nav="blog">Blog</a></li>\n' + s[m.end():]


# ---------------------------------------------------------------- şablon parçaları (teklif.html'den)
teklif, _ = oku("teklif.html")
teklif = menu_blok(ikon_blok(teklif))
HEAD_ORTAK = teklif[teklif.index("  <!-- Sekme ikonu -->"):teklif.index("</head>")]
GOVDE_UST = teklif[teklif.index("  <!-- ============ PRELOADER ============ -->"):teklif.index("  <main")]
GOVDE_ALT = teklif[teklif.index("  <!-- ============ ORTAK ALT BİLGİ ============ -->"):]


def og_blok(title, desc, url, jsonld=None, tur="website", ek=()):
    satir = [
        f'  <link rel="canonical" href="{url}">',
        "",
        "  <!-- Paylaşım önizlemesi (LinkedIn, WhatsApp, X) -->",
        f'  <meta property="og:type" content="{tur}">',
        '  <meta property="og:site_name" content="ModWare Technology">',
        '  <meta property="og:locale" content="tr_TR">',
        f'  <meta property="og:title" content="{e(title)}">',
        f'  <meta property="og:description" content="{e(desc)}">',
        f'  <meta property="og:url" content="{url}">',
        f'  <meta property="og:image" content="{OG_IMG}">',
        '  <meta property="og:image:width" content="1200">',
        '  <meta property="og:image:height" content="630">',
        '  <meta name="twitter:card" content="summary_large_image">',
    ] + list(ek)
    if jsonld:
        satir += ["", "  <!-- Arama motorları için yapılandırılmış veri (schema.org) -->",
                  '  <script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/") + "</script>"]
    return "\n".join(satir)


def kart(ikon, baslik, metin, link=None):
    ic = f'<span class="value-icon-wrap"><svg class="value-icon" viewBox="0 0 24 24" aria-hidden="true">{IKON[ikon]}</svg></span>\n              ' if ikon else ""
    lk = f'\n              <a class="link-u" href="{link[0]}">{e(link[1])} <span aria-hidden="true">→</span></a>' if link else ""
    return (f'            <article class="value-card tilt-card" data-glow data-tilt>\n'
            f'              {ic}<h3>{e(baslik)}</h3>\n'
            f'              <p>{e(metin)}</p>{lk}\n'
            f'            </article>')


def bolum(kod, eyebrow, baslik, govde, alt=False, ek=""):
    cls = "section section-alt" if alt else "section"
    return (f'    <section class="{cls}" aria-labelledby="{kod}-title">\n'
            f'      <div class="container">\n'
            f'        <header class="section-head">\n'
            f'          <p class="eyebrow">{e(eyebrow)}</p>\n'
            f'          <h2 id="{kod}-title" data-split-reveal>{e(baslik)}</h2>{ek}\n'
            f'        </header>\n'
            f'{govde}\n'
            f'      </div>\n'
            f'    </section>')


def izgara(kartlar):
    return '        <div class="values-grid">\n' + "\n".join(kartlar) + "\n        </div>"


def surec(baslik, adimlar, alt):
    li = []
    for i, (h3, p) in enumerate(adimlar, 1):
        ok = '\n            <svg class="p-arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>' if i < len(adimlar) else ""
        li.append(f'          <li class="p-step">\n'
                  f'            <span class="p-step-n">{i:02d}</span>\n'
                  f'            <h3>{e(h3)}</h3>\n'
                  f'            <p>{e(p)}</p>{ok}\n'
                  f'          </li>')
    cls = "section section-alt process" if alt else "section process"
    return (f'    <!-- Süreç: animations.js → initProcess (#nasil-calisiyoruz) -->\n'
            f'    <section class="{cls}" id="nasil-calisiyoruz" aria-labelledby="process-title">\n'
            f'      <div class="container">\n'
            f'        <header class="section-head">\n'
            f'          <p class="eyebrow">Süreç</p>\n'
            f'          <h2 id="process-title" data-split-reveal>{e(baslik)}</h2>\n'
            f'        </header>\n\n'
            f'        <ol class="p-list">\n' + "\n".join(li) + "\n        </ol>\n"
            f'      </div>\n'
            f'    </section>')


def teklif_href(urun):
    return "teklif.html" + (f"?urun={quote(urun)}" if urun else "")


def kapanis(baslik, urun):
    return (f'    <section class="section cta-band" aria-labelledby="cta-title">\n'
            f'      <div class="container cta-inner">\n'
            f'        <h2 id="cta-title" data-cta-split>{e(baslik)}</h2>\n'
            f'        <p class="cta-text">Projenizi kısaca anlatın; kapsam, süre ve tahmini bütçeyle dönelim.</p>\n'
            f'        <div class="cta-actions">\n'
            f'          <a class="btn btn-accent" href="{teklif_href(urun)}" data-burst>Teklif Al</a>\n'
            f'          <a class="btn btn-ghost" href="hizmetler.html" data-burst>Tüm hizmetler</a>\n'
            f'        </div>\n'
            f'      </div>\n'
            f'    </section>')


def sayfa_head(title, desc, url, jsonld, tur="website", ek=()):
    return ('<!doctype html>\n<html lang="tr">\n<head>\n'
            '  <meta charset="utf-8">\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'  <title>{e(title)}</title>\n'
            f'  <meta name="description" content="{e(desc)}">\n'
            + og_blok(title, desc, url, jsonld, tur, ek) + "\n\n" + HEAD_ORTAK + "</head>\n")


def sayfa_bas(eyebrow, h1, lede):
    return ('  <main id="main">\n\n'
            '    <!-- ============ SAYFA BAŞLIĞI ============ -->\n'
            '    <section class="page-head" aria-labelledby="page-title">\n'
            '      <div class="container page-head-inner">\n'
            f'        <p class="eyebrow" data-anim="hero">{e(eyebrow)}</p>\n'
            f'        <h1 id="page-title" data-split-intro>{e(h1)}</h1>\n'
            f'        <p class="page-lede" data-anim="hero">{e(lede)}</p>\n'
            '      </div>\n'
            '    </section>\n\n')


def servis_jsonld(slug, s):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": H[slug]["ad"],
        "serviceType": H[slug]["ad"],
        "description": s["desc"],
        "url": f"{ALAN}/{slug}",
        "areaServed": {"@type": "Country", "name": "Türkiye"},
        "provider": {"@type": "Organization", "@id": ORG_ID, "name": "ModWare Technology", "url": f"{ALAN}/"},
    }


def servis_sayfasi(slug):
    s = SAYFALAR[slug]
    url = f"{ALAN}/{slug}"
    bol = [lambda alt: bolum("kapsam", "Kapsam", s["kapsam_baslik"], izgara([kart(*k) for k in s["kapsam"]]), alt=alt)]
    if "kapsam2" in s:
        k2 = s["kapsam2"]
        bol.append(lambda alt: bolum("kapsam2", k2["eyebrow"], k2["baslik"], izgara([kart(*k) for k in k2["kartlar"]]), alt=alt))
    bol.append(lambda alt: surec(s["surec_baslik"], s["surec"], alt=alt))
    bol.append(lambda alt: bolum("teslim", "Teslimatlar", "Projenin sonunda elinizde olanlar", izgara([kart(*k) for k in s["teslim"]]), alt=alt))
    if "ornek" in s:
        b, m = s["ornek"]
        ek = (f'\n          <p class="page-lede">{e(m)}</p>\n'
              f'          <p><a class="btn btn-ghost" href="urunler.html">Ürünleri inceleyin</a></p>')
        bol.append(lambda alt: bolum("ornek", "Örnek", b, "", alt=alt, ek=ek))
    bol.append(lambda alt: bolum("sss", "Sık sorulanlar", "Merak edilenler", izgara([kart(None, q, a) for q, a in s["sss"]]), alt=alt))
    diger = [kart(h["ikon"], h["ad"], h["ozet"], (f'{h["slug"]}.html', "Hizmeti inceleyin")) for h in HIZMETLER if h["slug"] != slug]
    bol.append(lambda alt: bolum("diger", "Diğer hizmetler", "Tek ekipte, uçtan uca", izgara(diger), alt=alt))
    govde = "\n\n".join(f(i % 2 == 1) for i, f in enumerate(bol))
    return "".join([sayfa_head(s["title"], s["desc"], url, servis_jsonld(slug, s)),
                    '<body data-page="hizmetler">\n\n', GOVDE_UST,
                    f'  <!-- Hizmet sayfası: {slug}. Yeni hizmet eklenirse sitemap.xml de güncellenir. -->\n',
                    sayfa_bas(s["eyebrow"], s["h1"], s["lede"]), govde, "\n\n",
                    kapanis(s["cta"], H[slug]["urun"]), "\n\n  </main>\n\n", GOVDE_ALT])


def hub_sayfasi():
    url = f"{ALAN}/hizmetler"
    jl = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Hizmetler", "url": url,
          "description": HUB["desc"], "about": {"@id": ORG_ID},
          "hasPart": [{"@type": "Service", "name": h["ad"], "url": f"{ALAN}/{h['slug']}"} for h in HIZMETLER]}
    kartlar = [kart(h["ikon"], h["ad"], h["ozet"], (f'{h["slug"]}.html', "Hizmeti inceleyin")) for h in HIZMETLER]
    adimlar = [("Keşif ve kapsam", "İhtiyaçları ve başarı kriterlerini netleştirir, teknik gereksinimleri çıkarırız."),
               ("Tasarım ve doğrulama", "Şematik, PCB ve yazılım mimarisi; hesap ve ara teslimlerle doğrulama."),
               ("Prototip ve test", "Prototipi üretir, ölçer ve iyileştiririz."),
               ("Üretime geçiş", "PCB üretimi, tedarik ve dokümantasyon.")]
    return "".join([sayfa_head(HUB["title"], HUB["desc"], url, jl), '<body data-page="hizmetler">\n\n', GOVDE_UST,
                    "  <!-- Hizmetler sayfası. Yeni hizmet eklenirse kartı buraya, adresi sitemap.xml'e eklenir. -->\n",
                    sayfa_bas(HUB["eyebrow"], HUB["h1"], HUB["lede"]),
                    bolum("hizmet", "Ne yapıyoruz?", "Hizmetlerimiz", izgara(kartlar)), "\n\n",
                    surec("Fikirden üretime tek ekip", adimlar, alt=True), "\n\n",
                    kapanis("Projenizi birlikte geliştirelim.", None), "\n\n  </main>\n\n", GOVDE_ALT])


# ---------------------------------------------------------------- blog (/blog/; metinler blog_yazilar.py'de)
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
TR_ASCII = str.maketrans("çğıöşüÇĞİÖŞÜâîû", "cgiosuCGIOSUaiu")
Y = {y["slug"]: y for y in YAZILAR}
BLOG_URL = f"{ALAN}/blog/"
YAYINCI = {"@type": "Organization", "@id": ORG_ID, "name": "ModWare Technology", "url": f"{ALAN}/",
           "logo": {"@type": "ImageObject", "url": f"{ALAN}/assets/logo/modware-icon-512.png"}}
BLOG = dict(
    title="Blog: Elektronik Kart, PCB ve Gömülü Yazılım Yazıları | ModWare",
    desc="Elektronik kart tasarımı, PCB üretimi, EMC ve gömülü yazılım üzerine pratik teknik yazılar: süreçler, üretim dosyaları, sık yapılan hatalar ve maliyet ipuçları.",
    eyebrow="Blog",
    h1="Teknik yazılar",
    lede="Elektronik kart tasarımından PCB üretimine, EMC'den gömülü yazılıma; projelerde işe yarayan pratik bilgileri paylaşıyoruz.",
)


def tarih_tr(t):
    yil, ay, gun = t.split("-")
    return f"{int(gun)} {AYLAR[int(ay) - 1]} {yil}"


def slugla(metin):
    return re.sub(r"[^a-z0-9]+", "-", metin.translate(TR_ASCII).lower()).strip("-")


def baslik_bicimi(metin):
    """Düz metni başlık yazımına çevirir (sekme başlığı, içindekiler ve yapılandırılmış veri için)."""
    return html.unescape(_baslik_ic(e(metin)))


def satir_ici(t):
    """**kalın**, `kod` ve [metin](adres); metin önce HTML için kaçırılır."""
    out = []
    for p in re.split(r"(`[^`]+`)", t):
        if len(p) > 1 and p.startswith("`") and p.endswith("`"):
            out.append(f"<code>{e(p[1:-1])}</code>")
            continue
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e(p))
        out.append(re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', p))
    return "".join(out)


def md(metin):
    """blog_yazilar.py gövde biçimini HTML'e çevirir; (html, [(kimlik, h2 metni)]) döndürür."""
    sat = metin.strip("\n").split("\n")
    out, h2ler, i = [], [], 0
    ozel = re.compile(r"(#{2,3} |> |- |\d+\. |\||```)")
    while i < len(sat):
        s = sat[i]
        if not s.strip():
            i += 1
        elif s.startswith("```"):
            j = i + 1
            while not sat[j].startswith("```"):
                j += 1
            out.append("<pre><code>" + e("\n".join(sat[i + 1:j])) + "</code></pre>")
            i = j + 1
        elif s.startswith("## "):
            t = s[3:].strip()
            h2ler.append((slugla(t), t))
            out.append(f'<h2 id="{slugla(t)}">{satir_ici(t)}</h2>')
            i += 1
        elif s.startswith("### "):
            out.append(f"<h3>{satir_ici(s[4:].strip())}</h3>")
            i += 1
        elif s.startswith("> "):
            buf = []
            while i < len(sat) and sat[i].startswith("> "):
                buf.append(sat[i][2:])
                i += 1
            out.append('<aside class="callout">' + "".join(f"<p>{satir_ici(b)}</p>" for b in buf) + "</aside>")
        elif s.startswith("- ") or re.match(r"\d+\. ", s):
            desen = r"- " if s.startswith("- ") else r"\d+\. "
            et = "ul" if s.startswith("- ") else "ol"
            buf = []
            while i < len(sat) and re.match(desen, sat[i]):
                buf.append(re.sub("^" + desen, "", sat[i]))
                i += 1
            out.append(f"<{et}>\n" + "\n".join(f"  <li>{satir_ici(b)}</li>" for b in buf) + f"\n</{et}>")
        elif s.startswith("|"):
            satirlar = []
            while i < len(sat) and sat[i].startswith("|"):
                satirlar.append([c.strip() for c in sat[i].strip().strip("|").split("|")])
                i += 1
            bas, govde = satirlar[0], satirlar[2:]
            out.append('<div class="table-wrap"><table>\n<thead><tr>' + "".join(f"<th>{satir_ici(c)}</th>" for c in bas)
                       + "</tr></thead>\n<tbody>\n"
                       + "\n".join("<tr>" + "".join(f"<td>{satir_ici(c)}</td>" for c in r) + "</tr>" for r in govde)
                       + "\n</tbody>\n</table></div>")
        else:
            buf = []
            while i < len(sat) and sat[i].strip() and not ozel.match(sat[i]):
                buf.append(sat[i].strip())
                i += 1
            out.append(f"<p>{satir_ici(' '.join(buf))}</p>")
    return "\n".join(out), h2ler


def mutlak(s):
    """/blog/ altındaki sayfalarda göreli bağlantıları kökten başlayan yollara çevirir
    (Netlify yayında .html bağlantılarını sayfanın klasörüne göre çözer)."""
    return re.sub(r'\b(href|src)="(?!https?:|mailto:|tel:|data:|#|/)([^"]+)"', r'\1="/\2"', s)


def okuma(y):
    kelime = len(re.findall(r"\w+", re.sub(r"```.*?```", " ", y["govde"], flags=re.S)))
    return max(1, math.ceil(kelime / 200)), kelime


def blog_kart(y):
    return (f'            <article class="value-card tilt-card blog-card" data-glow data-tilt>\n'
            f'              <span class="value-icon-wrap"><svg class="value-icon" viewBox="0 0 24 24" aria-hidden="true">{IKON[y["ikon"]]}</svg></span>\n'
            f'              <p class="blog-meta">{e(y["kategori"])} · {okuma(y)[0]} dk okuma</p>\n'
            f'              <h3>{e(y["baslik"])}</h3>\n'
            f'              <p>{e(y["ozet"])}</p>\n'
            f'              <a class="link-u" href="/blog/{y["slug"]}.html">Yazıyı okuyun <span aria-hidden="true">→</span></a>\n'
            f'            </article>')


def blog_yazi_sayfasi(y):
    url = f"{ALAN}/blog/{y['slug']}"
    govde, h2ler = md(y["govde"])
    dk, kelime = okuma(y)
    b = baslik_bicimi(y["baslik"])
    jl = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": f"{url}#yazi", "headline": b, "description": y["desc"],
         "datePublished": TARIH, "dateModified": TARIH, "inLanguage": "tr-TR", "url": url, "mainEntityOfPage": url,
         "image": OG_IMG, "articleSection": y["kategori"], "wordCount": kelime,
         "author": {"@type": "Organization", "@id": ORG_ID, "name": "ModWare Technology", "url": f"{ALAN}/"},
         "publisher": YAYINCI, "isPartOf": {"@type": "Blog", "@id": f"{BLOG_URL}#blog", "url": BLOG_URL}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": f"{ALAN}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BLOG_URL},
            {"@type": "ListItem", "position": 3, "name": b}]},
    ]}
    ek = [f'  <meta property="article:published_time" content="{TARIH}">',
          f'  <meta property="article:section" content="{e(y["kategori"])}">']
    icindekiler = ('<nav class="toc" aria-label="İçindekiler">\n<p class="toc-title">İçindekiler</p>\n<ol>\n'
                   + "\n".join(f'  <li><a href="#{k}">{e(baslik_bicimi(t))}</a></li>' for k, t in h2ler) + "\n</ol>\n</nav>")
    bas = ('  <main id="main">\n\n'
           '    <!-- ============ SAYFA BAŞLIĞI ============ -->\n'
           '    <section class="page-head page-head--yazi" aria-labelledby="page-title">\n'
           '      <div class="container page-head-inner">\n'
           f'        <p class="eyebrow" data-anim="hero"><a href="/blog/index.html">Blog</a> · {e(y["kategori"])}</p>\n'
           f'        <h1 id="page-title" data-split-intro>{e(y["baslik"])}</h1>\n'
           f'        <p class="page-lede" data-anim="hero">{e(y["lede"])}</p>\n'
           f'        <p class="post-meta" data-anim="hero"><time datetime="{TARIH}">{tarih_tr(TARIH)}</time> '
           f'<span aria-hidden="true">·</span> <span>{dk} dk okuma</span> '
           '<span aria-hidden="true">·</span> <span>ModWare Technology mühendislik ekibi</span></p>\n'
           '      </div>\n'
           '    </section>\n\n')
    makale = ('    <section class="section article-section">\n'
              '      <div class="container">\n'
              '        <article class="prose">\n'
              f'{icindekiler}\n{govde}\n'
              '        </article>\n'
              '      </div>\n'
              '    </section>')
    ilgili = [kart(H[s]["ikon"], H[s]["ad"], H[s]["ozet"], (f"{s}.html", "Hizmeti inceleyin")) for s in y["ilgili"]]
    return mutlak("".join([
        sayfa_head(y["title"], y["desc"], url, jl, "article", ek), '<body data-page="blog">\n\n', GOVDE_UST,
        f'  <!-- Blog yazısı: {y["slug"]}. Metin site-araclar/blog_yazilar.py dosyasından üretilir. -->\n',
        bas, makale, "\n\n",
        bolum("ilgili", "İlgili hizmetler", "Bu konuda desteğe mi ihtiyacınız var?", izgara(ilgili), alt=True), "\n\n",
        bolum("diger-yazilar", "Blog", "Diğer yazılar", izgara([blog_kart(Y[s]) for s in y["diger"]])), "\n\n",
        kapanis(y["cta"], y["urun"]), "\n\n  </main>\n\n", GOVDE_ALT]))


def blog_liste_sayfasi():
    jl = {"@context": "https://schema.org", "@type": "Blog", "@id": f"{BLOG_URL}#blog", "name": "ModWare Technology Blog",
          "url": BLOG_URL, "description": BLOG["desc"], "inLanguage": "tr-TR", "publisher": YAYINCI,
          "blogPost": [{"@type": "BlogPosting", "headline": baslik_bicimi(y["baslik"]), "url": f"{ALAN}/blog/{y['slug']}",
                        "datePublished": TARIH} for y in YAZILAR]}
    return mutlak("".join([
        sayfa_head(BLOG["title"], BLOG["desc"], BLOG_URL, jl), '<body data-page="blog">\n\n', GOVDE_UST,
        "  <!-- Blog listesi. Yazılar site-araclar/blog_yazilar.py dosyasından üretilir. -->\n",
        sayfa_bas(BLOG["eyebrow"], BLOG["h1"], BLOG["lede"]),
        bolum("yazilar", "Yazılar", "Tüm yazılar", izgara([blog_kart(y) for y in YAZILAR])), "\n\n",
        kapanis("Projenizi birlikte geliştirelim.", None), "\n\n  </main>\n\n", GOVDE_ALT]))


for slug in SAYFALAR:
    yaz(f"{slug}.html", son_isle(servis_sayfasi(slug)))
yaz("hizmetler.html", son_isle(hub_sayfasi()))
print("hizmet sayfaları:", ", ".join(list(SAYFALAR) + ["hizmetler"]))
for y in YAZILAR:
    yaz(f"blog/{y['slug']}.html", son_isle(blog_yazi_sayfasi(y)))
yaz("blog/index.html", son_isle(blog_liste_sayfasi()))
print("blog:", len(YAZILAR), "yazı + liste (" + ", ".join(f"{y['slug']} {okuma(y)[1]} kelime" for y in YAZILAR) + ")")

# ---------------------------------------------------------------- mevcut sayfalar (görünüş değişmez)
ORG_JSONLD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Organization", "@id": ORG_ID, "name": "ModWare Technology", "alternateName": "ModWare", "url": f"{ALAN}/",
            "logo": f"{ALAN}/assets/logo/modware-icon-512.png", "email": "info@modwaretechnology.com",
            "address": {"@type": "PostalAddress", "addressLocality": "İzmit", "addressRegion": "Kocaeli", "addressCountry": "TR"},
            "areaServed": {"@type": "Country", "name": "Türkiye"},
            "sameAs": ["https://www.linkedin.com/company/modware-technology1/"],
            "knowsAbout": ["Elektronik kart tasarımı", "Donanım tasarımı", "PCB tasarımı", "PCB üretimi",
                           "Gömülü yazılım", "STM32", "Güç elektroniği", "DC-DC dönüştürücü", "Prototip geliştirme", "Ar-Ge"],
            "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": h["ad"], "url": f"{ALAN}/{h['slug']}"}} for h in HIZMETLER],
        },
        {"@type": "WebSite", "@id": f"{ALAN}/#website", "name": "ModWare Technology", "alternateName": "ModWare", "url": f"{ALAN}/",
         "inLanguage": "tr-TR", "publisher": {"@id": ORG_ID}},
    ],
}
MEVCUT = {
    "index.html": ("ModWare Technology | Elektronik Kart Tasarımı, PCB ve Gömülü Yazılım",
                   "Karmaşık elektronik sistemler için endüstriyel standartlarda donanım, gömülü yazılım ve Edge AI çözümleri geliştiriyoruz.",
                   f"{ALAN}/", ORG_JSONLD),
    "urunler.html": ("Ürünler: STM32 Kartları, Sensör, LoRa ve PRISM Güç Modülleri | ModWare",
                     "STM32 geliştirme ve kontrol kartları, akım ve basınç sensörü kartları, LoRa haberleşme modülü ve 12–48 V PRISM modüler güç platformu. ModWare Technology, Kocaeli.",
                     f"{ALAN}/urunler", None),
    "hakkimizda.html": ("Hakkımızda: Elektronik Ar-Ge ve Donanım Ekibi | ModWare Technology",
                        "Bir TEKNOFEST takımından doğan, İzmit, Kocaeli merkezli mühendislik ekibi: donanım ve PCB tasarımı, gömülü yazılım, proje yönetimi ve makine mühendisliği.",
                        f"{ALAN}/hakkimizda", None),
    "teklif.html": ("Teklif Al: Elektronik Tasarım, PCB Üretimi ve Gömülü Yazılım | ModWare",
                    "Elektronik kart ve donanım tasarımı, PCB tasarımı ve üretimi, gömülü yazılım ya da ürünlerimiz için teklif alın. Kapsam, süre ve tahmini bütçeyle dönüyoruz.",
                    f"{ALAN}/teklif", None),
}
for fn, (title, desc, url, jl) in MEVCUT.items():
    s, nl = oku(fn)
    s = menu_blok(ikon_blok(s))
    # Önceki çalıştırmanın eklediği blok (canonical … yapılandırılmış veri) kaldırılır, yeniden yazılır
    s = re.sub(r'  <link rel="canonical".*?\n(?=\n  <!-- Sekme ikonu -->)', "", s, count=1, flags=re.S)
    assert "og:title" not in s, f"{fn}: eski blok kaldırılamadı"
    s, n1 = re.subn(r"  <title>.*?</title>\n", f"  <title>{e(title)}</title>\n", s, count=1)
    s, n2 = re.subn(r'  <meta name="description" content="[^"]*">\n',
                    lambda m: f'  <meta name="description" content="{e(desc)}">\n' + og_blok(title, desc, url, jl) + "\n", s, count=1)
    assert n1 == n2 == 1, fn
    if fn == "index.html":
        yeni = '<h1 class="visually-hidden">ModWare Technology: Elektronik Kart Tasarımı, PCB Tasarımı ve Gömülü Yazılım</h1>'
        s, n = re.subn(r'<h1 class="visually-hidden">.*?</h1>', yeni, s, count=1)
        assert n == 1
    if fn == "teklif.html":
        s = s.replace('                    <option value="PCB üretimi ve dizgi">PCB üretimi ve dizgi</option>\n', "")
        eski = '                    <option value="PCB tasarımı">PCB tasarımı</option>\n'
        yeni = '                    <option value="PCB üretimi">PCB üretimi</option>\n'
        if yeni not in s:
            assert s.count(eski) == 1
            s = s.replace(eski, eski + yeni)
        inc = '                    <option value="Tasarım incelemesi">Tasarım incelemesi</option>\n'
        if inc not in s:
            s = s.replace(yeni, yeni + inc)
    yaz(fn, son_isle(s), nl)
s, nl = oku("404.html")
s = menu_blok(ikon_blok(s))
if 'name="robots"' not in s:
    s = s.replace('  <title>Sayfa bulunamadı | ModWare Technology</title>\n',
                  '  <title>Sayfa bulunamadı | ModWare Technology</title>\n  <meta name="robots" content="noindex">\n', 1)
s = s.replace("<title>Sayfa bulunamadı | ModWare Technology</title>", "<title>Sayfa Bulunamadı | ModWare Technology</title>")
yaz("404.html", son_isle(s), nl)
print("mevcut sayfalar: başlık, açıklama, canonical, önizleme; index yapılandırılmış veri; 404 noindex; başlık yazımı")

# ---------------------------------------------------------------- robots, sitemap, README engeli
yollar = (["", "urunler", "hakkimizda", "teklif", "hizmetler"] + [h["slug"] for h in HIZMETLER]
          + ["blog/"] + [f"blog/{y['slug']}" for y in YAZILAR])
yaz("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: https://modwaretechnology.com/sitemap.xml\n")
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for y in yollar:
    sm.append(f"  <url><loc>{ALAN}/{y}</loc><lastmod>{TARIH}</lastmod></url>")
sm.append("</urlset>")
yaz("sitemap.xml", "\n".join(sm) + "\n")
yaz("_redirects", "# Kalıcı (301) yönlendirmeler. README.md arama motorlarına _headers dosyasıyla kapatılır\n"
                 "# (Cloudflare Pages yönlendirmede 404 durumunu desteklemez).\n\n"
                 "# Kaldırılan hizmet sayfası (26.10.2026)\n/guc-elektronigi       /hizmetler  301\n/guc-elektronigi.html  /hizmetler  301\n"
                 "/pcb-tasarimi          /elektronik-kart-tasarimi  301\n/pcb-tasarimi.html     /elektronik-kart-tasarimi  301\n\n"
                 "# Eski sitenin Google'da kayıtlı kalan adresleri (26.10.2026)\n"
                 "/mwhub     /urunler     301\n/iletisim  /teklif      301\n/hakkmzda  /hakkimizda  301\n"
                 "\n# Google Search Console doğrulama dosyaları: Cloudflare .html adreslerini 308 ile uzantısız adrese\n"
                 "# yönlendirir, Search Console ise bu dosyada yönlendirme izlemez. 200 kuralı dosyayı aynı adreste gösterir.\n"
                 + "".join(f"/{f}  /{f[:-5]}  200\n" for f in sorted(os.listdir(SITE)) if re.fullmatch(r"google[0-9a-f]+\.html", f)))
print("robots.txt, sitemap.xml (", len(yollar), "adres), _redirects")
