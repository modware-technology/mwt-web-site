# ModWare Technology — web sitesi

modwaretechnology.com sitesinin kaynak dosyaları. Saf HTML + CSS + JavaScript; derleme adımı yoktur.

## Sayfalar

| Dosya | Sayfa |
|---|---|
| `index.html` | Ana sayfa: hero slaytı, "Nasıl çalışıyoruz" (kaydırmayla patlayan kart), değerler |
| `urunler.html` | Ürün galerisi, kategori filtresi, ürün detay penceresi |
| `hakkimizda.html` | Hakkımızda: fotoğraflı hero, cam kartlar, kaydırmayla açılan cümle |
| `teklif.html` | Teklif formu (Netlify Forms) |
| `404.html` | Bulunamayan sayfa |

## Klasörler

- `css/style.css`: tüm stiller (renkler en üstte `:root` içinde)
- `js/main.js`: menü, form, ürün penceresi, filtre gibi temel davranışlar (GSAP olmadan da çalışır)
- `js/animations.js`: GSAP animasyonları, preloader, Lenis yumuşak kaydırma, özel imleç
- `assets/urunler/`: ürün görselleri (şeffaf arka planlı WebP)
- `assets/sequence/`: kart patlatma kareleri (`pwr-bk/` masaüstü 114 kare, `pwr-bk-sm/` mobil 57 kare)
- `_headers`: Netlify önbellek ve güvenlik başlıkları
- `netlify.toml`: Netlify yayın ayarı

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
- Değiştirilecek metinler HTML'de `<!-- METİN -->` yorumlarıyla işaretlidir (özellikle Hakkımızda sayfası).
