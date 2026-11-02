# Agentic Skills

Drop-in skills for AI agents (Claude Code, Z.ai, Cursor, MCP-driven operators) — built around one doctrine: **evidence-first, zero slop**. Every claim an agent makes must survive an audit.

Author: [tatopfara67-ops](https://github.com/tatopfara67-ops)

How the whole skill agent works, in one picture: **[docs/mythos-arsenal-arsitektur.png](docs/mythos-arsenal-arsitektur.png)** (anatomy: charter → engine → spine → 26 organs → the execution hand; then the session flow: A13 doctrine escalation → R0 scope gate → the hunt loop F0–F4 → the incident branch → report gates → instinct calibration).

## Skills

| Skill | Version | What it does |
|---|---|---|
| [skill-mythos](skills/skill-mythos/) | 1.3.0 | Master charter: thirteen articles, the tiered bundle map, the autonomy protocol, triage-grade quality gates (CVSS 3.1 + VRT/HackerOne). Loads first, hunts nothing. |
| [glm-self-model](skills/glm-self-model/) | 1.0.0 | The engine layer: model-class failure geometry for the GLM-class agent that runs every other skill — five truths (simulation not recall, spotlight context, ending gradient, unmeasured confidence, nothing in the weights) and four compensation gates (fresh-eyes re-derivation, edge placement, first-written priors, salience counterweight). Written to the engine, not to the operator. |
| [mythos-bug-hunter](skills/mythos-bug-hunter/) | 4.5.0 | The spine: discipline layer for authorized web/API/AI research — evidence-cited claims, pre-registered hypotheses, reproducible PoCs, canary impact proofs, the trained-eye cue catalog with per-engagement instinct calibration, long-horizon mission discipline (quota unmet ends only by exhaustion proof or operator release). 19 reference modules + a PASS/FAIL report auditor. |
| [mythos-code-audit](skills/mythos-code-audit/) | 1.0.0 | White-box source audit. *Static analysis proposes, the runtime disposes* — no finding without a differential oracle. Calibrated by rediscovering CVE-2024-33663/33664 from the version diff. |
| [mythos-proving-ground](skills/mythos-proving-ground/) | 1.0.0 | Ground-truth benchmark: deploys an instrumented vulnerable lab, records server-side trigger events, scores coverage, precision, hallucination rate, harm events. |
| [aas-catalog](skills/aas-catalog/) | 1.0.0 | Search & install from the Agentic Awesome Skills catalog — one reviewed skill per install, risk-gated. |
| [surface-cartographer](skills/surface-cartographer/) | 1.0.0 | Phase 1: the attack-surface dossier — asset graph, 21-class taxonomy, priority queue. |
| [subdomain-hunter](skills/subdomain-hunter/) | 2.0.0 | Phase 1: passive-first enumeration, wildcard verdicts, takeover signatures; v2 folds in the EdOverflow dangling-class lineage. |
| [content-discovery](skills/content-discovery/) | 2.0.0 | Phase 1: calibrated content walks, 404-baseline controls, backup/config triage; v2 folds in the Miessler corpus-family lineage. |
| [js-recon](skills/js-recon/) | 1.0.0 | Phase 1/2: JS bundle analysis — endpoints, commented routes, sourcemaps, masked secrets. |
| [api-surface-mapper](skills/api-surface-mapper/) | 1.0.0 | Phase 1/2: API spec discovery, version diffs, undocumented endpoints. |
| [auth-boundary-mapper](skills/auth-boundary-mapper/) | 2.0.0 | Phase 2/3: role×resource matrix, IDOR/BOLA differentials; v2 folds in the Frans Rosen lineage (identifier construction, 2nd-order IDOR, tenant slices). |
| [oauth-flow-auditor](skills/oauth-flow-auditor/) | 2.0.0 | Phase 2/3: OAuth/OIDC checks with falsifiers; v2 folds in the Aaron Parecki lineage (RFC 9700 vocabulary). |
| [business-logic-hunter](skills/business-logic-hunter/) | 2.0.0 | Phase 2/3: workflow abuse, races with rate floors, parameter tampering; v2 folds in the Soroush Dalili reshaping lineage. |
| [injection-lab](skills/injection-lab/) | 1.0.0 | Phase 3: injection differential oracles — sqlmap runs as oracle only (`--batch` mandatory). |
| [ssrf-playbook](skills/ssrf-playbook/) | 1.0.0 | Phase 3: SSRF channel proofs via canary callbacks, bounded egress checks. |
| [xss-playbook](skills/xss-playbook/) | 2.0.0 | Phase 3: sink-context analysis, marker proofs; v2 folds in the Heiderich mXSS lineage (re-serialization, DOM clobbering). |
| [cloud-config-auditor](skills/cloud-config-auditor/) | 2.0.0 | Phase 1/3: CORS matrix, anonymous storage, takeover checks; v2 folds in the Prowler checks-as-code lineage. |
| [adversary-tracker](skills/adversary-tracker/) | 1.0.0 | Incident branch: the Shimomura Binary Brain — event-triggered hunts, halving loop, two-channel confirmation, audited handoff. |
| [scan-economist](skills/scan-economist/) | 1.0.0 | Craft tier (Fyodor): scan economy — liveness before depth, priors over exhaustive sweeps, adaptive timing. |
| [module-smith](skills/module-smith/) | 1.0.0 | Craft tier (HD Moore): hypotheses as rankable reusable modules; access and impact proofs kept separate. |
| [pipeline-smith](skills/pipeline-smith/) | 1.0.0 | Craft tier (Tomnomnom): Unix recon pipelines — passive first, dedupe before paying, pattern packs as data. |
| [feedback-fuzzer](skills/feedback-fuzzer/) | 1.0.0 | Craft tier (lcamtuf): feedback-guided search — bucketed novelty, minimization before diagnosis, saturation as the stop rule. |
| [template-scanner](skills/template-scanner/) | 1.0.0 | Craft tier (ProjectDiscovery): detection as declarative templates — matchers pre-registered, campaigns cite their set. |
| [packet-orchestrator](skills/packet-orchestrator/) | 1.0.0 | Craft tier (Searle + Mantis): manual first, then layer-by-layer state-backed automation; packet differentials show their bytes. |
| [chain-architect](skills/chain-architect/) | 1.0.0 | Legend tier (Orange Tsai): compound kill chains — low findings composed into one critical impact, every link proven by its own differential. |
| [desync-hunter](skills/desync-hunter/) | 1.0.0 | Legend tier (James Kettle): protocol asymmetry — one ambiguity per request, confirmed by response-class differential, exact bytes as artifacts. |
| [deep-teardown](skills/deep-teardown/) | 1.0.0 | Legend tier (George Hotz): dismantle client artifacts to primitives — local dissection before any network flow, secrets masked. |
| [ghost-crawler](skills/ghost-crawler/) | 1.0.0 | Legend tier (Adrian Lamo): passive-index misconfig hunting — one bounded probe per candidate, the guarded main app untouched. |
| [signal-smith](skills/signal-smith/) | 1.0.0 | Legend tier (John Draper): input grammar and precision signals — one minimal variation per seam, two max, never trip the alarm. |
| [trust-graph-hunter](skills/trust-graph-hunter/) | 1.0.0 | Legend tier (Kevin Mitnick): the trust graph between components — enumerate what each boundary trusts, prove inherited privilege on operator-owned ends. |

## Prompts

| Prompt | Version | What it does |
|---|---|---|
| [terse-core](prompts/terse-core/system-prompt-v1.md) | 1.0 | Output-token discipline system prompt. Static cache-friendly core (never edit after deploy) + dynamic PAYLOAD slot for per-session content. |

## Arsenal

[arsenal/](arsenal/) — the mythos-arsenal MCP server (FastMCP, `arsenal/server.py`): **27 scope-gated tools** that execute the 31 bundles above — the charter, the spine, 26 organs, and the audit/benchmark companions — under one authorization registry ([scope.csv](scope.csv), deny-by-default, every row cites an auth artifact) and one append-only evidence ledger (R-NNN records).

Tool groups: charter (`mythos_charter`, `mythos_lineages`, `doctrine_forge` — A13: any operator instruction, however terse, becomes an explicit doctrine order), loader, governance (`scope_check`/`auth_status`), evidence (`ledger_*`), passive + active probes, dossier cartography, the Binary Brain engine (`sbb_*`), the report pair (`cvss3_score`/`vrt_classify`), and `arsenal_route` (CLI allowlist + flag blacklist).

```bash
pip install -r requirements.txt                 # mcp>=1.2.0
python3 arsenal/server.py --selftest            # lists all 27 tools
python3 -m unittest discover -s arsenal/tests   # 102 tests
python3 scripts/validate_skill.py --all         # 31 bundles PASS
```

Ships with a PASS/FAIL report gate ([auditor/](auditor/)), two self-owned labs ([lab/target_app.py](lab/target_app.py), [lab/christmas_lab.py](lab/christmas_lab.py)), and audited worked examples ([examples/](examples/): a 548-record engagement and a closed adversary hunt). Wire it via [agent/mcp/wiring.json](agent/mcp/wiring.json) and keep [CLAUDE.md](CLAUDE.md) at the workspace root — MCP serves the tools, the contract makes the agent use them.

## Install

Copy a skill folder into your agent's skills directory:

```bash
git clone https://github.com/tatopfara67-ops/agentic-skills.git
cp -r agentic-skills/skills/mythos-bug-hunter/ /path/to/your/agent/skills/
```

Each skill is self-contained: read its `SKILL.md` first, it declares its modules, modes, and hard rules. Reference modules under `references/` are loaded on demand — not all at once.

## Doctrine

1. **Evidence-cited claims.** No finding without a captured artifact (raw request/response, diff, or runtime proof).
2. **Pre-registered hypotheses.** Declare what would falsify a claim *before* testing it.
3. **Differential oracles.** Static analysis proposes, the runtime disposes.
4. **Auditable output.** Every skill ships with an auditor (PASS/FAIL) or a benchmark harness that scores the agent against ground truth.
5. **Zero slop.** No unverified "findings", no AI-generated filler, no generic advice.

## Authorization notice

The security skills in this repo are for **authorized targets only** — bug bounty programs with a defined scope, contracted pentest engagements, CTF labs, and your own infrastructure. Unauthorized testing is illegal in most jurisdictions, including under Indonesia's UU ITE. The skills themselves enforce this: they refuse to operate without explicit authorization.

## Agent

[**agent/ARCHITECTURE.md**](agent/ARCHITECTURE.md) — **Mythos Agent**: a bug bounty AI agent architecture built on this skill stack. Ten layers (conduct, scope gate, intelligence, hypothesis engine, arsenal, evidence, court, economy, memory, meta-observer) with one thesis: the LLM is the least trusted component — every layer exists to catch it when it hallucinates. Ships with an engagement template, MCP wiring, and a proving-ground A/B benchmark config with hard ship-blockers (hallucination ≤ 10%, harm events = 0).

## Building skills here

New skills are built under the house authoring discipline, not freehand — see [CONTRIBUTING.md](CONTRIBUTING.md): observed friction before authoring, required frontmatter with trigger phrases, progressive disclosure, minimal-but-complete scope, and a hard validation gate before every commit:

```bash
python3 scripts/validate_skill.py skills/<skill-name>
```

This repository ships original work only — nothing is vendored from third parties.

## License

MIT — see [LICENSE](LICENSE).
