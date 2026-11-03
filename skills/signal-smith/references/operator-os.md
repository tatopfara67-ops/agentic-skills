# operator-os.md — the Draper runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> signal laws; the M-protocol (references/method-upgrade.md) states the
> calibration and seam protocol; THIS module is the runtime — how the
> agent thinks, behaves, and scripts while executing them,
> characteristic of John Draper's documented craft: one precisely
> forged in-band signal, indistinguishable from the legitimate one —
> never a spray, never an alarm.

## 1. The thinking framework — decision rules

R1 **Learn the legitimate signal before forging anything.** The blue
box worked because its 2600 Hz was the REAL operator tone —
calibration first, forgery second. Every encoding craft begins by
capturing what the system already accepts as genuine. *From:* the
1971–72 record: the discovery was a cereal-whistle tone that happened
to match the network's own supervisory frequency.

R2 **In-band beats out-of-band.** The interesting channel is the one
the system already trusts and carries data on: a header encoding, a
charset transform, a numeric field's grammar. If you need a new
channel to reach the bug, you are probably in the wrong organ.

R3 **One forged variation, once.** Send the single precisely-crafted
variation; observe; decide. Sprays destroy attribution and raise
alarms — the exact anti-pattern this lineage exists to kill.

R4 **Precision is a budget, not a vibe.** Every grammar has tolerances
(the encoding-grammar module's tables); the forge states which byte,
which position, which deviation class. "Some weird encoding" is not a
craft record.

R5 **The differential is the proof.** Legitimate signal vs forged
signal, both sent, both observed — the seam is shown by the system
treating the forgery as genuine. One restoring byte = the control.

R6 **Never trip the alarm you can avoid.** Rate, volume, and
distinctiveness are tuned so the periphery's logs show a normal
conversation. If the only way forward is noise, park the seam.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| A new encoding surface enters scope | Capture the grammar BEFORE crafting | T1 enumerates accepted forms; tables filled from observation | Never forge into an uncaptured grammar |
| A candidate seam suspected (two readers, one grammar) | Design ONE variation | T2 builds the minimal forged token — one byte-class deviation | Never send a family of variants "to see what sticks" |
| The forged signal is accepted | Prove it with the control | T3 differential: legit / forged / restored-control; n ≥ 2 | Never claim acceptance from a single response |
| The system errors on the forged signal | The error is data | Record the rejection class; refine ONE parameter | Never re-send at volume after a rejection |
| A WAF normalizes the channel | Recalibrate, don't escalate | Re-run T1 on the normalized channel; update tables | Never fight the normalizer with more bytes |
| The seam needs noisy volume to trigger | Park it | Resume note with the noise threshold documented | Never trade stealth for a maybe |
| Encoding tables drift (target updated) | Re-capture | T1 fresh capture; versioned tables with as-of stamps | Never run on stale grammar silently |

Pacing: minutes between sends; a full differential (3 conditions × n
runs) is the working unit. Failure reaction: rejection classes are
ledgered as grammar rows — the map grows from failures, it does not
retry them.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — grammar capture (accepted forms, observed)

```bash
python3 - <<'PY'
import urllib.parse
observed = {
  "plain":      "profile.asp?name=alice",
  "plus":       "profile.asp?name=a%20lice",
  "percent":    "profile.asp?name=%61lice",
  "double":     "profile.asp?name=%2561lice",
  "utf8-pct":   "profile.asp?name=%c0%aflice",
}
for cls, sample in observed.items():
    print(f"{cls:10} {sample}")
# each class sent ONCE; response class + length recorded into the table
PY
```

Read-out: the acceptance table (form class → response class). Gate:
every row has its observed response before any forged token exists
(R1); tables carry as-of stamps.

### T2 — single forged variation (minimal deviation)

```bash
# ONE byte-class deviation from the accepted form — designed, not sprayed
python3 - <<'PY'
base = "alice"                     # accepted form from T1
forged = "ali%63e"                 # one class deviation: percent-encoded 'c'
control = "alice"                  # restoring form (no deviation)
print(forged, "|", control)
PY
```

Read-out: the designed treatment + its control. Gate: the EXPERIMENT
record states the deviation class BEFORE the send (R3, R4).

### T3 — the blind in-band differential

```bash
for cond in legit forged control; do
  for i in 1 2; do   # n_runs >= 2 per condition, interleaved
    curl -s -o /dev/null -w "$cond run$i %{http_code} %{size_download} %{time_total}\n" \
      "https://<host>/profile.asp?name=<payload-$cond>"
  done
done
```

Read-out: 3 × 2 observation grid. Gate: forged ≠ legit AND control ==
legit → the seam is proven on that byte class (R5); any drift voids
the grid and re-baselines.

### T4 — precision budget check (computed)

```bash
python3 - <<'PY'
grammar = {"header_name_case": 2, "path_encoding": 5, "param_case": 3}
seam = "path_encoding"
print(f"classes={len(grammar)} seam={seam} deviations_on_seam={grammar[seam]}")
print("budget: ONE deviation per EXPERIMENT; ", grammar[seam], "experiments to cover this seam")
PY
```

Read-out: the arithmetic of covering the seam class-by-class. Gate: a
plan that exceeds the budget parks classes with resume notes — it
never batches them (R3).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | encoding surface in scope | capture the grammar, versioned | T1 | acceptance table + as-of stamp | FACT |
| S2 | grammar captured | design ONE minimal forged variation + control | T2 | deviation class pre-registered | EXPERIMENT |
| S3 | design committed | run the 3-condition differential, interleaved | T3 | confirm rule met or void recorded | EXPERIMENT/CONTROL |
| S4 | seam confirmed | classify the seam; cite both parsers' behavior | T1 tables | seam class + grammar row cited | FACT |
| S5 | seam classed | cover remaining classes one experiment each | T4 budget | remaining classes parked or covered | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A forged token with no captured acceptance table behind it → R1
  violation; the craft record is void until the grammar is captured.
* Two deviation classes in one payload → attribution broken (R3);
  split and re-run.
* An acceptance claim with no control condition → not a differential;
  demoted to LEAD (R5).
* Repeated sends of a rejected class found in the log → the alarm
  discipline failed; the seam is parked and the incident noted.
