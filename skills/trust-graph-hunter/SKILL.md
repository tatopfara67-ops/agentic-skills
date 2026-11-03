---
name: trust-graph-hunter
version: 1.2.0
type: ai-skill
architecture: package
description: >-
  Legend-tier organ (Tier B — The Human & Signal Manipulators) built from the
  Kevin Mitnick lineage, translated to systems — context deception and
  trust-graph auditing. Enumerates the trust edges between components (what
  each boundary trusts: IP allowlists, Referer/Origin checks, internal
  headers, webhook signatures, server-to-server tokens, shared secrets), draws
  the trust graph across the estate, then pre-registers deception hypotheses —
  can the context a system trusts be FORGED from outside it — and provesSince
  v1.1.0 the organ carries the executable method layer (A16) — a mechanical
  critique of the source material's floors as translated (trust edges narrated
  per-vignette and never assembled into a graph, forgery demonstrated without
  a differential against absent or legitimate context, no completeness
  accounting, third-party humans as instruments in the source practice, no
  falsifier anywhere) shipped as protocol M1–M5: the edge protocol with
  observed-behavior evidence, the three-condition context differential, the
  census gate that forbids claims on gapped boundaries, the operator-owned
  identity law, and the mechanical ethics gate. Use when auditing trust
  between a main server and third-party APIs, when hunting internal-header
  spoofing, webhook signature bypass, referer-based authorization,
  SSRF-as-trust-confusion, or server-to-server privilege escalation ("trust
  relationship", "context deception", "internal header spoof", "webhook
  signature bypass", "hubungan antar sistem", "privilege escalation via
  trust").
category: security/legend-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: >-
    Kevin Mitnick (1963-2023, author of The Art of Deception — trust
    exploitation, distilled here as a SYSTEMS discipline: forge the context a
    boundary trusts)
  tier: B — The Human & Signal Manipulators
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; both endpoints of every deception proof must be in scope and operator-owned
---

# trust-graph-hunter v1.2.0 — The System Trusts; Make It Trust You

## 0. What This Skill Is — and Is Not

* **Is**: the organ for INTER-SYSTEM trust. Its unit of work is the
  TRUST EDGE: the statement "component A grants capability C to any
  request presenting signal S" — enumerated across the estate into
  a trust graph, then audited with one question per edge: can S be
  forged from where the attacker actually stands?
* **Is not**: social engineering against humans. Mitnick's
  classic art targeted the human trust decision; this organ is the
  machine-to-machine translation — the human's "helpful voice on
  the phone" becomes the spoofable X-Internal header, the forged
  webhook signature, the referer the origin server believes. No
  human target is ever contacted.

## 1. Inherited Contracts

Plugs into **Phase 2** (trust graph as hypothesis source) and
**Phase 3** (deception differentials) of the mythos-bug-hunter
spine. Inherits the experiment contract (§6), the canary doctrine
(§8 — both ends of every deception proof are operator-owned
accounts/systems), and R0 scope (forging context at a THIRD-PARTY
system requires that system in program scope). Adjacent organs:
auth-boundary-mapper covers role×resource authorization INSIDE one
system — this organ covers the edges BETWEEN systems;
oauth-flow-auditor is the specialized protocol instance;
ssrf-playbook bridges when the edge is "the server trusts its own
outbound requests"; chain-architect composes forged-trust
primitives into escalation chains.

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

## 3.6 The Operator Layer (A17) — the Kevin Mitnick runtime

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
executing, characteristic of Kevin Mitnick.

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

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Edge enumeration from component map | `dossier_summary` + `ledger_append` (FACT) |
| Deception differentials (forged context) | `http_probe` (exact headers) |
| OAuth/OIDC identity-context edges | oauth-flow-auditor organ |
| Role×resource inside one system | auth-boundary-mapper organ |
| Outbound-request trust confusion | ssrf-playbook organ |
| Compoundable forged-trust primitives | chain-architect organ |
| Classification at report time | `cvss3_score` + `vrt_classify` |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Enumerating edges / signal classes / forgery matrix | `references/trust-context-catalog.md` |
| Verifying the Mitnick lineage and translation | `references/sources.md` |
| Grading the source translation, enumerating edges, running the context differential | `references/method-upgrade.md` |
| Running the hunt — the Kevin Mitnick runtime: thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
