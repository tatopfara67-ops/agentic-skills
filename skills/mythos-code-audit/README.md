# mythos-code-audit v1.0.0

**The white-box engine of the Mythos stack.** Companion skill to
mythos-bug-hunter v4.1.0 (the black-box discipline layer): this one aims an
agent at *source code* and holds every claim to the same standard.

> Core law: **static analysis proposes; the runtime disposes.**
> No finding ships without a differential oracle.

## Why this exists (the market gap)

Market code-audit skills are sink-listers: grep for `eval`, run a scanner,
emit a table. None of that survives a triage desk, because none of it is
*proven*. This package ships the three things they do not:

1. **Oracle discipline** — every finding is a two-arm differential
   experiment (vulnerable vs fixed), with regression controls, reproduction
   floors, and a verdict taxonomy that separates instrument failure from
   security controls.
2. **Patch archaeology** — fixed bugs are mined for surviving variants.
   The flagship move is *enumeration-gap analysis*: a guard implemented as
   a list is a map of its author's blind spots, and the diff tells you
   exactly which family members were missing.
3. **A crypto misuse catalog** — 16 usage classes (primitives are never the
   target), each with a runtime oracle design.

And unlike every market skill: **it ships with a calibration proof**.

## The calibration proof

`example/worked-example.md` documents a full engagement against a real
target in a fresh sandbox — python-jose 3.3.0 vs 3.4.0, both arms pinned,
era-matched dependencies:

- **Rediscovered** CVE-2024-33663 (OpenSSH-key → HMAC-secret confusion) and
  CVE-2024-33664 (JWE decompression bomb) from the version diff alone, with
  runtime differentials on both arms.
- **Predicted** two further variants (`ssh-ed25519`, `ssh-dss`) from the
  enumeration gap in the old 4-string blacklist — pre-registered before the
  cells ran — then confirmed at runtime.
- Mapped the mitigation boundary (single-family allowlists stop the attack
  even on 3.3.0; mixed-family ones do not) and kept regression controls
  green throughout.
- Recorded five honest mistakes (including a CVE-ID memory swap caught by
  web verification, and an instrument-vs-control conflation caught by the
  verdict taxonomy).

Re-run the calibration yourself:

```bash
python3 -m venv v330 && v330/bin/pip install "python-jose[cryptography]==3.3.0" "cryptography==42.0.8"
python3 -m venv v340 && v340/bin/pip install "python-jose[cryptography]==3.4.0" "cryptography==42.0.8"
# specialize scripts/two_arm_harness.py with the cells from example/worked-example.md
v330/bin/python two_arm_harness.py --runs 3 | tee transcript_330.txt
v340/bin/python two_arm_harness.py --runs 3 | tee transcript_340.txt
python3 scripts/audit_code_report.py example/worked-example.md            # exit 0
python3 scripts/audit_code_report.py example/sloppy-code-report-fixture.md # exit 1
```

## Contents

```
mythos-code-audit/
├── SKILL.md                          # always-loaded core: canon, pipeline, contracts
├── README.md                         # this file
├── references/
│   ├── patch-archaeology.md          # variant mining, enumeration-gap analysis
│   ├── trust-map-and-sinks.md        # terrain mapping, operators, priors
│   ├── crypto-misuse-catalog.md      # 16 usage classes with oracles
│   └── differential-oracles.md       # arm design, cell taxonomy, floors
├── scripts/
│   ├── audit_code_report.py          # mechanical report auditor (dual control)
│   └── two_arm_harness.py            # harness template
└── example/
    ├── worked-example.md             # the calibration engagement
    ├── sloppy-code-report-fixture.md # negative control
    ├── transcript_330.txt            # raw evidence, vulnerable arm
    ├── transcript_340.txt            # raw evidence, fixed arm
    ├── env_330.txt / env_340.txt     # provenance (pip freeze per arm)
    └── patch-diff-{native,jwe,utils}.txt  # the mined diffs
```

## Fixture key (negative control)

`example/sloppy-code-report-fixture.md` plants 31 violations the auditor
must catch — kept out of the fixture file itself so the count stays clean:

- 10 forbidden phrases: JACKPOT (9), might be ×2 (11, 24), probably (13),
  looks vulnerable (18), I believe (25), seems vulnerable (26), Should be
  tested further (34), seems exploitable + TODO (42, two on one line).
- 8 uncited severity claims (9, 11, 12, 18, 20, 24, 26, 42) — line 12's
  cite R-101 sits on line 13, so the claim line itself is uncited.
- 3 crypto-domain claims without CLASS-NN (12, 18, 24).
- 1 uncited diff-derived claim (19).
- 5 structural violations: H-001 CONFIRMED without code anchor, n_runs and
  arm evidence (3), H-002 INCONCLUSIVE without Park ID (1), H-003 without
  Closure (1).
- 4 file-level omissions: no canary, no impact chain, no mitigation
  boundary, no regression control.

## Install

Copy the package into your agent's skills directory next to
mythos-bug-hunter:

```
skills/mythos-code-audit/SKILL.md
skills/mythos-code-audit/references/...
skills/mythos-code-audit/scripts/...
skills/mythos-code-audit/example/...
```

Both skills share the ledger format, the Canon, and the Closure vocabulary —
run them as one loop: black-box recon feeds white-box hypotheses; patch
diffs feed HTTP-level experiments.

## Honest limits

- Not a zero-day generator. It is a guarantee layer: what survives the
  pipeline is reproducible, anchored, and cited.
- The calibration target was chosen because its version pair ships two
  CVEs — target-selection bias is disclosed in the worked example's mistake
  ledger. The method executes end to end; it does not promise two CVEs per
  audit.
- Static-only audits (code you cannot run) are allowed but every finding is
  capped at hypothesis strength (SKILL.md Phase 0).
