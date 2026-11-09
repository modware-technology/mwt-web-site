/* =========================================================
   ModFlow sayfası (modflow.html) hareketleri
   1. Dağınık notlar: kaydırdıkça dağınıklıktan düzenli ızgaraya oturur (GSAP ScrollTrigger varsa)
   2. Akış çizgisi: bölüm ekrandan geçerken çizgi dolar, adımlar sırayla yanar (--mf-ilerleme)
   3. Komponent arama canlandırması: parça no yazılır, kaynaklar gelir, fiyatlar TL'ye döner,
      en uygun Türkiye ve yurt dışı kaynağı işaretlenir; ekrandayken döngüyle tekrarlanır
   "Hareketi azalt" tercihinde hiçbiri çalışmaz; içerik son hâliyle görünür.
   ========================================================= */
(function () {
  'use strict';

  const azalt = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const gsap = window.gsap;
  const st = gsap && window.ScrollTrigger;

  // ---------------------------------------------------------------- 2. akış çizgisi
  function akis() {
    const liste = document.querySelector('[data-mf-akis]');
    if (!liste) return;
    const adimlar = Array.from(liste.querySelectorAll('.mf-adim'));
    const ayarla = (p) => {
      liste.style.setProperty('--mf-ilerleme', p.toFixed(3));
      adimlar.forEach((a, i) => a.classList.toggle('yanik', p >= (i + 0.35) / adimlar.length));
    };
    if (azalt) { ayarla(1); return; }
    let bekliyor = false;
    const hesapla = () => {
      bekliyor = false;
      const r = liste.getBoundingClientRect();
      const vh = window.innerHeight;
      // Liste ekranın alt %85'ine girince başlar, üst %35'e gelince tamamlanır
      const bas = vh * 0.85;
      const bit = vh * 0.35 - r.height;
      const p = Math.min(1, Math.max(0, (bas - r.top) / (bas - bit)));
      ayarla(p);
    };
    const iste = () => { if (!bekliyor) { bekliyor = true; requestAnimationFrame(hesapla); } };
    window.addEventListener('scroll', iste, { passive: true });
    window.addEventListener('resize', iste);
    hesapla();
  }

  // ---------------------------------------------------------------- 1. dağınık notlar
  function daginik() {
    const kap = document.querySelector('[data-mf-daginik]');
    if (!kap || azalt || !st) return;
    const notlar = Array.from(kap.children);
    // Her not rastgele değil, sabit bir dağınıklıkla başlar (her ziyarette aynı görünüm)
    const dagit = [[-40, 50, -9], [30, -30, 7], [-20, -40, 5], [50, 40, -6], [-50, 20, 8], [20, 60, -5]];
    notlar.forEach((n, i) => {
      const [x, y, r] = dagit[i % dagit.length];
      gsap.fromTo(n, { x, y, rotation: r, opacity: 0.55 }, {
        x: 0, y: 0, rotation: 0, opacity: 1, ease: 'none',
        scrollTrigger: { trigger: kap, start: 'top 90%', end: 'top 35%', scrub: 0.6 },
      });
    });
  }

  // ---------------------------------------------------------------- 3. komponent arama
  function sahne() {
    const s = document.querySelector('[data-mf-sahne]');
    if (!s) return;
    const kartlar = Array.from(s.querySelectorAll('.mf-kaynak'));
    const yazi = s.querySelector('[data-mf-yazi]');
    const tam = yazi.textContent;
    const fiyat = (k) => Number(k.querySelector('.mf-k-fiyat b').textContent.replace(/[^\d,]/g, '').replace(',', '.'));
    const yerli = kartlar.filter((k) => k.querySelector('.mf-k-ad i'));
    const yd = kartlar.filter((k) => !k.querySelector('.mf-k-ad i'));
    const enUcuz = (l) => l.reduce((a, b) => (fiyat(b) < fiyat(a) ? b : a), l[0]);
    const isaretle = () => [enUcuz(yerli), enUcuz(yd)].forEach((k) => k && k.classList.add('en-uygun'));
    if (azalt) { isaretle(); return; }

    let gorunur = false;
    let calisiyor = false;
    const bekle = (ms) => new Promise((ok) => { setTimeout(ok, ms); });

    async function tur() {
      calisiyor = true;
      s.classList.add('mf-oynuyor');
      s.classList.remove('tl');
      kartlar.forEach((k) => k.classList.remove('gorunur', 'en-uygun'));
      yazi.textContent = '';
      for (let i = 1; i <= tam.length; i += 1) {
        yazi.textContent = tam.slice(0, i);
        await bekle(55);
      }
      await bekle(350);
      for (const k of kartlar) { k.classList.add('gorunur'); await bekle(320); }
      await bekle(500);
      s.classList.add('tl');
      await bekle(700);
      isaretle();
      await bekle(4200);
      calisiyor = false;
      if (gorunur) tur();
    }

    const io = new IntersectionObserver((girdiler) => {
      gorunur = girdiler[0].isIntersecting;
      if (gorunur && !calisiyor) tur();
    }, { threshold: 0.35 });
    io.observe(s);
  }

  function basla() { akis(); daginik(); sahne(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', basla);
  else basla();
}());
