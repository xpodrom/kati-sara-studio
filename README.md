# Kati Sara Studio — Site

Cinematic one-page site for a permanent makeup studio (Ashkelon).
Stack: vanilla HTML + Three.js (WebGL) + custom GLSL shaders. Zero build step.

## Local preview
Open `index.html` in a browser (or `python3 -m http.server`).

## Deploy targets
| Env | URL | Address |
|---|---|---|
| Production | https://kati-sara.vercel.app | kati-sara.vercel.app |
| QA | https://kati-sara-qa.vercel.app | kati-sara-qa.vercel.app |

Deploy steps (current, Vercel MCP):
1. Edit `index.html`
2. `DEPLOY_TO_VERCEL` (name=kati-sara → prod, name=kati-sara-qa → QA, target=production)
3. Verify live fetch (HTTP 200 + content markers)
4. Reply to user with deployment URL + alias

Coming: GitHub repo as source of truth (PR-per-change), Cloudflare Pages migration (commercial-friendly free tier).
