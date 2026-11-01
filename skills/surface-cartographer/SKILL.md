---
name: surface-cartographer
version: 1.0.0
type: ai-skill
architecture: package
description: Phase-1 execution organ that turns scattered recon output into ONE organized, prioritized attack-surface dossier — asset graph, 21-class taxonomy, evidence-cited surfaces, priority queue, backlog. Use when the operator asks to map an attack surface, build a target inventory, produce a dossier or asset graph, classify discovered surfaces, or prioritize what to test first ("pemetaan serangan", "surface inventory", "target list", "dossier", "attack surface map").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# surface-cartographer v1.0.0 — The Organized Map

## 0. What This Skill Is — and Is Not

* **Is**: the Phase-1 executor that ends with a single rendered artifact —
  `dossier.md` — where every surface has an ID, a class from the 21-class
  taxonomy, evidence citing ledger records, a reachability verdict, and a
  priority score. It is the answer to "map this target, and make it organized".
* **Is not**: a scanner, a hypothesis engine, or a substitute for the spine.
  It produces the *inventory* that Phase 2 rotates operators across; it does
  not speculate about behavior.

## 1. Inherited Contracts (do not restate, do not weaken)

This organ plugs into **Phase 1 (Recon and surface inventory)** of the
mythos-bug-hunter spine. The following are inherited wholesale:

* The Canon R0–R7 (authorization gate, plan-before-action, finish-or-park,
  gated victory language, no lying, tools-are-not-verdicts, calibrated
  instruments, effort budget).
* Evidence ledger record format and append-only discipline (spine §3).
* Backlog mechanics (spine §4.2): mid-engagement discoveries go to the
  backlog, never the active queue.

Load the spine's conduct and phase-playbook modules at engagement start;
this organ does not duplicate them.

## 2. The 21-Class Taxonomy

Every surface is classified into exactly one class. `dossier_add` enforces
membership mechanically — an unclassifiable surface is a taxonomy gap to
resolve, not a string to invent:

`static-content` · `web-app` · `api-rest` · `api-graphql` · `api-rpc` ·
`admin-console` · `auth-endpoint` · `file-storage` · `redirect-handler` ·
`upload-endpoint` · `websocket` · `job-worker` · `email-handler` ·
`payment-flow` · `search` · `debug-interface` · `deprecated-endpoint` ·
`backup-artifact` · `config-exposure` · `third-party-asset` ·
`ai-agent-surface`

Full definitions, disambiguation rules (api-rest vs api-rpc; backup-artifact
vs config-exposure), and worked classification examples live in
`references/taxonomy.md` — load it once per engagement, before the first
`dossier_add` call.

## 3. Procedure — Numbered Actions

Entry conditions: AUTH record exists in the engagement ledger (R0 — no AUTH,
no work); a program name is chosen; capability inventory was recorded in
Phase 0.

1. **Posture check.** Call `auth_status()`. Read the rows aloud in the
   engagement summary: which targets, which class, which artifact. A row with
   a missing artifact is a stop-and-fix, not a warning.
2. **Resolve, don't assume.** For each in-scope host, call
   `dns_resolve(program, host)`. Wildcard DNS (random-name resolution
   succeeding) is recorded as a FACT with a wildcard note — it changes the
   meaning of every later "live host" claim.
3. **Probe the front door.** `http_probe` the base URL, then `/robots.txt`
   and `/sitemap.xml`. Every Disallow entry in robots.txt is a SURFACE record
   and a dossier candidate — the operator's own map of what they do not want
   touched.
4. **Delegate the sweeps.** Content discovery, JS recon, API discovery, and
   subdomain enumeration are the sibling organs (content-discovery, js-recon,
   api-surface-mapper, subdomain-hunter). Call them; this organ consumes
   their findings, it does not re-implement them.
5. **Classify.** For each finding: pick the taxonomy class using
   `references/taxonomy.md`. If two classes argue, the more specific wins
   (admin-console beats web-app).
6. **Score.** Compute priority 0–100 with the formula in
   `references/scoring.md`. The formula rewards: authentication boundaries,
   business-logic surfaces, deprecated/debug remnants, and *unloved assets* —
   surfaces with no recent change signal, where hygiene decays first.
7. **Register with evidence.** One `dossier_add` per surface. The `evidence`
   argument must cite the R-NNN records that observed it — the tool refuses
   citations that are not in the ledger, which is the no-slop law applied to
   cartography: a surface without records does not exist.
8. **Park, don't drop.** Interesting-but-unripe discoveries get
   `backlog=True` with a resume note. The backlog is a first-class citizen.
9. **Render.** Call `dossier_render(program)`. The dossier is written from
   state that was built from records — never from memory.

Exit gate (all must hold, numbers required in the phase summary):

* Every discovered surface is classified and evidence-cited, or parked with
  a reason.
* `dossier.md` renders and the asset graph groups every surface under a host.
* The summary states counts: surfaces registered, active, backlog, hosts.
  "Recon complete" without numbers is the forbidden state (spine §4).

Failure modes: wildcard DNS inflating host counts (mitigated in step 2);
soft-404 traps inflating surface counts (content-discovery calibrates);
scope drift (every tool call re-checks the gate — refusals land in the
ledger as REFUSED records, which is the audit trail that the gate held).

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Posture / authorization summary | `auth_status` |
| Host liveness, wildcard check | `dns_resolve` |
| Front-door, robots, sitemap probing | `http_probe` |
| Registering a classified surface | `dossier_add` |
| Rendering the organized map | `dossier_render` |
| Compact context view between steps | `dossier_summary`, `ledger_summary` |

## 5. Hard Rules (mechanically enforced)

1. **No surface without evidence.** `dossier_add` rejects citations absent
   from the ledger. Enforcement lives in code, not in discipline.
2. **One class, from the taxonomy.** Unknown class strings are rejected.
3. **No duplicate surfaces.** Re-registering a URL is refused; add evidence
   or park instead.
4. **Numbers at the exit gate.** The phase summary without counts does not
   pass review — the auditor checks for it.

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Before the first classification decision | `references/taxonomy.md` |
| Before the first priority score | `references/scoring.md` |
