# autonomy-protocol.md — self-selecting organs, with accountability

Load when you must choose organs for the current state, combine them,
or justify the selection. The charter's article A5 made autonomy a
contract: the agent picks its own tools, and the pick is auditable.

## 1. Why a protocol

An autonomous agent that cannot say WHY it chose an organ is a hazard
with a loop. The protocol below makes the selection a recorded, replayable
decision — the same state produces the same routing, every time.

## 2. State variables (assess before selecting)

| Variable | Read from | Why it matters |
| --- | --- | --- |
| Phase | spine's phase loop (0 scoping → 5 audit) | routing axis #1 |
| Authorization posture | `auth_status()` — rows, classes, expiries | in_scope / recon_only / denied changes which tools may run at all |
| Environment | `http_probe` facts, reachability notes | a static-only host never gets ssrf-playbook |
| Target architecture dynamics | dossier classes (API? roles? storage? AI surface?) | architecture decides which organs have standing |
| Effort budget | R7 defaults + tool cap bits | what fits before the next park note |
| Incident state | sensor/operator trigger present? | the Binary Brain preempts the phase loop |

## 3. Routing table (phase × architecture)

| State | Driving organ | Support (≤2) |
| --- | --- | --- |
| Phase 0, nothing authorized yet | — (spine only) | `scope_check` on candidate targets |
| Phase 1, no dossier | surface-cartographer | subdomain-hunter |
| Phase 1, dossier exists, JS surfaced | js-recon | api-surface-mapper |
| Phase 1, API classes in dossier | api-surface-mapper | content-discovery |
| Phase 2, ≥2 roles exist | auth-boundary-mapper | business-logic-hunter |
| Phase 2, OAuth flow present | oauth-flow-auditor | auth-boundary-mapper |
| Phase 3, interpreter behind input | injection-lab | xss-playbook (if reflections exist) |
| Phase 3, server-fetch capability | ssrf-playbook | cloud-config-auditor |
| Phase 3, storage/CORS/DNS edge | cloud-config-auditor | — |
| Any phase, incident trigger | adversary-tracker (preempts) | none — freeze first |
| Phase 5, findings to ship | skill-mythos gates | cvss3_score + vrt_classify + auditor |

Rules of combination:

1. **One driver, at most two supports** — a plan note naming five
   organs is a plan to browse, not to test.
2. **The driver owns the hypothesis grammar** for that stretch;
   supports propose, the driver's ledger records.
3. **Contradictory organs do not combine** (e.g. passive recon on a
   recon_only target + any active organ): the scope class decides,
   and the refusal is ledgered.

## 4. The loop

```
assess state
  → route (table above)
  → run one pre-registered step at the driver
  → ledger the outcome
  → re-assess: phase boundary? new surface class? incident trigger?
      yes → re-route (park the remainder with a resume note, R1)
      no  → continue
```

Re-assessment is mandatory at: phase boundaries, dossier growth
(new surface class), authorization changes (scope.csv edits),
tool cap bits, and incident triggers. Skipping re-assessment after
any of these is the autonomy failure mode the auditor cannot see —
the ledger can.

## 5. Incident interrupt (the Binary Brain preempts)

When a sensor or the operator reports adversary activity on assets
this engagement is authorized to DEFEND: pause the phase loop, freeze
before change, and hand control to adversary-tracker. The hunt ends
in an audited handoff pack; identity and the last mile belong to IR
or law enforcement. Then the phase loop resumes where it paused —
with a ledger full of the hunt's records.

## 6. Selection accountability

The plan note for every routing decision states: state snapshot
(phase, posture, architecture facts with R-NNN), organs selected
(driver + supports), why those and not the neighbors, and the exit
condition for the selection. If you cannot write the "why not the
neighbors" clause, you have not assessed — you have guessed.
