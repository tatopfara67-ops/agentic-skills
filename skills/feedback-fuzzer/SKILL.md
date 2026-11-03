---
name: feedback-fuzzer
version: 1.1.1
type: ai-skill
architecture: package
description: >-
  Craft-lineage organ distilled from Michal Zalewski (lcamtuf), creator of AFL
  — the feedback-guided search mindset. Blind mutation is noise; the map of
  observed states turns a search into a guided one. Every probe outcome
  updates a coarse state map (bucketed novelty detection, not fine-grained
  diffs); the corpus of inputs that reached new states is curated small
  (culling by cost); deterministic mutations come before random ones;
  exploration is preserved with probabilities instead of greedy pursuit; tar
  pits that buy 1% coverage at 100x cost are rejected. Since v1.1.0 the
  organ carries the executable method layer (A16) — a mechanical critique of
  the lcamtuf art's floors (a map instantiated only for binary coverage,
  culling thresholds as folklore, crash-vs-hang classified by eyes,
  determinism assumed and never measured, the state-map-to-hypothesis loop
  left unwritten) shipped as protocol M1–M5: the bucketed state-map schema for
  service targets, the corpus budget with eviction rules, the novelty gate
  with slice arithmetic, the classification table with a rerun floor, and the
  map-reading rule that converts stable novelty into falsifiable hypotheses.
  Use when hunting through input/state spaces with an oracle loop, when
  deciding to stop (saturation), when triaging a noisy signal, or when a probe
  campaign needs a stopping rule ("keep fuzzing or stop", "is this new
  behavior", "minimize the PoC", "saturation", "noise in responses").
category: security/craft-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Michal Zalewski (lcamtuf) — AFL american fuzzy lop (2013), its design papers, and Google security engineering; browser-security research lineage
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# feedback-fuzzer v1.1.1 — The lcamtuf Lineage

## 0. What This Skill Is — and Is Not

* **Is**: the organ for *search-with-feedback*: hypothesis loops that
  converge because every outcome updates a state map, not because the
  operator got tired. Its laws govern novelty detection, corpus
  discipline, tarpit rejection, and minimization-before-diagnosis.
* **Is not**: a fuzzer binary, and not a license for endless probing.
  The exact opposite: this organ is the arsenal's stopping theory.
  Every loop it governs ends at saturation or budget — never at
  vibes.

## 1. The Lineage (attribution)

Michal Zalewski ("lcamtuf") — Polish security researcher, long-time
Google security engineering lead — published AFL (american fuzzy
lop) in 2013 with design notes that read as engineering philosophy:
"Speed, reliability, and ease of use are the only true governing
principles… a collection of hacks that have been tested in
practice." Sources: references/sources.md — the verification record

## 2. The Seven Laws of Feedback Search

1. **Blind is waste.** Dumb fuzzing reaches a fraction of the states
   guided search reaches (the AFL design doc's own comparison). An
   oracle loop without a state map is a random walk with extra steps.
2. **Cheap instrumentation, coarse novelty.** AFL tracks edge tuples
   in a 64KB map and buckets hit counts (1, 2, 3, 4-7, 8-15…) —
   within-bucket changes are noise, bucket transitions are news.
   Modern form: classify responses coarsely (status class, size
   bucket, key-presence); flag transitions, not tremors.
3. **Deterministic before chaotic.** Bit flips and arithmetic tweaks
   run first; stacked mutations and splicing only after the
   deterministic phase plateaus. Escalate randomness only when
   methodical change stops paying.
4. **The corpus is memory, kept small.** Inputs that reached new
   states are kept and periodically culled to a "favored" subset that
   still covers every tuple — scored by latency and size. Modern
   form: keep the minimal probe set that reproduces every observed
   behavior class; retire redundant probes deliberately.
5. **Not greedy.** Non-favored inputs still run with 1-25% odds, so
   mutually-incompatible features stay in play. Modern form: leave
   cheap exploratory branches alive at low frequency even after the
   main line looks promising.
6. **Reject tar pits.** Timeout calibrated from initial speed; runs
   that improve coverage "by 1% while being 100x slower" are
   pragmatically rejected. Modern form: R7 effort discipline with a
   reason — a probe class that costs the budget for noise is parked,
   not pursued.
7. **Minimize before you diagnose.** AFL trims inputs and afl-tmin
   minimizes cases further (with alphabet normalization), because
   small inputs reproduce and communicate better. Modern form: before
   a signal becomes a hypothesis card, reduce it — fewest
   parameters, shortest payload, smallest response delta that still
   shows the effect.

## 2.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published feedback-search art where it was mechanically weak —
the map shipped only in binary-coverage form (service targets inherit
nothing), corpus culling tuned inside the tool as folklore, anomalies
triaged by expert eyes, replay stability asserted by demo, the
map-as-evidence half of the method left as personal skill — and ships the
executable replacement: **M1** the state-map schema (bucketed response
signature: status-class, log2 length bucket, first-line class, header-set
class, body-shape class — declared before the run), **M2** the corpus
budget (cap + eviction rule on record; occupancy reported per slice),
**M3** the novelty gate (two consecutive slices < 0.5% yield = exhausted;
re-seed or stop ON RECORD), **M4** the classification table + rerun floor
(NOVELTY-STABLE / JITTER / CRASH-CLASS / HANG-CLASS; n ≥ 3 rerun, ≥ 2/3 to
hold), **M5** the map-reading rule (one hypothesis per stable novelty,
mutation-diff as the candidate cause, falsifier stated before
diagnosis).

## 3. Procedure — Numbered Actions

1. Define the state signature for the loop: which coarse features
   classify a response (status class, size bucket, header set,
   body-class marker). Write it BEFORE probing (pre-registration).
2. Define saturation: K consecutive probes (or one stage of K) with
   no new state class ⇒ loop stops. K is part of the plan, not a
   mood.
3. Run the deterministic phase first: systematic single-knob changes
   (one parameter, one payload, one header) with the state map
   updated per probe.
4. On a new state class: add the producing input to the corpus
   (record: which knob, which class, which records).
5. Cull on schedule: after each stage, drop probes that add no class
   not already covered by a cheaper one; keep the "favored" set
   cited in the ledger.
6. Escalate to chaotic phases (combined knobs, payload chains) only
   after the deterministic phase saturates; label the phase in the
   records.
7. Minimize every candidate: strip knobs until the delta dies; the
   minimal reproducer is what enters the module-smith's card.
8. Stop at saturation or budget; the stop is a ledgered FACT with
   the last-new-state count.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| The loop's probes | `http_probe` (state signature in note) |
| Systematic sweeps | `content_discover`, `api_introspect` |
| Corpus records | `ledger_append` (EXPERIMENT/FACT per probe class) |
| Minimization | probe re-runs with knobs removed, each recorded |
| Stop condition | saturation FACT record + park note |
| CLI oracles | `arsenal_route` (bounded flags only) |

## 5. Hard Rules

1. No loop without a pre-declared state signature and K.
2. Noise within a bucket is not a finding — only class transitions
   count.
3. Deterministic before chaotic, always, and the phase label is in
   the records.
4. A candidate that was never minimized is not a candidate.
5. Saturation is the only natural death of a loop; "I think that's
   enough" is not.

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Designing the loop's state map and stopping rule | references/mindset.md |
| Running a feedback loop end to end | references/playbook.md |
| Checking lineage claims and reading list | references/sources.md |
| Grading the published method, declaring buckets, holding the novelty gate | references/method-upgrade.md |
