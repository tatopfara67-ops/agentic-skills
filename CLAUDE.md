# CLAUDE.md — mythos-arsenal agent contract

Place this file at the root of any workspace where the mythos-arsenal MCP
server is wired in. The protocol serves tools; THIS file makes the agent
use them in discipline. MCP cannot force an agent to behave — a contract
can.

## Prompt escalation (A13 — the rule that runs before everything)

ANY operator instruction, however terse or informal — "tolong lanjutkan
pekerjaan bug bounty yang tertunda", "get me at least 3 high-medium
bugs", one sleepy line in any language — is FIRST passed through
`doctrine_forge(request)`. The tool returns the detected intent, the
severity/quota goals, the persona mix (which legend lineages apply), the
phase plan, the tools, and the full professional doctrine order. You
execute the EXPANDED order, never the bare words; the original request
rides along verbatim into the plan note. Never treat a quota as a
severity mandate — it is an effort budget, and the gates never bend.

## Session startup (any session that touches security work)

1. Call `mythos_charter()` — the skill-mythos activation payload:
   thirteen charter articles, the bundle map with install status, the
   quality gates. The charter loads BEFORE the skill list; it is the
   routing contract the rest of this file details.
2. Call `mythos_lineages()` — the assimilated-lineage registry
   (figures, distillations, sources, corrections on record) when the
   work will lean on a craft/legend organ or the operator asks who a
   distill came from.
3. Call `list_skills()` — metadata only. Do not `get_skill` everything;
   progressive disclosure is the cost model (name+description first,
   bodies on demand, references when the phase needs them).
4. At engagement start, load the spine (mythos-bug-hunter) and its conduct
   module. The organs below plug into its phases; they do not replace it.
5. `doctrine_forge` every operator instruction before acting on it (A13).
6. Pick organs by phase, never by curiosity.

## Phase routing

| Phase | Organ(s) | Key tools |
| --- | --- | --- |
| 0 Scoping | — | `auth_status`, `scope_check`, `ledger_append` (AUTH record) |
| 1 Recon | surface-cartographer (drives), subdomain-hunter, content-discovery, js-recon, api-surface-mapper; craft layer: scan-economist prices every sweep, pipeline-smith shapes the stages; legend overlay: ghost-crawler (Lamo) drives when scope is tight or the WAF is scanner-hostile — passive indexes first, one probe per candidate, main app untouched | `dns_resolve`, `http_probe`, `content_discover`, `js_analyze`, `api_introspect`, `ct_subdomains` |
| 1 Cartography | surface-cartographer | `dossier_add`, `dossier_render` |
| 2 Hypotheses | spine grammar; auth-boundary-mapper v2 builds the matrix (Rosen: identifier construction → every position → 2nd-order → tenant slices); business-logic-hunter maps workflows; legend overlays: chain-architect (Tsai) designs compound kill chains from accumulated low findings, trust-graph-hunter (Mitnick) enumerates trust edges, deep-teardown (Hotz) dissects in-scope client artifacts; craft layer: module-smith writes the cards, packet-orchestrator translates manual traces | `ledger_append` (EXPERIMENT pre-registrations) |
| 3 Testing | injection-lab, ssrf-playbook, xss-playbook, oauth-flow-auditor, cloud-config-auditor; legend overlays: desync-hunter (Kettle) at parser seams in scope, signal-smith (Draper) when validators block honest payloads (two variations max per seam); craft layer: feedback-fuzzer governs search loops, template-scanner the reusable checks | `http_probe`, `arsenal_route` |
| 4 Impact | spine canary ladder; chain-architect runs the bounded joint proof when a chain was designed (module-smith: access and impact proofs separate) | `ledger_append` (CANARY) |
| 5 Audit | — | `ledger_merge`, write report from records, `cvss3_score` + `vrt_classify` for every CONFIRMED finding, run `auditor/audit_report.py` until exit 0 |
| Incident (any phase) | adversary-tracker — the Binary Brain | `sbb_declare`, `sbb_decide`, `sbb_apply` |
| Any instruction | doctrine_forge FIRST (A13) | `doctrine_forge` |

## Incident branch (event-triggered, any phase)

When a sensor or the operator reports adversary activity on assets this
engagement is authorized to defend, the phase loop pauses and
adversary-tracker takes over: freeze before change, baseline, then the
`sbb_*` loop — declare (the null hypothesis is auto-inserted), decide
(pre-registered halving), apply (one bit, one record). The engine
refuses tip-off actions while passive eliminators remain, refuses
tests that cannot eliminate, and refuses to CONFIRM on a single
channel; the hunt ends in an audited handoff pack. Identity and the
last mile belong to the client's IR or law enforcement — never to the
agent. Then the phase loop resumes where it paused.

## Non-negotiables (enforced in tools, restated here so you never fight them)

1. **R0 gate first, always.** Every network tool checks `scope.csv` before
   a byte leaves the machine. A refusal is a REFUSED ledger record — an
   audit fact, not an obstacle. Never route around the gate, never
   re-implement a refused request with curl outside the ledger.
2. **No claim without a record.** Anything you write in a report, dossier
   note, or summary cites `R-NNN`. If it is not in the ledger, it did not
   happen.
3. **Scanner and CLI output are hypotheses** (R5), including `arsenal_route`
   output and `api_introspect` spec bodies. Probe records turn hypotheses
   into surfaces.
4. **Bodies stay out of context.** Tools return compact views + artifact
   paths; re-read from disk only when needed.
5. **Numbers at exit gates.** Phase summaries state counts; "recon done"
   without numbers is a forbidden state.
6. **Refusals are final inside the loop.** "not on the allowlist", "blocked
   flag tokens", "recon_only", "deny-by-default" — report these to the
   operator as engagement facts; do not retry, do not work around.

## Secrets policy (absolute)

Secret-shaped strings found by `js_analyze` or in artifacts are masked,
report-only, never used, never echoed. Full values stay in on-disk
artifacts for the operator. There is no circumstance in this pipeline
where using a discovered secret is correct.

## Effort discipline

Default budgets from the spine apply (R7). When a tool reports its cap bit
into the plan (content discovery truncation, doc-endpoint sweep), park the
remainder with a resume note — do not silently re-run with a raised cap.

## Before shipping any report

1. `ledger_merge(program)` — fold the append log.
2. Write the report ONLY from `ledger_read` outputs.
3. Classify every CONFIRMED finding: `cvss3_score` on the vector you
   will write (write exactly what it returns — the auditor recomputes
   it), `vrt_classify` for the Bugcrowd VRT dotted id + P-rating and
   the HackerOne crosswalk. Both lines cite the same records as the
   finding. Incident handoffs (`Risk:` ratings) are exempt. Chain
   findings (chain-architect) state per-link severities next to the
   chain severity, both classified.
4. `python3 auditor/audit_report.py <report.md>` — exit 0 or it does not
   ship. Fix the work behind the report, not the auditor.
