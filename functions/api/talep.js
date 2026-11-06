// Teklif formunun arka plan kaydı (Cloudflare Pages Function: POST /api/talep).
//
// Ziyaretçinin tarayıcısı formu her zamanki gibi Web3Forms'a (info@ e-postası) gönderirken aynı içeriği arka
// planda buraya da yollar. Bu fonksiyon talebi gizli anahtarla ModWare Panel'e iletir; panel talebe numara
// verir ve personel orada takip eder. Ziyaretçi bunu görmez; panele ulaşılamazsa form yine çalışır.
//
// Ayarlar (Cloudflare > Workers & Pages > modware-technology > Settings > Variables and Secrets):
//   TEKLIF_URL      panelin talep alma adresi (…/api/ic/talep)
//   TALEP_ANAHTARI  gizli; paneldeki TALEP_ANAHTARI ile aynı değer

const ALANLAR = ['konu', 'urun', 'aciklama', 'adet', 'asama', 'butce', 'zaman', 'ad', 'sirket', 'telefon', 'referans'];

const yanit = (durum) => new Response(null, { status: durum, headers: { 'Cache-Control': 'no-store' } });

export async function onRequestPost({ request, env }) {
  if (!env.TEKLIF_URL || !env.TALEP_ANAHTARI) return yanit(503);

  // Yalnızca bu sitenin kendi sayfalarından gelen istek (başka bir site ziyaretçinin tarayıcısını kullanamaz)
  const origin = request.headers.get('origin');
  if (origin && origin !== new URL(request.url).origin) return yanit(403);
  if (!(request.headers.get('content-type') || '').includes('application/json')) return yanit(415);

  const metin = await request.text();
  if (metin.length > 20000) return yanit(413);
  let f;
  try {
    f = JSON.parse(metin);
  } catch {
    return yanit(400);
  }
  if (!f || typeof f !== 'object' || Array.isArray(f)) return yanit(400);

  // Görünmez bot tuzağı işaretlenmişse sessizce yok sayılır (Web3Forms da aynısını yapar)
  if (f.botcheck) return yanit(204);

  // Yalnızca form alanları geçer; Web3Forms anahtarı gibi diğer her şey burada kalır
  const talep = {};
  for (const a of ALANLAR) if (typeof f[a] === 'string') talep[a] = f[a];
  talep.eposta = typeof f.email === 'string' ? f.email : '';
  talep.kvkk_onay = f.onay === 'evet' || f.onay === 'yes';
  talep.dil = f.dil === 'en' ? 'en' : 'tr';
  if (typeof f.sayfa === 'string') talep.sayfa = f.sayfa.slice(0, 300);

  try {
    const r = await fetch(env.TEKLIF_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Talep-Anahtari': env.TALEP_ANAHTARI,
        'X-Ziyaretci-IP': request.headers.get('cf-connecting-ip') || '',
      },
      body: JSON.stringify(talep),
    });
    if (r.ok) return yanit(204);
    return yanit(r.status === 429 ? 429 : 502);
  } catch {
    return yanit(502);
  }
}
