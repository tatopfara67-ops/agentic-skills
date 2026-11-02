# psychology-catalog.md — the lens set's evidence classes and the quarantine gate

The five lenses (L1–L5) name WHAT to read in a figure's documented
behavior. This catalog fixes, per lens dimension, WHICH evidence
classes are admissible and which are not — plus the OPINION
quarantine that keeps unartifacted readings out of distillation. A
psych-read without this gate produces vibes, and vibes do not forge
organs.

## Part 1 — The lens dimensions with evidence classes

| Lens | Dimension | Admissible evidence | NOT admissible |
| --- | --- | --- | --- |
| L1 heuristics | which shortcuts repeat | the same choice pattern across ≥ 3 independent artifacts, each cited | one-off cleverness; press retellings of cleverness |
| L2 obsession | which problem class spans the years | multi-year corpus arc: the figure's own artifacts returning to the class, cited per return | topics amplified by coverage but not by the figure's own output |
| L3 aesthetics | what they call elegant or ugly | quoted statements, cited to artifact and year — checked against what they actually built | aphorisms quoted out of context (context is the evidence) |
| L4 failure mode | how being wrong is handled | documented post-mortems, corrections, retractions, silence-with-dates — the record of what happened next | folklore about character; "they never admit mistakes" (check the record first) |
| L5 cadence | when the hunt stops and disclosure ships | public timelines where one exists: disclosure dates vs discovery windows, cited | assumed dates; the figure's self-reported speed unchecked |
| (cross-lens) | risk appetite | documented choices under uncertainty: target picks, tooling bets, disclosed tradeoffs in their own writing | press adjectives ("bold", "cautious") |
| (cross-lens) | evidence standard | what they accept as proof in their own writeups: differentials, PoCs, instrumentation — cited | their rhetorical confidence |
| (cross-lens) | composition habit | documented compositions in their own work (X plus Y becomes Z) — the chain shown, not just claimed | impact headlines without the composition shown |

## Part 2 — The quarantine gate (OPINION, on record, quarantined)

A psych-read line without its artifact is labeled OPINION and
quarantined:

```
OPINION figure=<name> lens=<L1..L5|cross> reading=<the claim>
  artifact=NONE status=quarantined next=<what evidence would admit
  it: which artifact class, where it might exist>
```

Opinions are allowed — they often point where evidence should be
gathered next (the `next` field exists for exactly this). But they
never feed P4's distillation record: a distillation line citing a
quarantined opinion fails the forge gate. This is the difference
between a lineage organ and every "think like a hacker" blog post
ever written.

## Part 3 — Reading the lenses together (the assembly crosswalk)

The lenses cross at the assembly-relevant traits — the ones the
operator's doctrine says to convert into method:

1. **Risk appetite × evidence standard** → the organ's confirmation
   rigor: how many controls, which thresholds, when a lead ships;
2. **Obsession (L2) × composition habit** → the organ's unit of work
   and chain doctrine: what counts as one finding, what composes
   into impact;
3. **Cadence (L5) × search-space ordering** → the organ's pacing and
   stop rules: sweeps versus campaigns, saturation gates;
4. **Aesthetics (L3) × abstraction level** → the organ's record
   shapes: what a finding must cite, where generalization stops.

Each crosswalk line cites BOTH lens lines that feed it — the
crosswalk is analysis with provenance, not a projection.

## Falsifiers — what would prove this catalog wrong

* A psych-read line cites press coverage as its only evidence →
  mythology-class; delete or re-source from primary artifacts
  (P2's census knows which artifacts are primary).
* Two lens lines cite the same artifact but contradict each other →
  the artifact was read partially; re-read in full before either
  line stands.
* A distillation line survives while citing a quarantined OPINION →
  the forge gate failed on audit; the distillation line is withdrawn
  until its evidence arrives.
