# differential-oracles.md — Two-Arm Harnesses and Cell Discipline

> Load when: designing or running the differential harness; verdict
> taxonomy; reproduction floors. SKILL.md wins on conflict.

## 1. What an Oracle Is

An oracle is the **minimal runtime experiment whose outcome changes iff the
hypothesis is true.** Not a demo, not a log excerpt, not a PoC video — an
experiment with two arms and a falsifier. If you cannot say what result
would *falsify* the claim, you do not have a hypothesis yet; go back to
Phase 3.

## 2. Arm Design

| Arm pattern | When | Example |
|-------------|------|---------|
| **Version pair** | a fix exists; audit mines the diff | python-jose 3.3.0 vs 3.4.0 (the calibration setup) |
| **Patch-revert** | no released pair; monkeypatch the fix out | import fixed lib, monkeypatch `is_ssh_key` to the old blacklist |
| **Config arm** | the bug is config-shaped | allowlist `['HS256','ES256']` vs `['ES256']` |
| **Feature-flag / code-path arm** | vulnerable path behind a branch | same binary, flag on/off |
| **Era arm** | suspected environment rot | same code, old vs new dependency (proves the ERROR was environmental) |

Rules:

- Both arms run **identical** cells — same inputs, same assertions, same
  script (the harness takes the arm as an argument, never a forked script).
- Pin and record both arms (`PROVENANCE`); era-match shared dependencies
  (the `RAND_bytes` lesson: cryptography 50.x + python-jose 3.3.0 made JWE
  cells ERROR — an instrument failure, not behavior).
- Arms must pass their own smoke test before any cell counts (import + one
  golden round-trip).

## 3. Cell Taxonomy

- **Treatment cell** — the attack input. One per hypothesis claim.
- **Regression control cell** — the legitimate input that must keep working
  on both arms. A treatment result without a green control is void: the
  "fix" might just be breakage. (Calibration: E3 legit RS256, E6B legit
  100KB JWE — green on both arms while the bombs were blocked.)
- **Boundary probe** — which configurations stop the attack and which do
  not. Produces the **mitigation boundary table**, the most valuable
  section of a defender-facing report. (Calibration: single-family allowlist
  stops the confusion even on 3.3.0; mixed-family does not; no-allowlist
  does not.)
- **Variant probe** — the sibling input predicted by the sweep (real key,
  real format). 
- **Marker probe** — a synthetic member of a format family used when
  generating a real key is expensive/impossible. Weaker evidence: proves
  the guard gap, not full exploit realism. Marker-only results cap the
  hypothesis at INCONCLUSIVE + Park. (Calibration: `ssh-dss` marker string,
  E7D.)

## 4. Verdict Taxonomy (per cell, per run)

| Verdict | Meaning | Produced by |
|---------|---------|-------------|
| `VERIFIED` | the behavior occurred (attack accepted, bomb materialized) | the cell's success return |
| `REJECTED` | a security control fired | an exception raised *by the library under test* |
| `ERROR` | the instrument failed | import errors, attribute errors, environment rot |

Why the split matters: in the first calibration run, JWE cells raised
`module 'lib' has no attribute 'RAND_bytes'`. Labeled REJECTED, that is a
false negative ("the cap works!") born from a broken instrument. Classify by
exception type and message — `AttributeError`/`ImportError`/`module … no
attribute` → ERROR, re-pin the environment, re-run. **ERROR cells void
their hypothesis's evidence until resolved.**

## 5. Reproduction Floors

- Deterministic behavior (most crypto/parsing/guard cells): **3 identical
  runs per arm**. Identical = same verdict + same **digit-normalized**
  detail: `re.sub(r"\d+", "N", detail)`. Millisecond jitter is not
  instability; treating it as such burns budget (calibration mistake-ledger
  entry: the 1MiB bomb cell flagged "UNSTABLE" because decrypt took 2ms vs
  3ms).
- Stochastic behavior (races, hash-order, GC): 20 runs, stability criterion
  = two consecutive 10-run windows within 10pp on the measured rate.
- Budget out before stability → INCONCLUSIVE + Park with the resume point
  "rerun with N=… criterion …".

## 6. Harness Skeleton

`scripts/two_arm_harness.py` (template) implements the required mechanics:

- cells registered by decorator; **one cell's crash must not kill the
  matrix** (wrap every cell);
- per-run ledger line: `R-LAB | CELL | run i/N | VERDICT | detail | ms`;
- per-cell `SUMMARY | CELL | N/N verdict | STABLE/UNSTABLE` with
  digit-normalized detail;
- `--runs N`, arm identity printed in the header (versions of the package
  *and* its dependencies — `pip freeze` on both arms next to the
  transcript);
- canary value constant at the top; canary rides inside every forged input
  so every VERIFIED line is also a canary round-trip.

Cell design checklist (each treatment cell): names its hypothesis (H-NNN),
runs on both arms, has a sibling regression control, states its falsifier
in the docstring, and never touches anything outside the lab environment.

## 7. From Cells to Closure

| Cell evidence | Closure |
|---------------|---------|
| treatment VERIFIED on vulnerable arm, REJECTED on fixed arm, control green on both, 3× stable | **CONFIRMED** |
| control green, treatment REJECTED on both arms | **FALSIFIED** (the guard holds — including the good-news case: a mitigation that works) |
| marker-only VERIFIED, or budget out, or ERROR unresolved | **INCONCLUSIVE + Park P-NNN** |

A CONFIRMED finding's report block therefore always contains: anchor,
invariant, per-arm verdicts with n_runs, control result, mitigation
boundary, canary. Anything less is a note, not a finding (Report Contract
§13).

## 8. Impact Without Harm (oracle edition)

The oracle runs in your own process or your own localhost lab: pip-installed
copies, self-generated keys, canary claims. No third-party system receives
anything. The "victim" in every cell is a config you wrote. That is what
makes the evidence admissible everywhere: you can hand the harness and both
pinned arms to anyone and they will reproduce your table row-for-row.

## 9. Common Harness Bugs (audit your instrument, R6)

1. Verdict conflation (REJECTED vs ERROR) — fixed by classifier.
2. Jitter-as-instability — fixed by digit normalization.
3. Arm drift — cells edited per-arm after the first run; fix: one script,
   arms as arguments, transcripts regenerated in full after any edit.
4. Silent partial runs — a cell crash kills later cells; fix: per-cell
   isolation, and the `# END cells=N all_stable=…` trailer line must be
   checked before transcripts are cited.
5. Missing control — treatment without regression control; the closure
   table refuses it, so should the auditor.
