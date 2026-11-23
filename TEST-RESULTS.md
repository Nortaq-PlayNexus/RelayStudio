# Relay Studio 03 — delivery validation

Studio 03 regression checks also cover mobile navigation drawer, mode-menu selection, details overlay, focus mode, and Alt F restoration. The refined light/dark, mobile, review, and connection screens were visually inspected.

Date: 23 November 2026, user timezone. Environment: Linux sandbox, Node.js 20.20.2, headless Chromium/Playwright. WebGL control checks used Chromium's software graphics backend, not a Windows GPU benchmark.

## Passed automated checks
- Server, app, and 3D JavaScript syntax.
- Browser load with no uncaught JavaScript exceptions.
- Theme selection and reload persistence.
- WebGL canvas initialisation, pause state, form switching, low-power state.
- System reduced-motion preference starts with paused animation.
- Scripted demo completion and explicit demo label; no fabricated demo timing.
- Conversation creation, switching, transcript restoration.
- Command palette keyboard opening and full-text conversation search.
- Fenced code rendering and code-to-review action.
- Raw model HTML remains inert text, including script-like strings.
- Local line diff for the illustrative sample.
- Download blocked without review approval.
- Approved replacement download uses the expected filename.
- Editor changes clear approval and stale diff state.
- Source file selection, preview, review baseline, and removal.
- Consent required to enable live replies.
- Missing provider key produces an error, with no paid fallback.
- Mocked SSE parsing, usage metadata, answer display, and measured-timer UI path.
- Changing provider updates models and disables live mode.
- Cancellation stops scripted output and labels the partial reply.
- Mobile viewport width checks at 390 × 844 for Workbench, Project, Review, Connections.
- localStorage contains only theme and low-power preferences in the test session.
- Server rejects unsupported models/providers and cross-origin JSON requests.
- Self-contained file runs scripted code replies with zero HTTP resource requests.
- Self-contained file prevents live mode and directs users to the local server.
- Static visual fallback appears when WebGL is disabled.

## Additional visual checks
Desktop screenshots of Porcelain and Obsidian themes, plus mobile layout, were inspected. Original procedural meshes render in the desktop screenshots. External CDN/image/font dependencies are not used.

## Not validated
- Actual Groq/OpenRouter inference, authentication, token accounting, speed, or quality: no user key supplied.
- Performance against OpenCode, Windows CPU/RAM/working-set budgets, real-device graphics power use.
- Native Windows installer, WebView2 integration, Credential Manager, ARM64.
- Windows `.cmd` execution; launcher source is included but the build environment is Linux.
- Real filesystem changes, terminal execution, Git operations, remote host provisioning: not implemented.
- Production/multi-user security audit or accessibility certification.

`tests.mjs` can reproduce browser checks against a running local server. Mocked SSE and a rendered timer do not establish real provider latency.
