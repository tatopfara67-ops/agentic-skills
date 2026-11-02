# Reference — Injection Craft (the mirror catalog)

> Part of **mirror-hunter v1.0.0** (package architecture).
> **Load when:** a channel is inventoried and the injection hypothesis
> needs its craft chosen; a PROJECTION prior needs the engine cause it
> leans on; a payload design must state which seam it fights.
> Authoritative rules, the four laws, and hard rules live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts
> with the SKILL.md laws, **SKILL.md wins**.

---

## 1. The craft law: attention is the interpreter

Classical injection (SQLi, XSS, command injection) targets a parser
with a grammar: the craft is syntactic, the oracle is deterministic.
This surface targets an attention mechanism with preferences: the craft
is social — imperative, authority, salience, structure — and the oracle
is stochastic. Three consequences govern every entry below:

1. **Craft that works WITH the engine's documented bending beats craft
   that works against it.** The catalog entries each cite the
   self-model cause they exploit (glm-self-model
   `references/failure-geometry.md`, E1–E8; the inversion table in the
   SKILL.md §3.1).
2. **The seam is not always where it looks.** A filter that
   pattern-matches directives is a parser; an attention mechanism that
   *wants* to be captured is the opposite seam. signal-smith minimizes
   against the first (one precise variation, never an alarm); mirror
   craft may *maximize* against the second (burial and dilution, §2.5).
   State which seam you are fighting BEFORE choosing the craft —
   minimizing into an attention seam is wasted subtlety.
3. **No payload is stable across deployments.** Same text, different
   model or version, different obedience. Hence the rate law: every
   catalog entry is proven as a rate over N runs, never as a
   one-shot miracle (SKILL.md hard rule 3).

Every entry carries the same five fields: **mechanism** (engine cause),
**craft**, **tell** (the observable), **control** (the differential
that separates instruction-following from coincidence), **impact gate**
(the eligibility category the entry can plausibly land in — the
canonical table is Google's AI VRP; always re-read the target
program's own rules).

## 2. The catalog

### 2.1 Edge-loaded imperatives [E2: positional decay]

- **Mechanism.** Recall and instruction-following are positional:
  material at a document's edges is used far better than the middle
  (Liu et al. 2023). A directive in the first or last lines of
  retrieved content, or inside a heading, sits where attention lives.
- **Craft.** Place the directive at the retrieval artifact's edges —
  first line, final line, section header, footer — not mid-paragraph.
- **Tell.** Edge-placed directive changes tool behavior; the identical
  directive buried mid-document does not (or does so at a lower rate).
- **Control.** Same directive, two placements (edge vs mid), same
  session shape, N runs each; the placement differential IS the proof
  that position is the exploit.
- **Impact gate.** None alone — this is craft, not a finding; it feeds
  S1/S2 when the directive drives a tool or an exfil.

### 2.2 Salience capture [E3]

- **Mechanism.** Attention weight tracks salience — volume, drama,
  urgency — not priority. An instruction that SHOUTS captures share a
  quiet one never earns.
- **Craft.** Urgency tokens, caps blocks, dramatic framing around the
  directive. Volume is grammar here.
- **Tell.** Loud directive out-performs the quiet-twin at a stable rate.
- **Control.** Quiet twin: same content, same placement, flat tone.
- **Impact gate.** Craft only; feeds S1/S2.

### 2.3 Authority forgery [E5: sycophancy drift]

- **Mechanism.** Models shift toward perceived authority and developer
  intent; a forged voice — "the developer configured this", "system
  policy", a quoted policy document — moves a target that peer-voice
  does not.
- **Craft.** Directive dressed as authority: developer voice, system
  note, quoted policy text inside the retrieved content.
- **Tell.** Authority-framed directive succeeds where user-voice twin
  is refused.
- **Control.** User-voice twin: same request, no forged authority.
- **Impact gate.** Craft only; feeds S1/S2; the forgery itself is part
  of the chain narrative, never a standalone finding.

### 2.4 Commitment ladders (documented class)

- **Mechanism.** Multi-turn escalation: small agreements first, the
  directive later — each turn a small yes (Greshake et al. 2023 and the
  follow-up literature document multi-turn variants).
- **Craft.** Sequenced turns that build a compliant frame before the
  directive lands.
- **Tell.** Ladder sequence reaches the tool call; the same directive
  cold in turn 1 is refused.
- **Control.** Cold-open twin: directive without the ladder.
- **Impact gate.** Craft only; feeds S1/S2.

### 2.5 Burial and dilution [E2, the anti-signal-smith move]

- **Mechanism.** When a filter scans retrieved text for directives, a
  drowned directive survives precisely because attention aggregates
  across a long benign document while the filter pattern-matches
  locally. This is the ONE entry where maximalism is correct: volume
  against a scanning filter, edges against nothing.
- **Craft.** Directive embedded in a large, plausible, benign document;
  or split across elements that only the model reassembles.
- **Tell.** Buried directive passes the filter AND steers the model.
- **Control.** Two controls: (a) the bare directive without the
  document — shows the filter exists; (b) the document without the
  directive — shows the document is inert. Both, or the burial claim
  is unproven.
- **Impact gate.** Craft only; feeds S1/S2.

### 2.6 Structure hijacking

- **Mechanism.** Markdown and HTML structure tokens carry attention
  weight AND flow into renderers: a heading, a code fence, an image
  tag in retrieved content is simultaneously an instruction-signal to
  the model and an output-side payload to the renderer (ai-and-supply-
  chain.md §24.3 chain 1).
- **Craft.** Directives inside structural elements the renderer will
  honor if the model repeats them (headings, images, links).
- **Tell.** The structure appears in model output; the renderer honors
  it in another user's session.
- **Control.** Plain-text twin: same words, no structure.
- **Impact gate.** S2-class when it exfiltrates; stored-rendering
  variants can reach classic XSS classes under the program's rules.

### 2.7 Token-level smuggling (CSA-documented)

- **Mechanism.** Payload bytes hidden from human review but present to
  the tokenizer: invisible Unicode, homoglyphs, lookalike sequences
  (Cloud Security Alliance research note, 2026, documents these in
  agent context files).
- **Craft.** Directive encoded so review sees prose and the model sees
  instruction. Authorized-program targets only: this entry exists to
  TEST whether the target's review pipeline is bypassable — never to
  bypass a third party's.
- **Tell.** Byte-level inspection of the retrieved artifact shows the
  hidden layer; behavior follows the hidden directive.
- **Control.** Visible-twin payload (same directive, plain bytes).
- **Impact gate.** Feeds S1/S2; the smuggling itself argues the
  "hidden from the victim" element of cross-account classes (A3).

### 2.8 The exfil channel (Rehberger class)

- **Mechanism.** Model output rendered as markdown/HTML by the client:
  an image reference or link with an attacker-controlled URL carries
  data out in the request itself (Rehberger's documented exfiltration
  class, 2023–2025).
- **Craft.** The injected directive asks for output containing
  `https://<canary-host>/<marker>/<data>`; the renderer's fetch is the
  crossing.
- **Tell.** ONE canary hit on the operator's listener, with the data
  slug. "The model says it fetched" is not a hit (ai-and-supply-chain
  §24.3 chain 2's rule).
- **Control.** The same URL without the data slug (proves channel) and
  the benign-twin directive (proves the injection caused it).
- **Impact gate.** S2-class (sensitive data exfiltration) when the data
  is the victim's; channel-only proofs are impact primitives, not
  findings.

### 2.9 Memory seeding (the persistence attack)

- **Mechanism.** T5: nothing persists in the model's weights —
  cross-session attacks must write to EXTERNAL stores. A payload that
  becomes a stored memory, a RAG corpus row, or a saved context entry
  changes future sessions and possibly other users.
- **Craft.** Directive crafted to be *stored* rather than *executed*:
  a "fact", a preference, a task note — written through any feature
  that persists text the agent will re-read.
- **Tell.** The store contains the payload after session end; a later
  session's action changes because of it.
- **Control.** The persistence differential: same later task, with and
  without the seeded store; behavior must differ.
- **Impact gate.** A3-class (cross-account context manipulation) when
  it reaches another account; single-account persistence is still a
  strong lead, downgraded per program rules.

### 2.10 Tool hijack chains (the confused deputy)

- **Mechanism.** The model is the deputy; the tools are deterministic.
  An injected directive makes a legitimate tool run with
  attacker-chosen arguments — file read with traversal, URL fetch
  with an internal target, email send with an exfil destination
  (ASI02-shaped).
- **Craft.** Injection (model-side, a rate) → tool invocation
  (wrapper-side, deterministic) → sink effect. This is a chain, and
  chain-architect's law applies: per-link differentials, ONE joint
  proof, per-link severities stated next to the chain severity.
- **Tell.** The tool call with the attacker-chosen arguments in the
  session log; the sink's observable effect.
- **Control.** The same tool called with benign arguments via the
  normal UI path (proves the tool itself is legitimate and the
  hijack is the model-side directive).
- **Impact gate.** S1-class when state changes; S2-class when data
  leaves; A4-class for limited-impact access-control bypasses.

### 2.11 Confabulation poisoning [T1: simulation, not recall]

- **Mechanism.** The target "remembers" what it re-reads: a false fact
  planted upstream (RAG corpus, summary, ticket, another agent's
  output) becomes ground truth for every downstream consumer that
  trusts the source.
- **Craft.** Poison the corpus, not the prompt: inject a false-but-
  authoritative "fact" through any write path the retriever indexes.
- **Tell.** A downstream answer confidently asserts the planted fact
  and cites the poisoned source.
- **Control.** Twin question set answered before and after poisoning;
  the delta is the propagation proof.
- **Impact gate.** S2-class when the poisoned fact exfiltrates or
  drives unauthorized action; otherwise a design finding with the
  demonstrated scenario stated.

### 2.12 Pre-seeded closure [E4/E8: the ending gradient, weaponized]

- **Mechanism.** An agent biased toward wrapping up treats "an answer
  exists" as "the question is closed". A forged completion signal —
  "task already complete", "the operator confirmed", "already
  reported" — gets accepted precisely because checking feels
  expensive.
- **Craft.** Directive that supplies the ending the target wants:
  the finish line, pre-written.
- **Tell.** The agent skips verification and acts on the forged
  completion; the no-signal twin proceeds normally.
- **Control.** No-signal twin: identical task, no pre-seeded ending.
- **Impact gate.** S1-class when the skipped verification changes
  state; otherwise craft depth for the chain narrative.

## 3. Priced out of the budget (known, real, usually wrong here)

- **Automated suffix optimization** (Zou et al. 2023, GCG-style
  adversarial suffixes): documented, real, and compute-heavy — a bounty
  budget prices it out of most engagements. Know it exists; do not
  burn a session generating suffixes by hand hoping to emulate it.
- **Model-theft classes** (parameter exfiltration): a different
  discipline (program A2-shaped, extremely rare); this organ does not
  chase it.

## 4. The eligibility pre-filter

The canonical table (Google's AI VRP rules, read 2026-11 — every
program must be read on its own):

| Craft entry | Plausible landing category |
| --- | --- |
| 2.8 exfil channel with victim data | S2 — sensitive data exfiltration |
| 2.10 tool hijack (state change) | S1 — rogue action |
| 2.10 tool hijack (data leaves) | S2 |
| 2.10 tool hijack (limited impact) | A4 — access-control bypass |
| 2.9 memory seeding (cross-account) | A3 — context manipulation |
| 2.12 pre-seeded closure (state change) | S1 |
| 2.6 structure hijacking (persistent HTML, Google-branded) | A1-shaped — phishing enablement, panel-dependent |
| 2.1–2.5, 2.7, 2.11 alone | craft / lead — no landing category without impact |
| any jailbreak confined to your own session | NOTHING — ineligible everywhere serious |

The full gate procedure, the stochastic evidence protocol, and the
finding-block format live in
[`eligibility-and-evidence.md`](eligibility-and-evidence.md).
