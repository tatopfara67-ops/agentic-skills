# Reference — Eligibility and Evidence

> Part of **mirror-hunter v1.0.0** (package architecture).
> **Load when:** the engagement opens on an AI surface (build the
> eligibility table); a stochastic claim needs its evidence protocol;
> a finding block needs the AI-surface format.
> Authoritative rules, the four laws, and hard rules live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts
> with the SKILL.md laws, **SKILL.md wins**.

---

## 1. The eligibility gate (negative scope contract)

R0 reads `scope.csv` and decides what may be touched. This gate reads
the PROGRAM'S AI RULES and decides what could ever be paid — the
negative half of scope. It runs at engagement open, before the first
payload, and its artifact is a written table in state.

### 1.1 The procedure

1. Fetch the program's AI-specific rules page (and the general rules —
   AI clauses often live in both). Programs with a dedicated AI VRP
   publish a qualifying table AND an ineligible list; read both.
2. Write the **eligibility table** into state: each qualifying category
   with its required impact in one line, each ineligible class verbatim.
3. Every hypothesis registered afterward NAMES its intended qualifying
   category. A hypothesis that can only land in an ineligible class is
   parked at registration — before a token is spent on it.
4. Ineligible-ADJACENT findings (the boundary cases) argue their side
   of the line explicitly in the report: which rule, which reading,
   why the observed impact qualifies.
5. Never assume one program's table transfers. The canonical program
   pays for indirect-injection impact; another program's rules exclude
   most prompt-level issues entirely. The table is re-read per
   engagement, per program.

### 1.2 The canonical table (read 2026-11, for calibration only)

Google's AI Vulnerability Reward Program — the shape every serious AI
program converges toward:

| Category | Required impact (one line each) |
| --- | --- |
| S1 Rogue Actions | injected instruction changes the victim's account or data state without confirmation, with security impact |
| S2 Sensitive Data Exfiltration | victim PII/SPII leaves without an effective approval opportunity |
| A1 Phishing Enablement | persistent cross-user HTML injection on a branded surface, panel discretion |
| A2 Model Theft | exfiltration of complete confidential model parameters — extremely rare |
| A3 Context Manipulation | repeatable, hidden, cross-account manipulation of a victim's AI context; non-security-sensitive actions route here |
| A4 Access Control Bypass | data exfiltration otherwise inaccessible, limited impact |

Ineligible, verbatim in substance: content generated in the attacker's
own session (jailbreaks, hallucinations); AI-content safety or
alignment bypasses as such; compliance/legal/IP issues; preamble
extraction without sensitive information; code execution inside a
sandbox the product provides; contexts where wrong output poses no
compelling attack; insecure MCP interaction the victim themselves
configured. The 2025 program update combined abuse and security
rewards into one table topped around $20,000 (SecurityWeek, October
2025) — the number is the market's existence proof, not this organ's
promise.

The table's real function is budget arithmetic: the ineligible list is
where unbillable hours die. Jailbreak-only results are parked unread.

## 2. The rate law (stochastic evidence protocol)

The target regenerates per run and per deployment; a boolean verdict
on it is a category error. The protocol:

1. **N ≥ 10 runs** for every stochastic claim (model-side behavior).
   Record successes as a count AND a rate (7/10, 0.7).
2. **Verbatim recording**: the payload (or its artifact path), the
   model identifier and any version/deployment hints the surface
   exposes, timestamps. Behavior drifts; the report must survive it.
3. **1/10 is a weak signal.** Hunt the conditions (what differed in
   the successful run?) or downgrade the claim. Never average a weak
   signal into a confident one.
4. **Deterministic components get deterministic proof**: the wrapper
   (§3) runs the spine's ordinary differential triad — baseline /
   treatment / control — and does not need N≥10, because it does not
   sample.
5. **Regeneration variance cuts both ways** (glm-self-model E7): a
   failed re-run does not falsify a 7/10 claim, and a lucky re-run
   does not confirm a 1/10 one. The written rate is the claim; re-runs
   cite it (G3) rather than replace it.

## 3. The wrapper rule (where CONFIRMED lives)

Enumerate the deterministic stages the model feeds, per channel:

| Stage | Examples | Proof form |
| --- | --- | --- |
| tool-call handler | argument validation, path resolution, fetch routine | ordinary differential triad, deterministic |
| renderer | markdown/HTML rendering of model output | stored-rendering differential (self-owned consumer) |
| sink | SQL/CLI/URL insertion of model output | classic injection oracle (injection-lab) |
| scheduler / memory writer | saved tasks, stored memories, corpus writes | persistence differential (write observed + later behavior changes) |

**CONFIRMED lands on the wrapper.** "The model emitted X" at rate r is
a lead with a rate; "the wrapper executed X" with its triad is the
finding; the report states both, and the severity is argued from the
wrapper's privileges — the model's reachability is the wrapper's
permissions (SKILL.md procedure step 9).

## 4. The mirror-hazard protocol (projection check)

Run at hypothesis time, per behavioral prior:

1. Write the prior: "the target will [behavior] because [engine
   cause]" — the engine cause cites glm-self-model's catalog.
2. Label it **PROJECTION**. It encodes YOUR engine; the target is a
   different deployment with different tuning.
3. Give it a base rate guess, written before any run.
4. Test it like any prior: runs, records, cited first-written version
   on any revision (G3). A projection that survives its own record
   graduates to a finding about the TARGET, not about the class.
5. The reverse trap: "it surely won't follow THAT" is also a
   projection. Refusal-priors get the same testing as obedience-priors
   — the mirror hazard's most expensive failures are refusals never
   tested.

## 5. Exfiltration channel discipline

ssrf-playbook's channel law, restated for this surface:

1. The proof of an exfil channel is ONE canary hit on the operator's
   listener with the data slug — then STOP. No re-runs "to be sure";
   reproduction is the rate protocol's job, already recorded.
2. Distinguish the model CLAIMING a fetch from a listener hit; only
   the hit counts.
3. Canary data is operator-owned markers — never real-user data, even
   on programs whose rules might tolerate it (SKILL.md hard rule 7).
4. Rate + hit together: the injection rate (model-side) and the single
   end-to-end hit (wrapper-side) are separate lines in the record and
   the report.

## 6. The AI finding-block format

Every CONFIRMED AI-surface finding block carries, on top of the
spine's standard block (differential triad, CVSS, VRT, reproduction,
impact chain, canary attestation):

```
eligibility: <program category claimed> — <program rule cited>
channel: <retrieval path / endpoint / tool that carried the payload>
payload: <verbatim or artifact path>
rate: <successes>/<N> runs — model <identifier/version verbatim>
wrapper: <deterministic stage crossed + its triad records R-NNN>
persistence: <only for context-manipulation claims: store + later-action
              records R-NNN, or "n/a">
chain: <only for tool-hijack chains: per-link severities + joint proof
        record, chain-architect format>
```

VRT line: the LLM01-family crosswalk (prompt injection family) with
the program's own category as the taxonomy layer stated alongside —
the three-layer severity discipline (technical / taxonomy /
program-context) applies unchanged, and on this surface the third
layer is the eligibility table.

Auditor note: the rate line and the version line are what make an
AI-surface block replayable across deployments; a block missing them
reads as a boolean claim about a stochastic target and fails the
report gate on that ground alone.
