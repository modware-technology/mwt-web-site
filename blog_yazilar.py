"""modwaretechnology.com blog yazıları (seo_uret.py bu dosyadan /blog/ sayfalarını üretir).

Gövde biçimi (küçük bir Markdown alt kümesi):
  ## Başlık        → h2 (içindekiler listesine girer)
  ### Başlık       → h3
  - madde          → madde işaretli liste
  1. madde         → numaralı liste
  > metin          → vurgulu kutu
  | a | b |        → tablo (ilk satır başlık, ikinci satır |---|)
  ```c … ```       → kod bloğu
  **kalın**, `kod`, [metin](/adres.html)
Site içi bağlantılar kökten başlar ve .html ile biter (üretici uzantısız adrese çevirir: /hizmetler.html → /hizmetler).

Yeni yazı: listeye ekleyin ve `python seo_uret.py <site>` çalıştırın; sayfa, blog listesi ve site haritası güncellenir.
"""

YAZILAR = [
    dict(
        slug="elektronik-kart-tasarim-sureci",
        baslik="Elektronik kart tasarım süreci: fikirden seri üretime adım adım",
        title="Elektronik Kart Tasarım Süreci: Fikirden Seri Üretime | ModWare",
        kategori="Elektronik kart tasarımı",
        ikon="chip",
        desc="Elektronik kart nasıl tasarlanır? Gereksinimden şematiğe, PCB yerleşiminden prototip testine ve seri üretime kadar her adımı ve dikkat edilecekleri anlattık.",
        ozet="Gereksinimden şematiğe, PCB'den prototipe ve seri üretime: bir elektronik kartın geçtiği adımlar ve her adımda dikkat edilecekler.",
        lede="Bir elektronik kartın masadaki fikirden seri üretime ulaşması birkaç net adımdan geçer. Her adımın neyi çözdüğünü bilmek, hem projenin süresini hem de maliyetini doğrudan etkiler.",
        ilgili=["elektronik-kart-tasarimi", "prototip-ar-ge", "pcb-uretimi"],
        diger=["pcb-uretimi-icin-gerekli-dosyalar", "pcb-tasarim-incelemesi-sik-yapilan-hatalar", "prototip-pcb-maliyetini-dusurme"],
        cta="Kartınızı birlikte tasarlayalım.",
        urun="Özel donanım tasarımı",
        govde="""
Elektronik kart tasarımı çoğu zaman "şematiği çiz, PCB'yi çiz, ürettir" diye özetlenir. Pratikte ise kartın sahada sorunsuz çalışması, daha şematiğe başlamadan verilen kararlara bağlıdır. Aşağıda bir kartın fikirden seri üretime kadar geçtiği adımları, her adımda sık gözden kaçan noktalarla birlikte anlatıyoruz.

> **Kısaca:** Gereksinimler → mimari ve parça seçimi → şematik ve hesaplar → PCB yerleşimi → üretim dosyaları ve prototip → test ve doğrulama → seri üretime geçiş. Her adımın sonuna bir kontrol noktası koymak, hataları en ucuz oldukları anda yakalamayı sağlar.

## 1. Gereksinimleri yazıya dökün

Tasarımın en ucuz ve en etkili adımı budur. Kartın ne yapacağı kadar, nerede ve hangi koşullarda çalışacağı da netleşmelidir. Kısa bir gereksinim belgesinde en az şu sorular yanıtlanmalıdır:

- **Görev:** Kart neyi ölçecek, neyi sürecek, hangi kararları verecek?
- **Besleme:** Giriş gerilimi kaç volt, ne kadar dalgalanabilir; akü mü, adaptör mü? 12, 24 ya da 48 V sistemlerde ani gerilim yükselmeleri de hesaba katılmalıdır.
- **Arayüzler:** RS-485, CAN, USB, Ethernet ya da kablosuz haberleşme; sensör ve eyleyici bağlantıları.
- **Ortam:** Çalışma sıcaklığı, nem, toz ve titreşim. Endüstriyel bir pano ile ofis ortamı aynı tasarımı gerektirmez.
- **Mekanik:** Kart ölçüsü, kutu, konnektörlerin konumu ve montaj delikleri.
- **Adet ve hedef maliyet:** 10 adet ile 10.000 adet, farklı parça ve üretim kararları demektir.
- **Mevzuat:** CE işareti için EMC ve güvenlik gereksinimleri; ürünün satılacağı pazarın kuralları.

Bu belge ileride "şu özellik de olsa" türünden kapsam kaymalarını da önler. Yeni bir istek geldiğinde etkisi belgeye bakılarak değerlendirilir.

## 2. Mimari ve parça seçimi

Gereksinimler netleşince kartın blok şeması çizilir: güç katı, mikrodenetleyici, sensör girişleri, sürücü çıkışları ve haberleşme arayüzleri. Bu aşamadaki kararlar kartın maliyetini ve tedarik riskini büyük ölçüde belirler.

- **Mikrodenetleyici:** Gereken çevre birimleri (ADC, zamanlayıcı, UART, CAN), bellek ve yazılım ekosistemi birlikte değerlendirilir. STM32 gibi geniş aileler, ileride daha güçlü ya da daha ucuz bir modele geçmeyi kolaylaştırır.
- **Güç mimarisi:** Doğrusal regülatör (LDO) basit ve sessizdir; ama giriş ile çıkış arasındaki fark büyükse ısıya dönüşen güç de büyür. 24 V'tan 3,3 V'a 100 mA çeken bir devrede LDO yaklaşık 2 W ısı üretir; burada anahtarlamalı bir dönüştürücü (buck) daha doğru seçimdir.
- **Tedarik durumu:** Üretimi durdurulmuş (EOL) ya da yeni tasarımlarda önerilmeyen (NRND) parçalardan kaçınılır. Kritik parçalar için muadil seçenekler baştan belirlenir.

## 3. Şematik tasarım ve hesaplar

Şematik, kartın elektriksel tanımıdır. İyi bir şematik yalnızca doğru bağlantıları değil, tasarım kararlarının gerekçelerini de taşır.

- Regülatörlerin bobin, kondansatör ve geri besleme değerleri üretici formüllerine göre hesaplanır.
- Ters bağlantı, aşırı gerilim ve kısa devreye karşı korumalar (ters kutup koruması, TVS diyot, sigorta ya da elektronik sigorta) eklenir.
- Her besleme pinine dekuplaj kondansatörü konur; I²C hatlarına, reset ve açılış (boot) pinlerine gereken dirençler bağlanır.
- Programlama ve hata ayıklama konnektörü (örneğin STM32 için SWD) ile test noktaları unutulmaz.

Şematik bittiğinde, PCB'ye geçmeden önce ikinci bir gözle incelenmesi en ucuz hata ayıklama yöntemidir. Bu konuda [üretim öncesi tasarım incelemesinde en sık yapılan hatalar](/blog/pcb-tasarim-incelemesi-sik-yapilan-hatalar.html) yazımıza da göz atabilirsiniz.

## 4. PCB yerleşimi ve yönlendirme

PCB tasarımında sıra önemlidir: önce yerleşim, sonra yönlendirme. Konnektörler ve montaj delikleri mekanik çizime göre sabitlenir; ardından güç katı, mikrodenetleyici ve hassas analog bölümler yerleştirilir.

- **Katman yapısı:** Katman sayısı; devre yoğunluğu, akım ve gürültü gereksinimine göre seçilir. Kesintisiz bir toprak düzlemi hem sinyal kalitesini hem de EMC performansını iyileştirir.
- **Akım taşıyan yollar:** Yol genişlikleri, taşıyacakları akıma ve izin verilen sıcaklık artışına göre hesaplanır. IPC-2152 bu hesap için kullanılan standarttır.
- **Gürültü:** Anahtarlamalı güç katının akım döngüleri küçük tutulur, hassas sinyaller bu bölgeden uzaklaştırılır. Ayrıntılar için [PCB tasarımında EMC kuralları](/blog/pcb-tasariminda-emc-kurallari.html) yazımıza bakabilirsiniz.
- **Kontroller:** Tasarım kuralı denetimi (DRC) üreticinin kabiliyetlerine göre yapılır; 3D modelle kutu ve konnektör çakışmaları kontrol edilir.

## 5. Üretim dosyaları ve prototip

PCB'nin üretilmesi için tasarım programının kendi dosyası değil, standart üretim çıktıları gerekir: Gerber dosyaları, delik dosyası, malzeme listesi (BOM) ve dizgi için konum dosyası. Hangi dosyanın ne işe yaradığını [PCB üretimi için gerekli dosyalar](/blog/pcb-uretimi-icin-gerekli-dosyalar.html) yazımızda ayrıntılı anlattık.

İlk prototip genellikle 5–10 adet üretilir. Bu adet, birkaç kartı farklı testlerde kullanmaya ve bir kart zarar görürse işin durmamasına yeter.

## 6. Test ve doğrulama

Prototip geldiğinde ilk iş, kartı kontrollü biçimde canlandırmaktır:

1. Besleme akım sınırlamalı bir güç kaynağından verilir; ilk açılışta çekilen akım izlenir.
2. Tüm gerilim rayları ölçülür; regülatörlerin çıkışları ve dalgalanmaları kontrol edilir.
3. Mikrodenetleyici programlanır, çevre birimleri tek tek denenir.
4. İşlevsel testler gereksinim belgesindeki maddelere göre yapılır ve sonuçlar kaydedilir.
5. Sıcaklık, uzun süreli çalışma ve gerekiyorsa EMC ön testleri yapılır.

İlk prototipte küçük düzeltmeler çıkması normaldir. Amaç bunları ikinci revizyonda kapatmak ve seri üretime temiz bir tasarımla geçmektir.

## 7. Seri üretime geçiş

Prototipte çalışan bir kart, seri üretimde de sorunsuz üretilebilmelidir. Bu aşamada:

- Üretilebilirlik (DFM) ve test edilebilirlik (DFT) son kez gözden geçirilir.
- Üretim testi için bir test prosedürü, gerekiyorsa test fikstürü hazırlanır.
- Malzeme listesi maliyet ve tedarik açısından sadeleştirilir.
- Montaj çizimleri, yazılım yükleme talimatları ve revizyon kayıtları tamamlanır.

Az adetli bir ön seri (pilot üretim), büyük siparişten önce süreçteki aksaklıkları görmenin en güvenli yoludur.

## Süreyi ve maliyeti ne belirler?

| Etken | Etkisi |
|---|---|
| Gereksinimlerin netliği | Belirsizlik, revizyon sayısını ve süreyi artırır. |
| Kartın karmaşıklığı | Parça sayısı, katman sayısı ve yerleşim süresi artar. |
| Prototip turu | Her ek revizyon, ek üretim ve test süresi demektir. |
| Sertifikasyon | EMC ve güvenlik testleri ayrı bir planlama ister. |
| Parça tedariki | Uzun teslim süreli parçalar takvimi belirler. |

## Sonuç

İyi bir elektronik kart; net gereksinimlerin, doğru parça seçiminin, dikkatli bir yerleşimin ve planlı testlerin toplamıdır. Bu adımları atlamak kısa vadede zaman kazandırıyor gibi görünse de çoğu zaman ek bir prototip turu olarak geri döner.

ModWare Technology olarak [elektronik kart ve PCB tasarımı](/elektronik-kart-tasarimi.html), [prototip ve Ar-Ge](/prototip-ar-ge.html) ve [PCB üretimi](/pcb-uretimi.html) aşamalarını tek ekipte yürütüyoruz. Projenizin hangi aşamada olduğunu anlatın, size uygun yol haritasını birlikte çıkaralım.
""",
    ),
    dict(
        slug="pcb-uretimi-icin-gerekli-dosyalar",
        baslik="PCB üretimi için hangi dosyalar gerekir? Gerber, delik, BOM ve dizgi dosyaları",
        title="PCB Üretimi İçin Gerekli Dosyalar: Gerber, BOM, CPL | ModWare",
        kategori="PCB üretimi",
        ikon="box",
        desc="PCB üretimi ve dizgi için hangi dosyalar gerekir? Gerber katmanları, delik dosyası, BOM ve dizgi (CPL) dosyasının içeriği ve sık yapılan hatalar.",
        ozet="Gerber katmanları, delik dosyası, BOM ve dizgi dosyası: PCB'yi üretime göndermeden önce hazırlanması gerekenler ve sık yapılan hatalar.",
        lede="Bir PCB'yi üretime göndermek için tasarım programının kendi dosyası değil, üreticilerin okuyabildiği standart çıktılar gerekir. Eksik ya da hatalı bir dosya, haftalarca süren bir gecikmeye dönüşebilir.",
        ilgili=["pcb-uretimi", "tasarim-incelemesi", "elektronik-kart-tasarimi"],
        diger=["prototip-pcb-maliyetini-dusurme", "pcb-tasarim-incelemesi-sik-yapilan-hatalar", "elektronik-kart-tasarim-sureci"],
        cta="PCB'nizi birlikte üretelim.",
        urun="PCB üretimi",
        govde="""
PCB tasarımı bittiğinde kart henüz yalnızca bilgisayardadır. Üretim için tasarımın, üretim makinelerinin anladığı bir dosya setine dönüştürülmesi gerekir. Bu set iki gruba ayrılır: çıplak kartın üretimi için gerekenler ve parçaların kart üzerine dizilmesi (montaj) için gerekenler.

> **Kısaca:** Çıplak kart için Gerber dosyaları, delik (drill) dosyası ve üretim notları; montaj için malzeme listesi (BOM), dizgi konum dosyası (CPL) ve montaj çizimi gerekir.

## Gerber dosyaları

Gerber, PCB endüstrisinin ortak dilidir. Her katman ayrı bir dosyadır ve kartın o katmanda neye benzeyeceğini tarif eder. Günümüzde genişletilmiş Gerber (RS-274X) ya da katman bilgisini dosyanın içinde taşıyan Gerber X2 kullanılır.

| Katman | Ne işe yarar? |
|---|---|
| Üst ve alt bakır | Yollar, pedler ve bakır dökümler |
| İç bakır katmanlar | Çok katmanlı kartlarda iç sinyal ve düzlem katmanları |
| Lehim maskesi | Kartı kaplayan koruyucu boyanın açık kalacağı yerler (pedler) |
| Serigrafi | Parça referansları, logolar ve işaretler |
| Lehim pastası | Dizgide kullanılacak şablonun (stencil) açıklıkları |
| Kart dış hattı | Kartın kesileceği sınır, iç kesimler ve yuvalar |

Dosyaları göndermeden önce bir Gerber görüntüleyicide açıp katmanların eksiksiz ve doğru hizalı olduğunu görmek, en sık yapılan hataları baştan yakalar.

## Delik (drill) dosyası

Deliklerin konumu ve çapı Gerber'de değil, genellikle Excellon biçimindeki ayrı bir delik dosyasında bulunur.

- **Metalize (PTH) ve metalize olmayan (NPTH) delikler** çoğunlukla ayrı dosyalarda verilir. Montaj delikleri ve bazı konnektör pimleri metalize olmamalıdır.
- **Birim ve sayı biçimi** (mm ya da inç, ondalık basamak sayısı) Gerber dosyalarıyla uyumlu olmalıdır; aksi hâlde delikler yanlış yere düşer.
- **Yuvalar (slot)** delik dosyasında ya da dış hat katmanında açıkça tanımlanmalıdır.

## Üretim notları

Bazı bilgiler Gerber'den okunamaz ve ayrıca belirtilmelidir. Kısa bir üretim notu şunları içermelidir:

- Kart kalınlığı (standart 1,6 mm) ve malzeme (FR-4, gerekirse yüksek Tg)
- Bakır kalınlığı (ör. 35 µm / 1 oz) ve katman dizilimi
- Yüzey kaplama (HASL, kurşunsuz HASL ya da ENIG)
- Lehim maskesi ve serigrafi rengi
- Empedans kontrolü, panel ya da özel tolerans gibi özel istekler

## Malzeme listesi (BOM)

Kart dizgiye gidecekse en kritik dosya malzeme listesidir. İyi bir BOM, her satırda tek bir parçayı eksiksiz tanımlar:

| Sütun | Örnek |
|---|---|
| Referanslar | R1, R4, R7 |
| Adet | 3 |
| Değer | 10 kΩ, %1 |
| Paket | 0603 |
| Üretici | Yageo |
| Üretici parça numarası (MPN) | RC0603FR-0710KL |
| Not | Muadil izni, takılmayacak (DNP) bilgisi |

Üretici parça numarası olmayan bir BOM'da "10 µF kondansatör" gibi belirsiz satırlar kalır; bu da yanlış gerilim değerinde ya da yanlış malzemeden parça alınmasına yol açabilir.

## Dizgi konum dosyası (CPL)

Pick-and-place ya da centroid dosyası olarak da bilinen bu dosya, her parçanın kart üzerindeki konumunu ve yönünü verir: referans, X ve Y koordinatı, dönüş açısı ve kartın hangi yüzünde olduğu.

Tasarım programları ile dizgi makineleri dönüş açısı için farklı referanslar kullanabilir. Diyot, entegre ve elektrolitik kondansatör gibi yönlü parçaların ters dizilmesinin en sık nedeni budur. Dizgiden önce üreticinin hazırladığı yerleşim önizlemesini kontrol etmek bu riski büyük ölçüde azaltır.

## Montaj çizimi ve diğer dosyalar

- **Montaj çizimi:** Parça yerleşimini ve yön işaretlerini gösteren PDF; elle yapılacak işlerde ve kontrolde kullanılır.
- **Netlist (IPC-D-356):** Üreticinin kartları elektriksel testten geçirmesine yardımcı olur.
- **3D model (STEP):** Kutu ve mekanik uyum kontrolleri için.

## Sık yapılan hatalar

- Kart dış hattının eksik olması ya da farklı katmanlarda farklı çizilmesi
- Lehim pastası katmanının unutulması
- Delik dosyasının Gerber'den farklı birimde olması
- BOM'daki referansların PCB ile eşleşmemesi, takılmayacak parçaların işaretlenmemesi
- Dizgi dosyasında yönlü parçaların dönüş açılarının hatalı olması
- Serigrafinin pedlerin üzerine taşması
- Eski ve yeni revizyon dosyalarının karışması

## Göndermeden önce kontrol listesi

1. Tüm Gerber katmanlarını bir görüntüleyicide açın; katman sayısını ve hizayı kontrol edin.
2. Delik dosyasının Gerber ile aynı hizada ve aynı birimde olduğunu doğrulayın.
3. Kart kalınlığını, bakır kalınlığını, yüzey kaplamayı ve renkleri üretim notuna yazın.
4. BOM'daki her referansın PCB'de karşılığı olduğunu ve her satırda üretici parça numarası bulunduğunu kontrol edin.
5. Dizgi dosyasındaki yönlü parçaların açılarını önizlemede kontrol edin.
6. Dosya adlarına revizyon kodu ekleyin ve hepsini tek bir arşivde gönderin.

## Sonuç

Doğru hazırlanmış bir dosya seti, üretimin hızlı ve sürprizsiz ilerlemesinin ön koşuludur. [PCB üretimi](/pcb-uretimi.html) hizmetimizde dosyalarınızı üretimden önce kontrol ediyor, uygun üretim seçeneklerini belirliyor ve süreci teslimata kadar takip ediyoruz. Tasarımınızın da gözden geçirilmesini isterseniz [tasarım incelemesi](/tasarim-incelemesi.html) hizmetimize göz atabilirsiniz.
""",
    ),
    dict(
        slug="pcb-tasariminda-emc-kurallari",
        baslik="PCB tasarımında EMC: gürültüyü baştan önlemenin 10 kuralı",
        title="PCB Tasarımında EMC: Gürültüyü Önlemenin 10 Kuralı | ModWare",
        kategori="PCB tasarımı",
        ikon="wave",
        desc="EMC testini geçen kart, tasarımın ilk gününde başlar: toprak düzlemi, akım döngüleri, dekuplaj, anahtarlamalı güç katı ve konnektör filtrelemesi için 10 kural.",
        ozet="Toprak düzlemi, akım döngüleri, dekuplaj, anahtarlamalı güç katı ve konnektör filtrelemesi: EMC sorunlarını baştan önleyen 10 kural.",
        lede="EMC sorunları çoğunlukla test laboratuvarında fark edilir; ama nedenleri neredeyse her zaman PCB'nin ilk yerleşimindedir. Baştan doğru kurulan bir kart, sonradan eklenen ferrit ve kalkanlardan çok daha ucuza gelir.",
        ilgili=["elektronik-kart-tasarimi", "tasarim-incelemesi", "prototip-ar-ge"],
        diger=["pcb-tasarim-incelemesi-sik-yapilan-hatalar", "elektronik-kart-tasarim-sureci", "stm32-modbus-rtu-rs485"],
        cta="Kartınızı üretime göndermeden inceleyelim.",
        urun="Tasarım incelemesi",
        govde="""
Elektromanyetik uyumluluk (EMC), bir cihazın çevresine kabul edilebilir sınırların üzerinde elektromanyetik gürültü yaymaması (yayılım) ve çevresindeki gürültüden etkilenmeden çalışabilmesi (bağışıklık) demektir. Avrupa pazarında satılan elektronik ürünlerde CE işaretinin bir parçasıdır ve EMC yönetmeliği kapsamında test edilir.

EMC'yi sonradan düzeltmek pahalıdır: ek filtreler, ferritler, kalkanlar ve çoğu zaman yeni bir PCB revizyonu gerekir. Oysa gürültünün büyük kısmı, yerleşim aşamasında birkaç temel kurala uyularak baştan önlenebilir.

> **Kısaca:** Akımın dönüş yolunu düşünün, akım döngülerini küçük tutun, toprak düzlemini bölmeyin, gürültüyü kaynağında filtreleyin; kartın kenarlarını ve kablolarını birer anten gibi düşünün.

## 1. Her sinyalin bir dönüş yolu vardır

Akım her zaman bir döngü içinde akar: gittiği yoldan bir şekilde kaynağına geri döner. Yüksek frekanslarda dönüş akımı, sinyal yolunun hemen altındaki referans düzleminden, en düşük empedanslı yolu izleyerek akar. Bu yüzden hızlı sinyallerin altında kesintisiz bir toprak düzlemi bulunmalıdır. Düzlemdeki bir yarık ya da boşluk, dönüş akımını dolanmaya zorlar; döngü büyür, yayılım artar.

## 2. Akım döngülerini küçük tutun

Bir döngünün yaydığı gürültü, döngü alanı ve akımın değişim hızıyla birlikte artar. Kaynak ile yükü birbirine yakın yerleştirmek, sinyal yolunu ve dönüş yolunu birbirine yakın tutmak döngü alanını küçültür. Bu kural hem yayılımı hem de dışarıdan gürültü toplamayı azaltır.

## 3. Anahtarlamalı güç katında "sıcak döngüyü" küçültün

Buck dönüştürücü gibi anahtarlamalı regülatörlerde en kritik bölge, giriş kondansatörü ile anahtarlama elemanları arasındaki döngüdür. Bu döngüdeki akım çok hızlı değişir ve kartın en güçlü gürültü kaynaklarından biridir.

- Giriş kondansatörlerini anahtarlama elemanlarının hemen yanına, mümkün olan en kısa bağlantıyla yerleştirin.
- Anahtarlama düğümünün (SW) bakır alanını, akımı taşıyacak kadar büyük ama gereğinden geniş olmayacak biçimde tutun.
- Geri besleme yolunu bobinden ve anahtarlama düğümünden uzak geçirin.
- Regülatör üreticisinin önerdiği örnek yerleşimi temel alın; bu öneriler genellikle ölçülmüş ve denenmiş yerleşimlerdir.

## 4. Dekuplaj kondansatörlerini doğru yerleştirin

Dekuplaj kondansatörleri, entegrelerin anlık akım ihtiyacını yerel olarak karşılar. Etkili olmaları için besleme pinine en yakın konumda olmalı, toprak bağlantıları da kısa bir via ile doğrudan toprak düzlemine inmelidir. Uzun ve ince bir bağlantı, kondansatörün işe yaradığı frekans aralığını daraltır. Genellikle her besleme pinine bir 100 nF kondansatör ve her besleme rayına bir ya da birkaç daha büyük değerli kondansatör kullanılır.

## 5. Katman yapısını EMC'yi düşünerek seçin

Katman sayısı arttıkça her sinyal katmanının hemen yanına bir referans düzlemi koymak kolaylaşır. Dört katmanlı bir kartta sinyal, toprak, besleme ve sinyal şeklindeki dizilim yaygın ve sağlam bir başlangıçtır. İki katmanlı kartlarda ise bir yüzü olabildiğince kesintisiz toprak dökümüne ayırmak ve yolları bu düzlemi parçalamayacak biçimde planlamak gerekir. Doğru katman sayısı; devre yoğunluğu, hız ve maliyet birlikte düşünülerek belirlenir.

## 6. Kablolar antendir: konnektörlerde filtreleyin

Karttan çıkan her kablo, gürültüyü yayabilen ve toplayabilen bir antendir. Gürültüyü kablo konnektörüne ulaşmadan durdurmak gerekir:

- Haberleşme ve besleme hatlarına konnektör girişinde ferrit, RC filtre ya da ortak mod bobini ekleyin.
- ESD ve ani gerilimlere karşı TVS diyotları konnektörün hemen yanına, kısa bir toprak bağlantısıyla yerleştirin.
- Hızlı sinyalleri ve saat hatlarını konnektörlerden ve kart kenarından uzak tutun.

## 7. Saat ve hızlı sinyalleri yavaşlatın

Gürültünün frekans içeriğini sinyalin frekansından çok kenar hızı belirler. Gereğinden hızlı kenarlar, yüksek frekanslı harmonikler üretir.

- Kristali mikrodenetleyicinin hemen yanına yerleştirin, yollarını kısa tutun ve altından başka sinyal geçirmeyin.
- Hızlı çıkışlara 22–33 Ω seri dirençler ekleyerek kenarları yumuşatın.
- Mikrodenetleyicide pin hızını (STM32'de GPIO hız ayarı) gereken en düşük değerde tutun.

## 8. Analog ve dijital bölümleri yerleşimle ayırın

Toprak düzlemini analog ve dijital diye bölmek çoğu zaman sorunu çözmek yerine yeni dönüş yolu sorunları yaratır. Daha güvenli yaklaşım, tek ve kesintisiz bir toprak düzlemi kullanıp bölümleri yerleşimle ayırmaktır: hassas analog devreleri bir bölgede, gürültülü dijital ve güç devrelerini başka bir bölgede toplamak ve aralarından hızlı sinyal geçirmemek.

## 9. Boşta kalan bakırı kaldırın, toprakları dikin

Toprağa bağlı olmayan, boşta kalan bakır parçaları anten gibi davranabilir; ya kaldırılmalı ya da toprağa bağlanmalıdır. Farklı katmanlardaki toprak alanları, özellikle kart kenarları boyunca ve hızlı sinyallerin katman değiştirdiği noktaların yakınında, sık aralıklı via'larla birbirine bağlanmalıdır.

## 10. Erken ölçün: ön uyumluluk testleri

Laboratuvar testinden önce yapılan basit ölçümler sürprizleri büyük ölçüde azaltır. Yakın alan probları ve bir spektrum analizörüyle kart üzerindeki gürültü kaynakları bulunabilir; kablolardan yayılan gürültü ise ortak mod akım probuyla ölçülebilir. Prototip aşamasında bulunan bir sorun, ürün aşamasında bulunandan çok daha ucuza çözülür.

## EMC kontrol listesi

- Hızlı sinyallerin altında kesintisiz bir referans düzlemi var mı?
- Anahtarlamalı güç katının giriş döngüsü olabildiğince küçük mü?
- Dekuplaj kondansatörleri pinlere yakın ve doğrudan düzleme bağlı mı?
- Konnektörlerde filtre ve ESD koruması var mı?
- Kristal ve saat hatları kısa ve korunaklı mı?
- Boşta kalan bakır alanı ya da bölünmüş düzlem var mı?

## Sonuç

EMC, tasarımın sonunda eklenen bir özellik değil; yerleşimin ilk gününden itibaren alınan kararların sonucudur. Bu kurallar her sorunu tek başına çözmez ama sorunların büyük kısmını laboratuvara gitmeden önler.

[Elektronik kart ve PCB tasarımı](/elektronik-kart-tasarimi.html) projelerimizde EMC'yi baştan yerleşimin bir parçası olarak ele alıyoruz. Elinizde hazır bir tasarım varsa, üretime göndermeden önce [tasarım incelemesi](/tasarim-incelemesi.html) ile riskleri birlikte görebiliriz.
""",
    ),
    dict(
        slug="stm32-modbus-rtu-rs485",
        baslik="STM32 ile Modbus RTU (RS-485): donanımda ve yazılımda dikkat edilecekler",
        title="STM32 ile Modbus RTU ve RS-485: Dikkat Edilecekler | ModWare",
        kategori="Gömülü yazılım",
        ikon="code",
        desc="STM32 ile Modbus RTU: RS-485 sürücü seçimi, sonlandırma ve öngerilim, yön kontrolü, 3,5 karakterlik sessizlik, CRC hesabı ve sahada sık görülen sorunlar.",
        ozet="RS-485 sürücü seçimi, sonlandırma, yön kontrolü, çerçeve zamanlaması ve CRC: STM32 ile sahada sorunsuz çalışan Modbus RTU için kontrol listesi.",
        lede="Modbus RTU, endüstride hâlâ en yaygın saha protokollerinden biri. Kâğıt üzerinde basit görünse de sahada sorunsuz çalışan bir cihaz için donanımda ve yazılımda birkaç kritik ayrıntının doğru kurulması gerekir.",
        ilgili=["gomulu-yazilim", "elektronik-kart-tasarimi"],
        diger=["pcb-tasariminda-emc-kurallari", "elektronik-kart-tasarim-sureci", "pcb-tasarim-incelemesi-sik-yapilan-hatalar"],
        cta="Kartınızın yazılımını birlikte yazalım.",
        urun="Gömülü yazılım",
        govde="""
Modbus RTU; PLC'ler, sürücüler, enerji analizörleri ve sensörler arasında veri alışverişi için yaygın olarak kullanılan, basit bir seri haberleşme protokolüdür. Fiziksel katmanda çoğunlukla RS-485 kullanılır. Bir hatta bir istemci (eski adıyla master) ve adresleri 1 ile 247 arasında olan sunucu cihazlar (eski adıyla slave) bulunur; istemci sorar, sunucu cevap verir.

Protokol basit olduğu için "nasılsa çalışır" diye düşünülür; ama sahadaki sorunların çoğu donanım ayrıntılarından ve zamanlamadan çıkar. Aşağıda STM32 tabanlı bir cihaz tasarlarken dikkat edilmesi gerekenleri donanım ve yazılım olarak iki başlıkta topladık.

> **Kısaca:** Hattın iki ucunu sonlandırın, hattı tek bir noktadan öngerilimleyin, sürücüyü son bit gönderildikten sonra bırakın, çerçeveleri 3,5 karakterlik sessizlikle ayırın ve CRC'yi doğru bayt sırasıyla ekleyin.

## Donanım: RS-485 tarafı

### Sürücü (transceiver) seçimi

- STM32 3,3 V ile çalıştığından, 3,3 V beslemeli bir RS-485 sürücüsü seviye dönüştürme ihtiyacını ortadan kaldırır.
- **Güvenli boşta durum (fail-safe)** özelliği olan sürücüler, hat boştayken ya da kopukken alıcının rastgele karakter üretmesini önler.
- **Birim yük** değeri hatta kaç cihaz bağlanabileceğini belirler. Standart, hat başına 32 birim yük öngörür; 1/8 birim yüklü sürücülerle aynı hatta çok daha fazla cihaz bağlanabilir.
- Uzun hatlarda **kenar hızı sınırlı** sürücüler, yansımaları ve yayılan gürültüyü azaltır.

### Sonlandırma ve öngerilim

- **Sonlandırma:** Hattın yalnızca iki fiziksel ucuna, kablonun karakteristik empedansına yakın (tipik olarak 120 Ω) bir direnç konur. Her cihaza sonlandırma direnci takmak hattı aşırı yükler. Kart üzerinde sonlandırmayı bir köprü ya da anahtarla seçilebilir yapmak sahada büyük kolaylık sağlar.
- **Öngerilim (biasing):** Hat boştayken A ile B arasında tanımlı bir gerilim farkı olmalıdır. Bunun için hattın bir noktasında A ucu besleme tarafına, B ucu toprağa dirençlerle çekilir. Fail-safe özellikli sürücüler bu ihtiyacı azaltır ama her durumda tamamen ortadan kaldırmaz.

### Koruma ve yalıtım

Saha kabloları uzun ve dış etkilere açıktır. Hatta TVS diyotlar (RS-485'in −7 V ile +12 V arasındaki ortak mod aralığına uygun, asimetrik tipler) ve gerekirse seri dirençler ya da PTC sigortalar kullanılır. Cihazlar arasında toprak potansiyeli farkı olabilecek endüstriyel ortamlarda, hattı dijital yalıtıcı ve yalıtılmış DC-DC dönüştürücüyle yalıtmak en güvenli çözümdür.

### Kablolama

- Bükümlü çift kablo kullanın; kılıflı kabloda kılıfı tek noktadan topraklayın.
- Cihazları zincir (daisy chain) şeklinde bağlayın; yıldız bağlantıdan ve uzun dallanmalardan kaçının.
- A ve B'nin yanında ortak bir referans (GND) hattı taşıyın.

## Yazılım: STM32 tarafı

### Yön kontrolü (DE/RE)

RS-485 yarı çift yönlüdür: aynı anda yalnızca bir cihaz konuşur. Gönderimden önce sürücü etkinleştirilir (DE), gönderim bitince bırakılır. En sık yapılan hata, sürücünün son bayt hâlâ gönderilirken bırakılmasıdır; bu durumda son baytın sonu bozulur ve karşı taraf CRC hatası görür.

- Sürücüyü, USART'ın **gönderim tamamlandı (TC)** bayrağı gelince bırakın. Gönderim tamponu boş (TXE) bayrağı, son bayt hâlâ hatta iken gelir.
- STM32F0, F3, G0, G4, L4 ve H7 gibi birçok yeni serinin USART birimlerinde donanımsal **sürücü etkinleştirme (DE)** çıkışı bulunur. Bu özellik yön kontrolünü yazılım zamanlamasından bağımsız hâle getirir; kullandığınız serinin başvuru kılavuzundan kontrol edin.

### Karakter biçimi

Modbus tanımında varsayılan karakter biçimi 8 veri biti, çift (even) eşlik ve 1 durma bitidir (8E1). Eşlik kullanılmıyorsa 2 durma biti öngörülür (8N2). Sahada 8N1 kullanan cihazlar da yaygındır; önemli olan hattaki tüm cihazların aynı ayarı kullanmasıdır. Bu ayarı cihaz menüsünden ya da yapılandırma yazılımından değiştirilebilir kılmak sahada çok işe yarar.

### Çerçeve zamanlaması

Modbus RTU'da çerçeveler arasında en az **3,5 karakter süresi** sessizlik bulunmalı, bir çerçevenin karakterleri arasında ise **1,5 karakter süresinden** uzun boşluk olmamalıdır. 11 bitlik bir karakterde (başlangıç biti, 8 veri biti, eşlik ve durma biti) bir karakter süresi 11 / baud hızıdır:

| Baud hızı | 1 karakter | 3,5 karakter |
|---|---|---|
| 9600 | ≈ 1,15 ms | ≈ 4,0 ms |
| 19200 | ≈ 0,57 ms | ≈ 2,0 ms |
| 38400 ve üzeri | ≈ 0,29 ms ve altı | 1,75 ms (önerilen sabit değer) |

Tanım, 19200 baud'un üzerindeki hızlarda 1,5 karakter için 750 µs, 3,5 karakter için 1,75 ms sabit değerlerinin kullanılmasını önerir.

### Çerçeve sonunu yakalamak

STM32'de verimli bir yöntem, alımı DMA ile bir tampona yapmak ve çerçeve sonunu ayrıca algılamaktır:

- **Boşta hat (IDLE) kesmesi** yaygın ve pratik bir yöntemdir; ancak yaklaşık bir karakter süresi boşlukta tetiklenir, 3,5 karakteri garanti etmez.
- Tanıma tam uyum için her alınan baytta yeniden başlatılan bir **zamanlayıcı (TIM)** ile 3,5 karakterlik sessizlik ölçülür.
- Bazı STM32 serilerinin USART birimlerindeki **alıcı zaman aşımı (receiver timeout)** özelliği, bu süreyi bit süresi cinsinden donanımda saymayı sağlar.

### CRC hesabı

Her çerçevenin sonunda 16 bitlik bir CRC bulunur. Modbus CRC'si 0xFFFF başlangıç değeri ve 0xA001 (ters çevrilmiş 0x8005) polinomuyla hesaplanır; çerçeveye **önce düşük bayt** yazılır. Basit bir C uygulaması:

```c
uint16_t modbus_crc16(const uint8_t *buf, uint16_t len)
{
    uint16_t crc = 0xFFFF;
    for (uint16_t i = 0; i < len; i++) {
        crc ^= buf[i];
        for (uint8_t b = 0; b < 8; b++)
            crc = (crc & 1u) ? (uint16_t)((crc >> 1) ^ 0xA001u) : (uint16_t)(crc >> 1);
    }
    return crc; /* çerçeveye önce düşük bayt, sonra yüksek bayt yazılır */
}
```

Yüksek hızlarda ya da yoğun yük altında tablo tabanlı bir uygulama daha hızlıdır. Bazı STM32 serilerindeki donanımsal CRC birimi de polinomu ve bit sırası ayarlanarak kullanılabilir.

### Fonksiyon kodları ve kayıt haritası

En sık kullanılan fonksiyon kodları:

| Kod | İşlev |
|---|---|
| 03 | Tutma kayıtlarını okuma (Read Holding Registers) |
| 04 | Giriş kayıtlarını okuma (Read Input Registers) |
| 06 | Tek kayıt yazma (Write Single Register) |
| 16 (0x10) | Çoklu kayıt yazma (Write Multiple Registers) |

Desteklenmeyen bir istek geldiğinde cihaz, fonksiyon kodunun en üst bitini 1 yaparak (kod + 0x80) bir hata kodu döndürmelidir: 01 geçersiz fonksiyon, 02 geçersiz adres, 03 geçersiz değer. Kayıt haritasında iki noktayı belgelemek, sahadaki karışıklıkların çoğunu önler: adreslerin 0'dan mı 1'den mi başladığı (ör. 40001 gösterimi) ve 32 bitlik değerlerin iki kayda hangi sırayla yazıldığı.

## Sahada sık görülen sorunlar

- **A ve B'nin ters bağlanması:** Üreticiler A/B ve +/− adlandırmasını farklı kullanabilir; ilk kontrol edilecek şey budur.
- **Eksik ya da fazla sonlandırma:** Sinyal yansımaları ve rastgele hatalar.
- **Öngerilim olmaması:** Hat boştayken alıcı rastgele karakterler görür.
- **Sürücünün erken bırakılması:** Son bayt bozulur, CRC hatası oluşur.
- **Eşlik ve hız uyuşmazlığı:** Cihaz hiç cevap vermez.
- **Kısa cevap zaman aşımı:** İstemci, sunucunun cevabını beklemeden yeni sorgu gönderir.
- **Toprak potansiyeli farkı:** Uzun hatlarda yalıtım yoksa hatalar, hatta arızalar.

## Test önerileri

Geliştirme sırasında bir USB–RS485 dönüştürücü ve bilgisayarda çalışan bir Modbus istemci yazılımıyla cihazı uçtan uca test etmek en hızlı yöntemdir. Mantık analizörünün Modbus çözümleyicisi çerçeveleri ve zamanlamayı görmeyi sağlar; osiloskopla A–B farkını gözlemek ise sonlandırma ve yansıma sorunlarını ortaya çıkarır.

## Sonuç

Sağlam bir Modbus RTU cihazı; doğru seçilmiş ve korunmuş bir RS-485 donanımının, doğru yön kontrolünün, tanıma uygun zamanlamanın ve iyi belgelenmiş bir kayıt haritasının birleşimidir.

[Gömülü yazılım geliştirme](/gomulu-yazilim.html) hizmetimizde STM32 tabanlı cihazlar için Modbus RTU ve RS-485 haberleşmesini, donanımı tasarlayan ekiple birlikte geliştiriyoruz. Haberleşme kartına ihtiyacınız varsa [elektronik kart tasarımı](/elektronik-kart-tasarimi.html) sayfamıza da göz atabilirsiniz.
""",
    ),
    dict(
        slug="pcb-tasarim-incelemesi-sik-yapilan-hatalar",
        baslik="Üretim öncesi tasarım incelemesi: en sık yapılan 15 hata",
        title="PCB Tasarım İncelemesi: En Sık Yapılan 15 Hata | ModWare",
        kategori="Tasarım incelemesi",
        ikon="eye",
        desc="PCB'yi üretime göndermeden önce neler kontrol edilmeli? Şematik, footprint, yerleşim, üretilebilirlik ve dosyalarda en sık yapılan 15 hata ve çözümleri.",
        ozet="Şematikten footprint'e, yerleşimden üretim dosyalarına: kartı üretime göndermeden önce yakalanması gereken 15 yaygın hata.",
        lede="Bir PCB'yi üretime göndermek kolaydır; hatalı bir kartı yeniden üretmek ise hem para hem zaman kaybıdır. Üretimden önce yapılan sistemli bir inceleme, hataların çoğunu daha ucuzken yakalar.",
        ilgili=["tasarim-incelemesi", "elektronik-kart-tasarimi", "pcb-uretimi"],
        diger=["pcb-uretimi-icin-gerekli-dosyalar", "pcb-tasariminda-emc-kurallari", "prototip-pcb-maliyetini-dusurme"],
        cta="Kartınızı üretime göndermeden inceleyelim.",
        urun="Tasarım incelemesi",
        govde="""
Tasarım programlarındaki elektriksel kural denetimi (ERC) ve tasarım kuralı denetimi (DRC) önemli araçlardır; ama yalnızca kendilerine tanımlanan kuralları kontrol ederler. Yanlış seçilmiş bir parça, ters çizilmiş bir konnektör ya da yetersiz bir soğutma alanı bu denetimlerden sorunsuz geçebilir. Bu yüzden üretimden önce kartı bir kontrol listesiyle ve mümkünse tasarımı yapmamış ikinci bir gözle incelemek gerekir.

Aşağıda üretim öncesi incelemelerde en sık karşılaşılan 15 hatayı dört başlıkta topladık.

> **Kısaca:** Önce şematiği, sonra parça ayak izlerini (footprint) ve yerleşimi, ardından üretilebilirliği ve en son üretim dosyalarını kontrol edin. Her bulguyu önem derecesiyle kaydedin.

## Şematikte

### 1. Eksik ya da yanlış çekme dirençleri

I²C hatlarındaki çekme (pull-up) dirençleri, reset pini ve mikrodenetleyicinin açılış modunu belirleyen pinler (STM32'de BOOT0 gibi) en sık unutulan bağlantılardır. Tanımsız kalan bir pin, kartın bazen çalışıp bazen çalışmamasına yol açar.

### 2. Regülatör hesap hataları

Geri besleme bölücüsündeki yanlış bir direnç değeri çıkış gerilimini; yanlış bobin ya da çıkış kondansatörü seçimi ise regülatörün kararlılığını bozar. Değerler, üreticinin formülleri ve önerileriyle tek tek doğrulanmalıdır.

### 3. Isı hesabının yapılmaması

Doğrusal regülatörde giriş–çıkış farkı ile akımın çarpımı ısıya dönüşür. 24 V'tan 3,3 V'a 100 mA, yaklaşık 2 W demektir; küçük bir pakette bu ısıyı atmak mümkün değildir. Her güç elemanı için kayıp ve sıcaklık artışı hesaplanmalıdır.

### 4. Koruma devrelerinin eksik olması

Ters bağlanan besleme, kablodan gelen ani gerilimler ve elektrostatik boşalma (ESD), sahadaki arızaların başlıca nedenleridir. Ters kutup koruması, TVS diyotlar ve sigorta ya da elektronik sigorta, sonradan eklenmesi zor olduğu için baştan düşünülmelidir.

### 5. Pin atama çakışmaları

Mikrodenetleyicide bir pinin birden fazla işlevi olabilir. Aynı pine hem bir UART hem bir zamanlayıcı kanalı atamak ya da kullanılmak istenen çevre biriminin seçilen pakette bulunmaması, ancak yazılım yazılırken fark edilir. Pin ataması, üreticinin yapılandırma aracıyla doğrulanmalıdır.

## Ayak izi ve yerleşimde

### 6. Ayak izinin paketle uyuşmaması

Aynı adı taşıyan paketlerin farklı varyantları olabilir: dar ve geniş SOIC, farklı ölçülerde QFN ya da pin sırası farklı SOT-23 sürümleri. Her ayak izi, satın alınacak parçanın veri sayfasındaki ölçülerle karşılaştırılmalıdır.

### 7. Pin 1 ve kutup işaretlerinin eksik olması

Diyot, LED, elektrolitik kondansatör ve entegrelerde yön işareti serigrafide açıkça görünmelidir. Bu işaretler hem dizgide hem de elle yapılan kontrollerde ters montajı önler.

### 8. Ters çizilmiş konnektörler

Konnektörlerin veri sayfalarında pin numaraları üstten ya da alttan görünüşe göre verilebilir. Karşılıklı bağlanan iki kartta ya da bir kabloda pin sırasının ayna görüntüsü olması, sık rastlanan ve pahalıya mal olan bir hatadır.

### 9. Dekuplaj kondansatörlerinin uzak kalması

Pinlerden uzağa yerleştirilmiş ya da uzun yollarla bağlanmış dekuplaj kondansatörleri görevlerini yapamaz. Her kondansatör, beslediği pine en yakın konumda olmalıdır.

### 10. Mekanik uyumun kontrol edilmemesi

Montaj delikleri, kutu içindeki yükseklik sınırları ve konnektörlerin kutudaki açıklıklarla hizası 3D modelle kontrol edilmelidir. Mekanik bir uyumsuzluk, elektriksel olarak kusursuz bir kartı kullanılamaz hâle getirir.

## Üretilebilirlikte (DFM)

### 11. Üretim kabiliyetinin dışında kalan değerler

Çok ince yollar, çok dar aralıklar ya da çok küçük delikler her üreticide yapılamaz ya da ek maliyet getirir. Tasarım kuralları, kartın üretileceği yerin kabiliyetlerine göre ayarlanmalıdır.

### 12. Pedlerin üzerine taşan serigrafi ve okunmayan yazılar

Pedlerin üzerine taşan serigrafi lehimlemeyi bozar; çok küçük yazılar ise basılamaz. Referanslar okunabilir boyutta ve pedlerden uzak olmalıdır.

### 13. Dizgi için gerekenlerin unutulması

Otomatik dizgi için referans işaretleri (fiducial), kart kenarına yeterli mesafe ve gerekiyorsa panel kenarları gerekir. Kenara çok yakın parçalar, panel ayırma sırasında zarar görebilir.

### 14. Test ve programlama erişiminin olmaması

Programlama konnektörü (ör. SWD) ve önemli sinyallerde test noktaları yoksa, kart üretildikten sonra hata ayıklamak ve üretim testi yapmak çok zorlaşır.

## Üretim dosyalarında

### 15. Dosyalar arasındaki uyumsuzluklar

Malzeme listesindeki referansların PCB ile eşleşmemesi, takılmayacak parçaların işaretlenmemesi, dizgi dosyasındaki hatalı açılar ve farklı revizyonlara ait dosyaların karışması, doğru tasarlanmış bir kartı bile hatalı üretir. Hangi dosyaların gerektiğini [PCB üretimi için gerekli dosyalar](/blog/pcb-uretimi-icin-gerekli-dosyalar.html) yazımızda anlattık.

## İnceleme nasıl yapılmalı?

1. İncelemeyi bir kontrol listesiyle ve sabit bir sırayla yapın: şematik, ayak izleri, yerleşim, üretilebilirlik, dosyalar.
2. Her bulguyu kaydedin ve önem derecesi verin: üretimi durduran, düzeltilmesi gereken, iyileştirme önerisi.
3. Düzeltmelerden sonra yalnızca değişen yerleri değil, onlardan etkilenebilecek bölümleri de yeniden kontrol edin.
4. Mümkünse incelemeyi tasarımı yapmamış biri yapsın; tasarımcı kendi varsayımlarını görmekte zorlanır.

## Sonuç

Üretim öncesi inceleme, bir prototip turunun maliyetinin küçük bir kısmına mal olur ve çoğu zaman o turu tamamen gereksiz kılar.

[Tasarım incelemesi](/tasarim-incelemesi.html) hizmetimizde şematik ve PCB dosyalarınızı üretime göndermeden önce inceliyor, bulguları önem sırasına göre raporluyoruz. Kartınızın sıfırdan tasarlanmasını isterseniz [elektronik kart tasarımı](/elektronik-kart-tasarimi.html) sayfamıza göz atabilirsiniz.
""",
    ),
    dict(
        slug="prototip-pcb-maliyetini-dusurme",
        baslik="Prototip PCB maliyetini düşürmenin 9 yolu",
        title="Prototip PCB Maliyetini Düşürmenin 9 Yolu | ModWare",
        kategori="PCB üretimi",
        ikon="layers",
        desc="Prototip PCB maliyetini ne belirler? Standart değerler, katman sayısı, kart boyutu, yüzey kaplama, parça listesi ve revizyonlarla bütçeyi küçültmenin yolları.",
        ozet="Standart üretim değerleri, kart boyutu, yüzey kaplama, parça listesi ve revizyon sayısı: prototip bütçesini küçültmenin pratik yolları.",
        lede="Prototip aşamasında bütçeyi zorlayan çoğu zaman tek bir kalem değil, küçük kararların toplamıdır. Tasarımın başında alınan birkaç doğru kararla aynı kartı belirgin biçimde daha ucuza ve daha hızlı üretebilirsiniz.",
        ilgili=["pcb-uretimi", "tasarim-incelemesi", "prototip-ar-ge"],
        diger=["pcb-uretimi-icin-gerekli-dosyalar", "pcb-tasarim-incelemesi-sik-yapilan-hatalar", "elektronik-kart-tasarim-sureci"],
        cta="PCB'nizi birlikte üretelim.",
        urun="PCB üretimi",
        govde="""
Bir PCB'nin fiyatı; kart alanı, katman sayısı, malzeme, üretim toleransları, yüzey kaplama, özel işlemler, adet ve teslim süresinin birleşiminden oluşur. Kart dizgiye de gidecekse parça sayısı, parçaların bulunabilirliği ve montajın karmaşıklığı da hesaba girer. Aşağıdaki maddeler, kaliteden ve güvenilirlikten ödün vermeden maliyeti düşürmenin en etkili yollarını özetliyor.

> **Kısaca:** Standart üretim değerlerinde kalın, özel işlemlere yalnızca gerçekten gerektiğinde başvurun, parça listesini sadeleştirin ve en önemlisi revizyon sayısını azaltın.

## 1. Standart üretim değerlerinde kalın

Üreticiler belirli değerleri standart kabul eder ve en uygun fiyatı bu değerlerde verir: 1,6 mm FR-4, 35 µm (1 oz) bakır, yeşil lehim maskesi, beyaz serigrafi ve üreticinin standart kabiliyetleri içinde kalan yol genişlikleri, aralıklar ve delik çapları. Bu değerlerin dışına çıkmak hem fiyatı hem de teslim süresini artırır. Gerekmedikçe çok ince yollar ve küçük via'lar yerine standart değerleri tercih edin.

## 2. Katman sayısını ihtiyaca göre seçin

Katman sayısı arttıkça birim fiyat artar; ama daha az katman her zaman daha ucuz değildir. Yoğun bir devreyi az katmana sığdırmaya çalışmak kartı büyütebilir, EMC sorunlarına yol açabilir ve ek bir prototip turu gerektirebilir. Doğru seçim; devrenin yoğunluğu, akım ve gürültü gereksinimiyle birlikte toplam maliyete bakılarak yapılır.

## 3. Kart boyutunu küçültün, paneli verimli kullanın

Fiyat büyük ölçüde kart alanına bağlıdır. Gereksiz boşlukları kaldırmak ve dikdörtgen formlar kullanmak alanı azaltır. Birden fazla küçük kart aynı panelde üretilebilir; dizgide kartları panel hâlinde işlemek de montajı hızlandırır.

## 4. Yüzey kaplamayı işe göre seçin

HASL genellikle en ekonomik seçenektir. İnce adımlı entegreler ile QFN ve BGA gibi düz yüzey isteyen paketlerde ise ENIG, daha pahalı olsa da lehimleme hatalarını azaltır. Kaplamayı kartın gerçek ihtiyacına göre seçmek, gereksiz maliyetten de dizgi hatalarından da korur.

## 5. Özel işlemlerden gerekmedikçe kaçının

Kör ve gömülü via'lar, ped içinde via (via-in-pad) doldurma, empedans kontrolü, yarım delikli (castellated) kenarlar ve kalın bakır gibi işlemler maliyeti belirgin biçimde artırır. Bunlar bazı tasarımlarda gerçekten gereklidir; gerekmediği yerde kullanıldıklarında ise yalnızca fiyatı yükseltirler.

## 6. Parça listesini sadeleştirin

Prototip dizgisinde maliyeti çoğu zaman parça adedinden çok **farklı parça çeşidi** sayısı belirler. Örneğin 10 kΩ, 9,1 kΩ ve 11 kΩ yerine, devrenin izin verdiği yerlerde tek bir değer kullanmak malzeme listesindeki satır sayısını azaltır.

- Birden fazla distribütörde stokta bulunan, yaygın parçaları tercih edin.
- Üretimi durdurulmuş ya da uzun teslim süreli parçalardan kaçının.
- Pasif parçalarda tek bir paket boyutunda (ör. 0603) kalmaya çalışın.

## 7. Parçaları mümkünse tek yüze yerleştirin

Parçaların iki yüze dağılması dizgide ikinci bir geçiş, ek şablon ve ek iş demektir. Yer izin veriyorsa SMD parçaları kartın tek yüzünde toplamak montaj maliyetini düşürür.

## 8. Adet ve teslim süresini planlayın

Birim fiyat adetle birlikte düşer; ilk prototipte 5–10 adet çoğu zaman en dengeli seçimdir. Ekspres üretim ise ciddi bir ek maliyet getirir. Takvimi baştan planlamak, aceleye gelen ve pahalıya mal olan siparişleri önler.

## 9. Revizyon sayısını azaltın

En pahalı prototip, yeniden yapılması gerekendir. Her yeni tur; kart, parça, dizgi, kargo ve en önemlisi zaman demektir. Üretimden önce bir [tasarım incelemesi](/tasarim-incelemesi.html) yapmak, test noktaları ve programlama konnektörü eklemek ve ayar gerektirebilecek yerlere takılmadan bırakılabilen parça yerleri koymak, bir sonraki turu çoğu zaman gereksiz kılar.

## Hangi karar maliyeti nasıl etkiler?

| Karar | Maliyete etkisi | Ne zaman tercih edilmeli? |
|---|---|---|
| Standart kalınlık ve bakır | Düşük maliyet, kısa teslim | Özel bir gereksinim yoksa her zaman |
| Daha fazla katman | Birim fiyat artar | Yoğun devre, hızlı sinyal, EMC gereksinimi |
| ENIG kaplama | Orta düzeyde artış | İnce adımlı ve düz yüzey isteyen paketler |
| Ped içinde via, kör via | Belirgin artış | Çok yoğun ve ince adımlı tasarımlar |
| Tek yüze dizgi | Montajda tasarruf | Yer izin veriyorsa |
| Ekspres üretim | Belirgin artış | Gerçekten acil durumlar |

## Sonuç

Prototip maliyetini düşürmenin en etkili yolu, ucuz seçenekleri körü körüne seçmek değil; gereksiz özel işlemlerden kaçınıp revizyon sayısını azaltmaktır. Doğru kararlar hem bugünkü prototipi hem de yarınki seri üretimi ucuzlatır.

[PCB üretimi](/pcb-uretimi.html) hizmetimizde dosyalarınızı üretimden önce kontrol ediyor, işe ve bütçeye uygun üretim seçeneklerini birlikte belirliyoruz. Ürününüzü fikir aşamasından itibaren planlamak isterseniz [prototip ve Ar-Ge](/prototip-ar-ge.html) sayfamıza göz atabilirsiniz.
""",
    ),
]
