/* =========================================================
   ModWare Technology — ortak davranışlar
   - Aktif menü bağlantısını işaretleme
   - Mobil menü aç/kapa (tam ekran overlay, linkler sırayla gelir)
   - Kaydırınca menü görünümünü değiştirme
   - Kart parıltısı (fare konumu)
   - Görseller: lazy-load sonrası belirme
   - Yukarı çık butonu
   - Alt bilgideki yılı güncelleme
   GSAP varsa (CDN'den bu dosyadan önce yüklenir) menü animasyonunda
   kullanılır; yoksa her şey CSS geçişleriyle çalışır.
   ========================================================= */

(function () {
  'use strict';

  const header = document.getElementById('site-header');
  const toggle = document.getElementById('nav-toggle');
  const nav = document.getElementById('site-nav');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const gsap = window.gsap;

  /* ---------- Aktif sayfa ----------
     <body data-page="urunler"> ile eşleşen menü bağlantısına
     aria-current="page" eklenir; stil CSS'te bu özelliğe bağlıdır. */
  const currentPage = document.body.dataset.page;
  document.querySelectorAll('[data-nav]').forEach((link) => {
    if (link.dataset.nav === currentPage) {
      link.setAttribute('aria-current', 'page');
    }
  });

  /* ---------- Mobil menü ---------- */
  const navItems = nav ? nav.querySelectorAll('.nav-list li, .nav-cta') : [];

  function setMenu(open) {
    const wasOpen = nav.classList.contains('is-open');
    if (open === wasOpen) return;

    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Menüyü kapat' : 'Menüyü aç');

    // Lenis (yumuşak kaydırma, animations.js) varsa menü açıkken sayfayı kaydırmasın
    if (window.lenis) {
      if (open) window.lenis.stop(); else window.lenis.start();
    }

    // Linkler alttan sırayla gelsin (yalnızca mobil overlay görünürken)
    const isOverlay = window.matchMedia('(max-width: 960px)').matches;
    if (gsap && isOverlay && !reduceMotion) {
      gsap.killTweensOf(navItems);
      if (open) {
        gsap.fromTo(navItems,
          { y: 40, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.6, stagger: 0.07, delay: 0.08, ease: 'power3.out' });
      } else {
        gsap.set(navItems, { clearProps: 'transform,opacity' });
      }
    }
  }

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });

    // Menüdeki bir bağlantıya tıklanınca menüyü kapat
    nav.addEventListener('click', (e) => {
      if (e.target.closest('a')) setMenu(false);
    });

    // Escape tuşuyla kapat ve odağı butona geri ver
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        setMenu(false);
        toggle.focus();
      }
    });

    // Masaüstü genişliğine dönülürse açık kalan mobil menüyü sıfırla
    window.matchMedia('(min-width: 961px)').addEventListener('change', (e) => {
      if (e.matches) setMenu(false);
    });
  }

  /* ---------- Kaydırınca menü ----------
     Sayfa birkaç piksel kaydırıldığında .is-scrolled eklenir. */
  if (header) {
    const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Fareyi takip eden kart parıltısı ----------
     [data-glow] kartlarına fare konumu --mx / --my olarak verilir;
     parıltının kendisi CSS'te (.value-card::before). */
  document.querySelectorAll('[data-glow]').forEach((card) => {
    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });

  /* ---------- Görseller: lazy-load + belirme ----------
     loading="lazy" görseller yüklenince yumuşakça belirir. Sınıfı JS eklediği
     için JS çalışmazsa görseller zaten görünür kalır. */
  document.querySelectorAll('img[loading="lazy"]').forEach((img) => {
    if (img.complete && img.naturalWidth) return; // zaten yüklenmiş
    img.classList.add('lazy-fade');
    const done = () => img.classList.add('is-loaded');
    img.addEventListener('load', done, { once: true });
    img.addEventListener('error', done, { once: true });
  });

  /* ---------- Yukarı çık butonu ----------
     Sayfanın sonuna yaklaşınca (son ~%60 ekran boyu) belirir.
     Tıklanınca Lenis varsa onunla, yoksa tarayıcının kaydırmasıyla yukarı çıkar. */
  const toTop = document.getElementById('to-top');
  if (toTop) {
    const update = () => {
      const doc = document.documentElement;
      const remaining = doc.scrollHeight - (window.scrollY + window.innerHeight);
      const show = window.scrollY > window.innerHeight * 0.8 && remaining < window.innerHeight * 0.6;
      toTop.classList.toggle('is-visible', show);
    };
    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);

    toTop.addEventListener('click', () => {
      if (window.lenis) {
        window.lenis.scrollTo(0, { duration: 1.6 });
      } else {
        window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
      }
      // Odağı sayfanın başına taşı (klavye kullanıcıları için)
      const skip = document.querySelector('.skip-link');
      if (skip) skip.focus({ preventScroll: true });
    });
  }

  /* =========================================================
     Ürünler sayfası: kategori filtresi + detay penceresi
     Yalnızca #product-grid bulunan sayfada çalışır.
     ========================================================= */
  const grid = document.getElementById('product-grid');
  const modal = document.getElementById('product-modal');
  const dataEl = document.getElementById('product-data');

  if (grid) {
    const cards = Array.from(grid.querySelectorAll('.product-card'));
    const chips = Array.from(document.querySelectorAll('.filter-chip'));
    const empty = document.getElementById('product-empty');

    /* ----- Kategori filtresi ----- */
    function applyFilter(cat) {
      chips.forEach((c) => c.setAttribute('aria-pressed', String(c.dataset.filter === cat)));
      const show = cards.filter((c) => cat === 'all' || c.dataset.category === cat);
      const hide = cards.filter((c) => !show.includes(c));
      empty.hidden = show.length > 0;

      const refresh = () => { if (window.ScrollTrigger) window.ScrollTrigger.refresh(); };
      if (gsap && !reduceMotion) {
        // Önce eşleşmeyenler söner, sonra eşleşenler alttan sırayla gelir
        const reveal = () => {
          hide.forEach((c) => { c.hidden = true; });
          show.forEach((c) => { c.hidden = false; });
          gsap.fromTo(show, { opacity: 0, y: 24, scale: 1 }, {
            opacity: 1, y: 0, duration: 0.5, stagger: 0.05, ease: 'power3.out',
            clearProps: 'transform,opacity', onComplete: refresh,
          });
        };
        const toHide = hide.filter((c) => !c.hidden);
        if (toHide.length) {
          gsap.to(toHide, { opacity: 0, scale: 0.96, duration: 0.25, ease: 'power2.in', onComplete: reveal });
        } else {
          reveal();
        }
      } else {
        cards.forEach((c) => { c.hidden = !show.includes(c); });
        refresh();
      }
    }
    chips.forEach((chip) => chip.addEventListener('click', () => applyFilter(chip.dataset.filter)));

    // "Güç modüllerini göster" gibi butonlar: filtreyi uygula ve galeriye kay
    document.querySelectorAll('[data-filter-jump]').forEach((btn) => {
      btn.addEventListener('click', () => {
        applyFilter(btn.dataset.filterJump);
        const target = document.querySelector('.product-filters') || grid;
        const offset = -(header ? header.offsetHeight : 0) - 24;
        if (window.lenis) window.lenis.scrollTo(target, { offset });
        else window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY + offset, behavior: reduceMotion ? 'auto' : 'smooth' });
      });
    });

    /* ----- Detay penceresi ----- */
    if (modal && dataEl && typeof modal.showModal === 'function') {
      const products = JSON.parse(dataEl.textContent);
      const inner = modal.querySelector('.pm-inner');
      const img = modal.querySelector('#pm-img');
      const thumbs = modal.querySelector('#pm-thumbs');
      const field = (id) => modal.querySelector(`#${id}`);
      let lastTrigger = null;
      let closing = false;

      function setImage(src, alt) {
        if (gsap && !reduceMotion && img.getAttribute('src')) {
          gsap.fromTo(img, { opacity: 0, scale: 0.97 }, { opacity: 1, scale: 1, duration: 0.4, ease: 'power2.out' });
        }
        img.src = src;
        img.alt = alt;
      }

      function fill(p) {
        field('pm-code').textContent = p.code;
        field('pm-title').textContent = p.title;
        field('pm-slogan').textContent = p.slogan;
        field('pm-long').textContent = p.long;

        const specs = field('pm-specs');
        specs.innerHTML = '';
        p.specs.forEach(([k, v]) => {
          const row = document.createElement('div');
          const dt = document.createElement('dt');
          const dd = document.createElement('dd');
          dt.textContent = k;
          dd.textContent = v;
          row.append(dt, dd);
          specs.appendChild(row);
        });

        const tags = field('pm-tags');
        tags.innerHTML = '';
        p.tags.forEach((t) => {
          const li = document.createElement('li');
          li.textContent = t;
          tags.appendChild(li);
        });

        field('pm-note').hidden = !p.platform;
        field('pm-quote').href = `teklif.html?urun=${encodeURIComponent(p.code)}`; // formda ürün seçili gelir

        // Görseller: ikinci görsel varsa küçük resimlerle seçilebilir
        img.removeAttribute('src');
        const images = [p.img, p.img2].filter(Boolean).map((f) => `assets/urunler/${f}`);
        setImage(images[0], `${p.title} kartı`);
        thumbs.innerHTML = '';
        thumbs.hidden = images.length < 2;
        if (images.length > 1) {
          images.forEach((src, n) => {
            const b = document.createElement('button');
            b.type = 'button';
            b.className = 'pm-thumb';
            b.setAttribute('aria-label', `${n + 1}. görsel`);
            b.setAttribute('aria-pressed', String(n === 0));
            const t = document.createElement('img');
            t.src = src;
            t.alt = '';
            b.appendChild(t);
            b.addEventListener('click', () => {
              thumbs.querySelectorAll('.pm-thumb').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
              setImage(src, `${p.title} kartı, ${n + 1}. görsel`);
            });
            thumbs.appendChild(b);
          });
        }
      }

      function openProduct(id, trigger) {
        const p = products[id];
        if (!p) return;
        lastTrigger = trigger || null;
        fill(p);
        modal.showModal();
        document.documentElement.classList.add('modal-open');
        if (window.lenis) window.lenis.stop();
        if (gsap && !reduceMotion) {
          gsap.fromTo(inner,
            { opacity: 0, scale: 0.92, y: 24 },
            { opacity: 1, scale: 1, y: 0, duration: 0.55, ease: 'power3.out' });
          gsap.fromTo(inner.querySelectorAll('.pm-content > *'),
            { opacity: 0, y: 14 },
            { opacity: 1, y: 0, duration: 0.45, stagger: 0.04, delay: 0.12, ease: 'power2.out' });
        }
        inner.scrollTop = 0;
        history.replaceState(null, '', `#${id}`); // paylaşılabilir bağlantı: urunler.html#pwr-bk
      }

      function closeProduct() {
        if (!modal.open || closing) return;
        closing = true;
        const done = () => {
          modal.classList.remove('is-closing');
          modal.close();
          closing = false;
        };
        modal.classList.add('is-closing');
        if (gsap && !reduceMotion) {
          gsap.to(inner, { opacity: 0, scale: 0.95, y: 12, duration: 0.28, ease: 'power2.in', onComplete: done });
        } else {
          done();
        }
      }

      modal.addEventListener('close', () => {
        document.documentElement.classList.remove('modal-open');
        if (window.lenis) window.lenis.start();
        if (gsap) gsap.set(inner, { clearProps: 'transform,opacity' });
        history.replaceState(null, '', window.location.pathname + window.location.search);
        if (lastTrigger) lastTrigger.focus({ preventScroll: true });
      });
      // Escape: animasyonlu kapat
      modal.addEventListener('cancel', (e) => { e.preventDefault(); closeProduct(); });
      // Kapat butonları ve pencerenin dışına (arka plana) tıklama
      modal.addEventListener('click', (e) => {
        if (e.target === modal || e.target.closest('[data-pm-close]')) closeProduct();
      });

      // Kartın herhangi bir yerine tıklanınca aç (metin seçimi hariç)
      cards.forEach((card) => {
        card.addEventListener('click', () => {
          if (String(window.getSelection()).length) return;
          openProduct(card.dataset.product, card.querySelector('.product-more'));
        });
      });

      // urunler.html#pwr-bk gibi bir bağlantıyla gelindiyse o ürünü aç
      const initial = window.location.hash.slice(1);
      if (initial && products[initial]) {
        const card = grid.querySelector(`[data-product="${initial}"]`);
        // Preloader perdesi kalkana kadar bekle (pencere onun üstünde açılmasın)
        const tryOpen = () => {
          if (document.documentElement.classList.contains('is-loading')) { setTimeout(tryOpen, 150); return; }
          openProduct(initial, card && card.querySelector('.product-more'));
        };
        setTimeout(tryOpen, 300);
      }
    }
  }

  /* =========================================================
     Teklif formu (teklif.html)
     - ?urun=MW-PWR-BK ile gelinirse ürün seçili gelir
     - Konu "Teklif / proje" değilse ürün seçimi opsiyonel olur
     - Zorunlu alanlar doldukça ilerleme çubuğu dolar
     - Alan altında Türkçe hata mesajları
     - Netlify Forms'a gönderir; başarılıysa teşekkür ekranı
     ========================================================= */
  const quote = document.getElementById('quote-form');
  if (quote) {
    const $ = (id) => document.getElementById(id);
    const product = $('q-product');
    const msg = $('q-msg');
    const name = $('q-name');
    const email = $('q-email');
    const ref = $('q-ref');
    const consent = $('q-consent');
    const status = $('quote-status');
    const submit = quote.querySelector('.quote-submit');
    const submitLabel = quote.querySelector('.quote-submit-label');
    let tried = false; // ilk gönderim denemesinden sonra alanlar anında doğrulanır

    // Ürün ön seçimi (ürün penceresindeki "Teklif Al" bağlantısından)
    const pre = new URLSearchParams(window.location.search).get('urun');
    if (pre && Array.from(product.options).some((o) => o.value === pre)) product.value = pre;

    // Konu: yalnızca "Teklif / proje" seçiliyken ürün/hizmet zorunlu
    const topics = Array.from(quote.querySelectorAll('input[name="konu"]'));
    const isQuote = () => {
      const t = topics.find((r) => r.checked);
      return !t || t.value === 'Teklif / proje';
    };
    function syncTopic() {
      const need = isQuote();
      product.required = need;
      $('q-product-star').hidden = !need;
      $('q-product-opt').hidden = need;
    }

    // Kurallar: [alan, hata kutusu, kontrol → hata metni ya da '']
    const rules = [
      [product, 'q-product-error', () => (!isQuote() || product.value ? '' : 'Lütfen bir ürün veya hizmet seçin.')],
      [msg, 'q-msg-error', () => {
        const n = msg.value.trim().length;
        if (!n) return 'Lütfen projenizi kısaca anlatın.';
        return n < 20 ? `Biraz daha ayrıntı yazın (en az 20 karakter, şu an ${n}).` : '';
      }],
      [name, 'q-name-error', () => (name.value.trim().length >= 2 ? '' : 'Lütfen adınızı ve soyadınızı yazın.')],
      [email, 'q-email-error', () => {
        const v = email.value.trim();
        if (!v) return 'Lütfen e-posta adresinizi yazın.';
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : 'E-posta adresi geçerli görünmüyor (ör. ad@firma.com).';
      }],
      [consent, 'q-consent-error', () => (consent.checked ? '' : 'Devam etmek için onay kutusunu işaretleyin.')],
    ];
    // Opsiyonel ama doldurulduysa geçerli olmalı
    const optional = [
      [ref, 'q-ref-error', () => (!ref.value.trim() || /^https?:\/\/\S+\.\S+/.test(ref.value.trim()) ? '' : 'Bağlantı https:// ile başlamalı.')],
    ];

    function check([el, errId, test], show) {
      const error = test();
      const box = el.closest('.field') || el.closest('.check');
      if (show) {
        $(errId).textContent = error;
        if (box) box.classList.toggle('is-invalid', !!error);
        el.setAttribute('aria-invalid', String(!!error));
        el.setAttribute('aria-describedby', errId);
      }
      return !error;
    }

    function updateProgress() {
      const done = rules.filter((r) => check(r, false)).length;
      $('quote-progress-bar').style.transform = `scaleX(${done / rules.length})`;
      $('quote-progress-text').textContent = `Zorunlu alanlar: ${done} / ${rules.length}`;
    }

    // Karakter sayacı
    const count = $('q-count');
    const updateCount = () => { count.textContent = `${msg.value.length} / 800`; };

    [...rules, ...optional].forEach((r) => {
      const [el] = r;
      const evt = el.type === 'checkbox' || el.tagName === 'SELECT' ? 'change' : 'input';
      el.addEventListener(evt, () => { updateProgress(); if (tried) check(r, true); });
      el.addEventListener('blur', () => { if (tried || el.value) check(r, true); });
    });
    msg.addEventListener('input', updateCount);
    topics.forEach((r) => r.addEventListener('change', () => {
      syncTopic();
      updateProgress();
      if (tried) check(rules[0], true);
    }));
    syncTopic();
    updateCount();
    updateProgress();

    quote.addEventListener('submit', async (e) => {
      e.preventDefault();
      tried = true;
      const results = [...rules, ...optional].map((r) => [r[0], check(r, true)]);
      const firstBad = results.find(([, ok]) => !ok);
      if (firstBad) {
        status.className = 'quote-status is-error';
        status.textContent = 'Lütfen işaretli alanları kontrol edin.';
        firstBad[0].focus();
        return;
      }

      submit.disabled = true;
      submitLabel.textContent = 'Gönderiliyor…';
      status.className = 'quote-status';
      status.textContent = '';

      try {
        const res = await fetch('/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams(new FormData(quote)).toString(),
        });
        if (!res.ok) throw new Error(String(res.status));

        // Başarılı: formun yerine teşekkür ekranı
        const success = $('quote-success');
        $('quote-success-email').textContent = email.value.trim();
        quote.hidden = true;
        success.hidden = false;
        if (gsap && !reduceMotion) gsap.from(success, { opacity: 0, y: 24, duration: 0.6, ease: 'power3.out' });
        success.focus({ preventScroll: true });
        const offset = -(header ? header.offsetHeight : 0) - 24;
        if (window.lenis) window.lenis.scrollTo(success, { offset });
        else success.scrollIntoView({ block: 'start' });
        if (window.ScrollTrigger) window.ScrollTrigger.refresh();
      } catch (err) {
        status.className = 'quote-status is-error';
        status.textContent = 'Form şu an gönderilemedi. Lütfen info@modwaretechnology.com adresine e-posta gönderin.';
        submit.disabled = false;
        submitLabel.textContent = 'Teklif iste';
      }
    });
  }

  /* ---------- Kopyala butonları ([data-copy]) ---------- */
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    const label = btn.textContent;
    btn.addEventListener('click', () => {
      const text = btn.dataset.copy;
      const done = (ok) => {
        btn.textContent = ok ? 'Kopyalandı' : 'Seçildi';
        setTimeout(() => { btn.textContent = label; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => done(true)).catch(() => { selectNear(btn); done(false); });
      } else {
        selectNear(btn);
        done(false);
      }
    });
  });
  // Kopyalama engellenirse yanındaki metni seç (kullanıcı Ctrl+C yapabilsin)
  function selectNear(btn) {
    const el = btn.previousElementSibling;
    if (!el) return;
    const range = document.createRange();
    range.selectNodeContents(el);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }

  /* ---------- Alt bilgi yılı ---------- */
  document.querySelectorAll('[data-year]').forEach((el) => {
    el.textContent = new Date().getFullYear();
  });
})();
