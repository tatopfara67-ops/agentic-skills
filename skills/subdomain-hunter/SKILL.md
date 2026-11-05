---
name: subdomain-hunter
version: 2.3.0
type: ai-skill
architecture: package
description: >-
  Phase-1 subdomain enumeration organ, upgraded (v2) with the EdOverflow
  lineage — passive-first ladder (certificate transparency, passive CLI
  routing), resolution and CDN/wildcard detection, permutation round, and
  CNAME-dangling takeover checks with a full dangling-class taxonomy
  (NXDOMAIN-CNAME, fingerprint-CNAME, dangling MX/NS, deep chains), TTL-aSince
  v2.1.0 the organ carries the executable method layer (A16) — a mechanical
  critique of the EdOverflow art's floors (a community wiki read by memory,
  dead/dangling/claim-able conflated in one-shot demos, single-read DNS state,
  deep chains narrated per-bug, disclosure as afterthought) shipped as
  protocol M1–M5: the fingerprint-registry freshness discipline, the dangling
  differential ladder, the TTL-aware verification rule with SOA stability, the
  chain walk, and the disclosure gate. Use when the operator asks to enumerate
  subdomains, expand a domain's asset inventory, check wildcard DNS, or
  investigate subdomain takeover ("cari subdomain", "enum subdomain",
  "subdomain takeover", "permutasi domain", "asset discovery", "dangling MX",
  "dangling NS", "takeover verification").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: v2 — EdOverflow (creator/maintainer of can-i-take-over-xyz; the dangling-record taxonomy and fingerprint-registry discipline)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# subdomain-hunter v2.2.0 — Passive First, Always

## 0. What This Skill Is — and Is Not

* **Is**: the Phase-1 organ that answers "what exists under this domain?"
  with a deduplicated, resolved, classified list — and then answers the
  follow-up nobody should skip: "is any of it dangling?"
* **Is not**: a brute-force firehose. Active enumeration is the LAST rung of
  the ladder, and it is rate-courteous when it runs. Since v2 it carries
  the **EdOverflow lineage** as its field-guide layer — the dangling-class
  taxonomy and fingerprint discipline that turn "CNAME looks weird" into
  a classed, dated, claim-path-tested verdict.

## 1. Inherited Contracts

Plugs into **Phase 1** of the mythos-bug-hunter spine. Inherits the Canon
(especially R0 scope gate, R1 plan-before-action, R5 tools-are-not-verdicts),
the ledger record format, and backlog mechanics. Does not restate them.

## 2. The Lineage Layer (v2 — the EdOverflow doctrine)

**EdOverflow** created and maintains the community takeover registry
(`can-i-take-over-xyz`: verdict table + machine-readable
`fingerprints.json`). v2 folds the lineage in as five field rules,
applied inside the takeover discipline (§4) and detailed in
`references/takeover-field-guide.md`:

1. **Class the dangling record, not just the CNAME.** NXDOMAIN-CNAME,
   fingerprint-CNAME, dangling MX, dangling NS, deep chains — the class
   IS the blast-radius argument (content control vs email reception vs
   subtree control).
2. **Three legs of verification:** DNS chain (every hop, terminal
   included), provider marker (quoted fingerprint, body not status
   alone), cache/TTL (negatives say their TTL; load-bearing verdicts
   re-read after expiry).
3. **Fingerprints are quoted, tables are dated.** The signature table is
   a sync of the upstream registry, date-pinned; upstream wins
   disagreements on load-bearing verdicts.
4. **Run the claim-path test before CONFIRMED.** Ownership-verification-
   gated claim paths make the record a hygiene finding, not a takeover.
5. **Retirements are records too.** Providers harden; entries retire;
   the correction tradition is doctrine, not noise.

## 3. The Ladder — Cheapest Signal First

1. **Certificate transparency** — `ct_subdomains(program, domain)`. Reads a
   public database; the target is never touched. Offline egress returns
   `ok=False` gracefully — record it and move down the ladder, never pretend.
2. **Passive CLI routing** — if the environment has `subfinder` or
   `amass -passive`, `arsenal_route(program, "subfinder", domain, "-silent")`
   harvests aggregated passive sources. Scanner output is a hypothesis about
   existence, not a finding (R5): each discovered name still needs resolution
   evidence before it becomes a SURFACE record.
3. **Resolution round** — `dns_resolve(program, name)` for every candidate.
   Only resolving names are surfaces. Record wildcard behavior FIRST:
   resolve two random non-existent names; if they resolve, every "live"
   claim downstream must say "live-or-wildcard" until proven otherwise.
4. **Permutation round** — only when the asset space is thin: generate
   permuted candidates (dev/staging/uat/internal prefixes, `-word` and
   `word2` joins — the generator table is in `references/sources.md`) and
   resolve them. This is DNS-side only, still not an HTTP flood.
5. **HTTP liveness** — `http_probe` each resolved name once. Status, server
   header, and redirect target become the reachability verdict for the
   dossier.

## 4. Takeover Discipline (the follow-up that matters)

A resolving name with a CNAME pointing at a deprovisioned third party is a
takeover candidate. The check sequence and the provider signature table
(Heroku/GitHub Pages/Shopify/Azure/CloudFront and friends) live in
`references/takeover-signatures.md`; the v2 dangling-class taxonomy,
TTL-aware verification protocol, fingerprint discipline, and claim-path
test live in `references/takeover-field-guide.md`. The discipline that
makes it evidence:

* The CNAME chain is a FACT record (from `dns_resolve`).
* The provider's "not found" marker on the dangling target is a second FACT
  record (from `http_probe` of the service host).
* Only the two records together justify a Phase-2 hypothesis; neither alone
  is a finding.

## 4.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published takeover art where it was mechanically weak — fingerprints
read from an unversioned wiki, dead/dangling/claim-able blurred in demo
stories, DNS read once without TTL or a second resolver, mid-chain dangle
points missed without a walk protocol, disclosure left to prose — and ships
the executable replacement: **M1** the fingerprint-registry discipline
(per-entry freshness stamp; > 180 days = STALE, cited as such), **M2** the
dangling differential (dead / dangling / claim-able decided by probe, never
prose), **M3** TTL-aware verification (≥ 2 resolvers, ≥ 5 of 6 stable
across the TTL window, SOA serial check), **M4** the chain walk (CNAME→CNAME
to terminal, MX/NS classes separately, no single-read hops), **M5** the
disclosure gate (wording capped at the demonstrated class).

## 4.6 The Operator Layer (A17) — the EdOverflow runtime

`references/operator-os.md` ships the figure's documented psychology
as the agent's RUNTIME, in four parts: the thinking framework (numbered
if-then decision rules, each citing the documented behavior it
distills), the behavioral protocol (situation → move → agent action →
refusal, with pacing and failure-reaction rules — how the agent acts
and behaves while hunting), the scripting arsenal (the organ's core
techniques as exact, tool-agnostic commands and micro-scripts, each
with its read-out and decision gate), and the rigid run-order binding
rules, behavior, and scripts onto the M-protocol above. Load it when
the hunt runs: the doctrine states the posture, the M-protocol states
the procedure — the operator OS is how the agent BEHAVES while
executing, characteristic of EdOverflow. Since v2.3.0 it also ships
**The opening ladder** (A18): where EdOverflow's candidates come
from — the perception layer that PRODUCES typed candidates before
any verification is due (rungs write census rows, never claims;
ranking rationale stated; generation falsifier on record; the
signature kit is the date-pinned registry sync).

## 5. Procedure — Numbered Actions

1. Entry: AUTH record present; domain is in scope (`scope_check`).
2. Run ladder rungs 1–2; merge candidate names; dedupe; count them.
3. Wildcard probe (two random names) — record the verdict.
4. Resolve all candidates; drop non-resolving ones with a FACT record each
   (a negative is still an observation).
5. `http_probe` the survivors; classify (surface-cartographer taxonomy) and
   `dossier_add` each with evidence citations.
6. For names whose CNAME leaves the parent domain: run the takeover
   sequence from `references/takeover-signatures.md`, classed and verified
   per `references/takeover-field-guide.md` (chain + marker + TTL +
   claim-path test).
7. Exit gate: numbers stated — candidates found, resolving, live, wildcard
   verdict, takeover candidates. Anything unresolved is parked with a
   reason, not dropped.

## 6. Hard Rules (mechanically enforced)

1. **Passive before active.** The permutation round and HTTP liveness run
   only after CT and passive routing produced their records — the ledger's
   record order proves it (auditor checks: first subdomain-related record
   is a passive-source one).
2. **Wildcard is a verdict, not a vibe.** Two random-name resolutions,
   recorded, before any "live host" claim.
3. **Takeover claims need both records** (CNAME chain + provider marker),
   the dangling class stated, and the claim-path verdict on record
   (v2).
4. **No invented names in the dossier.** Every name cites a discovery record
   (CT output, CLI output, or permutation record).

## 7. Tool Routing

| When | Tool |
| --- | --- |
| CT enumeration | `ct_subdomains` |
| Passive CLI harvest | `arsenal_route` (subfinder / amass -passive) |
| Resolution, CNAME chains, wildcard probe | `dns_resolve` |
| HTTP liveness + provider markers | `http_probe` |
| Registering surfaces | `dossier_add` (surface-cartographer) |

## 8. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Building the candidate ladder or permutation set | `references/sources.md` |
| Grading the published method, dating fingerprints, running the dangling differential | `references/method-upgrade.md` |
| Running the hunt — the EdOverflow runtime: the opening ladder (A18), thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
| Any CNAME leaves the parent domain | `references/takeover-signatures.md` |
| Verifying any takeover candidate (class, TTL, claim path) | `references/takeover-field-guide.md` |
