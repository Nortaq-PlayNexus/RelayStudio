# Contributing to Relay Studio

## Scope

Relay Studio is an unsigned desktop evaluation build. Contributions should preserve the existing security boundaries: isolated renderer, restricted preload bridge, fixed provider/model allowlists, no shell execution, no autonomous writes.

## Local setup

```powershell
git clone https://github.com/Nortaq-PlayNexus/RelayStudio.git
cd RelayStudio
node server.mjs
```

Open `http://127.0.0.1:3000` for the browser prototype. No npm install is required for the prototype.

For the Electron desktop shell, install Electron 45.x and launch from `desktop/`:

```powershell
npm install --no-save electron@45.4.1
npx electron desktop
```

## Checks

```powershell
node --check server.mjs
node --check public/app.js
node --check public/desktop-ui.js
node --check desktop/main.cjs
node --check desktop/preload.cjs
node --check desktop/security.cjs
```

The full Electron desktop test suite (`desktop/tests.mjs`) requires Playwright and a matching Electron test runtime; see `TEST-REPORT-DESKTOP.md`.

## Pull requests

- Keep changes focused.
- Do not weaken CSP, sandbox, IPC caller checks, or provider/model allowlists without explicit justification.
- Do not add telemetry, background uploads, shell execution, or autonomous file writes.
- Update docs/tests when behavior changes.
- Describe what was tested and what was not tested on Windows.
