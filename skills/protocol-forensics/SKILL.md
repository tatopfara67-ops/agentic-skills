---
name: protocol-forensics
version: 1.1.0
type: ai-skill
architecture: package
description: >-
  Craft-lineage organ forged from Dan Kaminsky (IOActive director of
  penetration testing, later White Ops chief scientist; the 2008 DNS
  cache-poisoning disclosure, VU#800113) — protocol forensics at internet
  scale. Treats a specification as a treaty between strangers: every
  implementation of one RFC class resolves the spec's ambiguities
  independently, so the hunting unit is the class-times-population, never one
  product. The organ ships with its method layer born in (A16): a mechanical
  critique of the published Kaminsky art — the hunt itself told as story with
  no replayable procedure, the entropy arithmetic scattered across talks and
  advisories instead of one decision table, the vendor census executed through
  personal trust networks rather than a reproducible matrix, post-patch
  deployment tracked by anecdote, and humor compressing the executable steps
  out of the talks — and the replacement protocol M1–M6: the population census
  with its boundary argument against desync-hunter and scan-economist, the
  invariant audit with computed collision arithmetic (worked from the recorded
  VU#800113 constants — 16-bit transaction ID, 32,768 average blind attempts,
  ~16 additional bits of source-port entropy — and the birthday structures
  computed on record), the disagreement-matrix differential probes, the impact
  ladder with a measured denominator, the coordinated-disclosure engineering
  (vendor matrix, embargo, simultaneous patch day), and post-patch
  verification with a measured saturation gate plus a residual-risk register
  that labels every stopgap a stopgap. Use when a protocol-level or spec-level
  weakness is suspected or must be argued; when one RFC class must be hunted
  across its implementation population; when entropy or collision arithmetic
  must price an invariant; when a finding's blast radius needs a measured
  denominator; or when disclosure must be engineered as a coordinated
  multi-vendor event ("protocol forensics", "spec-level bug", "systemic
  weakness across implementations", "invariant audit", "coordinated
  disclosure", "the Kaminsky move", "kelemahan level spesifikasi", "bedah
  protokol kelas RFC", "diferensial antar implementasi", "populasi
  implementasi").
category: security/craft-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Dan Kaminsky (1979-2021) — the 2008 DNS cache-poisoning disclosure (VU#800113, the July 8 patch day, Black Hat 2008), the Black Ops talk series 2001-2016, Paketto Keiretsu (2002), the Sony rootkit census (2005), the DNSSEC root key-holder role (2010); first candidate-queue execution of the lineage-smith forge
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; skill-mythos charter v1.11+
---

# protocol-forensics v1.1.0 — The Kaminsky Lineage

## 0. What This Skill Is — and Is Not

* **Is**: the organ that hunts **the specification's ambiguity across
  the entire implementation population** — the class-level flaw. DNS
  2008 was one ambiguity (insufficient entropy in the
  transaction-ID-plus-port match between query and reply) resolved
  differently by every resolver on earth, so the finding was not "a
  BIND bug" but "nearly every implementation of one RFC class fails
  the same invariant" — and the fix was engineered as an
  industry-wide simultaneous event. This organ turns that shape into
  a numbered procedure: census the population, audit the spec's
  implicit invariants, price each invariant with computed arithmetic,
  probe for disagreement, ladder the impact with a measured
  denominator, engineer the disclosure, and verify the patch's
  deployment as a measurement.
* **Is not**: a per-product bug hunter (that is every other organ's
  default posture), and not a parser-seam hunter — a disagreement
  between two parsers on ONE request path is desync-hunter's ground
  (Kettle lineage); this organ's ground is the disagreement between
  IMPLEMENTATIONS of one specification class, where the unit of work
  is the class, not the request.

## 1. The Lineage (attribution)

Dan Kaminsky (February 7, 1979 – April 23, 2021), director of
penetration testing at IOActive, later co-founder and chief scientist
of White Ops (Human Security). The documented corpus: the Black Ops
talk series (Black Hat/DEF CON, 2001–2016 — from "Gateway
Cryptography" through "Black Ops of TCP/IP 2011"); the Paketto
Keiretsu tools (2002); the Sony rootkit population census (568,000+
machines, 2005); the 2008 DNS cache-poisoning disclosure — discovered
early 2008, coordinated in secret with vendors and DHS, patched
simultaneously on July 8, 2008 (CERT VU#800113), leaked July 21,
fully revealed at Black Hat 2008 ("It's The End Of The Cache As We
Know It"); the X.509 structural research with Meredith Patterson and
Len Sassaman (2009); the Conficker detection work (2009); Interpolique
(2010); and the DNSSEC root Trusted Community Representative role
(named by ICANN June 16, 2010). His own stated specialty, in his own
talk abstracts: "design-level fault analysis, particularly against
large-scale systems." Nothing here is his code; this is his decision
logic, re-expressed as engagement rules. Sources and the read
ledger: references/sources.md — the verification record.

## 2. The Five Laws of Protocol Forensics

1. **The spec is a treaty between strangers.** A specification is
   what independent implementers agreed to READ, not what they
   actually BUILT; every underspecified corner is resolved
   independently by each implementation. The bug class lives in the
   gap — so the target is the class × population, and "works on my
   resolver" is a category error. Kaminsky's own words on record:
   every functioning system has the abstraction outsiders are led to
   believe and the reality insiders operate — "you eventually
   unlearn its necessary lies" (2018).
2. **Entropy is arithmetic, not vibes.** An invariant's strength is
   a number: bits of unpredictability, collision probability at a
   stated packet budget, computed BEFORE any claim. The 2008 record:
   16-bit transaction ID → 32,768 average blind attempts; source-port
   randomization buys ~16 more bits; birthday structures multiply
   odds by outstanding-query count. Numbers first, narrative second.
3. **The population is the finding's denominator.** "Half a million
   machines" (Sony, 2005) and "nearly all vendors" (VU#800113's
   vendor list) are MEASUREMENTS, not adjectives. An impact claim
   about a class without a counted denominator is a lead, never a
   finding.
4. **The fix is an engineered event.** Coordinated disclosure at
   this scale is infrastructure: a vendor matrix, an embargo, a
   single simultaneous patch day (July 8, 2008), an advisory
   registration (VU#800113) — engineered months in advance, not
   announced when convenient. A class-level fix that drips vendor by
   vendor re-opens the window it was supposed to close.
5. **The patch is a stopgap until the structural fix lands.** Port
   randomization raised the cost of the 2008 race from trivial to
   expensive; DNSSEC removed the trust assumption. The record says
   the stopgap's limits out loud, tracks residual risk with dates,
   and never lets a partial fix be reported as closure.

## 2.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published Kaminsky art where it was mechanically weak —
the hunt narrated as story with no replayable search procedure, the
entropy math scattered across talks/advisories instead of one
decision table, the vendor census run through personal trust
networks, post-patch deployment tracked by anecdote, and the humor
that compresses executable steps out of the talks (a documented
trade-off: his most information-dense talk drew "fails on delivery"
from a professional reviewer) — and ships the executable
replacement: **M1** the population census (with the desync-hunter and
scan-economist boundary argued on record), **M2** the invariant
audit with computed collision arithmetic and threshold tables,
**M3** the disagreement-matrix differential probes, **M4** the impact
ladder with a measured denominator, **M5** the coordinated-disclosure
engineering, **M6** the post-patch verification with a saturation
gate and a residual-risk register.

## 2.6 The Operator Layer (A17) — the Dan Kaminsky runtime

`references/operator-os.md` ships the figure's documented psychology
as the agent's RUNTIME, in four parts: the thinking framework (numbered
if-then decision rules, each citing the documented behavior it
distills), the behavioral protocol (situation → move → agent action →
refusal, with pacing and failure-reaction rules — how the agent acts
and behaves while hunting), the scripting arsenal (the organ's core
techniques as exact, tool-agnostic commands and micro-scripts, each
with its read-out and decision gate), and the rigid run-order binding
rules, behavior, and scripts onto the M-protocol above. Load it when
the hunt runs: the doctrine states the posture, the M-protocol states
the procedure — the operator OS is how the agent BEHAVES while
executing, characteristic of Dan Kaminsky.

## 3. Procedure — Numbered Actions

1. **Name the class.** Write the census header: the RFC class, the
   load-bearing ambiguity suspected, and the boundary row (why this
   is protocol-forensics and not desync-hunter's single-request seam
   or scan-economist's probe budget — one sentence each, on record).
2. **Census the population** (M1): every reachable implementation of
   the class in scope, each pinned by name and version; a population
   under three is a product review, not a class hunt — park and say
   so.
3. **Audit the invariants** (M2): extract the spec's implicit
   invariants — entropy budgets, ordering assumptions, trust
   delegations, encoding rules. For each, compute the attack
   arithmetic from recorded constants (worked DNS example in
   references/protocol-method.md, including the birthday tables) and
   write the threshold: at what computed win probability, within
   what stated packet budget, the invariant is declared broken.
4. **Probe for disagreement** (M3): one minimal probe per invariant,
   one variable per probe, run across the whole population; the
   disagreement matrix (implementation × invariant) is the evidence
   artifact; n_runs ≥ 2 on every cell that matters (A8).
5. **Ladder the impact** (M4): single-implementation degradation →
   class-wide failure → ecosystem trust root; every rung cites its
   denominator — counted or measured, never adjectival.
6. **Engineer the disclosure** (M5): vendor matrix with per-vendor
   status, embargo date, simultaneous release target, advisory
   registration; the report ships as the fix's instrument, not as a
   substitute for it.
7. **Verify the patch as a measurement** (M6): sample the population
   post-patch, measure deployment against the saturation gate or the
   deadline (whichever the engagement states), file the residual-risk
   register with dates, and label the stopgap a stopgap.
8. Every step files its record in the ledger (R-NNN); a census row, a
   computed threshold, or a disagreement cell without its record is
   an anecdote, not a measurement.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Population discovery, version pinning | `dossier_add` + passive recon organs (subdomain-hunter, surface-cartographer) |
| Spec text, RFC sections, prior art | operator-supplied corpus + references/sources.md read ledger |
| Disagreement probes across implementations | `http_probe` / `api_introspect` with the experiment card (n_runs ≥ 2) |
| Entropy / collision arithmetic | computed on record (references/protocol-method.md tables; recompute, never recall) |
| Blast-radius denominators | `dossier_summary` + ledger counts |
| Disclosure drafts, vendor matrix | `dossier_render` + report organs (report gates apply) |

## 5. Hard Rules

1. The class before the product: a finding reported against one
   implementation while the census row for its siblings is unprobed
   is incomplete — the disagreement matrix comes first.
2. No entropy claim without its arithmetic: "weak randomness" is a
   lead; "16 bits → 32,768 average attempts → computed birthday
   table" is a finding.
3. No impact claim without a denominator: "widespread" is refused at
   the report gate; a count or a measured sample is required.
4. The stopgap is named on delivery: every partial fix ships with
   its residual-risk row and the structural fix it deferred.
5. The disclosure timeline is part of the method, not the politics:
   an embargo breaks, the fallback (accelerated reveal, as July 21,
   2008 forced) executes on record.

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Running the full hunt end to end (invariant classes, birthday tables, matrix schema) | references/protocol-method.md |
| Grading the lineage, running M1–M6, holding the thresholds | references/method-upgrade.md |
| Running the hunt — the Dan Kaminsky runtime: thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
| Checking what was actually consulted; the census, read ledger, psych-read evidence | references/sources.md |
