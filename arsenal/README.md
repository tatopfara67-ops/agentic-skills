# mythos-arsenal

The specialized **organs + execution hand** for the Mythos agent stack:
13 skills (recon, mapping, access, logic, technical deep-dive, and the
incident branch) plus a scope-gated MCP server that executes them with
an append-only evidence ledger.

Designed as **Spine + Organs**: `mythos-bug-hunter` stays the single
discipline layer (ledger, hypothesis grammar, closure gates); every skill
here is an organ that plugs into one of its phases and inherits its
contracts instead of duplicating them.

```
                 ┌────────────────────────────────────────────┐
                 │  mythos-bug-hunter (spine, skills/mythos-  │
                 │  bug-hunter) — R0–R7 canon · ledger ·      │
                 │  hypotheses · gates                        │
                 └───────┬──────────────────────────┬─────────┘
      Phase 1           │ Phase 2/3                │ evidence
┌───────────────────────┴───────────┴──────────────┴──────────┐
│ arsenal/  MCP server — 22 tools, every one scope-gated      │
│   passive: ct_subdomains, dns_resolve                       │
│   active : http_probe, content_discover, api_introspect,    │
│            js_analyze                                       │
│   map    : dossier_add, dossier_render, dossier_summary     │
│   brain  : sbb_declare, sbb_decide, sbb_apply               │
│            (Shimomura Binary Brain — adversary-tracker)     │
│   hand   : arsenal_route (CLI allowlist + flag blacklist)   │
│   gov    : scope_check, auth_status, ledger_* , list/get_skill │
└─────────────────────────────────────────────────────────────┘
```

## Skill index

| Tier | Skill | Plugs into |
| --- | --- | --- |
| 1 Recon & Mapping | surface-cartographer | Phase 1 — the organized dossier (asset graph, 21-class taxonomy, priority queue) |
| 1 | subdomain-hunter | Phase 1 — passive-first enumeration, wildcard verdicts, takeover pairs |
| 1 | content-discovery | Phase 1/3 — calibrated walks, backup/config triage |
| 1 | js-recon | Phase 1/2 — bundle analysis, commented routes, masked secrets |
| 1 | api-surface-mapper | Phase 1/2 — spec parsing, version diffs, undocumented endpoints |
| 2 Access & Logic | auth-boundary-mapper | Phase 2/3 — role×resource matrix, IDOR/BOLA differentials |
| 2 | oauth-flow-auditor | Phase 2/3 — 12-check catalog with falsifiers |
| 2 | business-logic-hunter | Phase 2/3 — workflow abuse, races with rate floors |
| 3 Deep technical | injection-lab | Phase 3 — differential oracles; sqlmap as oracle only |
| 3 | ssrf-playbook | Phase 3 — canary-callback channel proofs, bounded egress |
| 3 | xss-playbook | Phase 3 — sink contexts, marker proofs, CSP as fact |
| 3 | cloud-config-auditor | Phase 1/3 — CORS matrix, anonymous storage (bounded), takeover checks |
| 4 Incident branch | adversary-tracker | event-triggered, any phase — the Shimomura Binary Brain: freeze, halve by bits, two-channel fix, handoff (distilled from the 1994–95 hunt that ended in Raleigh) |

All 13 pass `scripts/validate_skill.py` — run it from the repo root:
`python3 scripts/validate_skill.py --all` (17 bundles, including the
repo's original four).

## Install & wiring

```bash
pip install -r requirements.txt        # mcp>=1.2.0 (FastMCP SDK)
python3 arsenal/server.py --selftest   # should list 22 tools
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

Copy `CLAUDE.md` (repo root) to the workspace root — it is the agent
contract that makes the tools get used in discipline (MCP serves; the
contract steers).

Environment overrides: `MYTHOS_ARSENAL_ROOT` (package root, default:
the repo checkout — `scope.csv` and `skills/` resolve relative to it),
`MYTHOS_ARSENAL_SCOPE` (scope.csv path),
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
# then, as the agent: auth_status() → http_probe /robots.txt →
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
python3 -m unittest discover -s arsenal/tests    # 48 tests
```

Covers: scope-gate matching (suffix/CIDR/host:port/URL-prefix/recon_only/
denied/expired/missing-artifact), ledger append-only discipline, tool
behavior against a live lab (refusals, calibration, extraction, masking,
dossier evidence validation), arsenal_route governance (allowlist,
flag blacklist, sqlmap `--batch` rule, scope refusal), and the Binary
Brain engine (null auto-insert, partition validation, information-gain
ranking, pre-registration idempotence, tip-off gating, two-channel
confirmation, falsified-space MISTAKE, mid-hunt extension, convergence
at the log2 floor).

## Layout in this repo

This package is merged into the agentic-skills repo — the 13 organ
skills live under `skills/` next to the spine, and the execution hand
lives at the top level:

```
agentic-skills/
├── CLAUDE.md            agent contract (the enforcement MCP can't provide)
├── scope.csv            authorization registry — operator-writable only
├── arsenal/             MCP server + tools + engine (sbb.py) + tests  ← here
├── skills/              13 organ skills + the repo's original four
├── auditor/             audit_report.py — PASS/FAIL report gate
├── lab/                 target_app.py + christmas_lab.py (self-owned)
└── examples/            worked-engagement/ + adversary-hunt/ (audited PASS)
```

`engagements/` (runtime evidence state) is gitignored — it is created
per engagement and never committed.

## Doctrine & safety

* Authorized targets only: bug-bounty programs with defined scope,
  contracted engagements, CTF labs, self-owned infrastructure.
* Evidence-first: every claim cites a ledger record; surfaces without
  records are structurally impossible (`dossier_add` enforces it).
* Bounded proofs: one page, one canary, one transaction — then stop.
* Secrets are report-only and masked in context, always.
* The flag blacklist on `arsenal_route` is deliberate: destructive modes
  belong to manual operator sessions, not to an agent loop.
