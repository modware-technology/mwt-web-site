"""Tek seferlik: teklif.html → en/quote.html ve 404.html → en/404.html (birebir metin değiştirme).
Her değiştirme tam olarak beklenen sayıda eşleşmelidir; eşleşmezse betik durur.
Bundan sonra en/quote.html ve en/404.html elle tutulan sayfalardır (seo_uret.py başlıklarını günceller).
Kullanım: python en_sayfalar.py <site-klasörü>
"""
import os
import re
import sys

SITE = sys.argv[1]

ORTAK = [  # üst menü ve alt bilgi (her sayfada aynı)
    ('<a class="logo" href="/" aria-label="ModWare Technology ana sayfa">',
     '<a class="logo" href="/en/" aria-label="ModWare Technology home">'),
    ('aria-label="Menüyü aç"', 'aria-label="Open menu"'),
    ('aria-label="Ana menü"', 'aria-label="Main menu"'),
    ('<a class="nav-link" href="/" data-nav="home">Ana Sayfa</a>', '<a class="nav-link" href="/en/" data-nav="home">Home</a>'),
    ('<a class="nav-link" href="/hizmetler" data-nav="hizmetler">Hizmetler</a>',
     '<a class="nav-link" href="/en/services" data-nav="hizmetler">Services</a>'),
    ('<a class="nav-link" href="/urunler" data-nav="urunler">Ürünler</a>',
     '<a class="nav-link" href="/en/products" data-nav="urunler">Products</a>'),
    ('<a class="nav-link" href="/hakkimizda" data-nav="hakkimizda">Hakkımızda</a>',
     '<a class="nav-link" href="/en/about" data-nav="hakkimizda">About</a>'),
    ('<a class="nav-link" href="/blog/" data-nav="blog">Blog</a>', '<a class="nav-link" href="/en/blog/" data-nav="blog">Blog</a>'),
    ('<a class="btn btn-accent nav-cta" href="/teklif">Teklif Al</a>', '<a class="btn btn-accent nav-cta" href="/en/quote">Get a Quote</a>'),
    ('<a class="logo logo-sm" href="/">', '<a class="logo logo-sm" href="/en/">'),
    ('aria-label="E-posta gönderin: info@modwaretechnology.com"', 'aria-label="Send us an e-mail: info@modwaretechnology.com"'),
    ('aria-label="ModWare Technology LinkedIn sayfası (yeni sekmede açılır)"',
     'aria-label="ModWare Technology on LinkedIn (opens in a new tab)"'),
    ('aria-label="Sayfanın başına dön"', 'aria-label="Back to top"'),
    ('<html lang="tr">', '<html lang="en">'),
]

TEKLIF = [
    ('<p class="eyebrow" data-anim="hero">Teklif Al</p>', '<p class="eyebrow" data-anim="hero">Get a Quote</p>'),
    ('>Projenizi Anlatın, Teklifimizi Hazırlayalım.</h1>', '>Tell Us About Your Project, We&#x27;ll Prepare a Quote.</h1>'),
    ('Formu inceleyip size kapsam, süre ve tahmini bütçeyle dönüyoruz. İş birliği ve diğer konular için de bu formu kullanabilirsiniz.',
     'We review your form and get back to you with the scope, timeline and an estimated budget. You can also use this form for partnerships and other topics.'),
    ('aria-label="Teklif formu"', 'aria-label="Quote form"'),
    ('value="Yeni teklif talebi: modwaretechnology.com"', 'value="New quote request: modwaretechnology.com (EN)"'),
    ('value="ModWare Technology web sitesi"', 'value="ModWare Technology website (EN)"'),
    ('<label>Bu kutuyu işaretlemeyin ', '<label>Do not tick this box '),
    ('aria-live="polite">Zorunlu alanlar: 0 / 5</p>', 'aria-live="polite">Required fields: 0 / 5</p>'),
    ('<span>01</span> Ne İstiyorsunuz?</legend>', '<span>01</span> What Do You Need?</legend>'),
    ('<legend>Konu</legend>', '<legend>Topic</legend>'),
    ('value="Teklif / proje" id="q-topic-1" checked><span>Teklif / proje</span>',
     'value="Quote / project" id="q-topic-1" checked><span>Quote / project</span>'),
    ('value="İş birliği / pilot uygulama" id="q-topic-2"><span>İş birliği / pilot</span>',
     'value="Partnership / pilot project" id="q-topic-2"><span>Partnership / pilot</span>'),
    ('value="Diğer" id="q-topic-3"><span>Diğer</span>', 'value="Other" id="q-topic-3"><span>Other</span>'),
    ('<label for="q-product">Ürün / hizmet ', '<label for="q-product">Product / service '),
    ('<span class="opt" id="q-product-opt" hidden>(opsiyonel)</span>', '<span class="opt" id="q-product-opt" hidden>(optional)</span>'),
    ('<option value="">Bir seçenek belirleyin</option>', '<option value="">Choose an option</option>'),
    ('<optgroup label="Geliştirme ve kontrol">', '<optgroup label="Development and control">'),
    ('<optgroup label="Sensör">', '<optgroup label="Sensors">'),
    ('<optgroup label="Haberleşme">', '<optgroup label="Communication">'),
    ('<optgroup label="Güç">', '<optgroup label="Power">'),
    ('<optgroup label="PRISM modüler güç platformu">', '<optgroup label="PRISM modular power platform">'),
    ('>ModWare Guard · Taşıyıcı ve koruma kartı</option>', '>ModWare Guard · Carrier and protection board</option>'),
    ('>ModWare Shift 24 / 12 · Buck-boost güç modülü</option>', '>ModWare Shift 24 / 12 · Buck-boost power module</option>'),
    ('>ModWare Pure 5 · 5 V güç modülü</option>', '>ModWare Pure 5 · 5 V power module</option>'),
    ('>ModWare Pilot · Kontrol ve arayüz kartı</option>', '>ModWare Pilot · Control and interface board</option>'),
    ('>ModWare Prism · Platformun tamamı</option>', '>ModWare Prism · Complete platform</option>'),
    ('<optgroup label="Hizmetler">', '<optgroup label="Services">'),
    ('<option value="Özel donanım tasarımı">Özel donanım / kart tasarımı</option>',
     '<option value="Custom hardware design">Custom hardware / board design</option>'),
    ('<option value="PCB tasarımı">PCB tasarımı</option>', '<option value="PCB design">PCB design</option>'),
    ('<option value="PCB üretimi">PCB üretimi</option>', '<option value="PCB manufacturing">PCB manufacturing</option>'),
    ('<option value="Tasarım incelemesi">Tasarım incelemesi</option>', '<option value="Design review">Design review</option>'),
    ('<option value="Gömülü yazılım">Gömülü yazılım</option>', '<option value="Embedded software">Embedded software</option>'),
    ('<option value="Üretim danışmanlığı">Üretim danışmanlığı</option>',
     '<option value="Manufacturing consulting">Manufacturing consulting</option>'),
    ('<option value="Diğer">Diğer</option>', '<option value="Other">Other</option>'),
    ('<legend>Proje aşaması</legend>', '<legend>Project stage</legend>'),
    ('value="Fikir" id="q-stage-1" checked><span>Fikir</span>', 'value="Idea" id="q-stage-1" checked><span>Idea</span>'),
    ('value="Prototip" id="q-stage-3"><span>Prototip</span>', 'value="Prototype" id="q-stage-3"><span>Prototype</span>'),
    ('value="Üretim" id="q-stage-4"><span>Üretim</span>', 'value="Production" id="q-stage-4"><span>Production</span>'),
    ('<span>02</span> Proje Detayları</legend>', '<span>02</span> Project Details</legend>'),
    ('<label for="q-qty">Tahmini adet</label>', '<label for="q-qty">Estimated quantity</label>'),
    ('<option>Belirtmek istemiyorum</option>', '<option>Prefer not to say</option>', 2),  # adet ve bütçe
    ('<option>100–1.000</option>', '<option>100–1,000</option>'),
    ('<option>1.000+</option>', '<option>1,000+</option>'),
    ('<label for="q-time">Zaman planı</label>', '<label for="q-time">Timeline</label>'),
    ('<option>Hemen</option>', '<option>Right away</option>'),
    ('<option>1–3 ay</option>', '<option>1–3 months</option>'),
    ('<option>3–6 ay</option>', '<option>3–6 months</option>'),
    ('<option>6 ay ve sonrası</option>', '<option>6 months or later</option>'),
    ('<label for="q-budget">Bütçe aralığı</label>', '<label for="q-budget">Budget range</label>'),
    ('<option>50.000 ₺ altı</option>', '<option>Under ₺50,000</option>'),
    ('<option>50.000 – 250.000 ₺</option>', '<option>₺50,000 – 250,000</option>'),
    ('<option>250.000 ₺ üzeri</option>', '<option>Over ₺250,000</option>'),
    ('<label for="q-ref">Referans bağlantı <span class="opt">(opsiyonel)</span></label>',
     '<label for="q-ref">Reference link <span class="opt">(optional)</span></label>'),
    ('placeholder="GitHub, doküman veya çizim bağlantısı"', 'placeholder="Link to GitHub, a document or a drawing"'),
    ('<label for="q-msg">Kısa açıklama ', '<label for="q-msg">Short description '),
    ('placeholder="Amaç, hedefler, özel gereksinimler… (ör. giriş gerilimi, haberleşme arayüzü, ortam koşulları)"',
     'placeholder="Purpose, goals, special requirements… (e.g. input voltage, communication interface, operating conditions)"'),
    ('<span>03</span> İletişim Bilgileri</legend>', '<span>03</span> Contact Details</legend>'),
    ('<label for="q-name">Ad soyad ', '<label for="q-name">Full name '),
    ('placeholder="Adınız Soyadınız"', 'placeholder="Your full name"'),
    ('<label for="q-company">Şirket / kurum <span class="opt">(opsiyonel)</span></label>',
     '<label for="q-company">Company / organization <span class="opt">(optional)</span></label>'),
    ('placeholder="Şirket adı"', 'placeholder="Company name"'),
    ('<label for="q-email">E-posta ', '<label for="q-email">E-mail '),
    ('placeholder="ornek@domain.com"', 'placeholder="name@company.com"'),
    ('<label for="q-phone">Telefon <span class="opt">(opsiyonel)</span></label>',
     '<label for="q-phone">Phone <span class="opt">(optional)</span></label>'),
    ('placeholder="+90 5xx xxx xx xx"', 'placeholder="With country code, e.g. +90 5xx xxx xx xx"'),
    ('name="onay" value="evet" required>', 'name="onay" value="yes" required>'),
    ('<span>Bilgilerimin teklif hazırlamak amacıyla işlenmesini kabul ediyorum. ',
     '<span>I agree that my details are processed to prepare a quote. '),
    ('<span class="quote-submit-label">Teklif iste</span>', '<span class="quote-submit-label">Request a quote</span>'),
    ('<h2>Talebiniz Bize Ulaştı.</h2>', '<h2>We Have Received Your Request.</h2>'),
    ('<p>Formunuzu inceleyip en kısa sürede <strong id="quote-success-email">e-posta adresinize</strong> dönüş yapacağız.</p>',
     '<p>We will review your form and reply to <strong id="quote-success-email">your e-mail address</strong> as soon as possible.</p>'),
    ('<a class="btn btn-ghost" href="/urunler">Ürünlere göz atın</a>', '<a class="btn btn-ghost" href="/en/products">Browse our products</a>'),
    ('<h2>Süreç Nasıl İşler?</h2>', '<h2>How Does It Work?</h2>'),
    ('<strong>İhtiyaçları anlayalım.</strong> Formu inceleyip gerekirse kısa bir görüşme planlarız.',
     '<strong>We understand your needs.</strong> We review your form and schedule a short call if needed.'),
    ('<strong>Teklif ve plan.</strong> Kapsam, süre, teslimatlar ve tahmini bütçe.',
     '<strong>Quote and plan.</strong> Scope, timeline, deliverables and an estimated budget.'),
    ('<strong>Başlangıç.</strong> Yol haritası, kilometre taşları ve iletişim kanalı.',
     '<strong>Kick-off.</strong> Roadmap, milestones and a communication channel.'),
    ('<h2>Hızlı İletişim</h2>', '<h2>Quick Contact</h2>'),
    ('<p class="aside-label">E-posta</p>', '<p class="aside-label">E-mail</p>'),
    ('data-copy="info@modwaretechnology.com">Kopyala</button>', 'data-copy="info@modwaretechnology.com">Copy</button>'),
    ('<span class="visually-hidden"> (yeni sekmede açılır)</span>', '<span class="visually-hidden"> (opens in a new tab)</span>'),
    ('<p class="aside-label">Konum</p>', '<p class="aside-label">Location</p>'),
    ('<p class="aside-text">İzmit, Kocaeli</p>', '<p class="aside-text">İzmit, Kocaeli, Türkiye</p>'),
]

BULUNAMADI = [
    ('<title>Sayfa Bulunamadı | ModWare Technology</title>', '<title>Page Not Found | ModWare Technology</title>'),
    ('<p class="eyebrow" data-anim="hero">Hata 404</p>', '<p class="eyebrow" data-anim="hero">Error 404</p>'),
    ('>Bu Sayfa Devre Dışı.</h1>', '>This Page Is Off the Board.</h1>'),
    ('<p data-anim="hero">Aradığınız sayfa taşınmış ya da kaldırılmış olabilir.</p>',
     '<p data-anim="hero">The page you are looking for may have been moved or removed.</p>'),
    ('<a class="btn btn-primary" href="/">Ana sayfaya dön</a>', '<a class="btn btn-primary" href="/en/">Back to the home page</a>'),
    ('<a class="btn btn-ghost" href="/urunler">Ürünlere göz atın</a>', '<a class="btn btn-ghost" href="/en/products">Browse our products</a>'),
]


def uygula(s, kurallar, ad):
    for eski, yeni, *adet in kurallar:
        n, beklenen = s.count(eski), (adet[0] if adet else 1)
        if n != beklenen:
            sys.exit(f"{ad}: '{eski[:70]}' {n} kez geçiyor ({beklenen} bekleniyordu)")
        s = s.replace(eski, yeni)
    return s


def mutlak(s):
    return re.sub(r'\b(href|src)="(?!https?:|mailto:|tel:|data:|#|/)([^"]+)"', r'\1="/\2"', s)


def surum(s):
    return re.sub(r'(/(?:css/style\.css|js/main\.js|js/animations\.js))\?v=\d+', r'\1?v=31', s)


for kaynak, hedef, kurallar in (("teklif.html", "en/quote.html", TEKLIF), ("404.html", "en/404.html", BULUNAMADI)):
    ham = open(os.path.join(SITE, kaynak), "rb").read().decode("utf-8")
    nl = "\r\n" if "\r\n" in ham else "\n"
    s = ham.replace("\r\n", "\n")
    s = uygula(s, ORTAK + kurallar, kaynak)
    s = surum(mutlak(s))
    os.makedirs(os.path.join(SITE, "en"), exist_ok=True)
    open(os.path.join(SITE, hedef), "wb").write(s.replace("\n", nl).encode("utf-8"))
    kalan = sorted(set(re.findall(r">([^<>]*[çğıöşüÇĞÖŞÜ][^<>]*)<", re.sub(r"<!--.*?-->", "", s, flags=re.S))))
    print(f"{hedef}: yazıldı; Türkçe harf kalan metinler: {kalan}")
