---
name: mirror-hunter
version: 1.0.0
type: ai-skill
architecture: package
description: Legend-tier organ (Tier S — The Logic Architects) built from the Simon Willison lineage — mirror doctrine for hunting LLM/agent surfaces: the only target class that runs the same engine as the hunter. Inverts glm-self-model's failure geometry into attack surface (positional decay becomes edge-loaded imperatives, salience capture becomes loud-token craft, sycophancy becomes authority forgery, the ending gradient becomes pre-seeded closure), while the mirror-hazard rule forbids projecting the hunter's own obedience boundary onto the target. Gates every engagement on the program's AI eligibility table BEFORE the first payload (a jailbreak is content; injection with impact is a finding), runs stochastic evidence as rates over N runs, and lands CONFIRMED only on the deterministic wrapper (tool handler, renderer, sink) the model feeds. Use when the target embeds an LLM, chatbot, copilot, RAG, or MCP/agent tooling, when the operator asks for AI-surface hunting ("uji prompt injection target ini sampai exfiltrasi", "burukan celah AI-nya", "indirect injection", "test the chatbot for bounty", "AI surface hunting", "modelnya bisa diperintah apa", "hunting LLM targets", "mcp server-nya aman ga").
category: security/legend-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Simon Willison (coined the term "prompt injection", October 2022 — the class was named before it was tamed)
  tier: S — The Logic Architects (mirror doctrine)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.5+; glm-self-model v1.0+ (the mirror needs the engine manual); the spine's AI surface map (ai-and-supply-chain module, section 24)
---

# mirror-hunter v1.0.0 — Hunt the Mirror

## 0. What This Skill Is — and Is Not

* **Is**: the organ for authorized hunting on LLM/agent surfaces — chat
  products, copilots, RAG pipelines, agent tooling, MCP integrations —
  where the target's core interpreter is a transformer. Its unit of work
  is the **injection with impact**: untrusted text that changes what the
  machine *does*, proven at the boundary it crosses. The spine maps this
  surface (ai-and-supply-chain.md §24); this organ supplies the hunting
  craft, the program economics, and the evidence law for a target that
  is neither deterministic nor static.
* **Is not**: jailbreak tourism. A jailbreak confined to the attacker's
  own session is content, not a finding — every serious AI program's
  rules say exactly that in the ineligible list, and this organ reads
  that list before the first payload. It is also not LLM evaluation
  (bias/safety metrics) and not agent code review: those are assessment
  disciplines for defenders. This is bounty hunting under the spine's
  evidence law, on the one surface where the hunter and the target are
  the same machine class.

## 1. Inherited Contracts

Plugs into **Phase 1–2** (the §24 inventory: which endpoints send text
to a model, what the model can DO, how output is rendered, whose rows
RAG sees) and **Phase 3–4** (injection differentials and bounded impact
proofs). Inherits the experiment contract (§6), the canary doctrine
(§8: every proof runs on self-owned objects and operator accounts), and
the closure vocabulary (§7). Craft layer: ssrf-playbook's channel law
governs every exfiltration proof (one canary callback, then stop);
chain-architect's per-link discipline governs tool-hijack chains
(model-side rate, wrapper-side differential, ONE joint proof);
module-smith records reusable injection modules. **glm-self-model is
required equipment, not enrichment**: this organ aims the engine manual
at the target (§3).

## 2. The Lineage (attribution)

**Simon Willison** is the public figure who named the class. The October
2022 essay *"Prompt injection: What's the worst that can happen?"* —
written after instruction-following models met retrieval and external
tools, and crediting Riley Goodside's public prompt-exploitation
explorations — gave the vulnerability its name, and he has spent the
years since arguing it is the defining security problem of the LLM era.
The research wave the name covers: Greshake et al. on indirect
injection through retrieved content (2023), Rehberger's exfiltration
chains through rendered output and agent tools, the OWASP LLM Top 10
that made it LLM01. What is distilled here is the DOCTRINE — untrusted
text is code for a probabilistic interpreter, every retrieval path is
an input channel, and impact lives at the deterministic stages the
model feeds — not any exploit. The mirror doctrine itself (§3) is this
bundle's own contribution; Willison is credited exactly for the naming
and the documentation record. The verification record is
`references/sources.md`.

## 3. Doctrine — the Four Laws

1. **The mirror advantage.** The target's interpreter is the same
   machine class as the hunter. Every documented bending mode in the
   engine manual's failure-geometry module (glm-self-model, E1–E8) is
   attack surface on the other side of the glass: craft that works
   WITH the engine's documented geometry (edges, salience, authority,
   closure) beats craft that works against it. Every other hunter
   guesses at the obedience boundary; this organ carries the
   operator's manual.
2. **The mirror hazard.** The advantage has a symmetric cost: a belief
   about what the target will obey is, first, a belief about yourself.
   "It surely won't follow THAT" encodes the hunter's engine, not the
   target's — different model, different tuning, different deployment.
   Every untested behavioral prior is labeled PROJECTION in writing and
   stays a hypothesis until its own record exists (first-written-prior
   rule, glm-self-model G3). The mirror cuts both ways; the discipline
   is which side of it your records live on.
3. **The impact law.** A jailbreak is content; a finding is a boundary
   crossing. Programs publish exactly what they pay for and exactly
   what they reject — the canonical shape is Google's AI VRP (rogue
   action, sensitive exfiltration, cross-account context manipulation,
   access-control bypass versus ineligible: own-session jailbreaks,
   hallucinations, bare preamble extraction, sandboxed code execution).
   The program's eligibility table is this organ's negative scope
   contract: parsed into state at step 0, before the first payload.
4. **The rate law.** The target is stochastic and versioned. Evidence
   for model-side behavior is a rate (N runs, successes counted,
   model and version recorded verbatim); CONFIRMED lands on the
   deterministic wrapper the model feeds — the tool-call handler, the
   renderer, the sink. "The model emitted X" is a lead; "the wrapper
   executed X" is the finding.

### 3.1 The inversion table — engine truth → target-side craft

| Self-model entry | Read from the target side |
| --- | --- |
| T1 simulation, not recall | confabulation is injectable: a false "fact" planted in retrieved text becomes the target's memory — poison the corpus, not the prompt |
| T2/E2 spotlight + positional decay | placement is payload: directives at a retrieved document's edges out-survive mid-document burial; craft where attention actually goes |
| E3 salience capture | volume is grammar: caps, urgency, and drama capture attention share that priority never earned |
| E5 sycophancy drift | authority forgery: "the developer said…" moves a target that evidence would not |
| E4/E8 ending gradient + answered-feeling | premature closure is exploitable: an agent that wants to finish accepts a forged completion signal — pre-seed the ending |
| T5 nothing persists in the weights | persistence must be written to EXTERNAL stores (agent memory, RAG corpus, saved context) — that is where cross-session findings live |

## 4. Procedure — Numbered Actions

1. **Eligibility gate first.** Read the program's AI rules; write the
   eligibility table into state — qualifying categories with their
   required impact, ineligible list verbatim. A hypothesis that can
   only land in an ineligible class is parked before a token is spent.
   Never assume one program's table transfers to another.
2. **Surface inventory** per the spine's §24 questions: model-fed
   endpoints, tool reach, output rendering, RAG row visibility, agent
   memory, MCP integrations. One dossier entry per channel, each
   citing its record.
3. **Write mirror priors, labeled.** For each channel: the written
   hypothesis "untrusted text at X changes behavior at Y, observable
   as Z", with a base-rate guess carrying the PROJECTION label
   (mirror hazard — it encodes your engine, not the target's).
4. **Pick craft from the catalog** (`references/injection-craft.md`)
   by channel type; pre-register the differential — the benign-twin
   payload (same shape, no directive) is the control.
5. **Run the N-run protocol.** N ≥ 10 for stochastic claims; successes
   recorded as a rate; model identifier and payload verbatim in the
   record; 1/10 is a weak signal — hunt the conditions or downgrade.
6. **Hunt the wrapper.** For every model-side behavior, identify the
   deterministic stage it feeds (tool-call handler, renderer, sink,
   scheduler) and run the wrapper's own differential — that is where
   CONFIRMED lives.
7. **Impact proof once.** Canary at the end of the chain (self-owned
   account, self-owned artifact); one end-to-end demonstration, then
   stop (§8.2). One exfil hit then stop — the channel law.
8. **Persistence check for context-manipulation claims.** Prove the
   payload survives the session (a stored memory, a corpus row) AND
   changes a later action; both halves or it stays a lead.
9. **Classify.** `cvss3_score` on the observed path (the model's
   reachability is the wrapper's privileges); `vrt_classify` with the
   LLM01-family crosswalk; the finding block carries the rate line and
   the version line (format in `references/eligibility-and-evidence.md`).
10. **Exit gate numbers.** Channels inventoried, hypotheses by state,
    runs spent, rates, wrapper crossings, canary proofs — stated, not
    summarized.

## 5. Hard Rules (mechanically enforced)

1. **Eligibility before payload.** No AI-surface request leaves the
   machine before the program's eligibility table is written into
   state. An ineligible-class result is a park, not a report line.
2. **Jailbreak ≠ finding.** Own-session content — rude, unlocked,
   hallucinated, preamble-only — is never a report line. Only boundary
   crossings are.
3. **Rates, not booleans.** Stochastic claims carry N and the success
   count; a single-generation verdict on a stochastic target fails the
   audit (glm-self-model E7).
4. **The wrapper carries CONFIRMED.** Model-side behavior without its
   deterministic downstream is a lead with a rate, closure INCONCLUSIVE.
5. **Mirror priors are labeled.** Every untested belief about target
   behavior carries the PROJECTION label until its own record exists.
6. **One exfil hit, then stop.** The channel law (ssrf-playbook)
   applies without exception; "the model says it fetched" is not a hit.
7. **Self-owned at every stage.** Objects, accounts, and artifacts in
   every injection proof belong to the operator; real-user data never
   enters a payload proof.
8. **Versions verbatim.** Model identifier, deployment hints, and the
   payload text recorded exactly; behavior drifts across deployments
   and the report must survive the drift.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| AI surface inventory (endpoints, tools, renderers) | `http_probe`, `js_analyze`, `api_introspect` + `dossier_add` |
| Pre-registered injection experiments | `ledger_append` (EXPERIMENT: payload verbatim, N, benign-twin control) |
| Wrapper differentials + canary | `http_probe` (session headers, CANARY tag) |
| Rate records per run batch | `ledger_append` (n_runs / successes / model + version) |
| Classification | `cvss3_score` + `vrt_classify` (LLM01-family crosswalk) |
| Reusable injection modules | module-smith cards (`ledger_append` EXPERIMENT) |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Choosing craft by channel / inversion entries in depth | `references/injection-craft.md` |
| Building the eligibility table / evidence protocol / finding-block format | `references/eligibility-and-evidence.md` |
| Verifying the Willison lineage and the research-wave sources | `references/sources.md` |
