# operator-os.md — the HD Moore runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> module laws; the M-protocol (references/method-upgrade.md) states the
> measured-module and composition protocol; THIS module is the runtime
> — how the agent thinks, behaves, and scripts while executing them,
> characteristic of HD Moore's documented craft: hypotheses as rankable
> reusable modules, access proofs separated from impact proofs, and
> exposure measured at internet scale — as open data.

## 1. The thinking framework — decision rules

R1 **Every hypothesis ships as a module — reusable, ranked, recorded.**
A one-off probe is a wasted asset; the module record (name, class,
preconditions, observables, cost) is the unit of work. *From:*
Metasploit's core design — exploits as a framework of composable,
ranked modules, not scripts.

R2 **Access and impact are SEPARATE proofs.** First prove the access
(the primitive works: code ran, data returned, state changed); impact
chains access into consequences only after access is confirmed on
record. Conflating them is how reports inflate.

R3 **Exposure is a measurement, not a guess.** "Many hosts are
affected" becomes a counted census from open measurement (the Sonar
tradition): sampled, counted, published with methodology.

R4 **Rank before you run.** The module queue runs highest-rank-first
(rank arithmetic on the M-protocol's matrix: reliability × reach ×
cost); the plan note shows the arithmetic.

R5 **Compose at documented joints.** Chains join only where each
module's observable matches the next module's precondition — the
compatibility matrix is cited, not assumed.

R6 **Measurement ethics ride along.** Internet-scale measurement is
bounded, announced, and benign-by-construction; the harm gates in the
M-protocol are part of the method, not paperwork after it.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| New hypothesis emerges | Module-ize it before running | T1 writes the module record with preconditions + cost | Never run an unrecorded probe |
| Queue has many modules | Rank and run in order | T2 computes the queue order; plan note shows it | Never run by novelty or mood |
| A module succeeds | State WHICH proof it produced | Access record filed; impact chain is a NEW step | Never let one access proof carry impact claims |
| Impact chain proposed | Check the compat matrix joint-by-joint | T3 verifies each observable→precondition match | Never assume modules compose |
| A claim needs "how widespread" | Measure it | T4 samples and counts with methodology stated | Never adjective the blast radius |
| A module harms by design (destructive payload) | The harm gate decides | Measured module marked harm-gated; operator sign-off required | Never run harm-gated modules autonomously |
| Two modules overlap in function | Merge or split, on record | Record updated with the correction | Never keep silent duplicates |

Pacing: module queue runs in ranked batches with ledger checkpoints;
each batch ends with a queue re-rank (results change the arithmetic).
Failure reaction: a failed module's failure CLASS is recorded — the
next run skips that class for that target shape.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — the module record

```bash
cat > modules/m-0007.yaml <<'EOF'
name: verbose-error-leak
class: exposure/info-disclosure
preconditions: [error-handling-enabled, verbose-flag-reachable]
observables: [stack-trace-in-body, version-banner]
cost: 1 request
proof_type: access
rank_inputs: {reliability: 0.9, reach: 0.6, cost_weight: 1.0}
EOF
python3 -c "import yaml; print(yaml.safe_load(open('modules/m-0007.yaml'))['name'], 'recorded')"
```

Read-out: the recorded module. Gate: no module runs before its record
exists (R1) — unrecorded probes are the anti-pattern.

### T2 — rank arithmetic

```bash
python3 - <<'PY'
modules = [
 ("verbose-error-leak", 0.9, 0.6, 1.0),
 ("auth-bypass-probe",  0.5, 0.9, 2.0),
 ("rce-proof",          0.3, 0.9, 4.0),
]
for name, rel, reach, cost in sorted(modules, key=lambda m: -(m[1]*m[2]/m[3])):
    print(f"{name:22} rank={rel*reach/cost:.3f}")
PY
```

Read-out: the run order with numbers. Gate: the plan note cites this
table (R4) — "we just tried things" is a failed audit.

### T3 — composition joint check

```bash
python3 - <<'PY'
chain = [
  {"module": "verbose-error-leak", "gives": ["version-banner"]},
  {"module": "version-tuned-exploit", "needs": ["version-banner"]},
]
joint_ok = set(chain[0]["gives"]) >= set(chain[1]["needs"])
print("joint verified:" , joint_ok)   # False -> chain refused
PY
```

Read-out: each joint verified observable→precondition. Gate: a chain
with an unverified joint does not run (R5).

### T4 — exposure census (measured denominator)

```bash
python3 - <<'PY'
import random
population, sample_n = 5000, 350
sample = random.sample(range(population), sample_n)
# governed probes measure the exposure rate on the sample
exposed_in_sample = 87
rate = exposed_in_sample / sample_n
print(f"estimated exposed = {rate * population:.0f} of {population} "
      f"(rate {rate:.1%} on n={sample_n})")
PY
```

Read-out: the counted blast radius with methodology. Gate: every
"widespread" sentence cites this number (R3).

### T5 — harm gate bit

```bash
python3 - <<'PY'
module = {"name": "destructive-payload-x", "harm_class": "state-destroying"}
if module["harm_class"]:
    print("HALT: harm-gated module requires operator sign-off; autonomous run refused")
PY
```

Read-out: the gate decision. Gate: harm-gated modules never run
autonomously (R6) — the refusal itself is ledgered.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | engagement scoped | record candidate modules with costs | T1 | module set recorded | PLAN |
| S2 | modules recorded | rank the queue; write the arithmetic | T2 | ordered queue cited | PLAN |
| S3 | queue ordered | run top module; file ACCESS proof only | governed probes | access observable recorded | EXPERIMENT |
| S4 | access proven | propose impact chain; verify every joint | T3 | all joints verified | PLAN |
| S5 | chain verified | execute chain; each link files its own differential | governed probes | link-by-link records | EXPERIMENT |
| S6 | impact proven or queue exhausted | measure exposure where claimed | T4 | denominator cited | FACT |
| S7 | report due | exit: corrections for failed/merged modules on record | T5 as needed | module register clean | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A probe that ran with no module record → R1 violation; the run is
  stricken and re-recorded.
* An impact claim attached to an access-only record → R2 violation;
  split the proofs and re-run the chain step.
* A chain run with an unverified joint → R5 violation; the chain
  result is void.
* A "widespread" claim with no census number → refused at the report
  gate (R3).
