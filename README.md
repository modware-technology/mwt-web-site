# modwaretechnology.com — site üretici araçları

Bu dal (`site-araclari`) yalnızca sitenin bazı sayfalarını üreten yardımcı dosyaları saklar. Sitenin kendisi `main` dalındadır; bu dal yayına girmez.

| Dosya | Ne yapar? |
|---|---|
| `seo_uret.py` | Sitenin Türkçe ve İngilizce (`/en/`) sürümlerini birlikte üretir: hizmet sayfaları (`hizmetler.html`, `elektronik-kart-tasarimi.html` … / `en/services.html` …), blog sayfaları (`blog/`, `en/blog/`), sekme başlıkları, açıklamalar, paylaşım önizlemeleri, yapılandırılmış veri, menüdeki Blog bağlantısı, TR/EN dil düğmesi, `hreflang` dil eşleri, `robots.txt`, `sitemap.xml`, `llms.txt` ve `_redirects`. Türkçe hizmet metinleri dosyanın içindeki `HIZMETLER` ve `SAYFALAR` bölümlerindedir. |
| `blog_yazilar.py` | Türkçe blog yazılarının metinleri. Yeni yazı için listeye ekleyip `seo_uret.py`'yi çalıştırın; yazı sayfası, blog listesi, site haritası ve `llms.txt` birlikte güncellenir. |
| `hizmet_en.py` | İngilizce hizmet sayfası metinleri (`HIZMETLER_EN`, `SAYFALAR_EN`, `HUB_EN`) ve üreticinin sabit arayüz metinlerinin İngilizce karşılıkları (`METIN_EN`). |
| `blog_en_1.py`, `blog_en_2.py` | İngilizce blog yazıları. Her yazının `tr` alanı, Türkçe karşılığının adresidir (ör. `stm32-modbus-rtu-rs485`). |
| `seo_kontrol.py` | Üretilen sayfaları denetler: kapanmamış etiket, tekrarlanan kimlik, tek `h1`, yapılandırılmış veri, kırık iç bağlantı, iki dildeki teklif formu seçenekleri, doğru `lang`, dil düğmesi, karşılıklı `hreflang`, İngilizce sayfada kalan Türkçe kelime veya Türkçe eşiyle birebir aynı kalan (çevrilmemiş) metin, site haritası ve `llms.txt` (bağlantılar çalışıyor mu, site haritasındaki her sayfa listede mi). Sonunda `SORUN YOK` yazmalı. |
| `js_metinler.py` | JS dosyalarında kullanıcıya görünen Türkçe metinleri listeler (çevrilmemiş metin kalmış mı?): `python js_metinler.py js/main.js js/animations.js` |
| `en_sayfalar.py` | Tek seferlik: `teklif.html` ve `404.html` dosyalarından `en/quote.html` ve `en/404.html` sayfalarını çıkardı. Ortak menü ve alt bilginin İngilizce karşılıkları da bu dosyadadır. |
| `ceviri-rehberi.md` | Çeviri rehberi: Türkçe–İngilizce adres eşlemesi, terim sözlüğü, yazım kuralları. |
| `lh_ozet.py` | Lighthouse hız ölçümü raporlarını (JSON) kısaca özetler. |
| `onizleme.py` | Yerel önizleme sunucusu: temiz adresleri (`/hizmetler` → `hizmetler.html`) Cloudflare Pages gibi açar; bulunamayan adreste en yakın 404 sayfasını gösterir (`/en/…` → `en/404.html`). `python onizleme.py <site-klasörü>` → `http://127.0.0.1:8765/` |

## Kullanım

Python 3.10 veya üstü yeterlidir; ek paket gerekmez.

```
python seo_uret.py <site-klasörü>
python seo_kontrol.py <site-klasörü>
```

`<site-klasörü>`, `main` dalının bilgisayardaki kopyasıdır. Üretici mevcut dosyaların üzerine yazar; çalıştırdıktan sonra `git diff` ile değişiklikleri kontrol edin.

## Dikkat

- Üretici her çalıştırmada aynı sonucu verir (ikinci çalıştırma hiçbir dosyayı değiştirmez). Hizmet ve blog sayfalarını elle düzenlerseniz, bir sonraki çalıştırmada bu düzenlemeler silinir; kalıcı değişiklikleri buradaki dosyalarda yapın.
- Başlıklarda her kelime büyük harfle başlar ("ve, ile, ya da, mi" küçük kalır); üretici bunu kendisi uygular.
- Site içi bağlantıları üretici temiz adrese çevirir (`hizmetler.html` → `/hizmetler`); `seo_kontrol.py` uzantılı bağlantı kalırsa uyarır.
- `main` dalına yapılan her gönderim bir yayın demektir (Cloudflare Pages ücretsiz planda ayda 500). Yine de değişiklikleri biriktirip tek seferde göndermek iyi bir alışkanlıktır.

## İngilizce site (`/en/`)

- Ana sayfa, ürünler, hakkımızda, teklif ve 404 sayfalarının İngilizcesi (`en/index.html`, `en/products.html`, `en/about.html`, `en/quote.html`, `en/404.html`) elle tutulur. Türkçe karşılığında metin değişirse İngilizcesini de güncelleyin; başlık, açıklama ve `hreflang` satırlarını üretici yazar (`seo_uret.py` → `MEVCUT`).
- Hizmet ve blog sayfalarının İngilizcesi üretilir. Yeni blog yazısı hem `blog_yazilar.py`'ye hem de `blog_en_1.py` / `blog_en_2.py`'den birine eklenmelidir; iki dil birebir eşleşmezse üretici durur.
- İngilizce yazıların yayın tarihi `seo_uret.py` içindeki `TARIH_EN` değeridir.
- JS dosyalarındaki görünen metinler `T('Türkçe', 'English')` biçiminde yazılır; dil, sayfanın `<html lang>` değerinden anlaşılır.
- Teklif formundan gelen İngilizce taleplerin e-posta konusu `(EN)` ile biter.
