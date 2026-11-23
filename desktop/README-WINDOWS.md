# Relay Studio Desktop 0.4.0 — Windows 11 x64

## What this package is
A Windows desktop application with its own bundled Electron 45.4.1 runtime. No separate Node.js, browser tab, development server, CUDA, Ollama, or local model installation is required. The source is included for inspection and modification.

This is an **unsigned evaluation build**, not a code-signed production release. The installer was compiled on Linux; a matching Linux Electron build was exercised, but the Windows installer and Windows-specific protected storage have **not** been executed on a Windows machine in this environment. Review the validation report before installing. Windows or organisational policy may block unsigned software; do not bypass your organisation's security policy. Code signing and real Windows acceptance testing are release gates.

## Install
1. Verify the ZIP and installer SHA-256 values against the supplied manifest.
2. Extract the ZIP.
3. Close any existing Relay Studio instance.
4. Run `RelayStudio-0.4.0-Windows-x64-Setup.exe` if you trust this build.
5. Choose the installation directory. The default is `%LOCALAPPDATA%\Programs\RelayStudio`, for the current user. The installer does not request administrator access by default.
6. Launch Relay Studio from the Start menu.

Keep the entire installed application directory intact; the executable needs its bundled runtime files. This package is x64, not a native ARM64 or 32-bit build. Windows 11 x64 is the intended acceptance-test target.

Uninstall using Windows Installed Apps or the Start menu shortcut. The uninstaller asks separately whether to delete Relay Studio user settings and encrypted saved keys. It does not delete source files or exported conversations saved elsewhere.

## Round 1 — actual desktop shell
- Isolated application window with native menus and zoom controls.
- Local `relay://app/` protocol, not an HTTP listener; no local web server is started.
- Renderer Node integration disabled; context isolation and renderer sandbox enabled in the shipped configuration.
- Restricted preload bridge; no general filesystem, shell, IPC, or `eval` endpoint is exposed.
- Content Security Policy restricts scripts and connections to the local application origin.
- Main-process provider requests use fixed official endpoints and model allowlists.
- External links open only from an official-domain allowlist, after a confirmation dialog.
- Single-instance behaviour and cancellation on window/app close.

## Round 2 — useful native workflow
### Files and folders
- **Ctrl O:** select up to four small source files through a native dialog.
- **Ctrl Shift O:** choose a folder for read-only browsing.
- Folder listing is bounded to 200 supported small text files, maximum traversal depth 3, and a bounded scanned-entry budget. Common dependency/build directories, hidden entries, and symbolic links are skipped. This is not full repository indexing.
- File reads use opaque main-process file IDs and workspace checks. No folder path supplied by a model is accepted as an arbitrary read request.
- Previewing a file is local. **Add to conversation** explicitly selects it for context. Only a later live send uploads selected context.
- Existing limits remain: 12 KB per source file, 24 KB total, four attached files.
- Filename filtering is not a secret scanner. Inspect source text yourself before sending.

### Reviewed saves
Compare original/proposed code, inspect the diff, check approval, then choose **Save reviewed copy…**. A native Save dialog chooses the destination. Replacing an existing file requires additional confirmation. Cancellation does not save. No terminal, test runner, Git commit, autonomous patch, or automatic project write is implemented.

Code snippets and exported replies also use native Save dialogs. Clipboard actions use a limited native text-copy bridge.

### Conversation portability
File menu → Export/Import conversation, or the controls in **Behind the build**. JSON exports include visible messages and title, not credential fields or internal model history. Imported transcript text is rendered safely; it does not become model history automatically. A prompt that you yourself pasted a secret into would still contain that secret—review exports before sharing.

### Runtime diagnostics
Behind the build → Check runtime reads actual current application process counts and summed working sets. The sum can double-count shared pages; it is not unique/private RAM or a provider speed benchmark. No continuous performance polling is needed.

## Round 3 — desktop credentials and distribution
### Connect to a provider
1. Open Connections and choose an official provider/model.
2. Enter your own provider API key.
3. Approve remote transmission.
4. Optionally enable **Remember this provider key using Windows-protected storage**.
5. Enable live replies, then send a small test prompt.

The first message tests authentication; enabling live mode alone does not. Requests go **directly from the desktop main process to the provider**, not through Arena or the web-prototype proxy. The renderer transfers a newly entered key to the main process and clears its input. Saved keys are never returned to the renderer.

Keys are memory-only unless you opt in to remembering them. On Windows, Electron safeStorage's asynchronous API uses OS-protected encryption backed by DPAPI, scoped to your Windows user. It does **not** protect against every other application running as that same user. Encrypted blobs live under the application's user-data directory, typically `%APPDATA%\Relay Studio\keys`. If protected storage is unavailable, remember-key saving is refused rather than falling back to plaintext. The remember feature is intentionally disabled on non-Windows test platforms.

**Clear key** removes this provider's in-memory key and encrypted saved blob. Environment-variable keys, if an advanced user configured them externally, are not modified. Provider selection disables live mode and clears model histories, but does not silently delete another provider's saved credentials.

## What runs locally
The interface, optional procedural 3D, native dialogs, text comparison, and runtime use local CPU/RAM/GPU. The AI model's weights and inference remain remote. Compilation, tests, and terminal workloads have not been moved to a remote development machine because those tools are not implemented here.

The bundled runtime increases download size and usually RAM use relative to a system-WebView/Tauri design. The large installer is useful distribution content, **not a quality metric** and not a way to obtain free compute. No padding files, fake assets, duplicate runtimes, local model weights, or filler videos were added to meet the ZIP size request.

## Free is still limited
Use a legitimate free provider account. An already-paid account can incur charges; Relay cannot enforce your subscription tier. No automatic paid fallback, top-up, model/provider switching, quota circumvention, or account cycling. Actual account limits, network latency, model availability, privacy policy, and provider terms govern. No provider key was supplied for a real inference benchmark during delivery; the transport test used mocked SSE.

## Security and release boundaries
The isolated renderer and narrow bridge reduce risk, but do not constitute an independent security audit. Runtime/source files are not tamper-proof, and unsigned application code should be treated as an evaluation build. No automatic updater is included. Electron/Chromium must be updated and re-tested for future releases. Do not deploy a stale runtime indefinitely.

Generated model/repository text is treated as data, not executed. Native file paths come from user dialogs or main-process workspace IDs. Any file save requires an explicit dialog. No shell execution bridge, remote code loader, background upload, or telemetry collector is included in the application code. OS/runtime networking behaviour and provider policies remain separate considerations.

## Third-party components
The Windows runtime was downloaded from the official Electron GitHub release and matched against that release's published SHA-256 checksum. Electron's LICENSE and LICENSES.chromium.html are preserved in the installation along with the runtime components. NSIS builds the installer and uses its own open-source licence. Verification against a published checksum is provenance checking, not a source-level audit or an Authenticode signature for Relay Studio.

## Development
Source entry: `desktop/main.cjs`; preload: `desktop/preload.cjs`; pure guards: `desktop/security.cjs`; desktop UI adapter: `public/desktop-ui.js`.

The browser prototype can still run via `node server.mjs`, using its separate proxy/key-handling boundary. The desktop adapter only activates when the isolated native bridge exists.

See `TEST-REPORT-DESKTOP.md` for tested/untested details and `BUILD-REPORT.json` for actual package sizes and hashes.
