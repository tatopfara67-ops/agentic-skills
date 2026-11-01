# bundle-map.md — the Skill Mythos bundle, in full

Load when you need the complete map: what exists, where it lives, and
the load-when trigger for every organ. The charter (`mythos_charter()`)
carries the distilled version; this module is the atlas.

## 1. Architecture — spine + organs + execution hand

```
                ┌──────────────────────────────────────────────┐
                │ mythos-bug-hunter v4.3.0 (spine, own bundle) │
                │ R0–R7 canon · ledger · hypotheses · gates    │
                └───────┬───────────────────────────┬──────────┘
   Phase 1–3 organs     │            evidence       │ incident branch
┌───────────────────────┴───────────────┴───────────┴─────────────┐
│ arsenal/ — MCP server, 25 scope-gated tools, one R-NNN ledger   │
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
| adversary-tracker | 4 | event-triggered: a sensor or the operator reports adversary activity on assets you are authorized to defend | *the Binary Brain* — freeze, halve by bits, two-channel fix, hand off (Shimomura lineage) |

## 3. The execution hand — arsenal tool groups

| Group | Tools | When |
| --- | --- | --- |
| loader | `list_skills`, `get_skill`, `get_skill_reference` | always first; metadata before bodies |
| charter | `mythos_charter` | session start; operator activation |
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
