# mythos-arsenal

The specialized **organs + execution hand** for the Mythos agent stack:
the **skill-mythos master charter** plus 25 organ skills — recon,
mapping, access, logic, technical deep-dive, the incident branch, the
**craft tier** (six organs distilled from named public researchers:
Fyodor, HD Moore, Tomnomnom, lcamtuf, ProjectDiscovery, Searle +
Mantis/PhonePe), and the **legend tier** (six organs distilled from the
operator's Tier-S/A/B list: Orange Tsai, James Kettle, George Hotz,
Adrian Lamo, John Draper, Kevin Mitnick — plus the Frans Rosen lineage
folded into auth-boundary-mapper v2) — and a scope-gated MCP server
that executes them with an append-only evidence ledger and **A13 prompt
escalation** (`doctrine_forge`: any operator instruction, however terse,
becomes an explicit doctrine order before any organ acts).

The bundle's identity, autonomy contract, and quality standard live in
**skills/skill-mythos/SKILL.md** — the activation module, formalized from
the operator's charter instruction: extreme expertise over generality,
legitimate assimilation of public methodologies, autonomous organ
selection bounded by scope and ledger, and triage-grade findings
(zero false positives, fully reproducible, CVSS 3.1 + Bugcrowd VRT /
HackerOne classification on every confirmed report line). The
assimilated lineages — figures, distillations, consulted sources, and
attribution corrections on record — are enumerated by the
`mythos_lineages` tool.

Designed as **Spine + Organs**: `mythos-bug-hunter` stays the single
discipline layer (ledger, hypothesis grammar, closure gates); every skill
here is an organ that plugs into one of its phases and inherits its
contracts instead of duplicating them.

```
                 ┌────────────────────────────────────────────┐
                 │  mythos-bug-hunter (spine, not included)   │
                 │  R0–R7 canon · ledger · hypotheses · gates │
                 └───────┬──────────────────────────┬─────────┘
      Phase 1           │ Phase 2/3                │ evidence
┌───────────────────────┴───────────┴──────────────┴──────────┐
│ arsenal/  MCP server — 27 tools, every one scope-gated      │
│   charter: mythos_charter, mythos_lineages,                 │
│            doctrine_forge (A13 prompt escalation)           │
│   passive : ct_subdomains, dns_resolve                       │
│   active : http_probe, content_discover, api_introspect,    │
│            js_analyze                                       │
│   map    : dossier_add, dossier_render, dossier_summary     │
│   brain  : sbb_declare, sbb_decide, sbb_apply               │
│            (Shimomura Binary Brain — adversary-tracker)     │
│   report : cvss3_score, vrt_classify (CVSS 3.1 + Bugcrowd   │
│            VRT + HackerOne crosswalk, official taxonomy)    │
│   hand   : arsenal_route (CLI allowlist + flag blacklist)   │
│   gov    : scope_check, auth_status, ledger_* , list/get_skill │
└─────────────────────────────────────────────────────────────┘
```

## Skill index

| Tier | Skill | Plugs into |
| --- | --- | --- |
| 0 Master | skill-mythos | activation module: thirteen charter articles (incl. A13 prompt escalation), bundle map, autonomy protocol, triage-grade quality gates (CVSS 3.1 + VRT/HackerOne classification) — loads first, hunts nothing |
| 1 Recon & Mapping | surface-cartographer | Phase 1 — the organized dossier (asset graph, 21-class taxonomy, priority queue) |
| 1 | subdomain-hunter | Phase 1 — passive-first enumeration, wildcard verdicts, takeover pairs |
| 1 | content-discovery | Phase 1/3 — calibrated walks, backup/config triage |
| 1 | js-recon | Phase 1/2 — bundle analysis, commented routes, masked secrets |
| 1 | api-surface-mapper | Phase 1/2 — spec parsing, version diffs, undocumented endpoints |
| 2 Access & Logic | auth-boundary-mapper | Phase 2/3 — role×resource matrix, IDOR/BOLA differentials; v2 folds in the Frans Rosen lineage (identifier construction, every parameter position, 2nd-order IDOR, tenant slices) |
| 2 | oauth-flow-auditor | Phase 2/3 — 12-check catalog with falsifiers |
| 2 | business-logic-hunter | Phase 2/3 — workflow abuse, races with rate floors |
| 3 Deep technical | injection-lab | Phase 3 — differential oracles; sqlmap as oracle only |
| 3 | ssrf-playbook | Phase 3 — canary-callback channel proofs, bounded egress |
| 3 | xss-playbook | Phase 3 — sink contexts, marker proofs, CSP as fact |
| 3 | cloud-config-auditor | Phase 1/3 — CORS matrix, anonymous storage (bounded), takeover checks |
| 4 Incident branch | adversary-tracker | event-triggered, any phase — the Shimomura Binary Brain: freeze, halve by bits, two-channel fix, handoff (distilled from the 1994–95 hunt that ended in Raleigh) |
| 5 Craft lineage | scan-economist | the Fyodor lineage: scan economy — cost hierarchy, technique triangle, states as inferences, priors over exhaustiveness, adaptive pacing (Phrack 51, read in full) |
| 5 | module-smith | the HD Moore lineage: hypotheses as rankable reusable modules; access and impact proofs separate; exposure is a measurement with a denominator (Metasploit architecture, Project Sonar) |
| 5 | pipeline-smith | the Tomnomnom lineage: Unix recon pipelines — passive first, dedupe before probes, pattern packs as data, diff to decide (assetfinder/httprobe/gf/meg/gron) |
| 5 | feedback-fuzzer | the lcamtuf lineage: feedback-guided search — state maps, bucketed novelty, curated corpora, minimization, saturation as the stop rule (AFL design doc, read in full) |
| 5 | template-scanner | the ProjectDiscovery lineage: detection as declarative templates — matchers pre-registered, packs versioned, campaigns cite their set (Sandeep Singh, Rishiraj Sharma, Marco Rivoli, Nizamul Rana) |
| 5 | packet-orchestrator | the Searle + Mantis lineage: manual first, then layer-by-layer translation into state-backed automation; packet differentials show their bytes (attribution corrected on record) |
| 6 Legend tier | chain-architect | the Orange Tsai lineage (Tier S): the compound kill chain — low-severity primitives composed into critical impact, every link proven by its own differential (the ProxyLogon pattern) |
| 6 | desync-hunter | the James Kettle lineage (Tier S): protocol & specification asymmetry — parser-seam ambiguities one per request, bytes as artifacts, timing stays a lead |
| 6 | deep-teardown | the George Hotz lineage (Tier S): dismantle client artifacts to primitives — JS/APK/binary ladders, local data flow before network flow, secrets masked |
| 6 | ghost-crawler | the Adrian Lamo lineage (Tier A): enter without knocking — passive-index misconfig hunting, one bounded probe per candidate, main app untouched (authorized translation on record) |
| 6 | signal-smith | the John Draper lineage (Tier B): input grammar and precision signal craft — calibrate the filter, forge ONE minimal variation, two per seam max, never an alarm |
| 6 | trust-graph-hunter | the Kevin Mitnick lineage (Tier B, systems edition): the trust graph between components — forgeable context, inherited privilege, operator-owned ends only |

All 26 pass `scripts/validate_skill.py` from the agentic-skills repo —
drop-in compatible with its CONTRIBUTING workflow.

## Install & wiring

```bash
pip install "mcp>=1.2.0"        # FastMCP SDK
python3 arsenal/server.py --selftest   # should list 27 tools
```

`.mcp.json` (Claude Code / Cursor), adjusting the path:

```json
{
  "mcpServers": {
    "mythos-arsenal": {
      "command": "python3",
      "args": ["/absolute/path/to/mythos-arsenal/arsenal/server.py"]
    }
  }
}
```

Copy `CLAUDE.md` to the workspace root — it is the agent contract that
makes the tools get used in discipline (MCP serves; the contract steers).

Environment overrides: `MYTHOS_ARSENAL_ROOT` (package root, default:
server.py's parent), `MYTHOS_ARSENAL_SCOPE` (scope.csv path),
`MYTHOS_ARSENAL_ENGAGEMENTS` (engagement state dir), `MYTHOS_ARSENAL_SKILLS`.

## Authorization — scope.csv (deny-by-default)

```
target,class,auth_artifact,issued,expires,operator,notes
127.0.0.1,in_scope,self-owned lab declaration (lab/target_app.py),...
*.example.com,recon_only,https://hackerone.com/example,..,2027-01-31,..
```

* classes: `in_scope` (full testing), `recon_only` (passive sources),
  `denied` (explicit refusal — always wins)
* `auth_artifact` must be non-empty: bug-bounty scope page, engagement
  letter, or self-owned lab declaration. No artifact, no traffic (R0).
* domains cover subdomains; rows may also be IP, CIDR, host:port, or a
  URL prefix. Unknown targets are refused and the refusal is ledgered.
* The server never writes this file — it is operator-writable only.

## Try it safely (self-owned lab)

```bash
python3 lab/target_app.py 8477 &          # synthetic target on localhost
python3 arsenal/server.py                 # start the MCP server
# then, as the agent: auth_status() → http_probe / robots.txt →
# content_discover → js_analyze → api_introspect → dossier_add → dossier_render
```

The complete run, captured from a live session, is in
`examples/worked-engagement/`: `TRANSCRIPT.md` (every tool call and its
real output), `ledger/records.md` (548 records), `dossier.md` (the
organized map), and `report.md` (audited PASS by `auditor/audit_report.py`).

## Try the Binary Brain (self-owned synthetic hunt)

```bash
MYTHOS_ARSENAL_ROOT=/tmp/christmas-lab \
  python3 lab/christmas_lab.py     # 8 hypotheses, 3 bits, two channels
python3 auditor/audit_report.py \
  /tmp/christmas-lab/engagements/christmas-lab/HANDOFF.md    # PASS
```

A captured run — transcript, engine state, ledger, and the audited
handoff pack — lives in `examples/adversary-hunt/`.

## Tests

```bash
python3 -m unittest discover -s arsenal/tests    # 100 tests
```

Covers: scope-gate matching (suffix/CIDR/host:port/URL-prefix/recon_only/
denied/expired/missing-artifact), ledger append-only discipline, tool
behavior against a live lab (refusals, calibration, extraction, masking,
dossier evidence validation), and arsenal_route governance (allowlist,
flag blacklist, sqlmap `--batch` rule, scope refusal), and the Binary
Brain engine (null auto-insert, partition validation, information-gain
ranking, pre-registration idempotence, tip-off gating, two-channel
confirmation, falsified-space MISTAKE, mid-hunt extension, convergence
at the log2 floor), the CVSS v3.1 engine (FIRST published example
scores, PR-scope coupling, severity bands, malformed-vector refusals),
vrt_classify (variant selection, taxonomy resolution, HackerOne
crosswalk, template shaping), the charter payload (thirteen articles,
the seven-tier registry, the A13 prompt-escalation contract), the
lineage registry (fourteen lineages, verified figures, corrections on
record), the doctrine_forge engine (the operator's own Indonesian
example phrasings, every intent class, severity/quota extraction,
quota discipline, verbatim preservation, determinism), and the
hardened report gates (cvss score recomputation, unknown VRT ids,
missing reproduction, incident-handoff exemption, strict block
boundaries).

## Layout

```
mythos-arsenal/
├── CLAUDE.md            agent contract (the enforcement MCP can't provide;
│                        A13: doctrine_forge runs before every instruction)
├── scope.csv            authorization registry — operator-writable only
├── arsenal/             MCP server + tools + engine (sbb.py, cvss.py) + tests
├── skills/              skill-mythos master charter + 25 organ skills
│                        (validator-compatible; VRT data: Apache-2.0, NOTICE.md;
│                        craft tier: 6 organs with per-organ sources.md;
│                        legend tier: 6 organs with per-organ sources.md, plus
│                        the Rosen lineage folded into auth-boundary-mapper v2)
├── auditor/             audit_report.py — PASS/FAIL report gate (recomputes
│                        CVSS, validates VRT ids against the shipped taxonomy)
├── lab/                 target_app.py + christmas_lab.py (self-owned)
└── examples/            worked-engagement/ + adversary-hunt/ (audited PASS)
```

## Merging into the agentic-skills repo

1. `skills/*` → `agentic-skills/skills/` (each bundle is self-contained;
   run the repo's own `scripts/validate_skill.py skills/<name>` to confirm).
2. `arsenal/`, `auditor/`, `lab/`, `examples/` are new top-level dirs,
   like the existing `agent/` and `prompts/`.
3. Keep `CLAUDE.md` at whatever workspace the MCP server serves.

## Doctrine & safety

* Authorized targets only: bug-bounty programs with defined scope,
  contracted engagements, CTF labs, self-owned infrastructure.
* Evidence-first: every claim cites a ledger record; surfaces without
  records are structurally impossible (`dossier_add` enforces it).
* Bounded proofs: one page, one canary, one transaction — then stop.
* Secrets are report-only and masked in context, always.
* The flag blacklist on `arsenal_route` is deliberate: destructive modes
  belong to manual operator sessions, not to an agent loop.
