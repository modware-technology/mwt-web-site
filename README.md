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
- `assets/og/modware-og.png`: paylaşım önizlemesi görseli (1200 × 630; LinkedIn, WhatsApp, X)

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

- Her sayfanın `<head>` bölümünde: anahtar kelimeli `<title>` (≈ 70 karakterden kısa), `description` (≈ 160 karakter), `canonical` (uzantısız adres, ör. `https://modwaretechnology.com/urunler`) ve paylaşım önizlemesi (`og:*`). Ana sayfada firma ve web sitesi, hizmet sayfalarında hizmet için yapılandırılmış veri (`application/ld+json`, schema.org) var.
- Yeni sayfa eklerken: başlık ve açıklamayı benzersiz yazın, `canonical` ekleyin ve `sitemap.xml`'e adresini ekleyin.
- Google Search Console ve Bing Webmaster Tools'a site haritası olarak `https://modwaretechnology.com/sitemap.xml` gönderilir.
- Görünmeyen metne anahtar kelime doldurmayın (Google bunu cezalandırır); bir konuda görünmek için o konuyu anlatan görünür bir sayfa gerekir.
