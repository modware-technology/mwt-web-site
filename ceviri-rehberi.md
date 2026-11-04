# ModWare Technology web sitesi — İngilizce çeviri rehberi (EN)

All translators must follow this guide. Output language: **US English**. Tone: professional B2B engineering, plain and concise, same meaning as the Turkish source. Do not add claims, certifications, numbers, client names, a factory or facility that the Turkish text does not state. PCB manufacturing is offered as a managed service ("we take care of manufacturing, follow the process end to end and deliver your boards"); never name suppliers.

## Site paths (TR → EN)

All EN pages live under `/en/`. Internal links must be root-absolute.

| TR path | EN path | EN file |
|---|---|---|
| `/` | `/en/` | `en/index.html` |
| `/hizmetler` | `/en/services` | `en/services.html` (generated) |
| `/urunler` | `/en/products` | `en/products.html` |
| `/hakkimizda` | `/en/about` | `en/about.html` |
| `/teklif` | `/en/quote` | `en/quote.html` |
| `/elektronik-kart-tasarimi` | `/en/electronics-pcb-design` | generated |
| `/pcb-uretimi` | `/en/pcb-manufacturing` | generated |
| `/gomulu-yazilim` | `/en/embedded-software` | generated |
| `/tasarim-incelemesi` | `/en/design-review` | generated |
| `/prototip-ar-ge` | `/en/prototyping-rd` | generated |
| `/blog/` | `/en/blog/` | generated |
| `/blog/elektronik-kart-tasarim-sureci` | `/en/blog/electronics-design-process` | generated |
| `/blog/pcb-uretimi-icin-gerekli-dosyalar` | `/en/blog/pcb-manufacturing-files` | generated |
| `/blog/pcb-tasariminda-emc-kurallari` | `/en/blog/pcb-emc-design-rules` | generated |
| `/blog/stm32-modbus-rtu-rs485` | `/en/blog/stm32-modbus-rtu-rs485` | generated |
| `/blog/pcb-tasarim-incelemesi-sik-yapilan-hatalar` | `/en/blog/pcb-design-review-common-mistakes` | generated |
| `/blog/prototip-pcb-maliyetini-dusurme` | `/en/blog/reduce-prototype-pcb-cost` | generated |

- In Python data files (service pages, blog articles) write internal links as root-absolute with `.html`, e.g. `[PCB manufacturing](/en/pcb-manufacturing.html)`, `[design review checklist](/en/blog/pcb-design-review-common-mistakes.html)`. The generator turns them into clean URLs.
- In HTML pages write clean root-absolute links, e.g. `href="/en/services"`, `href="/en/quote?urun=MW-SPARK"`.
- Asset, style and script paths in EN HTML pages are root-absolute: `/assets/...`, `/css/style.css?v=31`, `/js/main.js?v=31`, `/js/animations.js?v=31`.

## Quote form values (`?urun=` and `urun=` fields)

Product codes (`MW-SPARK`, `MW-PRISM`, …) never change. Service values on the EN quote form:

| TR value | EN value |
|---|---|
| Özel donanım tasarımı | Custom hardware design |
| PCB tasarımı | PCB design |
| PCB üretimi | PCB manufacturing |
| Tasarım incelemesi | Design review |
| Gömülü yazılım | Embedded software |
| Üretim danışmanlığı | Manufacturing consulting |
| Diğer | Other |

## Names that never change

ModWare Technology, ModWare, product names (ModWare Spark, Axis, Sense, Aero, Link, Energy, Power), PRISM, GUARD, SHIFT 24 / SHIFT 12, PURE 5, PILOT, product codes (MW-…), TEKNOFEST, STM32, LoRa, Modbus RTU, RS-485, KiCad, part numbers. Place names keep Turkish letters: **İzmit, Kocaeli, Türkiye** (use "Türkiye", not "Turkey").

Where the Turkish text says the company serves "Türkiye geneline" (all of Türkiye), write "for clients in Türkiye and abroad" — an offer, not a claim of existing foreign clients. TEKNOFEST may get a short explanation on first use: "TEKNOFEST, Türkiye's largest technology festival".

## Glossary

| Turkish | English |
|---|---|
| elektronik kart | electronic board, circuit board |
| elektronik kart tasarımı | electronic board design, electronics design |
| donanım tasarımı | hardware design |
| PCB tasarımı / üretimi | PCB design / PCB manufacturing |
| dizgi, montaj | assembly (PCBA) |
| dizgi dosyası (CPL) | pick-and-place file (CPL) |
| malzeme listesi (BOM) | bill of materials (BOM) |
| delik dosyası | drill file |
| gömülü yazılım | embedded software (firmware where it fits) |
| tasarım incelemesi | design review |
| prototip ve Ar-Ge | prototyping and R&D |
| şematik | schematic |
| yerleşim | layout, placement |
| iz | trace |
| bakır döküm | copper pour |
| katman yapısı | layer stackup |
| yüzey kaplama | surface finish |
| toprak düzlemi | ground plane |
| sinyal bütünlüğü | signal integrity |
| ped | pad |
| lehim | solder |
| güç kartı | power board |
| ters kutup koruması | reverse-polarity protection |
| aşırı gerilim / kısa devre | overvoltage / short circuit |
| sahaya dayanıklı | field-ready, rugged |
| keşif / kapsam | discovery / scope |
| teslimatlar | deliverables |
| süreç | process |
| sık sorulanlar | FAQ, frequently asked questions |
| Teklif Al / Teklif iste | Get a Quote / Request a quote |
| Hizmetler / Ürünler / Hakkımızda / Ana Sayfa | Services / Products / About / Home |
| Hizmeti inceleyin | Learn more |
| Ürünleri inceleyin | Explore products |
| Yazıyı okuyun | Read the article |
| dk okuma | min read |

## Formatting

- Decimal point, thousands comma: `0,5 mm` → `0.5 mm`, `1.000+` → `1,000+`, `%10` → `10%`.
- Units with a space: `12 V`, `5 A`, `100 nF`, `25 °C`; ranges with an en dash: `12–48 V`.
- Dates: `26 Ekim 2026` → `October 26, 2026`.
- Headings (h1–h3, page titles, card titles): write them in sentence case; the generator converts them to Title Case. Keep acronyms as they are.
- Keep Markdown markers, HTML structure, classes, ids, `data-*` attributes and JSON keys exactly; translate only human-visible text, `aria-label`, `alt`, `title`, `placeholder` and meta text.
- HTML comments may stay in Turkish. **Never change the marker comments** `<!-- Sekme ikonu -->`, `<!-- ============ PRELOADER ============ -->`, `<!-- ============ ORTAK ÜST MENÜ ============`, `<!-- ============ ORTAK ALT BİLGİ ============ -->`; the generator uses them.

## Shared header and footer (EN HTML pages)

Use exactly this navigation (the generator adds the TR/EN language switch itself):

```html
      <a class="logo" href="/en/" aria-label="ModWare Technology home">
        <img src="/assets/logo/modware-logo-light.png" alt="ModWare" width="275" height="30">
      </a>

      <!-- Mobilde menüyü açıp kapatan buton -->
      <button class="nav-toggle" id="nav-toggle" type="button"
              aria-controls="site-nav" aria-expanded="false" aria-label="Open menu">
        <span class="nav-toggle-bar"></span>
        <span class="nav-toggle-bar"></span>
        <span class="nav-toggle-bar"></span>
      </button>

      <nav class="site-nav" id="site-nav" aria-label="Main menu">
        <ul class="nav-list">
          <li><a class="nav-link" href="/en/" data-nav="home">Home</a></li>
          <li><a class="nav-link" href="/en/services" data-nav="hizmetler">Services</a></li>
          <li><a class="nav-link" href="/en/products" data-nav="urunler">Products</a></li>
          <li><a class="nav-link" href="/en/about" data-nav="hakkimizda">About</a></li>
          <li><a class="nav-link" href="/en/blog/" data-nav="blog">Blog</a></li>
        </ul>
        <a class="btn btn-accent nav-cta" href="/en/quote">Get a Quote</a>
      </nav>
```

Footer: logo link `/en/`; `footer-location` stays "İzmit, Kocaeli"; e-mail icon `aria-label="Send us an e-mail: info@modwaretechnology.com"`; LinkedIn icon `aria-label="ModWare Technology on LinkedIn (opens in a new tab)"`; back-to-top button `aria-label="Back to top"`. Keep `<body data-page="…">` values as in the Turkish page (they are internal keys).
