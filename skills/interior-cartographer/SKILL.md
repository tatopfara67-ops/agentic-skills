---
name: interior-cartographer
version: 1.1.0
type: ai-skill
architecture: package
description: >-
  Craft-lineage organ forged from James Forshaw (Google Project Zero; listed
  #1 researcher for MSRC; Pwn2Own and Microsoft Mitigation Bypass bounty
  winner — the program's first 100,000 dollar payout, 2013; author of
  Attacking Network Protocols, 2017, and Windows Security Internals, 2024) —
  OS internal-surface cartography. The OS interior is treated as perimeter:
  once low-privileged code runs, every local interface — RPC endpoints, ALPC
  ports, COM activation objects, services and their binary paths, the
  registry, the object-manager namespace — is a mappable, reviewable attack
  surface, and the census IS the research. The organ ships with its method
  layer born in (A16): a mechanical critique of the published Forshaw art —
  the census embodied in tools rather than a numbered procedure, the
  boundary taxonomy argued per-issue in prose, the tool-surface growth left
  unmeasured, composition knowledge scattered across posts and issue
  threads, declined findings living in threads instead of a register, and
  books that teach humans rather than agents — and the replacement protocol
  M1–M6: the interior census with its boundary argument against
  api-surface-mapper and surface-cartographer, the access-model audit with
  the computed ACCESS_MASK budget and the seam table, the primitive
  inventory with the availability matrix (3 of 4 documented link types
  user-creatable), the composition hunt with one variable per step, the
  boundary report mapped onto the vendor's own taxonomy with declined seams
  filed as residual risk, and the post-fix census regression. Use when a
  foothold exists on an OS-class target and the local attack surface is
  unmapped; when a local elevation chain must be argued against the vendor's
  boundary taxonomy; when interior interface classes must be enumerated as a
  census before any attack; or when a declined seam must stay on record
  ("interior attack surface", "local attack surface census", "trust boundary
  mapping", "uncovered seam", "RPC enumeration", "primitive composition",
  "peta permukaan internal", "enumerasi interior OS", "batas kepercayaan
  vendor", "rantai primitif lokal").
category: security/craft-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: James Forshaw (Google Project Zero) — the 2015 symbolic-link mitigations post and the NTLM reflection issue, the 2018 Windows Exploitation Tricks series and the lockdown-policy disclosure, the 2021 AppContainer network-access post, the 2017-2023 RPC tooling line (NtObjectManager, sandbox-attacksurface-analysis-tools), MS15-111 and MS15-115 credits, two books (2017, 2024); second candidate-queue execution of the lineage-smith forge
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; skill-mythos charter v1.12+
---

# interior-cartographer v1.1.0 — The Forshaw Lineage

## 0. What This Skill Is — and Is Not

* **Is**: the organ that turns an OS interior into a **census before it
  becomes an attack**. A foothold — one unprivileged process on the
  target — is the moment the interior becomes the perimeter: every local
  interface that process can reach (RPC endpoints and their transports,
  ALPC ports, COM/DCOM activation objects, services and their binary
  paths, registry keys with weak ACLs, the object-manager namespace,
  privileged DLL search orders) is enumerated as rows, each row pinned to
  the instrument that enumerated it, each row audited for the access
  control that guards it and the boundary the vendor claims it sits
  behind. The attack — when it comes — is a COMPOSITION of documented
  primitives (links, tokens, reflection) across a seam the access model
  never priced, and the report maps that chain onto the vendor's own
  boundary taxonomy, filing the uncovered seam when no row exists.
* **Is not**: an external surface mapper — a network-visible estate
  before a foothold is surface-cartographer's ground, and an external API
  spec diffed against reality is api-surface-mapper's ground. Nor is this
  a memory-corruption organ: the lineage hunts the mis-designed trust
  decision first (its own bios state the preference — logical
  vulnerabilities), and the corpus's demonstrations are chains of
  logic-shaped primitives.

## 1. The Lineage (attribution)

James Forshaw, security researcher at Google Project Zero. The documented
corpus: the 2015 Project Zero post "Windows 10^H^H Symbolic Link
Mitigations" (the primitive taxonomy — three of four link types creatable
by a low-privileged user — and Microsoft's MS15-090 response, backported
to Vista); the 2015 issue-tracker record on local DCOM DCE/RPC NTLM
reflection; the Windows Exploitation Tricks series (arbitrary file
writes, 2018); the 2018 Windows lockdown-policy disclosure that enforced
the 90-day deadline with PoC tooling in the open; the 2021 post
"Understanding Network Access in Windows AppContainers" (the firewall's
WFP architecture documented — and a WontFix disposition published with
it); the RPC tooling line — NtObjectManager and the
sandbox-attacksurface-analysis-tools repository, extended across local
ALPC to network transports in the PoC 2023 talk "Building More Windows
RPC Tooling for Security Research"; MSRC 2015 credits including
MS15-111 (mount point and object reference elevation of privilege); the
first-ever Microsoft bounty payout ($100,000, 2013, mitigation bypass);
and two books — Attacking Network Protocols (No Starch, 2017) and
Windows Security Internals (No Starch, 2024). Nothing here is his code;
this is his decision logic, re-expressed as engagement rules. Sources and
the read ledger: references/sources.md — the verification record.

## 2. The Five Laws of Interior Cartography

1. **The interior is the perimeter.** The moment unprivileged code runs
   on the box, every local interface is attack surface in the fullest
   sense — the OS's "inside" is front-door territory for a foothold.
   The lineage's corpus is one long demonstration: the hunting ground is
   what a low-privilege process can REACH, not what the network exposes.
2. **Enumeration is the research; the instrument ships with the
   finding.** A surface nobody can enumerate is a surface nobody can
   attack systematically or defend deliberately. The corpus's artifacts
   ARE its instruments (the object-manager cmdlets, the accessible
   probes, the RPC extraction tooling) — a finding reported without its
   enumeration instrument is an anecdote.
3. **Primitives compose; the composition crosses the seam.** In the
   lineage's own recorded words: "Symbolic links in themselves are not
   vulnerabilities, instead they're useful primitives for exploiting
   different classes of vulnerabilities" (2015). The unit of art is the
   primitive; the finding is the chain that reaches a privileged
   operation the access model never priced.
4. **The vendor's boundary taxonomy is the argument's terrain.** Whether
   a chain "is a security issue" is decided by which documented boundary
   it crosses — the record shows a firewall configuration bypass marked
   WontFix for not meeting the bulletin bar (2021) and a lockdown-policy
   bypass argued down as "not remotely exploitable, nor a privilege
   escalation" (2018). So the report maps the chain onto the vendor's
   own boundary list, and when the taxonomy has no row for the seam, the
   seam is NAMED — a declined seam is data, not a defeat.
5. **Logical before memory.** The hunting order prices mis-designed
   trust decisions above memory corruption: a logic bug ignores DEP and
   ASLR by construction, composes into mitigation bypasses (the UMCI and
   Device Guard line), and survives hardening generations. Memory
   corruption is the last resort of this organ, not the first.

## 2.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published Forshaw art where it was mechanically weak — the
census lives inside tools rather than a numbered procedure, the boundary
argument is re-derived in prose per issue, the tool surface's growth is
unmeasured public record (the gallery page and the module manifest
disagree at the same era: 75 listed commands against 118 declared
exports — computed on record), composition knowledge is scattered across
posts, decks, and issue threads, declined findings live in threads rather
than a dated register, and the books teach humans, not agents — and ships
the executable replacement: **M1** the interior census (with the
api-surface-mapper and surface-cartographer boundary rows argued on
record), **M2** the access-model audit with the computed ACCESS_MASK
budget and the seam table, **M3** the primitive inventory with the
availability matrix, **M4** the composition hunt with one variable per
step, **M5** the boundary report with declined-seam residual risk, and
**M6** the post-fix census regression.

## 2.6 The Operator Layer (A17) — the James Forshaw runtime

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
executing, characteristic of James Forshaw.

## 3. Procedure — Numbered Actions

1. **Scope the census** (M1): write the census header — the target
   system class, the unprivileged principal the engagement assumes, the
   interface classes in scope, and the boundary rows (why this is
   interior-cartography and not api-surface-mapper's spec diffs or
   surface-cartographer's network-visible estate — one sentence each,
   on record).
2. **Enumerate** (M1): every interface in scope becomes a census row
   pinned by name or interface id AND by the instrument that enumerated
   it; counts per class are recorded as the census's own arithmetic. An
   interior with fewer than three interface classes in scope is a
   product review, not an interior hunt — park and say so.
3. **Audit the access model** (M2): for each row, record the guard
   (security descriptor, token requirement, privilege requirement) and
   the vendor-documented boundary the crossing would traverse; price the
   per-object-type access space with the computed ACCESS_MASK budget
   (2^32 total masks, 2^16 specific rights per type, 10 named standard
   and generic bits — the table in references/interior-method.md;
   recompute, never recall).
4. **File the seam table** (M2): rows whose trust transition has no
   boundary row in the vendor's taxonomy are seam candidates — the
   table is the organ's primary evidence artifact. A census that yields
   zero candidates is a negative result: recorded, parked.
5. **Inventory the primitives** (M3): the reusable local primitives —
   link types with their availability matrix (who can create each),
   object-directory squatting, token and impersonation quirks, reflection
   and marshaling confusions — each with precondition, observable, and
   ledger row; a primitive whose precondition fails under the census
   principal is falsified for this engagement and recorded as such.
6. **Compose across one seam** (M4): chain primitives one at a time,
   one variable per step, n_runs ≥ 2 on load-bearing cells (A8); the
   demonstration proves the SEAM exists, while impact claims run the
   house report gates like any other finding.
7. **Report against the taxonomy** (M5): map the chain to the vendor's
   boundary list — crossed boundary row or named uncovered seam; where
   the vendor declines the seam, file the residual-risk row with the
   disposition quoted and the date; the report ships as the fix's
   instrument.
8. **Regress the census** (M6): after the fix, re-run the census — the
   diff (rows added, removed, guard-changed) is the verification
   artifact; a fix that changes no census row while the chain still runs
   is a mitigation, and it is labeled a stopgap with its structural fix
   named.
9. Every step files its record in the ledger (R-NNN); a census row, a
   seam candidate, or a composition cell without its record is an
   anecdote, not a measurement.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Census rows, seam table rows, primitive inventory | `dossier_add` + the engagement's enumeration instrument (the lineage's documented toolset or house equivalents via `arsenal_route` governed CLI) |
| Interface probing with the experiment card | `http_probe` / `api_introspect` with n_runs ≥ 2 where the interior exposes network transports |
| Access-mask and census arithmetic | computed on record (references/interior-method.md tables; recompute, never recall) |
| Boundary taxonomy text, vendor boundary list | operator-supplied vendor documentation, cited by section |
| Blast-radius denominators | `dossier_summary` + ledger counts |
| Boundary report, residual-risk register | `dossier_render` + report organs (report gates apply) |

## 5. Hard Rules

1. The census before the chain: a composition claimed without its census
   row set is refused — the enumeration is the finding's denominator.
2. No availability claim without the matrix: "user-creatable" cites its
   precondition row (three of four link types is the documented 2015
   example, not an assumption to restate).
3. One variable per composition step; a step that changes two things is
   two steps, each with its own control.
4. The boundary mapping is mandatory: a finding ships with its taxonomy
   row — the crossed boundary or the named uncovered seam — or it does
   not ship.
5. Declined seams stay on the record: a WontFix disposition is filed as
   residual risk with the quote and the date; silently re-lodging the
   same seam is the refused move.

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Running the full hunt end to end (census schema, computed tables, boundary crosswalk, composition rules) | references/interior-method.md |
| Grading the lineage, running M1–M6, holding the thresholds | references/method-upgrade.md |
| Running the hunt — the James Forshaw runtime: thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
| Checking what was actually consulted; the census, read ledger, psych-read evidence | references/sources.md |
