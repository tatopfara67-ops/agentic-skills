---
name: chain-architect
version: 1.1.0
type: ai-skill
architecture: package
description: Legend-tier organ (Tier S — the Logic Architects) built from the Orange Tsai lineage — the compound kill-chain doctrine. Maps the target's component architecture from the dossier, inventories low/informational findings as chainable primitives, and designs pre-registered attack chains that compose 3-4 individually-harmless gaps into a critical whole (the ProxyLogon pattern). Severity floors stay honest per link while the chain carries the real impact. Since v1.1.0 the organ carries the executable method layer (A16) — a mechanical critique of the Tsai art's floors (chains told after the fact, per-link confidence never tracked, endpoint lineage narrated as insight, single-path demos, impact ceilings conflated) shipped as protocol M1–M5: the pre-hunt chain candidate schema, the surface-diff protocol, the chain tree with evidenced prunes, the weakest-link differential gate, and the proven/demonstrated/claimed ceiling statement. Use when hunting without a scanner, when low-severity findings pile up and the operator wants them weaponized legitimately, when composing SSRF + auth bypass + file write into escalation, or when the operator asks for chained bugs ("bug chaining", "rangkai celah kecil jadi kritis", "compose findings", "ProxyLogon style", "impact amplification", "chain low findings").
category: security/legend-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Orange Tsai (DEVCORE — ProxyLogon, "A New Era of SSRF", Confusion Attacks on Apache)
  tier: S — The Logic Architect & Reverse Engineers
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; an engagement with at least a Phase-1 dossier
---

# chain-architect v1.1.0 — The Compound Kill Chain

## 0. What This Skill Is — and Is Not

* **Is**: the organ that refuses the fantasy of "one giant bug that pops
  instantly". Its unit of work is the CHAIN: an explicit, pre-registered
  path through 3-4 individually low-severity gaps whose composition is
  critical. Each link is CONFIRMED by its own differential triad; the
  chain supplies the impact that no single link has.
* **Is not**: severity inflation. A link that is informational stays
  informational in the report; the chain line carries the combined
  severity, argued link by link. It is also not a scanner: chains are
  designed by reading architecture, not discovered by payload volume.

## 1. Inherited Contracts

Plugs into **Phase 2** (architecture maps and chain hypotheses) and
**Phase 4** (impact synthesis — the chain IS the impact proof) of the
mythos-bug-hunter spine. Inherits the experiment contract (§6), the
canary doctrine (§8: every link's proof runs on self-owned objects and
operator accounts), and the closure vocabulary (§7). Craft layer:
module-smith records each link as a reusable module; feedback-fuzzer
governs any search a link needs.

## 2. The Lineage (attribution)

**Orange Tsai** (DEVCORE, Taiwan) is the public archetype of this
doctrine. ProxyLogon (2021) is the canonical demonstration: an
authenticated SSRF plus a post-auth arbitrary-file-write — each a
bounded finding on its own — composed by reading Exchange's
architecture into an unauthenticated RCE chain that took the full
Pwn2Own award. The same shape recurs across his public work: URL
parser confusion ("A New Era of SSRF", DEF CON 28), hidden semantic
ambiguity in Apache ("Confusion Attacks"), and multi-year
single-target campaigns ("A 3-Year Tale of Hacking a Pwn2Own Target",
HEXACON 2023). What is distilled here is the METHOD — read the
architecture deeply, hunt the seams between components, treat low
findings as primitives, compose deliberately — not any of his
exploits. The verification record is `references/sources.md`.

## 3. Doctrine — How Tsai-Thinking Runs

1. **The architecture IS the attack surface.** The UI is not; the
   component graph is. Frontends, auth services, internal APIs,
   job workers, file stores, trust zones, and the data paths between
   them — mapped as a graph before any chain is designed.
2. **Low severity is raw material, not noise.** An informational
   disclosure, a post-auth SSRF, a verbose error, an open redirect:
   each is a PRIMITIVE whose value is decided by what it can be
   composed WITH, never by its standalone rating.
3. **Hunt the seams.** Bugs live where two components disagree about
   who validated what. Every boundary crossing (client→server,
   frontend→backend, service→service, parser→parser) is a seam where
   one component's assumption can be violated by another's behavior.
4. **Design the chain on paper first.** A chain is a hypothesis with
   an explicit path: primitive A grants position B, position B exposes
   primitive C, C gives write access D, D executes. Pre-registered
   before a single chained request is sent.
5. **Prove each link, then the joint.** Every link needs its own
   baseline/treatment/control; the chain proof then shows the joints
   — that link k's OUTPUT actually feeds link k+1's INPUT.

## 3.5 The Method Layer — Critique, Upgrade, M1–M5 (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published chain art where it was mechanically weak — the
winning path narrated as if architected, every hop reading equally
solid, endpoint lineages discovered by one analyst's noticing, one
chain shown while alternates stay invisible, proven/demonstrated/
claimed collapsed into one sentence — and ships the executable
replacement: **M1** the chain candidate schema (registered BEFORE the
hunt; a link with an empty precondition cell is daydreaming), **M2**
the surface-diff protocol (component inventory, version pinning,
cross-reference graph walks — the eureka, mechanized), **M3** the
chain tree with prunes (a branch pruned without evidence is
abandoned, not pruned), **M4** the weakest-link differential gate
(chain confidence = MIN over live links; the report names the floor
link), **M5** the ceiling statement (registered/pruned/live counts,
end-to-end n_runs distribution, org-wide claims ONLY with fleet
evidence).

## 4. Procedure — Numbered Actions

1. Rebuild the component graph from the Phase-1 dossier (asset graph,
   api-surface-mapper inventory, js-recon internal endpoints). One
   FACT record per edge: components, protocol, who authenticates whom.
2. Inventory primitives: every CONFIRMED or open finding so far,
   re-described as a capability — grants read of X, write to Y,
   reach of internal Z, confusion of parser P. The primitive
   vocabulary is in `references/chaining-catalog.md`.
3. For each primitive, ask the composition question: "what does this
   give me a position FOR?" — post-auth→pre-auth pivots,
   file-write→code-execution, SSRF→internal-service reach,
   parser-confusion→validation bypass.
4. Design candidate chains as pre-registered EXPERIMENT records:
   the full path, link by link, with the predicted joint behavior.
   Two chains maximum designed per session (effort discipline).
5. Verify links bottom-up: each link runs its own differential triad
   on self-owned objects/accounts; a link that fails its triad kills
   the chain honestly (closure: FALSIFIED link, not "assumed").
6. Run the joint proof ONCE, bounded: the end-to-end chain executed a
   single time, with a canary artifact as the final impact evidence
   (a self-owned file, a self-owned session, a marker value). Then
   stop — no re-runs "to be sure" (spine §8.2).
7. Classify the chain: `cvss3_score` on the vector of the OBSERVED
   combined path (privileges required by the FIRST link only; scope
   change when the chain crosses a trust zone boundary — S:C);
   `vrt_classify` on the final impact class. Per-link severities are
   stated separately and honestly in the same block.
8. Exit gate: component-graph edge count, primitives inventoried,
   chains designed, links confirmed per chain, joint proofs run,
   every link citing its triad records.

## 5. Hard Rules (mechanically enforced)

1. **No assumed links.** A chain line citing a link without that
   link's own differential records fails the audit.
2. **Per-link honesty.** The report states each link's standalone
   severity next to the chain severity; the chain line argues the
   composition, it never silently upgrades a link.
3. **One end-to-end proof.** The joint demonstration runs once;
   reproducibility is served by the per-link triads, not by re-runs.
4. **Self-owned at every link.** Objects, accounts, files, and
   sessions at each stage belong to the operator; real-user data
   never appears inside a chain proof.
5. **Two chains per session.** More is design sprawl; park the rest
   with a resume note (R1).

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Component graph, primitives, chain design | `dossier_summary` / `dossier_render` + `ledger_append` (EXPERIMENT) |
| Link differentials | `http_probe` (session headers per link's account) |
| Joint proof + canary | `http_probe` (CANARY tag) |
| Chain classification | `cvss3_score` (S:C when crossing trust zones) + `vrt_classify` |
| Link modules for reuse | module-smith cards (`ledger_append` EXPERIMENT) |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Choosing primitives / chain archetypes | `references/chaining-catalog.md` |
| Verifying the Orange Tsai lineage and sources | `references/sources.md` |
| Grading the published method, registering candidates, running link gates | `references/method-upgrade.md` |
