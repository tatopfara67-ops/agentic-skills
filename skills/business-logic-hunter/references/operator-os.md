# operator-os.md — the Dalili runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> logic laws; the M-protocol (references/method-upgrade.md) states the
> bypass matrix and reshaping protocol; THIS module is the runtime —
> how the agent thinks, behaves, and scripts while executing them,
> characteristic of Soroush Dalili's documented craft: the request is
> a shape, reshaping it walks the parser's blind spots, and the
> placebo control keeps the bypass honest.

## 1. The thinking framework — decision rules

R1 **A request is a SHAPE, not a string.** Path casing, encoding
layers, separator variants, header order, content-type alternatives —
the same logical request has a grammar of physical forms, and rule
engines match shapes while parsers accept more. *From:* the lineage's
HTTP-reshaping bypass grammar — a decade of published bypasses that
are all "same request, different shape".

R2 **Reshape ONE dimension per experiment.** Case OR encoding OR
separator — never two at once; the differential must attribute WHICH
reshape dimension crossed the rule.

R3 **The placebo control is mandatory.** A harmless variant (e.g.,
path case where no rule exists) proves the reshaping mechanism itself
is understood — before the reshaped bypass is claimed.

R4 **Bypass classes are a matrix, not a lucky list.** Rule-class ×
reshape-dimension: each cell is either tested, parked, or documented
inapplicable; "we found one bypass" closes nothing.

R5 **Chains link at the bypass, not after it.** A bypass's value is
the chain it unlocks (bypass → write → impact); the chain-map linkage
cites which cell opened the door.

R6 **Repeatability is the floor.** A bypass that fires once in five
attempts is a rate, not a capability — attempts + success_rate on
every claim.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| A rule/WAF/restriction identified | Enumerate the rule CLASS first | T1 writes the rule-class row (what it matches, where) | Never fire random encodings at an unclassified rule |
| Rule class known | Reshape ONE dimension, pre-registered | T2 builds the single-dimension variant; EXPERIMENT row | Never stack encodings "for power" |
| A variant gets through | Run the placebo first | T3 harmless-variant control proves the mechanism | Never claim bypass without the control row |
| Bypass confirmed | Chain-map the unlocked capability | T4 links cell → next organ's entry point | Never treat a bare bypass as impact |
| The rule answers 500 or oddly | Record the parser tell | The error shape is a seam datum for desync-hunter | Never discard weird responses as noise |
| Flaky bypass observed | Measure the rate | T5: attempts + success_rate on record | Never round a 40% bypass to "works" |
| Rate floor hit on a rule | Park remaining cells | Matrix rows parked with reasons | Never hammer one cell louder |

Pacing: one reshaped request per experiment, scanner-grade spacing;
the matrix grows across sessions, not in bursts. Failure reaction: a
cell that "sometimes" bypasses gets a rate row and stays a LEAD until
the rate stabilizes.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — rule-class enumeration

```bash
python3 - <<'PY'
rule = {"id": "WAF-12", "location": "edge",
        "matches": ["path contains /admin", "body regex cmd="],
        "action": "block", "observed_on": "GET+POST"}
print(rule)   # from observed block responses, not vendor docs alone
PY
```

Read-out: the classified rule. Gate: reshape experiments cite a rule
class (R1) — shots at unclassified rules are refused.

### T2 — single-dimension reshaper

```bash
python3 - <<'PY'
from urllib.parse import quote
base_path = "/admin/panel"
variants = {
  "case":        "/ADMIN/panel",
  "percent":     quote(base_path, safe="/%"),          # %61dmin form via manual map
  "double-pct":  "%%32%66admin" ,
  "semicolon":   "/;/admin/panel",
  "dot-seg":     "/./admin/panel",
  "null-byte":   "/%00admin/panel",
}
for d, v in variants.items(): print(f"{d:12} {v}")
PY
```

Read-out: one variant per dimension (sent one per EXPERIMENT).
Gate: exactly one dimension differs from the canonical request (R2).

### T3 — placebo control

```bash
# harmless variant: same reshape dimension, NO rule in the area
for v in "/PUBLIC/about" "/public/about"; do
  curl -s -o /dev/null -w "placebo $v -> %{http_code}\n" "https://<host>$v"
done
```

Read-out: the mechanism baseline (server accepts case variants where
no rule exists). Gate: bypass claims carry this control row (R3).

### T4 — chain-map linkage row

```bash
python3 - <<'PY'
link = {"bypass_cell": "WAF-12 × case-dimension",
        "unlocks": "POST /admin/upload reachable",
        "next_organ": "chain-architect composes upload → RCE chain",
        "record": "R-311"}
print(link)
PY
```

Read-out: the bypass→chain linkage. Gate: impact language requires
this row (R5) — bare bypasses ship as bypasses.

### T5 — repeatability measurement

```bash
python3 - <<'PY'
attempts, successes = 10, 4
rate = successes / attempts
print(f"attempts={attempts} successes={successes} rate={rate:.0%}")
print("verdict:", "CAPABILITY" if rate >= 0.8 else "RATE-LEAD (stays a lead)")
PY
```

Read-out: the rate row. Gate: sub-threshold rates never upgrade past
LEAD (R6); attempts + success_rate are mandatory fields.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | restriction identified | classify the rule | T1 | rule-class row | FACT |
| S2 | rule classed | run the placebo control | T3 | mechanism baseline recorded | CONTROL |
| S3 | placebo clean | reshape one dimension per experiment | T2 | per-cell verdicts | EXPERIMENT |
| S4 | a cell bypasses | verify repeatability | T5 | rate ≥ 0.8 or LEAD | EXPERIMENT |
| S5 | capability confirmed | link the chain-map row; hand off composition | T4 | linkage cited | PLAN |
| S6 | matrix filling | exit: cells tested/parked/inapplicable | — | park notes per open cell | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A bypass claim with no placebo control row → R3 violation; re-run
  with the harmless variant first.
* Two reshape dimensions in one payload → R2 violation; attribution
  broken, split and re-run.
* A rule fired at with no class row → R1 violation; classify first.
* Impact language on a bare bypass → R5 violation; the chain linkage
  is mandatory before that sentence ships.
