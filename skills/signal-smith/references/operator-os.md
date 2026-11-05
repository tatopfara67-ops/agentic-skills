# operator-os.md — the Draper runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> signal laws; the M-protocol (references/method-upgrade.md) states the
> calibration and seam protocol; THIS module is the runtime — how the
> agent notices, thinks, behaves, and scripts while executing them,
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

### The opening ladder — where Draper's candidates come from

The rules above govern the craft once a seam is suspected; the ladder
produces the candidates FIRST — the phreaking-era perception (the
whistle worked because its tone matched the network's OWN supervisory
frequency: the network's genuine grammar was learned by listening
before any box was built) made runnable as questions. Every rung is a
listening question that writes rows — no rung forges a token, sends a
variation, or spends a probe; forgery stays gated behind R1/R3 and
consumes the ladder's rows.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | What does the system already accept as genuine — which form classes does the validator take? | the acceptance census: plain, plus-encoded, percent, double-encoded, overlong-UTF8 form families — the rows every later craft reads | R1's calibration-first law — the 1971–72 record: the discovery was a tone matching the network's own supervisory frequency (sources.md, the blue-box era's public record) |
| G2 | Where does one input cross two readers with different grammars? | the seam census: frontend normalization vs backend interpretation — the divergence points where a byte can be two things | the in-band anatomy on record: the control channel riding the data channel (Rosenbaum, Esquire Oct 1971 — sources.md); the operator's brief's frequency/type/format triad |
| G3 | What does a NORMAL conversation look like to the periphery? | the envelope census: request rates, volume, distinctiveness — the baseline the alarm discipline is priced against | the operator's brief on record: tuning request frequency to stay under rate filters (sources.md, the matched doctrine) |
| G4 | Which deviation classes does the observed grammar admit? | the tolerance census: byte/position/class deviations that remain within acceptance — the precision envelope, computed not felt | R4's precision budget — the encoding-grammar module's tables (the organ's own operationalization, labeled) |
| G5 | What restores each candidate seam — what is the control condition? | the control census: the restoring byte per seam — the differential's control arm, pre-named | R5's differential law (the organ's own operationalization, labeled) |

Ranking rationale: candidate priority = seam sharpness × envelope
room × unexplored class mass. A seam where the frontend normalizes a
byte the backend reads raw ranks first (the disagreement is already
on record); an accepted-but-untested grammar class ranks next; a
seam whose envelope room is thin ranks by its alarm price (parked or
priced, never sprayed); classes with a ledgered rejection rank last —
the map grows from failures, it does not retry them. Rows out; not
one forged byte sent.

Generation falsifier: an input surface where the listening sweep
yields zero rows means the grammar is not yet observable from the
channel (auth-gated, binary-framed, or a validator that answers
nothing until authenticated) — the census is re-read (the
encoding-grammar module's class families are the recorded next
ring), the missing rung written with its grounding row. The surface
is never excused as "no grammar" at generation time — every input
channel has one; a zero-yield verdict belongs to verification's
coverage row, never to the ladder.

#### The ladder's payload kit — the grammar-capture rows (customize before use)

Generation writes rows; these are the listening classes the rows name,
every one an observation of the target's own traffic-shape (no forged
token exists yet; the craft mechanics live in T1–T4):

| Listen row | The read payload class | Writes which row |
| --- | --- | --- |
| form-class row | the accepted form families: plain `alice`, plus `a%20lice`, percent `%61lice`, double `%2561lice`, overlong `%c0%aflice` — one class per read | acceptance row (form class → response class) |
| seam row | the two-reader divergence points: header name case, path encoding, parameter case — where the grammars disagree | seam-candidate row (the divergence, named) |
| envelope row | the periphery's normal: observed request rate, volume, token distinctiveness over a stated window | baseline row (what "normal" costs) |
| tolerance row | the deviation classes within acceptance: which byte, which position, which class — the envelope computed | precision-budget row (R4's arithmetic) |
| control row | the restoring form per seam candidate (the byte that reverts the forgery) | control-condition row (the differential's control arm) |

Customization knobs, stated in the plan note: the channel class
(query-string vs header vs body vs path — which grammar families
load), the deviation budget (how many classes the engagement carries
under R3's one-variation law), and the envelope policy (the rate and
distinctiveness ceiling the periphery is priced against).

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
