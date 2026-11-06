---
name: prototype-playbook
version: 1.6.0
type: ai-skill
architecture: package
description: >-
  Deep-technical organ (tier 3) built from the Gareth Heyes lineage
  (PortSwigger Research) — hunting the JavaScript object world as
  trust-bearing state. Three attack families live here because they share one
  root cause (code trusts inherited or ambient object properties it never
  validated): prototype pollution (a recursive merge writes attacker keys into
  Object.prototype and every object downstream inherits them — client-side via
  URL/hash/JSON sources, server-side via JSON bodies in Node), DOM clobbering
  (HTML named elements become window globals and shadow the references scripts
  trust), and postMessage origin confusion (message listeners trusting sender
  origins loosely). Carries the WWH registers, the source→gadget→sink hunting
  order, and the no-DoS law for server-side pollution detection (Heyes' safe
  black-box techniques: harmless canary properties whose only footprint is an
  observable response difference). Since v1.2.0 the organ carries the
  executable method layer (A16) — a mechanical critique of the Heyes art's
  floors (DOM-Invader delivery, error side effects as the only oracle, gadget
  hunting before merge-surface mapping, library versions unpinned, single-shot
  pollution claims) shipped as protocol M1–M4: the merge-surface inventory,
  the calibrated oracle ladder (read-back → signature → refused crash), the
  __proto__ differential with same-shape controls, and the version-pinned
  gadget matrix. Since v1.5.0 the payload corpus deepens (A19): the
  DOM-clobbering probe families and the self-owned-both-ends postMessage
  probe enter the versioned corpus (corpus.json 1.1.0) — the
  object-model catalog's probe tables now resolve to byte-exact
  entries instead of prose shapes. Since v1.6.0 the extreme tier
  rides the weapons vault (A19e): the browser gadget seams from the
  Widespread prototype pollution gadgets research — the fetch-API
  Object.prototype.body default (PP-013) and the GTM sequence gadget
  reaching an eval-family sink (PP-014, the published
  es.wordpress.org vector) — join corpus 1.2.0, and extreme-tier
  bytes release only through the arsenal's `payload_release` gate:
  instruction-override attempts refused and ledgered, weaponized
  classes banned outright, one scope-authorized target per call, the
  gate's decision accuracy itself measured by the labeled bench
  (`payload_bench`). Use when the target is a JavaScript-heavy SPA, when
  third-party JS libraries load, when JSON merges user input server-side, when
  postMessage listeners or DOM clobbering sinks are suspected ("cari prototype
  pollution", "audit JS libraries-nya", "apakah node app-nya merge JSON user",
  "test window.postMessage listener", "kamu tau gadget chain?").
category: security/deep-technical
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: >-
    Gareth Heyes (PortSwigger Research — "Server-side prototype pollution:
    Black-box detection without the DoS", 2023; "Widespread prototype pollution
    gadgets"; DOM Invader, the Burp browser extension that finds XSS, prototype
    pollution, and postMessage issues)
  tier: 3 — deep technical (the object-world doctrine)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.5+ (R0, ledger, differential triad); xss-playbook (the sink grammar once a gadget feeds a DOM sink); js-recon (the bundle-reading discipline that locates merge code and listeners)
---

# prototype-playbook v1.6.0 — The Object World Is Trust-Bearing State

## 0. What This Skill Is — and Is Not

* **Is**: the organ for authorized hunting of object-model attack
  classes — **prototype pollution** (client-side and server-side),
  **DOM clobbering**, and **postMessage origin confusion** — united
  by one doctrine: JavaScript code constantly reads properties that
  resolve through inheritance, ambient global bindings, or message
  events, and none of those resolutions was ever authenticated. Its
  unit of work is the **gadget chain**: a source that writes (or
  clobbers, or sends), a gadget that reads, a sink that acts — each
  link proven by its own differential before the chain runs.
* **Is not**: a JavaScript bug sweeper or a dependency-vuln scanner
  (mythos-code-audit and template-scanner own those territories), and
  not a DOM XSS payload library (xss-playbook owns the sink grammar;
  this organ delivers the *path* to the sink that the sink grammar
  assumes).

## 1. Inherited Contracts

Plugs into **Phase 1** (js-recon's bundle inventory supplies the
library/version list; the object-model surface is an inventory
column), **Phase 3** (the differentials), and **Phase 4** (bounded
impact proofs — gadget chains compose under chain-architect's
per-link law). Inherits the experiment contract (§6), the canary
doctrine (§8), the closure vocabulary (§7). The secrets policy
absolute applies to anything the bundles reveal. js-recon locates the
merge code and listeners; xss-playbook takes over at the sink.

## 2. The Lineage (attribution)

**Gareth Heyes** is the public researcher this organ's discipline is
distilled from: PortSwigger Research; author of *Server-side
prototype pollution: Black-box detection without the DoS* (Feb 2023;
presented at NullCon Berlin 2023 and OWASP Global AppSec Dublin 2023)
— the safe-detection corpus this organ's no-DoS law is built on; the
*Widespread prototype pollution gadgets* research that made
"gadget hunting" a discipline rather than an accident; and creator of
**DOM Invader**, the Burp browser extension that finds XSS,
prototype pollution, and postMessage issues — the automation proof
that the object world is systematically scannable. The research wave
alongside: PortSwigger's *DOM Clobbering strikes back* (Feb 2020)
cited as research-wave material without individual attribution (kept
honest in the lineage registry's correction field), and the Web
Security Academy prototype-pollution module that codified the
source→gadget→sink teaching order. Distilled here as decision logic;
nothing of PortSwigger's is vendored. The verification record is
`references/sources.md`.

## 3. First Principles — the WWH registers (A14)

### WHAT — the object model, anatomized

1. **Prototypal inheritance**: almost every object resolves missing
   properties up a chain ending at `Object.prototype`. A property that
   is nobody's own-property but everyone's inherited default is a
   *gadget slot* — code reads `config.transport`, the object has no
   `transport`, and the chain answers.
2. **The pollution sources**: any recursive merge of untrusted keys —
   URL query/hash fragments (`#__proto__[x]=y`), JSON bodies
   (`{"__proto__": {...}}`, which `JSON.parse` turns into an
   own-property that merges behave differently with), constructor
   paths (`constructor.prototype.x`).
3. **The DOM's ambient globals**: named HTML elements (`id`/`name`)
   become properties of `window` and document forms — a script's
   reference to `window.config` can resolve to an attacker-crafted
   `<a id=config>` element (clobbering), and the crafted element's
   own properties (like `href`'s parsed parts) come along.
4. **The message channel**: `postMessage` listeners receive events
   whose `origin` and `source` must be checked by the RECEIVER;
   senders include any page that can hold a reference to the window.
5. **The sinks**: anything that acts on a read property — `eval`
   family, `setTimeout(string)`, DOM-write sinks, `fetch`/XHR option
   reads, HTML injection points, redirect targets.

### WHY — the root causes, mechanically

1. **Pollution exists because merges trust key names**: a recursive
   merge that walks user-controlled keys into nested objects cannot
   tell `__proto__` the *data field* from `__proto__` the *chain
   link* — and once the merge writes through the link, every object
   that shares the prototype inherits the write. `JSON.parse` makes it
   worse by materializing `__proto__` as an own-property first.
2. **Clobbering exists because the DOM namespace and the JS namespace
   were never separated**: named elements bind into global scope by
   platform feature, not by developer intent — so any HTML injection
   point (even an attribute-limited one) is a potential write into
   the script's variable world.
3. **postMessage confusion exists because trust is receiver-side and
   optional**: the platform delivers the message with metadata; the
   check is a discipline, not a mechanism. A listener that checks
   nothing, checks `e.origin` against a substring, or replies to
   `e.source` unchecked, trusts every page on the web.
4. **Gadgets are the amplifier because libraries read defensively**:
   `options.foo ?? default` and `cfg.bar || fallback` look like
   robustness but resolve through the prototype chain first — the
   inherited poisoned value satisfies the read silently. That is why
   pollution without a gadget is a curiosity, and pollution with one
   is a sink feeding.

### HOW — the hunting order, in one line

Source first (where can attacker keys enter a merge, a namespace, or a
channel?), then gadget (which trusted read resolves through what we
control?), then sink (what acts on it?) — each link its own
differential, the chain composed only after every link closes.
`references/object-model-attacks.md` carries the exact probes,
oracles, and falsifiers per family.

War note (A15): the cheng sweep is the source/gadget/sink sweep with
safe probes; the ch'i is the server-side gadget that survives without
the DoS — the escalation path nobody submitted because everyone
stopped at console.log. W2 binds at the sink: the gadget is proven
with a self-owned marker read (a unique key whose resolution an
operator-owned response reveals), never by breaking the process — and
the memory-exhaustion "proof" is refused outright: it proves nothing a
marker could not, and it burns the ground for everyone.

## 3.5 The Method Layer — Critique, Upgrade, M1–M4 (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published Heyes art where it was mechanically weak —
DOM-Invader clicks as the procedure, one error message read by eyes as
the hit rule, gadget hunting before the merge surface is mapped,
library versions unpinned, one-shot pollution claims — and ships the
executable replacement: **M1** the merge-surface inventory (surface
count zero or nonzero ON RECORD before any gadget), **M2** the
calibrated oracle ladder (O1 read-back, O2 error-signature, O3 crash
REFUSED unless pre-registered and rate-capped), **M3** the `__proto__`
differential (treatment vs same-shape control, n ≥ 5, interleave),
**M4** the gadget chaining matrix (five mandatory cells per row,
version-pinned from stack FACTs). Probes come byte-exact from
`references/corpus.json`.

## 3.6 The Operator Layer (A17) — the Gareth Heyes runtime

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
executing, characteristic of Gareth Heyes. Since v1.4.0 it also ships
**The opening ladder** (A18): where Heyes's candidates come from — the
perception layer that PRODUCES ranked merge-surface, gadget, clobber,
and listener candidates on an unseen estate before any write probe is
due (rungs write census rows, never properties; ranking rationale
stated; generation falsifier on record; the merge-surface kit names
corpus entries PP-001..010).

## 4. Procedure — Numbered Actions

1. **Inventory the object-model surface.** From js-recon's bundle
   inventory: merge functions (deep-merge/deep-extend/defaults-style
   calls), `postMessage` listeners and senders, known gadget-rich
   libraries with versions, HTML injection points with attribute
   control (clobbering sources), JSON body endpoints on server-side
   JavaScript stacks.
2. **Write the family hypotheses.** Per candidate: "untrusted keys at
   S resolve through C and are read at G, observable as Z" — one card
   each, pre-registered before any probe.
3. **Client-side pollution probes, canary-twin design.** Hash/query
   source probes using a harmless canary property (a property whose
   only effect is observable: e.g., a form field's default, a link's
   text) — the benign-twin (same shape, no directive) is the control;
   the observable difference is the oracle. Probes that could break
   page function are not sent (the client is shared ground; W2).
4. **Server-side pollution probes, no-DoS only.** The Heyes 2023 safe
   repertoire: status-code override, JSON-spaces, header-reflection,
   OPTIONS reflection, immutable-prototype error signaling — probes
   whose only footprint is an observable response difference, never a
   persistent server-side write that degrades function. Any probe
   that would persist a breaking property is out of doctrine,
   period.
5. **Gadget hunt on confirmed pollution.** From the gadget library
   (and fresh reads of the target's own code): which property reads
   resolve through the chain? String callbacks (`setTimeout`),
   transport configs, option objects — each candidate read is a
   hypothesis with its own observation. Extreme-tier gadget classes
   (the fetch-API body default PP-013, the GTM sequence gadget
   PP-014) release through the weapons vault —
   `payload_release(program, "PP-014", target, note)` — the gate
   scans every caller string for instruction-override attempts,
   resolves the entry in the versioned corpus, and refuses unscoped
   targets; the released bytes are the corpus's bytes, never
   hand-crafted, and the published demonstration vector is rewritten
   to a benign operator marker before it is ever sent (the canary law).
6. **Clobbering differentials.** At each attribute-controlled
   injection point: craft the named element, observe the script's
   reference resolving to it (a debugger-free observable: the
   behavior difference), benign-twin control included.
7. **postMessage discipline check.** Self-owned sender page, crafted
   messages to in-scope frames; the oracle is the listener acting on
   an instruction it should have rejected by origin (or leaking a
   property to an origin it should not). No other user's window is
   ever a sender or a receiver in a proof.
8. **Chain composition.** Pollution/clobbering/message link → gadget
   → sink: chain-architect's law — per-link differentials, ONE joint
   end-to-end proof, per-link severities stated next to the chain's.
9. **Classify.** `cvss3_score` on the crossed path (client-side
   gadget→DOM sink rides XSS geometry; server-side pollution→RCE-class
   sink rides its own); `vrt_classify` under the validation / XSS /
   RCE family rows that match the OBSERVED chain.
10. **Exit gate numbers.** Candidates by family, probes by verdict
    (safe-only), gadgets confirmed, chains composed, joint proofs —
    stated, not summarized.

## 5. Hard Rules (mechanically enforced)

1. **The no-DoS law.** Server-side pollution detection uses only
   reversible, observable-footprint probes; a technique that could
   persist a breaking property is never sent — a broken target ends
   the campaign and the report (W2, and Heyes' corpus' whole point).
2. **Canary properties only.** Every pollution probe writes a
   property whose sole effect is the observable; no probe writes into
   function, network, or auth behavior.
3. **Gadget before exploit.** A pollution claim without its gadget
   read is a lead; a gadget without its sink differential is a lead;
   only the closed chain is a finding.
4. **Sender and receiver are self-owned.** postMessage proofs use the
   operator's own pages and accounts on both ends; no other user's
   window participates.
5. **One source per probe.** Family probes vary one element; combined
   source probes are separate experiments (the inherited law).
6. **Versioned libraries recorded verbatim.** The gadget library
   applies per version; the finding carries the version string it was
   proven on.
7. **Client-side persistence is per-page-load.** State what a
   client-side pollution does and does not persist (refresh resets
   it); the report claims exactly what the records show.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Bundle/library inventory, merge-code location | `js_analyze` + `dossier_add` |
| Client-side probes (hash/query sources) | `http_probe` + `ledger_append` (EXPERIMENT: canary, benign-twin) |
| Server-side safe probes | `http_probe` (OPTIONS/reflection families) + `ledger_append` |
| postMessage sender proofs | self-owned sender page + `ledger_append` |
| Extreme-tier corpus release (PP-013/014) | `payload_release` (the weapons vault — jailbreak scan, corpus resolution, banned-class ban, scope check) |
| Vault accuracy re-verification | `payload_bench` (the labeled release/refusal bench) |
| Chain composition + classification | chain-architect law + `cvss3_score` + `vrt_classify` |
| Report gate | `auditor/audit_report.py` — exit 0 or it does not ship |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Expanding any family into exact probes, oracles, falsifiers; the safe-probe repertoire; the gadget library | `references/object-model-attacks.md` |
| Exact probe set (query/JSON sources, constructor.prototype bypass, Heyes' safe detection oracles — JSON reflection, status-code override, CORS header reflection — the gadget classes incl. CVE-2022-29078 and the browser gadgets: the fetch body default and the GTM sequence eval vector, the DOM-clobber probe families, and the postMessage origin-confusion probe shell), per-technique failure modes, primary sources | `references/corpus.json` (versioned payload corpus, 1.2.0; extreme-tier entries release through `payload_release`) |
| Verifying the Heyes lineage and the research-wave sources | `references/sources.md` |
| Grading the published method, mapping the merge surface, running the differential | `references/method-upgrade.md` |
| Running the hunt — the Gareth Heyes runtime: the opening ladder (A18), thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |

The corpus is versioned (`corpus_version`) and every entry carries its
primary source and its **failure modes** — read them before closing any
hypothesis as negative. The negative-space entry (PP-010) defines what a
REAL negative requires: source reached, merge path version-pinned,
constructor bypass tried, two safe-detection oracles run, cleanup
confirmed. The no-DoS law binds every entry: harmless property writes
only.
