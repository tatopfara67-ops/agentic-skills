# Agentic Skills

Drop-in skills for AI agents (Claude Code, Z.ai, Cursor, MCP-driven operators) — built around one doctrine: **evidence-first, zero slop**. Every claim an agent makes must survive an audit.

Author: [tatopfara67-ops](https://github.com/tatopfara67-ops)

## Skills

| Skill | Version | What it does |
|---|---|---|
| [skill-mythos](skills/skill-mythos/) | 1.0.0 | Master activation module for the Skill Mythos bundle — the charter every other skill converges on. Twelve articles (extreme-expertise identity, research-grounded synthesis, legitimate assimilation of public methodologies, stability-first autonomy, quality over bounty), the tiered bundle map, the autonomy protocol for self-selecting organs by phase and event, and the triage-grade quality gates: zero false positives (differential triad), fully reproducible findings, CVSS 3.1 vectors with recomputed scores, Bugcrowd VRT P-ratings with the HackerOne crosswalk (official taxonomy shipped, Apache-2.0). |
| [mythos-bug-hunter](skills/mythos-bug-hunter/) | 4.3.0 | Discipline layer for authorized security research, bug bounty, and pentest work on web apps, APIs, and AI-powered surfaces. Enforces evidence-cited claims, pre-registered falsifiable hypotheses, reproducible PoCs, canary-based impact proof. Ships 19 reference modules — reasoning engine, attack classes, recon toolchain with target triage, researcher conduct, phase playbook — plus a PASS/FAIL report auditor. |
| [mythos-code-audit](skills/mythos-code-audit/) | 1.0.0 | White-box source-code audit engine, companion to mythos-bug-hunter. Doctrine: *static analysis proposes, the runtime disposes* — no finding ships without a differential oracle. Calibrated by rediscovering CVE-2024-33663 and CVE-2024-33664 from the version diff alone. |
| [mythos-proving-ground](skills/mythos-proving-ground/) | 1.0.0 | Ground-truth benchmark harness for AI security agents. Deploys an instrumented vulnerable lab on localhost, watches what the agent actually does via server-side trigger events, and scores claimed findings against a seeded manifest: coverage, precision, hallucination rate, harm events, evidence discipline, efficiency. |
| [aas-catalog](skills/aas-catalog/) | 1.0.0 | On-demand search & install from the Agentic Awesome Skills catalog (2,884+ community SKILL.md playbooks). One reviewed skill per install, risk-gated, post-install checklist enforced. |
| [surface-cartographer](skills/surface-cartographer/) | 1.0.0 | Phase-1 organ: the organized attack-surface dossier — asset graph, 21-class taxonomy, evidence-cited priority queue. |
| [subdomain-hunter](skills/subdomain-hunter/) | 1.0.0 | Phase-1 organ: passive-first subdomain enumeration, wildcard verdicts, takeover-signature pairs. |
| [content-discovery](skills/content-discovery/) | 1.0.0 | Phase-1 organ: calibrated content walks — 404-baseline controls, rate-courteous sweeps, backup/config triage. |
| [js-recon](skills/js-recon/) | 1.0.0 | Phase-1/2 organ: JS bundle analysis — endpoints, commented routes, sourcemap refs, masked secret hints. |
| [api-surface-mapper](skills/api-surface-mapper/) | 1.0.0 | Phase-1/2 organ: API spec discovery & parsing, version diffs, undocumented endpoints. |
| [auth-boundary-mapper](skills/auth-boundary-mapper/) | 1.0.0 | Phase-2/3 organ: role×resource matrix, IDOR/BOLA differential probes. |
| [oauth-flow-auditor](skills/oauth-flow-auditor/) | 1.0.0 | Phase-2/3 organ: 12-check OAuth/OIDC flow catalog, each check with a falsifier. |
| [business-logic-hunter](skills/business-logic-hunter/) | 1.0.0 | Phase-2/3 organ: workflow abuse, race conditions with rate floors, parameter tampering. |
| [injection-lab](skills/injection-lab/) | 1.0.0 | Phase-3 organ: injection differential oracles — sqlmap runs as oracle only (`--batch` mandatory). |
| [ssrf-playbook](skills/ssrf-playbook/) | 1.0.0 | Phase-3 organ: SSRF channel proofs via canary callbacks, bounded egress checks. |
| [xss-playbook](skills/xss-playbook/) | 1.0.0 | Phase-3 organ: sink-context analysis, marker proofs, CSP treated as recorded fact. |
| [cloud-config-auditor](skills/cloud-config-auditor/) | 1.0.0 | Phase-1/3 organ: CORS matrix, anonymous storage (bounded), takeover checks. |
| [adversary-tracker](skills/adversary-tracker/) | 1.0.0 | Incident-branch organ: the Shimomura Binary Brain — event-triggered adversary hunts on assets you are authorized to defend. Four binary registers, halving loop, two-channel confirmation, audited handoff; distilled from the 1994–95 hunt that ended in Raleigh. |
| [scan-economist](skills/scan-economist/) | 1.0.0 | Craft-lineage organ (the Fyodor lineage): scan economy — cost hierarchy (liveness before depth), speed/stealth/reliability triangle, states as recorded inferences with retransmission, empirical priors over exhaustive sweeps, adaptive pacing. Distilled from Phrack 51's "The Art of Port Scanning" (1997, read in full) and Nmap Network Scanning. |
| [module-smith](skills/module-smith/) | 1.0.0 | Craft-lineage organ (the HD Moore lineage): exploitation as composition — hypotheses as rankable reusable modules, access and impact proofs as separate artifacts, exposure as a measurement with a denominator. Distilled from the Metasploit module architecture and Project Sonar. |
| [pipeline-smith](skills/pipeline-smith/) | 1.0.0 | Craft-lineage organ (the Tomnomnom lineage): Unix recon pipelines — passive sources before active probes, dedupe before paying, cheap liveness, pattern knowledge as versioned data, diff against siblings to decide. Distilled from assetfinder/httprobe/gf/meg/gron. |
| [feedback-fuzzer](skills/feedback-fuzzer/) | 1.0.0 | Craft-lineage organ (the lcamtuf lineage): feedback-guided search — coarse state maps, bucketed novelty, deterministic before chaotic, curated corpora, tarpit rejection, minimization before diagnosis, saturation as the stopping rule. Distilled from AFL's design document (read in full). |
| [template-scanner](skills/template-scanner/) | 1.0.0 | Craft-lineage organ (the ProjectDiscovery lineage — Sandeep Singh, Rishiraj Sharma, Marco Rivoli, Nizamul Rana): detection knowledge as declarative templates — matchers pre-registered, engine and packs evolve separately, campaigns cite their template set. |
| [packet-orchestrator](skills/packet-orchestrator/) | 1.0.0 | Craft-lineage organ (the Searle + Mantis lineage): manual first, then layer-by-layer translation into structured, state-backed automation; packet differentials show their bytes. Justin Searle (InGuardians, SamuraiWTF/STFU) + the Mantis framework (PhonePe); attribution corrected on record. |

## Prompts

| Prompt | Version | What it does |
|---|---|---|
| [terse-core](prompts/terse-core/system-prompt-v1.md) | 1.0 | Output-token discipline system prompt. Static cache-friendly core (never edit after deploy) + dynamic PAYLOAD slot for per-session content. |

## Arsenal — the execution hand

[**arsenal/**](arsenal/) — the mythos-arsenal MCP server (FastMCP, `arsenal/server.py`): **26 scope-gated tools** that execute the 20 bundles above (the skill-mythos charter + 13 phase organs + 6 craft-lineage organs) under one authorization registry ([scope.csv](scope.csv) — deny-by-default, every row cites an auth artifact) and one append-only evidence ledger (R-NNN records). Tool groups: charter (`mythos_charter` + `mythos_lineages` — the activation payload and the assimilated-lineage registry with corrections on record), loader (progressive skill disclosure), governance (`scope_check`/`auth_status`), evidence (`ledger_*`), passive + active probes, dossier cartography, the **Binary Brain** engine (`sbb_declare`/`sbb_decide`/`sbb_apply` — the incident branch), the report pair (`cvss3_score`/`vrt_classify` — spec-exact CVSS 3.1 scoring and Bugcrowd VRT classification against the shipped official taxonomy, with the HackerOne crosswalk), and `arsenal_route` (CLI allowlist + flag blacklist for Kali-style tools).

```bash
pip install -r requirements.txt                 # mcp>=1.2.0
python3 arsenal/server.py --selftest            # lists all 26 tools
python3 -m unittest discover -s arsenal/tests   # 78 tests
python3 scripts/validate_skill.py --all         # 24 bundles PASS
```

Ships with a PASS/FAIL report gate ([auditor/](auditor/)), two self-owned labs ([lab/target_app.py](lab/target_app.py) and [lab/christmas_lab.py](lab/christmas_lab.py) — a synthetic Binary Brain hunt), and audited worked examples ([examples/](examples/): a 548-record engagement and a closed adversary hunt). Wire it via [agent/mcp/wiring.json](agent/mcp/wiring.json) (`mythos-arsenal` entry) and keep [CLAUDE.md](CLAUDE.md) at the workspace root — MCP serves the tools, the contract makes the agent use them in discipline.

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

[**agent/ARCHITECTURE.md**](agent/ARCHITECTURE.md) — the flagship: **Mythos Agent**, a bug bounty AI agent architecture built on this repo's skill stack. Ten layers (conduct, scope gate, intelligence, hypothesis engine, arsenal, evidence, court, economy, memory, meta-observer) with one thesis: the LLM is the least trusted component — every layer exists to catch it when it hallucinates. Ships with an engagement template (scope.csv allowlist, hypothesis ledger schema, evidence index), MCP wiring for the Kali bridge / acb / github / mythos-arsenal servers, and a proving-ground A/B benchmark config with hard ship-blockers (hallucination ≤ 10%, harm events = 0).

## Building skills here

New skills are built under the house authoring discipline, not freehand — see [CONTRIBUTING.md](CONTRIBUTING.md): observed friction before authoring, required frontmatter with trigger phrases, progressive disclosure, minimal-but-complete scope, and a hard validation gate before every commit:

```bash
python3 scripts/validate_skill.py skills/<skill-name>
```

This repository ships original work only — nothing is vendored from third parties.

## License

MIT — see [LICENSE](LICENSE).
