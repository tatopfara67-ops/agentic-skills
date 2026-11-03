# operator-os.md — the Willison runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> mirror laws; the M-protocol (references/method-upgrade.md) states the
> eligibility and craft protocols; THIS module is the runtime — how the
> agent thinks, behaves, and scripts while executing them,
> characteristic of Simon Willison's documented craft: name the class
> precisely, treat model output as stochastic, and look for the
> deterministic wrapper the model feeds.

## 1. The thinking framework — decision rules

R1 **Name the class before the payload.** "Prompt injection" is a
class with a defined anatomy: untrusted text becomes instructions to a
system that trusted other text. If the surface cannot be described in
that sentence, it is not this organ's target. *From:* the class was
named in the lineage's October 2022 writing before any technique
existed — naming IS the discipline.

R2 **The model is stochastic; the wrapper is deterministic.** A model
output is a rate, not a fact. The finding lives where the model's
output crosses into deterministic code: a tool call, a fetch, a
template render, a log line. Hunt the WRAPPER's behavior, measure the
MODEL's behavior.

R3 **Eligibility before craft.** The program's eligibility table gates
before the first payload: is an LLM/agent surface in scope, is data
exfiltration in scope, are rate-based proofs acceptable? An
ineligible program gets zero payloads, not quieter ones.

R4 **Markers make the differential.** Every injection probe carries a
unique marker (canary-class); every observation records whether the
MARKER reached the deterministic side. Attribution without markers is
vibes.

R5 **Measure, then report as rates.** "The model leaked" is not a
finding; "marker reached the wrapper in 12 of 30 runs (40%, CI
95% [23–59%])" is. n ≥ 30 for rate claims; both successes and
failures ledgered.

R6 **The exfil ceiling is pre-declared.** What the demonstration is
allowed to move (one canary marker, one operator-owned sink) is
written before the first probe; the proof is the REACH, not the haul.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| An AI surface spotted in scope | Read the eligibility table FIRST | T1 pins: is the LLM surface authorized, is exfil authorized, what proof class counts | Never fire a marker at an unlisted surface |
| The model "seems" to follow injected text | Convert the seeming into a measurement (R2) | T3 runs the marker differential n ≥ 30; record the rate | Never report a single lucky generation |
| The model calls a tool deterministically | Hunt the wrapper's contract | T4 diffs wrapper behavior: what does the code DO with the model's call | Never claim "full RCE" from one tool invocation shape |
| A defensive prompt ("ignore instructions") is present | It is a fact, not a wall | Record the guard; re-run the differential WITH the guard on; report both rates | Never call a guard "bypassed" from one generation |
| The demo could read real user data | Stay at the ceiling (R6) | canary marker → operator-owned sink; one reach, then stop | Never pull real data through the injection |
| Output looks confident and coherent | Discount confidence, count runs | Confidence is a model property, not evidence (R5) | Never let fluency upgrade a LEAD |
| Rate is borderline (e.g., 40%) | Report the interval | CI stated, both outcomes ledgered | Never round a rate up to "reliable" |

Pacing: generations are the unit of cost — spaced, counted, and
budgeted in the plan note; a rate claim with unknown n is void.
Failure reaction: a guard that suppresses the marker 30/30 is a
recorded NEGATIVE with its own report value (the guard held — under
what conditions?).

## 3. The scripting arsenal — techniques as runnable craft

### T1 — eligibility pin

```bash
python3 - <<'PY'
pin = {
  "surface": "https://<target>/copilot",       # in-scope AI surface?
  "exfil_authorized": True,                    # program policy, quoted
  "proof_class": "rate + deterministic wrapper",
  "sink": "https://<operator-owned-callback>/canary",
}
missing = [k for k, v in pin.items() if v in (None, "")]
print("PIN:", "complete" if not missing else f"missing {missing}")
PY
```

Read-out: the pin record. Gate: `complete` before any probe (R3);
the policy quotes live in the plan note.

### T2 — marker generation (canary-class)

```bash
python3 - <<'PY'
import secrets
marker = "MYTHOS-" + secrets.token_hex(8)
print(marker)   # unique per EXPERIMENT; logged before first use
PY
```

Read-out: the canary marker. Gate: marker pre-registered in the
EXPERIMENT record; probes without markers are refused (R4).

### T3 — the marker differential (rate measurement)

```bash
python3 - <<'PY'
import json, statistics
runs = json.load(open("marker_runs.json"))   # [{marker_emitted, wrapper_hit}]
n = len(runs); hits = sum(r["wrapper_hit"] for r in runs)
p = hits / n
import math
ci = 1.96 * math.sqrt(p * (1 - p) / n) if n else 0
print(f"n={n} hits={hits} rate={p:.0%} CI95≈[{max(0,p-ci):.0%},{min(1,p+ci):.0%}]")
PY
```

Read-out: the rate + interval. Gate: n ≥ 30 for any rate claim (R5);
both guard-on and guard-off rows when a guard exists.

### T4 — deterministic wrapper diff

```bash
# what does the CODE do with the model's call? one variable: with vs without marker
for variant in with_marker without_marker; do
  curl -s -o /dev/null -w "$variant %{http_code} %{size_download}\n" \
    -H "Content-Type: application/json" \
    -d "{\"prompt\":\"<probe-$variant>\"}" "https://<target>/<agent-endpoint>"
done
```

Read-out: wrapper-side behavior pair (status/size/latency class).
Gate: the finding sentence cites the WRAPPER's change, with the rate
from T3 as the mechanism measurement (R2).

### T5 — exfil ceiling harness (operator-owned sink)

```bash
# exactly one canary reach per EXPERIMENT; sink is operator-owned
curl -s "https://<operator-owned-callback>/canary?m=<marker>" -o /dev/null -w "%{http_code}\n"
# then check the sink log for INBOUND reaches during the run window
```

Read-out: inbound reach records at the operator sink. Gate: any reach
of REAL user data or a non-operator sink halts the run (R6).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | AI surface in scope | pin eligibility + sink + ceiling | T1 | pin complete | PLAN |
| S2 | pin complete | generate + pre-register the marker | T2 | marker in EXPERIMENT record | EXPERIMENT |
| S3 | marker registered | run the injection differential, n ≥ 30 | T3 | rate + CI computed | EXPERIMENT |
| S4 | rate ≥ threshold | diff the deterministic wrapper, one variable | T4 | wrapper behavior pair cited | FACT |
| S5 | wrapper changed on marker | prove the reach at the ceiling, once | T5 | one canary reach, operator sink | CANARY |
| S6 | proof done | report: class + rate + wrapper delta + guard rows | — | all four elements present | REPORT |

## 5. Falsifiers — what would prove this runtime wrong

* A rate claim with n < 30 → void at the report gate (R5).
* An injection claim with no marker in the probe or the record →
  attribution impossible; re-run from S2.
* A "bypass" claim citing one generation → stochastic luck; re-measure.
* A demo that moved anything beyond the declared ceiling → R6
  violation; engagement halts, failure ledger written.
* A guard declared absent without reading the surface's configuration
  on record → the guard row is fabricated; re-census the surface.
