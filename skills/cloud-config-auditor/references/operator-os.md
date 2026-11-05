# operator-os.md — the de la Fuente runtime: notice, think, behave, script

> A17's layer. Load when the audit RUNS. Doctrine (SKILL.md) states the
> posture laws; the M-protocol (references/method-upgrade.md) states
> the check-review and delta protocol; THIS module is the runtime —
> how the agent notices, thinks, behaves, and scripts while executing them,
> characteristic of Toni de la Fuente's documented craft: posture is
> checks-as-code, benchmarks are re-derived not trusted, and the
> finding is the DELTA with its severity argued on a ladder.

## 1. The thinking framework — decision rules

R1 **A posture claim is a check record, or it is nothing.** Every
assertion ("this bucket is public", "this CORS policy reflects any
origin") is a versioned check: id, input, logic, expected, observed.
*From:* the Prowler line — checks-as-code is the lineage's whole
thesis.

R2 **Benchmarks are re-derived, never quoted.** A CIS/PCI control is
re-implemented from its stated intent against the live config; the
benchmark citation rides beside the derived check, not instead of it.

R3 **The delta is the finding.** Two config states (policy vs
practice, declared vs effective) compared mechanically — drift IS the
report. "Looks misconfigured" is not a row.

R4 **Severity walks the ladder.** Default severity → context-adjusted
(exposure, auth, blast radius) → program-bounded; each step's row is
cited. Inherited severity is a placeholder, never a verdict.

R5 **Anonymous access is bounded to proof.** Public-bucket and
anonymous-endpoint checks demonstrate existence + one marker object,
never enumeration of the tenant's data.

R6 **Regression rows keep the fix honest.** Post-fix re-runs produce
delta rows; a fix that changes no effective state is a stopgap, named
as one.

### The opening ladder — where drift is born

Prowler's checks are the codified openings; the ladder is where the
lineage's craft points BEFORE the check run. Drift has a birthplace,
and it is almost always the console — the change someone made at
human speed, outside the code path that reviews catch. Every rung
reads config sources already collected; no rung changes state.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | Which resources were born outside the template? | console-created versus IaC-tracked — drift's birthplace, where the unreviewed change lives | checks-as-code inverted — what ISN'T code is the question |
| G2 | Which policies got wider over time? | statement and version diffs — permission accretion, the grant that never shrank | the delta doctrine (R3) applied to history, not just state |
| G3 | Which services skipped the org controls? | org-policy versus member-exception gaps — the "temporary" exception that aged into architecture | benchmark re-derivation (R2) at the org layer |
| G4 | Which exposures are new primitives? | the service nobody benchmarked yet — newest service, thinnest guardrails, checks still being written | the lineage's own growth record — checks lag services |
| G5 | Which credentials outlived their owners? | unused keys, orphaned service accounts — hygiene debt that compounds with every offboarding | the hygiene check class the toolchain is famous for |

Ranking rationale: blast radius × exposure × age of exception. The
wide-exposure exception that aged three years outranks the fresh
narrow one; the new primitive with no checks outranks both when it
is internet-reachable. Drift ages like debt — the ranking follows
the interest.

Generation falsifier: an account where no drift class yields means
the CONFIG SOURCES are incomplete — a read-level gap (a region not
enumerated, a service not inventoried), not the account's posture.
The census re-runs before any "clean" claim is written.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Cloud account/posture in scope | Enumerate the check set BEFORE scanning | T1 lists checks with their benchmark mapping | Never run "all checks" uncurated |
| A benchmark control cited | Re-derive its logic | T2 shows intent → derived check side by side | Never paste benchmark text as the finding |
| Config collected | Diff declared vs effective | T3 computes the drift table | Never eyeball JSON policies |
| A public bucket found | Marker-proof, don't tour | T4 lists one marker object (if any) | Never enumerate tenant objects |
| Severity assignment due | Walk the ladder with rows | T5 records the three steps | Never ship default severity |
| Fix claimed | Re-run for regression rows | T3 again | Never accept "fixed" without the delta |
| Check fails on this environment | Fix or retire the check, on record | Check-review gate row | Never tolerate a noisy check silently |

Pacing: checks run in batches by service class; each batch ends with
delta + noise counts before the next starts. Failure reaction: a
check that errors on this environment is REVIEWED (fixed or retired
with a row) — erroring checks are never skipped silently.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — check-set enumeration with mapping

```bash
python3 - <<'PY'
checks = [
 # id, service, class, benchmark mapping
 ["s3-public-read",      "s3",    "exposure", "CIS S3.5 / PCI 1.2"],
 ["cors-reflect-origin", "api",   "config",   "derived (no CIS row)"],
 ["iam-unused-key",      "iam",   "hygiene",  "CIS IAM 1.12"],
]
for c in checks: print(f"{c[0]:22} {c[1]:5} {c[2]:9} {c[3]}")
PY
```

Read-out: the curated run set. Gate: every run cites its check list
by id (R1) — "we scanned everything" is unauditable.

### T2 — benchmark re-derivation row

```bash
python3 - <<'PY'
control = {"benchmark": "CIS S3.5",
           "intent": "S3 buckets should not allow public READ",
           "derived_check": "get_bucket_acl -> grantee URI == AllUsers AND permission in (READ, READ_ACP)",
           "divergence": "none (intent maps 1:1)"}
print(control["derived_check"])
PY
```

Read-out: intent vs derived logic side by side. Gate: findings cite
the DERIVED logic; benchmark text is context, not evidence (R2).

### T3 — the drift delta table

```bash
python3 - <<'PY'
declared  = {"cors": "origin=https://app.example", "bucket_acl": "private"}
effective = {"cors": "origin=*",                   "bucket_acl": "public-read"}
for k in declared:
    if declared[k] != effective[k]:
        print(f"DRIFT {k}: declared={declared[k]!r} effective={effective[k]!r}")
PY
```

Read-out: mechanical drift rows. Gate: the finding IS the delta row
(R3); prose without a row is refused.

### T4 — bounded anonymous-access marker proof

```bash
# existence + ONE marker object; never enumeration
curl -s -o /dev/null -w "root %{http_code}\n" "https://<bucket>.s3.amazonaws.com/"
curl -s "https://<bucket>.s3.amazonaws.com/?list-type=2&max-keys=1" | head -c 200
```

Read-out: public status + one-entry listing shape. Gate: the marker
row is the impact ceiling (R5); deeper listing routes to the
engagement's scope decision.

### T5 — severity ladder row

```bash
python3 - <<'PY'
default, context, bounded = "medium", {"exposed": "config JSON with internal hosts", "auth": "none"}, "P3"
adjusted = "high" if "internal hosts" in str(context) and context["auth"] == "none" else default
print(f"ladder: {default} -> {adjusted} -> {bounded} (rows cited)")
PY
```

Read-out: the three-step severity record. Gate: report lines cite the
ladder (R4); default-only severity is a placeholder violation.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | posture scope set | enumerate + curate the check set | T1 | check ids cited | PLAN |
| S2 | check set locked | re-derive benchmark logic per check | T2 | derivation rows | FACT |
| S3 | derivations ready | collect configs; compute drift deltas | T3 | delta table | FACT |
| S4 | drift found | bounded proofs (marker rules) where exposure class | T4 | ceiling respected | CANARY |
| S5 | deltas classified | severity ladder per finding | T5 | three-step rows cited | REPORT |
| S6 | fixes land | regression delta re-run | T3 | stopgaps named | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A posture claim with no check record → R1 violation; void until
  recorded.
* A finding quoting benchmark text as its logic → R2 violation; the
  derivation row replaces it.
* A "misconfigured" sentence with no delta row → R3 violation;
  rewritten from the table or deleted.
* Anonymous access proven by enumerating objects → R5 violation; the
  marker rule was breached and the incident is ledgered.
