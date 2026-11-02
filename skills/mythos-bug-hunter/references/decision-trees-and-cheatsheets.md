# Reference — Decision Trees And Cheatsheets

> Part of **mythos-bug-hunter v4.4.0** (package architecture).
> **Load when:** Fast lookup: non-2xx diagnosis tree, authorization differential tree, race/cache/prompt-injection trees, verdict flow, classification and false-positive cheat sheets.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

# Appendices

## A. Decision Trees

### A.1 Non-2xx Diagnosis Tree

```
RECEIVED NON-2XX RESPONSE
│
├── In scope?                            NO  → STOP; document; move on
│                                        YES ↓
├── Baseline request valid?              NO  → fix the request; re-test
│                                        YES ↓
├── Authenticated as intended?           NO  → fix auth; re-test
│                                        YES ↓
├── Actor authorized for the resource?   NO  → 403 is expected → test the
│                                            boundary (section 20), not
│                                            the code
│                                        YES ↓
├── Identify the responding tier; record origin evidence (§3.7)
│
├── Consistent across repeats?           NO  → intermittent: rate limit or
│                                            WAF heuristic; investigate
│                                        YES ↓
├── Differs by actor / resource / method / param?
│                                        YES → the difference IS the
│                                            signal → analyze per §8
│                                        NO  ↓
├── Alternate paths / methods exist?     YES → test them; record results
│                                        NO  ↓
├── Related endpoint provides evidence?  YES → test the sibling
│                                        NO  ↓
├── Access-control behavior itself testable (403-vs-404 leak)?
│                                        YES → design the differential (§8)
│                                        NO  ↓
└── Next test with a clear hypothesis?   YES → execute; loop back to §5
                                          NO  → stop branch per §17.1
```

### A.2 Authorization Differential Tree

```
HAVE (ACTOR, RESOURCE, ACTION) HYPOTHESIS
│
├── Baseline (own resource) obtainable?    NO → BLOCKED; request access
│├── Control (non-existent id) obtainable? NO → use clearly-invalid id;
││                                              note limitation
│├── Test (foreign resource) obtainable?   NO → BLOCKED; request 2nd account
│
└── Compare test vs control vs baseline:
    ├── test == baseline (200 + foreign data) → boundary violated →
    │        impact → reproduce → CONFIRMED candidate
    ├── test == control (404)    → enforced for this id → more ids,
    │        other methods, alternates
    ├── test == 403              → check fired → consistency, differential,
    │        alternates (§21)
    └── other (500/redirect/partial) → investigate; may be another class
```

### A.3 Race Condition Tree

```
ENDPOINT WITH CHECK-THEN-WRITE SEMANTICS
│
├── Identify the business limit (single use / max count / balance)
├── Baseline single request → exactly 1 effect?
│    NO → the bug is already sequential; report directly
│    YES → continue
├── N concurrent copies (single-packet / last-byte sync, §23.3)
│    ├── effects == 1 across ≥3 runs → controls hold → FP path
│    ├── effects > 1, reproduces ≥2/3 runs → CONFIRMED path
│    └── effects > 1 once → weak signal → investigate preconditions,
│         retry with tuned N/timing; downgrade if unstable
└── Always count state effects, not response bodies (§23.3 step 3)
```

### A.4 Cache Attack Tree

```
CACHE TIER PRESENT (X-Cache/Age headers observed)
│
├── Identify cache keys: vary elements; watch HIT/MISS transitions
├── Unkeyed input found that alters the stored response?
│    ├── YES → cache poisoning path (§23.2): prove with cache buster +
│    │        own two-session setup; impact = other user receives payload
│    └── NO → deception path: does /sensitive-page/<junk>.css style path
│         get cached while returning the dynamic page?
│         ├── YES → prove private content retrievable by attacker identity
│         └── NO → record; not a cache finding
```

### A.5 Prompt Injection Validation Tree (AI surfaces)

```
UNTRUSTED TEXT REACHES AN LLM/AGENT
│
├── Define the boundary the injection would cross (data → action,
│    user A context → user B data, output → sink)
├── Canary injection (harmless unique marker, §26.9)
│    ├── Marker echoed only → weak: observe where it propagates
│    └── Marker drives a tool call / sink → strong: continue
├── Does the effect cross the named boundary?
│    ├── NO → model followed instructions within its own remit →
│    │        usually NOT a vulnerability (§24.4); note and move on
│    └── YES → count effects, N-run reproduction rate (≥10 runs),
│              prefer proving the deterministic sink (renderer/tool/SQL)
└── Impact gate: data exposure / unauthorized action / cross-user effect
```

### A.6 Verdict Assignment Flow

```
VALIDATION LOOP EXIT
│
├── All gates G0-G7 passed?                YES → CONFIRMED
├── Exactly one gap, next test resolves?   YES → LIKELY (P0 TODO)
├── Signals ambiguous/contradictory?       YES → INCONCLUSIVE
├── Difference not security-meaningful?    YES → FALSE POSITIVE
├── Matches documented/expected behavior?  YES → FALSE POSITIVE
└── Out of scope / duplicate / no boundary → NOT APPLICABLE
```

---

## B. Cheat Sheets

### B.1 Finding Classification

```
OBSERVED BEHAVIOR                            → CANDIDATE CLASS
user A reads user B's data                   → broken object-level authz
user A invokes admin endpoint                → broken function-level authz
anonymous reads protected resource           → broken authentication
user A modifies user B's data                → broken write authz
tenant A accesses tenant B's data            → broken tenant isolation
endpoint returns data without token          → missing authn
endpoint accepts expired/invalid token       → token validation bug
error message leaks paths/stack/SQL          → info disclosure (A10:2025)
redirect to attacker-controlled host         → open redirect
parameter reflected without encoding         → reflected XSS (verify execution)
parameter alters server-side query           → injection (A05:2025 family)
external URL fetched server-side             → SSRF (+AI fetcher variant §23.4)
file path traversal in parameter             → path traversal (verify access)
upload accepts executable type               → unrestricted upload (verify)
concurrent requests exceed business limit    → race condition (§23.3)
unkeyed header changes cached response       → cache poisoning (§23.2)
static-suffixed path caches private page     → cache deception (§23.2)
GraphQL sibling field leaks foreign data     → field-level authz (§20.2 M)
middleware-bypass header reaches protected   → framework edge bypass (§23.5)
retrieved content steers agent tools         → indirect prompt injection (§24.3)
model output rendered as HTML unsanitized    → improper output handling (§24.2)
modified JWT accepted where control rejected → JWT validation flaw (§22.2)
GraphQL introspection enabled                → info disclosure (often OOS)
GraphQL query depth unlimited                 → DoS (often OOS)
WebSocket no origin check                    → CSWSH (verify cross-origin)
```

### B.2 Verdict Assignment

See the calibration ladder, section 6.3 — it is the single source.

### B.3 Differential Signals

```
SIGNAL                                        → MEANING
test 200, control 404                         → resource exists for actor
                                                 (authz may be broken)
test 403, control 404                         → exists; authz enforced
test 200 with B's data, baseline A's data     → object-level authz broken
test 500, baseline 200                        → input causes server error
                                                 (investigate; no conclusion)
test response contains extra sensitive field → input controls output
test timing persistently ≥2x longer          → possible blind/blind-OOB path
                                                 (verify with second method)
test 302 to attacker host                     → open redirect (verify)
test 200 with file contents                   → path traversal (verify)
two sessions receive different bodies on same → cache key variance (§23.2)
cache key
N concurrent, >N-permitted successes          → race condition (§23.3)
canary URL hit from target egress IP          → SSRF confirmed OOB
```

### B.4 Common False Positives

```
PATTERN                                       → WHY IT IS NOT A VULN
"404 on /admin"                               → may simply not be deployed
"200 on / with no auth"                       → public homepage, expected
"response lengths differ per user"            → personalization / A/B
"500 on malformed input"                      → expected error handling
"rate limit hit"                              → control working as designed
"GraphQL introspection enabled"               → often explicitly allowed
"X-Powered-By reveals framework"              → informational
"CSRF token present"                          → presence ≠ correct validation
"cookie without Secure flag"                  → check whether it carries session
"HSTS missing" / "clickjacking on login"      → often out of program scope
"password complexity weak"                    → policy issue, not technical
self-XSS                                      → not a vulnerability
XSS visible only to the admin themself        → low impact, usually NA
scanner says "CVE-X" + banner matches         → version ≠ configuration ≠
                                                 exploitable path (§25.2)
model obeys instructions in its own remit     → no boundary crossed (§24.4)
jailbreak producing rude text                 → not a vulnerability
```

### B.5 Modern Attack Quick Reference

| Class | Entry signal | First differential | Impact gate |
|---|---|---|---|
| Request smuggling | tier chain + framing conflicts | benign CL+TE probe, timing/status repeats | queue poisoning / bypass demonstrated |
| Cache poisoning | cache headers present | unkeyed-element HIT/MISS probing | another user receives payload |
| Cache deception | static-rule cache + dynamic pages | `/private/x.css` vs `/private` | private content retrievable |
| Race condition | check-then-write endpoints | 2-copy then N-copy concurrency | overdraw reproduced ≥2/3 runs |
| SSRF (AI edge) | any server-side fetch feature | canary + internal-vs-blocked differential | internal access or canary+internal |
| Framework header bypass | stack fingerprint (e.g. Next.js) | protected route ± bypass header | protected data/action reached |
| JWT jku/x5u/kid | JWT auth in use | modified token vs tampered control | forged token accepted doing a real action |
| PKCE downgrade/mix-up | OAuth flows | mutated flow vs normal flow | code/token interception or ATO |
| Indirect prompt injection | LLM + retrieved content + tools | canary instruction in retrieved doc | boundary crossed at N-run rate |
| MCP tool poisoning | agent + external tools/servers | inspect descriptions; untrusted-source injection | hidden instruction executed |
| Engine CVE exposure (php2shell-class) | engine version evidence | advisory facts vs observed versions | exposure mapped; never exploit |

---
