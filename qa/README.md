# QA toolkit

Automated mobile QA for the site — no human eyeballs required to catch regressions.

## One-time setup (sandbox-safe, no root)
```bash
bash qa/setup.sh
```

## Run a full scan
```bash
NODE_PATH=/tmp/qa_node/node_modules LD_LIBRARY_PATH=~/.qa-libs/root/usr/lib/x86_64-linux-gnu node qa/scan.js [url]
```

What it checks and reports (`/tmp/qa_out/report.json` + screenshots):
1. **Console/page errors** — any JS failure kills the cinema engine silently on phones; this catches it
2. **Layout probe** — bounding boxes of island / hero title / hero logo / price section / CTA / Waze button
3. **Horizontal overflow** — element max right-edge vs viewport (fail threshold = vw + 2%)
4. **DOM drift detector** — x-position of key nodes sampled over 3s; any movement > 2px = FAIL
   (this is how the real RTL scrollX oscillation bug was found: scrollX jumped to -178px every ~2.5s)
5. **Screenshots** — hero / mid / final for visual review

Exit code: 0 = clean, 2 = problems found.

## Deploy gate (rule)
After every deploy: `node qa/scan.js https://kati-sara.pages.dev` must be QA CLEAN
before reporting the deploy as done. Additionally curl-verify: HTTP 200 on `/`
and `/legacy/logo.svg`, and size of index within ±5% of previous verified size.
