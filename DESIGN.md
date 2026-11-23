# Relay — Windows 11 coding assistant
## Research, product design, and prototype handoff
> **Studio 02 update:** This document preserves the initial research and native architecture plan. The client now includes three themes, optional procedural 3D, session search/switching, safe formatted replies, project-file previews, and local proposed-change diff review with approval-gated downloads. See **UPGRADE-NOTES.md** and **README.md** for current implementation scope; section 6 below describes the earlier baseline. Native installation, filesystem edits, execution tools, and remote development hosting remain unimplemented.

**Research date:** 23 November 2026 · **Budget:** free services only · **Status:** browser-based functional prototype; native Windows app proposed, not built.

## 1. Recommendation
Use a lightweight Windows desktop interface with **open-weight models hosted remotely**, not a model running on your PC. Start by testing **existing OpenCode Desktop with a supported remote provider** before investing in a replacement: OpenCode already offers a Windows desktop client and provider connectivity. Relay is useful if you want a more explicit lightweight/free-only workflow and a custom interface. [1](https://opencode.ai/docs)

**Recommended default:** Groq Free account → `openai/gpt-oss-20b`; manually evaluate `openai/gpt-oss-120b` for more demanding tasks. **Optional alternative:** OpenRouter's `openrouter/free` endpoint. Do not automatically route sensitive code to a different provider.

This does **not** create unlimited free remote hardware. It uses legitimate provider quotas. No stolen API keys, hidden peer compute, account cycling, or quota circumvention.

### What is and isn't possible
- **Possible:** no local model weights, no local inference runtime, no requirement for a powerful local GPU.
- **Possible:** responsive streaming from specialised remote inference hardware, subject to network and provider load.
- **Not possible:** a usable desktop app with literally zero CPU, RAM, disk, or network activity on your PC.
- **Not guaranteed:** faster responses than OpenCode. OpenCode is a client; model, provider, prompt size, reasoning, network, tool calls, and queueing determine much of its speed.
- **Important:** remote *inference* does not move builds, tests, terminals, containers, or project indexing off your PC. For those to be remote too, you need a separate remote development machine. A persistent, fast, private development machine is not a dependable always-free resource.

## 2. Provider findings
| Option | Verified offer | Suitability |
|---|---|---|
| Groq | The public limits table lists 30 requests/minute, 1,000 requests/day, 8,000 tokens/minute, and 200,000 tokens/day for GPT-OSS 20B and 120B. Organisation-specific limits are authoritative. | Best starting candidate for fast, free, small-context work. |
| OpenRouter free | 20 requests/minute and 50/day without a credit purchase; a qualifying US$10 credit purchase raises the daily cap. Failed attempts count. | Optional free alternative; small daily allowance for an agent loop. |
| Cerebras | US$5 trial credits after verifying a payment method, expiring in 30 days; API access inactive without the required payment-method step. | Excluded as an ongoing zero-budget default. |
| Self-hosted rented GPU | User controls model/runtime but must supply a host and capacity. | Does not fit a dependable zero-cost requirement. |

Provider sources: [2](https://console.groq.com/docs/rate-limits), [3](https://openrouter.ai/pricing), [4](https://inference-docs.cerebras.ai/support/rate-limits).

Groq lists about **1,000 tokens/sec for GPT-OSS 20B** and **500 tokens/sec for GPT-OSS 120B**. Those are provider-published model generation figures, not Relay benchmark results or guaranteed first-token latency. A small response can spend more time waiting, reasoning, or crossing the network than emitting text. [5](https://console.groq.com/docs/models)

**Token limits matter more than the headline request count.** A roughly 6,000-input-token request with 1,000 output tokens can consume most of an 8,000-token minute. A multi-step agent could hit the token ceiling well before 30 calls. This is an illustrative budget calculation, not a provider billing measurement. Avoid sending whole repositories.

### Privacy
Groq says inference inputs/outputs are not retained by default, but reliability and abuse investigations can involve retention up to 30 days; usage metadata is retained. Do not describe a free remote service as equivalent to private local inference. Review account controls and policy before sending sensitive code. [6](https://console.groq.com/docs/your-data)

OpenRouter is an intermediary with downstream providers. Its FAQ distinguishes its own logging from provider handling; review the selected route and privacy controls. The generic free router may select different models, so it is not a reproducible quality benchmark and does not enforce an open-weight-only catalogue in this prototype. Strict open-weight-only mode should use verified, pinned models. [7](https://openrouter.ai/docs/faq)

## 3. Proposed native Windows architecture
```text
Windows 11 PC
  Tauri 2 shell + system WebView2
  ├── UI: sessions, prompt composer, context preview, diff approvals
  ├── Rust: streaming HTTP, cancellation, provider adapters
  ├── Windows Credential Manager: API keys (native version only)
  └── scoped bridge: explicitly selected workspace/files
                 │ HTTPS: selected prompt and context
                 ▼
  Official inference provider → remotely hosted open-weight model

Optional, separate layer:
  authenticated remote development host
  └── repository, search, terminal, builds, tests, git operations
```
Tauri exposes a Rust/WebView trust boundary and capability-scoped IPC; application-core code still has broad system privileges and must validate input. Using Tauri is not sufficient by itself to secure an agent. [8](https://v2.tauri.app/security/)

**Three deployment choices**
1. **Least build effort:** existing OpenCode Desktop plus a remote provider; local file and command operations may still use local resources.
2. **Custom low-overhead client:** Relay native shell plus an existing agent service behind a versioned adapter. OpenCode's current API reference explicitly labels the HTTP surface experimental, so pin versions and test integrations rather than assuming older examples remain compatible. [9](https://opencode.ai/docs/api)
3. **Most compute offloaded:** lightweight Relay client plus agent and repository on an authenticated remote development host. Inference-provider accounts do not automatically give you this host. This may require existing equipment or a future paid budget.

**Implementation principles**
- No Electron or bundled model server in the proposed release. Use system WebView2 and a small native networking layer.
- No background embeddings or repository-wide watchers by default. Use bounded text search and user-selected files; move heavy search to a remote host if configured.
- Never expose an unauthenticated agent server or terminal to the internet.
- File access confined to canonical workspace paths; reject path traversal and symlink escapes. UI approval is not a substitute for OS access controls.
- Treat repository text and tool results as untrusted data. They cannot authorise actions or alter permission policy.
- Require explicit approval for writes, execution, deletes, package installs, and network tools. Show exact command, working directory, and file diff.
- Apply patches in a worktree, check for concurrent modification, and provide rollback. Prefer structured patch tools to model-generated shell commands.
- No automatic destructive retry. No hidden provider failover, paid fallback, or top-up.
- Use Windows Credential Manager and least-privilege IPC; never persist a raw key in localStorage.

## 4. Interaction design
**Workbench:** session navigation, prompt composer, attach selected source files, streamed reply, provider route, context list, and measured first-visible-text/elapsed time.

**Connections:** explicit provider and model, remote-transmission consent, free-tier caveats, session key clearing, demo/live controls.

**Blueprint:** architecture, verified provider links, implementation boundary, and export.

**Future agent review:** structured plan → tool request → approval → execution → result → proposed diff → apply/reject. Don't use a terminal animation as a substitute for real execution.

Visual language: dark graphite, muted sage accents, compact desktop controls, thin borders, restrained status indicators, keyboard-friendly entry. The preview is a Windows-oriented design, not a claim that it uses native Windows controls.

## 5. Speed plan and acceptance gates
**Design targets, not measured results:**
- First interface paint under 1 second on the agreed Windows test laptop.
- Idle application CPU target below 1% after settling; validate with Windows tools, not a fabricated UI counter.
- Working-set budget initially below 200 MB including associated WebView processes for a small session; validate on Windows. No memory guarantee is made.
- Responsive typing and cancellation while streaming; batch DOM updates if needed.
- Keep free-tier requests to a small context and an explicit output cap; stop growing history before provider limits.

**Measure separately:** network time, first stream event, first visible answer text, final answer, output-token count, tool duration, and total task completion. Reasoning tokens can precede visible text. Never infer exact token counts from character counts.

**Comparison protocol:** test Relay and OpenCode on the same provider/model and equivalent context from the same Melbourne network. Run repeated short fixes, multi-file explanations, and patch tasks; compare median/p95 first-visible-text and total useful-task time, including correctness. A faster bad answer is not an improvement. Free quotas may require spreading the evaluation across days.

**Rate limit behaviour:** surface 429 and Retry-After; do not spin. The current prototype shows the error and asks the user to retry. A production queue may add bounded jittered retries for safe requests, not repeated agent actions or provider switching.

## 6. Prototype implementation
**Included now**
- A runnable Node 20+ server, no runtime npm dependencies.
- Browser interface with clearly labelled, scripted offline inference demo.
- Opt-in real streamed chat through Groq or OpenRouter, using official HTTPS endpoints.
- Speed-first and larger-model Groq selection; manually selected OpenRouter free router.
- Cancel button; recent conversation context; text attachments; safe text rendering.
- Up to 4 selected files, 12 KB per file / 24 KB total; client bounds request context and server caps request body.
- Session-only in-memory key, no persisted chat; export current visible chat as Markdown.
- Real-request first-visible-text and elapsed telemetry, not CPU/RAM counters or benchmark claims.
- Fixed upstream endpoints and model allowlists; origin check; server error handling; 90-second upstream timeout; no request-body logging in application code.

**Not included**
- A compiled, signed Windows `.exe`/`.msi` or a Tauri project.
- An OpenCode integration, autonomous coding loop, local filesystem writes, shell execution, live repository access, semantic indexing, or remote workspace provisioning.
- Verified model-quality or latency benchmarks. No provider key was supplied, so no real inference was exercised during delivery.
- Authentication, multi-user isolation, deployment hardening, or a publicly hosted API service. Don't expose this development server publicly with a valuable environment key.

**Security boundary of this preview:** a typed key travels from your browser through the preview backend to your selected provider. It is not saved by Relay application code, but the hosting platform and provider remain part of the trust chain. Use a restricted disposable key here, or preferably run locally with an environment key. Frontend-only provider examples are not a secure substitute for a native credential boundary.

**Free-only is configuration, not account enforcement:** Relay never automatically changes providers/models or purchases credits. A Groq account already upgraded to a paid tier can still incur costs from a manually selected Groq model. Use an actual Free account and provider-side controls. The prototype does not authenticate your subscription tier.

## 7. Build sequence
1. **Validate before rebuilding:** try existing OpenCode plus Groq; use Relay to compare the desired UX. Verify provider account/model access and actual latency.
2. **Native thin client:** port networking to Rust/Tauri, use Credential Manager, add workspace selection and a signed installer; profile CPU/memory on Windows 11 x64 and ARM64 as applicable.
3. **Guarded coding workflow:** integrate a pinned agent core or implement a small structured-tool loop; add permission prompts, workspace confinement, tested patches, rollback, and integration tests.
4. **Optional remote development:** pair with an existing user-controlled host, SSH or short-lived token authentication, persistent sessions, and explicit repo transfer. Keep this separate from inference configuration and budget.
5. **Release gate:** security review, prompt-injection tests, key/logging audit, quota handling, interrupted-stream recovery, real task-quality evaluation, and published measurements.

## 8. Bottom line
The feasible zero-budget starting point is **a lightweight client + legitimate free remote inference**, with quota and privacy limits. You can avoid local model load, but not every byte of local resource usage. You cannot responsibly promise unlimited free remote compute or faster-than-OpenCode performance without matching benchmarks.
