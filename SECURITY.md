# Security Policy

## Reporting

Do not open public issues for suspected vulnerabilities. Report privately to the maintainer via GitHub private vulnerability reporting if enabled, or contact Nortaq-PlayNexus directly.

Include: affected version/file, reproduction steps, impact, and any suggested mitigation.

## Scope

In scope:
- Renderer/preload/main-process boundary issues
- IPC validation/caller bypass
- Path traversal or workspace escape
- Unsafe external navigation or protocol handling
- Credential storage/handling issues
- CSP/sandbox weakening
- Archive/import injection or unsafe rendering

Out of scope:
- Vulnerabilities in upstream Electron/Chromium/NSIS not caused by this repo's configuration
- Social engineering, physical access, or compromised same-user OS accounts
- Provider-side issues (Groq/OpenRouter)
- Claims that require bypassing Windows policy to run unsigned software

## Supported versions

| Version | Supported |
|---|---|
| 0.4.x | Evaluation/security fixes as time permits |
| < 0.4.0 | No |

## Security notes

This is an unsigned evaluation build. It has not received an independent security audit or penetration test. Windows DPAPI behaviour and Windows installer execution were not validated in the delivery environment; see `TEST-REPORT-DESKTOP.md`.
