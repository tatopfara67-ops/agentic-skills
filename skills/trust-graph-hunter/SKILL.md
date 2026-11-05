---
name: trust-graph-hunter
version: 1.4.0
type: ai-skill
architecture: package
description: >-
  Legend-tier organ (Tier B — The Human & Signal Manipulators) built from the
  Kevin Mitnick lineage, translated to systems — context deception and
  trust-graph auditing — upgraded at v1.3.0 with the Sean Metcalf lineage
  layer: the DIRECTORY-INTERIOR trust edges (Active Directory and LDAP-analog
  estates). Enumerates the trust edges between components (what each boundary
  trusts: IP allowlists, Referer/Origin checks, internal headers, webhook
  signatures, server-to-server tokens, shared secrets) and inside the
  directory (membership nesting, ACL delegation, SIDHistory, GPO rights,
  credential-cache LSASS/ntds.dit edges, Kerberos protocol keys), draws the
  one trust graph across the estate, then pre-registers deception hypotheses
  — can the context a system trusts be FORGED from outside it — and prices
  every directory inheritance path (golden/silver ticket, DCSync, Kerberoast,
  the credential shuffle) by precondition, contact, and detection signal.
  Since v1.1.0 the organ carries the executable method layer (A16) — a
  mechanical critique of the source material's floors as translated (trust
  edges narrated per-vignette and never assembled into a graph, forgery
  demonstrated without a differential against absent or legitimate context,
  no completeness accounting, third-party humans as instruments in the source
  practice, no falsifier anywhere) shipped as protocol M1–M5: the edge
  protocol with observed-behavior evidence, the three-condition context
  differential, the census gate that forbids claims on gapped boundaries, the
  operator-owned identity law, and the mechanical ethics gate. Since v1.3.0
  the method layer extends with the Metcalf critique (techniques stated
  per-post but never assembled into one priced path graph; the attacker's
  starting position never a formal census step; mitigations as prose, never
  a mechanical checklist; detection shipped apart from the attack row) and
  protocol M6–M9: the eight-source directory-edge census, the priced
  inheritance-path matrix, the tier-boundary validation gate with the KRBTGT
  double-reset arithmetic, and the paired detection row with its rot caveat.
  Use when auditing trust between a main server and third-party APIs, when
  hunting internal-header spoofing, webhook signature bypass, referer-based
  authorization, SSRF-as-trust-confusion, server-to-server privilege
  escalation, or the directory interior — AD attack paths, privileged-group
  mapping, Kerberos ticket trust, DCSync rights, tiered-administration
  validation ("trust relationship", "context deception", "internal header
  spoof", "webhook signature bypass", "hubungan antar sistem", "privilege
  escalation via trust", "AD attack path", "who is really Domain Admin",
  "golden ticket", "kerberoast", "DCSync", "tier model", "admin SD holder").
category: security/legend-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: >-
    Kevin Mitnick (1963-2023, author of The Art of Deception — trust
    exploitation, distilled here as a SYSTEMS discipline: forge the context a
    boundary trusts) upgraded at v1.3.0 with the Sean Metcalf lineage layer
    (ADSecurity.org author, Trimarc founder/CTO, MCM Directory Services —
    the directory-interior trust edges: the eight-source combined-rights
    census, privilege inheritance priced as attack paths, defense stated as
    tier boundaries)
  tier: B — The Human & Signal Manipulators
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; both endpoints of every deception proof must be in scope and operator-owned
---

# trust-graph-hunter v1.4.0 — The System Trusts; Make It Trust You

## 0. What This Skill Is — and Is Not

* **Is**: the organ for INTER-SYSTEM trust. Its unit of work is the
  TRUST EDGE: the statement "component A grants capability C to any
  request presenting signal S" — enumerated across the estate into
  a trust graph, then audited with one question per edge: can S be
  forged from where the attacker actually stands? Since v1.3.0 the
  graph extends INTO the identity directory: the same edge protocol
  covers membership nesting, ACL delegation, SIDHistory, GPO
  rights, credential caches, and Kerberos protocol keys — the
  directory-interior edges where inherited privilege lives.
* **Is not**: social engineering against humans. Mitnick's
  classic art targeted the human trust decision; this organ is the
  machine-to-machine translation — the human's "helpful voice on
  the phone" becomes the spoofable X-Internal header, the forged
  webhook signature, the referer the origin server believes, the
  ticket a KDC never issued. No human target is ever contacted.

## 1. Inherited Contracts

Plugs into **Phase 2** (trust graph as hypothesis source) and
**Phase 3** (deception differentials) of the mythos-bug-hunter
spine. Inherits the experiment contract (§6), the canary doctrine
(§8 — both ends of every deception proof are operator-owned
accounts/systems), and R0 scope (forging context at a THIRD-PARTY
system requires that system in program scope). Adjacent organs:
auth-boundary-mapper covers role×resource authorization INSIDE one
system — this organ covers the edges BETWEEN systems and the
TRUST SUBSTRATE inside the identity directory that decides both;
oauth-flow-auditor is the specialized protocol instance;
ssrf-playbook bridges when the edge is "the server trusts its own
outbound requests"; chain-architect composes forged-trust
primitives into escalation chains; cloud-config-auditor takes the
cloud-identity tier (Entra ID Connect paths cross organ boundaries
as catalogued archetypes).

## 2. The Lineage (attribution — an honest translation)

**Kevin Mitnick (1963–2023)** was the century's best-publicized
demonstration that trust, not technology, is the softest layer:
The Art of Deception (2002) documents the pattern — reverse
social engineering, context fabrication, authority borrowing,
the exploit of an organization's internal trust assumptions.
This organ makes the translation the operator's brief requested:
the ANALYSIS OF CONTEXT AND TRUST RELATIONSHIPS between systems,
exploited to obtain elevated access — third-party API to main
server trust, service-to-service assumptions, the belief that a
request bearing the right context signal could only have come
from a trusted peer. The human-layer techniques themselves are
out of scope and unused; what is distilled is the trust-model
analysis behind them. The verification record is
`references/sources.md`.

### 2.5 The Metcalf layer (v1.3.0 — the directory-interior extension)

**Sean Metcalf** (ADSecurity.org author; Trimarc founder/CTO;
Microsoft Certified Master in Directory Services) spent a decade
mapping where privilege ACTUALLY lives in the Microsoft identity
stack: rights are the UNION of eight sources, not group
membership; the domain is not the security boundary — the forest
is; techniques (golden tickets with SIDHistory, silver tickets,
DCSync, Kerberoast) are priced doors between attacker positions;
and defense is stated as tier boundaries with mechanical
validation. The upgrade carries his documented craft as the
directory extension of the organ's graph model — the
attack-detection-mitigation record as ONE artifact, attribution
of every technique to its discoverer on record (Delpy, Le Toux,
Duckwall, Medin, Monné, harmj0y, Wald0 — see sources.md), and his
own research firsts (SIDHistory golden tickets with Delpy, 2015;
the original golden-ticket detection method; DCSync rights
documentation; SPN scanning). Folded per the queue's standing
rule: a documented upgrade of an existing organ counts as an
assimilation too.

## 3. Doctrine — How Mitnick-Thinking Runs (systems edition)

1. **Every capability grant rides a context signal.** No system
   grants capability to "a request" — it grants it to a signal:
   source IP, Referer, a header, a signature, a token's issuer, a
   network position. Name the signal, and the trust edge is
   auditable.
2. **Trust is transitive and therefore compoundable.** A trusts B,
   B trusts C ⇒ attacks that borrow A's context through B are
   escalation CHAINS, not single bugs — the graph is drawn before
   any single edge is attacked.
3. **The question is always provenance.** For every trusted signal
   S: who can legitimately produce S, and can anyone else make
   something indistinguishable? The attack is "authority
   borrowing" when the answer is yes.
4. **Deception is proven with self-owned ends.** The demonstration
   forges context at one operator-owned component toward another
   operator-owned endpoint — inherited trust shown, real users'
   and third parties' systems never touched.
5. **The trust graph is a report artifact.** The finding block
   ships the edge, the forged signal, the differential, and the
   access inherited — drawn as a graph, so the triage desk sees
   the systemic issue, not one odd header.

### 3.4 The Metcalf doctrine (directory edition — v1.3.0)

1. **Rights are the union of eight sources.** Group membership is
   one source of eight (membership, computer-rights, ACL
   delegation, SIDHistory, GPO rights, user-rights assignments,
   local groups, share delegation); a principal's real power is
   the census of all eight, and the escalation paths live in the
   seven that everyone skips.
2. **The boundary is the forest, not the domain.** SIDHistory
   carries reach-back across trusts — a compromised child domain
   prices a forest-wide path through the Enterprise Admins RID.
3. **Mechanism before technique.** Every directory attack is
   stated as its protocol mechanics first (who signs what, which
   service validates it, what contact is required) — then priced:
   position → technique → cost → signal.
4. **Attack, detection, mitigation ship as one record.** A
   technique documented without its detection signal and its
   mechanical mitigation is half a finding; and indicators rot
   (the mimikatz domain-field fix of 2016 is the on-record
   example) while the method class persists — version the
   indicator, price the method.
5. **Assume breach, then validate the tiers.** The audit starts
   from the attacker's documented positions (any authenticated
   user; local admin on any host; replication rights) and defense
   is graded as tier-boundary pass/fail rows — the KRBTGT
   double-reset arithmetic included — not as hardening prose.

## 3.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered — and the translation itself
is graded, not inherited. `references/method-upgrade.md` grades the source
form where it was mechanically weak — one exploited edge per story with
the graph never assembled, "they believed me" conflating beats-absent with
matches-legitimate, survivorship bias as a genre, real employees as demo
instruments, a form in which nothing can be wrong — and ships the
executable replacement: **M1** the edge protocol (per boundary: trusts=
cited to OBSERVED behavior on operator-owned calls, classed
contextual/cryptographic/ambient, graded verification-strength), **M2**
the context differential (absent vs forged vs legitimate, n ≥ 5
interleaved; forged-beats-absent is weak evidence, forged-matches-legit
is the strong finding; challenged-and-held is defense data), **M3** the
census gate (every boundary EDGE-recorded or explicitly gapped; gapped
boundaries carry no claims), **M4** the identity law (operator-owned
identities only, each an ASSET with ownership basis; real-person
identities forbidden as a hard rule), **M5** the ethics gate (fields
filled BEFORE the run; any failing field = the run does not start).
Since v1.3.0 the layer extends with the Metcalf critique (techniques
stated per-post but never assembled into one priced path graph; the
attacker's starting position never a formal census step; mitigations
as prose best-practice, never a mechanical pass/fail checklist;
detection shipped in separate posts from the attack it answers) and
protocol **M6–M9**: **M6** the eight-source directory-edge census (every
DIR-EDGE row citing its LDAP read; the AdminCount seed; the census
gate extended to all eight sources), **M7** the inheritance-path pricing
matrix (every technique row priced by precondition position, required
contact, and emitted signal — priced as valuation data, never executed
on live estate), **M8** the tier-boundary validation gate (mechanical
pass/fail rows: admin-logon restrictions, service-account password
length, KRBTGT rotation state and the double-reset law, replication
rights, DC-logon groups, cloud/virtualization equivalence), **M9** the
paired detection row with its rot caveat (every priced path ships its
detection signal and the honest half-life statement).

## 3.6 The Operator Layer (A17) — the Mitnick + Metcalf runtime

`references/operator-os.md` ships both figures' documented psychology
as the agent's RUNTIME, in four parts: the thinking framework (numbered
if-then decision rules, each citing the documented behavior it
distills — R1–R6 the Mitnick rules, R7–R12 the Metcalf rules), the
behavioral protocol (situation → move → agent action → refusal, with
pacing and failure-reaction rules — how the agent acts and behaves
while hunting), the scripting arsenal (the organ's core techniques as
exact, tool-agnostic commands and micro-scripts, each with its read-out
and decision gate — T1–T4 the context-deception set, T5–T8 the
directory-census set), and the rigid run-order binding rules, behavior,
and scripts onto the M-protocol above (S1–S7 the web-edge hunt, S8–S12
the directory tier). Load it when the hunt runs: the doctrine states
the posture, the M-protocol states the procedure — the operator OS is
how the agent BEHAVES while executing, characteristic of Kevin
Mitnick's context-craft and Sean Metcalf's census-and-price discipline.
Since v1.4.0 it also ships **The opening ladder** (A18): where
Mitnick's and Metcalf's candidates come from — the perception layer
that PRODUCES ranked trust-edge, public-fact, and directory-rights
candidates from the estate's own published surface before any approach
is due (rungs write census rows, never pretexts; ranking rationale
stated; generation falsifier on record; the trust-edge census kit is
the pinned desk row set).

## 4. Procedure — Numbered Actions

1. Enumerate trust edges from the Phase-1 dossier and the
   component graph (chain-architect's map): for every pair of
   components, what does each side accept as proof of the other?
   Edge inventory template in
   `references/trust-context-catalog.md`.
2. Classify each edge's signal: network-position (IP allowlist,
   mTLS, VPC assumption), request-context (Referer/Origin, Host,
   X-Forwarded-For), application-context (internal headers,
   webhook signatures, shared secrets, HMAC schemes),
   identity-context (issuer/audience assumptions, server-to-server
   tokens, API keys with implicit role).
3. Score edges by forgeability priors: signals producible from
   OUTSIDE the trust zone (public Referer, client-supplied
   headers that survive the proxy, unsigned callbacks) rank
   first — the priority queue is the hunting order.
4. Pre-register the deception hypothesis per edge: "signal S,
   forgeable by party P, grants capability C" — one EXPERIMENT
   record per edge, prediction and falsifier stated.
5. Run the deception differential: baseline (legitimate context
   via the operator's own trusted component), treatment (the
   same capability request with forged context, sent from OUTSIDE
   the trust zone), control (capability request with unrelated
   wrong context). The triad separates "context is checked" from
   "context is decoration".
6. Access proof, bounded: inherited trust demonstrated on
   operator-owned objects/accounts at both ends — ONE privileged
   action, canary-tagged, then stop (spine §8.2).
7. Chain hand-off where the edge is compoundable: a forged trust
   edge that yields a position (internal reach, service identity)
   is a primitive for chain-architect; an outbound-request trust
   confusion routes to ssrf-playbook.
8. Exit gate: edges enumerated (by signal class), hypotheses
   pre-registered, differentials run with triads, access proofs
   bounded and canary-tagged, graph rendered into the report,
   every claim citing records.
9. Directory tier (v1.3.0): when the estate includes an identity
   directory, run the eight-source census — every DIR-EDGE row with
   its LDAP read cited (`references/directory-trust-catalog.md`,
   T5/T6) — and seed it with the interesting-principals table plus
   the AdminCount filter.
10. Price the inheritance paths from the operator's CURRENT
   authorized position: fill the pricing matrix rows whose
   preconditions the census shows are already met; each row names
   contact required and the detection signal emitted (M7).
11. Validate the tier boundaries mechanically (M8): admin-logon
   restrictions, service-account password lengths, KRBTGT rotation
   state with the double-reset law, replication-rights holders,
   DC-logon group membership, virtualization/cloud equivalence —
   every row pass/fail with its evidence read.
12. Pair every priced path with its detection row and the rot
   caveat (M9); directory exit gate: census closed or honestly
   gapped, price table filled, tier rows all pass/fail with
   evidence, and every recommendation mechanical (no prose-only
   hardening advice).

## 5. Hard Rules (mechanically enforced)

1. **Both ends owned.** Every deception proof runs operator-owned
   component → operator-owned endpoint; forging context toward
   third-party systems requires them in program scope, else it is
   reported as an identified edge, never executed.
2. **No human-target deception.** The organ never contacts,
   phishes, or manipulates people; machine-context signals only
   (this rule is the lineage's honest boundary).
3. **The differential triad is mandatory.** "It accepted my
   X-Internal header" without baseline/control is a LEAD.
4. **One inherited-privilege action per proof.** Then stop;
   reproducibility is the triad's job, not repetition's.
5. **The graph ships.** Trust findings are reported as edges on
   the graph, with the forged signal and inherited access —
   single-header anecdotes without the graph fail the audit.
6. **The directory census is read-only.** Every directory query the
   agent issues is a standard authenticated LDAP read within the
   authorized scope; no credential dumping, no ticket requests,
   no replication calls on live estate — the attack techniques are
   PRICED as data for the report, never executed.
7. **Priced paths prove nothing by execution.** Where a path must
   be demonstrated, the demonstration runs in an operator-owned
   lab replica with operator-owned accounts, one action,
   canary-tagged — the live estate sees only census rows and
   pass/fail validation rows.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Edge enumeration from component map | `dossier_summary` + `ledger_append` (FACT) |
| Deception differentials (forged context) | `http_probe` (exact headers) |
| Directory census (read-only LDAP reads) | T5/T6 in `references/operator-os.md` + `ledger_append` (FACT) |
| Path pricing + tier validation rows | T7/T8 in `references/operator-os.md` + `ledger_append` (REPORT) |
| OAuth/OIDC identity-context edges | oauth-flow-auditor organ |
| Role×resource inside one system | auth-boundary-mapper organ |
| Outbound-request trust confusion | ssrf-playbook organ |
| Compoundable forged-trust primitives | chain-architect organ |
| Cloud-identity tier (Entra ID Connect paths) | cloud-config-auditor organ |
| Classification at report time | `cvss3_score` + `vrt_classify` |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Enumerating edges / signal classes / forgery matrix | `references/trust-context-catalog.md` |
| Enumerating directory edges / inheritance-path pricing / tier validation / detection signals | `references/directory-trust-catalog.md` |
| Verifying the Mitnick lineage and translation | `references/sources.md` |
| Verifying the Metcalf census and the attribution ledger | `references/sources.md` (the Metcalf layer section) |
| Grading the source translation, enumerating edges, running the context differential | `references/method-upgrade.md` |
| Running the hunt — the Mitnick + Metcalf runtime: the opening ladder (A18), thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
