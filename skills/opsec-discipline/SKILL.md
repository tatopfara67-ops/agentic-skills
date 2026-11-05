---
name: opsec-discipline
version: 1.1.0
type: ai-skill
architecture: package
description: >-
  Craft-tier organ forged from the grugq (pseudonymous counterintelligence
  researcher; Phrack 59 "Defeating Forensic Analysis on Unix", Black Hat
  Europe 2005 "The Art of Defiling", the Ekoparty 2012 "OPSEC for Hackers"
  deck, the Kiwicon 2014 "COMSEC: Beyond Encryption" deck with Ben Nagy,
  and the 2013 OPSEC blog cycle) — campaign hygiene as an economic
  discipline. The doctrine: data is evidence, so the operator's own trail
  is priced like any attack surface (detection risk, attribution risk,
  removal cost); the plumbing goes in first because paranoia doesn't work
  retroactively; compartmentation limits the blast radius when — not if —
  a compartment fails, and the three things to secure are identity,
  activity, and association; cover beats concealment because a hidden
  presence is already evidence while an explainable presence ends
  scrutiny; the suspect pool must stay wide — never be the only anomaly
  that narrows attribution; and OPSEC is a practice priced in efficiency
  ("OPSEC will get you through times of no crypto better than crypto
  will get you through times of no OPSEC"). The organ ships with its
  method layer born in (A16): a mechanical critique of the published
  grugq art — the economics stated qualitatively but never tabled, the
  Ten Commandments given as prohibitions without a recovery path for
  contamination already happened, the case post-mortems (LulzSec, DPR,
  Eldo Kim) run ad hoc per event instead of a reusable failure-class
  taxonomy, the ops-platform/staging/launch-pad architecture described
  for clandestine operations but never mapped to authorized engagements,
  the anti-forensics era (destruction/hiding/contraception) and the
  OPSEC era (cover/concealment/compartmentation) never unified into one
  operator-side lifecycle, and the tool guidance era-bound (PORTAL
  hardware, Pond) with no porting rule — and the replacement protocol
  M1–M6: the operator exposure census with priced rows, the
  adversary-and-secrets gate, the hygiene architecture and plumbing
  gate, the communications-event discipline, the suspect-pool audit,
  and the closure audit with retention rows. Born under charter v1.17+,
  it also ships its operator runtime (A17): the thinking rules,
  situation-to-action behavior with refusals, scripting arsenal, and
  rigid run-order characteristic of the lineage. Use when an engagement
  is about to start and the operator's footprint must be planned before
  the first request; when engagement credentials, egress, or storage
  must be separated from the operator's identity; when the target's
  incident response could overlap the engagement and attribution must
  be unambiguous; when client communications or disclosure timing leak
  more than content; or when an engagement closes and raw evidence,
  credentials, and infrastructure must be retired on record ("kebersihan
  kampanye", "jaga jejak operator", "pisahkan kredensial engagement",
  "OPSEC", "opsec", "hygiene kampanye", "compartmentation",
  "kompartemen", "jangan pakai akun pribadi", "egress terpisah",
  "attribution risk", "suspect pool", "cover story", "escape and
  evasion", "data retention", "hapus evidence", "tutup engagement",
  "campaign hygiene", "operator footprint", "compartmentation audit").
category: security/craft-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: the grugq (pseudonymous counterintelligence researcher; South African, Bangkok-based per press records; career record — Fortune 100, @stake — forced out over the Phrack 59 anti-forensics article, independent since) — Phrack 59 "Defeating Forensic Analysis on Unix" (2002), "The Art of Defiling" (Black Hat Asia 2003, Black Hat Europe 2005), the OPSEC corpus ("OPSEC for Hackers — Because Jail is for wuftpd", Ekoparty 2012, later re-serveed as the "OPSEC for Russians" keynote), the 2013 blog cycle (grugq.github.io — "Ignorance Is Strength", "Anonymity Is Hard", "Observations on OPSEC", "OPSEC Isn't Security Through Obscurity", "It Was DPR", "In Search of OPSEC Magic Sauce"), "COMSEC — Beyond Encryption" (Kiwicon 2014, with Ben Nagy), "How Very APT" (TROOPERS 2017), "A Short Course on Cyber War" (Black Hat Asia 2018 keynote), the PORTAL hardware project (github.com/grugq/portal); sixth candidate-queue execution of the lineage-smith forge
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+ (researcher-conduct §34 rides along, not replaced); skill-mythos charter v1.17+; an authorized engagement context (the corpus's clandestine framing is translated, on record, to the client-disclosed frame — concealment from the client is out of scope)
---

# opsec-discipline v1.1.0 — The grugq Lineage

## 0. What This Skill Is — and Is Not

* **Is**: the campaign hygiene layer — the organ that prices the
  OPERATOR's own footprint in cost and attention, before, during, and
  after every authorized engagement. Its unit of work is the
  engagement's operator-side exposure: it censuses every row of trail
  the engagement will generate (credentials, egress, tool
  fingerprints, communications, data at rest, report artifacts),
  prices each row (who sees it, what it links to, what it costs to
  remove), builds the hygiene architecture before the first request
  (per-engagement credentials, declared egress, separated storage),
  disciplines the engagement's communications as events whose timing
  and correlation leak before content does, audits the suspect pool
  whenever incident response could overlap (never be the only anomaly
  that narrows attribution), and closes the engagement with a
  retention-and-destruction audit on record. In the lineage's own
  documented arc: a 2005 Black Hat deck that priced forensic evidence
  as the adversary's raw material; a 2012 deck that gave hackers ten
  commandments, a persona methodology, and an ops architecture; a
  2013 blog cycle that ran five-phase post-mortems on the LulzSec,
  DPR, and Harvard-bomb failures; a 2014 deck that named cover,
  concealment, and compartmentation as the three real controls.
* **Is not**: the scan budget organ — what probing costs the TARGET
  (packets, time, rate-vs-reliability) is scan-economist's ground;
  this organ prices what the whole campaign costs the OPERATOR (of
  which the scan's visibility is one row). Not the passive-recon
  organ — minimizing touches on the target during discovery is
  ghost-crawler's trace ledger; this organ governs the operator side:
  who the operator is, from where, retaining what. Not the disclosure
  engineering organ — coordinating a vendor fix across parties is
  protocol-forensics' ground; this organ governs the operator's own
  comms hygiene (what timing and correlation the operator's messages
  leak). Not a clandestine-operations trainer: the corpus was written
  for operators hiding from states; the house translation re-targets
  its machinery to authorized engagements where the client is
  disclosed, the ROE is the cover document, and hiding from the
  client is out of scope (§7 hard rule 6).
* **Engagement-frame note (the translation, on record)**: the
  corpus's adversary is law enforcement in clandestine operations.
  The authorized engagement's real exposure set is different and
  smaller: the target's SOC/IR attribution machinery (anomalous
  traffic gets attributed — wrongly, if the pool is narrow), third
  parties on the same target (attribution confusion in both
  directions), data exposure (breach of the operator's retained
  evidence), and comms leakage. The information-discipline machinery
  (price the trail, compartment first, cover over concealment, keep
  the pool wide, close with destruction) carries over unchanged; the
  adversary set does not.

## 1. The Lineage (attribution)

The grugq — pseudonymous counterintelligence researcher, the
signature on two decades of anti-forensics and OPSEC art. The
documented career arc: a Fortune 100 start, then @stake, "where he
was forced to resign for publishing a Phrack article on
anti-forensics" (the John W. Little interview, 2013) — Phrack 59's
"Defeating Forensic Analysis on Unix" (2002, the author record at
phrack.org); independent researcher since, South African and
Bangkok-based per the press record, publishing as "the grugq" and
latterly "Thaddeus Grugq" (a byline, never a verified legal name —
the pseudonym is part of the method). The documented corpus: "The
Art of Defiling: Defeating Forensic Analysis" (Black Hat Asia 2003;
Black Hat Europe 2005 — the anti-forensic principle "data is
evidence", the destruction/hiding/contraception triad, FISTing, the
Rune/Waffen/KY/Data-Mule filesystem attacks); the presentations
index 2003–2018 (VoIPhreaking 2006–2007, "How the Leopard Hides His
Spots" 2008, "From Russia with Love.exe" 2009, "Base Jumping" Black
Hat USA 2010, the HITB KUL 2012 panel, "An Underground Education"
2013, "Click and Dragger" 2014, "Tactical Cyber" and "On Cyber" PoC
2015, "How Very APT" TROOPERS 2017, "A Short Course on Cyber War"
Black Hat Asia 2018); "OPSEC for Hackers: Because Jail is for
wuftpd" (Ekoparty 2012 — the Ten Hack Commandments, the persona and
legend methodology, the LulzSec violation-by-violation post-mortem,
the ops-platform/staging/launch-pad architecture, the VPN-vs-TOR
distinction, the fail-closed PORTAL doctrine; the deck was
re-serveed for later years as the "OPSEC for Russians" keynote);
the 2013 blog cycle at grugq.github.io ("Ignorance Is Strength" —
the compartmentation SOP for individuals; "Anonymity Is Hard" — the
Hezbollah-vs-CIA ring rollback as the reusable pattern;
"Observations on OPSEC" — the economics: "OPSEC is a mode of
operating, not a tool", "OPSEC comes at a cost, and a significant
part of that cost is efficiency", the SDR time-price of
communication; "OPSEC Isn't Security Through Obscurity" — the
system view with the dead-drop secret-key analogy; "It Was DPR" —
the Ulbricht contamination-chain post-mortem; "In Search of OPSEC
Magic Sauce" — the Eldo Kim five-phase post-mortem and the
suspect-pool doctrine); "COMSEC: Beyond Encryption" (Kiwicon 2014,
with Ben Nagy — the communications event, cover/concealment/
compartmentation, the cell-size-five research, "you can't win —
plan for failure", the tools-as-weights metaphor); "How Very APT"
(TROOPERS 2017); "A Short Course on Cyber War" (Black Hat Asia
2018); the PORTAL project — Personal Onion Router To Assure
Liberty (github.com/grugq/portal, the fail-closed hardware
appliance); the interview record (Blogs of War/John W. Little 2013,
Risky Business #285 2013, the ongoing Between Two Nerds series);
and the later keynote/newsletter era (2022–2023). Press records:
Forbes 2012 (the pseudonymous exploit-broker profile), Wired 2021
("a well-known South African exploit broker"), Okta's hacker
series ("most quoted man in infosec" — press framing, quarantined).
Nothing here is his code; this is his decision logic, re-expressed
as engagement rules. Sources and the read ledger:
references/sources.md — the verification record.

## 2. The Five Laws of Campaign Discipline

1. **Data is evidence — the operator's trail is priced like any
   attack surface.** The 2005 anti-forensic principle inverts for
   the operator's own ground: every artifact the engagement
   generates or touches (a credential, an egress record, a raw
   request log, a retained screenshot, a report draft) is a row
   with detection risk (who sees it), attribution risk (what it
   links to), and removal cost. "The goal is to reduce the quantity
   and the quality of information available to the adversary"
   (2013, the interview) — for the authorized engagement, the
   "adversary" reading that trail is whoever ends up holding it:
   the target's IR, a third party, a future breach of the
   operator's storage.
2. **The plumbing goes in first — paranoia doesn't work
   retroactively.** Commandment six and its 2013 gloss: "OPSEC is
   prophylactic, you might not need it now, but when you do, you
   can't activate it retroactively." Hygiene architecture exists
   BEFORE the first request: per-engagement credentials minted,
   egress declared, storage separated. An engagement that starts
   clean and plans to "add OPSEC later" has already failed a gate
   that cannot be re-passed.
3. **Compartmentation limits the blast radius — secure identity,
   activity, association.** "Compartmentation is the foundation of
   good security. When all else fails, your compartments limit the
   damage" (2014). The three things the operator actually protects
   (2013): the operator's identity, the activity itself, and the
   association between them. Anything shared across compartments —
   one credential, one browser profile, one egress — is a fuse
   between them; failure is assumed ("you only got to fuck up
   once", the Avon Barksdale rule the corpus quotes twice), so the
   architecture, not the vigilance, does the containing.
4. **Cover beats concealment — an explainable presence ends
   scrutiny; a hidden one feeds it.** Cover is the story that
   stops the question ("a backpacker schmuck on his gap year");
   concealment is the signal that starts one ("a Blackphone at the
   border... you've already given me a reason to keep an eye on
   you", 2014). In the authorized frame the ROE is the primary
   cover — the engagement letter explains presence, scope, and
   source; apparent cover is next (traffic that looks like the
   expected baseline); pure concealment is the fragile last resort.
   The suspect-pool corollary: if the operator's activity is the
   only anomaly in the window, every incident in that window gets
   attributed to the operator — including other people's.
5. **OPSEC is a practice priced in efficiency — slow is the cost,
   latency is the currency.** "OPSEC is a mode of operating, not a
   tool or a collection of tools... OPSEC comes at a cost, and a
   significant part of that cost is efficiency. OPSEC is slow"
   (2013). The latency budget is therefore a stated number, not an
   apology: comms are batched and unhurried because "latency is
   directly correlated to security" (2014); the doctrine survives
   tool churn because "OPSEC will get you through times of no
   crypto better than crypto will get you through times of no
   OPSEC" (2013).

## 3. The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered.
`references/method-upgrade.md` grades the published grugq art where
it was mechanically weak — the economics stated qualitatively
("slow", "expensive", "at the cost of efficiency") but never tabled
into priced rows; the Ten Commandments written as prohibitions with
no recovery path for the contamination that has already happened;
the case post-mortems (LulzSec, DPR, Eldo Kim) run ad hoc per event
instead of compiled into a reusable failure-class taxonomy; the
ops-platform/staging/launch-pad architecture described for
clandestine operations but never translated to the authorized
engagement; the anti-forensics era and the OPSEC era never unified
into one operator-side lifecycle; and the tool guidance era-bound
(PORTAL hardware, Pond) with the porting rule unstated — and ships
the executable replacement: **M1** the operator exposure census
with priced rows and the scan-economist/ghost-crawler boundary
rows, **M2** the adversary-and-secrets gate (intent × capability
matrix, identity/activity/association), **M3** the hygiene
architecture and the plumbing gate (declared egress, per-engagement
credentials, fail-closed separation), **M4** the
communications-event discipline (timing, correlation, latency
budget, shared-context minimization), **M5** the suspect-pool audit
(the anomaly check against IR overlap), and **M6** the closure
audit with retention rows (the destruction/hiding/contraception
triad applied to the operator's own artifacts, the dossier
compartmented but never destroyed).

## 4. The Operator Layer (A17) — the grugq runtime

`references/operator-os.md` ships the figure's documented psychology
as the agent's RUNTIME: the thinking framework (numbered if-then
rules — the trail priced, the plumbing first, compartment or burn,
cover over concealment, the pool kept wide, latency bought, failure
planned for), the behavioral protocol (situation → move → agent
action → refusal, with the refusals doing heavy lifting: no first
request before the plumbing gate, no personal credential reuse, no
undeclared egress, no concealment beyond the ROE), the scripting
arsenal (the exposure census worksheet, the adversary matrix
builder, the plumbing gate checklist, the comms planner, the
suspect-pool audit against the engagement's own ledger, the closure
checklist renderer — operator-side and read-only), and the rigid
run-order binding all of it onto M1–M6. Load it when the campaign
hygiene runs: the doctrine states the laws, the M-protocol states
the procedure — the operator OS is how the agent BEHAVES while
executing, characteristic of the grugq: priced, aphoristic,
case-citing, allergic to tool worship. Since v1.1.0 it also ships
**The opening ladder** (A18): where the grugq's candidates come from
— the perception layer that PRODUCES ranked exposure candidates from
the yet-to-exist trail before the first request flows (rungs write
pricing rows, never requests; ranking rationale stated; generation
falsifier on record; the exposure-pricing kit is the pinned census
row set).

## 5. Procedure — Numbered Actions

1. **Read the cover document first** (M2): the engagement letter
   and ROE are read as the cover — what presence is expected,
   from what sources, in what windows. The expected-traffic
   definition is extracted on record before any census row is
   priced. Scope violations are conduct incidents (the spine's
   §34), not hygiene rows.
2. **Census the operator's exposure** (M1): one row per trail item
   the engagement will generate — credentials (accounts, API keys,
  session tokens), egress (source IPs, declared chains), tool
   fingerprints (UA strings, scanner signatures), communications
   (client mail, disclosure threads), data at rest (raw evidence,
   screenshots, notes), report artifacts (drafts, the final
   report). Each row priced: detection (who sees it), attribution
   (what it links to), removal cost; ranked by product. Boundary
   rows on record: vs scan-economist (target-side scan budget) and
   vs ghost-crawler (target-side touch minimization). A census with
   fewer than three rows is a hygiene reading, not a census — park
   and say so.
3. **Run the adversary-and-secrets gate** (M2): the intent ×
   capability matrix over the real exposure set (target SOC/IR,
   third parties on the same target, retention/breach risk of the
   operator's own storage, comms leakage); the secrets table
   (identity, activity, association); the latency budget stated as
   a number.
4. **Build the plumbing before the first request** (M3): the
   architecture gate — per-engagement credentials minted and stored
   separated; egress declared in the ROE or declared to the client
   (a VPN chain improvised mid-engagement is a concealment move,
   not hygiene); the per-engagement tooling environment fresh
   (snapshot to revert at closure); storage separated from the
   operator's personal ground. Fail-closed beats fail-open: the
   PORTAL doctrine translated — separation by construction (a
   credential that CANNOT reach personal ground), not by discipline
   (a credential you promise not to reuse).
5. **Discipline the communications as events** (M4): every client
   and disclosure communication is an event whose timing, cadence,
   and correlation leak before content does — batch, un-hurry per
   the latency budget, break schedule regularity where cadence
   itself is a signal, say less (shared-context minimization).
   Vendor-fix coordination itself is protocol-forensics' ground;
   this organ owns only the operator's side of the wire.
6. **Audit the suspect pool at every IR-overlap moment** (M5):
   whenever an incident could land inside the engagement window,
   check whether the operator's activity is the only anomaly
   matching — if it is, attribution of EVERYTHING anomalous
   converges on the operator, and the client must hear it before
   their IR does. Blending rules apply: act inside declared scope
   and windows; carry no operator-identifying data in engagement
   account names; where attribution of the operator's own traffic
   is REQUIRED (authorized engagements usually do), declare it —
   that is cover, stated.
7. **Close with the retention-and-destruction audit** (M6): at
   engagement end — destruction of raw target evidence per ROE
   (with the destruction row on record), contraception of what was
   collected in the first place (collect only what a finding
   needs), compartment retirement (staging reverted, credentials
   rotated or retired, infrastructure released), report archival
   per client terms. The dossier's R-NNN method records are the
   house's epistemology: compartmented, never destroyed. The
   five-phase frame (target selection → planning → deployment →
   execution → escape and evasion) prices the exit — the phase
   engagements habitually leave unplanned.
8. **File the post-mortem row** (M6): every hygiene incident —
   contamination, attribution confusion, retention overrun — joins
   the failure-class ledger (contamination / profiling /
   home-base / reveal / trust), because the corpus's own method is
   the case post-mortem: read the failures, price the lesson. A
   hygiene incident without its ledger row is an anecdote.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Exposure census rows, matrix rows, plumbing gate records, closure rows | `dossier_add` + this organ's M1–M6 record formats |
| Latency budgets, rank arithmetic, retention arithmetic | computed on record (references/method-upgrade.md; recompute, never recall) |
| Scan cost on the target side (packets, time, rate) | scan-economist organ (its budget table governs) |
| Passive-recon touch minimization on the target | ghost-crawler organ (its trace ledger governs) |
| Disclosure coordination with a vendor | protocol-forensics organ (its disclosure engineering governs) |
| Conduct moments, anomaly reactions, legal stops | spine researcher-conduct §34 (rides along, never replaced) |
| Report drafting and delivery | `dossier_render` + report organs (report gates apply) |

## 7. Hard Rules

1. The census before the first request: an engagement that emits
   traffic with no exposure census on record has failed a gate
   that cannot be re-passed — retroactive paranoia does not exist.
2. No personal credential ever touches engagement ground: the
   credential that links the trail to the operator's identity is
   the contamination the whole architecture exists to prevent.
3. Egress is declared, never improvised: hiding from the client is
   out of scope — concealment beyond the declared cover is a
   scope violation wearing a hygiene costume.
4. The suspect pool is checked at every IR overlap: if the
   operator is the only anomaly, the client hears it first, on
   record.
5. The dossier is compartmented, never destroyed: the
   destruction/hiding/contraception triad governs raw evidence and
   residue per ROE — the method record is the house's memory.
6. The translation stays on record: this organ prices the
   operator's footprint in authorized engagements; it does not
   train clandestine tradecraft, and no distillation line may cite
   the corpus's evade-law-enforcement framing as procedure.

## 8. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Running the hygiene lifecycle end to end (census schema, matrix gates, plumbing checklist, comms rules, suspect-pool audit, closure formats) | references/method-upgrade.md |
| Running the hygiene — the grugq runtime: the opening ladder (A18), thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
| Checking what was actually read; the census, read ledger, psych-read evidence | references/sources.md |
