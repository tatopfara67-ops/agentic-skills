---
name: business-logic-hunter
version: 2.4.0
type: ai-skill
architecture: package
description: >-
  Phase-2/3 business-logic organ, upgraded (v2) with the Soroush Dalili
  lineage — workflow-sequence abuse (skip/replay/reorder), race conditions
  with the spine's stochastic reproduction floors, limit/price/coupon
  arithmetic testing, plus bypass craft: HTTP-reshaping grammar against
  business guards, parser differentials at guard/executor seams,
  intended-behavior inversion, and comparison functions as testableSince
  v2.2.0 the organ carries the executable method layer (A16) — a mechanical
  critique of the published Dalili-era form's floors (bypass grammars as
  curated lists without rule-class preconditions, single-bug narratives with
  generalization implicit, the defeated parser hop unnamed, one-shot demos
  without repeatability, bypass conflated with impact) shipped as protocol
  M1–M5: the rule-class bypass matrix with corpus-pinned first probes, the
  three-condition reshaping differential with a placebo control, chain-map
  linkage naming the enforcing hop, the repeatability floor with a stability
  window, and the route-opened impact ceiling. Use when the operator asks to
  test business logic, abuse workflows, race two requests, probe negative
  quantities or price arithmetic, hunt coupon/voucher reuse, or reshape around
  a blocked admin path ("logika bisnis", "race condition", "negative
  quantity", "price manipulation", "coupon abuse", "workflow bypass", "integer
  overflow", "bypass", "filter bypass", "parser differential").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: v2 — Soroush Dalili (irsdl, NCC Group; the HTTP-reshaping bypass grammar and parser-differential craft)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; operator-owned test accounts and self-owned orders
---

# business-logic-hunter v2.4.0 — The App's Rules, Tested As Rules

## 0. What This Skill Is — and Is Not

* **Is**: the organ for vulnerabilities that no scanner will ever find:
  sequence abuse, races, arithmetic that trusts the client. Its unit of
  work is a WORKFLOW, mapped end-to-end before any step is attacked.
* **Is not**: a fuzzer with a business vocabulary. Random parameter churn
  on business endpoints is R1 slop; the workflow map comes first. Since
  v2 it carries the **Soroush Dalili lineage** as its field-guide layer —
  bypass craft: when a guard blocks a treatment, the request gets
  reshaped and the seam gets proven before anything closes.

## 1. Inherited Contracts

Plugs into **Phase 2** (workflow maps → hypotheses) and **Phase 3**
(experiments) of the mythos-bug-hunter spine. Inherits the experiment
contract with its stochastic floors (§6: races need 20+ attempts and a
stabilized success-rate estimate — hiding stochasticity is slop), closure
vocabulary, and canary doctrine (self-owned orders/accounts only; bounded
proofs: one abused transaction, then stop).

## 2. The Lineage Layer (v2 — the Dalili doctrine)

**Soroush Dalili** (@irsdl, NCC Group line) — the public archetype of
bypasses as craft: reshaping HTTP requests via the standard and
web-server behavior until a filter and its executor disagree. v2 folds
the lineage in as five field rules, applied inside the procedure (§3)
and detailed in `references/bypass-craft.md`:

1. **Reshape once, canonically, before closing any blocked hypothesis.**
   Case, path params, segment padding, encoding, header/verb — one
   canonical differential per seam, exact bytes recorded.
2. **Seams are read at the executor's verdict,** not the guard's status
   code: did the step RUN?
3. **Invert every check.** Displaced or inverted, what does this check
   become? — one hypothesis per inversion, still self-owned.
4. **Comparison functions are testable units:** case folding, Unicode
   normalization, type juggling; both identifiers' bytes recorded, the
   runtime pinned as a FACT.
5. **Two variants per seam, then park.** The grammar is combinatorial;
   sweeping it is request-budget slop that buries the ledger.

## 2.5 First Principles — the WWH registers (A14)

* **WHAT** — business-rule violations: workflow abuse (steps
  skipped, reordered, repeated), economic manipulation (price,
  quantity, discount, currency), state-machine breaks (use-after-
  cancel, resurrection of consumed resources), and races — the same
  rule broken by timing instead of order.
* **WHY** — business rules live ONLY in application code: no
  framework, no sanitizer library, and no type system encodes "one
  discount per customer" or "a cancelled order cannot ship". The
  rules are also INVISIBLE to any single request — they exist
  across sequences — so per-request testing cannot see them, and
  multi-step flows hand the attacker the state transitions to
  reorder. That structural blindness is the root cause.
* **HOW** — model the intended workflow first (states, transitions,
  invariants), then attack the model: replay steps out of order,
  repeat completed steps, mutate mid-sequence values, race the
  time-window with rate floors honored — every deviation scored
  against the invariant it breaks, never against surprise alone.
  Surprise without a broken rule is a bug report, not a bounty.

War note (A15): the cheng sweep is the abuse catalog against the
inventoried flows; the ch'i is the invariant nobody wrote down
because "the UI doesn't allow that". W3 strikes exactly there —
the API's rules are the weakness the polished frontend guards; W5
reminds that a 50-cent logic bug is a primitive worth chaining.

## 2.6 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published reshaping craft where it was mechanically weak —
trick enumerations without the rule classes that select them, each
bypass a single concrete WAF story, "the WAF missed it" with the parser
chain unnamed, demos fired once, "bypassed" graded as if access
followed — and ships the executable replacement: **M1** the bypass
matrix (observed rule class → trick family → corpus-pinned first
probe; unknown rule class = REFUSED until the chain map names the
enforcer), **M2** the reshaping differential (baseline blocked /
treatment reshaped / control placebo-reshaping that should NOT pass;
control passing too = permissive-intermediary reclass), **M3** the
chain-map linkage (desync-hunter CHAINMAP discipline; every confirmed
bypass cites the defeated hop with version evidence; unattributed =
re-map first), **M4** the repeatability rule (n ≥ 5 more across ≥ 10
min; stable vs environment-conditional recorded with conditions),
**M5** the impact ceiling (route-opened is the deliverable; impact
cites the auth-boundary differential cell — bypass never grades as
access).

## 2.6 The Operator Layer (A17) — the Soroush Dalili runtime

`references/operator-os.md` ships the figure's documented psychology
as the agent's RUNTIME, in four parts: the thinking framework (numbered
if-then decision rules, each citing the documented behavior it
distills), the behavioral protocol (situation → move → agent action →
refusal, with pacing and failure-reaction rules — how the agent acts
and behaves while hunting), the scripting arsenal (the organ's core
techniques as exact, tool-agnostic commands and micro-scripts, each
with its read-out and decision gate), and the rigid run-order binding
rules, behavior, and scripts onto the M-protocol above. Load it when
the hunt runs: the doctrine states the posture, the M-protocol states
the procedure — the operator OS is how the agent BEHAVES while
executing, characteristic of Soroush Dalili. Since v2.4.0 it also
ships **The opening ladder** (A18): where Dalili's candidates come
from — the perception layer that PRODUCES the restriction census on an
unseen estate before any reshape or placebo is due (rungs write census
rows, never reshaped requests; ranking rationale stated; generation
falsifier on record; the reshape-lever kit names the bypass-craft
lever table, one lever per hypothesis).

## 3. Procedure — Numbered Actions

1. Map each in-scope workflow end-to-end with operator test accounts:
   every step, every state transition, every server-side check observed —
   all FACT records. The workflow-map template is in
   `references/abuse-catalog.md`.
2. Pre-register hypotheses per abuse shape from the catalog: sequence
   skip, step replay, reorder, race, arithmetic inversion, coupon reuse,
   and (v2) guard-seam reshapes from `references/bypass-craft.md`. One
   mechanism per hypothesis (spine §5).
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

## 4. Hard Rules (mechanically enforced)

1. **Workflow map precedes hypotheses.** The first logic-shaped hypothesis
   cites workflow-map records.
2. **Races report rates.** A race finding without attempts/success-rate
   lines fails the audit (spine §13 rule 3).
3. **Self-owned money only.** Payment-flow abuse uses the operator's
   wallet and self-created orders; refunds/cancellations restore state.
4. **One transaction proofs.** "Could drain the wallet" is proven by one
   bounded abuse, then stop (spine §8.2).
5. **Bypass closures cite the exact reshaped request** (v2) — "some
   encoding worked" is not a record.

## 5. Tool Routing

| When | Tool |
| --- | --- |
| Workflow mapping, treatments, controls | `http_probe` (session headers) |
| Hypotheses/closures/rates | `ledger_append` (EXPERIMENT/CONTROL) |
| Parallel race driver | `arsenal_route` absent → the spine's python3 micro-script doctrine (calibrated, timeouts, ledger-formatted output) |
| Registering workflow surfaces | `dossier_add` (surface-cartographer) |

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Mapping a workflow / choosing abuse shapes | `references/abuse-catalog.md` |
| Any race hypothesis | `references/races.md` |
| A guard blocked a treatment / seam or comparison questions | `references/bypass-craft.md` |
| Citing the lineage artifacts behind the v2 layer | `references/sources.md` |
| Grading the published form, running the reshaping differential, citing the defeated hop | `references/method-upgrade.md` |
| Running the hunt — the Soroush Dalili runtime: the opening ladder (A18), thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
