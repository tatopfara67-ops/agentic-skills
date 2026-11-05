# bundle-map.md — the Skill Mythos bundle, in full

Load when you need the complete map: what exists, where it lives, and
the load-when trigger for every organ. The charter (`mythos_charter()`)
carries the distilled version; this module is the atlas.

Since charter v1.13.0 (A17 — behavior over biography), every
person-lineage organ also ships `references/operator-os.md` — the
figure's documented psychology as the agent's runtime: thinking rules,
situation-to-action behavior with refusals, the scripting arsenal as
exact commands, and the rigid run-order. Load it when the hunt runs,
not when it is planned. Since charter v1.18.0 the spine itself joins
that contract with its first lineage layer (the Jason Haddix
lineage, v4.6.0): the onboarding path's methodology-preservation
modules — `references/method-upgrade.md`, `references/operator-os.md`,
`references/sources.md` — load at engagement start (the PIN step), at
version bumps, and at newcomer first-runs. Since charter v1.19.1 the
spine's hypothesis rail is executable: `hypothesis_register` /
`hypothesis_close` / `hypothesis_list` in the arsenal server carry the
§5 contract as refusals — no facts, no hypothesis; three closure
states only; retrodiction discarded.

## 1. Architecture — spine + organs + execution hand

```
                ┌──────────────────────────────────────────────┐
                │ mythos-bug-hunter v4.7.0 (spine, own bundle) │
                │ R0–R7 canon · ledger · hypotheses · gates    │
                └───────┬───────────────────────────┬──────────┘
   Phase 1–3 organs     │            evidence       │ incident branch
┌───────────────────────┴───────────────┴───────────┴─────────────┐
│ arsenal/ — MCP server, 30 scope-gated tools, one R-NNN ledger   │
│ auditor/ — PASS/FAIL report gate (recomputes CVSS, validates    │
│            VRT ids against the shipped official taxonomy)       │
│ lab/     — target_app.py + christmas_lab.py (self-owned)        │
│ examples/— worked-engagement/ + adversary-hunt/ (audited PASS)  │
└─────────────────────────────────────────────────────────────────┘
```

The spine stays the discipline layer — every organ inherits its
contracts (R0 scope gate, append-only ledger, hypothesis grammar,
closure gates, R7 budgets) instead of restating them. The charter
(this bundle) sits at tier 0: it routes, it does not hunt.

## 2. The organs, with load-when triggers

| Organ | Tier | Load when… | Essence (philosophy it carries) |
| --- | --- | --- | --- |
| glm-self-model | 0 | session start of any long engagement; drift, déjà-vu, or unearned completion suspected; doctrine design; after an early engagement death | *know the engine* — the least trusted component gets its operator's manual: model-class failure geometry, labeled by epistemic class, every failure with a tell and a gate |
| surface-cartographer | 1 | an engagement opens; the asset graph does not exist yet, or new assets appeared | *map before you move* — an unmapped attack surface makes every later claim weaker |
| subdomain-hunter | 1 | the domain list is younger than the certificate logs | *passive first* — the target's own CT logs answer before the target is ever touched |
| content-discovery | 1 | the map exists but the hidden paths do not; a 404 baseline is cheap | *calibration before claims* — a control request on every walk, so a hit means something |
| js-recon | 1 | JavaScript bundles exist and nobody has read them | *the client confesses* — routes, ghosts of routes, and masked secrets live in shipped code |
| api-surface-mapper | 1 | an API serves the app; specs may lag reality | *spec is a hypothesis* — version diffs and undocumented endpoints are where the truth leaks |
| auth-boundary-mapper | 2 | two or more roles exist | *boundaries are behaviors, not diagrams* — the role×resource matrix comes from probes, not docs |
| oauth-flow-auditor | 2 | any OAuth/OIDC flow is in scope | *every check has a falsifier* — a flow audit that cannot fail is theater |
| business-logic-hunter | 2 | money, state, or permissions change hands in multi-step flows | *the rules between the rules* — abuse the workflow, not the syntax |
| injection-lab | 3 | an interpreter sits behind an input | *differential oracles* — the payload either changes an observable or it does not |
| ssrf-playbook | 3 | a server can be made to fetch | *the channel is the proof* — one canary callback, then stop |
| xss-playbook | 3 | untrusted strings can reach a sink | *context is the vulnerability* — the sink decides the payload, CSP is a recorded fact |
| cloud-config-auditor | 1/3 | object storage, CORS, or DNS edge assets exist | *the perimeter is a configuration file* — anonymous reads and dangling delegations |
| mobile-hunter | 3 | the target ships an Android/iOS app in scope, or an APK/IPA is in hand | *the binary is a confession* — manifest, strings, and bundled secrets read before the device is touched; store review is a hypothesis; findings land at the API boundary (Charlie Miller lineage, with Collin Mulliner) |
| cache-playbook | 3 | a CDN or caching proxy sits in front of the target (X-Cache/Age headers appear) | *the second silent parser* — origin/cache disagreement becomes stored secrets (deception) or stored payloads (poisoning); proofs run operator-as-victim and on nonce paths (Omer Gil + Kettle cache corpus) |
| prototype-playbook | 3 | JavaScript object-model surface exists: JSON merges, third-party JS libraries, postMessage listeners | *the object world is trust-bearing state* — pollution, clobbering, and message confusion hunted source → gadget → sink, server-side detection without the DoS (Gareth Heyes lineage) |
| adversary-tracker | 4 | event-triggered: a sensor or the operator reports adversary activity on assets you are authorized to defend | *the Binary Brain* — freeze, halve by bits, two-channel fix, hand off (Shimomura lineage) |
| scan-economist | 5 | any active sweep is planned — hosts, ports, or timing must be chosen | *scan economy* — liveness before depth, priors over exhaustive sweeps (Fyodor lineage) |
| module-smith | 5 | a hypothesis or finding will be reused across surfaces | *exploitation as composition* — rankable modules, access and impact proofs separate (HD Moore lineage) |
| pipeline-smith | 5 | a recon stage will run more than once | *small tools, stdout* — passive sources first, dedupe before paying (Tomnomnom lineage) |
| feedback-fuzzer | 5 | a search space is too big for enumeration and needs a stopping rule | *the map guides the search* — bucketed novelty, minimization, saturation (lcamtuf lineage) |
| template-scanner | 5 | a check will be reused across engagements and must be reproducible | *detection as data* — matchers pre-registered, campaigns cite their set (ProjectDiscovery lineage) |
| packet-orchestrator | 5 | a manual trace works and is worth automating | *manual first* — translate to state-backed automation layer by layer (Searle + Mantis lineage) |
| protocol-forensics | 5 | a specification class must be hunted across its implementation population, an invariant's entropy must be priced with computed arithmetic, or a class-level fix must be engineered as a coordinated event | *the spec is a treaty between strangers* — implementations resolve ambiguity independently; the class is the target, the population is the denominator, the fix is an event, and every stopgap is labeled a stopgap (Dan Kaminsky lineage) |
| interior-cartographer | 5 | a foothold exists on an OS-class target and the local attack surface is unmapped; a local elevation chain must be argued against the vendor's boundary taxonomy; a declined seam must stay on record | *the interior is the perimeter* — enumerate every local interface the low-privileged principal can reach before composing primitives across seams the access model never priced; the vendor's boundary list is the argument's terrain, and the census — not the exploit — is the research (James Forshaw lineage) |
| harness-smith | 5 | fuzzing effort must be pointed somewhere and the target list is unmapped; a parser surface must be ranked before a harness is built; a finding needs its missed-why | *the privileged parser is the target* — census by privilege × deployment × input hostility, build the missing instrument on a stated budget, declare the oracle before the run, minimize the repro, report without signing terms, and postmortem the miss (Tavis Ormandy lineage) |
| opsec-discipline | 5 | an engagement is about to start and the operator's own footprint must be planned before the first request; engagement credentials, egress, or storage must be separated from the operator's identity; IR could overlap the window and attribution must stay unambiguous; the engagement closes and raw evidence, credentials, and infrastructure must be retired on record | *the operator's trail is priced like any attack surface* — census every exposure row (detection × attribution × removal), put the plumbing in first because paranoia doesn't work retroactively, compartment per engagement (identity/activity/association), let the ROE be the cover and never conceal beyond it, keep the suspect pool wide, treat comms as events whose timing leaks before content, and close with the destruction/contraception triad while the dossier stays compartmented, never destroyed (the grugq lineage) |
| chain-architect | 6 | low/informational findings accumulate and want composition | *the compound kill chain* — 3-4 harmless gaps into critical impact, each link proven (Orange Tsai lineage) |
| desync-hunter | 6 | a parser seam (CDN/WAF/terminator/backend) sits in scope | *specifications are hypotheses* — one ambiguity per request, bytes as artifacts (James Kettle lineage) |
| deep-teardown | 6 | a client artifact (JS/APK/binary) is in scope and unread | *dismantle to primitives* — local dissection before any network flow (George Hotz lineage) |
| ghost-crawler | 6 | scope is tight or the WAF is scanner-hostile | *enter without knocking* — passive indexes first, one bounded probe per candidate (Adrian Lamo lineage) |
| mirror-hunter | 6 | the target embeds an LLM, chatbot, copilot, RAG, or agent/MCP tooling, and the program's AI rules are in hand | *hunt the mirror* — the only target class that runs the same engine as the hunter: the self-model is the target map, the program's eligibility table is the negative scope, and CONFIRMED lands on the deterministic wrapper the model feeds (Simon Willison lineage) |
| probe-smith | 6 | an in-scope IoT/embedded device must be opened physically; firmware must be extracted from a chip configured to refuse; a debug port, pinout, or radio channel must be discovered | *the probeable interface is ground truth* — census the physical interfaces, decide the cheap rig (junk-class always priced), map the pinout with the datasheet as hypothesis, walk the lock-bypass ladder rung by rung with prices, open radios by promiscuity before injection, and report from a priced parts list (Travis Goodspeed lineage) |
| signal-smith | 6 | a validator blocks honest payloads | *precision over volume* — one minimal variation per seam, two max (John Draper lineage) |
| trust-graph-hunter | 6 | components trust each other (headers, referers, signatures, tokens) — or the estate includes an identity directory to audit | *the trust graph* — enumerate trust edges, prove inherited privilege on operator-owned ends (Kevin Mitnick lineage); *the directory interior* — the eight-source rights census, the priced inheritance-path matrix, the tier-boundary validation gate with the KRBTGT double-reset law, detection rows paired at birth (Sean Metcalf lineage layer) |
| lineage-smith | 7 | a figure is nominated for assimilation, or the operator orders corpus growth ("rakit skill dari tokoh", "the next legend") | *read everything, ship the method* — the operator's doctrine as a factory: scored selection, complete-corpus census, documented-behavior psych-read, forge under the authoring contract, wiring through charter + registry + gates |
| rival-playbook | 7 | a rival corpus is named or encountered, positioning is questioned ("kalahkan kompetitor", "beat the competitor"), or any claim about rival corpora is about to ship | *know the rival, know yourself* — the census reads public artifacts date-pinned, force concentrates on the hollow axes, superiority claims land only on measured axes |

Selection is only half the routing contract: once loaded, every organ
RUNS under the execution doctrine (references/autonomous-operation.md)
— OODA-hygiene loop, D1–D7 decision rules, behavior contracts, and a
per-organ execution anchor, the decision scientist behind the craft
lineage: Boyd behind the spine, Simon behind scan-economist, March
behind feedback-fuzzer, Klein behind chain-architect, Kahneman behind
deep-teardown, Taleb behind ghost-crawler, Hofstadter behind
mirror-hunter, Tversky behind trust-graph-hunter, Chomsky behind
signal-smith, Ashby behind pipeline-smith, Popper behind
template-scanner, Snowden behind adversary-tracker, Ericsson behind
the proving ground, Kauffman behind doctrine-forge, Metzinger behind
glm-self-model, Shannon behind protocol-forensics, Korzybski behind
interior-cartographer. And the campaign those organs fight is SHAPED by the
war logic (references/war-doctrine.md, A15): spies before armies,
win without fighting, avoid strength and strike weakness, cheng
paired with ch'i, shih stored in the ledger. `doctrine_forge` carries
both summaries on every forged order, so the contracts ride with the
work.

## 3. The execution hand — arsenal tool groups

| Group | Tools | When |
| --- | --- | --- |
| loader | `list_skills`, `get_skill`, `get_skill_reference` | always first; metadata before bodies |
| charter | `mythos_charter`, `mythos_lineages`, `doctrine_forge` | session start; lineage questions; EVERY operator instruction (A13) |
| governance | `scope_check`, `auth_status` | before any traffic; R0 |
| evidence | `ledger_append`, `ledger_summary`, `ledger_read`, `ledger_merge` | continuously; merge at phase boundaries |
| passive | `ct_subdomains`, `dns_resolve` | Phase 1, recon_only surfaces |
| active | `http_probe`, `content_discover`, `api_introspect`, `js_analyze` | Phase 1–3, in_scope surfaces |
| cartography | `dossier_add`, `dossier_render`, `dossier_summary` | Phase 1; evidence-cited only |
| brain | `sbb_declare`, `sbb_decide`, `sbb_apply` | incident branch only |
| report | `cvss3_score`, `vrt_classify` | report time — the classification pair |
| arsenal | `arsenal_route` | governed CLI execution (allowlist + flag blacklist) |

## 4. Beyond the organs

* **auditor/audit_report.py** — the report gate: evidence citation,
  closure discipline, reproduction data, and (since skill-mythos) the
  classification set — CVSS recomputation, VRT id validation against
  the shipped taxonomy, reproduction reference.
* **lab/target_app.py** — a self-owned vulnerable app on localhost for
  safe rehearsal.
* **lab/christmas_lab.py** — a synthetic Binary Brain hunt (8
  hypotheses, 3 bits, two channels) ending in an audited handoff.
* **examples/worked-engagement/** — a captured 548-record engagement:
  transcript, ledger, dossier, audited report.
* **examples/adversary-hunt/** — a captured Binary Brain hunt: engine
  state, ledger, audited handoff.

## 5. What "extreme expertise" means here

Not volume — *closure*. Every organ ends in one of three states
(CONFIRMED / FALSIFIED / INCONCLUSIVE) with the evidence to show for
it, every confirmed finding carries the full classification set, and
every report passes a gate that would rather fail it than flatter it.
The bundle is finished when nothing in it can hallucinate its way past
the auditor.
