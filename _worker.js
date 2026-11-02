/* Kati Sara — Pages _worker.js (content + prices + images) */
const ADMIN_PASS = '112123';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/api/content') {
      if (request.method === 'GET') {
        let data = null;
        try { data = await env.PRICES_KV.get('content'); } catch (e) {}
        return new Response(data || '{}', {
          headers: { 'content-type': 'application/json;charset=utf-8', 'cache-control': 'no-store' },
        });
      }
      if (request.method === 'POST') {
        if (request.headers.get('x-admin-pass') !== ADMIN_PASS) return new Response('unauthorized', { status: 401 });
        const body = await request.text();
        try {
          const parsed = JSON.parse(body);
          if (typeof parsed !== 'object' || !parsed) return new Response('bad payload', { status: 400 });
          await env.PRICES_KV.put('content', JSON.stringify(parsed));
          return new Response('ok');
        } catch (e) { return new Response('bad json', { status: 400 }); }
      }
      return new Response('method not allowed', { status: 405 });
    }

    if (url.pathname === '/api/prices') {
      if (request.method === 'GET') {
        let groups = [];
        try {
          const c = JSON.parse((await env.PRICES_KV.get('content')) || '{}');
          groups = c.groups || [];
        } catch (e) {}
        if (groups.length === 0) {
          try {
            const legacy = JSON.parse((await env.PRICES_KV.get('prices')) || '{"groups":[]}');
            groups = legacy.groups || [];
          } catch (e) {}
        }
        return new Response(JSON.stringify({ groups }), {
          headers: { 'content-type': 'application/json;charset=utf-8', 'cache-control': 'no-store' },
        });
      }
      if (request.method === 'POST') {
        if (request.headers.get('x-admin-pass') !== ADMIN_PASS) return new Response('unauthorized', { status: 401 });
        const body = await request.text();
        try {
          const parsed = JSON.parse(body);
          if (!Array.isArray(parsed.groups)) return new Response('bad payload', { status: 400 });
          let cur = {};
          try { cur = JSON.parse((await env.PRICES_KV.get('content')) || '{}'); } catch (e) {}
          cur.groups = parsed.groups;
          await env.PRICES_KV.put('content', JSON.stringify(cur));
          return new Response('ok');
        } catch (e) { return new Response('bad json', { status: 400 }); }
      }
      return new Response('method not allowed', { status: 405 });
    }

    // GET /api/img/<key> - serve stored image bytes
    if (url.pathname.startsWith('/api/img/')) {
      const key = url.pathname.replace('/api/img/', '');
      if (!key) return new Response('bad request', { status: 400 });
      let data = null;
      try { data = await env.PRICES_KV.get('img_' + decodeURIComponent(key)); } catch (e) {}
      if (!data) return new Response('not found', { status: 404 });
      let obj = null;
      try { obj = JSON.parse(data); } catch (e) {}
      if (!obj || !obj.b64) return new Response('not found', { status: 404 });
      const bytes = Uint8Array.from(atob(obj.b64), c => c.charCodeAt(0));
      return new Response(bytes, { headers: { 'content-type': obj.mime || 'image/jpeg', 'cache-control': 'no-store' } });
    }

    // POST /api/img/<key> - upload: { mime, b64 }
    if (url.pathname.startsWith('/api/img/') && request.method === 'POST') {
      if (request.headers.get('x-admin-pass') !== ADMIN_PASS) return new Response('unauthorized', { status: 401 });
      const key = url.pathname.replace('/api/img/', '');
      if (!key) return new Response('bad request', { status: 400 });
      const body = await request.text();
      try {
        const obj = JSON.parse(body);
        if (!obj.b64) return new Response('bad payload', { status: 400 });
        await env.PRICES_KV.put('img_' + key, JSON.stringify(obj));
        return new Response('ok');
      } catch (e) { return new Response('bad json', { status: 400 }); }
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
