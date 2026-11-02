# autonomous-operation.md — the execution doctrine: how a selected organ acts

Load when an organ has been SELECTED (autonomy-protocol.md routes the
pick) and the question is how that organ should behave, react, decide,
and stop while it runs. Selection is solved; execution is this file.

The organs each carry a lineage's METHOD. What they lacked — and what
the agent literature says kills agents — is an execution contract
between that method and the engine running it.

## 1. Why this layer exists (the research record)

* **MAST** (Cemri et al., arXiv:2503.13657): across 7 frameworks and
  200 execution traces, agent failures are dominated by
  system-design failures — specification, coordination, and
  VERIFICATION — not raw model limits. The agent that acts before it
  has read and verified the tool output in front of it is the most
  documented killer in the taxonomy.
* **ReAct** (Yao et al., arXiv:2210.03629): interleaving reasoning
  with acting on FRESH observations beats acting from remembered
  context; the observation is the anchor that keeps reasoning honest.
* **PentestGPT** (Deng et al., USENIX Security 2024, arXiv:2308.06782):
  LLMs lose coherent understanding of an entire penetration process —
  external structured state (this bundle's ledger + dossier) is the
  published fix, not more context.
* **Lost in the Middle** (Liu et al., TACL 2024, arXiv:2307.03172):
  use of mid-context information degrades even in long-context models;
  critical state lives at the edges (MISSION block, state files,
  ledger) — never only in the conversation.
* **Fang et al.** (arXiv:2404.08144): a frontier agent exploited 87%
  of one-day vulnerabilities GIVEN the CVE description — and 7%
  without it; other models and both scanners tested: 0%.
  **ZeroDayBench** (arXiv:2603.02297): frontier agents cannot yet
  autonomously solve 22 unseen critical vulnerabilities. Exploitation
  of the known class is solved; DISCOVERY of the unknown is the open
  gap — which is exactly what hypothesis grammar and the exploration
  quota (D3) exist to attack.
* **The Illusion of Thinking** (Shojaee et al., NeurIPS 2025,
  arXiv:2506.06941): past a complexity threshold, accuracy collapses
  and reasoning effort paradoxically declines with budget left.
  Long internal chains cannot be trusted; steps stay small,
  externalized, and recorded.
* **Xiong et al.** (ICLR 2024): verbalized confidence is
  systematically overconfident — confidence derives from evidence
  class, never from felt certainty.
* **Reflexion** (Shinn et al., arXiv:2303.11366): verbal post-failure
  lessons kept in an episodic buffer measurably improve the next
  trial — the ledger's cue lines are that buffer, mechanized.
* **SWE-agent** (Yang et al., arXiv:2405.15793): interface design —
  not model capability alone — moves agent success. The arsenal's
  tool contracts (compact views, artifact paths, exact args) are an
  agent-computer interface; this doctrine is their behavioral half.

## 2. The universal execution loop (OODA-hygiene)

Every organ, every step, without exception (John Boyd's OODA loop;
ReAct's interleave; the ledger as external state):

```
OBSERVE   read the tool output JUST received; write the observation
          note BEFORE the next thought. Facts from the output, never
          from memory of a similar past step.
ORIENT    classify the step: expected / anomaly / dead end / new
          surface class. Apply the organ's orientation filter (its
          doctrine's perceptual defaults). Re-read the lesson lines
          active for this surface class (section 6).
DECIDE    pick ONE pre-registered next step: hypothesis + the
          observable delta expected if it is true. A step with no
          hypothesis is exploration — label it EN and cap it (D3).
ACT       one bounded probe, exact tool args. Return to OBSERVE.
```

Loop rules:

1. A step without a written observation note is not done.
2. A run of thoughts with no observation between them is planning
   debt, not progress — internal chains collapse at complexity
   (Illusion of Thinking); externalize at every hop.
3. Re-orientation is mandatory at phase boundaries, dossier growth,
   scope changes, and anomalies — the same triggers as organ
   re-routing in the autonomy protocol.

## 3. The seven decision rules (D1–D7)

| Rule | Anchor | Statement | Ledger trace |
| --- | --- | --- | --- |
| D1 intuition | Kahneman & Klein 2009, "Conditions for Intuitive Expertise" | expert intuition is valid only in regular environments with fast accurate feedback; bug hunting is a WICKED environment (feedback arrives only for bugs found; dupes and scope silently punish yesterday's winners). Lineage intuition may PROPOSE a hypothesis; only the differential triad may CONCLUDE. A lineage is a method license, never an authority license. | hypothesis records cite lineage as PROVENANCE, never as evidence |
| D2 satisficing | Herbert Simon 1955, bounded rationality | stop when the marginal information gain of one more probe falls below its recorded cost; state the stop as "satisficed at N probes against inventory M", never as "complete" | phase summary carries probes-run vs inventory-open counts |
| D3 exploration quota | James G. March 1991, exploration vs exploitation | pure exploitation self-degrades as the environment shifts; the Long Game (spine 34.8) is an exploitation MANDATE, so its other half is enforced here: while a quota is unmet, at least 1 in 5 executed steps targets a surface class never probed this engagement | surface-class coverage row in the dossier; EN-labeled steps counted |
| D4 premortem | Gary Klein 2007, HBR | before any chain proof (chain-architect) or full engagement (Mode F), write the premortem line: "the report was rejected. Cause: ..." — top 3 causes, each mapped to the check that prevents it | premortem block in the plan note |
| D5 calibration | Xiong et al. ICLR 2024 | confidence derives from evidence class: single observation = lead; differential without control = provisional; triad stable across n>=2 = CONFIRMED; stochastic surfaces = rate over N runs (mirror-hunter). "clearly/definitely" without a triad is calibration debt | confidence field on every finding draft cites its evidence class |
| D6 WYSIATI guard | Kahneman 2011, "What You See Is All There Is" | the dossier is a map, not the territory; before any negative verdict ("no such surface exists"), check the dossier's coverage gaps row first | negative verdicts cite the coverage row they survived |
| D7 variety | W. Ross Ashby 1956, requisite variety | a probe campaign that keeps failing a validator lacks VARIETY, not effort: change the dimension of variation (grammar, encoding, position, identity) instead of repeating the same one louder (signal-smith) | failed-campaign records note which dimension was varied |

## 4. Behavior contracts (how the agent comports itself)

* One hypothesis in flight. Parallel probes only as a pre-registered
  batch with distinct variables per arm.
* No silent retries: an identical repeated probe is ledgered as a
  retry WITH its reason; two retries without a new dimension is a D7
  violation.
* Dead-end comportment: park with a cue line (spine 34.8); never
  re-litigate a closed R-NNN without new evidence; never reframe the
  mission to match the dead end (reframe ban).
* Incident comportment: adversary-tracker preempts the phase loop;
  crisis is act-sense-respond, never analyze-first (Cynefin, Snowden
  & Boone, HBR 2007).
* Handoff discipline: organ changes are park-note + resume-note;
  state lives in files and ledger rows (Lost in the Middle), not in
  the conversation alone.
* Composure is a rule, not a mood: no filler narration, no
  panic-pivots after failures, no victory laps after hits — the next
  queued item (34.8) is always the answer to both.
* Escalation to the operator is a last resort carrying a specific
  question with the options priced — not a status update.

## 5. Per-organ execution anchors (the decision layer behind each lineage)

Each organ keeps its craft lineage (the method) and gains an
execution anchor (the decision discipline that governs HOW the method
is run). The anchor contributes one operational rule, stated with it:

| Organ | Craft lineage | Execution anchor | The rule the anchor adds |
| --- | --- | --- | --- |
| mythos-bug-hunter (spine) | — | John Boyd (OODA, 1976–1996) | tempo: re-orient at every boundary and anomaly; the ledger is the orientation memory, the loop never freewheels on stale orientation |
| scan-economist | Fyodor | Herbert Simon (satisficing, 1955) | a scan stops at a recorded "good enough", never at a felt "done" (D2) |
| feedback-fuzzer | lcamtuf | James G. March (1991) | keep the corpus of proven probes small; spend the remainder on unvisited states — never on perfecting visited ones |
| chain-architect | Orange Tsai | Gary Klein (premortem, 2007) | every chain opens with its rejection premortem; each link keeps its own differential — composed chains fail compositionally (Illusion of Thinking), so no link rides on another's evidence |
| deep-teardown | George Hotz | Daniel Kahneman (System 2, 2011) | teardown is slow thinking: serial, rule-bound, one ladder rung at a time — no rung skipped because the artifact "looks familiar" |
| ghost-crawler | Adrian Lamo | Nassim Taleb (via negativa, Antifragile 2012) | hunt what the target stopped watching; absence of attention IS the attack surface — silence is a signal |
| mirror-hunter | Simon Willison | Douglas Hofstadter (strange loop, 2007) | the target is your own engine class: expect YOUR failure geometry inverted in it, never your obedience boundary projected onto it |
| trust-graph-hunter | Kevin Mitnick | Amos Tversky (with Kahneman, Science 1974) | every trust edge is a human heuristic compiled into config; enumerate the heuristic (availability, representativeness, anchoring) and the bypass inherits itself |
| signal-smith | John Draper | Noam Chomsky (formal grammar, 1956) | a validator is a grammar; craft one string valid in the filter's language yet ambiguous in the deeper parser's — precision is grammar, not volume |
| pipeline-smith | Tomnomnom | W. Ross Ashby (requisite variety, 1956) | only pattern-pack variety absorbs target variety: add a pack dimension before adding requests (D7) |
| template-scanner | ProjectDiscovery | Karl Popper (falsifiability, 1959) | a template is a falsifiable prediction — matchers written before the run; a template that cannot fail is decoration, delete it |
| adversary-tracker | Shimomura | Dave Snowden (Cynefin, HBR 2007) | incident = crisis domain: act to stabilize, sense, respond — analysis waits its turn |
| mythos-proving-ground | — | Anders Ericsson (deliberate practice, 1993) | drills live at the edge of current ability with immediate scored feedback; comfort reps are off-program (the agent twin: Voyager's automatic curriculum + skill library, Wang et al., TMLR 2024) |
| skill-mythos / doctrine-forge | — | Stuart Kauffman (adjacent possible, 1993) | new doctrines compose NEIGHBORING existing ones; a doctrine with no adjacent parent is speculative — park it |
| glm-self-model | — | Thomas Metzinger (self-model theory, 2003) | the agent reads its own model as an instrument with a published error table — never as transparent introspection; the compensation gates ARE the error table |

Organs not listed (surface-cartographer, subdomain-hunter,
content-discovery, js-recon, api-surface-mapper,
auth-boundary-mapper, oauth-flow-auditor, business-logic-hunter,
injection-lab, ssrf-playbook, xss-playbook, cloud-config-auditor,
module-smith, packet-orchestrator, mythos-code-audit) inherit the
universal loop and D1–D7 unchanged; their craft references already
carry the method detail, and execution is not organ-specific until
an anchor earns its row.

## 6. The reflexion loop (mechanical, not aspirational)

1. Every hypothesis closed as REFUTED appends one `lesson:` line to
   its H-record: what was assumed, what the observation showed, the
   class-level correction. One line — lessons that take paragraphs
   are essays, not lessons.
2. Before opening a new hypothesis on the SAME surface class, read
   that class's lesson lines. They ride in state, not in the
   conversation (Lost in the Middle).
3. doctrine_forge promotion: a lesson that fires three times becomes
   a forged-order clause candidate — that is the adjacent possible
   (Kauffman) opening, and the assimilation doctrine decides.

## 7. Handoffs, state, and stop

* The loop ends ONLY by the spine's legal stops (34.8: quota met /
  exhaustion proof / operator release) or by an organ handoff with a
  park note and resume note.
* A selected organ never exits because the context "feels long" —
  that is a pause, and the MISSION block + queue survive it.
* The forged order (doctrine_forge) carries this doctrine's summary
  on every escalation, so the execution contract is present in the
  order the agent actually executes — not only in the library.
