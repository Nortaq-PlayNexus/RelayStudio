# Security

## Threat model summary

Relay Studio handles user-selected source text and optional provider API keys. The main risks are: renderer compromise, IPC misuse, path traversal/workspace escape, unsafe file writes, credential exposure, malicious imported/exported content, and unsafe external navigation.

## Controls present

| Risk | Control |
|---|---|
| Renderer compromise | `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`, `webSecurity: true` |
| Untrusted IPC | `caller()` checks sender, main frame, and `relay://app/index.html` URL |
| Arbitrary file access | Native dialogs; workspace reads by opaque ID; `realpath` + `within()` boundary; extension/size/name checks |
| Large/binary input | 12 KB file limit, 24 KB selected context, binary/null-byte rejection, bounded archive size |
| Credential leakage | Keys not returned to renderer; session-only default; opt-in Windows safeStorage/DPAPI; no key in exports |
| Unsafe writes | Native Save dialog; existing-file replace confirmation; symlink destination rejected |
| External navigation | `https` + official host allowlist + confirmation dialog; window-open denied |
| Network scope | Fixed provider endpoints and model allowlists; CSP `connect-src 'self'` in renderer |
| Generated/imported content | Rendered as data/text; no shell execution bridge |

## Known gaps / not verified

- No independent security audit or penetration test.
- Unsigned installer; runtime/source files are not tamper-proof.
- Windows DPAPI behavior not validated in delivery environment.
- Same-user malware on Windows can still attack user-session data; DPAPI does not protect against every same-user process.
- Upstream Electron/Chromium vulnerabilities require timely updates.
- No automatic updater.

## Reporting

See [SECURITY.md](../SECURITY.md).
