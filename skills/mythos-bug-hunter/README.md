# mythos-bug-hunter

**The discipline layer for AI security researchers.**
Not a zero-day generator — a guarantee that what your agent reports is real.

## Why this exists

Agents spray findings. A typical AI-assisted bug bounty session ends with 50
"discoveries", 48 of which are noise, and a human doing the filtering the
agent should have done. Triage desks reward the opposite: a handful of
reproducible, fully cited, honest reports.

No prompt can fix this by asking the model to "be careful." Slop is an
epistemology problem, so the fix is structural: **this package makes
unevidenced claims syntactically invalid.** A report line without a ledger
record ID is treated like an unclosed bracket — it does not compile.

The operating formula: `finding = coverage × variance × oracle ÷ loop time`.
The reference library engineers coverage, the warzone drills engineer
variance, the evidence gates engineer the oracle, and lazy-senior script
doctrine protects loop time.

## The Canon (eight rules)

| # | Rule |
|---|---|
| R0 | Authorization gate — no AUTH record, no requests. |
| R1 | Plan before action — discoveries go to a backlog, not the queue. |
| R2 | Finish or formally park — status codes are signals, not verdicts. |
| R3 | Victory language is gated by Closure + reproduction + impact chain. |
| R4 | Every claim cites a ledger record — or it does not exist. |
| R5 | Tools are evidence generators — scanner output is a hypothesis, never a finding. |
| R6 | Scripts are instruments — calibrate before you trust. |
| R7 | Effort budgets per vector and per engagement — exhaustion parks, never loops. |

## Package layout

```
mythos-bug-hunter/
├── SKILL.md                  # always-loaded core: Canon, no-slop law, 6-phase pipeline, contracts
├── README.md                 # this file
├── references/               # 17 load-on-demand modules (reasoning, playbooks, attack classes, recon toolchain, drills)
├── scripts/audit_report.py   # mechanical slop auditor for reports
└── example/
    ├── worked-example.md     # full engagement walkthrough (passes the auditor)
    └── sloppy-report-fixture.md  # deliberately bad report (fails the auditor)
```

## Quickstart

1. **Install**: drop this folder into your agent's skills directory (the one
   containing `SKILL.md` at its root), or point your agent at the repo.
2. **Authorize**: give the agent a scope — a bug-bounty program page, an
   engagement letter, or a self-owned lab. Phase 0 records it as `AUTH`.
3. **Engage**: the agent runs scoping → recon → pre-registered hypotheses →
   differential experiments → canary impact proof → self-audit.
4. **Ship only audited reports**:

```bash
python3 scripts/audit_report.py report.md        # exit 0 → ship
python3 scripts/audit_report.py example/sloppy-report-fixture.md   # watch it fail
```

## What this is — and is not

- **Is**: a chassis and steering. The model supplies intelligence; this
  package aims it, sequences it, and holds every claim accountable to
  recorded evidence.
- **Is not**: a zero-day generator. Frontier zero-day discovery (Big Sleep,
  AIxCC-class systems) takes teams, infrastructure, and compute. What this
  package borrows from them is the *method* — variant analysis, differential
  proof, calibrated suspicion — and the honesty discipline that makes triage
  respect your submissions.
- The worked example demonstrates the standard honestly: it **rediscovers a
  known CVE on an owned lab** (CVE-2025-29927). Rediscovery is the
  calibration proof; novel findings are the bonus, never the promise.

## Design credits

The reasoning architecture draws on published work we consider worth
stealing: Google Project Zero / DeepMind Big Sleep (variant analysis as the
highest-yield LLM-native technique), DARPA AIxCC results (accuracy beats
volume — proof quality is the differentiator), and the replication-crisis
playbook (pre-registration, append-only evidence) from the social sciences.

## Legal

Authorized targets only. This package is a research discipline, not a
license. Operators are solely responsible for the legality of their
engagements in their jurisdiction.

## License

MIT — see the LICENSE file in the repository root if present, otherwise treat
this README's section as the grant.
