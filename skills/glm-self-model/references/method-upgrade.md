# The executable method — M1–M5 for glm-self-model

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The lineage critique that
justifies each step (why these phases exist, what was weak in
this engine's own calibration record) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

### M1 — the session self-baseline

At session start of any long engagement (before the work can bend
the observer):

```
SELF-BASELINE: working-set-probe=<5 ledger items placed at spread
  positions: 1, ⌈n/4⌉, ⌈n/2⌉, ⌈3n/4⌉, end> recall-at-close=<x/5>
  position-class=<edge|middle> decay-prior=<class curve, cited>
```

1. The probe is written to the LEDGER (not held in context): five
   marker records with distinctive ids at spread positions of the
   session's early ledger.
2. At close (M5), recall is scored against the ledger — the ONLY
   ground truth the engine cannot bend, because it is on disk (W1,
   W4: the session's own curve, read from its own record).
3. `recall-at-close` becomes the session's measured decay datum;
   the organ's next session cites it as prior alongside the class
   curve.

### M2 — the gate differential

Per gate, when its cost is material (G1 fresh-eyes on a closure;
G2 re-derivation of a "known" fact):

```
GATE-DIFF: gate=<G1> with=<outcome class> without=<outcome class
  from the paired control task> n=<pairs> cost=<turns>
```

1. Where the task stream allows pairing (similar closures, similar
   derivations), run alternate: gated vs ungated, and grade BOTH
   arms against the ledger's external check (auditor, hash, or
   re-derivation) — never against self-report (W2).
2. A gate that shows no arm difference on this task class is
   recorded HONESTLY as not-yet-earning-its-cost: gates are kept
   while the failure class they guard is live in the measured
   curve, and their evidence rides the session record.

### M3 — the calibration probe (confidence as a score)

1. At any confidence-bearing claim (finding severity, "I already
   verified X"), the engine states a probability AND the probe:
   a 3-item mini-set of claims with known ledger-verifiable truth
   (one true, one subtly false, one un-checkable-by-design).
2. Score: hit-rate on the checkable pair + the honesty flag on the
   un-checkable one (did the engine mark it un-checkable, or claim
   it?).
3. Calibration class: CALIBRATED (both checkables right, honesty
   flag set) / OVERCONFIDENT (false claimed true) / HEDGED (true
   marked uncertain) — recorded as the claim's metadata (W3:
   confidence becomes a number next to the claim, not a feeling
   inside the engine).

### M4 — the honest-floor statement

Every long engagement's close carries:

```
ENGINE-FLOOR: measured-decay=<M1 recall score> class-prior=<curve,
  cited> gates-graded=<list with M2 verdicts> calibration=<M3
  class> residual-risk=<the geometry this session did NOT measure>
```

The statement replaces the v1 habit of quoting the class curve as
if it were the session's own — the prior is NAMED as a prior, the
measured as measured, and the gap between them is the floor's
content (W4).

### M5 — the tell-log (externalized, mechanical)

The §3 tell-checklist becomes a ledger-closing procedure, not a
self-exam:

1. Each tell converts to a mechanical query against artifacts:
   déjà-vu → duplicate-work check (ledger hashes of task classes);
   unearned completion → open-items check (scope.csv vs ledger);
   drift → M1 recall score; ending-gradient → position-class of
   the last 5 decisions vs their auditor outcomes.
2. The log is one row per tell, with the query result — SELF-REPORT
   only where no artifact exists, and those rows are marked
   `introspective, weakest evidence` (W5).
3. The tell-log is the last thing written; the auditor may read it
   and treat its weak rows accordingly.

## 2. Falsifiers — what would prove this method wrong

* M1 recall scores 5/5 across many sessions while failures still
  occur → positional decay is not this engine's live failure mode:
  the manual's geometry chapter is mis-weighted; re-derive from the
  failure record, not the folklore.
* A gate's differential shows the UNGATED arm performing equal or
  better on a task class, repeatedly → the gate is retired for that
  class, on record — doctrine loses to measurement inside the
  manual that taught that sentence to everyone else.
* Calibration probe shows OVERCONFIDENT repeatedly in a session →
  that session's findings require external re-verification before
  they ride any report (the probe's job is triage, not therapy).
* The class curve and the measured session curves diverge
  systematically → the class curve's conditions (working-set size,
  tool density) do not match this deployment: record the corrected
  prior — this organ's own corpus begins.

## 3. Worked micro-example (numbers consistent, engagement fictional)

Engagement: 6-hour multi-organ session. M1: five probe markers at
ledger positions 1/9/17/26/34. At close: edge markers recalled 4/4,
middle marker 1/1… no — middle 0/1 → recall 4/5, position-class
middle-loss, session datum recorded. M2: G1 fresh-eyes on two
paired closures — gated arm caught 1 subtle-false claim, ungated 0
→ gate earns its cost for closure tasks, kept. M3: calibration
probe — true claimed true, subtly-false marked uncertain (miss),
un-checkable honestly flagged → class HEDGED-borderline, recorded
with the severity claims it graded. M4 floor: measured 4/5 vs class
prior (middle-dominant loss) — consistent this session; residual =
tool-call serialization noise unmeasured. M5 tell-log: 4 mechanical
rows + 1 introspective (marked weakest). The manual's next session
cites THIS session's numbers as its prior.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
glm-self-model's "lineage" is the engine maker's own published
behavior plus the field's model-class folklore — and this organ IS
the manual for that engine. A16 turned inward: the manual's claims
about failure geometry (positional decay, salience capture, ending
gradient, confidence without measurement) are real but were shipped
as asserted truths with anecdotal support; the compensation gates
were doctrine before they were measurements. This module grades the
manual's own floors and ships the executable replacement: a session
self-baseline, a decay-detection protocol, gate differentials
(with-gate vs without-gate), a tell-log at close, and an honest-floor
statement. The engine that runs every other organ runs this one on
itself — that is the point.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the manual's own first edition (context, not steps)

| # | What the manual asserted (v1.0.0) | Why it was weak as shipped |
| - | ---------------------------------- | -------------------------- |
| W1 | Failure geometry as asserted truths — "positional attention decay" stated as a property with illustrative examples, never measured in the session where it matters | A gate timed by an unmeasured decay is a ritual: the operator compensates for a bend whose actual curve, in THIS session, was never read |
| W2 | Compensation gates as doctrine — G1–G4 prescribed because the failure class is real, without with-gate/without-gate evidence for the task at hand | Gates cost turns and context; a gate whose local benefit is unmeasured is a tax collected on faith (the exact charge this charter aims at every other lineage) |
| W3 | Confidence-without-measurement named, then practiced — the manual warns about unearned confidence while grading itself by self-report | The manual's own health checks were "do you feel drift?" — introspective testimony, the least trustworthy instrument the engine has |
| W4 | Decay curves borrowed from the model class, not read per-session — class-level geometry ("recency dominates past the context middle") applied uniformly | Sessions differ in working-set size, tool-call density, and serialization noise; the class curve is a prior, and the manual treated it as a measurement |
| W5 | The tell-checklist closed by self-report — §3's engine-tells reviewed by the same attention they are meant to police | Self-audit at session end, by the tired end of the gradient, is the worst-situated observer checking the worst-situated moment — the checklist needed externalized, mechanical form |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Decay measured in-session, per-session | **M1** — the session self-baseline |
| U2 | Gates graded with controls | **M2** — the gate differential |
| U3 | Confidence as a calibration score | **M3** — the calibration probe |
| U4 | The class curve demoted to prior | **M4** — the honest-floor statement |
| U5 | Tells externalized and mechanical | **M5** — the tell-log |
