# Reference — Logic And Probability

> Part of **mythos-bug-hunter v4.2.0** (package architecture).
> **Load when:** Phase 2-3: formal logic core (modus ponens/tollens, invalid forms, induction, abduction), Bayesian suspicion engine, hypothesis grammar deep, calculation and CVSS precision.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

## 9. Formal Logic Core

Every verdict is an inference. An inference built on an invalid logical form
is a false positive (or a missed bug) no matter how much data appears to
back it. This section fixes the valid forms; §10 quantifies them.

### 9.1 The Three Inference Modes

| Mode | Direction | Certainty | Primary hunting use |
|---|---|---|---|
| Deduction | rule + case → conclusion | certain (if premises true) | exploit chains, falsification |
| Induction | observed cases → rule | probable | priors, pattern spread, class kill decisions |
| Abduction | observation → best explanation | ranked | anomaly triage, hypothesis origin |

Use all three, in that order of authority: a deductive chain outranks an
inductive pattern, which outranks an abductive guess. A verdict may rest on
abduction alone only at `INCONCLUSIVE` (§6.3).

### 9.2 Deduction — the Exploit Chain (Modus Ponens)

An exploit claim must compile to a chain of rule premises plus observed
premises:

```
R1: IF input is reflected unencoded in an HTML body context,
    THEN markup injection is possible at that point.
R2: IF markup injection is possible AND no CSP restricts it,
    THEN injected scripts execute.
O1: parameter `q` reflects the canary unencoded in the body.  [observed]
O2: the response ships no CSP header.                         [observed]
C : script injection executes via `q`.              [derived, not asserted]
```

Rules (R*) come from technology behavior, not intuition; observations (O*)
come from captured evidence (§7); the conclusion (C) is derived, never
asserted. If any premise is unverified, the chain is still a hypothesis
(§11) — and the unverified premise is the next TODO.

### 9.3 Deduction — the Falsifier (Modus Tollens)

```
IF H were true, THEN signal S must appear when probe P is sent.
S did not appear across N valid trials.
∴ H is false, OR the delivery of P is broken.
```

Silence is ambiguous: it either refutes the hypothesis or indicts the
probe. Resolve the ambiguity with a **positive control** — a known-true
trigger proving the delivery channel works (a canary that reflects, a
known-valid object that loads). One positive control per technique per
session (ledger in §13.6). Silence after a passed positive control is real
silence: apply the silence likelihood ratio (§10.6) and move on.

### 9.4 Invalid Forms — the False-Positive Factory

| Fallacy | Hunting shape | Why it fails | Required fix |
|---|---|---|---|
| Affirming the consequent | "SQLi causes 500s; I got a 500; SQLi." | 500s have a dozen causes | discriminating evidence: engine-specific error text, or boolean/timing differential (§8) |
| Denying the antecedent | "The admin flag gates access; it is absent; no attack path." | other paths exist | enumerate alternate paths (§20 matrix) before closing |
| Base-rate neglect | exotic bug matches 2 symptoms; conclude exotic bug | the prior was ~1% | start at the prior, let evidence raise it (§10.5) |
| Conjunction fallacy | a detailed multi-step story "feels more likely" | every AND multiplies requirements | each conjunct needs its own evidence or the chain degrades to INCONCLUSIVE |
| Post hoc | payload sent, then an alert fired | correlation is not causation | re-run with control; differential pair (§8 axis D) |

**Correlation language is banned** in any candidate above `INCONCLUSIVE`
until the differential holds.

### 9.5 Necessity and Sufficiency — the A↔X Proof

Two questions cover every causal claim: **"if X, then A?"** (does my input
produce the impact — sufficiency) and **"if A, why must X?"** (is my input
actually required for it — necessity). "The impact happened after my input"
proves neither yet. Both directions are cheap:

```
SUFFICIENCY  (X → A): my input alone produces the impact.
             Differential pair: test request vs baseline → the difference
             is security-meaningful (§8.2).
NECESSITY    (¬X → ¬A): neutralize my input and the impact disappears.
             Contrapositive probe: control request (no payload,
             non-existent object, untouched state).
```

| Sufficiency | Necessity | Reading |
|---|---|---|
| yes | yes | causation — report-grade |
| yes | no | impact has other triggers; widen the differential |
| no | yes | prerequisite only; find the trigger |
| no | no | coincidence — FALSE POSITIVE path |

The differential trio (baseline / control / test, §26.1) is Mill's method
of difference rendered as HTTP: it exists to make these two directions
mechanical.

### 9.6 Induction Discipline

- **Spread rule:** a pattern observed on one surface raises the prior for
  the *same class* of surfaces (same framework, same auth boundary), not
  for the whole target.
- **Laplace's rule of succession** for the next-trial estimate:
  `(s+1)/(n+2)` after s successes in n trials. 4 IDORs in 12 tenant-scoped
  objects → 5/14 ≈ 36% for the 13th — sampling remains EV-positive (§10.7).
- **Negative results are data:** log clean trials in the candidate record;
  they compound via the silence LR (§10.6). Twelve clean trials on a class
  legitimately kill the class for this target.
- **Never induce across trust boundaries:** a pattern inside user A's
  tenant says nothing about cross-tenant behavior until tested there.

### 9.7 Abduction — Anomaly Triage

When an anomaly appears, generate **at least three** candidate explanations
before testing any:

```
score  = prior x coverage / complexity      (Occam as arithmetic)
test   = the cheapest discriminator between the top two candidates
```

Anomaly: `?sort=-1` returns 500 while `?sort=1` returns 200.

| Candidate explanation | Prior | Coverage | Complexity | Order |
|---|---|---|---|---|
| unvalidated sort expression reaches a DB/ORM layer | medium | full | low | test first |
| backend flake unrelated to input | medium | partial | low | one re-run discriminates |
| a proxy mangles the `-1` into something else | low | partial | medium | echo canary check |

Testing candidate 1 first is not "assuming" — it is ranking, and the rank
is recomputed after every observation. Abduction proposes; deduction and
the validation loop (§5) dispose.

### 9.8 Logic Discipline Rules

1. State premises explicitly in the candidate record; conclusion strength
   equals the weakest premise.
2. Every causal claim requires sufficiency evidence before leaving
   `INCONCLUSIVE`.
3. Silence counts as evidence only after a positive control passes.
4. "It fits the story" is not a logical relation — name the inference mode
   being used.
5. If two hypotheses explain the data, design the request that separates
   them (§8 axis design) before testing either further.

---

## 10. Bayesian Suspicion Engine

Suspicion is a number, not an adjective. "Highly suspicious" is banned from
state; `P(H)=0.62` is a state. The engine has one job: decide, with
arithmetic instead of mood, when a hypothesis deserves more requests and
when it deserves to die. Percentages, not assumptions — every number traces
to named evidence.

### 10.1 Where the Number Lives

Every active hypothesis carries `p_prior` at creation and `p_post` after
each evidence event, stored in the candidate record (§5.4 / §28.1) and
mirrored in the TODO queue (§15). Granularity is 5%: two decimals fake a
precision the evidence cannot support.

### 10.2 The Update Rule (Odds Form)

```
odds            = P / (1 - P)
posterior_odds  = prior_odds x LR(E1) x LR(E2) x ...
P               = odds / (1 + odds)
```

Each evidence event contributes one likelihood ratio: `LR = P(E|H) /
P(E|not-H)`. `LR > 1` supports, `LR < 1` weakens. Every applied LR is named
in the record with its rationale — a posterior that cannot show its
arithmetic is reset to its prior.

Worked example (XSS hypothesis on parameter `q`):

```
prior                                        10%   odds 0.111
E1 canary reflected unencoded (HTML)         +4    odds 0.444  → P 31%
E2 CSP present with default-src 'none'       x0.5  odds 0.222  → P 18%
E3 re-check on the actual route: CSP absent  +2    odds 0.444  → P 31%
E4 second context found (attribute, quotes
   escapable)                                +6    odds 2.667  → P 73%
```

A re-checked observation is a new evidence event with its own LR; the
history stays in the journal (§31.1), it is never silently rewritten.

### 10.3 Default Likelihood-Ratio Table

Heuristic defaults — personal calibration replaces them over time (§31.5).
Ad-hoc LRs are allowed with a written rationale; an unexplained LR is a
fabrication (§4).

| Evidence event | LR | Notes |
|---|---|---|
| engine-specific DB error string (`ORA-`, `SQLSTATE`, "syntax near") | +8 | strong but spoofable in logs; confirm in the response body |
| generic 500/timeout on payload | +1.5 | weak: many causes (§9.4) |
| canary reflected unencoded in an HTML context | +4 | precondition, not impact |
| canary reflected but fully encoded | x0.5 | actively weakens injection; raises context-analysis need |
| a known security-header blocker absent (e.g. no CSP on the route) | +2 | removes a blocker; weakly positive |
| timing delta >= 3 sigma over >= 10 trials (§12) | +6 | hard to produce accidentally |
| canary re-appears from a second origin (stored) | +10 | storage confirmed; impact is a separate question |
| expected signal absent, positive control passed | x0.3 per trial | silence compounds (§10.6) |
| WAF block page on a benign payload | +12 for "WAF present" (neutral for H) | evidence about the environment, not the bug |
| same bug class confirmed on a sibling host/route | +3 | correlated codebases |
| behavior identical to documented/expected behavior | x0.2 | the §6.3 FALSE POSITIVE row, quantified |

### 10.4 Decision Bands (the hard gates)

| P(H) | Action | Request budget |
|---|---|---|
| < 10% | park; passive observation only | 0 |
| 10-30% | one cheap discriminating probe | <= 3 |
| 30-60% | differential pair + context analysis (§8) | <= 15 |
| 60-85% | targeted PoC chain, bounded | <= 40 |
| > 85% AND impact demonstrated | freeze; pass the §19 gate and write | writing time |

Budgets are hard: exceeding a band's budget without a new evidence event is
a discipline breach, not enthusiasm. The bands answer the only question
that matters mid-loop — *spend or kill?* — with a number instead of a
feeling.

### 10.5 Prior Discipline

Default priors (calibration anchors — replace with own base rates as the
journal fills):

| Hypothesis class | Default prior | Anchor |
|---|---|---|
| access-control flaw on a multitenant surface | 20% | broken access control tops the OWASP Top 10 in both the 2021 and 2025 editions |
| reflected XSS on a user-content surface, encoding unknown | 10% | common class, usually mitigated |
| SSRF where server-side fetching of user URLs is evidenced | 25% | the mechanism is directly observable |
| auth bypass via framework-internal mechanics | 8% | rare, but cheap to test when the stack matches (§23.5) |
| RCE with no engine/stack-specific evidence | 2% | extraordinary claims need evidence; php2shell-class requires the Appendix C.1 conditions |

Rules: start lower than intuition (intuition inflates); every prior names
its provenance (framework anchor, program history, or personal base rate);
a prior with no provenance defaults to 5% flat.

### 10.6 Silence Compounding

Modus tollens (§9.3), quantified: each clean trial with a passed positive
control multiplies the odds by 0.3.

```
prior 20% → odds 0.25
3 clean trials: 0.25 x 0.3^3 = 0.00675 → P 0.67%
outcome: hypothesis parked/killed, class logged as sampled
```

Three honest negatives take a 1-in-5 hypothesis below 1%. Hunting fast
means collecting honest negatives quickly — not collecting positives.

### 10.7 Expected-Value Prioritization

Rank the TODO queue (§15) by arithmetic, not adrenaline:

```
EV        = P(valid) x value(severity class) - remaining_cost
EV/minute = EV / estimated remaining minutes
```

Worked pair:

```
T-A: P 45%, value 500,  remaining 30 min  → EV 225,  7.5/min
T-B: P 15%, value 3000, remaining 120 min → EV 450,  3.75/min
Order: A first. Small-but-likely beats big-but-fantasy per minute spent.
```

Kill rule: cumulative time spent on a hypothesis > 3x its remaining EV →
park it, regardless of attachment. Sunk cost is not evidence (§31.3).

### 10.8 Calibration Audit

Keep a prediction log: every hypothesis closure records its final `p_post`
and the outcome. Monthly, bucket by decile and compare hit-rate to stated
probability — the 70% bucket should hit about 70% of the time. If it does
not, adjust the LR table (§10.3) in writing. A miscalibrated engine that is
audited converges; one that is not merely drifts.

### 10.9 What Probability May Never Do

P routes effort (bands, EV, kill decisions). It never:

- upgrades a verdict — a 95% posterior with an incomplete evidence chain is
  still `LIKELY` (§6.3 decides verdicts, always);
- substitutes for the differential — no posterior replaces
  baseline/control/test captures (§8);
- justifies requests outside scope or beyond the band budget — §33 gates
  everything, arithmetic included.

---

## 11. Hypothesis Grammar

Every non-recon request is justified by a hypothesis stated in this
grammar. The grammar exists to force falsifiability: if you cannot say what
signal would refute the hypothesis, you do not have a hypothesis.

### 11.1 Template

```
If <condition about the system>,
then sending <request R>
should produce <observable signal S>,
which would SUPPORT | REFUTE <hypothesis H>,
because <mechanism M>.
```

All five slots are required. `R` must be a concrete request; `S` must be
observable in the response, timing, or out-of-band channel (canary hit,
email received, state change); `M` is the causal story linking them.

### 11.2 Falsifiability Rules

1. `S` must distinguish H from "the system behaves normally". If normal
   behavior also produces `S`, the test is void.
2. State the **refuting** signal explicitly before sending (what result
   would kill the hypothesis?).
3. One hypothesis per test request. Multi-cause tests are uninterpretable.
4. Prefer mechanisms grounded in observed evidence (an error string, a
   header, a version banner) over invented architecture.
5. Every hypothesis enters the TODO queue with an explicit prior and leaves
   with an explicit posterior (§10); "it feels likely" is not a prior.

### 11.3 Examples

GOOD:

```
If the router dispatches on X-Original-URL but the authz middleware
checks the original path, then sending GET /api/orders with
"X-Original-URL: /api/admin/orders" should return 200 admin data
(SUPPORTS: dispatch/authz path mismatch), because the two tiers would
be authorizing different paths. Refuting: 403/404 identical to baseline.
```

```
If the /api/v1/files/{id} download endpoint lacks object-level authz,
then user A's token requesting user B's file id should return 200 with
user B's file bytes, because the handler would stream any id it is given.
Refuting: 403 or 404 matching the non-existent-id control.
```

```
If the promotion endpoint checks the balance before the DB write but
does not lock it, then N concurrent redemptions of one code should
yield >1 successes, because each worker reads the same stale state
(§23.3). Refuting: exactly 1 success across 3 runs.
```

BAD (and why):

```
"Test for IDOR."            — no condition, no request, no signal
"Check if the API is vulnerable."  — unfalsifiable, no mechanism
"Try SQL injection here."   — payload spray without a distinguishing signal
```

---

## 12. Calculation and Validation Precision

Numbers are evidence. Invented numbers are fabrications (§4).

### 12.1 Rules

1. **Compute with a tool.** Any non-trivial arithmetic (rate limits, byte
   deltas, percentages, offsets, token windows) is computed with a script
   or calculator, and the computation is shown, not just the result.
2. **Cross-check** the result with a second method when feasible.
3. **Check units** — bytes vs bits, seconds vs milliseconds, per-second vs
   per-window.
4. **Check the denominator** — is the rate limit per-IP, per-user,
   per-token, per-endpoint, per-tenant? Prove it, do not assume it.
5. **Round only at the end** of multi-step calculations.
6. **If two methods disagree, investigate** — do not silently pick one.
7. **Unknown means unknown.** If a number is unavailable, state that it is
   unknown; never estimate silently.

### 12.2 Worked Example — Rate Limit Characterization

BAD: `"I sent 10 requests and got rate-limited, so the limit is 10 per
minute."`

GOOD:

```
10 requests in 5s  → 429 on the 11th.
 9 requests in 5s  → no 429; wait 60s; 1 more → 429.
 9 requests in 5s  → no 429; wait 30s; 1 more → 429.
10 requests, wait 61s, 1 more → 200.
Conclusion: limit = 10 requests / 60s sliding window (per token);
window confirmed by the 30s/60s/61s differential.
```

### 12.3 Worked Example — Response Length Delta

```
Baseline: 1247 bytes. Test: 1389 bytes. Delta: +142 bytes.
Diff of bodies: test adds JSON field "email":"victim@example.com"
(142 bytes incl. key/quotes/comma — verified by reconstructing).
Meaning: the mutated input controlled an additional sensitive field,
not merely the length.
```

### 12.4 CVSS Discipline

- If a score is reported, show the vector and the inputs used.
- Use the program's required version (3.1 vs 4.0). Engine CVEs in 2025+
  are commonly scored in CVSS v4.0 — e.g. PHP rated both php2shell CVEs
  9.2 in v4.0 (Appendix C.1). Never mix versions in one report.
- If you cannot compute a defensible score, omit it and describe severity
  qualitatively.
- Severity for *reportability* is judged by the program's table, not by
  the raw score alone (§19).

---
