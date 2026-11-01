---
name: business-logic-hunter
version: 1.0.0
type: ai-skill
architecture: package
description: Phase-2/3 business-logic organ — workflow-sequence abuse (skip/replay/reorder), race conditions with the spine's stochastic reproduction floors, and limit/price/coupon arithmetic testing, all hypothesis-first with self-owned test accounts. Use when the operator asks to test business logic, abuse workflows, race two requests, probe negative quantities or price arithmetic, or hunt coupon/voucher reuse ("logika bisnis", "race condition", "negative quantity", "price manipulation", "coupon abuse", "workflow bypass", "integer overflow").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; operator-owned test accounts and self-owned orders
---

# business-logic-hunter v1.0.0 — The App's Rules, Tested As Rules

## 0. What This Skill Is — and Is Not

* **Is**: the organ for vulnerabilities that no scanner will ever find:
  sequence abuse, races, arithmetic that trusts the client. Its unit of
  work is a WORKFLOW, mapped end-to-end before any step is attacked.
* **Is not**: a fuzzer with a business vocabulary. Random parameter churn
  on business endpoints is R1 slop; the workflow map comes first.

## 1. Inherited Contracts

Plugs into **Phase 2** (workflow maps → hypotheses) and **Phase 3**
(experiments) of the mythos-bug-hunter spine. Inherits the experiment
contract with its stochastic floors (§6: races need 20+ attempts and a
stabilized success-rate estimate — hiding stochasticity is slop), closure
vocabulary, and canary doctrine (self-owned orders/accounts only; bounded
proofs: one abused transaction, then stop).

## 2. Procedure — Numbered Actions

1. Map each in-scope workflow end-to-end with operator test accounts:
   every step, every state transition, every server-side check observed —
   all FACT records. The workflow-map template is in
   `references/abuse-catalog.md`.
2. Pre-register hypotheses per abuse shape from the catalog: sequence
   skip, step replay, reorder, race, arithmetic inversion, coupon reuse.
   One mechanism per hypothesis (spine §5).
3. Run each as a differential: baseline (happy path, already recorded),
   treatment (the abuse), control (same effort, unrelated knob).
4. Races follow `references/races.md` exactly: the attempt floor, the
   stabilization windows, the honest rate report.
5. Arithmetic checks run on SELF-OWNED carts/orders with values the
   operator chose: negative quantities, zero-price items, overflow-shaped
   large numbers, currency/decimal confusion, discount stacking. CONFIRMED
   needs the differential delta (total changed vs baseline), not a
   suspicious-looking response.
6. Impact synthesis stays bounded: one abused self-owned transaction,
   amount differences stated, no fund movement beyond the operator's own
   test wallet.
7. Exit gate: workflows mapped, hypotheses closed by state, races with
   their attempt counts and rates, every closure citing records.

## 3. Hard Rules (mechanically enforced)

1. **Workflow map precedes hypotheses.** The first logic-shaped hypothesis
   cites workflow-map records.
2. **Races report rates.** A race finding without attempts/success-rate
   lines fails the audit (spine §13 rule 3).
3. **Self-owned money only.** Payment-flow abuse uses the operator's
   wallet and self-created orders; refunds/cancellations restore state.
4. **One transaction proofs.** "Could drain the wallet" is proven by one
   bounded abuse, then stop (spine §8.2).

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Workflow mapping, treatments, controls | `http_probe` (session headers) |
| Hypotheses/closures/rates | `ledger_append` (EXPERIMENT/CONTROL) |
| Parallel race driver | `arsenal_route` absent → the spine's python3 micro-script doctrine (calibrated, timeouts, ledger-formatted output) |
| Registering workflow surfaces | `dossier_add` (surface-cartographer) |

## 5. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Mapping a workflow / choosing abuse shapes | `references/abuse-catalog.md` |
| Any race hypothesis | `references/races.md` |
