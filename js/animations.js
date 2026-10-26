/* =========================================================
   ModWare Technology — animasyonlar (GSAP 3 + ScrollTrigger)

   İçindekiler
   0. Yardımcılar (SVG oluşturma, harf bölme, çizgi çizdirme)
   1. Hero görselleri: chip / schematic / modules (SVG, JS ile çizilir)
   2. Hero arka planı: devre izleri canvas'ı
   3. Hero slaytı: geçişler, otomatik oynatma, kontroller
   4. Nasıl çalışıyoruz: aşamalar sırayla belirir
   5. Bölüm başlıkları, kartlar ve kapanış girişleri
   6. Hero'su olmayan sayfalar için basit giriş
   7. Yumuşak kaydırma (Lenis)
   8. Preloader
   9. Özel imleç
   10. Arka plan katmanı
   11. Değer kartları: hover (ikon dönüşü, kalkma, 3D eğim)
   12. Manyetik butonlar + parçacık patlaması
   13. Kaydırma göstergeleri (üst çubuk, footer çizgisi)
   14. Sayfa geçişi
   15. Hakkımızda sayfası

   Kurallar
   - İçerik varsayılan olarak görünür. GSAP yüklenmezse görseller
     statik çizilir, ilk slayt görünür, kart tek kare olarak durur.
   - "Hareketi azalt" tercihinde otomatik hareket yok; slaytlar elle
     değişir, kart patlatma yerine sabit kare gösterilir.
   ========================================================= */

(function () {
  'use strict';

  const SVG_NS = 'http://www.w3.org/2000/svg';
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const gsap = window.gsap;
  const hasGsap = typeof gsap !== 'undefined';
  const hasScrollTrigger = hasGsap && typeof window.ScrollTrigger !== 'undefined';
  if (hasScrollTrigger) gsap.registerPlugin(window.ScrollTrigger);

  /* =======================================================
     0. Yardımcılar
     ======================================================= */

  // SVG elemanı oluştur, özelliklerini ver, isteğe bağlı ebeveyne ekle
  function el(tag, attrs, parent) {
    const node = document.createElementNS(SVG_NS, tag);
    Object.keys(attrs || {}).forEach((k) => node.setAttribute(k, attrs[k]));
    if (parent) parent.appendChild(node);
    return node;
  }

  // Her görsel için kök SVG + parıltı filtresi
  let uid = 0;
  function createSvg(host) {
    const id = `g${(uid += 1)}`;
    const svg = el('svg', { viewBox: '0 0 560 560', role: 'presentation' }, host);
    const defs = el('defs', {}, svg);
    const f = el('filter', { id: `glow-${id}`, x: '-100%', y: '-100%', width: '300%', height: '300%' }, defs);
    el('feGaussianBlur', { stdDeviation: '3.5', result: 'b' }, f);
    const m = el('feMerge', {}, f);
    el('feMergeNode', { in: 'b' }, m);
    el('feMergeNode', { in: 'SourceGraphic' }, m);
    return { svg, defs, id, glow: `url(#glow-${id})` };
  }

  // Çizgiyi "çizilecek" duruma getir (stroke-dasharray hilesi)
  function prepDraw(paths) {
    paths.forEach((p) => {
      const len = p.getTotalLength();
      p.style.strokeDasharray = `${len} ${len}`;
      p.style.strokeDashoffset = len;
    });
  }

  // Bir noktayı path boyunca hareket ettir (MotionPath eklentisi gerekmez)
  function travel(dot, path, opts) {
    const len = path.getTotalLength();
    const o = { t: opts.from == null ? 0 : opts.from };
    return gsap.to(o, {
      t: opts.to == null ? 1 : opts.to,
      duration: opts.duration || 1.2,
      ease: opts.ease || 'power1.inOut',
      onStart() { gsap.set(dot, { opacity: 1 }); },
      onUpdate() {
        const pt = path.getPointAtLength(o.t * len);
        dot.setAttribute('cx', pt.x);
        dot.setAttribute('cy', pt.y);
      },
      onComplete() {
        gsap.to(dot, { opacity: 0, duration: 0.2 });
        if (opts.onComplete) opts.onComplete();
      },
    });
  }

  // Başlığı kelime/harf span'lerine böl. .t-line satırları korunur.
  // Ekran okuyucular için tam metin aria-label olarak kalır.
  function splitChars(target) {
    if (target.dataset.splitDone) return Array.from(target.querySelectorAll('.split-char'));
    target.setAttribute('aria-label', target.textContent.replace(/\s+/g, ' ').trim());
    // Satır yoksa metni tek satıra sar (başlığın kendisi gizlenmesin diye)
    if (!target.querySelector('.t-line')) {
      const only = document.createElement('span');
      only.className = 't-line';
      only.textContent = target.textContent.trim();
      target.textContent = '';
      target.appendChild(only);
    }
    const lines = target.querySelectorAll('.t-line');
    const chars = [];

    lines.forEach((line) => {
      const words = line.textContent.trim().split(/\s+/);
      line.textContent = '';
      line.setAttribute('aria-hidden', 'true');
      words.forEach((word, wi) => {
        const w = document.createElement('span');
        w.className = 'split-word';
        Array.from(word).forEach((ch) => { // Array.from: Ü, İ, Ş tek karakter
          const c = document.createElement('span');
          c.className = 'split-char';
          c.textContent = ch;
          w.appendChild(c);
          chars.push(c);
        });
        line.appendChild(w);
        if (wi < words.length - 1) line.appendChild(document.createTextNode(' '));
      });
    });

    target.dataset.splitDone = '1';
    return chars;
  }

  /* =======================================================
     1. Hero görselleri
     Her biri { intro, start, stop } döndürür:
       intro → slayt açılınca bir kez oynayan timeline
       start/stop → sürekli tekrar eden hareketler (sinyal, LED…)
     ======================================================= */

  /* ----- 1a. "chip": ortada mikrodenetleyici, dört yönden izler,
             izlerden çipe akan sinyaller ----- */
  function buildChip(host) {
    const { svg, defs, id, glow } = createSvg(host);
    const C = 280;          // merkez
    const HALF = 90;        // çip yarı genişliği
    const PINS = 10;
    const PITCH = 15;
    const first = C - (PITCH * (PINS - 1)) / 2;

    const grad = el('radialGradient', { id: `die-${id}` }, defs);
    el('stop', { offset: '0%', 'stop-color': '#9b8fe0', 'stop-opacity': '0.55' }, grad);
    el('stop', { offset: '100%', 'stop-color': '#9b8fe0', 'stop-opacity': '0.05' }, grad);

    const ring = el('circle', { class: 'v-ring', cx: C, cy: C, r: 262 }, svg);

    const traces = [];
    const vias = [];
    const pins = [];
    const pulses = [];

    // Bir kenarı çiz, diğer üç kenar aynı grubun 90° döndürülmüş kopyası
    for (let side = 0; side < 4; side++) {
      const g = el('g', { transform: `rotate(${side * 90} ${C} ${C})` }, svg);
      for (let i = 0; i < PINS; i++) {
        const x = first + i * PITCH;
        const dx = (x - C) * 0.9;            // dışa doğru yelpaze
        const y0 = C - HALF - 14;            // pin ucu
        const y1 = 140;                      // 45° kırılım başlangıcı
        const yEnd = 34 + (i % 3) * 16;      // kademeli bitiş
        const p = el('path', {
          class: i % 4 === 1 ? 'v-trace-hot' : 'v-trace',
          d: `M${x} ${y0} V${y1} L${x + dx} ${y1 - Math.abs(dx)} V${yEnd}`,
        }, g);
        traces.push({ path: p, group: g });
        vias.push(el('circle', { class: 'v-via-blue', cx: x + dx, cy: yEnd, r: 4.5 }, g));
        pins.push(el('rect', { class: 'v-pin', x: x - 3, y: y0, width: 6, height: 14, rx: 1 }, g));
      }
      // Bu kenarın sinyal noktaları (aynı dönüşte olmalı)
      for (let k = 0; k < 3; k++) {
        pulses.push({ dot: el('circle', { class: 'v-pulse', r: 3.5, cx: -10, cy: -10, opacity: 0, filter: glow }, g), group: g });
      }
    }

    const body = el('rect', { class: 'v-chip', x: C - HALF, y: C - HALF, width: HALF * 2, height: HALF * 2, rx: 12 }, svg);
    el('circle', { cx: C - HALF + 16, cy: C - HALF + 16, r: 4, fill: '#2c3c66' }, svg);
    const die = el('rect', { x: C - 42, y: C - 42, width: 84, height: 84, rx: 8, fill: `url(#die-${id})` }, svg);
    const label = el('text', { class: 'v-label', x: C, y: C + 2, 'text-anchor': 'middle' }, svg);
    label.textContent = 'MW';
    const sub = el('text', { class: 'v-mono', x: C, y: C + 22, 'text-anchor': 'middle' }, svg);
    sub.textContent = 'EDGE AI';

    if (!hasGsap) return null;

    const paths = traces.map((t) => t.path);
    const intro = gsap.timeline({ paused: true });
    intro
      .call(() => prepDraw(paths), null, 0)
      .from(ring, { scale: 0.7, opacity: 0, transformOrigin: '50% 50%', duration: 1 }, 0)
      .from(body, { scale: 0.5, opacity: 0, transformOrigin: '50% 50%', duration: 0.7, ease: 'back.out(1.7)' }, 0)
      .from([die, label, sub], { opacity: 0, duration: 0.4 }, 0.4)
      .from(pins, { scaleY: 0, transformOrigin: '50% 100%', duration: 0.25, stagger: 0.004 }, 0.35)
      .to(paths, { strokeDashoffset: 0, duration: 0.9, stagger: { each: 0.01, from: 'random' }, ease: 'power2.out' }, 0.5)
      .from(vias, { scale: 0, transformOrigin: '50% 50%', duration: 0.3, stagger: { each: 0.008, from: 'random' } }, 0.9);

    // Sürekli hareket: dönen halka, nabız atan çekirdek, izlerden çipe akan sinyaller
    let running = false;
    let spinTween;
    let dieTween;
    let tick;
    function spawn() {
      if (!running) return;
      const free = pulses.find((p) => !p.busy);
      if (free) {
        const candidates = traces.filter((t) => t.group === free.group);
        const t = candidates[Math.floor(Math.random() * candidates.length)];
        free.busy = true;
        travel(free.dot, t.path, {
          from: 1, to: 0, duration: 0.9 + Math.random() * 0.8, ease: 'power1.in',
          onComplete() {
            free.busy = false;
            gsap.fromTo(die, { opacity: 1 }, { opacity: 0.6, duration: 0.3 });
          },
        });
      }
      tick = gsap.delayedCall(0.3 + Math.random() * 0.4, spawn);
    }

    return {
      intro,
      start() {
        running = true;
        spinTween = gsap.to(ring, { rotation: 360, svgOrigin: `${C} ${C}`, duration: 60, ease: 'none', repeat: -1 });
        dieTween = gsap.to(die, { opacity: 0.55, duration: 1.2, yoyo: true, repeat: -1, ease: 'sine.inOut' });
        spawn();
      },
      stop() {
        running = false;
        if (tick) tick.kill();
        if (spinTween) spinTween.kill();
        if (dieTween) dieTween.kill();
      },
    };
  }

  /* ----- 1b. "schematic": solda şematik çizilir, ok, sağda PCB'ye dönüşür ----- */
  function buildSchematic(host) {
    const { svg, defs, id, glow } = createSvg(host);

    // Sol: şematik sayfası
    const sheet = el('rect', { class: 'v-sheet', x: 14, y: 96, width: 250, height: 368, rx: 12 }, svg);
    const sheetLabel = el('text', { class: 'v-mono', x: 26, y: 452 }, svg);
    sheetLabel.textContent = 'SCH · REV A';

    const wires = [
      'M44 160 H98',                                             // giriş
      'M98 160 l6 -11 l12 22 l12 -22 l12 22 l12 -22 l6 11',      // R1
      'M158 160 H222 V196',
      'M200 196 H244', 'M200 208 H244',                          // C1 plakaları
      'M222 208 V306 H176',
      'M60 250 H156 V362 H60 Z',                                 // U1 gövdesi
      'M40 276 H60', 'M40 306 H60', 'M40 336 H60',               // U1 sol pinler
      'M156 276 H176', 'M156 336 H176',                          // U1 sağ pinler
      'M108 362 V396', 'M92 396 H124', 'M98 404 H118', 'M104 412 H112', // toprak
    ].map((d) => el('path', { class: 'v-wire', d }, svg));
    const node = el('circle', { cx: 44, cy: 160, r: 4, fill: '#dbe4f5' }, svg);

    const labels = [
      [56, 148, 'VIN'], [112, 140, 'R1 10k'], [232, 228, 'C1'], [232, 242, '100n'], [92, 312, 'U1'],
    ].map(([x, y, t]) => {
      const n = el('text', { class: 'v-mono', x, y }, svg);
      n.textContent = t;
      return n;
    });

    // Orta: ok
    const arrowLine = el('path', { class: 'v-arrow', d: 'M272 280 H302' }, svg);
    const arrowHead = el('path', { class: 'v-arrow', d: 'M293 271 L303 280 L293 289' }, svg);
    const arrowDot = el('circle', { class: 'v-pulse', r: 3.5, cx: 272, cy: 280, opacity: 0, filter: glow }, svg);

    // Sağ: PCB
    const clipId = `clip-${id}`;
    const clip = el('clipPath', { id: clipId }, defs);
    el('rect', { x: 312, y: 110, width: 234, height: 340, rx: 14 }, clip);

    const board = el('rect', { class: 'v-board', x: 312, y: 110, width: 234, height: 340, rx: 14 }, svg);
    const holes = [[330, 128], [528, 128], [330, 432], [528, 432]].map(([cx, cy]) =>
      el('circle', { class: 'v-via', cx, cy, r: 7 }, svg));

    const pads = [];
    // U1 (SOIC-8) pedleri
    [362, 446].forEach((cx) => {
      [262, 284, 306, 328].forEach((cy) => {
        pads.push(el('rect', { class: 'v-pad', x: cx - 13, y: cy - 5, width: 26, height: 10, rx: 2 }, svg));
      });
    });
    // R1 ve C1 pedleri
    pads.push(el('rect', { class: 'v-pad', x: 352, y: 161, width: 14, height: 18, rx: 2 }, svg));
    pads.push(el('rect', { class: 'v-pad', x: 396, y: 161, width: 14, height: 18, rx: 2 }, svg));
    pads.push(el('rect', { class: 'v-pad', x: 463, y: 192, width: 18, height: 14, rx: 2 }, svg));
    pads.push(el('rect', { class: 'v-pad', x: 463, y: 226, width: 18, height: 14, rx: 2 }, svg));

    const copper = [
      'M410 170 H452 L472 190 V192',
      'M472 240 V290 L455 306 H459',
      'M352 170 H336 V262 H349',
      'M459 262 H504 V384',
      'M349 328 H336 V398 L352 414 H432',
    ].map((d) => el('path', { class: 'v-copper', d }, svg));
    const vias = [[504, 384], [432, 414]].map(([cx, cy]) => el('circle', { class: 'v-via', cx, cy, r: 6 }, svg));

    const silk = [[350, 154, 'R1'], [490, 218, 'C1'], [390, 352, 'U1'], [330, 446, 'MW · REV A']].map(([x, y, t]) => {
      const n = el('text', { class: 'v-silk', x, y }, svg);
      n.textContent = t;
      return n;
    });

    // Optik kontrol (AOI) tarama çizgisi
    const scanG = el('g', { 'clip-path': `url(#${clipId})` }, svg);
    const scan = el('rect', { class: 'v-scan', x: 312, y: 110, width: 3, height: 340, filter: glow }, scanG);
    const copperDots = copper.map(() => el('circle', { class: 'v-pulse-orange', r: 3, cx: -10, cy: -10, opacity: 0, filter: glow }, svg));

    if (!hasGsap) return null;

    const intro = gsap.timeline({ paused: true });
    intro
      .call(() => prepDraw([...wires, arrowLine, arrowHead, ...copper]), null, 0)
      .from(sheet, { opacity: 0, x: -20, duration: 0.5 }, 0)
      .to(wires, { strokeDashoffset: 0, duration: 0.45, stagger: 0.06, ease: 'power1.inOut' }, 0.2)
      .from([node, ...labels], { opacity: 0, duration: 0.3, stagger: 0.05 }, 0.8)
      .to([arrowLine, arrowHead], { strokeDashoffset: 0, duration: 0.35, stagger: 0.1 }, 1.2)
      .from(board, { opacity: 0, x: 30, duration: 0.5 }, 1.35)
      .from(holes, { scale: 0, transformOrigin: '50% 50%', duration: 0.3, stagger: 0.05 }, 1.5)
      .from(pads, { scale: 0, transformOrigin: '50% 50%', duration: 0.3, stagger: 0.03, ease: 'back.out(2)' }, 1.6)
      .to(copper, { strokeDashoffset: 0, duration: 0.6, stagger: 0.1, ease: 'power2.out' }, 1.9)
      .from([...vias, ...silk], { opacity: 0, scale: 0.6, transformOrigin: '50% 50%', duration: 0.3, stagger: 0.04 }, 2.3);

    let loops = [];
    let running = false;
    let tick;
    function copperPulse() {
      if (!running) return;
      const i = Math.floor(Math.random() * copper.length);
      travel(copperDots[i], copper[i], { duration: 0.9 + Math.random() * 0.5 });
      tick = gsap.delayedCall(0.9 + Math.random() * 0.8, copperPulse);
    }

    return {
      intro,
      start() {
        running = true;
        loops = [
          gsap.fromTo(scan, { attr: { x: 312 } }, { attr: { x: 543 }, duration: 3, ease: 'none', repeat: -1, repeatDelay: 2.5 }),
          gsap.timeline({ repeat: -1, repeatDelay: 1.8 }).add(travel(arrowDot, arrowLine, { duration: 0.6, ease: 'none' })),
        ];
        copperPulse();
      },
      stop() {
        running = false;
        if (tick) tick.kill();
        loops.forEach((l) => l.kill());
      },
    };
  }

  /* ----- 1c. "modules": dört modül uçarak gelir, ortak hatta takılır,
             hat üzerinde veri paketleri akar, LED'ler yanıp söner ----- */
  function buildModules(host) {
    const { svg, glow } = createSvg(host);

    const bus = el('rect', { class: 'v-bus', x: 34, y: 260, width: 492, height: 40, rx: 10 }, svg);
    const lanes = [270, 280, 290].map((y) => el('path', { class: 'v-lane', d: `M48 ${y} H512` }, svg));
    const busLabel = el('text', { class: 'v-mono', x: 280, y: 318, 'text-anchor': 'middle' }, svg);
    busLabel.textContent = 'MODWARE BUS';

    const data = [
      { name: 'PWR', sub: '12–48 V', x: 56, y: 88, led: '#6c5bc4', from: [-180, -140, -14] },
      { name: 'MCU', sub: 'STM32', x: 354, y: 88, led: '#9b8fe0', from: [180, -140, 14] },
      { name: 'SENS', sub: 'I²C · SPI', x: 56, y: 362, led: '#34d399', from: [-180, 140, 12] },
      { name: 'COM', sub: 'LoRa · RS-485', x: 354, y: 362, led: '#c4b8f5', from: [180, 140, -12] },
    ];

    const connectors = [];
    const leds = [];
    const modules = data.map((m) => {
      const top = m.y < 260;
      const cx = m.x + 75;
      // Hatla modül arasındaki bağlantı (modülden önce çizilir, altında kalır)
      connectors.push(el('path', {
        class: 'v-trace-hot',
        d: top ? `M${cx} ${m.y + 110} V260` : `M${cx} 300 V${m.y}`,
      }, svg));

      const g = el('g', {}, svg);
      el('rect', { class: 'v-module', x: m.x, y: m.y, width: 150, height: 110, rx: 12 }, g);
      const t = el('text', { class: 'v-label', x: m.x + 16, y: m.y + 32 }, g);
      t.textContent = m.name;
      const s = el('text', { class: 'v-mono', x: m.x + 16, y: m.y + 50 }, g);
      s.textContent = m.sub;
      leds.push(el('circle', { cx: m.x + 132, cy: m.y + 22, r: 5, fill: m.led, filter: glow }, g));
      el('rect', { class: 'v-chip', x: m.x + 16, y: m.y + 64, width: 32, height: 30, rx: 4 }, g);
      el('path', { class: 'v-trace', d: `M${m.x + 48} ${m.y + 79} H${m.x + 88} L${m.x + 98} ${m.y + 69} H${m.x + 134}` }, g);
      el('path', { class: 'v-trace', d: `M${m.x + 48} ${m.y + 88} H${m.x + 134}` }, g);
      return { g, m };
    });

    const packets = lanes.map(() => el('rect', { class: 'v-packet', width: 14, height: 5, rx: 2, x: -20, y: 0, opacity: 0, filter: glow }, svg));
    const connDots = connectors.map(() => el('circle', { class: 'v-pulse', r: 3.5, cx: -10, cy: -10, opacity: 0, filter: glow }, svg));

    if (!hasGsap) return null;

    const intro = gsap.timeline({ paused: true });
    intro
      .call(() => prepDraw([...lanes, ...connectors]), null, 0)
      .from(bus, { scaleX: 0, transformOrigin: '50% 50%', duration: 0.6, ease: 'power3.out' }, 0)
      .to(lanes, { strokeDashoffset: 0, duration: 0.6, stagger: 0.08 }, 0.3)
      .from(busLabel, { opacity: 0, duration: 0.3 }, 0.6);
    modules.forEach(({ g, m }, i) => {
      intro.from(g, {
        x: m.from[0], y: m.from[1], rotation: m.from[2], opacity: 0,
        transformOrigin: '50% 50%', duration: 0.8, ease: 'back.out(1.4)',
      }, 0.5 + i * 0.12);
    });
    intro
      .to(connectors, { strokeDashoffset: 0, duration: 0.35, stagger: 0.08 }, 1.3)
      .from(leds, { scale: 0, transformOrigin: '50% 50%', duration: 0.3, stagger: 0.1, ease: 'back.out(3)' }, 1.5);

    let loops = [];
    let running = false;
    let tick;
    function connPulse() {
      if (!running) return;
      const i = Math.floor(Math.random() * connectors.length);
      const toBus = Math.random() < 0.5;
      travel(connDots[i], connectors[i], { from: toBus ? 0 : 1, to: toBus ? 1 : 0, duration: 0.5, ease: 'none' });
      gsap.fromTo(leds[i], { opacity: 0.3 }, { opacity: 1, duration: 0.25, repeat: 1, yoyo: true });
      tick = gsap.delayedCall(0.8 + Math.random() * 0.8, connPulse);
    }

    return {
      intro,
      start() {
        running = true;
        loops = packets.map((p, i) => gsap.fromTo(p,
          { attr: { x: i % 2 ? 512 : 34, y: 267.5 + i * 10 }, opacity: 1 },
          { attr: { x: i % 2 ? 34 : 512 }, duration: 3 + i * 0.6, ease: 'none', repeat: -1, delay: i * 0.5 }));
        connPulse();
      },
      stop() {
        running = false;
        if (tick) tick.kill();
        loops.forEach((l) => l.kill());
        gsap.set(packets, { opacity: 0 });
      },
    };
  }

  const VISUALS = { chip: buildChip, schematic: buildSchematic, modules: buildModules };

  // Görselleri hemen oluştur (GSAP olmasa da statik olarak görünürler)
  const visuals = Array.from(document.querySelectorAll('.hero-slide')).map((slide) => {
    const host = slide.querySelector('[data-visual]');
    const build = host && VISUALS[host.dataset.visual];
    return build ? build(host) : null;
  });

  if (!hasGsap) {
    // GSAP yüklenemedi: preloader'ı beklemeden kaldır, sayfa statik çalışsın
    clearTimeout(window.__preloaderSafety);
    document.documentElement.classList.remove('is-loading');
    return; // buradan sonrası animasyon
  }

  gsap.defaults({ ease: 'power3.out', duration: 0.8 });

  /* =======================================================
     2. Hero arka planı: 45° kırılımlı devre izleri, üzerlerinde
        akan sinyaller ve fareyi takip eden ışık
     ======================================================= */
  function initHeroCanvas() {
    const canvas = document.querySelector('.hero-canvas');
    if (!canvas) return null;
    const ctx = canvas.getContext('2d');
    const hero = canvas.closest('.hero');
    let traces = [];
    let pulses = [];
    let w = 0;
    let h = 0;
    let visible = true;
    const glow = { x: 0.75, y: 0.45 };   // slayta göre kayan ışık (oran)
    const pointer = { x: -1000, y: -1000, a: 0 };

    let seed = 11; // her yüklemede aynı desen
    const rnd = () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;

    function build() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.clientWidth;
      h = canvas.clientHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed = 11;
      traces = [];
      const step = 32;
      const count = Math.round((w * h) / 7000);
      for (let i = 0; i < count; i++) {
        let x = Math.round((rnd() * w) / step) * step;
        let y = Math.round((rnd() * h) / step) * step;
        const pts = [[x, y]];
        let horizontal = rnd() < 0.6;
        const segs = 2 + Math.floor(rnd() * 4);
        for (let s = 0; s < segs; s++) {
          const len = step * (1 + Math.floor(rnd() * 5));
          const sign = rnd() < 0.5 ? -1 : 1;
          if (s % 2 === 0) {
            if (horizontal) x += len * sign; else y += len * sign;
          } else {
            const d = step * (1 + Math.floor(rnd() * 2));
            x += d * (rnd() < 0.5 ? -1 : 1);
            y += d * (rnd() < 0.5 ? -1 : 1);
            horizontal = !horizontal;
          }
          pts.push([x, y]);
        }
        let total = 0;
        for (let k = 1; k < pts.length; k++) total += Math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]);
        traces.push({ pts, total });
      }
      pulses = traces.filter((_, i) => i % 7 === 0).map((t) => ({ t, d: rnd() * t.total, v: 30 + rnd() * 50 }));
    }

    function pointAt(t, d) {
      for (let k = 1; k < t.pts.length; k++) {
        const [ax, ay] = t.pts[k - 1];
        const [bx, by] = t.pts[k];
        const l = Math.hypot(bx - ax, by - ay);
        if (d <= l) return [ax + (bx - ax) * (d / l), ay + (by - ay) * (d / l)];
        d -= l;
      }
      return t.pts[t.pts.length - 1];
    }

    function draw() {
      ctx.clearRect(0, 0, w, h);

      // Slayta göre konumlanan büyük mavi ışık
      const gx = glow.x * w;
      const gy = glow.y * h;
      const big = ctx.createRadialGradient(gx, gy, 0, gx, gy, Math.max(w, h) * 0.55);
      big.addColorStop(0, 'rgba(155, 143, 224, 0.16)');
      big.addColorStop(1, 'rgba(155, 143, 224, 0)');
      ctx.fillStyle = big;
      ctx.fillRect(0, 0, w, h);

      ctx.lineWidth = 1.4;
      ctx.lineJoin = 'round';
      ctx.strokeStyle = 'rgba(155, 143, 224, 0.16)';
      ctx.beginPath();
      traces.forEach((t) => {
        ctx.moveTo(t.pts[0][0], t.pts[0][1]);
        for (let k = 1; k < t.pts.length; k++) ctx.lineTo(t.pts[k][0], t.pts[k][1]);
      });
      ctx.stroke();

      ctx.fillStyle = 'rgba(108, 91, 196, 0.45)';
      traces.forEach((t) => {
        const p = t.pts[t.pts.length - 1];
        ctx.beginPath();
        ctx.arc(p[0], p[1], 2.4, 0, Math.PI * 2);
        ctx.fill();
      });

      pulses.forEach((p) => {
        const [x, y] = pointAt(p.t, p.d);
        const g = ctx.createRadialGradient(x, y, 0, x, y, 9);
        g.addColorStop(0, 'rgba(155, 143, 224, 0.95)');
        g.addColorStop(1, 'rgba(155, 143, 224, 0)');
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(x, y, 9, 0, Math.PI * 2);
        ctx.fill();
      });

      // Fare ışığı: altındaki izleri aydınlatır
      if (pointer.a > 0.01) {
        const g = ctx.createRadialGradient(pointer.x, pointer.y, 0, pointer.x, pointer.y, 220);
        g.addColorStop(0, `rgba(155, 143, 224, ${0.14 * pointer.a})`);
        g.addColorStop(1, 'rgba(155, 143, 224, 0)');
        ctx.fillStyle = g;
        ctx.fillRect(pointer.x - 220, pointer.y - 220, 440, 440);
      }
    }

    let last = performance.now();
    function frame(now) {
      const dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      if (visible) {
        pulses.forEach((p) => { p.d += p.v * dt; if (p.d > p.t.total) p.d = 0; });
        draw();
      }
      requestAnimationFrame(frame);
    }

    build();
    draw();
    window.addEventListener('resize', () => { build(); draw(); });

    // Hero ekranda değilse çizmeyi bırak (pil / işlemci tasarrufu)
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(hero);

    if (finePointer) {
      hero.addEventListener('pointermove', (e) => {
        const r = canvas.getBoundingClientRect();
        pointer.x = e.clientX - r.left;
        pointer.y = e.clientY - r.top;
        gsap.to(pointer, { a: 1, duration: 0.3, overwrite: 'auto' });
      });
      hero.addEventListener('pointerleave', () => gsap.to(pointer, { a: 0, duration: 0.5, overwrite: 'auto' }));
    }

    if (!reduceMotion) requestAnimationFrame(frame);

    return {
      // Slayt değişince ışığı yeni konuma kaydır
      moveGlow(x, y) {
        gsap.to(glow, { x, y, duration: 1.4, ease: 'power2.inOut', onUpdate: () => { if (reduceMotion) draw(); } });
      },
    };
  }

  /* =======================================================
     3. Hero slaytı
     ======================================================= */
  function initSlider(bg) {
    const hero = document.getElementById('hero');
    if (!hero) return;
    const slides = Array.from(hero.querySelectorAll('.hero-slide'));
    const controls = hero.querySelector('.hero-controls');
    const dots = Array.from(hero.querySelectorAll('[data-slide-to]'));
    const fills = dots.map((d) => d.querySelector('.slide-dot-fill'));
    const counter = hero.querySelector('[data-slide-current]');
    const pauseBtn = hero.querySelector('[data-slide-pause]');
    const DURATION = 9;                                   // slayt başına saniye
    const GLOW = [[0.75, 0.45], [0.68, 0.35], [0.8, 0.6]]; // slayta göre ışık konumu

    // Her slaydın parçaları
    const parts = slides.map((s) => ({
      eyebrow: s.querySelector('.slide-eyebrow'),
      chars: splitChars(s.querySelector('.slide-title')),
      text: s.querySelector('.slide-text'),
      actions: s.querySelector('.slide-actions'),
      visual: s.querySelector('.slide-visual'),
    }));

    let current = 0;
    let transition = null;
    let progress = null;
    let userPaused = reduceMotion; // hareket azaltılmışsa otomatik geçiş kapalı başlar
    let hoverPaused = false;
    let inView = true;

    controls.hidden = false;
    if (reduceMotion) pauseBtn.setAttribute('aria-pressed', 'true');

    function setInactive(i) {
      slides[i].classList.remove('is-active');
      slides[i].setAttribute('aria-hidden', 'true');
      slides[i].inert = true; // gizli slayttaki bağlantılara Tab ile gidilmesin
    }
    function setActive(i) {
      slides[i].classList.add('is-active');
      slides[i].removeAttribute('aria-hidden');
      slides[i].inert = false;
    }
    slides.forEach((_, i) => { if (i !== 0) setInactive(i); });

    // Gelen slaydın giriş animasyonu
    function enter(i, dir) {
      const p = parts[i];
      const v = visuals[i];
      const tl = gsap.timeline();
      if (reduceMotion) {
        tl.fromTo(slides[i], { opacity: 0 }, { opacity: 1, duration: 0.3 });
        if (v) v.intro.progress(1);
        return tl;
      }
      tl.fromTo(p.eyebrow, { opacity: 0 }, { opacity: 1, duration: 0.5 }, 0)
        .fromTo(p.chars,
          { yPercent: 100, opacity: 0 },
          { yPercent: 0, opacity: 1, duration: 0.7, stagger: 0.012, ease: 'power3.out' }, 0.05)
        .fromTo(p.text, { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0.35)
        .fromTo(p.actions, { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5 }, 0.5)
        .fromTo(p.visual, { x: 30 * dir, opacity: 0 }, { x: 0, opacity: 1, duration: 0.9 }, 0);
      if (v) {
        tl.add(() => { v.intro.restart(); v.start(); }, 0.1);
      }
      return tl;
    }

    // Giden slaydın çıkışı
    function leave(i, dir) {
      const p = parts[i];
      const v = visuals[i];
      const tl = gsap.timeline({ onComplete: () => { if (v) v.stop(); } });
      if (reduceMotion) return tl;
      tl.to(p.chars, { opacity: 0, duration: 0.35, stagger: 0.004, ease: 'power2.in' }, 0)
        .to([p.eyebrow, p.text, p.actions], { y: -16, opacity: 0, duration: 0.35, stagger: 0.04, ease: 'power2.in' }, 0)
        .to(p.visual, { x: -30 * dir, opacity: 0, duration: 0.45, ease: 'power2.in' }, 0);
      return tl;
    }

    function updateUi(i) {
      dots.forEach((d, n) => {
        d.classList.toggle('is-active', n === i);
        d.setAttribute('aria-current', n === i ? 'true' : 'false');
        gsap.set(fills[n], { scaleX: n < i ? 1 : 0 });
      });
      counter.textContent = String(i + 1).padStart(2, '0');
      if (bg) bg.moveGlow(GLOW[i][0], GLOW[i][1]);
    }

    // Otomatik geçiş: aktif noktanın çizgisi dolunca sonraki slayt
    function runProgress() {
      if (progress) progress.kill();
      progress = gsap.fromTo(fills[current], { scaleX: 0 }, {
        scaleX: 1, duration: DURATION, ease: 'none',
        onComplete: () => goTo(current + 1, 1),
      });
      syncPause();
    }
    function syncPause() {
      if (!progress) return;
      if (userPaused || hoverPaused || !inView || document.hidden) progress.pause();
      else progress.resume();
    }

    function goTo(n, dir) {
      const next = (n + slides.length) % slides.length;
      if (next === current) return;
      const d = dir || (next > current ? 1 : -1);
      if (transition) transition.progress(1); // önceki geçişi hemen bitir
      const prev = current;
      current = next;
      updateUi(next);
      transition = gsap.timeline({ onComplete: () => { transition = null; } })
        .add(leave(prev, d))
        .add(() => { setInactive(prev); setActive(next); })
        .add(enter(next, d));
      runProgress();
    }

    // Kontroller
    hero.querySelector('[data-slide-prev]').addEventListener('click', () => goTo(current - 1, -1));
    hero.querySelector('[data-slide-next]').addEventListener('click', () => goTo(current + 1, 1));
    dots.forEach((d, n) => d.addEventListener('click', () => goTo(n)));
    pauseBtn.addEventListener('click', () => {
      userPaused = !userPaused;
      pauseBtn.setAttribute('aria-pressed', String(userPaused));
      pauseBtn.setAttribute('aria-label', userPaused ? 'Otomatik geçişi başlat' : 'Otomatik geçişi durdur');
      syncPause();
    });

    // Klavye: hero içindeyken sol/sağ ok
    hero.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') goTo(current - 1, -1);
      if (e.key === 'ArrowRight') goTo(current + 1, 1);
    });

    // Fare metnin üzerindeyken dur (okuma süresi), odak içerideyken de dur
    hero.querySelector('.hero-stage').addEventListener('pointerenter', (e) => {
      if (e.pointerType === 'mouse') { hoverPaused = true; syncPause(); }
    });
    hero.querySelector('.hero-stage').addEventListener('pointerleave', () => { hoverPaused = false; syncPause(); });
    hero.addEventListener('focusin', () => { hoverPaused = true; syncPause(); });
    hero.addEventListener('focusout', () => { hoverPaused = false; syncPause(); });

    // Dokunmatik kaydırma (swipe)
    let startX = null;
    hero.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') startX = e.clientX; });
    hero.addEventListener('pointerup', (e) => {
      if (startX === null) return;
      const dx = e.clientX - startX;
      if (Math.abs(dx) > 50) goTo(current + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1);
      startX = null;
    });

    // Hero ekrandan çıkınca ya da sekme gizlenince otomatik geçişi beklet
    new IntersectionObserver(([e]) => { inView = e.isIntersecting; syncPause(); }, { threshold: 0.3 }).observe(hero);
    document.addEventListener('visibilitychange', syncPause);

    updateUi(0);

    // İlk slaydın girişi ve otomatik geçiş, preloader açıldıktan sonra başlar
    return {
      start() {
        enter(0, 1);
        runProgress();
      },
    };
  }

  /* =======================================================
     4. Nasıl çalışıyoruz
     Bölüm ekrana girince dört aşama sırayla alttan gelir; her biri
     geldiğinde yanar (.is-lit) ve oku bir sonrakini gösterir.
     ======================================================= */
  function initProcess() {
    const steps = gsap.utils.toArray('#nasil-calisiyoruz .p-step');
    if (!steps.length) return;

    if (reduceMotion || !hasScrollTrigger) {
      steps.forEach((s) => s.classList.add('is-lit'));
      return;
    }

    gsap.set(steps, { y: 40, opacity: 0 });
    const tl = gsap.timeline({
      scrollTrigger: { trigger: steps[0].parentNode, start: 'top 78%', once: true },
    });
    steps.forEach((step, i) => {
      tl.to(step, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, i * 0.28)
        .add(() => step.classList.add('is-lit'), i * 0.28 + 0.3);
    });
  }

  /* =======================================================
     4b. Ürünler: kartın içine bakın (MW-PWR-BK kare dizisi)
     Aşağı kaydırdıkça kart açılır, son adımda yeniden birleşir;
     yukarı çıkınca aynı yol tersinden izlenir. Her açıklama adımı
     ekranın ortasına gelince yanar (.is-active).
     ======================================================= */
  function initSequence() {
    const box = document.querySelector('.bk-explode');
    if (!box) return;
    const steps = gsap.utils.toArray(box.querySelectorAll('.bk-step'));
    const canvas = box.querySelector('.seq-canvas');
    const poster = box.querySelector('.seq-poster');
    if (reduceMotion || !hasScrollTrigger) {
      steps.forEach((s) => s.classList.add('is-active'));
      return; // sabit ilk kare (poster) kalır
    }

    // Adımın kutusu okuma çizgisini içerdiği sürece adım yanar (kutular eşit boy, yazı ortalı).
    // Masaüstü: çizgi ekranın %35'i; yazı soluk gelir, %70'e gelince yanar ve ekrandan çıkana kadar
    // yanık kalır. Mobil (CSS ile aynı kırılım, 860 px; kart üstte yapışık): yazı yapışık kartın altındaki
    // alana girince yanar, kartın altına girene kadar yanık kalır. Çizgi her yenilemede yeniden hesaplanır.
    const stackedMq = window.matchMedia('(max-width: 860px)');
    const small = window.matchMedia('(max-width: 767px)').matches; // küçük kare seti
    const stage = box.querySelector('.bk-stage');
    function stepLine() {
      if (!stackedMq.matches) return window.innerHeight * 0.35;
      const stuckBottom = parseFloat(getComputedStyle(stage).top) + stage.offsetHeight;
      return stuckBottom + steps[0].offsetHeight / 2;
    }
    const seqMark = stackedMq.matches ? '74%' : '60%';
    steps.forEach((step) => {
      window.ScrollTrigger.create({
        trigger: step,
        start: () => `top ${stepLine()}px`,
        end: () => `bottom ${stepLine()}px`,
        toggleClass: 'is-active',
      });
    });

    const ctx = canvas.getContext('2d');
    // Mobilde daha küçük ve daha az kareli set (57 kare)
    const count = Number(small ? box.dataset.seqCountSm : box.dataset.seqCount);
    const path = small ? box.dataset.seqPathSm : box.dataset.seqPath;
    const version = box.dataset.seqVersion ? `?v=${box.dataset.seqVersion}` : '';
    const frames = new Array(count);
    const state = { frame: 0 };
    let drawn = -1;

    function resize() {
      // clientWidth: CSS ölçeği dahil edilmez, canvas tam çözünürlükte kalır
      const dpr = Math.min(window.devicePixelRatio || 1, 3);
      canvas.width = Math.round(canvas.clientWidth * dpr);
      canvas.height = Math.round(canvas.clientHeight * dpr);
      drawn = -1;
      render();
    }

    // İstenen kare henüz yüklenmediyse en yakın yüklenmiş kare
    function nearestLoaded(i) {
      for (let d = 0; d < count; d++) {
        const a = frames[i - d];
        const b = frames[i + d];
        if (a && a.complete && a.naturalWidth) return i - d;
        if (b && b.complete && b.naturalWidth) return i + d;
      }
      return -1;
    }

    function render() {
      if (canvas.hidden) return;
      const i = nearestLoaded(Math.round(state.frame));
      if (i < 0 || i === drawn) return;
      const img = frames[i];
      const k = Math.min(canvas.width / img.naturalWidth, canvas.height / img.naturalHeight);
      const w = img.naturalWidth * k;
      const h = img.naturalHeight * k;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(img, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h);
      drawn = i;
    }

    // Kareleri bölüm yaklaşınca yükle: önce ilk kare, sonra her 8., 4., 2., kalanlar
    function load() {
      const order = [];
      const seen = new Set();
      [count, 8, 4, 2, 1].forEach((step) => {
        for (let i = 0; i < count; i += step) if (!seen.has(i)) { seen.add(i); order.push(i); }
      });
      order.forEach((i) => {
        const img = new Image();
        img.decoding = 'async';
        img.onload = () => {
          if (i === 0) { canvas.hidden = false; poster.hidden = true; resize(); } else render();
        };
        img.src = `${path}${String(i + 1).padStart(3, '0')}.webp${version}`;
        frames[i] = img;
      });
    }
    window.ScrollTrigger.create({ trigger: box, start: 'top 250%', once: true, onEnter: load });

    /* İlerleme (0 → 1) → kare: 1.–4. adım boyunca açılır, açık kalır,
       son adımda yeniden birleşir. */
    const OPEN = 0.62;
    const CLOSE = 0.8;
    const scroll = { p: 0 };
    function frameFromProgress(p) {
      let t;
      if (p < OPEN) t = p / OPEN;
      else if (p < CLOSE) t = 1;
      else t = 1 - (p - CLOSE) / (1 - CLOSE);
      return Math.max(0, Math.min(1, t)) * (count - 1);
    }

    gsap.to(scroll, {
      p: 1,
      ease: 'none',
      onUpdate() {
        state.frame = frameFromProgress(scroll.p);
        render();
      },
      scrollTrigger: {
        trigger: steps[0],
        start: `center ${seqMark}`,
        endTrigger: steps[steps.length - 1],
        end: `center ${seqMark}`,
        scrub: 0.4,
      },
    });

    window.addEventListener('resize', resize);
  }

  /* =======================================================
     5. Bölüm başlıkları, değer kartları, kapanış
     ======================================================= */
  function initReveals() {
    if (reduceMotion || !hasScrollTrigger) return;

    // Başlıklar harf harf alttan kayarak gelir
    document.querySelectorAll('[data-split-reveal]').forEach((h) => {
      const chars = splitChars(h);
      gsap.from(chars, {
        yPercent: 115, opacity: 0, duration: 0.7, stagger: 0.015, ease: 'power4.out',
        scrollTrigger: { trigger: h, start: 'top 85%' },
      });
    });

    // Değer kartları: ekrana giren kartlar alttan sırayla gelir (stagger 0.1)
    const cards = gsap.utils.toArray('.value-card');
    if (cards.length) {
      gsap.set(cards, { y: 60, opacity: 0 });
      window.ScrollTrigger.batch(cards, {
        start: 'top 90%',
        once: true,
        onEnter: (batch) => gsap.to(batch, {
          y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: 'power3.out', overwrite: 'auto',
        }),
      });
    }

    // Ürün kartları: ekrana girdikçe alttan sırayla gelir. clearProps ile
    // animasyon bitince CSS hover kalkışı (translateY -8px) yeniden çalışır.
    const productCards = gsap.utils.toArray('.product-card');
    if (productCards.length) {
      gsap.set(productCards, { y: 50, opacity: 0 });
      window.ScrollTrigger.batch(productCards, {
        start: 'top 92%',
        once: true,
        onEnter: (batch) => gsap.to(batch, {
          y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: 'power3.out',
          overwrite: 'auto', clearProps: 'transform,opacity',
        }),
      });
    }

    // Kapanış başlığı: SplitType ile harflere bölünür, kaydırdıkça açılır (scrub)
    const ctaTitle = document.querySelector('[data-cta-split]');
    if (ctaTitle) {
      let chars;
      if (typeof window.SplitType !== 'undefined') {
        ctaTitle.setAttribute('aria-label', ctaTitle.textContent.trim());
        const split = new window.SplitType(ctaTitle, { types: 'words,chars' });
        split.words.forEach((w) => w.setAttribute('aria-hidden', 'true'));
        chars = split.chars;
      } else {
        chars = splitChars(ctaTitle); // SplitType yüklenemezse kendi bölücümüz
      }
      gsap.from(chars, {
        yPercent: 100, opacity: 0, stagger: 0.04, ease: 'power3.out',
        scrollTrigger: { trigger: ctaTitle, start: 'top 92%', end: 'top 55%', scrub: 0.6 },
      });
    }

    // Kapanış metni ve butonları
    const cta = document.querySelector('.cta-band');
    if (cta) {
      gsap.from(cta.querySelectorAll('.cta-text, .cta-actions'), {
        y: 30, opacity: 0, duration: 0.7, stagger: 0.12,
        scrollTrigger: { trigger: cta, start: 'top 75%' },
      });
    }
  }

  /* =======================================================
     6. Hero'su olmayan sayfalar (placeholder'lar)
     ======================================================= */
  function initPageIntro() {
    if (reduceMotion || document.getElementById('hero')) return;
    // Sayfa başlığı harf harf, ardından etiket/metin/filtre sırayla
    const title = document.querySelector('[data-split-intro]');
    if (title) {
      let chars;
      if (typeof window.SplitType !== 'undefined') {
        title.setAttribute('aria-label', title.textContent.replace(/\s+/g, ' ').trim());
        const split = new window.SplitType(title, { types: 'words,chars' });
        split.words.forEach((w) => w.setAttribute('aria-hidden', 'true'));
        chars = split.chars;
      } else {
        chars = splitChars(title);
      }
      gsap.from(chars, { yPercent: 110, opacity: 0, duration: 0.8, stagger: 0.025, ease: 'power4.out' });
    }
    gsap.from('[data-anim="hero"]', { y: 24, opacity: 0, stagger: 0.1, delay: title ? 0.2 : 0 });
  }

  /* =======================================================
     7. Yumuşak kaydırma (Lenis)
     Lenis pencerenin kendi kaydırmasını yumuşatır; ScrollTrigger her
     Lenis karesinde güncellenir. Sticky ve çapa bağlantıları çalışmaya devam eder.
     ======================================================= */
  function initLenis() {
    if (reduceMotion || typeof window.Lenis === 'undefined') return null;

    const lenis = new window.Lenis({
      duration: 1.15,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // yumuşak "expo" yavaşlama
      smoothWheel: true,
    });

    // GSAP ile aynı saatten çalış (tek requestAnimationFrame döngüsü)
    if (hasScrollTrigger) lenis.on('scroll', window.ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);

    // Sayfa içi çapa bağlantıları (#nasil-calisiyoruz vb.) Lenis ile kaysın
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const id = a.getAttribute('href');
      const target = id.length > 1 && document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const header = document.getElementById('site-header');
      lenis.scrollTo(target, { offset: -(header ? header.offsetHeight : 0) - 16 });
      if (target.matches('#main')) target.focus({ preventScroll: true });
    });

    window.lenis = lenis; // main.js mobil menü açılınca kaydırmayı durdurmak için kullanır
    return lenis;
  }

  /* =======================================================
     8. Preloader
     "MODWARE" harf harf açılır, alttaki çizgi %0 → %100 dolar.
     Bitince perde yukarı kayar, sayfa 1.05 → 1 ölçek + belirme ile gelir.
     done() → hero slaytı ve sayfa girişleri bundan sonra başlar.
     ======================================================= */
  // Preloader parçaları sayfa geçişinde de kullanılır (bkz. initPageTransitions)
  const pre = {};

  function runPreloader(lenis, done) {
    const root = document.documentElement;
    pre.el = document.getElementById('preloader');
    clearTimeout(window.__preloaderSafety); // güvenlik zamanlayıcısı artık gerekmez

    // Adreste #çapa varsa (ör. hakkimizda.html#hikaye) açılıştan sonra oraya git
    const hashTarget = (() => {
      try { return location.hash.length > 1 ? document.querySelector(location.hash) : null; } catch (err) { return null; }
    })();

    const finish = () => {
      root.classList.remove('is-loading');
      if (pre.el) pre.el.classList.remove('is-transition');
      if (lenis) lenis.start();
      if (hasScrollTrigger) window.ScrollTrigger.refresh();
      if (hashTarget) {
        const header = document.getElementById('site-header');
        const offset = -(header ? header.offsetHeight : 0) - 16;
        if (lenis) lenis.scrollTo(hashTarget, { offset, immediate: true });
        else window.scrollTo(0, hashTarget.getBoundingClientRect().top + window.scrollY + offset);
      }
      done();
    };

    // Önceki sayfadan geçişle mi gelindi?
    let fromNav = false;
    let seen = false;
    try {
      fromNav = sessionStorage.getItem('mw-nav') === '1';
      sessionStorage.removeItem('mw-nav');
      seen = sessionStorage.getItem('mw-preloaded') === '1';
      sessionStorage.setItem('mw-preloaded', '1');
    } catch (err) { /* depolama kapalı olabilir */ }

    if (!pre.el || reduceMotion) { finish(); return; }

    pre.word = pre.el.querySelector('[data-preloader-word]');
    pre.fill = pre.el.querySelector('.preloader-bar-fill');
    pre.count = pre.el.querySelector('[data-preloader-count]');
    // SplitType yüklenemezse kelime tek parça animasyon yapar
    pre.chars = typeof window.SplitType !== 'undefined'
      ? new window.SplitType(pre.word, { types: 'chars' }).chars
      : [pre.word];

    if (lenis) lenis.stop();
    if (!hashTarget) window.scrollTo(0, 0);

    const page = ['.site-header', 'main', '.site-footer'];
    const setFill = (v) => {
      pre.fill.style.transform = `scaleX(${v / 100})`;
      pre.count.textContent = Math.round(v);
    };

    /* ----- Sayfa geçişiyle gelindiyse: kısa nabız, çizgi %60 → %100,
             perde söner, yeni sayfa aşağıdan + 0.98 → 1 ölçekle gelir ----- */
    if (fromNav) {
      pre.el.classList.add('is-transition');
      const progress = { v: 60 };
      setFill(60);
      gsap.timeline({ onComplete: finish })
        .fromTo(pre.word, { scale: 1, opacity: 0.7 }, { scale: 1.06, opacity: 1, duration: 0.3, yoyo: true, repeat: 1, ease: 'sine.inOut' }, 0)
        .to(progress, { v: 100, duration: 0.5, ease: 'power2.out', onUpdate: () => setFill(progress.v) }, 0)
        .to(pre.el, { opacity: 0, duration: 0.45, ease: 'power2.out' }, 0.55)
        .fromTo(page,
          { opacity: 0, scale: 0.98, y: 40, transformOrigin: '50% 0%' },
          { opacity: 1, scale: 1, y: 0, duration: 0.8, ease: 'power3.out', clearProps: 'transform,opacity,transformOrigin' },
          0.6);
      return;
    }

    /* ----- İlk giriş: harfler açılır, çizgi %0 → %100 dolar,
             perde yukarı kayar, sayfa 1.05 → 1 ölçekle gelir.
             Sayfa yaklaşık 1 sn'de görünmeye başlar (açılış hızı Google'ın ölçtüğü
             "en büyük içerik" süresini doğrudan etkiler). ----- */
    const fillTime = seen ? 0.4 : 0.6; // aynı ziyarette yeniden yüklemede daha kısa
    const progress = { v: 0 };
    const intro = gsap.timeline();
    intro
      .from(pre.chars, { yPercent: 110, opacity: 0, duration: 0.45, stagger: 0.03, ease: 'power4.out' }, 0)
      .to(progress, { v: 100, duration: fillTime, ease: 'power2.inOut', onUpdate: () => setFill(progress.v) }, 0.05);

    // Hem dolum bitsin hem yazı tipleri hazır olsun (en fazla 1,2 sn bekle)
    const fontsReady = document.fonts && document.fonts.ready
      ? Promise.race([document.fonts.ready, new Promise((r) => setTimeout(r, 1200))])
      : Promise.resolve();
    const introDone = new Promise((r) => intro.eventCallback('onComplete', r));

    Promise.all([fontsReady, introDone]).then(() => {
      gsap.timeline({ onComplete: finish })
        .to(pre.chars, { yPercent: -110, opacity: 0, duration: 0.25, stagger: 0.02, ease: 'power3.in' })
        .to([pre.fill.parentNode, pre.count], { opacity: 0, duration: 0.2 }, '<')
        .to(pre.el, { yPercent: -100, duration: 0.5, ease: 'power4.inOut' }, '-=0.1')
        .fromTo(page,
          { scale: 1.05, opacity: 0, transformOrigin: '50% 0%' },
          { scale: 1, opacity: 1, duration: 0.6, ease: 'power3.out', clearProps: 'transform,opacity,transformOrigin' },
          '<0.1');
    });
  }

  /* =======================================================
     9. Özel imleç
     Via (uç) ve köşeli çerçeve imleci doğrudan izler (gecikme yok).
     Bağlantı/buton üzerinde çerçeve biraz büyür ve parlar.
     Dokunmatik cihazlarda ve "hareketi azalt" tercihinde çalışmaz.
     ======================================================= */
  function initCursor() {
    if (!finePointer || reduceMotion) return;
    const cursor = document.querySelector('.cursor');
    if (!cursor) return;
    const dot = cursor.querySelector('.cursor-dot');
    const frame = cursor.querySelector('.cursor-frame');

    document.documentElement.classList.add('has-cursor');
    gsap.set([dot, frame], { xPercent: -50, yPercent: -50 });

    let shown = false;
    window.addEventListener('mousemove', (e) => {
      gsap.set([dot, frame], { x: e.clientX, y: e.clientY });
      if (!shown) {
        shown = true;
        gsap.to([dot, frame], { opacity: 1, duration: 0.2 });
      }
    });

    // Pencereden çıkınca gizle, girince göster
    document.documentElement.addEventListener('mouseleave', () => gsap.to([dot, frame], { opacity: 0, duration: 0.2 }));
    document.documentElement.addEventListener('mouseenter', () => { if (shown) gsap.to([dot, frame], { opacity: 1, duration: 0.2 }); });

    const interactive = 'a, button, [role="button"], label[for], .slide-dot';
    document.addEventListener('mouseover', (e) => {
      if (e.target.closest(interactive)) cursor.classList.add('is-hover');
    });
    document.addEventListener('mouseout', (e) => {
      const from = e.target.closest(interactive);
      const to = e.relatedTarget && e.relatedTarget.closest ? e.relatedTarget.closest(interactive) : null;
      if (from && from !== to) cursor.classList.toggle('is-hover', Boolean(to));
    });
    window.addEventListener('mousedown', () => cursor.classList.add('is-down'));
    window.addEventListener('mouseup', () => cursor.classList.remove('is-down'));
  }

  /* =======================================================
     10. Arka plan katmanı
     Işık imleci yumuşakça izler; kaydırdıkça perde koyulaşır.
     ======================================================= */
  function initBackground() {
    const layer = document.querySelector('.bg-layer');
    if (!layer) return;
    const glow = layer.querySelector('.bg-glow');
    const shade = layer.querySelector('.bg-shade');

    gsap.set(glow, { x: window.innerWidth * 0.7, y: window.innerHeight * 0.35 });

    if (!reduceMotion) {
      if (finePointer) {
        const gx = gsap.quickTo(glow, 'x', { duration: 1.4, ease: 'power3.out' });
        const gy = gsap.quickTo(glow, 'y', { duration: 1.4, ease: 'power3.out' });
        window.addEventListener('mousemove', (e) => { gx(e.clientX); gy(e.clientY); });
      } else {
        // Dokunmatikte ışık ekranda yavaşça gezinir
        gsap.to(glow, {
          x: () => window.innerWidth * 0.25, y: () => window.innerHeight * 0.7,
          duration: 9, ease: 'sine.inOut', yoyo: true, repeat: -1,
        });
      }
    }

    // Sayfanın sonuna doğru zemin hafifçe koyulaşır (0 → %45 siyah)
    if (hasScrollTrigger) {
      gsap.to(shade, {
        opacity: 0.45,
        ease: 'none',
        scrollTrigger: { start: 0, end: 'max', scrub: true },
      });
    }
  }

  /* =======================================================
     11. Değer kartları: hover etkileşimi
     İkon 360° döner, kart 6px kalkar, fare konumuna göre en fazla 6°
     eğilir. Gölge ve neon çizgi CSS'te (:hover).
     ======================================================= */
  function initValueCards() {
    if (!finePointer || reduceMotion) return;
    const MAX_TILT = 4;

    document.querySelectorAll('[data-tilt]').forEach((card) => {
      const icon = card.querySelector('.value-icon');
      gsap.set(card, { transformPerspective: 900 });
      const rotX = gsap.quickTo(card, 'rotationX', { duration: 0.5, ease: 'power3.out' });
      const rotY = gsap.quickTo(card, 'rotationY', { duration: 0.5, ease: 'power3.out' });

      card.addEventListener('pointerenter', () => {
        gsap.to(card, { y: -6, duration: 0.4, ease: 'power3.out', overwrite: 'auto' });
        if (icon) gsap.fromTo(icon, { rotation: 0 }, { rotation: 360, duration: 0.6, ease: 'power2.inOut', transformOrigin: '50% 50%' });
      });
      card.addEventListener('pointermove', (e) => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;   // -0.5 … 0.5
        const py = (e.clientY - r.top) / r.height - 0.5;
        rotY(px * MAX_TILT * 2);
        rotX(-py * MAX_TILT * 2);
      });
      card.addEventListener('pointerleave', () => {
        rotX(0);
        rotY(0);
        gsap.to(card, { y: 0, duration: 0.5, ease: 'power3.out', overwrite: 'auto' });
      });
    });
  }

  /* =======================================================
     12. Manyetik butonlar + parçacık patlaması
     Fare butona yaklaşınca (buton boyutunun ~yarısı kadar dışından
     itibaren) buton imlece doğru kayar; uzaklaşınca esneyerek döner.
     [data-burst] butonlarında hover'da arkadan parçacıklar saçılır.
     ======================================================= */
  function initMagnetic() {
    if (!finePointer || reduceMotion) return;

    const items = Array.from(document.querySelectorAll('.btn, .slide-arrow, .slide-pause')).map((el) => ({
      el,
      x: gsap.quickTo(el, 'x', { duration: 0.5, ease: 'power3.out' }),
      y: gsap.quickTo(el, 'y', { duration: 0.5, ease: 'power3.out' }),
      active: false,
      visible: true,
    }));

    // Yalnızca ekrandaki butonları hesapla
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        const it = items.find((i) => i.el === en.target);
        if (it) it.visible = en.isIntersecting;
      });
    });
    items.forEach((it) => io.observe(it.el));

    const STRENGTH = 0.2;
    window.addEventListener('mousemove', (e) => {
      items.forEach((it) => {
        if (!it.visible) return;
        const r = it.el.getBoundingClientRect();
        // Kendi dönüşümünü çıkararak gerçek merkezi bul
        const cx = r.left + r.width / 2 - (gsap.getProperty(it.el, 'x') || 0);
        const cy = r.top + r.height / 2 - (gsap.getProperty(it.el, 'y') || 0);
        const dx = e.clientX - cx;
        const dy = e.clientY - cy;
        const reachX = r.width / 2 + Math.max(30, r.width * 0.5);
        const reachY = r.height / 2 + Math.max(30, r.height * 0.8);
        if (Math.abs(dx) < reachX && Math.abs(dy) < reachY) {
          it.active = true;
          it.x(dx * STRENGTH);
          it.y(dy * STRENGTH);
        } else if (it.active) {
          it.active = false;
          gsap.to(it.el, { x: 0, y: 0, duration: 0.9, ease: 'elastic.out(1, 0.4)', overwrite: 'auto' });
          // quickTo'nun sonraki çağrısı esnek dönüşü bozmasın diye hedefleri sıfırla
          it.x = gsap.quickTo(it.el, 'x', { duration: 0.5, ease: 'power3.out' });
          it.y = gsap.quickTo(it.el, 'y', { duration: 0.5, ease: 'power3.out' });
        }
      });
    });

    // Parçacık patlaması
    const COLORS = ['#9b8fe0', '#6c5bc4', '#ffffff'];
    document.querySelectorAll('[data-burst]').forEach((btn) => {
      btn.addEventListener('mouseenter', () => {
        const host = btn.parentElement; // .cta-actions (position: relative)
        const cx = btn.offsetLeft + btn.offsetWidth / 2;
        const cy = btn.offsetTop + btn.offsetHeight / 2;
        for (let i = 0; i < 10; i++) {
          const p = document.createElement('span');
          p.className = 'particle';
          const size = 3 + Math.random() * 5;
          p.style.width = `${size}px`;
          p.style.height = `${size}px`;
          p.style.left = `${cx}px`;
          p.style.top = `${cy}px`;
          p.style.background = COLORS[i % COLORS.length];
          p.style.boxShadow = `0 0 8px ${COLORS[i % COLORS.length]}`;
          host.appendChild(p);
          const angle = Math.random() * Math.PI * 2;
          const dist = btn.offsetWidth * 0.4 + 16 + Math.random() * 30;
          gsap.fromTo(p,
            { x: 0, y: 0, scale: 1, opacity: 1 },
            {
              x: Math.cos(angle) * dist,
              y: Math.sin(angle) * dist * 0.7,
              scale: 0,
              opacity: 0,
              duration: 0.7 + Math.random() * 0.5,
              ease: 'power3.out',
              onComplete: () => p.remove(),
            });
        }
      });
    });
  }

  /* =======================================================
     13. Kaydırma göstergeleri
     Üstte ilerleme çubuğu; footer üstündeki çizgi sayfanın son
     ekranında soldan sağa dolar.
     ======================================================= */
  function initScrollUi() {
    if (!hasScrollTrigger) return;
    document.documentElement.classList.add('has-st');

    const bar = document.querySelector('.scroll-progress-bar');
    if (bar) {
      gsap.to(bar, { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: 0.3 } });
    }

    const line = document.querySelector('.footer-line-fill');
    if (line) {
      gsap.to(line, {
        scaleX: 1,
        ease: 'none',
        scrollTrigger: {
          // Son ekran boyunun %80'i içinde dolar; kısa sayfalarda baştan dolu
          start: () => Math.max(0, window.ScrollTrigger.maxScroll(window) - window.innerHeight * 0.8),
          end: 'max',
          scrub: 0.4,
          invalidateOnRefresh: true,
        },
      });
    }
  }

  /* =======================================================
     14. Sayfa geçişi
     Site içi bir sayfaya giden bağlantıya tıklanınca: sayfa söner ve
     0.98'e küçülür, ortada "MODWARE" nabız atar, çizgi %60'a dolar,
     sonra yeni sayfa açılır. Yeni sayfadaki giriş runPreloader içinde.
     ======================================================= */
  function initPageTransitions(lenis) {
    if (reduceMotion || !pre.el) return;
    const root = document.documentElement;
    let leaving = false;

    function leaveTo(href) {
      if (leaving) return;
      leaving = true;
      try { sessionStorage.setItem('mw-nav', '1'); } catch (err) { /* yok say */ }
      if (lenis) lenis.stop();

      // Perdeyi geçiş moduna hazırla (açılıştan kalan durumları sıfırla)
      root.classList.add('is-loading');
      pre.el.classList.add('is-transition');
      gsap.set(pre.el, { yPercent: 0, opacity: 0 });
      gsap.set(pre.chars, { yPercent: 0, opacity: 1 });
      gsap.set(pre.fill.parentNode, { opacity: 1 });
      pre.fill.style.transform = 'scaleX(0)';
      const progress = { v: 0 };

      gsap.timeline({ onComplete: () => { window.location.href = href; } })
        .to(['.site-header', 'main', '.site-footer'], {
          opacity: 0, scale: 0.98, duration: 0.45, ease: 'power2.in',
          transformOrigin: `50% ${window.innerHeight / 2}px`,
        }, 0)
        .to(pre.el, { opacity: 1, duration: 0.35, ease: 'power2.out' }, 0.15)
        .fromTo(pre.word, { scale: 0.96, opacity: 0.6 }, { scale: 1.04, opacity: 1, duration: 0.3, yoyo: true, repeat: 1, ease: 'sine.inOut' }, 0.2)
        .to(progress, {
          v: 60, duration: 0.55, ease: 'power2.inOut',
          onUpdate: () => { pre.fill.style.transform = `scaleX(${progress.v / 100})`; },
        }, 0.2);
    }

    document.addEventListener('click', (e) => {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const a = e.target.closest('a[href]');
      if (!a || a.hasAttribute('download') || (a.target && a.target !== '_self')) return;
      const raw = a.getAttribute('href');
      if (!raw || raw.startsWith('#')) return; // sayfa içi çapalar Lenis'te

      let url;
      try { url = new URL(a.href, window.location.href); } catch (err) { return; }
      if (!/^https?:|^file:/.test(url.protocol) || url.origin !== window.location.origin) return; // mailto, dış site

      // Aynı sayfa: çapaya ya da en üste yumuşak kay
      if (url.pathname === window.location.pathname) {
        e.preventDefault();
        const target = url.hash && document.querySelector(url.hash);
        const header = document.getElementById('site-header');
        const offset = -(header ? header.offsetHeight : 0) - 16;
        if (lenis) lenis.scrollTo(target || 0, { offset: target ? offset : 0 });
        else window.scrollTo({ top: target ? target.getBoundingClientRect().top + window.scrollY + offset : 0, behavior: 'smooth' });
        return;
      }

      e.preventDefault();
      leaveTo(url.href);
    });

    // Geri/ileri ile önbellekten dönülürse (bfcache) sayfayı görünür hale getir
    window.addEventListener('pageshow', (e) => {
      if (!e.persisted) return;
      leaving = false;
      root.classList.remove('is-loading');
      pre.el.classList.remove('is-transition');
      gsap.set(['.site-header', 'main', '.site-footer'], { clearProps: 'transform,opacity,transformOrigin' });
      if (lenis) lenis.start();
      try { sessionStorage.removeItem('mw-nav'); } catch (err) { /* yok say */ }
    });
  }

  /* =======================================================
     15. Hakkımızda sayfası
     - Arka plandaki fotoğraf kaydırdıkça yavaşça kayar ve kararır
     - Hero'daki neon gradient kaydırmayla ters yönde akar (parallax)
     - Cam kartlar alttan sırayla gelir, köşe çizimleri çizilir
     - Büyük cümlenin kelimeleri kaydırdıkça tek tek aydınlanır
       (.statement-cta eklenirse en sonda o da belirir)
     ======================================================= */
  function initAbout() {
    const page = document.querySelector('.about');
    if (!page || !hasScrollTrigger) return;

    const hero = page.querySelector('.about-hero');
    const photo = document.querySelector('.about-photo img');
    const dim = document.querySelector('.about-photo-dim');
    const glow = page.querySelector('.about-hero-glow');

    // Cümleyi kelimelere böl (vurgulu <span data-accent> korunur)
    const text = page.querySelector('.statement-text');
    const words = [];
    if (text) {
      const wrapWords = (node) => {
        Array.from(node.childNodes).forEach((child) => {
          if (child.nodeType === Node.TEXT_NODE) {
            const frag = document.createDocumentFragment();
            child.textContent.split(/(\s+)/).forEach((part) => {
              if (!part) return;
              if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
              const w = document.createElement('span');
              w.className = 's-word';
              w.textContent = part;
              frag.appendChild(w);
              words.push(w);
            });
            child.replaceWith(frag);
          } else if (child.nodeType === Node.ELEMENT_NODE) {
            wrapWords(child);
          }
        });
      };
      wrapWords(text);
    }

    if (reduceMotion) return; // fotoğraf sabit, kelimeler tam görünür

    // Fotoğraf: hero boyunca aydınlık, sonra kararır; tüm sayfa boyunca yavaş kayar
    if (dim) {
      gsap.fromTo(dim, { opacity: 0 }, {
        opacity: 0.8, ease: 'none',
        scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom 20%', scrub: true },
      });
    }
    if (photo) {
      gsap.fromTo(photo, { yPercent: 3, scale: 1.08 }, {
        yPercent: -3, scale: 1, ease: 'none',
        scrollTrigger: { start: 0, end: 'max', scrub: true },
      });
    }
    if (glow) {
      gsap.to(glow, {
        yPercent: 35, xPercent: -8, ease: 'none',
        scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true },
      });
    }

    // Cam kartlar + köşe çizimleri
    const cards = gsap.utils.toArray('.glass-card');
    if (cards.length) {
      gsap.set(cards, { y: 60, opacity: 0 });
      cards.forEach((card) => {
        const art = card.querySelectorAll('.glass-art *');
        prepDraw(Array.from(art));
      });
      window.ScrollTrigger.batch(cards, {
        start: 'top 88%',
        once: true,
        onEnter: (batch) => {
          gsap.to(batch, { y: 0, opacity: 1, duration: 0.9, stagger: 0.12, ease: 'power3.out', overwrite: 'auto' });
          batch.forEach((card, i) => {
            gsap.to(card.querySelectorAll('.glass-art *'), {
              strokeDashoffset: 0, duration: 1.2, stagger: 0.05, delay: 0.3 + i * 0.12, ease: 'power2.out',
            });
          });
        },
      });
    }

    // Büyük cümle: kelimeler sırayla aydınlanır, sonra buton belirir
    const statement = page.querySelector('.statement');
    const cta = page.querySelector('.statement-cta');
    if (statement && words.length) {
      gsap.set(words, { opacity: 0.14 });
      if (cta) gsap.set(cta, { opacity: 0, y: 30, scale: 0.94 });
      const tl = gsap.timeline({
        scrollTrigger: { trigger: statement, start: 'top top', end: 'bottom bottom', scrub: 0.5 },
      });
      tl.to(words, { opacity: 1, duration: 0.3, stagger: 0.12, ease: 'none' });
      if (cta) tl.to(cta, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: 'power2.out' }, '+=0.1');
      tl.to({}, { duration: 0.3 }); // buton belirdikten sonra kısa bekleme
    }
  }

  /* =======================================================
     Başlatma sırası
     ======================================================= */
  const lenis = initLenis();
  initBackground();
  initCursor();
  initScrollUi();
  const bg = initHeroCanvas();
  const slider = initSlider(bg);
  initProcess();
  initSequence();
  initReveals();
  initValueCards();
  initMagnetic();
  initAbout();

  runPreloader(lenis, () => {
    if (slider) slider.start();
    initPageIntro();
  });
  initPageTransitions(lenis); // preloader parçaları hazırlandıktan sonra

  // Yazı tipleri ve görseller geç yüklenirse sayfa yüksekliği değişir;
  // kaydırma tetikleyicilerinin konumlarını yeniden hesapla.
  if (hasScrollTrigger) {
    const refresh = () => window.ScrollTrigger.refresh();
    window.addEventListener('load', refresh);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(refresh);
  }
})();
