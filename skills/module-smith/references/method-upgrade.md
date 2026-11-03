# The executable method — M1–M5 for module-smith

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The lineage critique that
justifies each step (why these phases exist, what was weak in
HD Moore's module corpus) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

Quickstart — reliability MEASURED, never asserted (the M1 record's
fields come from these runs; M4 is the measurement loop itself):

```bash
# M2/M4 stager differential — n >= 5 per delivery class, lab rig only
for i in 1 2 3 4 5; do
  ./stager --rig lab-1 --token "run-$i" --json >> stager-runs.jsonl
done
# rank arithmetic — reliability(n,k) computed from the ledger
python3 - <<'PY'
import json
runs = [json.loads(l) for l in open('stager-runs.jsonl')]
ok = sum(bool(r.get('delivered')) for r in runs)
print(f"reliability = {ok}/{len(runs)} = {ok/len(runs):.2f}")
PY
# gate: FIELD-READY needs >= 4/5 clean reruns; abort at 2% error rate
```

### M1 — the module record

Every module (exploit, stager, payload — in this arsenal: every
reusable hypothesis or technique module) carries measured fields,
not labels:

```
MODULE: id=<X-007> kind=<technique> target-class=<web-front/J2EE>
  reliability: n=<runs> full=<k> partial=<j> clean-fail=<m>
  conditions=<precondition list each run required>
  last-measured=<date> source=<EXPERIMENT ids>
```

Rules: `reliability` without `n` is a label, refused at the report
gate; a record older than the target's last observed change is
STALE and must be re-measured before it supports a claim (W1).

### M2 — the stager differential (transport is not a detail)

Per delivery class (and per target-class where the fleet varies):

1. **Conditions, n ≥ 5 each**: stager-A (default reverse-TCP
   equivalent) vs stager-B (the alternate transport — bind-class,
   different port family, tunnel-compatible) on the SAME target
   class, interleaved.
2. **Observation vector**: established/not, latency to first stage,
   stability class (survives 60 s / dies at once / flaps).
3. **Confirm rule**: a stager class is FIELD-READY at ≥ 4/5
   established AND stability "survives" in ≥ 4/5; anything less is
   recorded conditional with its failure distribution (W2).

### M3 — the composition proof (the joint gate)

1. Each link earns M1/M2-grade evidence SEPARATELY (the
   chain-architect weakest-link rule).
2. The JOINT then runs n ≥ 5, clean-state per run, and the
   observation includes the failure classes the demo hides: stager
   size vs memory context, payload side-effects on the process the
   chain needs alive, cleanup (does the joint leave the target
   restorable?).
3. Joint confidence = min(link confidences) × joint-n factor; the
   report states the floor link (W3 made arithmetic).

### M4 — the measurement protocol (the Sonar fix)

For any exposure-measurement activity (broad, low-rate, authorized):

```
MEASURE: scope=<authorization basis> population=<n targets, source>
  rate=<pps/reqps, civility-capped> window=<duration>
  dedup=<rule: same-response-hash collapse>
  artifacts=<raw+summarized, retention window>
  harm-gates: no-exploit-class probes; abort on error-rate spike;
  disclosure=<aggregate-only, no per-org naming without basis>
```

Every field is filled BEFORE the run; deviations during the run are
appended, never edited (append-only measurement, auditable by a
third party — W4).

### M5 — the compat matrix + rank arithmetic

**(a) Matrix**: rows = module, columns = target-class × version-band;
cells = measured outcome class with n. Folklore prose converts to
cells with sources; a cell with no measurement reads EMPTY (never
"works").

**(b) Rank arithmetic** (replacing the static label):

```
rank = reliability(n,k) × field-readiness(stager class)
     × joint-factor(composition n)
```

Reported with all three factors visible; a module's rank changes
when its evidence changes, and the delta cites the EXPERIMENT that
moved it (W5, W1 together).

## 2. Falsifiers — what would prove this method wrong

* M2's alternate stager beats the default on the same class → the
  default's conditions were wrong for this fleet: re-measure, and
  the module record's `conditions` field is corrected on record.
* The joint gate passes 5/5 but a field-class precondition (egress
  rule) was absent from the lab → the composition's condition list
  was incomplete: downgrade to conditional, add the precondition as
  a first-class field.
* A compat cell measured EMPTY shows a live success in the field →
  the cell's target-class definition is too coarse: split the class,
  file the correction, re-measure both halves.
* The measurement protocol's error-rate spike abort fires at 2% of
  population → the abort was right; the follow-up rate halves and
  the event is disclosed in the aggregate (the protocol is the
  arbiter, not the operator's curiosity).

## 3. Worked micro-example (numbers consistent, incident fictional)

Technique module X-007 (deserialization check) on target-class
`web-front/J2EE`: M1 n = 12 → 9 full, 2 partial, 1 clean-fail,
conditions = "Java 8u-below + gadget lib present". M2: stager-A 5/5
established, 4/5 survives-60 s; stager-B (tunnel-compatible) 3/5
established → FIELD-READY = A only. M3 joint: 5 runs, min-link 0.9 ×
joint 5/5 → 0.9, floor link = X-007. M5(b): rank = 0.75 (reliability
9/12) × 1.0 (stager A) × 0.9 (joint) = 0.68, reported with factors.
Compat matrix: J2EE/8u-below cell = measured-positive (n = 12);
J2EE/current cell = EMPTY, no claim. All ids ledgered.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
HD Moore's art is real — Metasploit made exploitation composable,
Project Sonar made internet measurement open — but the published form
has floors: module reliability asserted in rank metadata rather than
measured, stagers tuned for one target class, composition proven by
demo, and the Sonar method's reproducibility left to goodwill. This
module extracts what is protocol-shaped and ships the replacement:
a module record with measured reliability, a stager differential, a
composition joint-gate, an exposure-measurement protocol, and rank
arithmetic. An agent without a framework must run this at his
precision.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Rank metadata asserted, not measured — Metasploit's `Rank: Excellent` grades the module author's confidence, and the framework shows no per-environment reliability runs | Reliability is a property of module × target-class × payload, never a static label; a "Great" module at 40% on the deployed target class is a trap with a badge |
| W2 | Stager/delivery tuned for one target class — the default reverse-TCP stager assumes egress and a POSIX-ish target; the art treats transport as a detail | Cross-class claims (different egress rules, different arch/OS) silently inherit the demo's conditions; the composition fails in the field where it was "proven" in the lab |
| W3 | Composition proven by demo — exploit + stager + payload shown working end-to-end ONCE | The joint failure modes (stager mis-sized for the exploit's memory context, payload blocking the process the exploit needs alive) are invisible to a single-shot demo |
| W4 | Sonar's method opaque to re-run — the scan parameters, rate, dedup, and ethics were described in talks, not shipped as a reproducible protocol | Internet-scale measurement without a written protocol cannot be audited for harm OR reproduced for science; goodwill is not a method |
| W5 | Payload compatibility as anecdote — "works on 2003, sometimes 2008" folklore in module notes | The compat matrix is data-shaped but shipped as prose; nothing recomputes it when the payload or target changes |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Reliability measured per module × target-class, in records | **M1** — the module record |
| U2 | Stagers differentially tested across classes | **M2** — the stager differential |
| U3 | Composition with a joint gate, not a demo | **M3** — the composition proof |
| U4 | Exposure measurement as a written, auditable protocol | **M4** — the measurement protocol |
| U5 | Compatibility as a versioned matrix | **M5** — the compat matrix |
| U6 | Rank as computed arithmetic | **M5(b)** — rank arithmetic |
