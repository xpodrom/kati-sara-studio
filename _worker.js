const ADMIN_PASS = '112123'; // .ערך ציבורי — סדר גודל הגנה בסיסי; משתנה בקובץ זה בלבד

// Kati Sara — Pages _worker.js
// GET  /api/prices  → { groups: [...] } מ-KV (או null אם טרם נשמר)
// POST /api/prices  → ← גוף { groups: [...] } + header x-admin-pass (דורש סיסמה)
// /admin/*          → static admin.html
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/prices') {
      if (request.method === 'GET') {
        let data = null;
        try { data = await env.PRICES_KV.get('prices'); } catch (e) { data = null; }
        return new Response(data || '{"groups":null}', {
          headers: { 'content-type': 'application/json;charset=utf-8', 'cache-control': 'no-store' },
        });
      }
      if (request.method === 'POST') {
        if (request.headers.get('x-admin-pass') !== ADMIN_PASS) {
          return new Response('unauthorized', { status: 401 });
        }
        const body = await request.text();
        try {
          const parsed = JSON.parse(body);
          if (!parsed || !Array.isArray(parsed.groups)) {
            return new Response('bad payload', { status: 400 });
          }
          await env.PRICES_KV.put('prices', JSON.stringify(parsed));
          return new Response('ok');
        } catch (e) {
          return new Response('bad json', { status: 400 });
        }
      }
      return new Response('method not allowed', { status: 405 });
    }
    if (url.pathname === '/admin' || url.pathname.startsWith('/admin/')) {
      const assetUrl = new URL(request.url);
      assetUrl.pathname = '/admin.html';
      const res = await env.ASSETS.fetch(new Request(assetUrl, { method: 'GET' }));
      return withNoStore(res);
    }
    const res = await env.ASSETS.fetch(request);
    return withNoStore(res);
  },
};

function withNoStore(res) {
  const h = new Headers(res.headers);
  h.set('cache-control', 'no-store, must-revalidate');
  return new Response(res.body, { status: res.status, headers: h });
}
