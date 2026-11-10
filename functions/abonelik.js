// Tanıtım e-postalarındaki "listeden çık" bağlantısı (Cloudflare Pages Function: GET/POST /abonelik).
//
// ModWare Panel'den giden tanıtım e-postalarının sonunda modwaretechnology.com/abonelik?k=…&i=… bağlantısı
// bulunur. Bu fonksiyon isteği olduğu gibi panelin /abonelik sayfasına iletir ve sayfayı geri döndürür;
// alıcı panelin adresini görmez. Bağlantıyı panel imzalar ve doğrular; burada gizli bir değer yoktur.
// Gmail/Yahoo'nun "tek tıkla abonelikten çık" isteği (POST) da aynı yoldan geçer.
//
// Ayar: teklif formunun kullandığı TEKLIF_URL (…/api/ic/talep); panel kökü buradan alınır.

const CSP = "default-src 'none'; style-src 'unsafe-inline'; img-src 'none'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'";

function sayfa(durum, metin) {
  return new Response(`<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Listeden çık</title></head><body style="font-family:system-ui,sans-serif;padding:40px 16px;max-width:460px;margin:auto"><p>${metin}</p></body></html>`, {
    status: durum, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'Content-Security-Policy': CSP, 'X-Robots-Tag': 'noindex' },
  });
}

export async function onRequest({ request, env }) {
  if (request.method !== 'GET' && request.method !== 'POST') return new Response(null, { status: 405, headers: { Allow: 'GET, POST' } });
  if (!env.TEKLIF_URL) return sayfa(503, 'Şu anda işlem yapılamıyor. Listeden çıkmak için e-postayı yanıtlamanız yeterli.');
  const hedef = new URL('/abonelik', env.TEKLIF_URL);
  hedef.search = new URL(request.url).search;
  const govde = request.method === 'POST' ? await request.text() : undefined;
  if (govde && govde.length > 2000) return sayfa(413, 'Geçersiz istek.');
  try {
    const r = await fetch(hedef, {
      method: request.method,
      headers: govde !== undefined ? { 'Content-Type': request.headers.get('content-type') || 'application/x-www-form-urlencoded' } : {},
      body: govde,
      redirect: 'manual',
    });
    return new Response(await r.text(), {
      status: r.status,
      headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'Content-Security-Policy': CSP, 'X-Robots-Tag': 'noindex', 'Referrer-Policy': 'no-referrer' },
    });
  } catch {
    return sayfa(502, 'Şu anda işlem yapılamıyor. Listeden çıkmak için e-postayı yanıtlamanız yeterli.');
  }
}
