# Relay Studio Changelog

All notable changes to this repository package are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.4.0] — 2026-11-23

### Added
- Windows 11 x64 Electron 45.4.1 desktop shell with isolated renderer, local `relay://app/` protocol, restricted preload bridge, and CSP.
- Direct main-process provider transport to official Groq/OpenRouter endpoints with fixed model allowlists.
- Native file/folder dialogs, read-only workspace browsing with opaque file IDs and bounded traversal.
- Reviewed-save workflow with diff, explicit approval, native Save dialog, and replacement confirmation.
- Conversation export/import as JSON archives (no credential fields, no automatic model-history restore).
- Opt-in Windows-protected key storage via Electron safeStorage/DPAPI; session-only keys remain the default.
- Runtime diagnostics panel showing actual Electron process counts and summed working sets.
- Unsigned NSIS installer, SHA256 manifest, verify script, and test/build reports.

### Security / Boundaries
- No shell execution bridge, remote code loader, telemetry collector, automatic updater, or autonomous patch/apply flow.
- Renderer context isolation, sandbox, and Node integration disabled in shipped configuration.
- External links limited to official-domain allowlist with confirmation dialog.

### Known limitations
- Unsigned evaluation build; Windows installer/DPAPI/SmartScreen not executed on a real Windows 11 machine in the build environment.
- Native dialog behaviour mocked in Linux Electron tests.
- No real provider inference benchmark or billing/quota validation in delivery.
- No independent security audit, penetration test, or production update process.
