# HUNT.md — the Christmas Lab run, captured from a live session

Everything on this page came out of a real run of
`lab/christmas_lab.py` (synthetic, self-owned — the lab file is the
authorizing artifact, exactly like `lab/target_app.py`). Reproduce it:

```bash
rm -rf /tmp/christmas-lab
MYTHOS_ARSENAL_ROOT=/tmp/christmas-lab python3 lab/christmas_lab.py
python3 auditor/audit_report.py /tmp/christmas-lab/engagements/christmas-lab/HANDOFF.md
```

## The scenario

03:14 local. The lab's auth log shows six failed logins and one
success against the debug console, from `10.10.4.23` — an address
inside the lab net but unassigned in the inventory. The sensor fired;
the Binary Brain opens the hunt. Eight hypotheses (null
auto-inserted), four tests on three channels, one of them a tip-off
tripwire that the engine is about to refuse.

## The run

```
THE CHRISTMAS LAB — a Shimomura Binary Brain run (synthetic, self-owned)
trigger: 03:14 auth log: 6 failed + 1 successful debug-console login
         from 10.10.4.23 (in-lab, unassigned in inventory)

── declare ───────────────────────────────────────────────────
hunt opened (R-001) — 8 hypotheses (null auto-inserted), 4 tests, floor 3
warning: none

── decide #1 ─────────────────────────────────────────────────
registers: SIGNAL=1 SPLIT=1.00 TRUTH=0ch TIP-OFF=armed
chosen: T-001 (netflow, passive) — 1.00 bits
  on 1 kills: H-005 H-006 H-007 H-008
  on 0 kills: H-001 H-002 H-003 H-004
pre-registered: R-002 (partitions frozen before the outcome)

── the impatient move — apply the tripwire first ─────────────
REFUSED (R-003): tip-off test T-004 refused while passive tests still
eliminate: run T-001, T-002, T-003 first — the adversary must not
learn what you know
the adversary must not learn what we know — Rule P holds

── apply T-001 outcome=1 (netflow history exists) ────────────
eliminated: H-005 H-006 H-007 H-008 → active=4 (R-004)

── decide #2 ─────────────────────────────────────────────────
registers: SIGNAL=1 SPLIT=1.00 TRUTH=1ch TIP-OFF=armed
chosen: T-002 (netflow) — 1.00 bits over 4 active

── apply T-002 outcome=1 (lease from the cluster bridge) ─────
eliminated: H-001 H-002 → active=2 (R-006)

── decide #3 ─────────────────────────────────────────────────
registers: SIGNAL=1 SPLIT=1.00 TRUTH=1ch TIP-OFF=armed
chosen: T-003 (host-audit — a SECOND channel) — 1.00 bits

── apply T-003 outcome=1 (veth MAC prefix observed) ──────────
eliminated: H-003 → active=1 (R-008)
CONFIRMED: H-004 — compromised container in the build cluster (R-009)
channels: host-audit, netflow (two independent channels — Rule T satisfied)
efficiency: 3 tests used, floor 3 — log2(8) = 3 exactly

── close ─────────────────────────────────────────────────────
mode: closed — hunt closed — write the handoff pack from ledger records
```

## What to notice

* **The gate bit first.** The very first thing the run does after the
  first decision is try the impatient move — resetting the credential
  the actor used. The engine refuses it (R-003) because three passive
  eliminators are still on the table. The hunt stays quiet; the
  tripwire becomes IR's containment action at handoff.
* **Every split is 1.00 bit.** The brain halves 8 → 4 → 2 → 1 and
  closes at exactly the information-theoretic floor: 3 tests,
  log2(8) = 3. Two records per test in the ledger (EXPERIMENT
  pre-registration + FACT outcome) prove the partitions were frozen
  before the world answered.
* **The null hypothesis dies like any other.** "Authorized or benign
  activity" is H-001, killed by T-002's outcome (R-006) — the boring
  explanation had to be eliminated with evidence, not waved away.
* **Confirmation needed two channels.** Netflow alone (T-001, T-002)
  left the singleton unconfirmed; the host-audit test (T-003) crossed
  it, and only then did the engine mint R-009 with CONFIRMED.
* **The hunt ends in a handoff.** `HANDOFF.md` (this directory) is
  written from the nine ledger records, passes
  `auditor/audit_report.py` with exit 0, and states what was NOT
  established — identity, intent, the container's original compromise
  — as leads for IR, not as claims.

## Files in this directory

| File | What it is |
| ---- | ---------- |
| `HANDOFF.md` | the audited evidence pack (PASS) written from the records |
| `hunt.json` | final engine state: eliminations, channels, register history |
| `ledger/records.md` | the nine R-NNN records — the immutable history |
