# campaign-protocol.md — the season layer: Tian Ji allocation and tempo doctrine

The method-upgrade module (M1–M5) governs ONE contest — census, hollow
map, pressure, duel, re-census. This module governs the SEASON: how
campaigns are chosen against the field, how the budget is allocated
across segments, and which tempo each campaign runs at. It is the
allocation arithmetic of 田忌赛马 (Sun Bin, in Sima Qian's Shiji) and
the tempo doctrine of 持久战 vs 速决战, as records and gates.

## S1 — The two ledgers (知彼知己, seasonal form)

```
KNOW season=<id>
  RIVAL entry=<hunter|team|corpus> evidence=<date-pinned public
    artifacts: disclosed reports, published methodology, leaderboard
    capture + date> strengths=<axes where their record is strong>
    hollow=<axes their record never touches>
  SELF axes=<per axis: measured record from this corpus's ledger —
    findings by class, median severity, reproducibility rate> assets=<
    versioned: corpora, pattern packs, method layers> budget=<the
    season's honest effort cap>
```

Same evidence law as M1's census: public artifacts only, dates
pinned; anything "just known" about a rival is inadmissible until it
has a citation. The self ledger is the module ledger's yield record
— self-image without yield history is astrology.

## S2 — The segment map (the hollow map, extended with yield)

Per program in scope, one row per segment (bug class × surface):

```
SEGMAP program=<id> segment=<class×surface>
  density=<low|med|high — rivals visibly working it, cited>
  yield=<payout flow per unit effort: program payment history +
    disclosed reports, cited> difficulty=<execution cost per the
    corpus's cost hierarchy> verdict=<hollow|contested|flagship|desert>
```

Verdict grammar (extends the hollow map with food): **hollow** = low
density + real yield (STRIKE HERE — this is 避实击虚 with dinner);
**contested** = high density + real yield (enter only with an edge);
**flagship** = high density + high visibility (enter when position is
assembled); **desert** = low density + no yield (quiet is not enough
— strategy needs food, not just emptiness).

## S3 — The Tian Ji allocation table (田忌赛马, as arithmetic)

The race from the Shiji: Tian Ji lost every same-tier matchup until
Sun Bin re-ordered — worst horse against the king's best (concede),
best against the king's middle (win), middle against the king's worst
(win): the series 2:1. The anecdote is taught as cleverness; the
executable content is a TABLE:

```
ALLOCATE season=<id>
  comparative=<per segment: our axis strength (S1 SELF) vs the
    field's (S1 RIVAL), both cited — the ranking and its evidence>
  concede=<segment(s) where field strength is dominant THIS season,
    with the comparative reason on record>
  commit=<at most TWO segments — the concentrated budget, the
    pressure principle (压强) applied at season scale>
  arithmetic=<expected yield per committed segment from SEGMAP
    yield × committed share — the numbers that chose this>
```

Gates (mechanically enforced):

1. **At most two committed segments** — 集中优势兵力 as a hard cap;
   spreading thin is the season-scale cardinal error;
2. **Every concession and commitment carries its comparative
   citation** — the table is arithmetic, not hope;
3. **Deserts are never commitments**, no matter how quiet;
4. **Re-rank next season** (S6 → S1): strengths drift, fields change;
   last season's right concession may be this season's wrong one.
   One mis-rank is data; two is a broken map.

## S4 — The tempo declaration (持久战 vs 速决战)

Per committed segment, BEFORE it runs:

```
TEMPO segment=<id> class=<protracted|quick-decisive>
  protracted:    progress-gates=<skill assembled / asset versioned,
                  per season> stop=<gates met | season end — sunk
                  cost is never a reason to continue>
  quick-decisive: window=<what opened it: fresh scope, new
                  disclosure, new program> stop=<the census shows the
                  contest arriving (density signal) | window closed —
                  rotate out, do not grind>
```

Rules:

1. **A campaign without its TEMPO line is untempoed** — it defaults
   to grinding, which the canon and this corpus both grade as the
   expensive way to lose;
2. **Protracted campaigns compound**: the skill being built, the
   corpus asset being versioned — 以战养战 (use the war to feed the
   war): every campaign's findings upgrade the assets, every season
   review upgrades the next allocation;
3. **Quick-decisive campaigns rotate**: when the density signal shows
   the field arriving, exit on record — the window, not the grind,
   was the edge.

## S5 — Execute and observe

Campaigns run under the owning organs' method layers (this organ
plans; it never hunts). The strategist's only acts during execution:

1. Phase-boundary review: actual vs planned yield per segment;
2. Re-census on new public data (M5's loop) — a disclosed report
   changes the map ONLY if it changes density or yield evidence;
3. Re-allocation at phase boundaries ONLY (mid-sprint pivoting is
   whim wearing strategy's clothes), with the new arithmetic
   recorded.

## S6 — The season review

```
REVIEW season=<id> planned=<allocations + expected yields>
  actual=<yields per segment, cited from the ledger>
  table-verdict=<which concessions were right, which commitments
    mis-ranked, with the misses' evidence>
  compounding=<which reusable assets the season upgraded — corpus,
    pack, method layer; a season that only spent is graded wasted
    regardless of yield>
  next-season=<feeds S1: re-ranked axes, refreshed ledgers>
```

## Falsifiers — what would prove this protocol wrong

* A committed segment yields below plan across two reviews while its
  SEGMAP evidence stood → the yield model is miscalibrated for that
  program class; re-derive from the miss, never re-commit on hope.
* A concession's segment is won by a weaker rival → the comparative
  table mis-ranked (strength evidence stale); ledger the miss and
  tighten the re-census cadence.
* A "quick-decisive" window stays open a year; a "protracted" skill
  assembles in weeks → the window signals need recalibration; the
  DECLARATION discipline stays — undeclared tempo is grinding.
* Mid-sprint re-allocation without a phase boundary → hard violation;
  the re-allocation is void and the record shows it.
