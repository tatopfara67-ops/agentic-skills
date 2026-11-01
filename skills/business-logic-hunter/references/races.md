# Race Condition Methodology

## The spine's floor, operationalized

* **Attempt floor: 20.** No race hypothesis closes with fewer than 20
  treatment attempts. Deterministic-style single-shot "races" are not
  races — reclassify.
* **Stabilization:** continue in 10-attempt windows until two consecutive
  windows agree within 10 percentage points. THEN report the rate:
  "14/40 attempts (35%)" — the honest number, because characterizing the
  variance IS the reproduction (spine §6).
* **Budget interplay:** if the window stability never arrives inside the
  vector budget, close INCONCLUSIVE with a Park record carrying the last
  two windows' rates. Unbounded loops are a budget decision, not rigor.

## The minimal race driver (python3 micro-script doctrine)

One file, one job: fire N identical requests as simultaneously as the
client can, record per-request status+body-hash+timing, emit ledger-ready
lines. Requirements (R6): calibrated against a control endpoint with
known behavior FIRST, timeouts on every socket, strict quoting, output
that drops into `ledger_append` without hand-editing.

## Windows vs single-shot verdicts

| Observation | Meaning |
| --- | --- |
| 1 success in 1 attempt | an anecdote — keep going |
| success in every window, rate stable ≥ threshold | the server lacks the guard; CONFIRMED candidate |
| successes vanish after warm-up | cache/lock warm state — record, re-hypothesize mechanism |
| rate collapses when requests are serialized | guard exists but is timing-sensitive — INCONCLUSIVE + Park, note serialization dependency |

## What earns "race" at triage

Two state-mutating requests whose COMBINED effect violates an invariant
each individually respects: double-redeem a self-owned coupon, overspend
a self-owned wallet's limit once, double-issue a self-owned voucher.
One request's odd behavior is another organ's problem (injection-lab,
auth-boundary-mapper).

## Reporting

Attempts, window rates, the stabilized estimate, the differential delta
on the self-owned object, and the canary attestation. A race report
without its rate table is exactly the slop the spine's auditor rejects.
