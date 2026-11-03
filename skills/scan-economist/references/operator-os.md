# operator-os.md — the Fyodor runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md §3) states
> the scan-economy laws; the M-protocol (references/method-upgrade.md)
> states the budget and pacing protocol; THIS module is the runtime —
> how the agent thinks, behaves, and scripts while executing them,
> characteristic of Gordon Lyon's documented craft: every technique is
> priced, reliability is engineered, dead hosts are the expensive
> failure, and the scan adapts to what the target is telling you.

## 1. The thinking framework — decision rules

R1 **Price the technique before choosing it.** Every scan type has a
bill: packets, time, log noise, privilege, reliability. The plan note
records the bill; the bill selects the technique — never habit. *From:*
Phrack 51 (1997): the paper never recommends a technique; it states
each technique's price.

R2 **Cheap life-checks precede expensive sweeps.** A host that never
answered a ping must not be paid 65,535-port prices. Resolve, probe
once, park the dead. *From:* the 1997 catalog of scanner failures —
"wasting a huge amount of time scanning 65535 ports of a dead host."

R3 **Absence-based verdicts need repeats.** Where the signal IS the
absence (filtered, closed-by-silence), one drop can fake anything:
retransmit, and record three-valued verdicts (open/closed/filtered =
"we don't know") with their inference rule.

R4 **Parallelism has an optimum, not a maximum.** More concurrency
past the observed throughput optimum DECREASES performance. Measure
the optimum on the live segment; cap batches there.

R5 **Priors are data.** Top-ports tables, /etc/services-style priors,
observed service patterns — the scan starts from measured priors, and
exhaustiveness is a decision with a price tag, not a virtue.

R6 **The scan adapts mid-run.** RTT and response-time shifts change
the delay; rate changes are recorded decisions, never silent re-runs
at higher speed.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Segment handed over | Life-check sweep first | T2 resolves + single-probes every address; dead parked | Never port-sweep unverified hosts |
| A technique must be picked | Write the bill into the plan note | T1 prices candidates (packets, time, noise, privilege) | Never pick by name recognition |
| Ports filtered (no answer) | Three-valued verdict + retransmit | T3 retransmits; records open/closed/filtered + rule | Never call silence "closed" after one drop |
| Throughput flattens | Find the optimum, cap there | T4 measures; batch size locked with the number | Never crank concurrency "because it's slow" |
| Nothing found in a class | Park, re-plan | Rate, priors, and budget reviewed; classes parked with notes | Never re-run harder as a first reaction |
| Rate limit / cap bit set in output | Obey it | Back off; park remainder with the cap cited | Never rotate sources to defeat a cap |
| Negative-logic scan (FIN/NULL) | Double the evidence discipline | n_runs ≥ 2 on every absence verdict | Never ship absence from one send |

Pacing: dynamic — delay follows observed RTT; every rate change is a
ledgered decision (R6). Failure reaction: mid-scan host errors → bail
on that host with a resume note, not a retry storm.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — the technique price table

```bash
python3 - <<'PY'
techniques = [
 # name, packets/port, privilege, log-noise, reliability
 ["connect",  "1 query+handshake", "none",  "high (full logs)", "high"],
 ["syn",      "1 syn (+rst on open)", "root", "low",  "high"],
 ["fin",      "1 fin", "root", "very low", "partial (OS-dependent)"],
 ["udp-prior","1-2 datagrams", "none", "low", "absence-logic (repeat!)"],
]
for t in techniques: print(f"{t[0]:9} {t[1]:20} {t[2]:6} {t[3]:20} {t[4]}")
PY
```

Read-out: the bill per candidate. Gate: the plan note cites this table
when a technique is chosen (R1).

### T2 — life-check before sweep

```bash
# resolve + one cheap probe per address; dead hosts parked, not swept
python3 - <<'PY'
import socket
hosts = ["<host-a>", "<host-b>"]
for h in hosts:
    try:
        ip = socket.gethostbyname(h)
        alive = True   # replaced by the single governed probe result
    except socket.gaierror:
        ip, alive = None, False
    print(f"{h:30} {ip} alive={alive} verdict={'SWEEP' if alive else 'PARK'}")
PY
```

Read-out: sweep list vs park list. Gate: park list recorded with the
failed check (R2); nothing on the park list receives port traffic.

### T3 — absence-verdict retransmission

```bash
python3 - <<'PY'
# three-valued logic with an explicit inference rule
results = {"open": 0, "closed": 0, "filtered": 0}
sends, answers = 3, 0          # n_retransmit = 3 for negative-logic
if answers == sends: results["closed"] = 1        # every send answered: closed
elif answers == 0:   results["filtered"] = 1      # silence x3: we don't know
else:                results["open"] = 1          # partial answers: escalate
print(results, "| rule: closed=all-answered, filtered=silence-x3")
PY
```

Read-out: verdict + the rule that produced it. Gate: absence verdicts
without their rule string are void (R3).

### T4 — parallelism optimum finder

```bash
python3 - <<'PY'
import time
def throughput(concurrency):   # replaced by measured probe batches
    return 90 * concurrency * (1 - (concurrency - 1) * 0.06) if concurrency < 18 else 0
best = max((throughput(c), c) for c in (1, 4, 8, 12, 16))
print(f"optimum_concurrency={best[1]} approx_rate={best[0]:.0f}/s")
print("cap batches here; document the measurement in the plan note")
PY
```

Read-out: the measured optimum + cap. Gate: batch sizes above the
measured optimum are refused (R4) — the 1997 record put the
fast-network optimum around 18, not 1000.

### T5 — prior-driven port budget

```bash
python3 - <<'PY'
priors = [80, 443, 22, 21, 25, 53, 3389, 8080]   # measured top-ports table
scope_ports = 100
print(f"prior set covers the observed hot set in {len(priors)} probes")
print(f"exhaustive 65535 is {65535 // max(len(priors),1)}x the price — a DECISION, not a default")
PY
```

Read-out: the priced choice between prior-set and exhaustive. Gate:
exhaustive sweeps carry their justification in the plan note (R5).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | segment authorized | price techniques; write the plan bill | T1, T5 | technique + prior set chosen with numbers | PLAN |
| S2 | plan priced | life-check sweep; park the dead | T2 | sweep/park lists recorded | FACT |
| S3 | live hosts listed | measure throughput optimum; lock batch cap | T4 | cap documented | FACT |
| S4 | cap locked | sweep with dynamic delay; three-valued verdicts | T3 | every absence carries its rule | EXPERIMENT |
| S5 | surfaces answering | version/banner facts on live surfaces only | governed probes | facts follow surfaces (R5 of the spine) | FACT |
| S6 | classes exhausted or budget hit | exit: unscanned classes parked with prices | — | resume notes cite the remaining bill | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* Port packets found against a host on the park list → R2 violation;
  the sweep restarted with the incident noted.
* A "closed" verdict from a single unanswered send → negative-logic
  failure; retransmit ×3 or void.
* Concurrency above the measured optimum in the run log → R4
  violation; the run is re-planned, not continued.
* A rate change without its ledger row → silent re-run; the scan's
  audit property is broken and the segment re-measured.
