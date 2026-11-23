# Development

## Prerequisites

- Windows 11 x64 for desktop acceptance testing (the app targets Windows 11 x64).
- Node.js 20+ for browser prototype and syntax checks.
- Electron 45.x for desktop shell development.
- Optional: Playwright + matching Electron test runtime for `desktop/tests.mjs`.

## Browser prototype

```powershell
cd RelayStudio
$env:HOST="127.0.0.1"
node server.mjs
# http://127.0.0.1:3000
```

No npm install required. Use `Ctrl+C` to stop.

## Desktop shell

```powershell
npm install --no-save electron@45.4.1
npx electron desktop
```

The desktop app loads `relay://app/index.html`, not the HTTP server.

## Checks

```powershell
node --check server.mjs
node --check tests.mjs
node --check public/app.js
node --check public/sculpture.js
node --check public/polish.js
node --check public/desktop-ui.js
node --check desktop/main.cjs
node --check desktop/preload.cjs
node --check desktop/security.cjs
node --check desktop/tests.mjs
```

Pure security guard smoke:

```powershell
node -e "const S=require('./desktop/security.cjs'); const assert=require('node:assert/strict'); assert.throws(()=>S.provider('__proto__')); console.log('ok')"
```

## Desktop test suite

`desktop/tests.mjs` runs Playwright Electron tests. In the original delivery environment it used a Linux Electron runtime with mocked dialogs and mocked SSE. See `docs/release/TEST-REPORT-DESKTOP.md` for what passed and what was not verified on Windows.

## Project layout

```text
desktop/      Electron main/preload/security/packaging/tests
public/       Shared UI (browser + desktop renderer)
docs/         Architecture, deployment, security, release artifacts, screenshots
server.mjs    Browser prototype server
tests.mjs     Browser prototype tests
```
