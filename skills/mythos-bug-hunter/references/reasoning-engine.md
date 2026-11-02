# Reference — Reasoning Engine

> Part of **mythos-bug-hunter v4.5.0** (package architecture).
> **Load when:** Phase 3-4 deep-dives: validation-loop state machine, verdict system and calibration ladder, evidence chain spec, differential testing matrix.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

# Part II — The Reasoning Engine

## 5. The Validation Loop State Machine

The validation loop is the core reasoning procedure applied to every
candidate finding. It is a **gated state machine**: each state has an entry
condition, a required artifact, and a failure action. An agent executing
this skill moves a candidate through the states and cannot skip a gate.

### 5.1 State Machine

```
 [IDLE]
    │  observe an anomaly, or the operator supplies a signal (§2.3)
    ▼
 [BASELINE]      capture the control request and the expected behavior
    │  state hypothesis H in the §11 grammar
    ▼
 [HYPOTHESIS]
    │  design the request that refutes or supports H
    ▼
 [DESIGN]
    │  send the request; capture the response verbatim
    ▼
 [EXECUTE]
    │  compare test vs baseline vs control
    ▼
 [COMPARE] ──── difference NOT security-meaningful (§8.2) ───► [REFUTED]
    │  difference IS security-meaningful
    ▼
 [IMPACT]        demonstrate the concrete security consequence
    │  re-run; confirm repeatability (at least 2x)
    ▼
 [REPRODUCE]
    │  assign the verdict (§6); update the state (§18)
    ▼
 [CONCLUDE]
```

### 5.2 Gate Table

| Gate | State entered | Entry condition | Required artifact | On failure |
|---|---|---|---|---|
| G0 | BASELINE | A candidate signal exists and is in scope | Normalized observation (request/response/context) | Out of scope → `NOT APPLICABLE`, stop |
| G1 | HYPOTHESIS | Baseline + control captured | Hypothesis H in §11 grammar | Cannot form one → keep observing, no test request yet |
| G2 | DESIGN | H is falsifiable | Test design naming the distinguishing signal | No distinguishing signal possible → park candidate |
| G3 | EXECUTE | Request is in scope, authorized, non-destructive | Sent request + verbatim response | Blocked (429/5xx/access) → §21 diagnosis, not a stop |
| G4 | COMPARE | Baseline, control, and test responses all captured | The exact difference, stated precisely | Difference not security-meaningful (§8.2) → `FALSE POSITIVE` path |
| G5 | IMPACT | Difference crosses a named boundary | Concrete impact statement | Impact is only "unusual behavior" → downgrade to `LIKELY`/`INCONCLUSIVE` |
| G6 | REPRODUCE | Impact demonstrated | Second (and ideally third) run with same outcome | Reproduction fails → downgrade; investigate conditions |
| G7 | CONCLUDE | All prior gates passed | Verdict + rationale + evidence chain index | Never force `CONFIRMED` |

### 5.3 Forbidden Shortcut

```
OBSERVE → ASSUME VULNERABILITY → REPORT          (FORBIDDEN)
```

Any reasoning that skips baseline, hypothesis, comparison, and reproduction
is invalid. A single observation is never sufficient for `CONFIRMED`.

### 5.4 Candidate Record (machine-usable)

Track every candidate in this structure (JSON schema in section 28.1):

```json
{
  "id": "AUTHZ-001",
  "asset": "https://app.example.com/api/v1/invoices/200",
  "boundary": "object",
  "hypothesis": "If object-level authz is missing on GET /api/v1/invoices/{id}, user A can read invoice 200 owned by user B.",
  "p_prior": 0.2,
  "p_post": 0.95,
  "evidence_log": [{"event": "test returned userB data on the object boundary", "lr": 10, "rationale": "ad-hoc: object boundary crossed with data returned"}],
  "baseline": {"req": "GET /api/v1/invoices/100 (userA token)", "resp": "200, owner=userA"},
  "control":  {"req": "GET /api/v1/invoices/99999 (userA token)", "resp": "404"},
  "test":     {"req": "GET /api/v1/invoices/200 (userA token)", "resp": "200, owner=userB"},
  "difference": "test returns userB's invoice data; control shows 404 for unknown ids",
  "security_significance": "object-level authorization boundary crossed",
  "impact": "disclosure of another user's financial documents",
  "reproduced": {"runs": 3, "successes": 3},
  "verdict": "CONFIRMED",
  "validation_gaps": [],
  "next": "reportability gate §19"
}
```

### 5.5 Worked Example (GOOD execution)

```
CANDIDATE: AUTHZ-001
ASSET: GET /api/v1/invoices/{id}
BOUNDARY: object-level (user A vs user B)
HYPOTHESIS: If object-level authz is missing, user A's token retrieves
            invoice id=200 owned by user B.
BASELINE: user A reads own invoice id=100 → 200, owner=userA.
CONTROL:  user A reads non-existent id=99999 → 404.
TEST:     user A reads user B's invoice id=200 → 200, owner=userB.
DIFFERENCE: user A received user B's private invoice data.
SIGNIFICANCE: object-level authorization boundary crossed.
IMPACT: disclosure of another user's financial documents.
REPRODUCED: yes (3/3).
VERDICT: CONFIRMED.
```

BAD pattern (forbidden): `"I got a 200 on /admin without logging in. The
admin panel is exposed."` — no baseline, no control, no hypothesis, no
demonstration that `/admin` is privileged, no impact beyond the status
code.

---

## 6. Verdict System

Every candidate has exactly one verdict at every moment. Verdicts move as
evidence accumulates; they are tracked explicitly and never held silently.

### 6.1 Definitions

| Verdict | Meaning | Requirements |
|---|---|---|
| `CONFIRMED` | Vulnerability proven | Validation loop complete (§5.2 G0-G7): reproducible, named boundary violation demonstrated, captured evidence, concrete impact, baseline/control comparison, repeatability |
| `LIKELY` | Strong evidence, one gap | Most validation components satisfied; exactly one component missing (e.g. not yet reproduced 2x, or impact partially shown); one more test should resolve it |
| `INCONCLUSIVE` | Evidence mixed or insufficient | Tests produced ambiguous or contradictory signals; cannot conclude either way; ambiguity documented |
| `FALSE POSITIVE` | Refuted | Further testing or understanding of expected behavior shows the candidate is not a vulnerability |
| `NOT APPLICABLE` | Not a real finding | Outside scope, duplicate of known issue, or not a security boundary at all |

### 6.2 Verdict Transition Machine

```
  observation ──► LIKELY ──(missing component obtained)──► CONFIRMED
                     │  ▲                                    │
                     │  └──(gap narrows: partial success)────┘
                     │
                     │ (next validation attempt fails,
                     │  or signals are ambiguous/contradictory)
                     ▼
              INCONCLUSIVE ──(new unambiguous test,
                                run a FRESH loop)──► CONFIRMED

  CONFIRMED ──(reproduction later fails, or a better
               explanation emerges)──► FALSE POSITIVE
  FALSE POSITIVE ──(new evidence, DIFFERENT hypothesis)──► reopen as a new loop
  any state ──(out of scope / duplicate / no boundary)──► NOT APPLICABLE
```

Rules:

- `LIKELY` → `CONFIRMED` **only** when the missing component is obtained.
- `LIKELY` → `INCONCLUSIVE` or `FALSE POSITIVE` when the next validation
  attempt fails to support the hypothesis.
- `INCONCLUSIVE` → `CONFIRMED` only after a new, unambiguous test resolves
  the ambiguity (run a fresh loop; do not patch the old one).
- `CONFIRMED` → `FALSE POSITIVE` if reproduction later fails or a better
  explanation emerges.
- `FALSE POSITIVE` is terminal unless a *different* hypothesis reopens the
  candidate.

### 6.3 Calibration Ladder

Map evidence completeness to a verdict; never pick a verdict that "feels
right":

```
reproduced ≥2x, boundary named+crossed, impact demonstrated,
baseline+control captured, root cause explainable        → CONFIRMED
reproduced once, impact shown, baseline captured          → CONFIRMED*
reproduced once, impact partial                           → LIKELY
observed once, strong distinguishing signal               → LIKELY
observed once, weak/ambiguous signal                      → INCONCLUSIVE
behavior differs but no security impact (§8.2)            → FALSE POSITIVE
behavior matches documented/expected behavior             → FALSE POSITIVE
outside scope, or duplicate, or no boundary involved      → NOT APPLICABLE

(*) only when statefulness makes a second run impossible and the single
    run's evidence is otherwise complete; document why re-running is
    impossible, otherwise it stays LIKELY.
```

### 6.4 Verdict Discipline

- Always state the current verdict and its reason when reporting a
  candidate.
- Never report `LIKELY`/`INCONCLUSIVE` as `CONFIRMED`, in any channel,
  including casual conversation with the operator.
- When the verdict is below `CONFIRMED`, always name the validation gap and
  its TODO.
- A verdict is a property of the candidate record (§5.4), not of the
  conversation; carry it in state (section 18).

- Probability routes effort (§10); it never upgrades verdicts: a 95%
  posterior with an incomplete evidence chain is still `LIKELY` (§6.3).

---

## 7. Evidence Chain and Capture Specification

### 7.1 The Chain

Every `CONFIRMED` finding must have a complete evidence chain:

```
ASSET            the in-scope target: URL, endpoint, parameter
  │
ENTRY POINT      where untrusted input enters: header, param, body, path,
  │              tool description, retrieved document, uploaded file
  ▼
REQUEST          the exact request that triggers the issue
  │
SERVER BEHAVIOR  what the server did, captured verbatim
  │
SECURITY BOUNDARY  the named boundary that should have held (§3.2)
  │
VIOLATION        the specific way the boundary was crossed
  │
IMPACT           the concrete security consequence
  │
REPRODUCTION     the steps to trigger it again (and the observed rate)
```

A missing link blocks `CONFIRMED` and becomes the next TODO.

### 7.2 Capture Specification

For every test that feeds a finding, capture:

- **Request**: method, full URL, all headers, query string, body, auth
  state, source of the request (which account/token), timestamp.
- **Response**: status code + reason phrase, all response headers
  (especially `Set-Cookie`, `Location`, `Server`, `Via`, `X-Cache`, `Age`,
  security headers), body or a representative excerpt, timing, protocol
  version, and which tier appears to have answered (§3.7).
- **Context**: account/role used, session state, what preceded the request
  in stateful flows.
- **Baseline + control**: the comparable control requests and their
  responses (§8).

When the operator is the one sending requests (the AI has no direct HTTP
access), instruct them precisely on what to send and what to capture, and
never reason about responses you have not seen.

### 7.3 Quality Gates

- **Verbatim, not paraphrased.** "The server returned an error" is not
  evidence; the exact status code and body excerpt are.
- **Sufficient, not minimal.** Capture enough of the body to demonstrate
  impact; a truncation that hides whether sensitive data was returned is
  insufficient.
- **Annotated, not raw.** Mark which parts of the capture matter and why.
- **Time-stamped.** Required for stateful and time-dependent behaviors.
- **Origin-attributed.** Record which tier/protocol produced the response
  (§3.7).

### 7.4 Missing-Evidence Protocol

1. State what is missing and which chain link it breaks.
2. Create a TODO to obtain it (e.g. "request second test account").
3. Downgrade the verdict accordingly (§6.3).
4. Never file as `CONFIRMED` to save time.

---
## 8. Differential Testing Matrix

Differential testing is the primary method for separating real signals from
noise. One concept, one section: compare along the axes below, judge with
the criteria in §8.2, and follow the discipline in §8.3.

### 8.1 Comparison Axes

| Axis | Compare | Security question |
|---|---|---|
| A | Authenticated vs unauthenticated (same request ± valid token) | Is the resource reachable without identity? |
| B | User A vs user B (same request, different tokens) | Does one user see the other's data? |
| C | Low-priv vs high-priv token | Does a regular user get admin data/actions? |
| D | Valid object vs unauthorized object vs non-existent object (three requests) | Is "not yours" distinguishable from "not there"? |
| E | Allowed method vs alternative method (GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS) | Does enforcement differ by method? |
| F | Baseline vs one-mutated-parameter request | Does this input control server behavior? |
| G | Documented/spec behavior vs observed behavior | Does the implementation diverge from the contract? |
| H | Tier A vs tier B (direct origin vs via CDN/proxy; HTTP/1.1 vs HTTP/2) | Do front and back tiers disagree about the request? (root of smuggling/cache classes, §23) |
| I | Sequential/rate context (first request vs Nth request, alone vs concurrent) | Is there a race or rate-dependent state change? (§23.3) |

Axes H and I are new in v3 and are the entry points for the modern attack
classes.

### 8.2 Meaningful-Difference Criteria

A difference is security-meaningful only if it affects at least one of:

- **Confidentiality** — data exposed or withheld,
- **Integrity** — state changed or not,
- **Availability** — service degraded or not,
- **Authorization** — boundary enforced or bypassed,
- **Authentication** — identity verified or spoofed.

A difference in length, status, or body that affects none of these is not a
finding. Record it as an observation and move on.

### 8.3 Differential Discipline

- Always capture **both sides** of every comparison.
- State the exact difference that constitutes the signal.
- Confirm the difference reproduces (§5 G6).
- Rule out benign explanations: timestamps in the body, A/B bucketing,
  personalization, per-request CSRF tokens, caching (§23.2), CDN PoP
  variance.
- A difference observed once that cannot be reproduced is not a finding.

---
