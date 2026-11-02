# The method upgrade — critiquing the SecLists tradition, shipping the executable discovery economy

The charter's A16 charge: **a lineage named is not expertise delivered.**
Daniel Miessler's art is real — SecLists is the field's corpus-family
discipline, and the composition law (lists combine) is his — but the
published practice has floors: which list answers which question is
taste, dictionary spraying runs uncalibrated to the target's naming
grammar, yield is never accounted per list class, and freshness
rides on repo pulls nobody stamps. This module extracts what is
protocol-shaped and ships the replacement: a question→list-class
binding table, target grammar calibration, a per-list yield ledger
with a marginal gate, as-of stamps, and an interesting-class
decision table. An agent with a stale local SecLists checkout must
run this at its economy.

## 1. The critique — five mechanical weaknesses of the published practice

| # | What the practice shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------------- | --------------------------------- |
| W1 | List choice as taste — the README organizes by category; WHICH list for WHICH question stays folk knowledge | Two hunters "check for backups" with different lists and different coverage, and neither knows their gap; the artifact is versioned, the METHOD is not |
| W2 | Spraying uncalibrated dictionaries — `dirsearch -w common.txt` against a target whose naming grammar (kebab? camel? digits? locale?) was never read | Most of every list is dead weight for a given target; the grammar is harvestable from the target's own 200-class pages, and the practice never harvests |
| W3 | Yield unaccounted — no run reports hit-rate or marginal yield per list class | Budget discipline is impossible without selectivity numbers: the practice burns flat budgets on flat yield and calls it thoroughness |
| W4 | Freshness unstamped — the lists are living repo artifacts; local checkouts drift for months | A wordlist's hit-rate claim made in March is about March's list; September's re-run compares nothing (the pipeline-smith as-of floor, dictionary edition) |
| W5 | "Interesting" by eyes — a found path is triaged by an operator's glance | The interesting-class (extension × status × size × context) is a decision table the practice never writes; drama files (admin.php 200, 0 bytes) waste follow-up budget |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Questions bound to list CLASSES, on record | **M1** — the binding table |
| U2 | The target's naming grammar harvested and used | **M2** — grammar calibration |
| U3 | Yield + marginal gate per list | **M3** — the yield ledger |
| U4 | As-of stamp per list per run | **M4** — the freshness rule |
| U5 | Interesting-class as a decision table | **M5** — the triage table |

## 3. The executable protocol — M1 through M5

### M1 — the binding table (questions before lists)

```
BINDING: question="exposed panels" -> list-class=<tech-specific-
  panels packs, versioned> question="backup artifacts" -> class=
  <extension-derivatives of KNOWN paths (M2), not generic backup
  lists> question="dev/staging" -> class=<environment-word packs +
  target-grammar variants>
```

A run cites its QUESTIONS and their bound classes; "ran common.txt
because it's common" is the refused habit (W1).

### M2 — grammar calibration (harvest before spraying)

1. From the target's KNOWN 200-class paths (crawl records, sitemap,
   operator-provided): extract the naming grammar — delimiter class
   (kebab/snake/none), digit usage, abbreviation style, locale
   tells, extension set.
2. Emit the derivative list for path-tied questions (backup class:
   `<known-path>.bak|~|old` + extension swaps) — derivatives of
   KNOWN paths outperform generic lists by construction.
3. The grammar row is a FACT: `grammar: kebab, digits-no, ext=php,
   locale=en` — every later list choice cites it (W2).

### M3 — the yield ledger (marginal economics per list)

```
YIELD: list=<name@hash> question=<bound> requests=<n> hits=<h>
  hit-rate=<h/n> marginal=<hits-not-already-found / n>
```

**Gate**: a list whose MARGINAL yield is 0 across its run is
recorded exhausted-for-this-target; stacking more lists of the same
class after a flat marginal is refused budget (the scan-economist
marginal-yield habit, dictionary edition — W3).

### M4 — the freshness rule

```
AS-OF: list=<name@hash> pulled=<date> drift-risk=<days> rule:
  yield claims cite the stamp; a > 90-day pull is re-fetched before
  its hit-rate supports any coverage claim
```

Comparative claims ("this found nothing in March") are void across
stamps — re-run or re-stamp (W4).

### M5 — the triage table (interesting as arithmetic)

| Extension class | Status | Size bucket | Route |
| --------------- | ------ | ----------- | ----- |
| code/config/db | 200/403 | any | candidate; 403-200 pair = access-map row |
| doc/txt/log | 200 | non-trivial | read-gate: operator decides export class |
| drama (admin/login/phpinfo) | 200 | 0-bytes/redirect | discount row — verify depth before routing |
| any | 3xx | — | follow only if in-scope + target-host (offsite redirect routes to ssrf-playbook) |

Every found path exits through a table row; glance-triage is
refused at the ledger (W5).

## 4. Falsifiers — what would prove this method wrong

* A generic list outperforms the calibrated derivatives → the
  grammar harvest mis-read the target (mixed conventions per
  section): split the grammar per path-tree, re-derive.
* Marginal gate fires but the NEXT list class finds a path → the
  classes were not disjoint (overlapping packs): the ledger's
  hit-attribution is the defect; re-attribute and recompute
  marginals.
* A > 90-day pull outperforms a fresh one → the fresh fetch changed
  the list's composition (curation churn): record the churn; both
  stamps stand as separate evidence.
* The triage table's discount row proves deep (drama file is real)
  → the size-bucket rule was too coarse for this target: add the
  exception class with the evidence; the table grows by
  falsification, not by operator hope.

## 5. Worked micro-example (numbers consistent, incident fictional)

Question set: panels, backups, staging. M2 grammar: kebab, ext=php,
digits-no. Derivatives: `/api/report` → `report.bak, report.php~,
report.old` (8 variants × 14 known paths = 112 candidates). M3:
derivatives 112 req → 3 hits (marginal 2.7%); panels pack
(tech-pinned @hash, as-of 11 days) 900 req → 1 hit (marginal 0.1%
→ class exhausted on record); staging env-words 240 req → 2 hits
(0.8%). M5: `report.bak` 200, size 4k, doc-class → operator
read-gate → contains internal API paths (finding, P4, evidence
bytes attached). Drama `admin.php` 200/0-bytes → discount row,
verified depth 1 → redirect-to-login → closed as route. Coverage
statement cites three exhausted classes by ledger row, not by
feeling.
