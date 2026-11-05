---
name: mobile-hunter
version: 1.3.0
type: ai-skill
architecture: package
description: >-
  Deep-technical organ (tier 3) built from the Charlie Miller lineage (with
  Collin Mulliner on the 2009 iPhone SMS compromise) — the mobile teardown
  discipline for authorized bug bounty on Android (APK) and iOS (IPA) targets.
  The shipped binary is treated as a confession read in full before the device
  is ever touched (manifest, exported components, deep links, bundled strings
  and secrets, ghost endpoints), store review and code-signing are treated as
  hypotheses about attacker effort rather than walls, and every finding lands
  at a boundary — the API differential behind the app, or the runtime
  observation on an operator-owned device. Carries the WWH registers (WHAT the
  mobile attack surface is, WHY each class exists mechanically, HOW it is
  hunted step by step), the static-before-dynamic ladder, and the evidence law
  that every claim cites file:line from the artifact. Since v1.1.0 the organ
  carries the executable method layer (A16) — a mechanical critique of the
  Miller/Mulliner art's floors (one-shot exploit narratives, dumb mutational
  fuzzing, the bench-to-field gap unmeasured, reversing as expert narration,
  demo theater as proof) shipped as protocol M1–M5: the device baseline
  inventory, coverage-gated harness discipline with budget tables, the crash
  signature-hash triage protocol, the exploit reliability differential (n ≥ 10
  with condition lists), and the fleet-gap statement. Use when the target
  ships a mobile app in scope, when the operator provides an APK/IPA, when
  mobile-only endpoints or ghost APIs are suspected, or when the operator says
  to audit the app ("audit APK ini", "uji aplikasi mobile mereka", "cari celah
  di app-nya", "mobile app testing", "iOS app hunting", "ada endpoint yang
  cuma app yang manggil").
category: security/deep-technical
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Charlie Miller (iOS Hacker's Handbook, Wiley 2012; Pwn2Own champion 2008/2009; five years NSA; the 2011 Instastock code-signing demonstration; the 2015 remote Jeep exploit with Chris Valasek) with Collin Mulliner (the 2009 SMS compromise of the iPhone, demonstrated jointly)
  tier: 3 — deep technical (the mobile teardown discipline)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.5+ (R0 scope gate, ledger, differential triad); js-recon (client-code reading discipline); auth-boundary-mapper (the API-boundary differentials)
---

# mobile-hunter v1.2.0 — The Binary Is a Confession

## 0. What This Skill Is — and Is Not

* **Is**: the organ for authorized hunting on mobile application
  targets — Android APKs and iOS IPAs that the program's scope covers
  and the operator supplies or authorizes downloading from the official
  store. Its unit of work is the same as every tier-3 organ: a claim
  proven by a differential, with the added geometry that the app is a
  *client* to the same web API the program already pays for — so the
  richest mobile findings are API-boundary findings the web surface
  never exposed (ghost endpoints, mobile-only parameters, deprecated
  API versions still trusted by shipped binaries).
* **Is not**: piracy tooling, repackaging, or store-review
  circumvention research. It does not distribute modified binaries, it
  does not attack the store, and it does not run other people's
  devices. It is also not mobile malware research: the adversary
  direction lives in adversary-tracker's world, not here.

## 1. Inherited Contracts

Plugs into **Phase 1** (the app artifact joins the dossier as an asset
with its own entry), **Phase 2** (the app's API calls join the
authorization matrix — mobile is a client role), and **Phase 3**
(differentials at the API boundary). Inherits the experiment contract
(§6), the canary doctrine (§8 — runtime proofs run on operator-owned
accounts and self-owned artifacts), the closure vocabulary (§7), and
the secrets policy absolute (bundled secrets are masked, report-only,
never used). js-recon's reading discipline governs decompiled-source
review; auth-boundary-mapper's matrix governs the boundary
differentials the app's traffic implies.

## 2. The Lineage (attribution)

**Charlie Miller** is the public figure this organ's discipline is
distilled from: co-author of *iOS Hacker's Handbook* (Wiley, 2012,
with Dino Dai Zovi, Aaron Portnoy, and David Weinstein), five years at
the NSA before independent research, Pwn2Own champion (2008, the
MacBook Air; 2009, Safari), and the researcher whose 2011 *Instastock*
demonstration showed an App-Store-approved app downloading unapproved
logic at runtime — research on his own app that got him expelled from
the store, and the cleanest public lesson that store review is an
attacker-effort hypothesis, not a wall. With **Collin Mulliner** he
demonstrated the 2009 SMS-processing compromise of the iPhone — the
telephony attack surface most web hunters never touch. The later
Miller–Valasek remote Jeep work (2015) extends the same doctrine to
vehicles: the shipped binary and its update channels are the attack
surface. Distilled here as decision logic only; nothing of theirs is
vendored. The verification record is `references/sources.md`.

## 3. First Principles — the WWH registers (A14)

### WHAT — the mobile attack surface, anatomized

1. **The artifact**: APK (zip of DEX, resources, manifest, native
   libraries) or IPA (zip of the binary, Info.plist, bundles,
   entitlements). Everything the app will ever do is in there or
   fetched by something in there.
2. **The manifest layer** (Android: `AndroidManifest.xml`; iOS:
   `Info.plist`): exported components (activities, services,
   receivers, content providers), deep-link schemes and intent
   filters, permissions, debuggable/backup flags, URL schemes,
   ATS/NSAppTransportSecurity exceptions.
3. **The code layer**: decompiled application logic, bundled SDKs and
   their versions, WebView configurations (JavaScript, file access,
   universal links), crypto usage, certificate-pinning
   implementations, IPC handlers.
4. **The data layer**: bundled strings, "hidden" endpoints, API keys
   and tokens, feature flags, remote-config defaults, test/staging
   URLs that still resolve.
5. **The boundary layer**: the traffic the app actually sends —
   headers, tokens, mobile-only parameters, deprecated API versions —
   meeting the server's authorization decisions.
6. **The runtime layer** (operator-owned devices only): local storage
   (SharedPreferences, plists, Keychain/Keystore usage), logging,
   cache directories, IPC at execution.

### WHY — the root causes, mechanically

1. **Exported surface exists because inter-app communication is a
   platform feature**: any component that answers other apps' intents
   is reachable by any other app on the device; "reachable" plus
   "unvalidated input" is the same bug class as any web parameter, one
   platform down.
2. **Secrets ship because the binary is a client with no vault**:
   anything the app needs offline ships inside it, and extraction is
   unzip + strings — obfuscation raises effort, never to infinity
   (the code-signing-as-hypothesis law, straight from Instastock).
3. **Ghost endpoints exist because mobile release cadence is slower
   than web**: the app binary in users' hands pins API versions the
   web frontend abandoned — old routes stay alive for shipped
   binaries, and their authorization was frozen years ago.
4. **Mobile-only parameters exist because apps send what the platform
   makes easy** (device identifiers, carrier data, push tokens) — and
   server-side trust of client-attested values is the root cause of
   every BOLA/IDOR variant this organ hunts at the boundary.
5. **Pinning fails open or not at all because it is client code**: a
   pinning bypass is a client-side effort wall, identical in kind to
   store review — both are recorded, tested where scope allows, and
   never assumed to be walls.

### HOW — the procedure, in order

The numbered procedure is §4; the method module
(`references/mobile-method.md`) expands each rung with its oracles and
falsifiers. The one-line form: read the binary until it has nothing
left to confess, reconcile its endpoints against the web surface map,
then run boundary differentials on everything the app trusts that the
web never showed you.

War note (A15): the cheng sweep is the manifest + strings + secret
read of the shipped artifact; the ch'i is the ghost endpoint still
resolving, and the pinning bypass that turns the app into an
authenticated client of the API nobody mapped. W1 binds hardest here:
the store listing and the shipped binary are the spies' report — the
device is touched only after the confession is fully written. W2: the
client-side bypass is proven on an operator-owned device; other users'
installs are not instruments.

## 3.5 The Method Layer — Critique, Upgrade, M1–M5 (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published mobile art where it was mechanically weak —
exploits told as after-the-fact stories without rerun counts, mutation
without coverage gates, crash piles triaged by eyes, the bench Jeep
treated as the fleet, the method living in the IDA seat — and ships
the executable replacement: **M1** the device baseline inventory
(exact build, entitlements, signature posture, fleet variance table
as FACTs), **M2** harness discipline (reachability proof before
budget, coverage-slice gates, retire/reseed on zero new branches),
**M3** crash triage (stack signature hash → cluster table, n ≥ 5
repro rule, remote-reachability severity gate), **M4** the exploit
differential (n ≥ 10, bucket distribution, precondition list,
operator-owned marker end-state), **M5** the fleet-gap statement
(proven on the tested set; the fleet is arithmetic with sources,
never rounded up).

## 3.6 The Operator Layer (A17) — the Charlie Miller runtime

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
executing, characteristic of Charlie Miller. Since v1.3.0 it also
ships **The opening ladder** (A18): where Miller's candidates come
from — the perception layer that PRODUCES candidates before any
verification is due (rungs write census rows, never packets; ranking
rationale stated; generation falsifier on record; the entry-point
seed kit fires only inside T4's bounded lab runs).

## 4. Procedure — Numbered Actions

1. **Scope the artifact.** R0 gate first: is the app in the program's
   scope? Only operator-supplied artifacts or official-store downloads
   of in-scope apps; record provenance (store, version, hash) in the
   dossier before anything is unpacked.
2. **Unpack and inventory.** APK/IPA extracted; manifest/Info.plist
   parsed; the inventory table written (exported components, schemes,
   flags, permissions, ATS exceptions) with file:line citations. One
   dossier entry per finding-shaped surface.
3. **Run the confession sweep.** Strings, bundled resources, remote
   config, native libraries: endpoints, API keys (masked — the secrets
   policy absolute applies), staging URLs, feature flags. Every hit
   becomes a HYPOTHESIS card with its citation.
4. **Reconcile against the web map.** Diff the app's endpoint set
   against api-surface-mapper's inventory: endpoints the web never
   calls are ghost endpoints — hypotheses for the boundary
   differential, not findings yet.
5. **Read the code where it matters.** WebView configs, IPC handlers,
   pinning implementations, crypto call sites — js-recon's reading
   discipline, applied to decompiled source. Every claim cites
   file:line of the artifact.
6. **Boundary differentials.** Replay the app's requests (operator
   account, self-owned objects) with the auth-boundary-mapper matrix:
   role×resource on mobile-only routes, object identifiers swapped,
   deprecated-version authorization. The differential triad applies
   unchanged — baseline / treatment / control, ledgered.
7. **Runtime proofs, operator-owned only.** Device or emulator the
   operator owns, operator account: deep-link reachability, exported
   component behavior, storage observations. Screenshots and captured
   traffic are the evidence; no other user's data ever enters a proof.
8. **Classify at the observed boundary.** `cvss3_score` on the path
   that actually crossed (a pinning bypass alone is hardening evidence;
   pinning bypass → ghost endpoint → cross-account object is the
   finding). `vrt_classify` with the mobile rows of the taxonomy.
9. **Exit gate numbers.** Artifacts inventoried, components exported,
   strings swept, endpoints reconciled (ghosts by state), boundary
   differentials run, runtime proofs — stated, not summarized.

## 5. Hard Rules (mechanically enforced)

1. **The binary is evidence.** Every static claim cites file:line from
   the unpacked artifact; "it feels insecure" is not a record.
2. **Static before dynamic.** The teardown record (steps 2–5) precedes
   any runtime action; a runtime probe without its static hypothesis
   is noise, and noise fails the audit.
3. **Operator-owned at runtime.** Devices, emulators, accounts: the
   operator's. No other user's data in any proof, ever.
4. **Findings land at boundaries.** The API differential or the
   runtime observation on an owned device — never a client-side
   assertion about what the app "would probably" do.
5. **Ghost endpoints are hypotheses** until their own boundary
   differential runs; an endpoint's existence is not a vulnerability.
6. **Secrets are report-only.** Masked in records, full values in
   on-disk artifacts for the operator, never used, never echoed
   (secrets policy absolute).
7. **Review and signing are hypotheses.** Recorded as effort walls,
   tested only within scope rules, never assumed impassable — and
   never demonstrated by distributing anything.
8. **Provenance recorded.** Store, version, and hash of every analyzed
   artifact ride with the finding; behavior drifts across releases and
   the report must survive the drift.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Artifact unpacking, manifest/strings extraction | `arsenal_route` (governed CLI, allowlisted) + `dossier_add` |
| Endpoint reconciliation against the web inventory | `api_introspect` + `js_analyze` comparisons |
| Boundary differentials on ghost/mobile-only routes | `http_probe` (operator session) + `ledger_append` |
| Runtime captures (operator-owned device) | `ledger_append` (EXPERIMENT: capture references, hypothesis) |
| Classification | `cvss3_score` + `vrt_classify` |
| Report gate | `auditor/audit_report.py` — exit 0 or it does not ship |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Expanding any rung of §3/§4 into exact steps, oracles, falsifiers | `references/mobile-method.md` |
| Verifying the Miller/Mulliner lineage and its sources | `references/sources.md` |
| Grading the published method, running harness budgets, triaging crashes, claiming reliability | `references/method-upgrade.md` |
| Running the hunt — the Charlie Miller runtime: the opening ladder (A18), thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
