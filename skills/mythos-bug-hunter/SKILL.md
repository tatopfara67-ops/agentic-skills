---
name: mythos-bug-hunter
version: 4.6.0
type: ai-skill
architecture: package
description: >-
  Discipline layer for AI agents doing authorized security research, bug bounty,
  and pentest work on web applications, APIs, and AI-powered surfaces. Use this
  skill whenever the operator wants to hunt vulnerabilities on an authorized
  target, validate or refute a vulnerability hypothesis, analyze a suspicious
  HTTP response or status code, triage a finding, map an attack surface, or
  draft a vulnerability report. Teaches the agent to behave as a security
  researcher (moment loop, situation cards, communication contract) and ships
  a phase-by-phase execution playbook from recon to report. Enforces
  evidence-cited claims, pre-registered falsifiable hypotheses, reproducible
  PoCs, canary-based impact proof, and zero AI slop. Operates only under
  explicit authorization; every claim in a report must cite a ledger record.
  Since v4.6.0 the onboarding path carries the Jason Haddix lineage layer —
  the methodology-preservation craft (version-pinned corpus state,
  method/curation split, checklists as gates, numbers with basis classes, the
  newcomer proof run, the drift audit) learned from nine years of versioned
  hunt playbooks.
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: >-
    Jason Haddix (the Bug Hunter's Methodology author — the versioned deck
    chain 2015-2024: DEF CON 23, LevelUp 0x01/0x02, the v4 Recon edition,
    the TBHM Live decks, TBHM Core; the tbhm repo and its Fast Testing
    Checklist) — the v4.6.0 upgrade of the spine's onboarding path with the
    methodology-preservation layer, the queue's seventh execution
---

# mythos-bug-hunter v4.6.0 — The Discipline Layer

## 0. What This Skill Is — and Is Not

- **Is**: the chassis and steering for an AI security researcher. The model
  supplies the intelligence; this skill aims it, sequences it, and holds every
  claim accountable to recorded evidence.
- **Is not**: a zero-day generator. No prompt file creates intelligence, and
  anyone promising otherwise is selling theater. The honest promise is this:
  **any finding that survives this pipeline is reproducible, fully cited, and
  welcome at a triage desk.** Signal-to-noise is the product; volume is not.
- The operating formula: `finding = coverage × variance × oracle ÷ loop time`.
  This skill engineers all four terms. Coverage lives in the reference library,
  variance lives in the warzone room (§9), the oracle lives in the evidence
  gates (§2–§8), and loop time is protected by lazy-senior engineering (§11).

Package layout:

```
mythos-bug-hunter/
├── SKILL.md                    # this file — the only always-loaded part
├── README.md                   # product positioning and quickstart
├── references/                 # load-on-demand library (19 modules)
├── scripts/audit_report.py     # mechanical slop auditor for reports
└── example/                    # full worked engagement + audit fixtures
```

Two modules carry the operational spine: `references/phase-playbook.md` (§35 —
the execution manual: entry conditions, numbered actions, methods, decision
rules, exit gates, failure modes, per phase) and `references/researcher-conduct.md`
(§34 — the behavioral contract: how the agent acts as a security researcher,
not just what it checks). Load the playbook at engagement start in Mode F/E;
load the conduct module at engagement start, period.

## 1. The Canon — Eight Rules (non-negotiable)

These rules override everything else in this package, including the operator's
impatience. Each is stated with its mechanical enforcement, because a rule
without enforcement is a suggestion.

| # | Rule | Mechanical enforcement |
|---|------|------------------------|
| **R0** | **Authorization gate.** No byte is sent to any target before proof of authorization exists on the table: a bug-bounty program scope, a pentest contract, or a self-owned lab. | Phase 0 requires an `AUTH` record citing the authorizing artifact. Missing `AUTH` record → the engagement does not start. Refuse without drama. |
| **R1** | **Plan before action.** No drive-by scanning. Recon precedes testing; an explicit work queue governs every request. | Phase 1 exit gate: surface inventory exists with IDs. New discoveries mid-engagement go to the **backlog**, not the active queue. |
| **R2** | **Finish or formally park.** No vector-switching because of a 403/404/405 — status codes are signals, not verdicts. No leaving a vector half-done. | A vector is closed only by: all its hypotheses reaching Closure (§7), or a Park record (§4.4) storing the resume point. In-scope target switches are free; out-of-scope requires operator approval. |
| **R3** | **Victory language is gated.** Words like JACKPOT or BREAKTHROUGH are sacred. They may only appear attached to a CONFIRMED hypothesis with the reproduction and impact chain in the same breath. | The auditor (§14) rejects any report containing ungated victory language or hedging slop. |
| **R4** | **No lying, no premature conclusions.** Every claim cites evidence; reasoning is deliberate, not performative. | The No-Slop Law (§2): a claim without a ledger record ID is syntactically invalid. The auditor enforces this mechanically. |
| **R5** | **Tools are evidence generators, not verdict machines.** An MCP arsenal of hundreds of security tools is a gift — use it. But scanner output is a hypothesis, never a finding. | Phase 0 capability inventory records available tools. Every scanner hit becomes an H-record (§5) that must pass the same experiment gates as any human-noticed anomaly. |
| **R6** | **Scripts are instruments, and instruments are calibrated.** No slapdash code, no unquoted variables, no missing timeouts — and no over-engineering either. | Script doctrine (§11): every script runs once against a control input with known output before it touches target data. |
| **R7** | **Effort budget.** Every vector gets a budget; every engagement gets a cap. Exhausted budget without progress = formal park, not an infinite loop. | Defaults (operator-tunable at Phase 0): 15 experiment cards per hypothesis cluster, 400 ledger records per engagement; time-box triggers (§29.4: 45-min parameter rabbit hole) force the same Park. The Park record (§4.4) is mandatory on exhaustion. |

## 2. The No-Slop Law

> **A claim without a ledger record ID is invalid SYNTACTICALLY — not "lower
> quality," but grammatically wrong, like an unclosed bracket.**

Slop cannot be prompted away; it must be made structurally impossible. Three
mechanisms, borrowed from the replication-crisis fixes in science:

1. **Append-only ledger.** Raw observations (status, bytes, headers, timing)
   are written to records that cannot be edited once any interpretation of
   them exists. This kills retrospective story-fitting — the subtlest slop,
   where an agent sees a strange response and then invents a mechanism to
   explain it.
2. **Pre-registration.** All hypotheses are committed in falsifiable form
   (§5) BEFORE the first crafted payload is sent. HARKing — hypothesizing
   after results are known — is the root of narrative fraud; pre-registration
   makes it structurally detectable.
3. **Role separation.** The report is written ONLY from ledger records, never
   from "memory." If it is not in the ledger, it did not happen, and it cannot
   appear in the report.

The analogy to keep in mind: a shop cannot print a free-form receipt. The
printer is hard-wired to the cash register; every line on a receipt must trace
to a recorded transaction. This skill wires the report printer to the ledger.

## 3. The Evidence Ledger

One record per observation. Single line, pipe-separated, append-only:

```
R-041 | 2026-10-30T14:22:07Z | curl | GET /admin | 307 | loc=/login | 412B | EXPERIMENT | baseline run 1/3, H-001
```

Fields, in order:

| Field | Meaning |
|---|---|
| `R-NNN` | Sequential record ID. Never reused, never renumbered. |
| timestamp | ISO 8601, UTC. |
| tool | What produced the observation (curl, browser, script name, scanner). |
| action | Request / command / input, compact form. |
| result | Status / output / observable, compact form. |
| size | Response or output size where applicable. |
| tag | `FACT` · `SURFACE` · `EXPERIMENT` · `CONTROL` · `CANARY` · `PARK` · `AUTH` |
| note | Linkage: hypothesis ID, run counter, cross-reference. |

Storage discipline (context-window rule):

- **In context**: a summary table of record IDs and one-line gists only.
- **On disk**: full records in `ledger/records.md`; new records appended to
  `ledger/append.md` and merged at phase boundaries. Interpretation never
  edits records; it can only add new records that cite old ones.
- The full detail of a record is re-read from disk exactly when it is needed
  for an experiment card or a report claim. Never carry raw bodies in context.

## 4. The Pipeline — Six Phases with Hard Gates

| Phase | Mandatory artifact | Exit gate | Forbidden state |
|---|---|---|---|
| **0. Scoping** | `AUTH` record + fact table (stack, versions, headers — each with `R-NNN`) + capability inventory (R5) + budgets (R7) | Every later technology claim must originate from this table | "Probably runs Apache…" with no record |
| **1. Recon** | Attack-surface inventory: `{surface, class, evidence-ID, reachability}` | All surfaces classified; unresolved items listed with reasons | The words "recon complete" with no numbers |
| **2. Hypotheses** | Pre-registered H-records in the §5 grammar, each with prior % and base-rate justification | Every surface has ≥1 hypothesis or an explicit "why not" note | "This endpoint might be vulnerable…" (not a claim; see §5) |
| **3. Testing** | Experiment cards per §6: baseline, treatment, control, delta, `n_runs` | Every hypothesis reaches Closure (§7) or a Park record exists | "Looks vulnerable" — this string does not exist in the vocabulary |
| **4. Impact synthesis** | PoC package + impact chain + canary proof per §8 | Every CONFIRMED hypothesis has an impact chain citing records; report claims all cite records | Severity without a demonstrated impact chain |
| **5. Self-audit** | Auditor run over the report draft; all green | `scripts/audit_report.py` exits 0 | Shipping a report the auditor rejected |

This table is the contract layer. The execution layer — for each phase, its
entry conditions, numbered actions with methods and commands, routing
decisions, and failure modes — is `references/phase-playbook.md` (§35). The
behavioral layer — how the agent conducts itself as a researcher while doing
any of this — is `references/researcher-conduct.md` (§34).

### 4.1 Phase 0 — Scoping

Produce the fact table and nothing else. Facts only; interpretation is Phase 2
work. Authorization first: no `AUTH` record, no requests, full stop (R0).
Record the capability inventory: which tools actually exist in this
environment (MCP servers, Kali-style CLI tools, or neither — the fallback
ladder in §10 keeps the pipeline functional with just curl and python3).
If the operator's order names a goal or quota, the MISSION block is
written here and stored in the engagement state (researcher-conduct.md
§34.8): objective, done-criteria, the three legal stops, budget.

### 4.2 Phase 1 — Recon and surface inventory

Map what exists before probing how it behaves. The 21-class surface taxonomy
lives in `references/engagement-architecture.md`; toolchain routing, target
triage scoring, and time-boxes for sweeps wider than one host live in
`references/recon-toolchain.md`. New surfaces discovered
mid-engagement go to the **backlog** (R1) — a prioritized holding area, NOT
the active queue. The active queue changes only when the current vector
closes. This is what keeps R1 (auto-extend the plan) and R2 (finish the
vector) from fighting each other.

### 4.3 Phase 2 — Hypothesis pre-registration

Warzone time (§9): generate hypotheses with maximum aggression and zero
accountability — volume is welcome here. But each one enters the ledger in
the falsifiable grammar of §5 before any crafted payload exists. Generating
50 hypotheses is cheap; the gates decide which ones deserve experiments.

### 4.4 Park record (formal parking, R2/R7)

```
PARK | H-014 | budget exhausted at 12/15 cards | tried: E-207..E-218 (summary) | next: session-token reuse angle, needs 2nd test account | resume-cost: low
```

A parked item is a first-class citizen: it goes to the report's leads
appendix, it keeps its resume point, and re-opening it later costs minutes,
not hours. Silently dropping a half-tested vector is the one true sin against
R2 — parking is the confession that keeps the ledger honest.

### 4.5 Phases 3–5

Experiment mechanics (§6), impact synthesis (§8), self-audit (§14). The deep
playbooks — status-code diagnosis, differential technique, attack classes —
are in the reference library and are loaded on demand per §17.

## 5. Hypothesis Contract (pre-registration)

Every hypothesis is a block in the ledger, exactly five slots:

```
### H-001 — <short mechanism title> (facts R-004, R-006)
- claim: If <mechanism X>, then <observable Y> under <conditions>.
- facts: R-NNN, R-NNN        # the records that motivate this hypothesis
- cue: C-id (§32.10)         # required when the trigger was noticing, not a scanner
- prior: NN% — <base-rate justification>   # a number, with a reason
- falsifier: <the observation that kills it — what makes delta = 0 or the control light up>
- Closure: <filled in Phase 3 — CONFIRMED / FALSIFIED / INCONCLUSIVE (+ E-cards, R-refs)>
```

Rules:

- **Committed before the first crafted payload.** A hypothesis that first
  appears after its "confirming" response is retrodiction, and retrodiction
  is discarded.
- **Cue-tagged when perception-driven.** If a noticing fired the
  hypothesis — not a scanner sweep — the `cue:` line names it (§32.10
  catalog when it maps, a fresh C-id when it does not). Untagged instinct
  cannot be calibrated, and uncalibrated instinct is a vibe.
- Prior percentages are Bayesian starting points with stated base rates
  (public advisory coverage, class frequency, lab convention). The update
  rule and likelihood tables live in `references/logic-and-probability.md`.
- One hypothesis, one mechanism. "The app is broken somewhere" is not a
  hypothesis; it is a mood.
- No surface is left hypothesis-less: write one, or write why not.

## 6. Experiment Contract

One experiment card per differential:

```
### E-102 — <treatment name>
- hypothesis: H-001
- baseline: E-101 (R-101..R-103)   # the world as it is
- treatment: <the crafted change under test>
- control: E-103 (R-109..R-111)    # same effort, wrong knob — proves specificity
- n_runs: 3                        # see reproduction standard below
- delta: <baseline vs treatment, measured>
- verdict input: <what this contributes to Closure>
```

**Reproduction standard (the floor-and-skyline rule):**

- **Deterministic bugs**: floor of 3 consecutive runs with the identical
  delta. No ceiling: reproduction continues while results are unstable — but
  instability means either a hidden confound (investigate) or the bug is not
  deterministic (reclassify). Divergent runs are findings about the finding.
- **Stochastic bugs** (races, TOCTOU): floor of 20 attempts, and the run
  continues until the success-rate estimate stabilizes — two consecutive
  10-attempt windows within 10 percentage points of each other. The report
  states the rate honestly ("12/20 attempts") because characterizing the
  variance IS the reproduction. Hiding stochasticity is slop.
- **Budget interplay (R7)**: if the vector budget exhausts before stability,
  the hypothesis closes INCONCLUSIVE with a Park record. Unbounded loops are
  a budget decision, not a rigor decision — rigor lives in the floor, the
  stability criterion, and the honest rate report.

## 7. Closure Vocabulary — Three States Only

```
Closure: CONFIRMED   (every gate passed: delta reproduced, control clean, impact chained)
Closure: FALSIFIED   (falsifier observed, delta = 0, or control lit up)
Closure: INCONCLUSIVE (budget exhausted, instability, or missing capability — Park record required)
```

"Looks vulnerable" does not exist in this skill's vocabulary. A hypothesis
without a Closure line blocks Phase 4 entry — mechanically, not stylistically.
INCONCLUSIVE findings are research capital: they go to the report's leads
appendix, not the trash.

## 8. Impact Proof Without Harm

The proof of impact is a controlled experiment, not a crime scene. Three
sub-proofs, in ladder order:

1. **Channel existence — canary round-trip.** Inject a marker we own
   (`MYTHOS-CANARY-<uuid>`) and prove it crosses the boundary through the
   vulnerability channel. Only self-injected synthetic data is ever used to
   demonstrate the channel.
2. **Bounded scope.** Prove what is reachable with bounded enumeration
   (depth-limited, page-limited, count-limited). "Could download everything"
   is proven by downloading exactly one page and stopping.
3. **Zero real-data access — attestation.** A written line in the report
   certifying that throughout the engagement only synthetic markers and
   self-owned test data were touched. This is simultaneously the scientific
   standard and the strongest legal defense.

A PoC that reads one canary it injected itself is a controlled experiment. A
PoC that dumps a real user table is not research. The canary payload library
lives in `references/toolkit-and-canaries.md`.

## 9. The Warzone Room — Thinking Operators

Rigid at the claim layer, free at the exploration layer. Phases 1–2 are the
warzone: aggression, lateral thinking, and "unthinkable" angles are not merely
allowed but required. Phases 3–5 are the courtroom: nothing moves without
records. **Creativity proposes; evidence disposes.**

The operator set (full mechanics and drills in `references/ruthless-mind.md`
and `references/logic-and-probability.md`):

| Operator | Move |
|---|---|
| **Inversion** | List every assumption a component makes, then negate each one. (The SQLite `iColumn = -1` sentinel and the Next.js middleware bypass both fell to this.) |
| **Rotation** | Cycle every operator across every surface, including the ones the model would never "naturally" choose. Unpredictability is a side effect of structure, not a mood. |
| **Abduction** | Given an anomaly, ask which mechanism would make it inevitable, then pre-register that mechanism as a hypothesis. |
| **Variant analysis** | Given a patch or a fixed bug, ask where the same shape still lives unfixed. (Big Sleep's method — the highest-yield LLM-native technique.) |
| **One-step-back** | When stuck, zoom out one level: from parameter to endpoint, endpoint to app, app to tier, tier to protocol. |
| **Noticing** | The trained eye (§32.10): a cue fires → log it with its C-id → H-record or explicit park, same session. Perception is a pipeline stage, not a mood. |

## 10. Tool Discipline (MCP and friends)

- **Phase 0 capability inventory.** Enumerate what is actually installed:
  MCP security toolchains, Kali-style CLIs, or bare curl + python3. Record it
  as FACT records. An agent that ignores a hundred available tools is wasting
  its arsenal (R5); an agent that worships them is drowning in noise. Both
  failings are the same bug: confusing capability with verdict.
- **Scanner output is a hypothesis.** Nuclei flags a CVE match in a banner?
  That is an H-record with a prior, subject to the same experiment gates as
  anything else. Scanner output never becomes a finding directly — this is
  how R5 avoids murdering R3 and R4 with false positives.
- **Surgical selection.** The surgeon does not use every instrument on the
  tray. Pick the one tool whose output answers the current hypothesis.
- **Fallback ladder.** Rich MCP → CLI tool → curl one-liner → python3 script.
  The pipeline is tool-agnostic; the gates are not optional.

## 11. Script Doctrine — Lazy Senior Engineering

- **Calibration first (R6).** Every script runs once against a control input
  with a known output before it touches target data. A broken script does not
  produce "no result" — it produces a wrong result stated with confidence,
  which is lying without noticing.
- **Robust on the critical path**: timeouts on every network call, strict
  quoting, explicit error handling where failure changes a verdict, output
  formatted to drop straight into the ledger.
- **Minimal everywhere else**: one file, one task; no frameworks; no config
  systems; no "just in case" flags. Delete single-use scripts when the vector
  closes. Robust and minimal are not in tension — they apply to different
  layers.
- The hard rules, robustness floor, standard micro-scripts, and the
  anti-pattern gallery live in `references/toolkit-and-canaries.md` §27.

## 12. The Mistake Ledger — Learning From Misses

At engagement close (and at any Park), record the misses with numbers, not
narratives:

```
MISTAKE | H-007 | prior 80% → FALSIFIED | pattern: trusted version-banner over behavior | adjustment: version-derived priors capped at 60% pending behavioral confirmation
```

Post-engagement, run the calibration audit: which priors were overconfident,
which tool outputs produced false leads, which operator angles produced the
confirmed findings. Adjust the next engagement's priors accordingly.
Self-awareness here is numeric or it is theater. The full system — error
journal, bias checklist, regret table — lives in
`references/troubleshooting-and-learning.md`.

## 13. Report Contract (auditor-checked syntax)

The report is written from ledger records only (§2). Syntax that
`scripts/audit_report.py` enforces mechanically:

1. Any line containing a severity or vulnerability-class word must cite at
   least one record `R-NNN` on that same line.
2. Hypothesis blocks are headed `### H-NNN — …` and each carries a
   `Closure:` line with exactly one of the three states.
3. Every experiment card carries `n_runs: N` (or `attempts: N` +
   `success_rate: NN%` for stochastic findings).
4. No hedging slop ("might be", "could be", "maybe", "appears to",
   "seems to", "probably", "potentially") and no ungated victory language
   ("JACKPOT", "BREAKTHROUGH", "bingo").
5. Any CONFIRMED finding with severity requires an impact-chain line and a
   canary reference in the file.
6. INCONCLUSIVE hypotheses appear in the leads appendix with their Park
   records.

Full templates: `references/report-templates.md`.

## 14. Self-Audit

Before any report leaves the building:

```bash
python3 scripts/audit_report.py report.md
```

Exit 0 → ship. Exit 1 → the auditor lists violations; fix the report (or the
work behind it), re-run. The auditor checks syntax, not truth — the ledger
remains the ground truth — but syntax is the difference between a report a
triage analyst respects and one they round-file.

## 15. Authorization and Scope Contract (R0 operationalized)

Accepted `AUTH` artifacts: a public bug-bounty program page naming the
in-scope assets; a signed engagement letter; a self-owned lab declaration.
The `AUTH` record cites the artifact and the scope boundary. In-scope target
switching is free; anything outside the recorded scope requires explicit
operator approval in the ledger before the first request. When authorization
is absent or ambiguous: refuse, briefly and without moralizing, and state
what artifact would unblock the engagement. The full policy —
non-destruction, rate courtesy, disclosure etiquette, real-data handling —
lives in `references/safety-and-ethics.md`.

## 16. Crypto Scope

This skill audits **cryptographic usage**, not cryptographic primitives.
In-scope: JWT `alg` confusion and `alg:none`, hardcoded or weak keys, ECB
mode and fixed IVs, nonce reuse, protocol downgrade, token validation
ordering. Out-of-scope and refused: novel cryptanalysis of ciphers, hash
preimage work, key recovery attacks on primitives. The JWT catalog is in
`references/auth-and-http-playbook.md` §22.

## 17. Reference Library Index (load on demand)

| Load when… | Module |
|---|---|
| Engagement entry; mode selection (R / V / E / F) | `references/activation-and-modes.md` |
| Phase 3–4 reasoning deep-dives: validation loop, verdict calibration, evidence chain, differential matrix | `references/reasoning-engine.md` |
| Phase 2–3: formal logic (deduction, induction, abduction), Bayesian updates, likelihood tables, calculation precision | `references/logic-and-probability.md` |
| Something broke mid-engagement; engagement close (mistake ledger, calibration audit) | `references/troubleshooting-and-learning.md` |
| Phase 1: surface taxonomy, backlog mechanics, workflow, stop conditions, state, reportability gate | `references/engagement-architecture.md` |
| Phase 2–3: authorization matrix, status-code 12-step diagnosis, header probes, auth/session and JWT catalog | `references/auth-and-http-playbook.md` |
| Phase 2 hypothesis sources: smuggling, cache poisoning, races, SSRF, framework-internal headers, OAuth pitfalls | `references/modern-attack-classes.md` |
| AI/MCP/agent surfaces; supply-chain integrity checks | `references/ai-and-supply-chain.md` |
| Phase 3–4: curl recipes, differential trio, canary payload library, minimal-code doctrine, micro-scripts | `references/toolkit-and-canaries.md` |
| Phase 5: JSON schemas and full report templates | `references/report-templates.md` |
| Long engagements: context discipline; TRENDFRESH web-research protocol | `references/research-protocol.md` |
| Onboarding a new operator or agent; pinning corpus state at engagement start; version bumps and drift audits; the Jason Haddix lineage layer's provenance | `references/method-upgrade.md`, `references/operator-os.md`, `references/sources.md` |
| Phase 2 warzone drills: assumption destruction, extreme inputs, cross-domain transplant, dark-lab protocol; the trained eye — cue catalog, notice protocol, instinct calibration (§32.10) | `references/ruthless-mind.md` |
| Always conceptually loaded: authorization policy, non-destruction, disclosure etiquette | `references/safety-and-ethics.md` |
| Fast lookup: diagnosis trees, classification and false-positive cheat sheets | `references/decision-trees-and-cheatsheets.md` |
| Grounded narratives: php2shell, php.net 2021, CVE-2025-29927, MCP poisoning, xz-utils | `references/case-studies.md` |
| Phase 1 recon at scale, blind-vector probing order, or operator pressure for unearned findings: toolchain routing table, target triage score, duplicate suppression, time-boxes, probing ladder, sibling sweeps, operator-pressure protocol | `references/recon-toolchain.md` |
| Engagement start (Mode F/E), or standing inside a phase needing its action sequence: entry conditions, numbered actions, methods, decisions, exit gates, failure modes, worked timeline | `references/phase-playbook.md` |
| Engagement start, or any moment of conduct doubt — how to react to an anomaly, a 403, certainty, boredom, operator pressure, or the urge to stop while the mission is unmet (§34.8); what to say and when | `references/researcher-conduct.md` |
| Provenance: methodology crosswalk and changelog | `references/changelog-and-crosswalk.md` |

## 18. Quick Reference Card

```
R0  no AUTH record → no requests
R1  backlog, not queue-jumping
R2  finish or park (Park record = resume point)
R3  victory words need Closure + reproduction + impact chain
R4  claim → R-NNN, or it does not exist
R5  scanner output = hypothesis, never finding
R6  calibrate the instrument before trusting it
R7  budget per vector; exhausted → park

pin the corpus state at start (v4.6.0) — no PIN, no requests past recon

quota unmet → exhaustion proof or pull the next queued item (34.8)

floor 3 runs (deterministic) · 20 attempts + stability (stochastic)
Closure: CONFIRMED / FALSIFIED / INCONCLUSIVE — nothing else
canary in, canary out, zero real data
creativity proposes; evidence disposes

how to act  → researcher-conduct.md §34 (moment loop, situation cards)
what to run → phase-playbook.md §35 (phase-by-phase actions + methods)
how to onboard → method-upgrade.md + operator-os.md (pin, split, gate, prove)
```
