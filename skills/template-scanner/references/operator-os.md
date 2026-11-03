# operator-os.md — the ProjectDiscovery runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> template laws; the M-protocol (references/method-upgrade.md) states
> the matcher and RUN-PIN protocol; THIS module is the runtime — how
> the agent thinks, behaves, and scripts while executing them,
> characteristic of the ProjectDiscovery craft: detection as
> declarative templates, matchers pre-registered before the run, packs
> versioned as data, and noise filtered before it becomes a report.

## 1. The thinking framework — decision rules

R1 **Detection is a declarative template, never a script.** A
detection states: request shape, matcher, metadata — it does not
compute cleverness. If a check needs logic, the logic goes into the
template's structure, not into ad-hoc code. *From:* the nuclei design
line (subfinder, nuclei, naabu) — engines separate from detection
data.

R2 **The matcher is pre-registered.** What counts as a hit is written
BEFORE the run: status, word/regex set, DSL condition. A matcher
edited after seeing responses is a fabrication machine.

R3 **Templates compose into packs, packs are versioned data.** A
campaign cites its template set by version ("ran http/exposures
pack@v9.2.1, 412 templates") — replay requires the exact set.

R4 **A hit is a LEAD until its evidence row exists.** Every hit
carries: matched template, request/response fingerprints, and the
noise-filter verdict. Raw scanner output is hypothesis, not finding
(the spine's R5).

R5 **Severity is re-rated, never inherited.** The template ships a
default severity; the organ re-rates per the M-protocol's ladder
(context, exploitability, program scope) before any report line.

R6 **Noise is a first-class metric.** The run reports its noise ratio
(false-shaping hits filtered / total hits); a template whose noise
ratio exceeds the filter table's ceiling is retired or fixed, not
tolerated.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Campaign starts | Pin the pack set + versions | T1 lists the exact template inventory with version | Never run "whatever's installed" |
| A check needs logic | Make it declarative or split it | T2 shows the template structure with the DSL condition | Never ship a detection as free-form code |
| First hits appear | Filter noise BEFORE celebrating | T3 runs the filter table; noise verdict per hit | Never bulk-escalate raw hits |
| A hit survives filtering | Build the evidence row | T4 captures matched-template + fingerprints | Never let a bare hit reach a report |
| Template default says "critical" | Re-rate on the ladder | T5 re-rates with context rows | Never inherit severity silently |
| A template noisily fails on this target class | Retire or fix it, on record | Filter-table row updated; pack version bumped | Never tune the matcher to the observed responses (R2) |
| Re-run needed | Same RUN-PIN or a new pinned run | T1 re-pins; diff declared | Never mix template versions inside one run |

Pacing: batch runs with pinned sets; between runs, the only change is
a declared pack bump (R3). Failure reaction: a run with unexplained
noise spike is voided and re-pinned — the noise ratio is a health
metric, not a footnote.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — RUN-PIN: the exact template inventory

```bash
# the campaign's identity: engine version + pack versions + counts
<scanner-engine> -version
<scanner-engine> -tl 2>/dev/null | wc -l
python3 - <<'PY'
pin = {"engine": "<scanner> v3.x", "packs": {"http/exposures": "v9.2.1"},
       "template_count": 412, "run_id": "R-0417"}
print(f"RUN-PIN {pin['run_id']}: {pin['engine']} "
      f"packs={pin['packs']} templates={pin['template_count']}")
PY
```

Read-out: the pinned run identity. Gate: every hit cites its RUN-PIN
(R3) — orphan hits are refused.

### T2 — declarative template shape

```yaml
# detection as data: request, matcher, metadata — no scripts
id: backup-index-exposure
info:
  severity: low
  tags: exposure, backup
http:
  - method: GET
    path: ["{{BaseURL}}/backup/"]
    matchers:
      - type: dsl
        dsl: ["status_code == 200 && contains(body, 'Index of /backup')"]
        condition: and
```

Read-out: the check itself. Gate: matchers committed before the run
(R2); post-run matcher edits void the run.

### T3 — noise filter table

```bash
python3 - <<'PY'
filter = [
 # template-class, common false shape, action
 ["backup-index", "soft-404 page with 200", "require distinctive-body marker"],
 ["version-banner", "CDN-injected banner", "attribute to origin hop only"],
]
hits, filtered = 41, 12
print(f"hits={hits} noise_filtered={filtered} ratio={filtered/hits:.0%}")
print("ceiling 40%:", "OK" if filtered/hits <= 0.40 else "RETIRE/fix templates")
PY
```

Read-out: the run's noise ratio + verdicts. Gate: ratio above the
table's ceiling → templates retired or fixed before reporting (R6).

### T4 — hit evidence row

```bash
python3 - <<'PY'
row = {"run_pin": "R-0417", "template": "backup-index-exposure",
       "target": "https://<host>/backup/", "status": 200,
       "body_sha": "9f2a…", "noise_verdict": "survived-filter",
       "default_sev": "low"}
print(row)
PY
```

Read-out: the LEAD's complete evidence row. Gate: hits without this
row are not reportable (R4) — the row IS the promotion.

### T5 — severity re-rate ladder

```bash
python3 - <<'PY'
default, context = "low", {"exposed": "database dump file",
                           "auth": "none", "program": "public bounty"}
# ladder: default -> context-adjusted -> program-bounded
adjusted = "high" if "database dump" in context["exposed"] and context["auth"] == "none" else default
print(f"template_default={default} context_adjusted={adjusted} cited_rows={context}")
PY
```

Read-out: the re-rated severity with its context rows cited. Gate:
report lines cite the ladder, never the template default alone (R5).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | scope pinned | pin engine + packs + run id | T1 | RUN-PIN recorded | PLAN |
| S2 | pin exists | verify matcher pre-registration for custom templates | T2 | all matchers committed | PLAN |
| S3 | matchers locked | run the campaign | governed engine | hit stream + counts | EXPERIMENT |
| S4 | hits appear | filter noise; compute ratio | T3 | ratio ≤ ceiling | FACT |
| S5 | hits survive | build evidence rows | T4 | every lead has its row | FACT |
| S6 | evidence complete | re-rate severity on the ladder | T5 | context rows cited | REPORT |
| S7 | report ships | exit: run summary (pin, counts, noise, retirements) | — | run summary attached | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A matcher edited after responses were seen → R2 violation; the run
  is voided and re-pinned from scratch.
* A report line citing no RUN-PIN or no evidence row → unreplayable;
  refused (R3, R4).
* Severity inherited from the template default with no ladder row →
  R5 violation; re-rated before shipping.
* Noise ratio above ceiling found in the run summary → R6 violation;
  the campaign is not reportable until templates are fixed.
