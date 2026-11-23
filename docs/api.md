# API / Interfaces

Relay Studio has no public HTTP API for third parties. It exposes two local interfaces:

## Browser prototype HTTP (`server.mjs`)

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/chat` | POST | Streams chat completion from selected provider/model. Requires same-origin JSON request. |
| `/`, `/app.js`, `/style.css`, etc. | GET | Serves static prototype files from `public/`. |

`POST /api/chat` body fields:
- `provider`: `groq` or `openrouter`
- `model`: allowlisted model id for provider
- `key`: optional; if omitted, server uses `GROQ_API_KEY`/`OPENROUTER_API_KEY`
- `messages`: array of `{role:"user"|"assistant", content:string}`, max 24

Limits: 100 KB body, 1200 output tokens, 90s upstream timeout, fixed provider endpoints.

## Desktop preload bridge (`window.relayDesktop`)

Exposed by `desktop/preload.cjs` only in the Electron desktop app:

| Method | Purpose |
|---|---|
| `info()` | Version/runtime/storage/workspace status. |
| `openFiles()` | Native open dialog; returns read text files. |
| `openWorkspace()` | Native folder picker; returns bounded file list with opaque IDs. |
| `readWorkspace(id)` | Reads a workspace file by opaque ID. |
| `saveCopy({name,text})` | Native save dialog; writes user-approved copy. |
| `setKey(provider,key,remember)` | Stores session key; optionally saves with safeStorage. |
| `forgetKey(provider)` | Clears session and saved key. |
| `startChat(payload)` | Starts main-process provider request. |
| `cancelChat(id)` | Cancels active chat. |
| `onChatEvent(cb)` | Receives chunk/end/error events. |
| `copy(text)` | Native clipboard write. |
| `importArchive()` / `exportArchive` flow | Conversation JSON import/export via native dialogs. |
| `diagnostics()` | Process/runtime diagnostics. |
| `onAction(cb)` | Menu actions (open files/workspace/export/import). |

All IPC handlers validate caller and inputs in `desktop/main.cjs` and `desktop/security.cjs`.
