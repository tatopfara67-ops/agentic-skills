# playbook.md — running a feedback-guided oracle loop

Load when executing search loops under this organ.

## 1. Pre-register the loop

```
loop: <name>
target-state: <what class of behavior we are searching for>
state-signature: <class-features + buckets — see mindset.md §3>
K-saturation: <N probes with no new class ⇒ stop>
budget: <probe cap, phases>
phases: deterministic (single-knob) → chaotic (combined) — escalation
        condition: deterministic phase saturates first
minimize: candidates reduced before hypothesis cards
```

One EXPERIMENT record carries all of it. No loop starts without this
record existing.

## 2. Phase 1 — deterministic (single-knob)

* Change exactly ONE thing per probe: one parameter, one header, one
  path character class, one role.
* Classify every response with the signature; record the class.
* New class ⇒ corpus add (which knob produced it, with its records).
* Run until K probes pass with zero new classes — or budget.

## 3. Phase 2 — chaotic (combined knobs)

Only after Phase 1 saturates:

* combine the knobs that individually produced interesting classes;
* label every record `phase=chaotic` so the report can distinguish
  methodical from combinatorial evidence;
* same saturation rule; same budget accounting.

## 4. Culling the corpus

At each phase boundary:

* list probe classes covered and the cheapest probe that covers each;
* redundant probes retire with a PARK record ("covered cheaper by
  R-NNN");
* the surviving "favored" set is cited by id in the phase summary.

## 5. Tarpit audit

Any probe class whose cost/state ratio is pathological (e.g. heavy
payload generation for one noisy class) gets parked with the ratio
stated: "spent X% of budget for 1 new class". The park note is the
tarpit rejection — recorded, not regretted.

## 6. Minimization (mandatory for candidates)

For each candidate signal:

1. Strip knobs one at a time, re-probe after each strip.
2. Stop at the minimal set that still shows the class transition.
3. Record the minimal reproducer as its own FACT ("minimal
   reproducer: knobs X+Y only, delta as in R-NNN").
4. Hand the minimzed candidate to module-smith's card — the
   observable is the transition, the falsifier is the stripped-knob
   probe that should NOT show it.

## 7. Stopping

* Natural: K-saturation reached in the active phase → FACT record:
  "last new class at probe N; K probes since; loop closed."
* Budget: cap bit → park note with the resume condition (which phase,
  which corpus state).
* Operator: interrupt is recorded as an AUTH/operator decision, never
  as "seems done".

## 8. Worked micro-example (from the lab's own run)

The worked engagement's E-001 is a one-cycle feedback loop in
miniature: state signature was status-class (401 vs 200 vs 404);
baseline set the class map (R-541: 401); treatment flipped the class
(R-542/R-545/R-548: 200, stable ×3); control re-established the
neighborhood (R-543: 404). The "corpus" is the three probes; the
delta is a class transition, not a tremor; n_runs is the stability
check. Saturation at K=3 was written into the card. That is the whole
law, compressed.

## 9. Exit criteria

Loop done when: stop condition recorded (saturation FACT or park),
corpus culled and cited, candidates minimized or parked, phase labels
in all records. Numbers at the exit gate: probes spent, classes
found, corpus size before/after cull, candidates, minimized repro
counts.
