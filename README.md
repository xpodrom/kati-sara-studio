[![Live](https://img.shields.io/endpoint?url=https%3A%2F%2Fkati-sara.pages.dev%2Fapi%2Fstatus.json&cacheSeconds=60)](https://kati-sara.pages.dev)
[![Stack: Three.js](https://img.shields.io/badge/3D-Three.js-black?logo=three.js)](#)
[![Shaders: GLSL](https://img.shields.io/badge/Shaders-GLSL-orange)](#)
[![Smooth scroll: Lenis](https://img.shields.io/badge/Smooth_scroll-Lenis-blue)](#)
[![Hosted: Cloudflare Pages](https://img.shields.io/badge/Hosting-Cloudflare%20Pages-orange?logo=cloudflare)](#)
[![QA: automated](https://img.shields.io/badge/QA-automated_mobile_scan-brightgreen)](#)

# Kati Sara Studio — Site

Cinematic one-page commercial site for a permanent-makeup studio in Ashkelon.
**Live: https://kati-sara.pages.dev** · Admin dashboard: `/admin`

## What's inside
- **Hero**: full-bleed animated logo (official SVG emblem) with halo + orbiting gold rings
- **3D cinema background**: Three.js WebGL — dark silk fog shader + gold spark particles that twinkle and glow stronger while scrolling
- **Post-processing**: UnrealBloom, chromatic aberration (scroll-velocity driven), vignette
- **Buttery scroll** via Lenis (with non-WebGL fallback)
- **Full Hebrew/RTL**: `dir="rtl"`, logical CSS props, LTR runs for Latin text
- **Services · Process · Price list · Waze deep navigation** (exact coordinates + `navigate=yes`)
- **Admin dashboard** (password-protected): every text, service, journey step, price row and disclaimers editable; gallery frames with **image uploads** stored in Workers KV; business settings (phone, WhatsApp prefill, 2 Instagram profiles, Facebook, Waze URL) applied across the site on the fly
- **SEO/AI**: canonical, OpenGraph/Twitter, `robots.txt`, `sitemap.xml`, LocalBusiness JSON-LD structured data, `llms.txt` for AI crawlers

## Stack & architecture
Vanilla ESM (no build step) + Three.js r160 (importmap) + Lenis + custom GLSL shaders.
Backend: Cloudflare Pages `_worker.js` —
- `GET /api/content` full site content (KV)
- `POST /api/content` save content (password header)
- `GET/POST /api/img/:key` gallery images in KV (base64)
- `GET /api/prices` / `POST /api/prices` price list (KV)
- `GET /api/status.json` live-status badge JSON for the shields.io badge above

## QA gate (before any deploy is reported)
`qa/scan.js` auto-scans the live site on an iPhone-emulated browser: console/page
errors, layout probe (island/hero/logo/prices/CTA), horizontal overflow threshold
and a **DOM drift detector** (x-position sampling over 3s). Deployments ship only
when the scan is `QA CLEAN`.

## Repo layout
```
index.html      the site
admin.html      admin dashboard
_worker.js      Pages Functions (content/prices/images/status)
legacy/         recovered assets from the old site (logo.svg, trilingual DB, old price tables)
qa/             automated QA toolkit (scan.js + setup.sh)
```

## Local preview
Open `index.html` in a browser or `python3 -m http.server`.

## Credits
Design & development: built end-to-end with Hermes Agent.
