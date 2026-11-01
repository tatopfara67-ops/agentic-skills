# mindset.md — the lcamtuf decision logic, translated

## 1. The mind, as observed in the sources

From AFL's design document (technical_details.txt — read in full):

* **Coverage as cheap tuples.** `shared_mem[cur_location ^
  prev_location]++` — a 64KB map, sized to sit in L2 cache. "This form
  of coverage provides considerably more insight… than simple block
  coverage," while avoiding "computationally intensive and fragile
  global comparisons of complex execution traces" and "the scourge
  of path explosion." The lesson generalizes: novelty detection must
  be CHEAP or it will be skipped.
* **Bucketed counts.** Hit counts collapse into buckets (1, 2, 3,
  4-7, 8-15, 16-31, 32-127, 128+); "changes within a bucket are
  ignored; transitions between buckets are flagged as interesting."
  Coarse on purpose: fine-grained novelty is mostly jitter.
* **Guided beats blind, decisively.** The doc's comparison: ~1,765
  blocks / 2,597 edges explored by the guided model vs 228/265 by
  blind fuzzing. "Greedy approaches appear to confer no substantial
  benefits over blind fuzzing strategies" — the MAP is the value,
  not clever selection.
* **Not greedy, on purpose.** "Not a greedy genetic algorithm" —
  non-favored entries are skipped "with varying probabilities
  (75-99%)" so disjoint, mutually-incompatible features stay
  reachable. Exploration is budgeted, never zeroed.
* **The corpus is curated.** Periodic culling selects a subset that
  still covers every tuple, "scoring entries based on execution
  latency and file size"; the favored corpus is "usually 5-10x
  smaller than the starting data set." Memory that is not curated
  becomes ballast.
* **Trimming is a feature.** Small inputs fuzz faster and reproduce
  cleaner; afl-tmin goes further with alphabet normalization
  (ASCII '0' instead of 0x00 "to avoid interfering with text
  parsing" — even minimization thinks about the next tool).
* **Tarpits are rejected, not admired.** Timeouts calibrate from
  initial runs; "tarpits that improve coverage by 1% while being
  100x slower" are pragmatically rejected — "we… hope that the
  fuzzer will find a less expensive way to reach the same code."
* **The meta-lesson.** "AFL is not a proof of concept for any
  specific theory… a collection of hacks that have been tested in
  practice, found to be surprisingly effective, and implemented in
  the simplest, most robust way." Speed, reliability, ease of use
  over theoretical purity.

## 2. The translation table (AFL → arsenal)

| AFL concept | Organ behavior |
| --- | --- |
| edge-tuple coverage map | response state signature (status class, size bucket, key features) recorded per probe |
| bucketed hit counts | class buckets — within-bucket deltas ignored, transitions flagged |
| deterministic → chaotic phases | single-knob probes first; combined payloads only after plateau |
| input queue = corpus | the probe set that reaches each state class, kept minimal |
| corpus culling (favored set) | retiring redundant probes with records |
| 75-99% skip of non-favored | low-frequency exploratory branches stay alive |
| calibrated timeouts / tarpit rejection | R7 budget: probe classes with bad cost/state ratios get parked |
| trimming + afl-tmin | minimization of candidates before hypothesis cards |
| "collection of hacks" humility | pragmatic stopping rules over grand theory |

## 3. The state signature (this organ's unit of thought)

```
state-signature:
  class-features: [status-class, size-bucket(log2), auth-marker, key-set-hash]
  buckets: sizes as log2 bands; headers as presence-sets
  transition: any feature changes bucket/class
  K-saturation: <N> consecutive probes with zero transitions ⇒ stop
```

Write it, register it, THEN probe. The signature is the loop's
instrumentation — an uninstrumented loop is exactly the "dumb
fuzzing" the lineage exists to retire.

## 4. Failure modes this organ exists to kill

* The endless probe loop that stops when tokens run out, with no
  record of what the last 50 probes were for.
* Tremor-chasing: treating a 2-byte size difference as novelty
  (within-bucket noise) and burning budget "confirming" it.
* Chaos-first: jumping to payload chains before single-knob changes
  plateaued — then being unable to say WHICH knob mattered.
* Fat corpora: probe lists that grow monotonically because nothing
  is ever retired; the ledger equivalent of a 10x-too-big corpus.
* Unminimized PoCs: five-parameter "proofs" that no one — including
  their author — can decompose.

## 5. What the engine already enforces (do not re-implement)

* EXPERIMENT pre-registration (the signature and K are declared
  before outcomes exist).
* n_runs ≥ 2 stability before signals become surfaces (AFL's
  "reliability" principle, already the auditor's).
* Cap bits and park notes (R1/R7) — the budget side of tarpit
  rejection.
