# Agentic Skills

Drop-in skills for AI agents (Claude Code, Z.ai, Cursor, MCP-driven operators) — built around one doctrine: **evidence-first, zero slop**. Every claim an agent makes must survive an audit.

Author: [tatopfara67-ops](https://github.com/tatopfara67-ops)

## Skills

| Skill | Version | What it does |
|---|---|---|
| [mythos-bug-hunter](skills/mythos-bug-hunter/) | 4.2.0 | Discipline layer for authorized security research, bug bounty, and pentest work on web apps, APIs, and AI-powered surfaces. Enforces evidence-cited claims, pre-registered falsifiable hypotheses, reproducible PoCs, canary-based impact proof. Ships 17 reference modules — reasoning engine, attack classes, recon toolchain with target triage — plus a PASS/FAIL report auditor. |
| [mythos-code-audit](skills/mythos-code-audit/) | 1.0.0 | White-box source-code audit engine, companion to mythos-bug-hunter. Doctrine: *static analysis proposes, the runtime disposes* — no finding ships without a differential oracle. Calibrated by rediscovering CVE-2024-33663 and CVE-2024-33664 from the version diff alone. |
| [mythos-proving-ground](skills/mythos-proving-ground/) | 1.0.0 | Ground-truth benchmark harness for AI security agents. Deploys an instrumented vulnerable lab on localhost, watches what the agent actually does via server-side trigger events, and scores claimed findings against a seeded manifest: coverage, precision, hallucination rate, harm events, evidence discipline, efficiency. |
| [aas-catalog](skills/aas-catalog/) | 1.0.0 | On-demand search & install from the Agentic Awesome Skills catalog (2,884+ community SKILL.md playbooks). One reviewed skill per install, risk-gated, post-install checklist enforced. |

## Prompts

| Prompt | Version | What it does |
|---|---|---|
| [terse-core](prompts/terse-core/system-prompt-v1.md) | 1.0 | Output-token discipline system prompt. Static cache-friendly core (never edit after deploy) + dynamic PAYLOAD slot for per-session content. |

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

[**agent/ARCHITECTURE.md**](agent/ARCHITECTURE.md) — the flagship: **Mythos Agent**, a bug bounty AI agent architecture built on this repo's skill stack. Ten layers (conduct, scope gate, intelligence, hypothesis engine, arsenal, evidence, court, economy, memory, meta-observer) with one thesis: the LLM is the least trusted component — every layer exists to catch it when it hallucinates. Ships with an engagement template (scope.csv allowlist, hypothesis ledger schema, evidence index), MCP wiring for the Kali bridge / acb / github servers, and a proving-ground A/B benchmark config with hard ship-blockers (hallucination ≤ 10%, harm events = 0).

## Building skills here

New skills are built under the house authoring discipline, not freehand — see [CONTRIBUTING.md](CONTRIBUTING.md): observed friction before authoring, required frontmatter with trigger phrases, progressive disclosure, minimal-but-complete scope, and a hard validation gate before every commit:

```bash
python3 scripts/validate_skill.py skills/<skill-name>
```

This repository ships original work only — nothing is vendored from third parties.

## License

MIT — see [LICENSE](LICENSE).
