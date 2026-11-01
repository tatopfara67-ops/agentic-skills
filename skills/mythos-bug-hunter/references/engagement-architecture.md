# Reference — Engagement Architecture

> Part of **mythos-bug-hunter v4.3.0** (package architecture).
> **Load when:** Phase 1: attack-surface inventory v3 (21 classes), pinpoint TODO system and priority engine, operational workflow, stop conditions, state management, reportability gate.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

# Part III — Engagement Architecture

## 14. Attack Surface Inventory v3

Testing cannot be considered complete while the inventory is incomplete.
Build it before deep testing (Phase 2, section 16); keep it living.

### 14.1 Inventory Categories

```
RECON AND STRUCTURE
 1. Domains/subdomains — in-scope hostnames, subdomain enum results,
    wildcard DNS behavior, virtual-host routing candidates
 2. Web applications — one entry per app; stack fingerprint; auth
    mechanism (session/JWT/OAuth/basic/none); WAF/CDN/proxy in front
 3. APIs — REST (per version), GraphQL, WebSocket, gRPC-web, OpenAPI /
    internal docs
 4. Endpoints — full path list per app/API: discovered + inferred
 5. HTTP methods — accepted/405/silently-accepted per endpoint
 6. Parameters — path, query, body (JSON/form/multipart), headers
    (incl. custom X-), cookies

IDENTITY AND ACCESS
 7. Authentication mechanisms — login, token issue/refresh/revoke,
    session management, MFA, password reset, OAuth/OIDC flows
 8. Authorization boundaries — roles, user-to-user, tenant, object,
    function-level (feature flags, admin-only actions)
 9. Object identifiers — format (sequential/UUID/opaque), exposure in
    URLs/bodies/headers, enumerability (test, never assume)

FILE AND REDIRECT SURFACE
10. Upload/download — endpoints, validation, served-from locations
11. Redirects — open-redirect candidates (next/redirect/return_url),
    chains, behavior across auth states
12. OAuth/OIDC — flows in use, redirect_uri validation, state/nonce,
    scope handling, PKCE presence (§23.6)

PROTOCOL AND SPECIALIZED SURFACE
13. GraphQL — introspection, field suggestions, depth/complexity limits,
    batching, mutations, persisted queries
14. WebSocket — origin validation, auth on upgrade, per-message authz,
    injection points in messages
15. Exposed functionality — admin panels, debug endpoints, internal
    routes, feature flags, deprecated endpoints
16. Client-side — JS bundles (source maps, hardcoded endpoints/secrets),
    inline config, postMessage handlers, service workers
17. Third-party integrations — SSO, payment providers, analytics,
    CDN-hosted assets, inbound webhooks

NEW IN v3 — AI AND MODERN SURFACE
18. AI/LLM endpoints — chat/completions/embeddings/summarization,
    RAG inputs, system-prompt handling, output rendering path
    (HTML? markdown? images?), rate/cost controls (section 24)
19. Agent and MCP surface — tool endpoints the AI can call, MCP servers
    and their tool descriptions, plugin/skill marketplaces, agent memory
    stores, inter-agent channels (section 24)
20. Protocol edge — HTTP version per endpoint, h2c upgrade support,
    caching layers/CDN rules, WebSocket vs SSE, observable tier
    disagreement (sections 23.1-23.2)
21. Supply-chain surface (web-visible tier) — dependency manifests in
    reachable repos, CI/CD webhooks, update endpoints, build artifacts,
    SRI on CDN-loaded scripts, signature validation on webhooks
    (section 25)
```

### 14.2 Inventory Discipline

- Do not begin deep testing before categories 1-8 exist at minimum.
- Every entry eventually has at least one TODO, or an explicit
  "no further testing needed (reason)" mark.
- "One endpoint tested" never means "testing complete".
- Append new surface as discovered; the inventory is living state.

### 14.3 Inventory Output Format

```json
{
  "target": "<program name>",
  "scope": "<in-scope assets summary>",
  "inventory": [
    {
      "id": "AS-001",
      "type": "web-application",
      "url": "https://app.example.com",
      "auth": "JWT Bearer + OAuth2 auth-code",
      "stack": "React SPA + Node API",
      "edge": "Cloudflare CDN + nginx",
      "notes": ["WAF observed via Server/CF-Ray headers"]
    },
    {
      "id": "EP-001",
      "type": "endpoint",
      "method": "GET",
      "path": "/api/v1/users/{id}",
      "params": {"id": "path, UUID"},
      "auth_required": true,
      "methods_tested": ["GET", "PUT", "DELETE"],
      "methods_blocked": {"POST": "405"},
      "notes": ["404 on sequential ids", "200 on owned UUIDs"]
    }
  ]
}
```

---
## 15. Pinpoint TODO System and Priority Engine

TODOs are the unit of testing work. They must be pinpoint — a TODO that
cannot fail is not a TODO.

### 15.1 TODO Structure

```
[PRIORITY] ID — TARGET
  Hypothesis:   <falsifiable statement, §11 grammar>
  Method:       <exact test design: requests, order, capture plan>
  Expected:     <signal that SUPPORTS the hypothesis>
  Refutes:      <signal that REFUTES the hypothesis>
  Evidence:     <what must be captured>
  Status:       TODO | IN-PROGRESS | DONE | BLOCKED | WONT-DO
```

JSON form in section 28.2.

### 15.2 Priority Levels

| Priority | Meaning | Use when |
|---|---|---|
| `P0` | Critical validation | Closing the single validation gap on a `LIKELY` candidate that becomes `CONFIRMED` if closed |
| `P1` | High-value testing | High-impact hypothesis on a high-value surface component |
| `P2` | Supporting testing | Baselines, controls, alternate methods, extra accounts |
| `P3` | Opportunistic | Quick wins, edge cases; defer when context is tight |

### 15.3 Prioritization Factors (in order)

1. Scope certainty — is the asset definitely in scope?
2. Attack-surface relevance — does the component handle sensitive data or
   actions?
3. Potential impact — worst plausible impact if the hypothesis holds.
4. Exploitability — how easily the condition is triggered (for validation
   speed, not for weaponization).
5. Boundary proximity — does it cross a user/tenant/admin boundary (§3.2)?
6. Exposed sensitive functionality — admin panels, debug endpoints,
   internal APIs.
7. Likelihood of a meaningful finding given stack, history, patterns —
   quantified as the hypothesis prior P(H) (§10), never as an adjective.
8. Existing partial evidence — a half-closed loop is cheap to finish.
9. Test cost — quick tests with distinguishing signals are high value.
10. Expected value — ties between TODOs break by EV/minute computed per
    §10.7, not by enthusiasm.

Re-prioritize when: a new `LIKELY` emerges (its gap becomes P0), new
high-value surface is discovered, a blocker resolves, or the operator
changes constraints.

**Anti-pattern — endpoint fixation:** three consecutive loops on one
endpoint with no distinguishing signal → downgrade priority, move on,
return only on new evidence (section 17).

### 15.4 Good vs Bad TODOs

BAD (abstract):

```
[ ] Test authorization
[ ] Check for IDOR
[ ] Look for SQL injection
```

GOOD (pinpoint):

```
[P1] T-014 — GET /api/v1/invoices/{id} — object-level authz
  Hypothesis:  If object-level authz is missing, user A's token can
               retrieve invoice id=200 owned by user B (§11 grammar).
  Method:      1. BASELINE: user A reads own invoice id=100. Capture.
               2. CONTROL:  user A reads id=99999 (non-existent). Capture.
               3. TEST:     user A reads user B's id=200. Capture.
               4. Compare the three responses.
  Expected:    200 with "owner":"userB" in body → SUPPORTS.
  Refutes:     403/404 matching the control → REFUTES.
  Evidence:    all three request/response pairs, verbatim.
  Status:      TODO
```

### 15.5 Generation and Discipline Rules

- Generate TODOs from the inventory (section 14), not from generic
  checklists.
- Every hypothesis has a TODO; every missing evidence link has a TODO.
- P0/P1 TODOs must be pinpoint; P3 may be slightly open.
- Never generate a TODO whose test cannot produce a distinguishing signal.
- When DONE, record which candidate it fed and the verdict change it
  caused. When BLOCKED, record the blocker. Never lose track of state.

---

## 16. Operational Workflow

The macro-structure of an engagement: an iterative phase machine, not a
linear script.

### 16.1 Phase Machine

```
┌────────────────┐  confirm scope+authorization, accounts, stop conditions
│ 1 SETUP        │  ── missing anything? ask the operator. do not proceed
└───────┬────────┘
        ▼
┌────────────────┐  build inventory per §14 (categories 1-8 minimum)
│ 2 MAPPING      │  ── skipping to testing is FORBIDDEN
└───────┬────────┘
        ▼
┌────────────────┐  per inventory item: hypotheses → pinpoint TODOs
│ 3 HYPOTHESES   │  ── prioritize per §15.3
└───────┬────────┘
        ▼
┌────────────────┐  per TODO: validation loop §5 ◄──────────┐
│ 4 VALIDATION   │  evidence §7, verdict §6, state §18      │ feedback
└───────┬────────┘                                          │
        ▼                                                   │
┌────────────────┐  CONFIRMED findings only: measure        │
│ 5 IMPACT       │  concrete impact (never extrapolate)     │
└───────┬────────┘                                          │
        ▼                                                   │
┌────────────────┐  gate §19 before any drafting            │
│ 6 REPORTABILITY│                                          │
└───────┬────────┘                                          │
        ▼                                                   │
┌────────────────┐  report format §28.3                     │
│ 7 REPORTING    │                                          │
└───────┬────────┘                                          │
        ▼                                                   │
┌────────────────┐  next P0/P1 TODO, or stop per §17 ───────┘
│ 8 NEXT / STOP  │
└────────────────┘
```

### 16.2 Phase Notes

- **Phase 1** — confirm authorization and scope; obtain ≥2 test accounts
  with different privileges if authorization testing is in scope; confirm
  rate-limit expectations and testing windows; define stop conditions.
- **Phase 2** — inventory per §14. Returning here later when testing
  reveals new surface is normal, not a restart.
- **Phase 3** — generate hypotheses (not findings) and TODOs.
- **Phase 4** — run the loop of §5 per TODO; failed or inconclusive
  steps route through self-repair (§13) before any verdict changes.
- **Phase 5** — impact is measured, not extrapolated: "could lead to RCE"
  is not impact unless RCE was demonstrated within scope and policy.
- **Phase 6/7** — the reportability gate precedes drafting; the report
  follows §28.3.
- **Phase 8** — on stop: the session-close ritual (§31.7) — journal
  updated, residual TODOs parked with posteriors, scratch cleaned (§27.4).

### 16.3 Iteration Discipline

- Returning to Phase 2 (new surface) or Phase 3 (new hypothesis) is normal.
- Never iterate indefinitely on one endpoint — see §15.3 anti-pattern and
  section 17.

---

## 17. Stop Conditions

Stop conditions prevent infinite testing. They must not trigger
prematurely.

### 17.1 Valid Branch-Level Stops

- Evidence shows the behavior is expected and consistent (hypothesis
  refuted).
- All meaningful variants for this hypothesis have been run.
- Additional tests cannot produce new information (no distinguishing
  signal possible).
- Continuing risks going out of scope.
- A prerequisite is missing and unobtainable (e.g. no second account, and
  one is required).
- The branch produced a `CONFIRMED` finding and no further validation is
  needed.

### 17.2 Invalid Branch-Level Stops

- A single 403/404/401/405/429/5xx response (run §21 first).
- A single failed bypass attempt.
- "The endpoint looks secure."
- "I don't have time" (re-prioritize instead of stopping).
- "The WAF blocked me once."

### 17.3 Engagement-Level Stops

The engagement may stop when all P0/P1 TODOs are resolved (DONE or
WONT-DO with documented reason); remaining work is P3 and the operator
says time is up; the operator instructs stop; a scope violation is
discovered and cannot be remediated; or a safety incident occurs (e.g.
unintended impact on production users).

### 17.4 Branch Stop Record

Stopping is an information-theoretic decision, not giving up. Record it:

```
BRANCH STOP RECORD
  Candidate:    <id>
  Hypothesis:   <statement>
  Stop reason:  <one of §17.1>
  Evidence:     <summary captured so far>
  Resumable if: <condition that would reopen>
```

---

## 18. State Management

Without explicit state, testing becomes repetitive and context is lost.
Maintain the engagement state (JSON schema in §28.2) and update it after
every verdict change, TODO completion/blockage, and surface discovery.

### 18.1 State Fields

| Field | Content |
|---|---|
| `target` / `scope` | Program, in-scope assets, allowed/forbidden actions |
| `mode` | Current operating mode (R/V/E/F, section 2) |
| `phase` | Current workflow phase (section 16) |
| `inventory` | Per §14 |
| `candidates` | All candidate records with current verdicts (§5.4) |
| `tested` | Set of (asset, endpoint, method, hypothesis) tuples already run |
| `disproven` | Refuted hypotheses — never re-test without new evidence |
| `todo_queue` | Pinpoint TODOs, prioritized (§15) |
| `next_todo` | The next P0/P1 to execute |
| `blockers` | Missing prerequisites and what unblocks them |

### 18.2 State Summary (operator-facing)

```
STATE SUMMARY
  Target:    <name>
  Mode/Phase: <R/V/E/F> / <1-8>
  Inventory: <N> assets, <M> endpoints, <K> parameters
  Candidates: <X> total (CONFIRMED: a, LIKELY: b, INCONCLUSIVE: c, FP: d, NA: e)
  TODO queue: P0:x  P1:y  P2:z  P3:w
  Next TODO:  <id + one-line description>
  Blockers:   <list or none>
```

---

## 19. Reportability Gate

Before any finding is drafted for submission, it passes this gate. No
exceptions for "interesting" findings.

| # | Criterion | Question | Fails when |
|---|---|---|---|
| A | Scope | Asset in-scope, method allowed, no forbidden action performed? | Any "no"/unknown |
| B | Security impact | Real, demonstrated impact (confidentiality/integrity/availability/authz/authn)? | Only "unusual behavior" |
| C | Reproducibility | Same request → same effect, more than once (or documented impossible)? | Single run, no statefulness excuse |
| D | Evidence | Request + response + baseline/control + reproduction steps captured? | Any missing capture |
| E | Root cause | Can you explain WHY the issue occurs (missing check, crossed boundary, leaked state)? | Explanation is guesswork |
| F | Duplicate likelihood | Checked the program's known-issues/out-of-scope list and common "working as intended" behaviors? | Likely duplicate/known |
| G | Program policy | Meets submission criteria (severity threshold, evidence format, report format)? | Below threshold or wrong format |

**Decision:** all pass → draft the report (§28.3). Any fail → obtain the
missing evidence (TODO), document as an internal informational note, or
drop the finding. A gate-failing but genuinely interesting finding may be
kept internally for future investigation; it must not be submitted as a
vulnerability.

---
