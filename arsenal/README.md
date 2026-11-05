# mythos-arsenal

The MCP execution layer for this repo's skill stack: `arsenal/server.py` (FastMCP) serves **30 scope-gated tools** that execute the skill-mythos charter, the mythos-bug-hunter spine's contracts (append-only ledger, the v4.7.0 hypothesis rail, closure gates), the glm-self-model engine manual, and the organ skills — under one authorization registry ([`scope.csv`](../scope.csv), deny-by-default) and one append-only evidence ledger. `doctrine_forge` (A13) expands any operator instruction, however terse, into an explicit doctrine order before any organ acts.

The bundle's identity and quality standard live in [skills/skill-mythos/SKILL.md](../skills/skill-mythos/SKILL.md); the assimilated lineage registry (33 entries, corrections on record) is served by the `mythos_lineages` tool. Designed as **spine + organs**: `mythos-bug-hunter` stays the single discipline layer (ledger, hypothesis grammar, closure gates — mechanized since v4.7.0); every other skill is an organ that plugs into one of its phases and inherits its contracts instead of duplicating them.

## Skill index

The phase-routing view; the full 43-bundle catalog with versions is the
root `README.md`'s skill catalog.

| Tier | Skill | Plugs into |
| --- | --- | --- |
| 0 Master | skill-mythos | activation: seventeen charter articles (incl. A13), bundle map, autonomy protocol, quality gates — loads first, hunts nothing |
| 0 Engine | glm-self-model | session start of any long engagement — model-class failure geometry + compensation gates for the agent that runs every organ |
| 1 Recon & Mapping | surface-cartographer | Phase 1 — the dossier: asset graph, 21-class taxonomy, priority queue |
| 1 | subdomain-hunter | Phase 1 — passive-first enumeration, wildcard verdicts, takeover pairs; v2: EdOverflow dangling classes |
| 1 | content-discovery | Phase 1/3 — calibrated walks, backup/config triage; v2: Miessler corpus families |
| 1 | js-recon | Phase 1/2 — bundle analysis, commented routes, masked secrets |
| 1 | api-surface-mapper | Phase 1/2 — spec parsing, version diffs, undocumented endpoints |
| 2 Access & Logic | auth-boundary-mapper | Phase 2/3 — role×resource matrix, IDOR/BOLA differentials; v2: Rosen identifier-construction lineage |
| 2 | oauth-flow-auditor | Phase 2/3 — flow checks with falsifiers; v2: Parecki redirect_uri/state/PKCE matrix, RFC 9700 |
| 2 | business-logic-hunter | Phase 2/3 — workflow abuse, races with rate floors; v2: Dalili reshaping grammar |
| 3 Deep technical | injection-lab | Phase 3 — differential oracles; sqlmap as oracle only; versioned oracle corpus |
| 3 | ssrf-playbook | Phase 3 — canary-callback channel proofs, bounded egress |
| 3 | xss-playbook | Phase 3 — sink contexts, marker proofs, CSP as fact; v2: Heiderich mXSS layer + versioned mXSS corpus |
| 3 | cloud-config-auditor | Phase 1/3 — CORS matrix, anonymous storage, takeover checks; v2: Prowler checks-as-code |
| 3 | mobile-hunter | Phase 1/3 — the shipped APK/IPA read before the device is touched (Charlie Miller lineage) |
| 3 | cache-playbook | Phase 3 — cache-key baseline matrix for deception/poisoning (Omer Gil + James Kettle corpus) |
| 3 | prototype-playbook | Phase 3 — prototype pollution, DOM clobbering, postMessage: source → gadget → sink (Gareth Heyes lineage) |
| 4 Incident branch | adversary-tracker | event-triggered, any phase — the Shimomura Binary Brain: freeze, halve, two-channel fix, handoff |
| 5 Craft lineage | scan-economist | Fyodor — scan economy: cost hierarchy, priors, adaptive timing |
| 5 | module-smith | HD Moore — hypotheses as rankable modules; access/impact proofs separate |
| 5 | pipeline-smith | Tomnomnom — Unix recon pipelines: passive first, dedupe, pattern packs |
| 5 | feedback-fuzzer | lcamtuf — feedback-guided search: bucketed novelty, saturation stop rule |
| 5 | template-scanner | ProjectDiscovery — detection as declarative templates, matchers pre-registered |
| 5 | packet-orchestrator | Searle + Mantis — manual first, then state-backed automation |
| 5 | protocol-forensics | Dan Kaminsky — spec ambiguity across the implementation population, entropy-priced invariants |
| 5 | interior-cartographer | James Forshaw — OS internal-surface census, seam tables, ACCESS_MASK budget |
| 5 | harness-smith | Tavis Ormandy — fuzz-first triage, oracle engineering, the mandatory missed-why postmortem |
| 5 | opsec-discipline | the grugq — campaign hygiene as an economic discipline: exposure census, compartmentation, closure audit |
| 6 Legend tier | chain-architect | Orange Tsai (S) — compound kill chains, every link proven by its own differential |
| 6 | desync-hunter | James Kettle (S) — parser-seam ambiguities one per request, bytes as artifacts |
| 6 | deep-teardown | George Hotz (S) — client artifacts dismantled locally to primitives |
| 6 | ghost-crawler | Adrian Lamo (A) — passive-index misconfig hunting, one bounded probe per candidate |
| 6 | mirror-hunter | Simon Willison (S) — LLM/agent surfaces: self-model inverted into attack surface, eligibility gate before the first payload, rates over N runs, CONFIRMED on the deterministic wrapper |
| 6 | signal-smith | John Draper (B) — input grammar craft, one minimal variation per seam, two max |
| 6 | trust-graph-hunter | Kevin Mitnick (B) — the trust graph between components, inherited privilege on operator-owned ends |
| 6 | probe-smith | Travis Goodspeed — hardware teardown: pinout discovery, priced bypass ladder, radio promiscuity |
| 6 | threshold-hunter | Deviant Ollam — physical trust boundaries at the information layer; detection as the deliverable |
| 7 Forge | lineage-smith | the assimilation factory — scored selection, complete-corpus census, the five-lens psych-read |
| 7 | rival-playbook | corpus-vs-corpus competition — date-pinned rival census, proving-ground duel with capped wording |

All 43 bundles in `skills/` pass `scripts/validate_skill.py --all`.

## Install & wiring

```bash
pip install "mcp>=1.2.0"        # FastMCP SDK
python3 arsenal/server.py --selftest   # should list 30 tools
```

`.mcp.json` (Claude Code / Cursor), adjusting the path:

```json
{
  "mcpServers": {
    "mythos-arsenal": {
      "command": "python3",
      "args": ["/absolute/path/to/agentic-skills/arsenal/server.py"]
    }
  }
}
```

Copy `CLAUDE.md` to the workspace root — MCP serves the tools; the contract steers the agent.

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
  `denied` (explicit refusal — always wins), `canary` (the operator's
  OWN callback collector — reachable only via `http_probe(canary=True)`:
  GET-only, no body, no query string, bounded path; out-of-band canary
  verification can never double as an exfiltration channel)
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
organized map), and `report.md` (audited PASS by `auditor/audit_report.py`
— grounded against the sibling `ledger/` automatically: every cited
R-NNN exists and the claim lines share surface vocabulary with the
records they cite).

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
python3 -m unittest discover -s arsenal/tests    # 161 tests
```

Scope-gate matching (suffix/CIDR/host:port/URL-prefix/recon_only/denied/canary/expired/missing-artifact, canary exfil-channel refusal), ledger append-only discipline + O(1) id minting (tail-scan with full-scan fallback, portable cross-platform lock), the v4.7.0 hypothesis rail (pre-registration refusals, three-state closure, the retrodiction guard), tool behavior against a live lab, `arsenal_route` governance + civility rate defaults, the Binary Brain engine, the CVSS 3.1 engine, `vrt_classify` + HackerOne crosswalk, the charter payload, the lineage registry, `doctrine_forge`, and the hardened report gates — including citation grounding (fabricated / misdirected / non-evidence citations fail the audit).

## Layout

The server lives inside the agentic-skills repo; its working set:

```
CLAUDE.md        agent contract (A13: doctrine_forge before every instruction)
scope.csv        authorization registry — operator-writable only
arsenal/         this server: tools + engines (sbb.py, cvss.py) + tests
auditor/         audit_report.py — PASS/FAIL report gate (recomputes CVSS,
                 validates VRT ids against the shipped taxonomy, and
                 grounds citations: fabricated, borrowed, misdirected, or
                 non-evidence-tag citations fail the report)
lab/             target_app.py + christmas_lab.py (self-owned)
examples/        worked-engagement/ + adversary-hunt/ (audited PASS)
```

The full repo map (skills, agent, prompts) is in the root `README.md`.

## Doctrine & safety

* Authorized targets only: bug-bounty programs with defined scope,
  contracted engagements, CTF labs, self-owned infrastructure.
* Evidence-first: every claim cites a ledger record; surfaces without
  records are structurally impossible (`dossier_add` enforces it).
* Bounded proofs: one page, one canary, one transaction — then stop.
* Secrets are report-only and masked in context, always.
* The flag blacklist on `arsenal_route` is deliberate: destructive modes
  belong to manual operator sessions, not to an agent loop.
