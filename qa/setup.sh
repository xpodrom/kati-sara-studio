#!/usr/bin/env bash
# QA environment bootstrap (sandbox-safe: no root, no system packages)
# Sets up: node deps (playwright-core) + chromium headless shell + missing shared libs
set -e
cd "$(dirname "$0")/.."   # repo root

echo "==> node deps"
[ -d /tmp/qa_node ] || npm init -y >/dev/null 2>&1
npm install playwright-core --prefix /tmp/qa_node >/dev/null
export NODE_PATH=/tmp/qa_node/node_modules

echo "==> chromium headless shell"
npx playwright-core install chromium-headless-shell 2>&1 | tail -1

BIN=~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell
MISSING=$(LD_LIBRARY_PATH=~/.qa-libs/root/usr/lib/x86_64-linux-gnu ldd $BIN 2>/dev/null | grep "not found" | awk '{print $1}' | sort -u || true)
if [ -n "$MISSING" ]; then
  echo "==> downloading missing libs (DMZ mirror, to ~/.qa-libs)"
  mkdir -p ~/.qa-libs/root && cd ~/.qa-libs
  MIRROR=https://deb.debian.org/debian
  curl -s -m 30 "$MIRROR/dists/trixie/main/binary-amd64/Packages.gz" -o Pk.gz
  zcat Pk.gz > Packages.txt
  for lib in $MISSING; do
    for pkg in $(grep -oE "^Package: [a-z0-9.+-]+t64?$" Packages.txt | cut -d' ' -f2 | grep -iE "$(echo $lib | cut -d. -f1 | tr 'A-Z' 'a-z' | sed 's/^lib//')" | head -4); do
      f=$(grep -A20 "^Package: $pkg\$" Packages.txt | grep "^Filename:" | head -1 | cut -d' ' -f2)
      [ -n "$f" ] && curl -s -m 60 "$MIRROR/$f" -o "$pkg.deb" && dpkg-deb -x "$pkg.deb" ~/.qa-libs/root 2>/dev/null && echo "added $pkg (for $lib)"
    done
  done
  cd - >/dev/null
fi

echo "==> verify"
LD_LIBRARY_PATH=~/.qa-libs/root/usr/lib/x86_64-linux-gnu $BIN --version
echo "READY. run: LD_LIBRARY_PATH=~/.qa-libs/root/usr/lib/x86_64-linux-gnu node qa/scan.js"
