# Evidence templates — hunt ledger conventions and the handoff pack

## 1. Ledger conventions for hunts

Same append-only format as every engagement; the tags carry hunt-specific
meanings:

| Tag | Used for | Example gist |
| --- | -------- | ------------ |
| FACT | trigger event, freeze actions, test outcomes, confirmations | `apply: T-001 outcome=1; eliminated H-005..H-008; active=4` |
| CONTROL | baseline records the signal/noise line is calibrated against | `baseline: 3 nights of 02:00-04:00 login cadence for svc-debug` |
| EXPERIMENT | pre-registered partitions, frozen before outcomes | `decide: pre-register T-001 (netflow, passive); on 1 kills ... / on 0 kills ...; 1.00 bits over 8 active` |
| REFUSED | tip-off tests gated while passive eliminators remain | `apply: T-004 refused; tip-off gated while passive tests eliminate (T-001)` |
| MISTAKE | a falsified hypothesis space (all hypotheses dead) | `hypothesis space falsified — all eliminated` |
| PARK | dead ends and budget stops, with a resume note | `parked: external-passive channel unreachable offline; resume when egress returns` |

Two records per executed test is the healthy heartbeat: one EXPERIMENT
(pre-registration) + one FACT (outcome). A hunt whose tests lack
pre-registrations was improvised — the auditor treats that as
unauditable, and so should you.

## 2. The handoff pack (auditor-compatible skeleton)

Written ONLY from `ledger_read` outputs. Every severity word on a line
cites its R-NNN on the same line; every hypothesis block closes;
CONFIRMED blocks carry impact-chain and canary posture; INCONCLUSIVE
blocks appear in the leads appendix. The auditor
(`auditor/audit_report.py`) must exit 0.

```markdown
# Adversary handoff — case <name>, engagement <program>

## Summary
<3-5 sentences: trigger, space size, tests spent vs floor, survivor,
channels, what is handed to whom. Every claim cites R-NNN.>

## Timeline (from records)
| When | Record | Event |
| ---- | ------ | ----- |
| <ts> | R-001 | trigger: <observation> |
| <ts> | R-002 | freeze complete: <sensors captured> |
| ... | ... | ... |

## Hypotheses

### H-004 <survivor label>
Severity: high (state precisely what the actor holds) — R-009
- Closure: CONFIRMED — R-008, R-009
- Channels: netflow (R-004, R-006) + host-audit (R-008)
- impact-chain: <entry point> → <credential/session> → <reach>
- canary: none during the trace (TIP-OFF discipline, R-005); the
  credential-reset tripwire is IR's containment action, scheduled and
  owned by IR — not executed during the hunt

### H-001 <falsified label>
- Closure: FALSIFIED — eliminated by T-001 outcome 1 (R-004)
<...one block per hypothesis; no hypothesis left unclosed...>

## Elimination table
| Hypothesis | Died on | Record |
| ---------- | ------- | ------ |
| H-005 ... | T-001 outcome 1 | R-004 |
| ... | ... | ... |

## Channel matrix
| Hypothesis survived | Channel | Test | Record |
| ------------------- | ------- | ---- | ------ |
| H-004 | netflow | T-001 | R-004 |
| H-004 | netflow | T-002 | R-006 |
| H-004 | host-audit | T-003 | R-008 |

## Uncertainty and leads
<What the hunt did NOT establish: identity, physical location, intent
beyond observed actions. Parked items with resume notes.>

## Handoff statement
Localization within the authorized perimeter is complete: <survivor>,
evidence R-NNN citations above. Identity, upstream infrastructure, and
any action beyond this perimeter belong to <client IR / law
enforcement> with this pack as the evidentiary basis.
```

## 3. Auditor compliance notes

* Severity or class words (`high`, `vulnerable`, …) on a line require
  an R-NNN on that same line — keep citations inline, not in a
  footnote.
* `Closure:` lines accept exactly CONFIRMED / FALSIFIED /
  INCONCLUSIVE; ELIMINATED hypotheses are FALSIFIED in the pack (the
  engine's word is for hunt state, the report's word is for the
  auditor's grammar).
* CONFIRMED + severity requires `impact-chain:` and the word `canary`
  in the block; a quiet hunt states its canary posture honestly
  (none during the trace, IR-owned after) rather than inventing one.
* INCONCLUSIVE hypotheses must also appear in a `## Leads` appendix.
* No hedging phrases (`appears to`, `might be`, …) — the discipline's
  whole point is that bits do not hedge.
