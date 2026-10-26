# ModWare Technology — web sitesi

modwaretechnology.com sitesinin kaynak dosyaları. Saf HTML + CSS + JavaScript; derleme adımı yoktur.

## Sayfalar

| Dosya | Sayfa |
|---|---|
| `index.html` | Ana sayfa: hero slaytı, "Nasıl çalışıyoruz" aşamaları, değerler |
| `urunler.html` | Ürün galerisi (kartlar filtre başlıklarıyla aynı dört kategori grubunda), kategori filtresi, ürün detay penceresi, PRISM (MW-PWR01) entegrasyon şeması, kaydırmayla açılan MODWARE PURE 5 |
| `hakkimizda.html` | Hakkımızda: fotoğraflı hero, cam kartlar, kaydırmayla açılan cümle |
| `teklif.html` | Teklif formu (Netlify Forms) |
| `404.html` | Bulunamayan sayfa |

**Hizmet sayfaları** (ana menüdeki "Hizmetler" bağlantısı `hizmetler.html`'e gider; hepsi `sitemap.xml`'de de var). Mevcut sayfaların bileşenlerini (sayfa başlığı, kart ızgarası, süreç adımları, kapanış bandı) kullanır; `<body data-page="hizmetler">` menüde "Hizmetler"i seçili gösterir. Her sayfanın "Teklif Al" düğmesi formu ilgili hizmet seçili açar (`teklif.html?urun=…`; değer formdaki bir seçenekle birebir aynı olmalı).

| Dosya | Konu |
|---|---|
| `hizmetler.html` | Bütün hizmetlerin listesi |
| `elektronik-kart-tasarimi.html` | Elektronik kart, donanım ve PCB tasarımı |
| `pcb-uretimi.html` | PCB üretimi |
| `gomulu-yazilim.html` | Gömülü yazılım geliştirme (STM32, Modbus RTU, LoRa; mevcut yazılımın geliştirilmesi) |
| `tasarim-incelemesi.html` | Şematik ve PCB tasarım incelemesi (üretim öncesi kontrol) |
| `prototip-ar-ge.html` | Prototip geliştirme ve elektronik Ar-Ge |

**Blog** (ana menüde "Blog"; `<body data-page="blog">`). Sayfalar `blog/` klasöründedir; yayında `/blog/` ve `/blog/<yazı-adı>` adreslerinden açılır. Her yazının sonunda ilgili hizmet sayfalarına ve diğer yazılara bağlantılar vardır.

| Dosya | Konu |
|---|---|
| `blog/index.html` | Yazı listesi |
| `blog/elektronik-kart-tasarim-sureci.html` | Elektronik kart tasarım süreci |
| `blog/pcb-uretimi-icin-gerekli-dosyalar.html` | PCB üretimi için gerekli dosyalar |
| `blog/pcb-tasariminda-emc-kurallari.html` | PCB tasarımında EMC kuralları |
| `blog/stm32-modbus-rtu-rs485.html` | STM32 ile Modbus RTU (RS-485) |
| `blog/pcb-tasarim-incelemesi-sik-yapilan-hatalar.html` | Üretim öncesi tasarım incelemesi: sık yapılan hatalar |
| `blog/prototip-pcb-maliyetini-dusurme.html` | Prototip PCB maliyetini düşürme |

Blog sayfaları alt klasörde olduğu için içlerindeki bütün bağlantılar ve dosya yolları kökten başlar (`/css/style.css`, `/hizmetler.html`). Göreli yol (`css/style.css`) yayında `/blog/css/…` olarak çözülür ve sayfa bozulur.

Yeni yazı eklemek için mevcut bir yazının dosyasını kopyalayın; başlığı (`<title>`, `h1`), açıklamayı, `canonical` adresini, paylaşım önizlemesini, yapılandırılmış veriyi (BlogPosting ve BreadcrumbList) ve metni değiştirin. Ardından `blog/index.html`'deki listeye bir kart, `sitemap.xml`'e de adresi ekleyin.

## Klasörler

- `css/style.css`: tüm stiller (renkler en üstte `:root` içinde)
- `js/main.js`: menü, form, ürün penceresi, filtre gibi temel davranışlar (GSAP olmadan da çalışır)
- `js/animations.js`: GSAP animasyonları, preloader, Lenis yumuşak kaydırma, özel imleç
- `assets/urunler/`: ürün görselleri (şeffaf arka planlı WebP)
- `assets/hakkimizda/`: Hakkımızda arka plan fotoğrafı
- `assets/sequence/pwr-bk/` (114 kare) ve `pwr-bk-sm/` (57 kare, mobil): Ürünler sayfasındaki kart patlatma kareleri
- `_headers`: Netlify önbellek ve güvenlik başlıkları
- `_redirects`: `README.md` yayımlanmaz (404); kaldırılan `guc-elektronigi` sayfası `hizmetler`e, `pcb-tasarimi` sayfası `elektronik-kart-tasarimi`ne yönlenir (301)
- `netlify.toml`: Netlify yayın ayarı
- `robots.txt`, `sitemap.xml`: arama motorları için; site haritasında bütün sayfalar var
- `google9ae5025181fed89f.html`: Google Search Console sahiplik doğrulaması. **Silmeyin**; dosya kalkarsa doğrulama düşer.
- `assets/og/modware-og.png`: paylaşım önizlemesi görseli (1200 × 630; LinkedIn, WhatsApp, X)
- Sekme ikonu: `assets/favicon.svg` (tarayıcı sekmesi), `assets/favicon-32.png`, `assets/favicon-192.png` ve kök dizinde `favicon.ico` (16/32/48 px). Google arama sonuçları SVG kullanmadığı için PNG ve ICO da var; dosya adlarını değiştirmeyin (Google ikonu bu adreslerden tanır).
- `assets/logo/modware-icon-512.png`: arama motorlarına bildirilen firma logosu (ana sayfadaki yapılandırılmış veri)

Kütüphaneler CDN'den, sabit sürümle yüklenir: GSAP 3.12.5 + ScrollTrigger, SplitType 0.3.4, Lenis 1.1.13.

## Yayın (Netlify)

1. Netlify'da **Add new project → Import an existing project → GitHub** ile bu depoyu seçin.
2. Build ayarlarını boş bırakın (`netlify.toml` zaten "derleme yok, kökten yayınla" diyor) ve **Deploy** deyin.
3. **Forms → Enable form detection** açın, ardından bir kez **Deploys → Trigger deploy** yapın.
4. **Forms → Notifications** bölümüne `info@modwaretechnology.com` ekleyin.

Bundan sonra `main` dalına gönderilen her değişiklik siteye kendiliğinden yansır.

## Güncelleme notları

- CSS/JS değiştirdiğinizde HTML'deki `?v=…` sürüm numarasını artırın (tüm sayfalarda), yoksa ziyaretçiler eski dosyayı önbellekten görebilir.
- Ürün metinleri `urunler.html` içindeki kartlarda ve sayfanın altındaki `product-data` JSON bloğunda bulunur; ikisini birlikte güncelleyin.
- Kartlar kategori gruplarında durur (`<section class="product-group" data-group="…">`: gelistirme, sensor, haberlesme, guc). Yeni kartı doğru grubun içine koyun; kartın `data-category` değeri grubuyla aynı olsun. Filtre grupları gösterip gizler.
- Değiştirilecek metinler HTML'de `<!-- METİN -->` yorumlarıyla işaretlidir (özellikle Hakkımızda sayfası).
- Başlıklarda (`h1`–`h3`, teklif formundaki bölüm başlıkları) her kelime büyük harfle başlar: "Elektronik Kart ve Donanım Tasarımı". TDK kuralı gereği "ve, ile, ya da, veya, de/da, ki" ve soru eki "mi" küçük kalır: "Yalnızca PCB Tasarımı Yaptırabilir miyim?". Kısaltmalar (PCB, STM32) olduğu gibi yazılır.

## Arama motoru notları

- Her sayfanın `<head>` bölümünde: anahtar kelimeli `<title>` (≈ 70 karakterden kısa), `description` (≈ 160 karakter), `canonical` (uzantısız adres, ör. `https://modwaretechnology.com/urunler`) ve paylaşım önizlemesi (`og:*`). Ana sayfada firma ve web sitesi, hizmet sayfalarında hizmet, blog yazılarında yazı ve sayfa yolu için yapılandırılmış veri (`application/ld+json`, schema.org) var.
- Yeni sayfa eklerken: başlık ve açıklamayı benzersiz yazın, `canonical` ekleyin ve `sitemap.xml`'e adresini ekleyin.
- Google Search Console ve Bing Webmaster Tools'a site haritası olarak `https://modwaretechnology.com/sitemap.xml` gönderilir.
- Görünmeyen metne anahtar kelime doldurmayın (Google bunu cezalandırır); bir konuda görünmek için o konuyu anlatan görünür bir sayfa gerekir.
