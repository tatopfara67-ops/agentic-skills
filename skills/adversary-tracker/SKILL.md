---
name: adversary-tracker
version: 1.1.0
type: ai-skill
architecture: package
description: Event-triggered defensive organ — the Shimomura Binary Brain for tracing an adversary who touches assets you are authorized to defend. Four binary registers (SIGNAL / SPLIT / TRUTH / TIP-OFF) drive a halving loop freeze and capture first, classify against a calibrated baseline, enumerate hypotheses with the null auto-inserted, eliminate by halves with passive tests gated ahead of tip-off ones, and confirm the survivor only through two independent channels — then hand off, never retaliate. Since v1.1.0 the organ carries the executable method layer (A16): a mechanical critique of the 1994–95 hunt's floors (detection-by-luck, unsynced triangulation, ad-hoc fingerprinting, no deception layer, unstated localization floor) and their fixes as protocol M0–M5 — tripwire canaries, NTP-disciplined arrival deltas with a sync-error table, a four-feature stack-fingerprint predicate calibrated against known hosts, deception under the tip-off gate, and a stated localization floor. Use when the operator reports being probed or scanned, asks to investigate a suspicious login or intrusion, or wants an attacker traced ("ada yang scanning kita", "investigasi login aneh", "kenapa ada traffic ganjil", "trace the attacker", "incident triage").
category: security/defensive-ir
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# adversary-tracker v1.1.0 — The Binary Brain

## 0. What This Skill Is — and Is Not

* **Is**: the event-triggered organ for the question the offensive organs
  never ask: "someone is touching OUR side — who, from where, through
  what?" It runs the Shimomura Binary Brain (SBB): a tracker whose whole
  mind is four bits, distilled from the 1994–95 hunt that ended in
  Raleigh (the case and its sources: references/history-1995.md).
* **Is not**: retaliation, counter-intrusion, or attribution beyond the
  authorized perimeter. The hunt ends in a handoff pack; the last mile
  belongs to the client's IR team or law enforcement. In 1995 the FBI
  knocked on the door — the physicist handed them the location.

## 1. Inherited Contracts

Plugs into the spine's **incident branch** — event-triggered from any
phase, never scheduled. Inherits R0 (defense-side scope: only assets
you are authorized to defend — the same scope.csv, read as a defense
perimeter), the append-only ledger, the hypothesis grammar, and R7
budgets. Does not restate them. A confirmed hunt re-enters the spine's
normal hypothesis→report flow at Phase 4.

## 2. The Binary Brain — Four Registers

| Register | 1 means | 0 means |
| --- | --- | --- |
| SIGNAL | observation deviates from the calibrated baseline | baseline noise — freeze, do not hunt |
| SPLIT | the next test halves the active space | the test wastes bits — refused |
| TRUTH | two independent channels agree on the survivor | one channel is one story; localization forbidden |
| TIP-OFF | the action would reveal what we know | quiet to proceed |

The loop: FREEZE → BASELINE → CLASSIFY (SIGNAL) → ENUMERATE (null
first, always) → HALVE (passive before tip-off) → FIX (two channels)
→ HANDOFF. Formal spec, legal-state table, and the halving math live
in the `references/binary-brain.md` module.

## 3. The Hunt — P0…P6 (short form)

0. **FREEZE** — capture before change: full packet capture on, memory
   preserved (no power-off), clocks synced, snapshot hashes recorded.
   The 1994 discipline: the compromised machines were observed, not
   scrubbed.
1. **BASELINE** — "normal" from your own logs (CONTROL records); the
   signal/noise line is calibrated, never guessed.
2. **CLASSIFY** — each observation becomes a FACT record; signal vs
   noise is a recorded verdict, not a vibe.
3. **ENUMERATE** — hypotheses across identity / location / capability /
   intent / path; the engine inserts the null (authorized or benign
   activity) — the boring explanation is always in the space.
4. **HALVE** — `sbb_decide` ranks tests by expected bits and
   pre-registers the winner before any outcome exists.
5. **FIX** — the survivor is CONFIRMED only through two independent
   channels; the engine refuses otherwise.
6. **HANDOFF** — evidence pack written from ledger records, audited,
   delivered. The hunt ends there.

Full playbook, channel catalog, test menu, tip-off taxonomy:
the `references/hunt-playbook.md` module.

## 3.5 The Method Layer — Critique, Upgrade, M0–M5 (A16)

A lineage named is not expertise delivered. The 1994–95 hunt
succeeded on instrumentation luck, telephone-era triangulation, and
an expert's eyeball fingerprinting — documented floors, not
mythology. `references/method-upgrade.md` grades each floor (W1–W6),
states the should-have-been, and ships the replacement as executable
protocol:

* **M0 tripwire layer** — canaries + audit watches + ring capture +
  the clock gate (offset > 10 ms demotes timing evidence to coarse).
* **M1 freeze-plus** — the volatile state (socket→process, flow ages,
  login history) a 1994 disk-and-packet freeze could not hold.
* **M2 stack fingerprint discipline** — four features (initTTL, IP-ID
  arithmetic, window class, TSval Hz + uptime), one clustering
  predicate, calibrated against KNOWN hosts first: the fingerprint
  lives in the table, not the man.
* **M3 localization at the network floor** — passive handshake RTT
  (≤ (RTT/2) × 200 km/ms, consistency check unless path is known)
  + multi-sensor arrival deltas with the mechanical sync-error table
  (1 ms sync = ±200 km per pair). Rule T applies: timing alone is one
  story told with precision.
* **M4 deception under the tip-off gate** — tarpits and per-placement
  canary tokens that spend THEIR budget; engine-gated behind every
  passive eliminator.
* **M5 handoff with the floor stated** — metro/ASN granularity,
  person-level attribution explicitly the consumer's lane.

Every M-step names its ledger record type and its falsifier; the
worked micro-example at the module's end shows the whole chain in
numbers. Run P0–P6 for the loop; run M0–M5 for the mechanics.

## 4. Procedure — Numbered Actions

1. Entry: AUTH record + the trigger event as a FACT record with
   timestamps and sensor origin.
2. Run the freeze checklist (playbook P0) BEFORE the first sbb call —
   the brain reasons over evidence, not over a scene you altered.
3. `sbb_declare(program, case, trigger, hypotheses, tests)` — labels
   only; the engine numbers them and inserts the null. Declare tests
   on at least two channels or CONFIRMED is unreachable.
4. Loop: `sbb_decide` → run the chosen test passively →
   `sbb_apply(program, test_id, outcome)`. Two records per test:
   EXPERIMENT (pre-registration) + FACT (outcome). Attempted tip-off
   tests while passive eliminators remain are REFUSED and ledgered.
5. On `space-empty`: the space was wrong, not the logic — a MISTAKE
   record already exists; re-enumerate with what the eliminations
   taught (extend via sbb_declare).
6. On CONFIRMED: write the handoff pack from ledger records
   (references/evidence-templates.md), then
   `python3 auditor/audit_report.py <handoff.md>` — exit 0 or it does
   not ship.

## 5. Hard Rules (mechanically enforced by arsenal/sbb.py)

1. **Null first.** The engine inserts the authorized/benign hypothesis;
   a hunt without it is structurally impossible.
2. **Halving or nothing.** A test that cannot eliminate any active
   hypothesis is refused while the space is plural (Rule H).
3. **Two channels or it did not happen.** CONFIRMED requires two
   independent channels that the survivor actually crossed (Rule T).
4. **Tip-off gate.** A test that would reveal our knowledge is refused
   while any passive test still eliminates (Rule P — observe, never
   warn).
5. **The ledger decides.** Every bit is a record; a handoff claim
   without R-NNN citations is not a claim.
6. **Handoff, not vendetta.** Tracking stops at the perimeter's edge;
   identity and physical location go to IR or law enforcement with the
   pack.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Open or extend a hunt | `sbb_declare` |
| Next max-gain test, pre-registered | `sbb_decide` |
| Apply one observed outcome | `sbb_apply` |
| Passive evidence on assets you defend | `dns_resolve`, `http_probe` (scope-gated as always) |
| Freeze and baseline facts | `ledger_append` (FACT / CONTROL) |
| Fold the append log at phase boundaries | `ledger_merge` |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Formalizing registers, states, halving math | `references/binary-brain.md` |
| Running P0–P6, designing tests and channels | `references/hunt-playbook.md` |
| Grading the 1994–95 method, running M0–M5 mechanics (tripwire, fingerprint, localization, deception) | `references/method-upgrade.md` |
| Writing the audited handoff pack | `references/evidence-templates.md` |
| Grounding the discipline in the 1994–95 case | `references/history-1995.md` |
