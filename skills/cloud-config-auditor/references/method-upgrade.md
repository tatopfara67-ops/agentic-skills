# The method upgrade — critiquing the Prowler tradition, shipping the executable posture audit

The charter's A16 charge: **a lineage named is not expertise delivered.**
Toni de la Fuente's art is real — Prowler's checks-as-code,
benchmark mapping, and open posture tradition industrialized cloud
auditing — but the published practice has floors: checks run as
received, the CIS/benchmark mapping trusted and never re-derived,
severity as vendor label, re-runs compared to nothing, and one
snapshot sold as "posture". This module extracts what is
protocol-shaped and ships the replacement: a check review gate, a
benchmark spot-rederivation, a severity re-rate ladder, a delta
protocol between runs, and a posture-trend ceiling. An agent that
has never run Prowler must audit posture at its discipline.

## 1. The critique — five mechanical weaknesses of the published practice

| # | What the practice shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------------- | --------------------------------- |
| W1 | Checks run as received — the default is `prowler aws` against an account; the check logic is trusted like a compiler | Checks are heuristics with environments they misread (multi-account quirks, custom naming, nonstandard regions); un-audited checks produce findings that are the TOOL's opinion, not the account's state |
| W2 | Benchmark mapping trusted — the CIS column in each check's output cited as authority, never re-derived against the benchmark text | Mapping drift is silent and two-way: checks that cite a control they don't fully test (false coverage) and controls nobody checks (false completeness) — the audit's own coverage is unaudited |
| W3 | Severity as vendor label — fail/severity grades ride the output verbatim | Severity is target-relative (an open security group on a bastion VPC ≠ one on an isolated dev VPC); the label's universality misprices everything in particular |
| W4 | Re-runs compared to nothing — each execution emits a full report; nothing diffs against the last | Posture is a TIME SERIES; single-run reporting makes regressions invisible and fix-verification manual — the exact gap a delta protocol closes |
| W5 | Snapshot sold as posture — one run, one account, one region-set quoted as "the posture" | Without the window, scope, and delta discipline, "posture" is a screenshot with confidence it did not earn |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Check logic audited before its findings ride | **M1** — the check review gate |
| U2 | Benchmark mapping spot-re-derived | **M2** — the rederivation protocol |
| U3 | Severity re-rated per target context | **M3** — the re-rate ladder |
| U4 | Every run diffed against its predecessor | **M4** — the delta protocol |
| U5 | Posture as bounded time series | **M5** — the trend ceiling |

## 3. The executable protocol — M1 through M5

### M1 — the check review gate

1. Per run, the check set is sampled for audit (house rule: 100% of
   checks whose findings will ride the report + 10% random of the
   rest): each sampled check's LOGIC read — what API calls, what
   comparison, what environment assumptions.
2. A check whose logic cannot state its own falsifier (what
   environment makes it cry wolf) is quarantined: its findings park
   as tool-opinion until re-derived (W1).
3. Quarantine counts are reported — visible check-audit coverage,
   not silent trust.

### M2 — the benchmark rederivation protocol

1. Per run, ≥ 5 random check→control mappings are re-derived
   against the actual benchmark text (source-cited): does the
   check's logic test what the control demands?
2. Divergence classes: partial-coverage (check tests half the
   control — its FAIL is meaningful, its PASS is not), over-claim
   (check cites a control it does not test), uncovered (control
   with no check — the completeness gap).
3. Every rederivation is a CONTROL record; systematic divergence
   (≥ 2 of 5 wrong) triggers a full-mapping audit before ANY
   coverage claim (W2).

### M3 — the severity re-rate ladder

| Tool grade | Default re-rate | Escalates with | Demotes with |
| ---------- | --------------- | -------------- | ------------ |
| critical fail | P2-class hypothesis | internet-exposed resource (route/SG evidence) + no compensating control | isolated VPC + compensating control cited |
| high fail | P3-class hypothesis | blast-radius evidence (privilege path) | dev account, no data class |
| manual/notice | hygiene row | — | merged duplicates |

Both columns ride the output table (tool-grade AND re-rated);
label-only reports are refused at this organ's gate (W3).

### M4 — the delta protocol

```
DELTA: run-N vs run-(N-1) <same scope-set, same check-set-hash>
  new-fails=<list> resolved=<list> persistent=<count>
  regressions: any resolved-fail reappearing = REGRESSION row
  (finding class of its own — the fix that did not hold)
```

Rules: deltas are only computed within the same check-set hash
(check-set changed = re-baseline, not compare); the regression row
is the delta protocol's headline deliverable (W4).

### M5 — the posture-trend ceiling

```
POSTURE-CEILING: window=<first..last run> scope=<accounts/regions
  actually covered> checks-hash=<set identity> trend=<persistent
  count by class, regression count, resolution rate> claim-cap:
  "posture" statements bounded to THIS window+scope; outside
  scope = explicitly listed as unmeasured
```

The unmeasured list (accounts, regions, services not covered) is
mandatory — posture claims never leak past the measured set (W5).

## 4. Falsifiers — what would prove this method wrong

* A quarantined check's finding later proves real → the quarantine
  was right anyway (tool-opinion is not evidence); the check gets
  its falsifier written, re-derives, and the finding re-enters
  through evidence — luck is not a method.
* Rederivation shows 0 divergence across many runs → the mapping is
  good: the protocol's cost drops to the sampling floor it earned
  (5 checks), and the record says so.
* Delta shows zero regressions but production incident says
  otherwise → the incident's resource was outside the scope-set:
  the M5 unmeasured list catches the boundary; scope grows with
  the incident as data.
* Two consecutive runs disagree on a persistent check with the same
  hash → non-deterministic check logic (API pagination, eventual
  consistency): quarantine the check for flapping; its history is
  the evidence.

## 5. Worked micro-example (numbers consistent, incident fictional)

Run 14 vs run 13 (same scope: 2 accounts, 4 regions; check-set
@sha256:a1b2). M1: 9 report-riding checks audited + 6 random; 1
quarantined (root-MFA check assumes org alias — its FAIL on the
custom-alias account is tool-opinion; parked). M2: 5 mappings
re-derived — 1 partial-coverage (encryption-at-rest control cited
by a check that tests volume encryption only → its PASS
downgraded to partial). M3: open-SG critical → re-rated P3
(isolated dev VPC, compensating NACL cited, both columns shown).
M4: new-fails 3, resolved 5, regression 1 (S3-public-block re-
failed — REGRESSION row, headline). M5 ceiling: window 30 days,
scope-set listed, unmeasured = 1 account (no credentials), claim
capped: "persistent 12 by class, 1 regression, resolution rate
5/8" — no posture adjective beyond it.
