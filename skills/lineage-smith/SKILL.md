---
name: lineage-smith
version: 1.3.0
type: ai-skill
architecture: package
description: >-
  Forge-tier organ — the legend-assimilation factory. Turns a named public
  security figure into a shipped skill bundle under the operator's standing
  doctrine — find the popular figures, observe them, study their COMPLETE
  public corpus (talks, papers, journal publications, blogs, tools,
  advisories, post-mortems — read in full, never snippet-mined), model the
  psychology and the way of thinking from documented behavior only, extract
  the decision logic as a distillation, and forge the executable method into
  an organ that is BORN with its method layer and wired through the charter,
  the lineage registry, and the validation gates. Runs the scored selection
  gate against the candidate queue, the corpus census with a read-in-full
  ledger, the five-lens psych-read, the distillation record, the forge
  checklist, and the wiring gate. Since v1.1.0 the psych-read carries its
  evidence-class catalog (references/psychology-catalog.md): per lens
  dimension, which evidence is admissible and which is not (mythology-class
  exclusions on record), the OPINION quarantine gate that keeps unartifacted
  readings out of distillation, and the assembly crosswalk that pairs lens
  lines into organ design traits (confirmation rigor, unit of work, pacing,
  record shapes). Use when the operator nominates a figure for assimilation,
  orders corpus growth, or asks for the next organ ("rakit skill dari tokoh",
  "pelajari tokoh hacker", "analisis psikologi tokoh", "asimilasi lineage",
  "assimilate a lineage", "forge a new organ", "skill baru dari metodologi",
  "bangun organ baru", "the next legend", "korpus makin besar", "corpus
  growth").
category: security/craft-forge
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: v1 — the operator's assimilation doctrine, the standing brief behind the three method waves — find the figures, read everything public, model the thinking, ship the method; 26 lineages on the registry under this doctrine, the first two candidate-queue executions landed protocol-forensics (the Dan Kaminsky lineage) and interior-cartographer (the James Forshaw lineage)
  requires: mythos-arsenal MCP server (arsenal/server.py); skill-mythos charter v1.10+
---

# lineage-smith v1.3.0 — Read Everything, Ship the Method

## 0. What This Skill Is — and Is Not

* **Is**: the forge-tier organ that grows the corpus by assimilating
  named public figures — the operator's standing doctrine executed as
  a factory. It selects a figure from the candidate queue (or screens
  a fresh nomination), reads the complete public corpus, models the
  thinking from documented behavior, extracts the decision logic,
  forges the bundle under the house authoring contract, and wires it
  into the charter, the lineage registry, and the gates. Nothing
  ships on biography; everything ships on method.
* **Is not**: a biographer, a fan page, or a quote mine. Where a
  figure grew up, who they feuded with, what they said about life in
  a podcast — none of it enters a distillation. Only what the figure
  BUILT and WROTE and DEMONSTRATED in public does. Inner-life
  speculation is out of bounds by hard rule (§5.2).

## 1. Inherited Contracts

Plugs into the charter (skill-mythos) as the tier-7 forge organ.
Inherits A2 (research-grounded synthesis — read in full, never
snippet-mined), A3 (legitimate assimilation — attributed, verified,
no fabrication; the assimilation-doctrine module is the contract),
A14 (the three registers — WHAT/WHY/HOW or the technique does not
ship), and A16 (method over mythology — the critique-and-upgrade
layer is born in, not retrofitted). The authoring contract
(CONTRIBUTING.md) and the validation gate (scripts/validate_skill.py)
are part of the forge, not afterthoughts. The spine's R0 scope gate
does not apply here — the forge's targets are public figures and the
corpus itself, never live engagement infrastructure.

## 2. The Lineage Layer (v1 — the operator's doctrine)

The doctrine behind every lineage already on the registry, stated as
the organ's five tenets:

1. **Find the popular figures.** Fame is not the credential — corpus
   is. The gate wants figures with years of public, method-bearing
   output (P1's score, not follower counts).
2. **Read everything public.** Talks, papers, journal publications,
   blog posts, tools, advisories, post-mortems — the COMPLETE corpus,
   read in full. A distillation drawn from highlight reels is
   snippet-mining, and snippet-mining is fabrication with extra steps.
3. **Model the psychology and the thinking — from documented
   behavior.** Heuristics that repeat across works, obsessions that
   span years, aesthetics stated in the figure's own words, failure
   handling on the record, decision cadence where timelines are
   public. The lens set is §4.
4. **Ship the method, not the mythology.** The output is executable
   decision logic — numbered phases, gates, falsifiers — so an agent
   with zero prior exposure to the figure runs at precision. A
   lineage named is not expertise delivered (A16).
5. **Attribute, and keep corrections on record.** Every distillation
   names its sources; where the record needed correcting, the
   correction stays in the registry entry. Assimilation without
   attribution is borrowing without a license.

## 3. The Protocol — Six Phases, Each With Its Gate

### P1 — SELECT (the scored gate)

Score every candidate on five axes, 0–2 each (the queue ships the
running table — references/candidate-queue.md):

| Axis | 0 points | 2 points |
| --- | --- | --- |
| corpus volume | a few posts, one talk | years of method-bearing output |
| method explicitness | results only, no HOW | the HOW is documented |
| public verifiability | hearsay, interviews only | primary artifacts readable |
| house non-overlap | re-covers an existing organ | opens unclaimed ground |
| psych-read yield | behavior invisible | patterns repeat across works |

Gate: score ≥ 7/10 to hold a queue slot; ≥ 8 to be nominated next.
Overlap is resolved FIRST — a documented upgrade of an existing organ
counts as an assimilation too (see Q7 in the queue).

### P2 — COLLECT (the corpus census)

Inventory the figure's complete public corpus: primary artifacts
(tools, code, advisories, disclosed bugs), long-form writing (books,
papers, blog), talks with published decks or transcripts, and
documented interviews — each with year and access status. The census
is a table in the dossier, and the read ledger is part of it: which
artifact was read completely, which was skimmed and why. A census
with unread load-bearing artifacts blocks P3.

### P3 — READ (the psych-read, five lenses)

Run §4's lens set over the census. Every claim lands as documented
behavior — artifact, year. A pattern claimed from fewer than three
independent artifacts stays a hypothesis on the dossier, never a
distillation line.

### P4 — EXTRACT (the distillation record)

Distill to decision logic: the heuristics, the stop rules, the
aesthetic that decides what counts as a finding. The output format
is the registry entry — figure, distillation, sources, correction —
plus the critique floor list: where the figure's own published
method was mechanically weak (the W-list for the method-upgrade
module; the critique is a license granted by attribution, never a
ceiling).

### P5 — FORGE (the authoring contract)

Assemble the bundle: SKILL.md routing layer (three registers A14,
hard rules, falsifiers, trigger phrases), references depth modules,
and references/method-upgrade.md BORN IN — the critique and the
executable upgrade ship in the same commit the organ is born in. The
authoring contract applies line by line: minimal but complete,
original work only, no placeholder markers, no current-state
capture.

### P6 — WIRE (the gates)

Wire the organ in: charter bundle table + version bump, tier registry
(the 7-forge tier), lineage registry entry, README catalog row,
bundle-map load-when row, architecture diagram regeneration. Then the
gates: scripts/validate_skill.py --all exits PASS, the unit tests
agree with every count the wiring changed, the server selftest stays
green. An organ that is not wired is a draft, not a skill.

## 4. The Psych-Read — Five Lenses, Documented Behavior Only

| Lens | The question | Evidence floor |
| --- | --- | --- |
| L1 heuristics | which shortcuts repeat across separate works? | ≥ 3 independent artifacts |
| L2 obsession | which problem class spans the years? | multi-year corpus arc |
| L3 aesthetics | what does the figure call elegant or ugly, in their own words? | quoted statement, cited |
| L4 failure mode | how is being wrong handled — retraction, correction, silence? | documented post-mortem or correction |
| L5 cadence | when does the hunt stop and the disclosure ship? | public timeline where one exists |

The boundary: inner life is not evidence. Motives, childhood,
personality typing — anything the figure did not state or demonstrate
in public — never enters a distillation. The psych-read reads
behavior, and behavior leaves artifacts.

## 5. Hard Rules (mechanically enforced)

1. **Read-in-full before distillation.** The census's read ledger
   shows every load-bearing artifact read completely; a skimmed
   load-bearing artifact blocks P3 (the gate is the ledger).
2. **Documented behavior only.** Every psych-read claim cites
   artifact and year; patterns backed by fewer than three artifacts
   stay hypotheses.
3. **Born with the method layer.** No organ ships without its
   references/method-upgrade.md — A16 debt is not allowed to accrue
   again, not even for one release.
4. **One lineage, one forge.** A figure lands as one new organ or one
   documented upgrade of an existing organ; double-dipping needs a
   correction on record.
5. **The gates ride with the forge.** Validator, tests, selftest —
   the wiring commit fails if any of them fails. "Forge now, validate
   later" is the exact failure mode A16 exists to prevent.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Scoring a nomination, screening the queue | references/candidate-queue.md |
| Running census, psych-read, distillation | this file + references/method-upgrade.md |
| Forging the bundle | CONTRIBUTING.md + scripts/validate_skill.py |
| Wiring the registry entry | mythos_lineages registry (arsenal/tools/mythos.py) |
| Charter table, bundle map, README row | skill-mythos bundle (its own modules) |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Critiquing the folk way of studying famous figures; running the executable M1–M6 | references/method-upgrade.md |
| Screening the next legends; the scored queue with six standing candidates (Q1 and Q2 executed — retired into protocol-forensics and interior-cartographer) | references/candidate-queue.md |
| Evidence classes per lens dimension; the OPINION quarantine; the assembly crosswalk | references/psychology-catalog.md |
