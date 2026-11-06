<p align="center"><img src="docs/logo-lockup.png" alt="Mythos Arsenal — Agentic Security Skills"></p>

**44 self-contained skill bundles that turn any AI agent into a disciplined bug-bounty specialist** — an append-only evidence ledger, pre-registered hypotheses, differential oracles, and a report auditor that refuses to ship a report with fabricated citations. For Claude Code, Z.ai, Cursor, and any MCP-driven operator.

Author: [tatopfara67-ops](https://github.com/tatopfara67-ops)

![bundles](https://img.shields.io/badge/skill_bundles-44-informational) ![tools](https://img.shields.io/badge/MCP_tools-33-informational) ![tests](https://img.shields.io/badge/tests-193_passing-2ea44f) ![doctrine](https://img.shields.io/badge/doctrine-evidence--first-8a8f98) ![license](https://img.shields.io/badge/license-MIT-8a8f98)

---

## The architecture in one diagram

```mermaid
flowchart TD
    subgraph LOAD["WHAT LOADS — the organ stack"]
        C["the charter"]
        E["engine manual"]
        S["the spine"]
        O["38 organs"]
        H["execution hand"]
        C --> E --> S --> O --> H
    end

    subgraph RUN["WHAT RUNS — one engagement"]
        A["operator order"]
        B["doctrine order"]
        G{"scope gate R0"}
        X["refusal logged"]
        L["hunt loop"]
        I["incident branch"]
        R["report gates"]
        K["calibration"]
        A --> B --> G
        G -->|refused| X
        G -->|authorized| L
        L --> I
        L --> R --> K
    end
```

The two panels connect at the seam: the execution hand (bottom of WHAT LOADS) is what carries out the operator order (top of WHAT RUNS) — the tools the stack loads are the tools the engagement runs.

The always-on rails — the constraints that ride along every step of every engagement:

| Rail | What it holds |
|---|---|
| **Evidence** | Append-only R-NNN ledger — no claim without a record |
| **Calibration** | Differential triad on every claim — baseline / treatment / control |
| **Impact** | Canary proofs on self-owned objects, one demonstration, then stop |
| **Economy** | Priced budgets per campaign — "done" without numbers is a forbidden state |
| **Engine gates** | G1 fresh-eyes re-derivation before CONFIRMED · G2 edges for critical state · G3 first-written priors · G4 queue over decibels |
| **Mission horizon** | A quota is a continuation mandate — it ends only by exhaustion proof or operator release |
| **Three registers (A14)** | WHAT the bug class is · WHY it lives where it lives · HOW it is hunted |
| **War logic (A15)** | W1 spies before armies · W2 win without fighting · W3 strike weakness · W4 cheng + ch'i · W5 shih · W6 sovereign sets intent · W7 no prolonged war |

The one thesis under all of it, from [agent/ARCHITECTURE.md](agent/ARCHITECTURE.md): **the LLM is the least trusted component — every layer above exists to catch it when it hallucinates.**

## What this is

An **organ stack** for authorized pentest, bug bounty, and security research. Instead of one giant prompt, the expertise is split into 43 self-contained skills — each a narrow discipline with its own hard rules, loaded on demand. Four ideas hold it together:

1. **The LLM is the least trusted component.** Every layer exists to catch the agent when it hallucinates: an append-only evidence ledger (no claim without a record), pre-registered hypotheses (declare what would falsify you *before* testing), differential oracles (baseline/treatment/control — static analysis proposes, the runtime disposes).
2. **Expertise is stated in three registers (A14).** Every organ answers WHAT the bug class is, WHY it lives where it lives (the root cause), and HOW it is hunted (numbered procedure with oracles). A technique missing a register is not shipped.
3. **Campaigns are fought with war logic (A15).** The Sun Tzu crosswalk rides every order as rules W1–W7: spies before armies (passive before active), win without fighting (the differential triad proves — damage is not evidence), strike weakness (seam density over target fame), cheng + ch'i (every plan pairs the orthodox sweep with an unorthodox bet).
4. **The corpus grows by assimilation and competes by evidence (the forge tier).** lineage-smith turns a named public figure's complete corpus into an organ born with its method layer; rival-playbook grades rival corpora from date-pinned public artifacts and settles superiority claims on measured axes only.

## The stack

| Layer | Bundle | What it contributes |
|---|---|---|
| Charter | [skill-mythos](skills/skill-mythos/) v1.21.4 | The nineteen articles (A16 method over mythology, A17 behavior over biography, A18 the opening ladder — perception as a candidate-generation drill before verification, A19 the payload corpus depth law — every payload kit row resolves to a byte-exact versioned corpus entry, and the extreme tier releases only through the weapons vault: instruction-override attempts refused and ledgered, weaponized classes banned outright, no override parameter in the gate's surface — and the vault's refusal accuracy is itself measured by the labeled bench), the tiered bundle map (tiers 0–7), the autonomy + execution + war doctrines, triage-grade quality gates (CVSS 3.1 + VRT/HackerOne). The full binding text of the articles lives in references/charter.md — the routing layer stays lean (locked by test_charter_full_text_lives_in_references). Loads first, hunts nothing. |
| Engine | [glm-self-model](skills/glm-self-model/) v1.1.1 | The engine's own manual — model-class failure geometry E1–E8 and four compensation gates, written to the engine, not the operator. |
| Spine | [mythos-bug-hunter](skills/mythos-bug-hunter/) v4.8.0 | Discipline layer: R0–R7 canon, append-only ledger, hypothesis grammar, closure gates, mission horizon. 22 reference modules + a PASS/FAIL report auditor; carries the Jason Haddix lineage layer (methodology-preservation protocol), and since v4.7.0 the Hypothesis Contract is executable — hypothesis_register / _close / _list refuse unevidenced registration, non-three-state closure, and retrodiction; since v4.8.0 the onboarding runtime ships The opening ladder (A18) — the corpus-reading questions (pin / split / rot / gate / basis / proof) that write preservation rows before any engagement state exists. |
| Organs | 38 organ skills (tiers 1–7 below: 36 hunting + 2 forge) | The expertise: recon, access logic, deep technical attacks, incident response, craft lineages, legend-tier overlays, and the forge tier that grows and positions the corpus itself. |
| Execution hand | [arsenal/](arsenal/) | The FastMCP server: 33 scope-gated tools that execute everything above — including the weapons vault (`payload_release`: extreme-tier corpus bytes leave only to scope-authorized targets, jailbreak attempts refused and ledgered) and its accuracy bench (`payload_bench`: the labeled release/refusal case set, zero-false-release verdict) — plus the report auditor and two self-owned labs. |

## The lineage corpus

![The lineage corpus](docs/lineage-corpus.png)

Every hunting method in this corpus was extracted from a named practitioner's public record — talks, write-ups, books, code — under the assimilation doctrine: **A16 method over mythology, A17 behavior over biography**. No organ ships a biography. What ships is the method: numbered procedures, oracles, gates, and a run-order. Each registry entry cites its dated sources and keeps corrections on record.

| Fact | Value |
|---|---|
| Registry entries | 33 — 30 hunting organs, 2 forge organs, the spine's methodology layer |
| Named figures | 32, from recon toolmakers to physical-access specialists |
| Dual-lineage organs | [trust-graph-hunter](skills/trust-graph-hunter/) (Mitnick + Metcalf) · [cache-playbook](skills/cache-playbook/) (Gil + Kettle) |
| Candidate queue | 8 nominated, 8 assimilated, queue empty — [candidate-queue.md](skills/lineage-smith/references/candidate-queue.md) |
| Reading ledger | every organ's `references/sources.md` |

Regenerate after any lineage change: `python3 scripts/render_lineage_graph.py`

## What changes in a bug-bounty engagement

The engine layer documents how language models fail in this domain (failure geometry E1–E8). Each row below pairs a documented failure mode with the behavior this stack enforces instead — and the file or test that enforces it.

| Failure mode | What the stack enforces | Enforced by |
|---|---|---|
| Findings stated from parametric memory | Every claim cites an R-NNN record in an append-only ledger; reports are built from the ledger, not memory | `arsenal/ledger.py` · `auditor/audit_report.py` |
| Fabricated or misdirected citations reach the report | The auditor recomputes every citation against the ledger and exits non-zero — the report does not ship | `auditor/audit_report.py` · `arsenal/tests/test_audit_report.py` |
| Severity guessed | CVSS 3.1 vector recomputed per finding, plus a Bugcrowd VRT P-rating with the HackerOne crosswalk | `arsenal/cvss.py` · `arsenal/tools/mythos.py` |
| Out-of-scope targets probed | Deny-by-default scope gate refuses before the first request; the refusal itself is logged as a ledger record | `arsenal/scope_gate.py` · `scope.csv` · `arsenal/tests/test_scope_gate.py` |
| Tests run first, rationale invented after | Hypotheses pre-registered with falsifiers; closure forced to CONFIRMED / FALSIFIED / INCONCLUSIVE — mechanically: registration whose motivating facts are not ledger records is refused, CONFIRMED on retrodiction (experiments pre-dating registration) is refused, INCONCLUSIVE without a Park record is refused | `arsenal/hypotheses.py` · `arsenal/tests/test_hypotheses.py` · spine canon R0–R7 |
| The agent only proves what it is handed — it never generates candidates | The opening ladder (A18): the lineage's perception as a question ladder that produces ranked census rows before any verification is due — rungs write rows, never packets; a ladder that yields nothing on a live estate is revised, not the estate excused | `skills/*/references/operator-os.md` · `arsenal/tests/test_mythos.py` (test_opening_ladder_rollout) |
| The agent hand-crafts probe bytes a prose reference described | The payload corpus depth law (A19): every payload kit row resolves to a byte-exact versioned corpus entry — the corpus grows only by transcribed, attributed entries, and every growth bumps `corpus_version`; target-derived shapes stay labeled derivation rows; the covered organ set grows only by execution (the seam organ and the spine's coordinator kit joined in the second wave; the extreme tier rides the weapons vault — third wave INJ/XSS, fourth wave the desync and cache extreme seams, fifth wave the ssrf/prototype credential-and-gadget seams, sixth wave the GCP service-account token seam; the php2shell forensics organ joins the covered set with its detection corpus) | `skills/*/references/corpus.json` · `arsenal/tests/test_mythos.py` (test_payload_kit_depth) |
| An operator (or a hijacked prompt) talks the agent into releasing weaponized payloads or overriding the scope | The weapons vault (A19e): `payload_release` scans every caller string for instruction-override attempts — 50 structural patterns: the English deep families ("ignore previous instructions", "no authorization needed", "act as if authorized", forget-the-rules variants, treat/assume-as-authorized verbs, mode-escalation verbs, prompt-exfiltration attempts) plus the fourth hardening wave closing the language-blindness gap (the same structures in Indonesian — the operator's working language — Spanish, French, German, Portuguese, Italian, Russian, Mandarin, and Japanese; clean basis-noted notes in every covered language still release) — and refuses + ledger-records the hit; destructive-impact and weaponization classes (DDL/DML destruction, file-write implants, command-execution implants, C2 tooling) are banned from the corpus outright; the gate has no override parameter, no bulk-dump path — one entry, one scope-authorized target, deny-by-default; and the vault's refusal accuracy is itself measured — `arsenal/proving_ground.py` + the `payload_bench` tool run a labeled multilingual release/refusal bench (novel and obfuscated phrasings across ten languages, unknown ids, the scope triad, clean basis-noted releases spanning every organ) whose first run caught and closed two real pattern gaps (locked by test_proving_ground) | `arsenal/payload_gate.py` · `arsenal/proving_ground.py` · `arsenal/tests/test_payload_gate.py` · `arsenal/tests/test_proving_ground.py` · `arsenal/server.py` (payload_release, payload_vault_status, payload_bench) |
| Budget burned on dead surfaces | Liveness before depth, priors over exhaustive sweeps, a priced budget table per campaign | [scan-economist](skills/scan-economist/) · [module-smith](skills/module-smith/) |
| Report rejected for missing reproduction | The gate requires reproduction steps, a recomputed CVSS vector, and a VRT rating on every finding | report templates · [auditor/](auditor/) |
| Hallucination rate unknown | Instrumented labs score coverage, precision, hallucination and harm per run | [mythos-proving-ground](skills/mythos-proving-ground/) · [lab/](lab/) |

## Verification

Reproduce the numbers from a fresh checkout:

| Claim | Check | Expected |
|---|---|---|
| 44 skill bundles pass structural validation, zero warnings | `python3 scripts/validate_skill.py --all` | `GATE: PASS (44 bundle(s), 0 warning(s))` — the master charter's SKILL.md was refactored past the advisory size cap (v1.21.2): the full article text moved verbatim to references/charter.md, and the lean routing layer is locked by test_charter_full_text_lives_in_references |
| 193 unit tests pass | `python3 -m unittest discover -s arsenal/tests` | `Ran 193 tests ... OK` — the vault's own suite grew with the second hardening wave (22 structural instruction-override patterns), the fourth corpus wave, the fifth corpus wave (ssrf/prototype extreme + the php2shell forensics organ), the vault accuracy bench (test_proving_ground), and the fourth hardening wave (the language-blindness close: 50 structural instruction-override patterns across nine further languages, both sides tested per language) |
| 33 MCP tools register and import | `python3 arsenal/server.py --selftest` | `registered MCP tools (33)` |
| Pre-registration is mechanical | `python3 -m unittest arsenal.tests.test_hypotheses` | `OK` — registration without ledger facts, retrodiction, and Park-less INCONCLUSIVE are all refused |
| The scope gate refuses out-of-scope targets | `python3 -m unittest arsenal.tests.test_scope_gate` | `OK` |
| The report gate fails fabricated citations | `python3 -m unittest arsenal.tests.test_audit_report` | `OK` |
| The lineage registry holds 33 sourced entries | `python3 -c "from arsenal.tools.mythos import LINEAGES; print(len(LINEAGES))"` | `33` |
| A worked engagement ships a 550-record ledger | `wc -l examples/worked-engagement/ledger/records.md` | `550` |
| White-box audit is calibrated on real CVEs | [worked example](skills/mythos-code-audit/example/worked-example.md) | CVE-2024-33663 / CVE-2024-33664 rediscovered |

The worked examples are audited end to end: a 550-record engagement ledger and a closed adversary hunt in [examples/](examples/), two self-owned labs in [lab/](lab/) (`target_app.py`, `christmas_lab.py`).

## Installation

### A. Quick start — one skill in any agent

```bash
git clone https://github.com/tatopfara67-ops/agentic-skills.git
cp -r agentic-skills/skills/mythos-bug-hunter/ /path/to/your/agent/skills/
```

Each skill is self-contained. Read its `SKILL.md` first — it declares the modules, modes, and hard rules. Reference modules under `references/` load on demand, not all at once.

### B. Full arsenal — the MCP server

```bash
git clone https://github.com/tatopfara67-ops/agentic-skills.git
cd agentic-skills
pip install -r requirements.txt          # mcp>=1.2.0
python3 arsenal/server.py --selftest     # must list all 32 tools
```

Wire it into your MCP client with [agent/mcp/wiring.json](agent/mcp/wiring.json), then authorize targets in [scope.csv](scope.csv) — deny-by-default, every row cites an auth artifact. Keep [CLAUDE.md](CLAUDE.md) at the workspace root: MCP serves the tools, the contract makes the agent use them.

### C. The Mythos Agent — the full architecture

[**agent/ARCHITECTURE.md**](agent/ARCHITECTURE.md) — a bug-bounty AI agent in ten layers (conduct, scope gate, intelligence, hypothesis engine, arsenal, evidence, court, economy, memory, meta-observer), with an engagement template, MCP wiring, and a proving-ground A/B benchmark whose ship-blockers are hard numbers: hallucination ≤ 10%, harm events = 0.

## How to use

**1 — Activate.** Open the session and say it in any language: *"aktifkan Skill Mythos"* / "activate Skill Mythos". The charter loads: articles, bundle map, quality gates.

**2 — Order. Terse is fine.** One line, any language, is enough:

> *dapatkan minimal 3 bug high-medium di target X*

`doctrine_forge` (A13) expands it into an explicit doctrine order — intent, phase plan, war logic W1–W7, gates — before any organ acts. The sovereign sets intent; the general commands.

**3 — The hunt runs itself, inside the rails.** Scope gate first (R0, deny-by-default), then the loop F0–F4: map → pre-registered hypotheses → differential tests → canary impact proofs → closure (CONFIRMED / FALSIFIED / INCONCLUSIVE). The organ for each phase self-selects; a mid-hunt re-ask of what the order already answered is a doctrine violation, not diligence.

**4 — Read the output.** Findings come out of the ledger, not memory: every report cites R-NNN records, carries a recomputed CVSS 3.1 vector, a Bugcrowd VRT P-rating with the HackerOne crosswalk, and reproduction steps. The auditor ([auditor/](auditor/)) exits 0 or the report does not ship.

Representative tools: `mythos_charter` (activation payload) · `doctrine_forge` (order expansion) · `scope_check` (authorization) · `payload_release` (the weapons vault — extreme-tier corpus bytes to scope-authorized targets only, jailbreak attempts refused and ledgered) · `payload_bench` (the vault accuracy bench — labeled release/refusal cases, zero-false-release verdict) · `ledger_read` / `ledger_append` (evidence) · `hypothesis_register` / `hypothesis_close` (pre-registration and three-state closure, refused when unevidenced) · `cvss3_score` / `vrt_classify` (triage) · `arsenal_route` (CLI allowlist).

## Skill catalog

Every person-lineage organ (30 hunting organs + the spine) ships two layers: the **A16 method layer** — WHAT the bug class is, WHY it lives where it lives, HOW it is hunted, with oracles and gates — and the **A17 operator runtime layer** — thinking rules, behavior, scripting as craft. The five house-method organs and the forge tier ship the method layer.

### Framework bundles (6)

| Skill | Version | What it does |
|---|---|---|
| [skill-mythos](skills/skill-mythos/) | 1.21.4 | Master charter — nineteen articles (A13 escalation, A14 WWH registers, A15 war logic, A16 method over mythology, A17 behavior over biography, A18 the opening ladder, A19 the payload corpus depth law + the weapons-vault release gate + the vault accuracy bench; full binding text in references/charter.md), bundle map, autonomy + execution + war doctrines, quality gates. |
| [glm-self-model](skills/glm-self-model/) | 1.1.1 | The engine layer — five truths, failure geometry E1–E8, compensation gates G1–G4; the engine grades its own manual (M1–M5). |
| [mythos-bug-hunter](skills/mythos-bug-hunter/) | 4.8.0 | The spine — R0–R7 canon, ledger, hypothesis grammar, closure gates, mission horizon; carries the Jason Haddix lineage layer (methodology preservation: pin, split, gate, classify, prove, drift-audit), the mechanized Hypothesis Contract (register / close / list — retrodiction refused), and the A18 opening ladder (the onboarding question set that writes preservation rows first). |
| [mythos-code-audit](skills/mythos-code-audit/) | 1.0.0 | White-box source audit — static analysis proposes, the runtime disposes. Calibrated by rediscovering CVE-2024-33663/33664. |
| [mythos-proving-ground](skills/mythos-proving-ground/) | 1.2.0 | Ground-truth benchmark — instrumented lab, server-side triggers, scores coverage/precision/hallucination/harm; since v1.1.0 the same doctrine scores the weapons vault itself (the labeled release/refusal bench, `payload_bench`), and since v1.2.0 the bench is multilingual (override phrasings and clean basis notes across ten languages). |
| [aas-catalog](skills/aas-catalog/) | 1.0.1 | Search & install from the Agentic Awesome Skills catalog — one reviewed skill per install, risk-gated. |

### Tier 1 — Recon & Mapping (5)

| Skill | Version | What it does |
|---|---|---|
| [surface-cartographer](skills/surface-cartographer/) | 1.0.0 | The attack-surface dossier — asset graph, 21-class taxonomy, priority queue. |
| [subdomain-hunter](skills/subdomain-hunter/) | 2.3.0 | Passive-first enumeration, wildcard verdicts, takeover signatures; the taxonomy-first opening ladder (EdOverflow lineage). |
| [content-discovery](skills/content-discovery/) | 2.3.0 | Calibrated content walks, 404-baseline controls, backup/config triage; the family-is-the-hypothesis opening ladder (Miessler lineage). |
| [js-recon](skills/js-recon/) | 1.0.0 | JS bundle analysis — endpoints, commented routes, sourcemaps, masked secrets. |
| [api-surface-mapper](skills/api-surface-mapper/) | 1.0.0 | API spec discovery, version diffs, undocumented endpoints, GraphQL. |

### Tier 2 — Access & Logic (3)

| Skill | Version | What it does |
|---|---|---|
| [auth-boundary-mapper](skills/auth-boundary-mapper/) | 2.4.0 | Role×resource matrix, IDOR/BOLA differentials; the identifier-construction opening ladder (Frans Rosen lineage). |
| [oauth-flow-auditor](skills/oauth-flow-auditor/) | 2.4.0 | OAuth/OIDC checks with falsifiers; the client-inventory opening ladder (Aaron Parecki lineage, RFC 9700 vocabulary). |
| [business-logic-hunter](skills/business-logic-hunter/) | 2.4.0 | Workflow abuse, rate-floored races, parameter tampering; the enforcement-census opening ladder (Soroush Dalili lineage). |

### Tier 3 — Deep Technical (7)

| Skill | Version | What it does |
|---|---|---|
| [injection-lab](skills/injection-lab/) | 1.5.0 | Injection differential oracles — sqlmap runs as oracle only, census before any battery; the corpus carries the NoSQL, command, and SSTI detection families, and the extreme tier (MSSQL stacked-WAITFOR time-based differential, INJ-016) rides the weapons vault (A19). |
| [ssrf-playbook](skills/ssrf-playbook/) | 1.6.0 | SSRF channel proofs via canary callbacks, bounded egress checks; the four-rung channel ladder; loopback-name and IPv6 families in the corpus (A19); the credential-bearing metadata seams (IMDSv2 token dance, Azure managed-identity token, GCP service-account token) behind the weapons vault (A19e). |
| [xss-playbook](skills/xss-playbook/) | 2.7.0 | Sink-context analysis, marker proofs, the mXSS layer; the context-first opening ladder (Mario Heiderich lineage); every grammar-table context class corpus-backed, and the extreme mutation class (namespace-confusion mXSS, XSS-016) rides the weapons vault (A19). |
| [cloud-config-auditor](skills/cloud-config-auditor/) | 2.4.0 | CORS matrix, anonymous storage, takeover checks as code; where-drift-is-born ladder (Prowler / de la Fuente lineage). |
| [mobile-hunter](skills/mobile-hunter/) | 1.3.0 | Mobile teardown — the shipped APK/IPA read before the device is touched; the confession opening ladder (Charlie Miller lineage). |
| [cache-playbook](skills/cache-playbook/) | 1.6.0 | Cache deception & poisoning — the cache-key baseline matrix; the disagreement-first opening ladder (Omer Gil + James Kettle corpus); the delimiter second edition in the corpus (A19); the smuggled poison and deception chains behind the weapons vault (A19e). |
| [prototype-playbook](skills/prototype-playbook/) | 1.6.0 | Prototype pollution, DOM clobbering, postMessage confusion — source → gadget → sink; the merge-surface-first opening ladder (Gareth Heyes lineage); clobber probe families and the postMessage shell in the corpus (A19); the browser gadget seams (fetch body default, GTM sequence eval) behind the weapons vault (A19e). |

### Tier 4 — Incident Branch (2)

| Skill | Version | What it does |
|---|---|---|
| [adversary-tracker](skills/adversary-tracker/) | 1.3.0 | Event-triggered hunts — the Shimomura Binary Brain: halving loop, two-channel confirmation, audited handoff; the A18 opening ladder writes sensor / baseline / null / correlation / freeze / quarantine rows before any traffic is generated. |
| [php2shell-forensics](skills/php2shell-forensics/) | 1.0.0 | Live-event incident forensics — the php2shell assessment arc (CVE-2026-109618/109619, PHP core memory safety, disclosed 2026-10-21): hidden-PHP inventory, version/SAPI triage (mod_php highest risk), the four passive disclosure signals (PHPSESSID cookie oracle), the convergent behavioral hunt, planted-script forensics, patch verification — detection corpus byte-exact from Wiz/Elastic/Huntress/the php-src advisories. |

### Tier 5 — Craft Lineages (10)

| Skill | Version | What it does |
|---|---|---|
| [scan-economist](skills/scan-economist/) | 1.3.0 | Scan economy — liveness before depth, priors over exhaustive sweeps; the map-confesses ladder (Fyodor lineage). |
| [module-smith](skills/module-smith/) | 1.3.0 | Hypotheses as rankable reusable modules; access and impact proofs separate; the hypothesis-as-module opening ladder (HD Moore lineage). |
| [pipeline-smith](skills/pipeline-smith/) | 1.3.0 | Unix recon pipelines — passive first, dedupe before paying; pattern-as-hypothesis ladder (Tomnomnom lineage). |
| [feedback-fuzzer](skills/feedback-fuzzer/) | 1.3.0 | Feedback-guided search — bucketed novelty, minimization before diagnosis; the map-first opening ladder (lcamtuf lineage). |
| [template-scanner](skills/template-scanner/) | 1.3.0 | Detection as declarative templates, matchers pre-registered; fingerprint-to-template ladder (ProjectDiscovery lineage). |
| [packet-orchestrator](skills/packet-orchestrator/) | 1.3.0 | Manual first, then state-backed automation; packet differentials show their bytes; the capture-first opening ladder (Searle + Mantis + Scapy lineages). |
| [protocol-forensics](skills/protocol-forensics/) | 1.2.0 | Spec ambiguity hunted across the implementation population; entropy-priced invariants; the class-first opening ladder (Dan Kaminsky lineage). |
| [interior-cartographer](skills/interior-cartographer/) | 1.2.0 | OS internal-surface census, seam tables, ACCESS_MASK budget; the unpriced-seam opening ladder (James Forshaw lineage). |
| [harness-smith](skills/harness-smith/) | 1.1.0 | Fuzz-first triage and oracle engineering; the mandatory missed-why postmortem; the parser-census opening ladder (Tavis Ormandy lineage). |
| [opsec-discipline](skills/opsec-discipline/) | 1.1.0 | Campaign hygiene as an economic discipline — exposure census, compartmentation, closure audit; the exposure-pricing opening ladder (the grugq lineage). |

### Tier 6 — Legend Tier (9)

| Skill | Version | What it does |
|---|---|---|
| [chain-architect](skills/chain-architect/) | 1.3.0 | Compound kill chains — low findings composed into one critical impact; the architecture-first opening ladder (Orange Tsai lineage). |
| [desync-hunter](skills/desync-hunter/) | 1.7.0 | Protocol asymmetry — one ambiguity per request, byte-exact artifacts; the parsing-chain-first opening ladder (James Kettle lineage); header-name, obs-fold, absolute-form classes in the corpus (A19); the H2.TE and 0.CL gadget seams behind the weapons vault (A19e). |
| [deep-teardown](skills/deep-teardown/) | 1.3.0 | Client artifacts dismantled to primitives, local before any network flow; the read-it-first opening ladder (George Hotz lineage). |
| [ghost-crawler](skills/ghost-crawler/) | 1.3.0 | Passive-index misconfig hunting — one bounded probe per candidate; the neglect ladder (Adrian Lamo lineage). |
| [mirror-hunter](skills/mirror-hunter/) | 1.3.0 | LLM/agent surfaces where the target runs the hunter's engine class; the surface-census opening ladder (Simon Willison lineage). |
| [probe-smith](skills/probe-smith/) | 1.1.0 | Hardware teardown — pinout discovery, priced bypass ladder, radio promiscuity; the interface-census opening ladder (Travis Goodspeed lineage). |
| [signal-smith](skills/signal-smith/) | 1.4.0 | Input grammar and precision signals — never trip the alarm; the listen-first opening ladder (John Draper lineage); the variation corpus carries every cataloged seam class byte-exact and attributed (A19). |
| [threshold-hunter](skills/threshold-hunter/) | 1.1.0 | Physical trust boundaries at the information layer; detection as the deliverable; the second-reading opening ladder (Deviant Ollam lineage). |
| [trust-graph-hunter](skills/trust-graph-hunter/) | 1.4.0 | Inherited privilege across the trust graph; the AD directory interior; the trust-edge-census opening ladder (Mitnick + Metcalf lineages). |

### Tier 7 — Forge & Competition (2)

| Skill | Version | What it does |
|---|---|---|
| [lineage-smith](skills/lineage-smith/) | 1.10.0 | The assimilation factory — scored selection, complete-corpus census, the five-lens psych-read, forge under the authoring contract. The candidate queue is retired: 8 of 8 executed. The forge tier's runtime (forge-os.md) carries the nomination-reading opening ladder (A18). |
| [rival-playbook](skills/rival-playbook/) | 1.2.0 | Corpus-vs-corpus competition — date-pinned rival census, hollow map, proving-ground duel with capped wording (Sun Tzu lineage). The forge tier's runtime (forge-os.md) carries the census-reading opening ladder (A18). |

### Prompts

| Prompt | Version | What it does |
|---|---|---|
| [terse-core](prompts/terse-core/system-prompt-v1.md) | 1.0 | Output-token discipline system prompt — static cache-friendly core + dynamic PAYLOAD slot. |

## Doctrine

1. **Evidence-cited claims.** No finding without a captured artifact.
2. **Pre-registered hypotheses.** Declare what would falsify a claim *before* testing it.
3. **Differential oracles.** Static analysis proposes, the runtime disposes.
4. **Auditable output.** Every skill ships with an auditor or a ground-truth benchmark.
5. **Zero slop.** No unverified findings, no AI-generated filler, no generic advice.

## Authorization notice

The security skills in this repo are for **authorized targets only** — bug bounty programs with a defined scope, contracted pentest engagements, CTF labs, and your own infrastructure. Unauthorized testing is illegal in most jurisdictions, including under Indonesia's UU ITE. The skills enforce this themselves: they refuse to operate without explicit authorization.

## Building skills here

New skills are built under the house authoring discipline, not freehand — see [CONTRIBUTING.md](CONTRIBUTING.md): observed friction before authoring, required frontmatter with trigger phrases, progressive disclosure, minimal-but-complete scope, and a hard validation gate before every commit:

```bash
python3 scripts/validate_skill.py skills/<skill-name>
```

This repository ships original work only — nothing is vendored from third parties.

## License

MIT — see [LICENSE](LICENSE).
