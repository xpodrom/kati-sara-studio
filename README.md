# Kati Sara Studio — Site

Cinematic one-page site for a permanent makeup studio (Ashkelon).
Stack: vanilla HTML + Three.js (WebGL) + custom GLSL shaders. Zero build step.

## Local preview
Open `index.html` in a browser (or `python3 -m http.server`).

## Deploy targets
| Env | URL | Address |
|---|---|---|
| **Production (Cloudflare Pages)** | https://kati-sara.pages.dev | kati-sara.pages.dev |
| Production (Vercel, legacy) | https://kati-sara.vercel.app | kati-sara.vercel.app |
| QA (Vercel) | https://kati-sara-qa.vercel.app | kati-sara-qa.vercel.app |

## Workflow — one PR per change
1. `git checkout -b features/<change>` — edit `index.html`
2. Commit with a clear `feat:`/`fix:`/`docs:` message
3. Push the branch, open a PR to `main`
4. After review/merge, deploy (both targets) and reply to the user with links

## Deploy — Cloudflare Pages (primary)
Direct-upload pipeline via Cloudflare API (account `d99ba68591e145e25a9db1a71d95e7b8`,
project `kati-sara`, production branch `main`). Needs a token with
**Account → Cloudflare Pages → Edit**.

```
ACC=d99ba68591e145e25a9db1a71d95e7b8
H=$(python3 -c $'import blake3,base64\nraw=open("index.html","rb").read()\nb64=base64.b64encode(raw).decode()\nprint(blake3.blake3((b64+"html").encode()).hexdigest()[:32])')

# 1. upload-token
JWT=$(curl -s -H "Authorization: Bearer $CF_TOKEN" \
  https://api.cloudflare.com/client/v4/accounts/$ACC/pages/projects/kati-sara/upload-token \
  | jq -r .result.jwt)

# 2. upload missing assets
B64=$(base64 -w0 index.html)
curl -s -X POST -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" \
  https://api.cloudflare.com/client/v4/pages/assets/upload \
  -d "[{\"key\":\"$H\",\"value\":\"$B64\",\"metadata\":{\"contentType\":\"text/html\"},\"base64\":true}]"

# 3. create deployment (manifest = path -> hash)
curl -s -X POST -H "Authorization: Bearer $CF_TOKEN" \
  https://api.cloudflare.com/client/v4/accounts/$ACC/pages/projects/kati-sara/deployments \
  -F "branch=main" -F "manifest={\"/index.html\":\"$H\"}"
```

Notes:
- Hash algorithm: `blake3(base64(bytes) + extension).hex[:32]` (same as wrangler).
- Verify every deploy afterwards: HTTP 200 + content markers + size of index.

## Deploy — Vercel (legacy / backup)
Vercel free tier is **not licensed for commercial use** — kept only as backup.
Current pipeline: `DEPLOY_TO_VERCEL` (name=kati-sara / kati-sara-qa, target=production),
verify live fetch (HTTP 200 + content markers), reply with links per user convention.

## Legacy assets (`legacy/`)
Recovered from the user's old repo (archived here):
- `logo.svg` — official vector logo (integrate into the site — pending)
- `prices.json` — old site price table (42 entries, from/to ranges; Hebrew)
- `JsonDb.js` + `LanguageTranslate.js` — trilingual content DB (he/en/ru)
- `old-site-index.html` — the full previous site
