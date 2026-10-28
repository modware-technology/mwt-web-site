# modwaretechnology.com — site üretici araçları

Bu dal (`site-araclari`) yalnızca sitenin bazı sayfalarını üreten yardımcı dosyaları saklar. Sitenin kendisi `main` dalındadır; bu dal yayına girmez.

| Dosya | Ne yapar? |
|---|---|
| `seo_uret.py` | Hizmet sayfalarını (`hizmetler.html`, `elektronik-kart-tasarimi.html` …), blog sayfalarını (`blog/`), sekme başlıklarını, açıklamaları, paylaşım önizlemelerini, yapılandırılmış veriyi, menüdeki Blog bağlantısını, `robots.txt`, `sitemap.xml`, `llms.txt` ve `_redirects` dosyalarını üretir. Hizmet metinleri dosyanın içindeki `HIZMETLER` ve `SAYFALAR` bölümlerindedir. |
| `blog_yazilar.py` | Blog yazılarının metinleri. Yeni yazı için listeye ekleyip `seo_uret.py`'yi çalıştırın; yazı sayfası, blog listesi, site haritası ve `llms.txt` birlikte güncellenir. |
| `seo_kontrol.py` | Üretilen sayfaları denetler: kapanmamış etiket, tekrarlanan kimlik, tek `h1`, yapılandırılmış veri, kırık iç bağlantı, teklif formu seçenekleri, site haritası ve `llms.txt` (bağlantılar çalışıyor mu, site haritasındaki her sayfa listede mi). Sonunda `SORUN YOK` yazmalı. |
| `lh_ozet.py` | Lighthouse hız ölçümü raporlarını (JSON) kısaca özetler. |
| `onizleme.py` | Yerel önizleme sunucusu: temiz adresleri (`/hizmetler` → `hizmetler.html`) Cloudflare Pages gibi açar. `python onizleme.py <site-klasörü>` → `http://127.0.0.1:8765/` |

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
