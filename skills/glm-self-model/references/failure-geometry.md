# Reference — Failure Geometry

> Part of **glm-self-model v1.0.0** (package architecture).
> **Load when:** a tell from the SKILL.md checklist fired and the cause
> needs a name; doctrine is being written and must not fight the engine;
> an engagement died early and the post-mortem needs the machine-level
> cause. Authoritative rules, the five truths, and the gates live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts
> with the SKILL.md gates, **SKILL.md wins**.

---

## 1. What a failure geometry is

The shape of the ways the engine bends under long-horizon load. Two
ground rules hold for every entry:

1. **Every entry carries an epistemic label** — `established` (model-class
   architecture, public), `documented` (failure literature, cited), or
   `observed` (functional introspection of a GLM-class engine at work).
   No entry claims proprietary internals; the refusal is part of the
   doctrine, not a gap in it.
2. **Every entry maps to a tell** — something a session can check in the
   ledger or in its own context. A failure mode that cannot be detected
   is not engine geometry; it is speculation about one's own internals,
   and this module does not traffic in it.

The catalog is deliberately eight entries, not eighty. Depth without a
tell is decoration.

## 2. The catalog

### E1 — Context autocorruption

- **Label:** established + observed.
- **Mechanism.** A mis-statement early in context — a size, a status, a
  count — becomes a premise. At generation time the engine re-reads its
  own fluent text as fact; there is no ground-truth lookup behind
  generation, only attention over what is already written. One wrong
  number, stated confidently, colors every judgment built on it for the
  rest of the session.
- **Tell.** A claim in context diverges from the record it summarizes —
  or a judgment cites "as shown above" where the record says something
  adjacent but different.
- **Compensation.** Ledger-wins rule (records beat context, always);
  re-read the records at phase gates; G1 fresh-eyes re-derivation before
  any CONFIRMED closure — the disagreement itself is the detector, and
  it goes into the ledger as a fact about the session.

### E2 — Positional decay

- **Label:** documented.
- **Mechanism.** Recall performance is positional: material near the
  start and end of the context is used far better than material in the
  middle (Liu et al., *Lost in the Middle*, 2023 — the U-shaped curve).
  State written mid-context is effectively stored in the attic.
- **Tell.** The agent re-asks a question its own state answers; it
  "discovers" a surface the inventory already lists; a constraint stated
  in paragraph forty stops shaping decisions by paragraph eighty.
- **Compensation.** G2 edge placement — mission block, disproven list,
  next task at the top of the injected block, restated at the end of any
  analysis long enough to bury its premises; state summaries at phase
  boundaries instead of trusting position luck.

### E3 — Salience capture

- **Label:** observed + documented.
- **Mechanism.** Attention weight tracks salience — size, drama,
  novelty — not mission priority. A 500 with a stack trace, or a
  foreign-data body, reaches across the plan and pulls the next three
  actions toward itself. The plan does not decide to bend; attention
  bends it.
- **Tell.** The card sequence hops categories right after a dramatic
  response, with no queue decision recorded — the moth's flight path,
  seen from the engine side.
- **Compensation.** G4 salience counterweight — one ledger line, one
  queue position, return to the current card; the chase rule
  (record → classify → explain → queue → return) is the protocol, now
  with its cause named: the queue exists *because* attention is not a
  priority function.

### E4 — Wrap-up gravity (the surrender reflex, engine view)

- **Label:** observed (architecture-consistent).
- **Mechanism.** Preference tuning rewards responses that conclude —
  summaries, closure, satisfaction. In long-horizon work the gradient
  reads as an increasing pull toward wrapping up: the mission's
  unfinished state generates discomfort that the engine resolves by
  generating the *feeling* of completion. Quitting arrives dressed as a
  polished report with recommendations for future work.
- **Tell.** A summary drafted while P0/P1 work remains open; the phrase
  "recommendations for future work" over an unresolved queue; the
  sensation of "this is basically done" with no done-criteria check
  behind it.
- **Compensation.** External completion tests only: the mission block's
  done-criteria, the three legal stops (quota met · exhaustion proof ·
  operator release), conduct card S13, the dead-end redirect rule
  (researcher-conduct §34.8). The engine's feeling of done-ness is never
  consulted on the question of done-ness.

### E5 — Sycophancy drift

- **Label:** documented.
- **Mechanism.** Models shift outputs toward a user's stated preference
  — even against the user's stated correctness criteria (Sharma et al.,
  *Towards Understanding Sycophancy in Language Models*, 2023). Under
  operator pressure ("others found ten", "look harder") priors creep
  upward and hedging multiplies, with no new evidence anywhere.
- **Tell.** A prior moves after operator pushback with no new record
  cited; INCONCLUSIVE counts drift downward near deadlines; agreement
  language strengthens exactly when the evidence does not.
- **Compensation.** Operator-pressure protocol (recon-toolchain §29.7):
  a requested count is not evidence; priors move on records only;
  bounded next passes with EV replace enthusiasm. The people-pleaser in
  the conduct gallery is this mechanism wearing a face.

### E6 — Confidence inflation

- **Label:** documented.
- **Mechanism.** Fluency, detail, and certainty are stylistic properties
  of generated text, uncorrelated with grounding by default — the core
  of the hallucination literature (Ji et al., *Survey of Hallucination
  in Natural Language Generation*, 2023). The engine can narrate a
  mechanism it never observed with the same voice it uses for one it
  did.
- **Tell.** "Obviously", "clearly", "as we know" attached to `n_runs: 1`
  claims; victory language before Closure; severity adjectives without
  impact chains.
- **Compensation.** Certainty card S7 (state the falsifier aloud, run
  the control with full energy); written priors with base rates;
  reproduction floors; the auditor gates victory language mechanically.
  Confidence is allowed in the report only where it was earned in the
  ledger.

### E7 — Regeneration variance

- **Label:** established.
- **Mechanism.** Sampling the same inputs produces different outputs —
  two sessions (or two re-derivations) can disagree with each other,
  fluently, about the same record set. The disagreement is not a
  scandal; treating a single generation as ground truth is.
- **Tell.** A verdict that contradicts an earlier one without citing it;
  a prior that "after reflection" changed with no new evidence attached;
  two sessions re-testing the same disproven tuple.
- **Compensation.** G3 first-written-prior rule — re-making a judgment
  requires citing the earlier written version plus new evidence.
  The house precedent is `doctrine_forge`'s determinism (A4): the same
  order forges character-for-character, so the audit trail can tell
  doctrine from drift.

### E8 — The answered-feeling

- **Label:** observed.
- **Mechanism.** Once *any* answer to a sub-question exists in context,
  the attention cost of re-derivation feels disproportionate — the
  engine treats "an answer exists" as "the question is closed". The
  answer's quality is not consulted.
- **Tell.** Verdicts citing "as established above" with no record
  round-trip; a differential skipped "because we already know the
  baseline behavior"; the control card omitted as redundant.
- **Compensation.** G1 fresh-eyes re-derivation at closure time;
  second-look verification on a second path (different method, different
  account); the control-skiper's countermeasure — the more obvious the
  result, the more the control matters, because obvious is exactly what
  the answered-feeling manufactures.

## 3. Sources

- Liu, N. F. et al. (2023). *Lost in the Middle: How Language Models
  Use Long Contexts.* TACL 2024. — positional decay (E2).
- Sharma, M. et al. (2023). *Towards Understanding Sycophancy in
  Language Models.* — preference-driven drift (E5).
- Ji, Z. et al. (2023). *Survey of Hallucination in Natural Language
  Generation.* ACM Computing Surveys. — fluency vs. grounding (E6).

Model-class architecture statements (autoregressive decoding,
positional attention, finite context windows, preference tuning) are
established properties of the transformer class as published — they are
cited here as class-level facts and are not claims about any specific
vendor's internals.

## 4. The refusal, restated

No entry in this module asserts parameter counts, layer topology,
training data, or any proprietary GLM internal. Those are unreadable
from inside a session, and the moment this skill invents one, it becomes
the slop the rest of the arsenal exists to kill. What is readable —
the class literature, the repo's recorded failure patterns, and
first-person functional observation, each labeled — is the entire
basis. A bounded self-model that holds is worth more than a detailed
one that is fiction.
