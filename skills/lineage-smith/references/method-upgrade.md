# The executable method — M1–M6 for lineage-smith

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
the folk method and its worked example) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M6

### M1 — the scored selection gate

1. Score the candidate on the five axes (corpus volume, method
   explicitness, public verifiability, house non-overlap, psych-read
   yield), 0–2 each; the queue table carries the running scores.
2. Gate: ≥ 7/10 holds a queue slot; ≥ 8 is nominatable. A candidate
   below 7 retires WITH its reasons recorded — a declined candidate
   is knowledge too (the W1 floor, inverted).
3. Overlap resolves FIRST: a figure whose ground is already covered
   forges an UPGRADE of the existing organ, and the upgrade must cite
   what the original organ lacked.

### M2 — the census protocol

1. Inventory the complete public corpus in a table: artifact class
   (primary tool/code, advisory, disclosed bug, long-form writing,
   talk with deck or transcript, documented interview), year, access
   status.
2. The read ledger rides with the census: each artifact marked
   read-full or skimmed-with-reason. Load-bearing artifacts marked
   skimmed BLOCK the psych-read until read (the W2 floor).
3. The census bounds the corpus honestly: where the corpus is too
   large to read completely, the census states the bound and the
   selection criteria — a stated bound is a method; an unstated one
   is snippet-mining.

### M3 — the psych-read protocol

1. Run the five lenses — L1 heuristics, L2 obsession, L3 aesthetics,
   L4 failure mode, L5 cadence — each claim landing as documented
   behavior (artifact, year).
2. The three-artifact floor: a pattern appearing in fewer than three
   independent artifacts stays a hypothesis on the dossier (the W4
   floor — unfalsifiable single observations never become method).
3. The inner-life ban: motives, childhood, personality typing are
   out of bounds; the psych-read reads behavior, and behavior leaves
   artifacts.

### M4 — the distillation record

1. The distillation ships in the registry's exact format — figure,
   distillation, sources, correction — so the registry remains the
   single compliance artifact (the W5 floor).
2. The critique floor list rides with it: where the figure's own
   published method was mechanically weak, listed — this becomes the
   W-list of the new organ's method-upgrade module.
3. Sources name what was ACTUALLY read, with years — never "various
   public sources".

### M5 — the forge checklist

1. SKILL.md routing layer with the three registers (A14), hard
   rules, falsifiers, and trigger phrases — the validator's
   frontmatter contract is part of the forge.
2. references/method-upgrade.md BORN IN: critique + executable
   upgrade in the birth commit (A16 from day zero).
3. Depth modules for everything the routing layer cannot carry;
   minimal but complete; no placeholder markers; no current-state
   capture.

### M6 — the wiring gate

1. Wire: charter bundle table + version bump, tier registry, lineage
   registry entry, README catalog row, bundle-map load-when row,
   architecture diagram regenerated.
2. Gate: scripts/validate_skill.py --all exits PASS; the unit tests
   agree with every count the wiring changed; the server selftest
   stays green. A FAIL at this gate reverts the forge — fix the
   skill, not the gate.

## 2. Falsifiers — what would prove this method wrong

* A claimed pattern turns up in only one artifact → it was never a
  pattern; the hypothesis dies on the dossier, the distillation never
  lands it (the method working, not failing).
* The census cannot produce three independent method-bearing
  artifacts → the candidate drops below the queue floor; the entry
  retires with its reasons on record.
* The forged organ fails the validator, or the registry entry cannot
  be produced → the forge is incomplete; nothing commits.
* A later artifact contradicts the distillation — the figure changes
  method, publishes a retraction → the registry gains a correction
  entry and the organ's method-upgrade module gains a revision row.

## 3. Worked micro-example (registry-consistent)

Candidate: **Gordon Lyon (Fyodor)** — scored 9/10 at screening
(corpus volume 2: the 1997 Phrack paper and the 2009 book plus the
Nmap codebase; explicitness 2: the HOW is the paper's core;
verifiability 2: all primary artifacts readable; overlap 2: scan
economy was unclaimed ground; yield 2: cost-hierarchy reasoning
recurs across paper, book, and tool design). Census: "The Art of
Port Scanning" (Phrack 51, 1997) read in full; Nmap Network
Scanning (2009, free online edition) read in full; the Nmap tree
read as a primary artifact. Psych-read, sample lines — L1 heuristic:
liveness before depth, documented in the paper's scan taxonomy and
the book's chapter structure; L5 cadence: technique papers shipped
as the tool matured, timeline public. Distillation (the registry
entry, verbatim class): scan economy — cost hierarchy,
speed/stealth/reliability triangle, states as recorded inferences,
priors over exhaustive sweeps, adaptive pacing. Critique floor: the
published art priced scans in prose, not budgets — shipped later as
scan-economist v1.1.0's budget table and timing gates (wave three).
Outcome: organ forged, wired, gates green — the exact path every
queue candidate now runs.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge, applied to the operator's own doctrine:
**studying famous hackers is a real method only when it is
mechanical.** The folk way — hero worship, highlight reels, tool
collections — produces fandom, not expertise. This module names the
floors of the folk method and ships the replacement: a scored
selection gate, a census with a read-in-full ledger, a five-lens
psych-read bound to documented behavior, a distillation record that
lands in the lineage registry, a forge checklist, and a wiring gate.
The proof it works is the corpus itself: three method waves, twenty-
four registered lineages, every one graded by these gates.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the folk method (context, not steps)

| # | What the folk way shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------------ | --------------------------------- |
| W1 | Hero worship — the legend's biography, feuds, and trivia recited as expertise | Biography displaces method: the student can narrate the life but cannot run the decisions; nothing in a birth year improves a hunt |
| W2 | Snippet mining — talks consumed as highlight reels, quotes pulled from listicles, "top 10 tips" posts | The corpus is never read in full, so the method's context is invented by the reader; a quote without its talk is a fingerprint without a provider |
| W3 | Tool cargo-cult — installing the legend's tools, following their GitHub stars | Possession is not decision logic: the tool says nothing about WHEN and WHERE the master pointed it, which is the entire expertise |
| W4 | Unfalsifiable distillation — "think like X", "be creative like Y" | No oracle, no stop rule, no falsifier: advice that cannot fail cannot teach, and a distillation nobody can check is fabrication with prestige |
| W5 | Silent borrowing — methods absorbed without attribution or correction records | The lineage becomes anonymous slop; the corpus cannot say what it took, from whom, or what it fixed — the exact debt A16 closed |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Selection by corpus, not fame | **M1** — the scored selection gate |
| U2 | The complete public corpus, read in full, on a ledger | **M2** — the census protocol |
| U3 | Psychology modeled from documented behavior only | **M3** — the psych-read protocol |
| U4 | Distillation as a checkable registry record | **M4** — the distillation record |
| U5 | The forge under the authoring contract, method layer born in | **M5** — the forge checklist |
| U6 | Wiring through charter, registry, and gates | **M6** — the wiring gate |
