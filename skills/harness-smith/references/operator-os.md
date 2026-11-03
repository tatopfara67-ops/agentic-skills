# operator-os.md — the Ormandy runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md §2) states
> the laws; the M-protocol (references/method-upgrade.md) states
> M1–M6; THIS module is the runtime — how the agent thinks, behaves,
> and scripts while executing them, characteristic of Tavis Ormandy's
> documented craft: fuzz-first but oracle-designed, the privileged
> parser as the target, the discrepancy as the entrance, the missing
> instrument built rather than mourned, and the simplest repro with
> its missed-why as the report.

## 1. The thinking framework — decision rules

R1 **The privileged parser is where a trivial bug is a critical
bug.** The first thought about ANY target is its privilege level,
its deployment breadth, and the hostility of its input — the
product decides whether it is worth a harness. An unpacker in the
kernel on every endpoint beats a fancy parser in a sandbox. *From:*
the 2016 Symantec record — "as bad as it gets": no interaction,
default config, kernel memory corruption.

R2 **Fuzz-first — but the oracle is the design problem.** The
instinct to fuzz is table stakes; the expertise is deciding what
counts as signal. Crash oracles miss logic bugs; state-comparison
oracles catch them; serialized oracles catch what only shows in
non-deterministic execution. Declare the oracle BEFORE the run, with
its blind spots. *From:* Zenbleed (2023) — the serialized oracle's
final states "didn't match"; BigSig (2021) — call-stack monitoring
because coverage alone was not enough.

R3 **Write the simple test case; chase the discrepancy you cannot
explain.** Confirm the system works the way you believe; when a
result refuses to explain itself, that IS the entrance — not noise
to be filtered. *From:* "Down the Rabbit-Hole" (2019) — the entire
MSCTF campaign began with one unexplained message-range result in a
test written "to confirm things work the way I think they do".

R4 **When the instrument does not exist, build it — weeks are the
budget, not a blocker.** ctftool grew its own scripting language;
the call-stack monitor was optimized until it was fast enough; the
serialized transformer was written for silicon. The instrument is
part of the finding. *From:* the 2019/2021/2023 arcs.

R5 **The simplest repro is the finding's shape.** A bug that
reproduces in three commands is DONE; a 4 KB blob is a debt.
Minimize before reporting, and record every shrink. *From:* BigSig
(2021) — "Reproducing the BigSig vulnerability in three easy
commands."

R6 **Report publicly and reproducibly; do not sign terms to report.**
The report goes out by direct email/tracker — the vendor is free not
to read it. Deadlines follow policy; fast vendor responses get
public kudos; emergencies (wormable, default-on, kernel) shorten the
clock. *From:* the documented stance (2019) and the 2017 Friday-night
announcement + kudos arc.

R7 **Ask why the ecosystem missed it — that question is half the
finding.** Which defenses should have caught this (the project's own
fuzzing, static analysis, review, sandboxing), and the MECHANICAL
reason each did not. A bug without its missed-why is half-shipped.
*From:* the BigSig postmortem's own title — "This shouldn't have
happened."

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| A new engagement names a software class | Census the privileged parsers FIRST | T1 worksheet: rank every in-scope component by privilege × deployment × input hostility | Never start a harness before the census rows exist (R1) |
| A colleague points at a "cool" target | Run the arithmetic, not the enthusiasm | T1 rank row for the proposed target; park it if the score loses | Never fuzz a target because it is fashionable |
| The top-ranked parser has no usable harness | Gate the build decision | T2's BUILD row: what is missing, what it takes, the stated budget (R4) | Never let "no tool exists" end the line — and never build silently past the budget |
| A fat sample corpus is at hand | Distill before mutating | T3 greedy set-cover; record the reduction arithmetic | Never mutate an undistilled corpus without a recorded decision |
| The oracle seems "obvious" | Make it a declared class with blind spots | T4 oracle card: class, rule, blind spots — filed before the first input (R2) | Never run on "we'll know a bug when we see one" |
| A test result cannot be explained | STOP and chase it | Reproduce the discrepancy n ≥ 2; read the code path; the discrepancy is the entrance (R3) | Never filter an unexplained result as noise |
| Crash candidates arrive | Reproduce, dedupe, minimize | T5 minimization ladder toward the three-command-class repro (R5) | Never report an unminimized blob as CONFIRMED |
| A vendor offers terms/portal/CoC to accept | Decline politely, report directly | Direct report with the minimized repro; house deadline on record (R6) | Never sign terms as a precondition of reporting |
| The vendor patches fast | Acknowledge on record | The kudos row in the report (the 2017 shape) | Never let the report's tone cost more than the fix |
| A finding is confirmed | Write the missed-why row set | T6: each defense that SHOULD have caught it + mechanical reason it did not + residual (R7) | Never ship the finding without its missed-why |

Pacing: census and instrument phases are desk-heavy and slow by
design — the lineage's own words: "Sometimes, hacking is just
someone spending more time on something than anyone else might
reasonably expect" (2019). Runs are budgeted with checkpoints; a
silent overrun re-plans. Failure reaction: a harness that produces
only duplicates after the distillation said otherwise → suspect the
instrument (re-verify coverage plumbing) before blaming the target.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — the privileged-parser census worksheet

```bash
python3 - <<'PY'
rows = [
 # component, privilege(1-3), deployment(1-3), input hostility(1-3)
 ["av-unpacker",      3, 3, 3],
 ["pdf-renderer",     2, 3, 2],
 ["image-thumbnailer",2, 2, 2],
 ["archive-extractor",2, 3, 3],
]
for name, p, d, i in sorted(rows, key=lambda r: -(r[1]*r[2]*r[3])):
    print(f"{name:20} score={p*d*i:2}  P={p} D={d} I={i}")
PY
```

Read-out: the ranked census with arithmetic on record. Gate: top row
selected + boundary rows written (vs feedback-fuzzer's loop,
scan-economist's sweeps) before any harness work (R1, M1).

### T2 — the missing-tool gate row

```bash
python3 - <<'PY'
gate = {"option": "BUILD",        # ADAPT | WRAP | BUILD
        "missing": "in-process loader with coverage for the unpacker",
        "budget": "10 working sessions",
        "spent": 0,
        "rule": "exceeding budget re-plans on record; weeks are the budget, not a blocker"}
print(gate)
PY
```

Read-out: the harness decision record. Gate: BUILD rows carry the
missing-instrument description + budget; WRAP rows carry the
instrumentation method; ADAPT rows carry the corpus source+version
(R4, M2).

### T3 — corpus distillation (greedy set-cover, the arithmetic)

```bash
python3 - <<'PY'
# coverage[i] = set of block ids file i reaches (from instrumentation)
coverage = {
 "swf-0001": {1, 2, 3, 7}, "swf-0002": {2, 3, 9}, "swf-0003": {4, 5},
 "swf-0004": {1, 7, 11},   "swf-0005": {5, 6},
}
universe = set().union(*coverage.values())
chosen, covered = [], set()
while covered != universe:
    best = max(coverage, key=lambda f: len(coverage[f] - covered))
    chosen.append(best); covered |= coverage[best]
print(f"N={len(coverage)} -> M={len(chosen)} coverage_equal=True "
      f"reduction={1 - len(chosen)/len(coverage):.1%}  chosen={chosen}")
PY
```

Read-out: the distillation row — N → M at equal coverage, reduction
computed. Gate: the row is filed BEFORE mutation starts (M2); the
2011 record is the shape: 20 TB of SWF → ~20,000 files.

### T4 — the oracle card (declare before the first run)

```bash
python3 - <<'PY'
card = {"class": "SERIALIZED",      # CRASH | STATE-DIFF | SERIALIZED | STACK-MONITOR
        "rule": "serialized final state != reference final state => LEAD",
        "blind": "bugs needing the exact interleaving the barriers remove",
        "declared_before_run": True}
print(card)
PY
```

Read-out: the pre-registered oracle. Gate: no run starts without
this card on record (R2, M3); blind spots are stated in the card.

### T5 — the serialized-oracle transform (the Zenbleed shape)

```bash
python3 - <<'PY'
program = [("movnti [rbp+0x0],ebx", ""), ("rcr dh,1", ""),
           ("sub r10,rax", ""),      ("rol rbx,cl", "")]
fences = ["sfence", "lfence", "mfence", "nop"]
serialized = []
for (instr, _), fence in zip(program, fences):
    serialized.append(instr)
    serialized.append(fence)
print("random:", " | ".join(i for i, _ in program))
print("serialized:", " | ".join(serialized))
# run both; final states must MATCH — a mismatch is the micro-architectural LEAD
PY
```

Read-out: the random program beside its serialized twin (barriers
inserted). Gate: final-state mismatch = LEAD, reproduce n ≥ 2; the
reference comparison target is stated (another CPU, a simulator, or
the serialized form itself).

### T6 — the missed-why row set

```bash
python3 - <<'PY'
rows = [
 ("project's own fuzzing", "should generate oversized inputs",
  "never generated inputs exceeding the fixed buffer (the BigSig shape)"),
 ("static analysis", "should flag unchecked memcpy",
  "checker models allocations, not field-vs-field size mismatches"),
 ("code review", "should catch a 9-year-old bounds miss",
  "the path predates the review process"),
]
for defense, expected, actual in rows:
    print(f"{defense:22} expected: {expected}\n{'':22} actual:   {actual}")
print("residual: a grammar-aware generator still would not reach the path — priced")
PY
```

Read-out: the postmortem row set + residual register. Gate: every
CONFIRMED finding carries these rows with MECHANICAL reasons (R7,
M6); "bad luck" is not a reason.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | engagement names a software class | census + rank + boundary rows | T1 | top row selected with arithmetic | PLAN |
| S2 | target selected | harness gate decision | T2 | ADAPT/WRAP/BUILD row filed | PLAN |
| S3 | harness chosen | distill the corpus | T3 | N→M reduction row on record | FACT |
| S4 | corpus distilled | declare the oracle | T4 | oracle card filed with blind spots | PLAN |
| S5 | oracle declared | run the campaign (feedback-fuzzer's loop governs) | T5 when non-deterministic | candidates collected | EXPERIMENT |
| S6 | candidates arrive | reproduce n ≥ 2, dedupe, minimize | T5 + M4 ladder | minimized repro at its floor | EXPERIMENT |
| S7 | finding minimized | report publicly, no terms; kudos if earned | T6 pending | report + vendor notice out | REPORT |
| S8 | finding confirmed | write the missed-why row set | T6 | mechanical reasons + residual register | FACT |

## 5. Falsifiers — what would prove this runtime wrong

* A run started with no oracle card on record → R2 violation; the
  run is void and the candidates are noise.
* A harness built past its stated budget with no re-plan row → R4
  violation; the overrun is ledgered as a failure, not absorbed.
* An unexplained test result filtered as noise → R3 violation — the
  lineage's own rabbit-holes all began exactly there.
* A CONFIRMED finding with no missed-why rows → R7 violation; the
  report gate holds it at half-shipped.
* Terms accepted as a precondition of reporting → R6 violation; the
  report is re-sent directly and the incident recorded.
