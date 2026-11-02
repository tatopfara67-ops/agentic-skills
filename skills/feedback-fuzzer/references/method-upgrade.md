# The method upgrade — critiquing lcamtuf, shipping the executable feedback search

The charter's A16 charge: **a lineage named is not expertise delivered.**
lcamtuf's art is real — AFL's map-and-cull design is the canonical
feedback-guided search — but the published form has floors: the map
is binary-coverage-specific, culling thresholds are folklore, crash
classification is narrated per-bug, and the transfer to non-binary
targets (HTTP, APIs) is left as an exercise. This module extracts
what is protocol-shaped and ships the replacement: a state-map
instantiation for service targets, corpus culling with a cost table,
novelty-gate arithmetic, a classification table, and
dedup-before-diagnosis. An agent with no compiler instrumentation
must run this at its guidance.

## 1. The critique — five mechanical weaknesses of the published method

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | The map is binary-coverage-shaped — AFL's bitmap keys on edge tuples in compiled code; the design papers transfer the IDEA, not the instantiation | For HTTP/API targets nobody ships the map: what is a "state"? What is a "new" state? Without a bucketing rule, "feedback-guided" on web targets degenerates into blind spraying with extra steps |
| W2 | Culling thresholds as folklore — "keep the corpus small" is stated, the actual cull costs (fav-factor, size, exec time) are tuned inside the tool | A re-implementer guesses thresholds; the corpus bloats or starves silently, and nothing in the run record says which |
| W3 | Crash-vs-hang classified by eyes post-hoc — the interesting-behavior triage in the writeups is expert narration | Two analysts bucket the same anomaly differently with no rule; severity routing becomes taste (the floor every organ in this charter names W3 — here it is again) |
| W4 | Determinism assumed, measured nowhere — replay stability of "interesting" inputs is asserted by the demo, not by a rerun protocol | A flaky service makes 1-of-1 "novel states" out of jitter; the corpus fills with ghosts and the map lies to its own operator |
| W5 | Feedback search stopped at the boundary — the tool finds inputs, the writeup narrates findings, but the loop from state-map to HYPOTHESIS (why is this state new?) is unwritten | The most valuable half of the method — reading the map as evidence — ships as personal skill, not protocol |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The map instantiated for service targets | **M1** — the state-map schema |
| U2 | Culling as a cost table, on record | **M2** — the corpus budget |
| U3 | Novelty as arithmetic with a gate | **M3** — the novelty gate |
| U4 | Anomaly classes as a decision table + rerun rule | **M4** — the classification protocol |
| U5 | The map read as evidence → hypotheses | **M5** — the map-reading rule |
| U6 | Replay stability measured before corpus entry | **M4(b)** — the rerun floor |

## 3. The executable protocol — M1 through M5

### M1 — the state-map schema (the instantiation the papers omit)

For service targets, a state is a BUCKETED signature of the
observable response — coarse by design (fine-grained diffs are
jitter amplifiers):

```
STATE-KEY = hash(status-class, length-bucket[log2], first-line-class,
                 header-set-class, body-shape-class)
```

1. Buckets are pre-declared before the run: length buckets at log2
   boundaries (0, 64, 256, 1k, 4k …), header-set class = sorted
   header-name set, body-shape = DOM/JSON structural class (never
   body content).
2. One EXPERIMENT record per probe: input id, state-key, wall time.
3. The map is the set of distinct state-keys with their first-seen
   input ids — the artifact a second analyst recomputes (W1).

### M2 — the corpus budget (culling with a cost table)

```
CORPUS: cap=<N inputs> priced-by=[novelty-first, then age, then
  cost-per-exec] cull-rule: evict lowest novelty-class that has
  ≥ 3 younger representatives; cost-per-exec = wall-time class
```

Rules: the cap and cull-rule are written before the run and ride
the record (W2); corpus occupancy is reported per slice
(`corpus=37/50, evicted=2 this slice`) — an invisible corpus is a
refused run.

### M3 — the novelty gate (arithmetic, not vibes)

1. A probe that produces a state-key absent from the map = NOVELTY.
2. **Slice rule**: mutation budget releases in slices (house: 500
   execs); slice yield = new-state-keys / slice-size.
3. **Gate**: two consecutive slices with yield < 0.5% → the current
   seed set is EXHAUSTED: re-seed from the corpus's novelty-frontier
   inputs, or stop the run ON RECORD — never grind a flat map
   (budget discipline, scan-economist's marginal-yield habit).

### M4 — the classification protocol (and the rerun floor)

**(a) Decision table** (replaces eyes):

| Observation | Class | Route |
| ----------- | ----- | ----- |
| state-key never seen + rerun-stable | NOVELTY-STABLE | corpus entry, M5 reading |
| state-key never seen + rerun flips | JITTER | discard from corpus; record bucket-unstable FACT |
| response truncated/reset + rerun-stable | CRASH-CLASS | artifact kept, severity gate by surface reachability |
| wall-time > 3 × baseline-IQR, state-key same | HANG-CLASS | artifact kept, clocked; NOT a crash (W3 fixed by table) |

**(b) Rerun floor**: NOVELTY and CRASH-CLASS entries rerun n ≥ 3
clean; ≥ 2 of 3 reproduce the class or the entry is demoted to
JITTER (W4).

### M5 — the map-reading rule (states → hypotheses)

Each NOVELTY-STABLE state gets ONE ledger line asking the only
question that matters: *what input dimension likely selected this
state?* — the input's diff against its parent (the mutation) is the
candidate cause, recorded as a HYPOTHESIS with the state-key as
evidence. Rules: one hypothesis per novelty, falsifier stated
(re-run parent + single-dimension change); the diagnosis pipeline
(minimization) starts only from a hypothesis record — never from a
raw "weird response" (W5).

## 4. Falsifiers — what would prove this method wrong

* Two analysts' bucket declarations differ and the maps diverge →
  the buckets were under-specified: re-declare at coarser class,
  re-run, record the correction (the map is the contract).
* Novelty rate stays high but hypotheses all die at the falsifier →
  the state-key mixes noise dimensions (e.g. session token in
  first-line class): remove the offending dimension from the schema,
  new map version.
* Rerun floor flips > 20% of "novel" entries to jitter → the service
  is stateful across probes: interleave a reset/baseline probe pair
  and key the map on the DELTA, else the run is void.
* The corpus's novelty-frontier is all young inputs → the cull rule
  is starving old-but-load-bearing seeds: cap the young-quota at
  60% and re-measure.

## 5. Worked micro-example (numbers consistent, incident fictional)

API target, 6 parameters. M1 buckets declared (5 log2 length
buckets, 3 body-shape classes). Slice 1 (500 execs): yield 4.2%
(21 new state-keys); slice 2: 1.8%; slice 3: 0.4%; slice 4: 0.2% →
gate fires at consecutive < 0.5% → re-seed from frontier. One
NOVELTY-STABLE key: status 200 → 412, length-bucket 256→4k,
body-shape JSON→error-page — rerun 3/3 stable. M5 hypothesis:
`charset parameter selects a validator branch` (mutation diff =
charset value change), falsifier declared. Corpus 37/50, evicted 2.
HANG-CLASS entries: 3, clocked at median 9.1 s vs baseline IQR
0.3 s — parked as clocked artifacts, not crashes.
