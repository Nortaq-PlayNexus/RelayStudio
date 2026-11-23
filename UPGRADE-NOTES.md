# Relay Studio 02 — upgrade notes

## Design
Rebuilt the client around a warm editorial visual language, expressive typography, quiet panels, compact desktop controls, and original terracotta sculpture. Three complete themes: **Porcelain**, **Obsidian**, **Sage**. Theme changes update the interface and 3D material. No Anthropic logos or product identity are used; Relay is not affiliated with Anthropic.

## Original 3D renderer
`public/sculpture.js` generates tubular meshes along mathematical curves and shades them with a small WebGL pipeline. Orbit and Knot use distinct knot-like curves; Bloom uses a five-lobed ring. Geometry and shaders ship with the source—no asset licences, network libraries, model downloads, or external images are required.

The object is truly 3D, not a pre-rendered image. Pointer drag rotates it; three buttons change form, pause motion, and disable rendering. Lighting and material are intentionally warm and slightly rough.

### Performance choices
- 24 FPS animation cap; no render loop while paused, offscreen, or document-hidden.
- Reduced-motion preference produces a static render; pointer exploration remains possible.
- Low-power mode replaces WebGL drawing with a static typographic form. Theme/low-power preferences persist when permitted.
- `powerPreference: low-power`, bounded mesh size, and a maximum 1.5× render pixel ratio.
- No continuous reflow or repository indexing to support the visual effect.
- A static fallback when WebGL is unavailable.

**Important:** these are implementation choices, not a CPU/RAM benchmark. Actual use depends on device, graphics drivers, browser, and view size. Software-rendered WebGL can be costly. Enable low-power mode on constrained machines. This visual enhancement does not change where model inference runs.

## Workflow upgrades
| Area | Added capability |
|---|---|
| Conversations | Session switching and restoration, 12-session/40-turn caps, independent model histories |
| Search | Ctrl K palette searches actions and full conversation text |
| Replies | Safe Markdown subset, code controls, copy/download, code-to-review |
| Context | Source file list and plain-text preview; selected-only live transmission |
| Review | Before/after editors, local LCS line diff, approval invalidation, download gate |
| Modes | Ask, Plan, Review instructions; never mislabelled as autonomous tools |
| Accessibility | Keyboard palette navigation, reduced-motion handling, accessible mobile navigation labels |
| Windows setup | Loopback-bound `.cmd` launcher; no automatic dependency installation |

## What remains deliberately out of scope
No compiled Windows installer, native credential vault, filesystem write access, command runner, autonomous agent tools, Git commits, sandboxed execution service, or remote development machine. The local review download is not a filesystem patch operation. The original DESIGN.md explains the proposed native evolution and remote-compute trade-offs.

Real inference integration remains opt-in via user key. No provider key was supplied during this upgrade, so actual model latency and quality remain unverified. Browser streaming tests use mocked SSE, not a live provider.

## Files
- `Relay-Studio.html`: self-contained, demo-only preview.
- `server.mjs` + `public/`: runnable local server and upgraded source.
- `Start-Relay.cmd`: optional Windows browser launcher.
- `tests.mjs`: current upgrade regression tests.
- `README.md`: setup and data/security boundaries.
- `DESIGN.md`: underlying provider research and proposed native architecture.
- `TEST-RESULTS.md`: tested and untested scope.
