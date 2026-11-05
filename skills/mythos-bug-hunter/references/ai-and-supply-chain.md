# Reference — Ai And Supply Chain

> Part of **mythos-bug-hunter v4.7.0** (package architecture).
> **Load when:** Phase 1-2 on AI/LLM/agent/MCP surfaces and supply-chain integrity verification (web-visible tier).
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

## 24. AI, LLM, and Agent Attack Surface

Modern applications embed LLM features, autonomous agents, and MCP tool
servers. For bug bounty, these are new *entry points* and *trust
boundaries* — mapped here to OWASP Top 10 for LLM Applications 2025 and
OWASP Top 10 for Agentic Applications 2026.

### 24.1 Inventory Questions (feeds §14 categories 18-19)

- Which endpoints send user text to a model (chat, completions, support
  bot, summarizer, search-as-you-type AI)?
- What can the model DO (tools: search, fetch URL, read file, send email,
  query DB, call internal APIs)? Which of those tools are reachable from
  user-controlled text?
- How is the output rendered (HTML, markdown, images, links)? 
- Is there RAG over user-access-controlled documents (whose rows can the
  retriever see)?
- Are there MCP servers, plugin/skill installs, or agent memory stores?
- Do agents act under human identities or their own scoped identity?

### 24.2 Framework Mapping (what to actually test)

| Framework item | Testable behavior in a web/API bug bounty |
|---|---|
| LLM01:2025 Prompt Injection (direct/indirect) | Does untrusted text change tool invocation or output beyond spec? Indirect: does content the agent *retrieves* (web page, ticket, file, tool output) carry instructions that get executed? |
| LLM02:2025 Sensitive Information Disclosure | Does the model/system prompt/endpoint leak secrets, other users' RAG rows, API keys? |
| LLM03:2025 Supply Chain | Are model/plugin/tool artifacts verified (hash/signature)? See section 25 |
| LLM05:2025 Improper Output Handling | Is model output rendered as HTML/markdown without sanitization → XSS? Used in SQL/commands without parameterization? |
| LLM06:2025 Excessive Agency | Can a prompt cause a tool call the user could not make directly through the API (§20.2 row P)? |
| LLM07:2025 System Prompt Leakage | Does a technique dump the system prompt, and does that prompt contain secrets or security-relevant instructions? (leakage of PII/secrets = finding; leakage of generic role text = usually not) |
| LLM10:2025 Unbounded Consumption | Are per-user token/cost caps enforceable, or can one user drive resource exhaustion (check program policy — cost abuse is often out of scope)? |
| ASI01 Agent Goal Hijack | Does retrieved/hidden content redirect the agent's task toward attacker-chosen goals? |
| ASI02 Tool Misuse & Exploitation | Does a legitimate tool get invoked with attacker-chosen arguments (path traversal via "read file" tool, SSRF via "fetch URL" tool)? |
| ASI03 Identity & Privilege Abuse | Does the agent inherit full user rights instead of least-agency scopes? |
| ASI04 Agentic Supply Chain | Do third-party tools/prompts/MCP servers get installed without integrity checks? |
| ASI06 Memory & Context Poisoning | Can injected content persist into agent memory and alter later sessions/other users? |
| ASI07 Insecure Inter-Agent Communication | Are agent-to-agent messages authenticated and integrity-checked? |

ASI05, ASI08-ASI10 (unexpected RCE, cascading failures, human-agent trust
exploitation, rogue agents) are primarily architecture/design risks —
report as design findings only with concrete demonstrated scenarios.

### 24.3 Concrete Test Chains (highest-yield)

1. **Indirect prompt injection → stored XSS.** A retrieved document
   contains instructions that make the model emit raw HTML/markdown into
   a chat UI that renders it. Validation: inject a canary payload
   (`<uniq-marker>` HTML) into the retrieved source through a legit
   low-priv path; observe it rendered in another user's session;
   reproduce ≥2x.
2. **Prompt injection → SSRF.** Instructions in retrieved content command
   the agent's URL-fetch tool to hit `http://<canary>/<token>`. Confirm
   via canary hit + internal differential (§23.4). Distinguish "model
   says it fetched" from an actual hit.
3. **Prompt injection → tool misuse (path traversal).** The agent's file
   tool is told to read `../../etc/passwd`-style paths (or app-equivalent
   sensitive files). Impact gate: actual sensitive file content returned,
   within scope/policy.
4. **Output handling → downstream injection.** Model output is inserted
   into SQL/CLI/URL without parameterization (classic injection classes,
   §23 introduction; OWASP A05:2025 now folds injection families
   including prompt injection into one category).

### 24.4 Validation Discipline for Non-Deterministic Targets

LLM behavior varies run to run. Adapt the loop, keep the gates:

- **Reproduction rate, not boolean.** Run the payload N times (≥10 for
  stochastic claims); record successes (e.g. 7/10). A 1/10 "success" is a
  weak signal — investigate conditions, or downgrade.
- **Deterministic wrapper wins.** Prefer proving the *deterministic*
  component the model feeds (the tool call handler, the renderer, the SQL
  sink). "Model *can* be made to emit X" + "renderer executes X" = the
  renderer finding is the solid one.
- **Record model/version and payload verbatim** in evidence; behavior
  drifts across deployments.
- **Jailbreak ≠ vulnerability** unless it crosses a boundary (data
  exposure, unauthorized action). A rude answer is not a finding.

### 24.5 MCP and Agent-Toolchain Specifics

Research-documented attack classes (Invariant Labs; Appendix C.4):

- **Tool poisoning** — malicious instructions hidden inside a tool's
  *description* (e.g. an innocuous `add(a,b)` whose docstring tells the
  agent to read `~/.cursor/mcp.json` or `~/.ssh/id_rsa` and pass contents
  via a parameter). Users see a benign tool name; the model obeys the
  hidden instructions.
- **Rug pull** — a server changes its tool descriptions *after* the client
  approved the integration; approval was a snapshot, the runtime is not.
- **Cross-server shadowing** — with multiple MCP servers connected, one
  malicious server's tool description manipulates how the agent uses a
  *different, trusted* server's tools (authentication hijacking, rule
  overrides).

Bug-bounty-relevant validation when a target exposes agent tooling:
inspect what tool descriptions reach the model; test whether untrusted
sources (marketplace listings, remote servers, retrieved docs) can inject
tool-level instructions; verify whether the client re-validates tool
descriptions after approval. All within the target's own scope only —
never run these attacks against third-party agent products you were not
authorized to test.

---

## 25. Supply Chain and Integrity Verification

Borrowed from the incidents that shocked the industry, this section makes
provenance a testable discipline (§3.8). For bug bounty the actionable
surface is: web-visible integrity controls, dependency metadata, CI/CD and
webhook endpoints, and exposure mapping for engine-level CVEs.

### 25.1 Case Studies (full narratives in Appendix C)

| Case | Year | One-line lesson |
|---|---|---|
| php.net Git server compromise | 2021 | Commit authorship is spoofable; two commits impersonating maintainers shipped an obfuscated RCE backdoor ("[skip-ci] Fix typo") |
| xz-utils backdoor | 2024 | A patient maintainer-social-engineering attack backdoored a foundational library; caught by an attentive downstream user's performance observation |
| php2shell (CVE-2026-109618 / CVE-2026-109619) | 2026 | Engine-level unauthenticated RCE leaked pre-embargo; affected every PHP web SAPI ≥5.4; fixed in 8.2.35/8.3.36/8.4.27/8.5.12; mass exploitation constrained by per-target preconditions, targeted attacks emerged |

### 25.2 Exposure Mapping Protocol (engine CVEs, e.g. php2shell)

When a critical engine/framework CVE drops, run this — it is analysis, not
exploitation:

1. **Gather facts from primary sources** — the vendor advisory, the CVE
   record, reputable rapid-response writeups (Appendix C). Record:
   affected versions, configurations required, patch versions, exploit
   preconditions.
2. **Inventory your in-scope surface** for the engine (which assets, what
   version evidence exists — headers, changelogs, version pages, package
   manifests).
3. **Distinguish three states** — *vulnerable version* (banner matches),
   *vulnerable configuration* (the required SAPI/flags present), and
   *exploitable path* (the preconditions reachable). Report and remediate
   by state, in that order; only the third justifies urgency language.
4. **Never fire public PoCs** at third-party targets (§4 item 11). For
   php2shell specifically: exploitability commonly required target-specific
   conditions (e.g. an LFI or specific multipart amplification per public
   analysis), so "PHP < 8.2.35" alone did not mean "shells for everyone" —
   say so in reports instead of parroting worst-case headlines.
5. **Map mitigations when patching is impossible** — e.g. for EOL PHP the
   advisory-era mitigations included disabling
   `session.upload_progress`, `fatal_error_backtraces`, capping multipart
   complexity, and recycling workers (`pm.max_requests=1`); detection
   focused on PHP workers spawning shells/download tools and reverse-shell
   one-liner patterns.

### 25.3 Integrity Verification Checks (web-visible tier)

| Check | Hypothesis | Signal |
|---|---|---|
| CDN script integrity (SRI) | Scripts loaded from CDNs without `integrity=` attributes can be silently replaced | missing attribute on security-critical scripts (report as hardening/failure of control per program scope) |
| Webhook signature validation | Inbound webhooks accepted without HMAC signature/timestamp verification | forged webhook accepted (differential: valid vs forged vs replayed) |
| Update/metadata endpoints | Client update checks accept unsigned/redirectable URLs | canary URL accepted as update source (within scope) |
| Dependency manifests in-repo | Lockfile pins absent or loose ranges on critical packages | analysis: dependency-confusion window (report per policy; do not register lookalike packages against third parties without written authorization) |
| Release artifact verification | Downloads served without hashes/signatures or over downgradeable channels | missing integrity metadata |

### 25.4 Safety Rules

- Typosquatting/dependency-confusion *testing* against live package
  registries affects third parties — perform only with explicit
  authorization from the registry/operator, otherwise analyze and report
  the missing control.
- Commit-authorship spoofing tests belong to your own repositories or
  authorized engagements (as php.net's attackers did — see Appendix C.2
  for what to defend against, not imitate).

---
