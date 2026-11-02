---
name: rival-playbook
version: 1.1.0
type: ai-skill
architecture: package
description: Forge-tier organ — the competitor playbook. Positions THIS corpus against rival skill corpora and agentic-security stacks using the Chinese competitive-strategy tradition reduced to an evidence discipline. Runs the rival census (知彼知己，百战不殆 — know the rival and know yourself; both sides graded on the SAME axes strictly from public, date-pinned artifacts — evidence discipline, falsifiers, scope gates, method layers, reproducible output, audited closure), builds the hollow map (避实击虚 — avoid strength, strike weakness; the axes where rivals have no artifact-backed answer), allocates force by the pressure principle (压强原则 — disproportionate concentration on one or two hollows until they are owned outright by mechanical gates, not claims), settles superiority without a hype war (不战而屈人之兵 — win without fighting; proving-ground numbers, wording capped at the demonstrated axis), and takes the unclaimed ground first (农村包围城市 — niche encirclement before the mainstream contest). Hard-bans the deception stratagem family and every un-citable claim about a rival. Since v1.1.0 it also carries the season layer (references/campaign-protocol.md): the two seasonal ledgers, the segment map with yield verdicts, the Tian Ji allocation table (田忌赛马 — concede the unwinnable segment on record, commit to at most two, comparative arithmetic cited), the tempo declarations (持久战 vs 速决战 — protracted campaigns compound, quick-decisive windows rotate, stop rules stated), and the season review that feeds the next allocation; the stratagem map gains the translated middle class (围魏救赵, 李代桃僵, 顺手牵羊, 以逸待劳 — shape kept, harm removed, each bound to a census artifact). Use when the operator names a competitor, orders the corpus to win the market, or any claim about rival corpora is about to ship ("kalahkan kompetitor", "kalahkan korpus rival", "beat the competitor", "rival corpus", "benchmark rival", "posisi korpus", "competitive strategy", "strategi kompetitif", "why is our stack better", "bandingkan dengan korpus lain").
category: security/craft-forge
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: v1 — Sun Tzu (孙子) The Art of War and the 36-stratagem tradition (三十六计), plus documented modern Chinese competitive practice (the publicized pressure principle 压强原则); A15's war-doctrine crosswalk extended from the engagement campaign to corpus-vs-corpus competition
  requires: mythos-arsenal MCP server (arsenal/server.py); skill-mythos charter v1.10+
---

# rival-playbook v1.1.0 — Win the Market Without a Hype War

## 0. What This Skill Is — and Is Not

* **Is**: the forge-tier organ for corpus-vs-corpus competition. It
  grades rival skill corpora from their public artifacts, finds the
  hollow axes where rivals have no disciplined answer, concentrates
  the corpus's force there until gates — not marketing — prove
  ownership, and settles every superiority claim on a measured axis
  with capped wording.
* **Is not**: a marketing playbook, a FUD machine, or anything that
  touches a rival's infrastructure. The census reads PUBLIC
  artifacts (repos, docs, validators, test suites) the way
  subdomain-hunter reads certificate logs — passively, date-pinned,
  never touching the rival's live systems. Disparagement and
  speculation about rivals' internals are hard-banned (§5).

## 1. Inherited Contracts

Extends A15 (war logic) from the engagement campaign to the corpus
market: the charter's war-doctrine already shapes hunts with Sun
Tzu's maxims; this organ applies the same tradition to the stack's
own positioning. The proving ground (mythos-proving-ground) is the
duel floor; the charter's quality gates define the census axes; the
disclosure-gate habit (wording capped at the demonstrated class)
governs every superiority claim; A16 governs the hollow-map verdicts
(a positioning claim without an artifact behind it is mythology).
The spine's R0 scope gate applies in spirit: the census's only
targets are the rival's public artifacts — the same deny-by-default
discipline, pointed at documents instead of hosts.

## 2. The Lineage Layer (v1 — the strategist tradition)

Sun Tzu's maxims, the stratagem tradition, and documented modern
competitive practice, each reduced to an executable rule with its
evidence discipline:

1. **知彼知己 (zhī bǐ zhī jǐ — know the rival, know yourself).** The
   census: both sides graded on the same public axes, every row
   date-pinned. Self-knowledge rides the same table — the corpus is
   graded by its own gates, not its own README.
2. **避实击虚 (bì shí jī xū — avoid strength, strike weakness).**
   The hollow map: the axes where rivals have no artifact-backed
   answer are the only axes worth contesting.
3. **压强原则 (the pressure principle).** Force allocation: one or
   two hollows, disproportionate concentration, until ownership is
   demonstrated mechanically — enforced here and nowhere else, per
   the census.
4. **不战而屈人之兵 (bù zhàn ér qū rén zhī bīng — win without
   fighting).** The duel rule: measured axes beat marketing claims;
   the hype war is refused, not fought harder.
5. **农村包围城市 (niche encirclement).** The unclaimed ground
   first — legend tier, mirror hunting, method layer — dominate
   where the mainstream checklists are not, then let the niche's
   gates speak for themselves.

The full crosswalk — maxims, the stratagem register with its banned
deception family, and the attribution notes for the modern practice
— lives in the stratagem-map module (references/stratagem-map.md).

## 3. The Five Rules — R1 to R5

### R1 — the rival census (知彼知己)

Artifact classes, per corpus, per side: charter/README (doctrine),
validator (authoring gate), test suite (enforcement count), method
layer (A16 modules per organ), auditor (report gate), benchmark
(ground truth). Every row: artifact cited + pin date. Rows older
than 180 days are STALE and cited as such (the fingerprint-freshness
habit). Both sides graded on the SAME axes — a census that grades
the rival on artifacts and ourselves on intentions is not a census.

### R2 — the hollow map (避实击虚)

The axes × rivals matrix with grades. A HOLLOW verdict — axis where
a rival has no artifact-backed answer — cites the census rows that
show the absence. The hollow dies the day a rival ships a
disciplined answer; retirement is recorded, not resented.

### R3 — the pressure allocation (压强)

Pick at most two hollows. Concentrate until ownership is
demonstrated by GATES: the validator runs, the test counts, the
auditor pass rates — mechanical enforcement the census can point at.
Ownership means the axis is enforced here and nowhere else on the
table. Spreading force across five axes owns none of them.

### R4 — the duel rule (不战而屈人之兵)

Superiority claims ship ONLY on measured axes — proving-ground
numbers or census facts — with wording capped at the demonstrated
axis (the disclosure-gate habit applied to market claims). "Best",
"most advanced", "industry-leading" with no measured axis behind
them are banned wording, on our side, always.

### R5 — the loop (兵贵神速)

Census → hollow → forge (the lineage-smith queue decides the next
organ) → re-census after every rival release and every ownership
claim. A retired hollow is the method working; the correction record
is the proof the map stays honest.

## 4. Procedure — Numbered Actions

1. Trigger: a rival is named, positioning is questioned, or a claim
   about rival corpora is about to ship.
2. Run the census (R1) — both sides, same axes, pin dates on every
   row.
3. Build the hollow map (R2) — verdicts cited to census rows.
4. If an order follows: allocate force (R3) — at most two hollows,
   the lineage-smith queue takes the next organ from there.
5. If a claim is about to ship: run the duel rule (R4) — find the
   measured axis, cap the wording, attach the census pins.
6. Bookkeeping: every rival release is a re-census trigger; every
   retirement is a correction on record.
7. Exit gate: numbers stated — census rows counted, hollows held,
   claims shipped with their caps. Anything unmeasured is parked
   with a reason, not asserted.

## 5. Hard Rules (mechanically enforced)

1. **Public artifacts only, date-pinned.** A census row without
   artifact + date dies before the map; rows > 180 days are STALE.
2. **No disparagement, no FUD, no speculation** about rivals'
   internals or motives — the same inner-life ban the psych-read
   runs: documented artifacts only.
3. **The deception stratagem family is rejected** (the 声东击西
   class — see references/stratagem-map.md). Preparation and
   positioning only; a move that requires an un-citable claim is
   not a move.
4. **Wording capped at the demonstrated axis.** Unmeasured
   superlatives are banned on our side; the rival is quoted from
   its own artifacts, never characterized beyond them.
5. **No copying a rival's surface without their discipline.**
   Assimilation doctrine (A3) applies to rivals too: read it fully,
   attribute it, or do not ship it.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Census and hollow bookkeeping | the dossier table format + this file |
| Duel numbers | mythos-proving-ground benchmark + the arsenal test suite |
| Force allocation (the next organ) | lineage-smith + its candidate queue |
| Word capping at ship time | the quality-gates module of skill-mythos + the auditor |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Critiquing the folk competitor war; running the executable M1–M5 | references/method-upgrade.md |
| The full Sun Tzu + stratagem crosswalk, banned family included, plus the translated middle class | references/stratagem-map.md |
| Planning the SEASON: ledgers, segment map, the Tian Ji allocation table, tempo declarations, the review | references/campaign-protocol.md |
