# modwaretechnology.com — site üretici araçları

Bu dal (`site-araclari`) yalnızca sitenin bazı sayfalarını üreten yardımcı dosyaları saklar. Sitenin kendisi `main` dalındadır; bu dal yayına girmez.

| Dosya | Ne yapar? |
|---|---|
| `seo_uret.py` | Hizmet sayfalarını (`hizmetler.html`, `elektronik-kart-tasarimi.html` …), blog sayfalarını (`blog/`), sekme başlıklarını, açıklamaları, paylaşım önizlemelerini, yapılandırılmış veriyi, menüdeki Blog bağlantısını, `robots.txt`, `sitemap.xml` ve `_redirects` dosyalarını üretir. Hizmet metinleri dosyanın içindeki `HIZMETLER` ve `SAYFALAR` bölümlerindedir. |
| `blog_yazilar.py` | Blog yazılarının metinleri. Yeni yazı için listeye ekleyip `seo_uret.py`'yi çalıştırın; yazı sayfası, blog listesi ve site haritası birlikte güncellenir. |
| `seo_kontrol.py` | Üretilen sayfaları denetler: kapanmamış etiket, tekrarlanan kimlik, tek `h1`, yapılandırılmış veri, kırık iç bağlantı, teklif formu seçenekleri, site haritası. Sonunda `SORUN YOK` yazmalı. |
| `lh_ozet.py` | Lighthouse hız ölçümü raporlarını (JSON) kısaca özetler. |

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
- `main` dalına yapılan her gönderim Netlify'da bir yayın demektir ve ücretsiz planda ayda yaklaşık 20 yayın hakkı vardır. Değişiklikleri biriktirip tek seferde gönderin.
