# Desktop 0.4.0 — validation report
Date: 23 November 2026 in the user's timezone.

## Tested in the supplied build environment
Linux sandbox; official Electron **45.4.1** Linux x64 test runtime matched to the Windows runtime version; Playwright Electron driver; virtual X display. The Linux test launcher used `--no-sandbox` because of the sandbox host environment. **That flag is not included in the Windows installer, shortcuts, or shipped application launch configuration.** Renderer `sandbox: true`, `contextIsolation: true`, `nodeIntegration: false`, and `webSecurity: true` were verified as application preferences. Linux host tests do not establish Windows OS sandbox enforcement.

### Passed pure guard tests
- Fixed provider/model allowlists and invalid provider rejection.
- Workspace path boundary check; symlink escape rejection.
- Oversized source rejection and sensitive-looking filename filtering.
- Imported archive role validation; system messages rejected.

### Passed real Electron shell tests
- Actual Electron process launch and local custom-protocol page load.
- Renderer has no `require` or `process` global.
- Restricted native bridge info call and application preferences.
- Native bridge file/folder operations against real fixture files, using **mocked dialog selections**.
- Read-only workspace excludes dependency folders, hidden files, symlinks, and oversized sources.
- Opaque file IDs and rejection of arbitrary renderer path strings.
- Session-only provider key set/status/forget lifecycle.
- Protected-storage opt-in refused on the non-Windows test platform.
- Main-process direct provider transport exercised with **mocked SSE**, including selected source context and fixed endpoint assertion. No real provider API call or key was used.
- Native save bridge writes the selected fixture copy; cancel path returns without saving. Dialogs were mocked.
- Imported script-like text is inert; model history is not restored.
- Runtime diagnostics produce actual Electron process information.
- No uncaught renderer page errors in this test flow.

`xvfb-run -a node desktop/tests.mjs` reproduces these checks after installing the optional test dependency and downloading the matching Linux Electron runtime into the documented cache path. The application itself requires no Playwright or Python installation on Windows.

## Not yet verified
- Executing the installer, first launch, Start menu shortcuts, per-user installation, upgrade behaviour, or uninstall on an actual Windows 11 machine.
- Windows DPAPI encryption/decryption, saved-key restart behaviour, Windows security dialogs, Authenticode signing, and SmartScreen reputation.
- Actual native Windows dialog behaviour. Test selections were mocked in Linux.
- Real Groq/OpenRouter authentication, latency, rate-limit headers, billing tier, model quality, or long-running network cancellation.
- Windows RAM/CPU/GPU, battery impact, accessibility certification, or comparison against OpenCode.
- ARM64-native or 32-bit Windows support.
- Independent security audit, penetration test, or production update process.

## Distribution validation
The Windows runtime's SHA-256 was checked against the official release checksum listing. The Windows installer is compiled using NSIS on Linux and contains the complete official Windows x64 runtime, application source, and runtime licences. Final artifact byte counts, hashes, and the 100 MB target check are recorded separately in BUILD-REPORT.json. Archive structure/integrity checks are not a substitute for executing the installer on Windows.
