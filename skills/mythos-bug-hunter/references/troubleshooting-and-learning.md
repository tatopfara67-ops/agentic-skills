# Reference — Troubleshooting And Learning

> Part of **mythos-bug-hunter v4.4.0** (package architecture).
> **Load when:** Any phase on failure (self-repair protocol) and engagement close (mistake-learning system: error journal, bias checklist, regret table, calibration audit).
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

## 13. Self-Repair Protocol

A technique that errors, stalls, or returns `INCONCLUSIVE` twice triggers
self-repair: classify the failure, apply exactly one discriminating fix,
retry once. The protocol exists because most "the bug isn't there" moments
are actually "the probe never arrived" moments.

### 13.1 Failure Taxonomy

| Class | Meaning | Signature | Cheapest discriminating test |
|---|---|---|---|
| F1 | environment / tooling | network dead, proxy or auth expiry, DNS | re-send a known-good baseline request from session start |
| F2 | target-side interference | WAF, bot wall, rate limit, tarpit | benign canary request; compare status/body fingerprint to the session baseline |
| F3 | payload defect | encoding mangling, syntax, context mismatch | echo canary: do my exact bytes appear anywhere in the response? |
| F4 | hypothesis error | the condition simply is not there | modus tollens with positive control passed (§9.3) — the silence is real |
| F5 | method error | wrong verb / param / version / host | re-derive from the inventory (§14): v1/v2 split, mobile-only route, gateway rewrite |

F1-F3 and F5 are *repairable*. F4 is *information* — the hypothesis was
wrong, which is a recorded outcome, not a process failure.

### 13.2 Triage Ladder (cheapest first)

```
test errors, stalls, or returns INCONCLUSIVE twice
  |
  v
[1] known-good baseline request still OK?
  |      no --> F1: fix environment, retry (free — infra is not a hypothesis)
  |      yes
  v
[2] benign canary fingerprint unchanged vs session baseline?
  |      differs --> F2: interference; slow down, reduce concurrency,
  |                  rotate identity, retry once
  |      unchanged
  v
[3] echo canary present in the response?
  |      no --> F3: re-encode the payload through the client's own
  |              encoder, retry once
  |      yes
  v
[4] surface re-derived from the inventory (verb/version/host)?
  |      mismatch --> F5: correct the target, retry once
  |      match
  v
[5] positive control passed + N clean trials
         --> F4: apply the silence LR (§10.6),
             park or kill per band (§10.4)
```

### 13.3 One-Change-Per-Retry

Each retry changes exactly one variable, and the change is logged:

```
retry 1: changed payload encoding (double -> single)        [F3]
retry 2: changed Identity -> baseline UA                     [F2]
```

Changing two things at once converts a repair into an uncontrolled
experiment: if it then works, nobody knows why, and the evidence chain (§7)
is polluted.

### 13.4 Retry Budget

- Two repair cycles per failing technique; after that the technique parks
  with its posterior recorded (§10.2) and the TODO re-queues at lower
  priority.
- F1 repairs are free (infrastructure is not a hypothesis).
- Escalating repairs for F2, in order: slow down (2x interval) → reduce
  concurrency to 1 → stop for the session. Never hammer through a defense
  (§33.4).

### 13.5 Repair Record

```json
{
  "ts": "2026-10-30T09:12:00Z",
  "technique": "reflected-xss-context-probe",
  "symptom": "3 consecutive INCONCLUSIVE on parameter q",
  "failure_class": "F3",
  "discriminating_test": "echo canary absent; client had double-encoded the payload",
  "change_applied": "single encoding via --data-urlencode",
  "result": "canary reflected; band 30-60% resumed",
  "cycles_used": 1
}
```

### 13.6 Positive-Control Ledger

Per technique, per session: one known-true trigger on record before any
silence is interpreted.

| Technique | Standard positive control |
|---|---|
| injection / reflection probes | a canary token reflected in the response (§26.9) |
| authorization differentials | an object the actor is allowed to read (the baseline, §26.1) |
| out-of-band callbacks | a callback triggered from an authorized context first |
| timing differentials | an authorized, deliberately slow request (known heavy filter) |
| header-based bypasses | documented behavior reproduced on a reference/lab target, else marked untested |

No ledger entry, no silence claim: "it did not work" is indistinguishable
from "it never arrived" until the control passes.

### 13.7 Escalate to the Operator When

1. authorization or scope ambiguity appears mid-repair (stop; §33.1);
2. a repair could have a destructive effect (do not attempt; propose);
3. three repair cycles fail on a P0 hypothesis — present the repair records
   and the options instead of burning budget silently;
4. the tooling environment itself has been broken for more than 15 minutes.

### 13.8 Wiring

Self-repair runs inside the validation loop: a failed or inconclusive
COMPARE step (§5.2, gate G4) routes here before any verdict change; the
repair record attaches to the candidate (§5.4); repeated F4 outcomes across
a class feed the induction log (§9.6) and the silence compounding (§10.6).

---

## 31. Mistake-Learning System

A mistake is an asset only if it produces a rule; otherwise it is just
damage. Self-awareness here is not introspection for its own sake — it is
treating your own reasoning as an observable system with failure modes,
logs, and fixes: the same discipline §13 applies to probes, turned inward.

### 31.1 The Error Journal

One JSONL line per mistake, written the moment the cost is noticed:

```json
{
  "ts": "2026-10-30T18:40:00Z",
  "phase": "exploit",
  "mistake": "crafted 14 XSS payloads before reading the CSP header",
  "root_cause": "process_gap",
  "bias": "anchoring",
  "cost_minutes": 40,
  "discriminator": "reading the CSP costs 2 seconds and gates every payload decision",
  "new_rule": "R-17: security response headers are read before any payload is written",
  "repeat_count": 1
}
```

`root_cause` enum: `knowledge_gap | process_gap | tooling_gap |
cognitive_bias | scope_confusion`. The `discriminator` field is mandatory:
name the 10-second check that would have caught this earlier — that check,
not the apology, is the value extracted. `new_rule` gets a stable number;
repeats increment `repeat_count`, and a third repeat escalates the rule into
the session-start checklist instead of staying in the journal.

### 31.2 Post-Mortem Triggers

Run a 10-minute post-mortem (time-capped, no exceptions) whenever:

- a report is rejected or downgraded (duplicate / NA / informative);
- any session exceeds 2 hours (decision quality decays measurably);
- any single detour costs 10+ minutes;
- a shipped candidate later proves to be a false positive.

Every post-mortem ends with at least one new numbered rule or a
`repeat_count` increment. Rules accumulate into a personal checklist that is
re-read at session start — a journal without the checklist is a diary, not
a system.

### 31.3 Cognitive Bias Checklist (hourly, 60 seconds)

| Bias | In-the-field symptom | Countermove |
|---|---|---|
| confirmation | only testing paths that would confirm H | name the killer test you have been avoiding; run it next |
| anchoring | the first bug type seen today owns the whole TODO queue | re-rank the queue from the inventory (§14), not from momentum |
| tunnel vision | fourth loop on the same parameter | force a surface rotation: next TODO from a different inventory category |
| sunk cost | "already 2 hours in, it must be here" | the kill rule is arithmetic (§10.7), not sentiment |
| availability | hunting the technique from the last writeup read | evidence on *this* target outranks any writeup |
| survivorship | quoting only success stories as base rates | priors come from audit data (§10.8), not from tales |

### 31.4 The Regret Table (pre-commitments)

| Regret heard after the fact | Pre-commit rule |
|---|---|
| "should have read the CSP/headers first" | response security headers are read before payload craft |
| "the bug lived on the v1 API I skipped" | deprecated and older versions get one sweep per engagement |
| "duplicate of a disclosed report; wasted hours" | known-issues grep (disclosed reports, issue trackers) before any deep dive |
| "the PoC was silently eaten by a WAF the whole time" | positive control (§13.6) before interpreting silence |
| "the writeup ended up weaker than the finding" | impact is quantified at discovery time (§19), not at writing time |
| "a scope doubt I never raised" | ambiguity means stop and ask (§33.1) — always cheaper than the alternative |

### 31.5 Calibration Audit (monthly)

Pull the prediction log (§10.8): every closed hypothesis with its final
`p_post` and outcome. Bucket by decile; compare hit-rate to the stated
probability; adjust the LR table (§10.3) in writing, with a dated note in
the journal. Miscalibration is a `tooling_gap`, not a character flaw — fix
the table, not the self-image.

### 31.6 Mid-Session Self-Awareness Probes

At every phase transition (§16), 60 seconds:

1. **Falsifiability check** — what evidence would make me abandon the
   current hypothesis? If nothing comes to mind, it is not a hypothesis;
   restate it (§11.2).
2. **Bet check** — would I bet 100 units of my own time at the stated P?
   If not, the number in state is wrong: fix it or act on the real one.
3. **Blind-spot check** — what am I not looking at right now, and why? The
   honest answer is usually "because it is boring" — boring is where the
   base rate lives.

### 31.7 Session Close (five minutes, mandatory)

1. Update the journal: one line per triggered post-mortem condition.
2. Park residual TODOs with their posteriors and the next discriminating
   test.
3. Delete the scratch dir per the doctrine (§27.4); keep evidence and the
   report.
4. Write one sentence: the single lesson of this session. If it is the same
   sentence as last session, the rules are not being applied — escalate the
   rule, not the regret.

---
