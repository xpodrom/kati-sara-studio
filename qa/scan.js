#!/usr/bin/env node
/**
 * kati-sara QA scan — mobile-emulated website QA
 *
 * Checks (all against the LIVE url):
 *  1. console errors / page errors / failed requests
 *  2. layout probe: key elements' bounding boxes on iPhone viewport
 *  3. horizontal overflow scan (max right edge over all elements)
 *  4. DOM drift detector: x-positions of key elements sampled over ~3s (zero movement expected)
 *  5. screenshots: hero / mid / final
 *
 * Usage:
 *   node qa/scan.js [url]            (default https://kati-sara.pages.dev)
 *   LD_LIBRARY_PATH=~/.qa-libs/root/usr/lib/x86_64-linux-gnu node qa/scan.js
 */
const { chromium, devices } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const URL = process.argv[2] || 'https://kati-sara.pages.dev';
const OUT = '/tmp/qa_out';
fs.mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ ...devices['iPhone 11'], locale: 'he-IL' });
  const page = await ctx.newPage();

  const problems = [];
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 300)); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  page.on('requestfailed', r => problems.push('REQFAIL: ' + r.url().slice(0, 120) + ' ' + (r.failure() && r.failure().errorText || '')));

  await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2500);

  // ---- layout probe
  const probe = await page.evaluate(() => {
    const r = sel => { const el = document.querySelector(sel); if (!el) return 'MISSING';
      const b = el.getBoundingClientRect(); return { x: Math.round(b.x), right: Math.round(b.right), w: Math.round(b.width), top: Math.round(b.top) }; };
    return {
      vw: innerWidth,
      scrollW: document.documentElement.scrollWidth,
      island: r('#island'), giant: r('#s1 h1'), heroLogo: r('.hero-logo'),
      prc: r('#prc'), final: r('#s5'), gbtn: r('#s5 .gbtn'), wbtn: r('.wbtn'),
      dir: getComputedStyle(document.documentElement).direction,
    };
  });

  // ---- overflow scan
  const overflow = await page.evaluate(() => {
    let maxRight = 0, worst = '';
    document.querySelectorAll('main *, #island, #cut, footer *').forEach(el => {
      const b = el.getBoundingClientRect();
      if (b.right > innerWidth + 8 && b.width < innerWidth * 3) {
        if (b.right > maxRight) { maxRight = Math.round(b.right); worst = el.tagName + '.' + String(el.className).slice(0, 40); }
      }
    });
    return { maxRight, worst };
  });

  // ---- drift detector (DOM x over ~3s, zero motion expected within tolerance)
  const sels = ['#island', '#s1 h1', 'main', '#cut'];
  const track = await page.evaluate(async (sels) => {
    const xs = {}; sels.forEach(s => xs[s] = []);
    for (let k = 0; k < 10; k++) {
      sels.forEach(s => { const el = document.querySelector(s); if (el) xs[s].push(Math.round(el.getBoundingClientRect().x * 10) / 10); });
      await new Promise(r => setTimeout(r, 300));
    }
    return xs;
  }, sels);
  const drift = {};
  for (const s of sels) {
    const xs = track[s]; if (!xs || xs.length === 0) continue;
    const d = Math.round((Math.max(...xs) - Math.min(...xs)) * 10) / 10;
    drift[s] = d;
    if (Math.abs(d) > 2) problems.push(`DRIFT ${s}: x moves ${d}px over 3s`);
  }

  // ---- screenshots
  const spots = [['hero', 0], ['mid', 0.45], ['final', 1]];
  for (const [name, f] of spots) {
    if (f > 0) await page.evaluate(f => scrollTo({ top: (document.documentElement.scrollHeight - innerHeight) * f, behavior: 'instant' }), f);
    await page.waitForTimeout(1400);
    await page.screenshot({ path: path.join(OUT, `${name}.png`) });
  }

  // ---- report
  if (errors.length) problems.push('CONSOLE: ' + errors.join(' | '));
  if (overflow.maxRight > Math.round(probe.vw * 1.02)) problems.push(`OVERFLOW ${overflow.maxRight}px on ${overflow.worst}`);
  if (probe.prc === 'MISSING') problems.push('MISSING #prc (price section)');
  if (probe.wbtn === 'MISSING') problems.push('MISSING waze button');

  const report = { url: URL, time: new Date().toISOString(), probe, overflow, drift, problems, shots: OUT };
  console.log(JSON.stringify(report, null, 1));
  fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 2));
  console.log(problems.length === 0 ? '\n✅ QA CLEAN' : `\n❌ ${problems.length} problem(s)`);
  await browser.close();
  process.exit(problems.length === 0 ? 0 : 2);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
