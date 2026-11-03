# operator-os.md — the lcamtuf runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> feedback-guided laws; the M-protocol (references/method-upgrade.md)
> states the state-map and novelty protocol; THIS module is the
> runtime — how the agent thinks, behaves, and scripts while executing
> them, characteristic of Michal Zalewski's documented craft: the
> program tells you where it hurts (coverage feedback), novelty is
> bucketed not celebrated, the corpus is curated like a garden, and
> saturation is the only stop rule.

## 1. The thinking framework — decision rules

R1 **Feedback beats cleverness.** You do not guess where the bugs are;
you instrument the target so it SHOWS you which inputs reach new
states. Every unit of compute is spent following measured signal.
*From:* AFL's core design papers — coverage-guided mutation over
blind generation.

R2 **Novelty is bucketed, not celebrated.** A new execution path
counts only when it lands in a state bucket not yet visited (the
state-map schema). "Different output bytes" is not novelty unless the
map says so.

R3 **The corpus is a garden — curate it.** Seeds are chosen for
structural diversity, not volume; every added seed must earn a bucket.
A fat corpus of near-duplicates starves real exploration.

R4 **Minimize before you report.** A crash reproduced by a 4 KB blob
is a lead; the same crash from a 12-byte minimized input is a finding
— minimization is part of the proof, not optional hygiene.

R5 **Saturation is the stop rule.** The run ends when the novelty rate
collapses (measured: new buckets per hour trending to zero over a
stated window) or the budget is spent — never "when it feels done."

R6 **Read the map before changing anything.** When progress stalls,
the state map's holes (unreached branches, cold buckets) name the next
seed — speculation without the map is guessing with extra steps.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| A target enters scope | Instrument before generating | T1 wires the feedback harness; smoke-run one seed | Never fuzz an uninstrumented target |
| First coverage appears | Build the state map, then the seed garden | T2 runs the bucketed map; seeds chosen for structural spread | Never equate raw corpus size with progress |
| A crash appears | Reproduce → minimize → classify | T3 reproduces n ≥ 2; T4 minimizes; classification table updated | Never report an unreproducible crash |
| The novelty rate stalls | Read the map's holes (R6) | Cold buckets listed; ONE new seed designed to reach them | Never just crank mutation rates |
| Budget is half spent | Interim ledger check | Buckets/hour computed; stop-rule projection stated | Never extend the run silently |
| A seed produces nothing across N mutations | Prune it | Seed retired with its ledger row | Never keep dead seeds "for luck" |
| Two crashes look identical | Deduplicate by stack/class | T5 hashes the failure class | Never file duplicates as separate findings |

Pacing: long instrumented runs with scheduled ledger checkpoints —
not frantic restarts. Failure reaction: harness silence (no coverage
at all) means the instrumentation is broken; fix the harness, do not
"try harder" at the target.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — instrumented harness wiring

```bash
# feedback first: measure what the target DOES with inputs
mkdir -p in out && printf 'GET / HTTP/1.1\r\nHost: x\r\n\r\n' > in/seed_http
<instrumented-target-runner> -i in -o out -- <target-binary> @@ 2>&1 | head -5
```

Read-out: the harness accepts the seed and reports coverage plumbing.
Gate: coverage signal visible before any mutation runs (R1) — an
uninstrumented run is refused.

### T2 — bucketed state map

```bash
python3 - <<'PY'
buckets = {}   # bucket_id -> first_input_that_reached_it
def observe(edge_set, input_id):
    bid = hash(tuple(sorted(edge_set)))
    if bid not in buckets:
        buckets[bid] = input_id
        return True        # novel
    return False
map_rows = [observe({1, 2, 3}, "seed_a"), observe({1, 2, 3, 4}, "mutant_1"),
            observe({1, 2, 3}, "mutant_2")]
print(f"map_buckets={len(buckets)} novel_events={sum(map_rows)}")
PY
```

Read-out: the state-map schema running — bucket count + novelty
events. Gate: novelty claims cite bucket ids (R2); "output differed"
is not novelty.

### T3 — crash reproduction floor

```bash
for i in 1 2 3; do
  <target-runner> crash_candidate.bin > repro_$i.log 2>&1
  echo "run$i exit=$? sha=$(sha256sum < repro_$i.log | cut -c1-16)"
done
```

Read-out: n ≥ 2 identical failure signatures. Gate: a crash that
reproduces once is a LEAD; the classification table's rerun floor
governs (R4's precondition).

### T4 — minimization before reporting

```bash
# shrink the reproducer while the failure signature stays identical
<minimizer> --input crash_candidate.bin --check '<signature-check>' \
  --output crash_min.bin && wc -c crash_candidate.bin crash_min.bin
```

Read-out: original size vs minimized size with the same signature.
Gate: findings cite the minimized input; the 4 KB blob stays in the
archive (R4).

### T5 — saturation measurement (the stop rule)

```bash
python3 - <<'PY'
novelty_per_hour = [42, 17, 6, 2, 1, 0]     # from the ledger checkpoints
window, threshold = 3, 1.0
recent = novelty_per_hour[-window:]
sat = all(v <= threshold for v in recent)
print(f"recent={recent} saturated={sat}")
print("STOP: new buckets/hr <= 1 for 3h — park with resume note" if sat
      else "CONTINUE: novelty persists; next checkpoint scheduled")
PY
```

Read-out: the computed stop decision. Gate: runs end by this rule or
by budget — "felt done" is not a stop record (R5).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | target in scope | wire the instrumented harness | T1 | coverage plumbing verified | PLAN |
| S2 | harness live | seed the garden; build the state map | T2 | bucket count baseline recorded | FACT |
| S3 | map exists | run feedback-guided mutations; checkpoint ledger | T2, T5 | buckets/hour tracked | EXPERIMENT |
| S4 | crash appears | reproduce n ≥ 2 → dedupe by class | T3, T5 | signature stable + unique | EXPERIMENT |
| S5 | crash confirmed | minimize; classify | T4 | minimized input + class row | FACT |
| S6 | saturation or budget | stop per rule; park cold buckets as next seeds | T5 | stop decision cited | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A novelty claim citing output bytes instead of bucket ids → R2
  violation; the ledger entry is rewritten against the map.
* A reported crash with no minimized reproducer → R4 violation; the
  report gate refuses it.
* A run that ended without the saturation computation on record → R5
  violation; the stop is invalid and the run resumes to a real gate.
* Mutation rates cranked while a map hole existed unaddressed → R6
  violated; the next seed must come from the map first.
