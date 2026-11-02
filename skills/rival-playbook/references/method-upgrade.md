# The method upgrade — critiquing the folk competitor war, shipping the evidence-disciplined playbook

The charter's A16 charge, applied to the strategist tradition:
**strategy named is not advantage delivered.** Sun Tzu survives
twenty-five centuries because the maxims are real; the folk way of
"beating competitors" fails because it keeps none of the
discipline. This module names the floors of the folk competitor war
and ships the replacement: a census protocol with pinned artifacts,
the hollow map with cited verdicts, the pressure allocation rule,
the duel rule with capped wording, and the re-census loop. An agent
that has never read The Art of War must still run this at precision.

## 1. The critique — five mechanical weaknesses of the folk way

| # | What the folk way shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------------ | --------------------------------- |
| W1 | The hype war — "most advanced", "industry-leading", adjectives as armament | No axis, no measurement, nothing falsifiable; a claim that cannot lose cannot win, it can only be louder |
| W2 | Feature-count parity — checklists compared by length, bullets counted | The corpus with more bullets "wins" while neither side runs an auditor; length measures verbosity, not enforcement |
| W3 | FUD and badmouthing — the rival's reputation as the battlefield, un-citable claims about its internals | Poison twice over: un-credible to anyone who checks, and it burns the claimant's own evidence discipline — the one asset the house actually owns |
| W4 | Un-pinned benchmarks — grading rivals from memory against last year's README screenshot | The census equivalent of the wiki-fingerprint floor: the "weakness" being attacked may have retired two releases ago |
| W5 | Cargo-cult copying — the rival ships a feature, the corpus ships its surface without the discipline | The copy is decoration: the validator, tests, and auditor that make the feature real are exactly what did not get copied |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Both sides graded on public, pinned artifacts | **M1** — the census protocol |
| U2 | Weakness as a cited verdict, not a vibe | **M2** — the hollow map |
| U3 | Concentration until mechanically owned | **M3** — the pressure allocation rule |
| U4 | Claims settled on measured axes | **M4** — the duel rule |
| U5 | The map kept honest after every release | **M5** — the re-census loop |

## 3. The executable protocol — M1 through M5

### M1 — the census protocol

1. One table, both sides, the SAME axes: charter or README (doctrine
   stated), validator (authoring gate), test suite (enforcement
   count), method layer (critique-and-upgrade modules per organ),
   auditor (report gate), benchmark (ground truth).
2. Every row cites the artifact and its pin date; a row older than
   180 days is STALE — usable, but the map says so (the W4 floor).
3. Grade = what the artifact enforces, never what the README
   claims. A "validated" with no validator script is a census row
   showing the ABSENCE of a validator.

### M2 — the hollow map

1. The axes × rivals matrix carries the census grades.
2. A HOLLOW verdict — an axis with no artifact-backed answer on the
   rival's side — cites the exact rows that show the absence; no
   hollow without rows.
3. The retirement rule: the day a rival ships a disciplined answer,
   the hollow retires with a correction on record. A map that never
   retires a verdict is a grudge, not a map.

### M3 — the pressure allocation rule

1. At most two hollows receive force; the rest are parked.
2. Ownership is demonstrated by GATES the census can point at:
   validator runs green, test counts rise, the auditor exits zero —
   the axis is enforced mechanically HERE and nowhere else on the
   table.
3. The ownership claim is worded exactly at what the gate shows —
   not at what the gate might someday show.

### M4 — the duel rule

1. A superiority claim ships only with a measured axis attached:
   proving-ground numbers (coverage, precision, hallucination, harm
   events) or census facts (artifact present or absent, pinned).
2. Wording is capped at the demonstrated axis — the disclosure-gate
   habit: "every bundle passes a mechanical validation gate; the
   census shows none in R" ships; "the best corpus on the market"
   does not.
3. The banned-wording list is mechanical: superlatives without a
   measured axis behind them fail the rule the same way a CVSS
   mismatch fails a report.

### M5 — the re-census loop

1. Every rival release is a re-census trigger for the affected rows;
   every ownership claim re-cites its pins.
2. Retirements and downgrades land as corrections on record — the
   corpus's own correction tradition applied to the market map.
3. The loop's cadence follows the release train, not the calendar:
   a census is refreshed when the artifacts move, and staleness is
   stamped, never ignored.

## 4. Falsifiers — what would prove this method wrong

* A rival ships the hollow WITH discipline → the hollow retires, the
  correction lands, and any claim built on the retired hollow is
  withdrawn. The method working, not the method failing.
* A census claim cannot name its artifact + date → the row dies
  before the map is built.
* A superiority claim survives only by dropping its superlative →
  the claim was hype; the measured form is what ships.
* The proving-ground number and the census grade disagree → one of
  them is stale; re-run both before any claim cites either.
* The hollow map has not retired a verdict across several rival
  releases → the census has gone stale; the map is being maintained
  by memory (the W4 floor, back again).

## 5. Worked micro-example (format is the deliverable; corpus R is fictional)

Rival corpus R is named. Census row (R, validator axis): "no
validation script found in the repository; README states 'every
skill is validated' — pinned 2026-11-02." Census row (ours,
validator axis): "scripts/validate_skill.py --all exits PASS across
all bundles, 0 warnings — pinned same date." Hollow verdict: "axis:
mechanical authoring gate — no artifact-backed answer on R's side
(census rows cited)." Ownership (pressure): the gate already runs in
the wiring commit of every organ — enforced here, absent there.
Duel: the claim ships as "every bundle in this corpus passes a
mechanical validation gate before commit; the census, pinned and
public, shows no equivalent artifact in R" — capped at the
demonstrated axis, both pins attached, no superlative, no
characterization of R beyond its own repository. If R ships a
validator next release, the hollow retires with a correction, and
the claim narrows to what remains measured.
