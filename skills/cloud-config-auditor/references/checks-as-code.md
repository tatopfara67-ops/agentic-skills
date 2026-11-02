# checks-as-code.md — the de la Fuente lineage layer for cloud-config-auditor (v2)

Load when preparing the check battery for an engagement, when a verdict
needs a benchmark citation, or when the report asks how fresh a config
fact is.

## 1. Checks Are Code; Verdicts Are Diffs

The Prowler tradition (Toni de la Fuente): a misconfig check is a
VERSIONED RULE with a severity, a rationale, and a remediation text —
not a scanner's private opinion. This organ already runs every check as
a differential with ledger records; the v2 layer pins the metadata:

* every check family row in the report carries its CHECK ID (organ-
  local, stable, e.g. `CCA-CORS-01`, `CCA-STOR-02`), the check's own
  version, and the benchmark paragraph it maps to;
* the rule text lives in this reference — if the rule changed, the
  version bumps and the ledger notes say so;
* a verdict is reproducible from its three records (baseline /
  treatment / control) by anyone, with no scanner trust required. That
  is the whole point of the append-only ledger.

## 2. Benchmark Mapping (CIS as the spine of severity words)

CIS Benchmarks (cisecurity.org) give the check families their public
severity vocabulary. The organ's local families map cleanly:

| Local family | CIS-shaped concerns | Our differential |
| --- | --- | --- |
| CORS (CCA-CORS-*) | permissive origin/access policy | three-origin matrix |
| Object storage (CCA-STOR-*) | anonymous access, public listing | anonymous vs garbage-token probes, one-page bound |
| DNS dangling (CCA-DNS-*) | orphaned records, takeover exposure | CNAME chain + provider marker pair |
| Hygiene headers (CCA-HYG-*) | missing transport/session protections | presence facts, severity only with a reachable sink |

Severity words in the report cite the mapped paragraph, never a mood.
Where CIS and the target's own hardening guide disagree, BOTH are
recorded and the operator picks the row — the disagreement is a fact.

## 3. Drift Discipline (verdicts have timestamps)

A config verdict is current AS OF its record timestamp. Between record
time and report time, configs drift:

* every load-bearing verdict re-verified inside the engagement window
  before the report ships (the re-run cites the earlier record and the
  fresh one);
* hygiene facts older than the window are re-run, not re-used;
* a verdict that flipped between runs is a report-worthy observation on
  its own (operational volatility — the client's SOC will want it).

## 4. Posture Families Across Providers

Multi-cloud check families share SHAPES: public exposure, anonymous
access, permissive web policy, missing encryption-in-transit. The craft
order: name the SHAPE first (family row), then the provider's instance
of it. Provider-specific fingerprints (bucket error bodies, header
quirks) live in the family's reference file, date-pinned like the
takeover table — providers harden, tables retire.

## 5. The Open-Posture Tradition

The lineage is openly open-source: transparent checks over magic scores.
In this organ's terms: no aggregated "grade" is ever reported — the
matrix tables with record citations ARE the deliverable; the auditor's
job is reading evidence, not trusting a badge. An aggregated score that
cannot be unpacked back into its records is exactly the hallucination-
shaped output this repo exists to prevent.

## 6. The Craft, Stated As Five Field Rules

1. Every check: stable ID + version + benchmark paragraph, in the rule
   text — not in the operator's memory.
2. Severity words cite the mapped paragraph.
3. Verdicts carry timestamps; load-bearing ones re-verify in-window.
4. Name the posture shape, then the provider instance.
5. Matrix tables over magic scores — unpackable or it doesn't ship.
