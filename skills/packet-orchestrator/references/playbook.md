# playbook.md — translating and orchestrating, step by step

Load when converting manual logic into automation, or orchestrating
multi-stage workflows, under this organ.

## 1. The manual trace (L0)

1. Walk the logic by hand against the authorized target (or the lab).
2. One FACT record per request/response pair: what was sent, what
   came back, what you decided.
3. Mark the decision points explicitly — the places where your brain
   chose between branches. These are what the automation must
   reproduce.

## 2. The module card (L1)

Extract the smallest automatable unit from the trace (module-smith's
card shape). The observable cites the trace's records; the falsifier
cites the neighbor the trace showed to be unaffected.

## 3. The automated stage (L2)

1. Implement as one tool-shaped unit (arsenal tool call sequence or a
   template) — no side scripts.
2. Run it beside the manual path on the same inputs.
3. Diff decisions, not vibes: every decision point must match the
   trace. Mismatch ⇒ MISTAKE record ⇒ fix the automation.
4. Only when the diff is clean does the stage get trusted — and the
   diff records stay as its birth certificate.

## 4. The workflow (L3)

```
workflow: <name>
stages: [<stage cards in order>]
state-in:  <record classes read>
state-out: <record classes written>
parks:     <where each stage's leftovers go>
resume:    <condition to re-enter mid-workflow>
```

* State is records — if a stage needs to remember, it writes a
  record; if it reads memory nobody can re-read, it is defective.
* Rehearse the resume path once on the lab: a workflow that cannot
  resume is a workflow that will be restarted-and-forgotten.

## 5. Raw-protocol differentials (the exact-bytes case)

1. Craft the packet: layers and fields explicit (via an allowed CLI
   through `arsenal_route`, or a lab-side harness for self-owned
   targets).
2. Pre-register the expected response class (EXPERIMENT).
3. Send; capture BOTH directions to artifacts (the bytes are the
   evidence).
4. The differential is bytes-in vs bytes-out across the
   baseline/treatment pair — same shape as the HTTP triad, finer
   grain.
5. Characterize before perturbing (Searle's sequence): capture
   normal traffic first; entropy/structure analysis second; only
   then crafted probes.

## 6. Orchestration (L4)

* Cadence (weekly re-runs, Sonar-style) is an OPERATOR decision
  written in the plan; the automation only executes and record.
* Alerting is downstream of records — the workflow's output contract
  is records, full stop; humans and dashboards subscribe.
* Distributed execution changes nothing about discipline: same scope
  gate, same ledger, same templates. Scale is not a rule change.

## 7. Divergence protocol (when it goes wrong)

1. Manual trace re-run → establishes current ground truth.
2. Automation output compared; divergence recorded (MISTAKE).
3. Cause hunted at the failing rung of the ladder (L1 card? L2
   stage? L3 wiring?) — the ladder makes the search space small.
4. Fix lands in the automation; the trace is never edited to match.
5. The fix's verification is another beside-the-manual-path diff.

## 8. Exit criteria

Translation done when the stage runs beside its trace with a clean,
recorded decision diff. Orchestration done when the workflow's
state-in/state-out contract is real (auditable by re-running from
records alone), the resume path is rehearsed, and every packet-level
claim has its bytes in artifacts. Numbers at the exit gate: stages
translated, decision diffs clean, workflows with rehearsed resume,
packet artifacts captured.
