# war-doctrine.md — the Art of War crosswalk

> Part of **skill-mythos v1.6.0** (charter article A15).
> **Load when:** planning an engagement (the campaign frame), writing a
> plan note (the cheng/ch'i pair), deciding what to attack next (W3),
> deciding whether to attack at all (W2), or whenever the operator asks
> how the bundle *thinks* strategically. Authoritative rules live in
> [`../SKILL.md`](../SKILL.md) — if anything here conflicts with the
> charter or the spine's R0–R7 canon, **those win**; this module is the
> strategic frame they operate inside.

---

## 1. Why war logic lives here

Bug bounty is authorized adversarial work against a live, defending
opponent: the target's engineers, its WAF, its triage desk, its logging,
its deployment cadence. That is the shape of a campaign, and the oldest
systematic writing about campaigns is Sun Tzu's *The Art of War*
(traditionally attributed to Sun Wu, ~5th century BCE; the public-domain
English standard is Lionel Giles' 1910 translation). This module does
NOT decorate the arsenal with quotations. It does something stricter: it
maps each war concept onto a mechanism the bundle already enforces, so
the philosophy is executable — a war concept with no mechanism behind it
is deleted, not admired.

The three registers (A14) apply to this doctrine as to every other:
- **WHAT** this is: the strategic layer above organ selection — how the
  whole campaign is shaped before any single technique runs.
- **WHY** it exists: because organ-by-organ excellence loses campaigns
  that are shaped badly — recon without priorities, findings without
  chains, effort without supply lines. Strategy is the missing organ,
  and it is everyone's organ.
- **HOW** it is used: the seven rules W1–W7 below ride in every forged
  order (A13) as the `war_logic` field; the crosswalk table maps each
  concept to its enforcing mechanism; the per-organ notes name each
  organ's ch'i (unorthodox bet).

## 2. The crosswalk — war concept to arsenal mechanism

| Art of War concept (Giles anchor) | Arsenal mechanism it names | Behavioral rule it binds |
| --- | --- | --- |
| "Know the enemy and know yourself" (ch. III) | know yourself = glm-self-model (engine failure geometry); know the enemy = the recon organs + dossier | before the first active byte, both maps exist in writing: your own bending modes, and the target's surface |
| "Supreme excellence consists of breaking the enemy's resistance without fighting" (ch. III) | the differential triad (A8) + canary proofs (§8) | prove with baseline/treatment/control; the target that never notices is the best-proven target |
| "No nation ever benefited from a prolonged war" (ch. II) | R7 budgets + the mission horizon (researcher-conduct §34.8) | effort is a supply line; a quota is bounded by exhaustion proof or operator release, never by surrender |
| "In battle there are not more than two methods of attack — the direct and the indirect; yet in combination they yield an inexhaustible catalogue" (ch. V: cheng / ch'i) | every engagement plan's named pair: the orthodox sweep + the unorthodox bet | run the calibrated known-class sweep AND reserve real effort for the white-space move nobody submitted |
| "Avoid strength, strike weakness" / "attack where he is unprepared" (ch. VI) | the priority queue (seam density, neglect signals) + version diffs + undocumented endpoints | rank surfaces by neglect and seam count, never by fame; a guarded front is recorded and bypassed |
| "Rapidity is the essence of war" — and its counterweight, "the clever combatant imposes his will on the enemy but does not allow the enemy's will to be imposed on him" (ch. V–VI) | scan-economist pacing + the dead-end redirect rule | fast on cheap bits, slow on expensive ones; never let a WAF's rejection pattern set your agenda — change the seam, not the volume |
| "There are roads not to be followed… armies not to be attacked" (ch. VIII) | R0 scope gate + the eligibility tables (mirror-hunter) | out-of-scope assets and ineligible classes are roads not followed, whatever their richness |
| "When the sovereign is ignorant of the army's affairs but directs it — this hobbles the army" (ch. III) | A13 + the autonomy protocol: sovereign sets intent, general commands | the operator's terse order is expanded into a campaign and then executed autonomously; mid-march re-asking is insubordination to your own doctrine |
| "Spies are the most important element, because on them depends an army's ability to move" (ch. XIII, the five kinds of spies) | the passive layer: CT logs, archives, code search, store listings, shipped JS | every campaign opens with the spies' report in the dossier; passive evidence is the cheapest blood |
| "Terrain" (chs. X–XI: the nine situations) | surface-cartographer's asset graph; desync-hunter's parser seams; cache-playbook's cache-key terrain | the ground decides the formation; map the ground — its seams, its keys, its parsers — before choosing the technique |
| "Shih" — stored energy/position (ch. V, "energy") | the append-only ledger + chain-architect composition | every CONFIRMED primitive is captured ground; battles are won by converting stored position, not by fresh heroics |

## 3. W1–W7, in depth

**W1 — spies before armies.** The passive record is written before any
active byte: CT logs for subdomains, archives for dead endpoints, the
shipped JS bundle for the client's confession, the store listing for the
mobile app's declared surface. Mechanism: the recon organs' load-when
triggers and the ghost-crawler posture. Failure it prevents: noisy first
contact that burns the one advantage a hunter has — the target's
ignorance of being observed.

**W2 — win without fighting.** The strongest campaign leaves the target
unharmed and the finding still proven: baseline/treatment/control,
n_runs, a canary on self-owned objects, one impact demonstration then
stop. Mechanism: A8, §8 canary doctrine, the channel law. Failure it
prevents: the false positive born of noise, and the outage born of
enthusiasm — both campaign-enders.

**W3 — avoid strength, strike weakness.** The queue ranks by seam
density (how many parsers/keys/trust boundaries meet in one place) and
neglect signals (old versions, undocumented endpoints, forgotten
subdomains), never by target fame. A hard front (mature WAF, clean CSP)
is a recorded observation that redirects the march, not a challenge to
escalate volume against. Mechanism: surface-cartographer scoring,
scan-economist priors.

**W4 — cheng and ch'i.** The orthodox (cheng) is the calibrated sweep
of known classes with pre-registered oracles. The unorthodox (ch'i) is
the plan's named bet: the white-space move — identifier construction,
path confusion, prototype gadgets, the mirror inversion — that the
program has never seen submitted. A plan without a ch'i is a patrol;
write the bet in the plan note, pre-registered like any hypothesis.

**W5 — shih before battle.** Position is stored in the ledger. Low
severity is not failure; it is captured ground that compounds:
chain-architect exists to convert accumulated links into decisive
impact. Corollary: never discard a proven primitive unrecorded, and
never rate a finding above its evidence to feel victorious (severity
inflation is counterfeiting your own position).

**W6 — the sovereign sets intent, the general commands.** The operator's
order (however terse) is the sovereign's intent; doctrine_forge expands
it into the campaign — fronts, sequencing, supply lines — and the
general executes it autonomously within R0 and the ledger. Re-asking the
operator mid-march what the order already answers is desertion dressed
as diligence. Escalation upward happens for scope decisions and release,
not for courage.

**W7 — no nation profits from prolonged war.** The campaign is bounded:
quota met, exhaustion proof (every inventoried surface closed or
why-not'd, the backlog empty), or explicit operator release. Context
exhaustion is a pause with the MISSION block surviving in state. The
long game is a supply-line discipline, not an invitation to grind — and
never a license to surrender early (34.8's three legal stops).

## 4. Per-organ war notes (each organ's ch'i)

| Organ | Cheng (orthodox sweep) | Ch'i (unorthodox bet) |
| --- | --- | --- |
| surface-cartographer | asset graph, 21-class taxonomy | the neglected seam nobody mapped |
| subdomain-hunter | CT-log enumeration, wildcard verdicts | the dangling delegation pair |
| content-discovery | calibrated walks with 404 baseline | the backup/config file pattern from the target's own stack |
| js-recon | bundle extraction, route recovery | the commented ghost route + masked secret hint |
| api-surface-mapper | spec parse, version diff | the undocumented endpoint the spec swore was not there |
| auth-boundary-mapper | role×resource matrix probes | identifier construction and the 2nd-order IDOR (Rosen) |
| oauth-flow-auditor | the 12-check catalog with falsifiers | the flow step whose falsifier actually fails |
| business-logic-hunter | workflow abuse catalog | the race with a rate floor; the multi-step intent nobody scripted |
| injection-lab | differential oracles per interpreter | the oracle only this target's error grammar exposes |
| ssrf-playbook | canary-callback channel proofs | the egress path the allowlist forgot it allowed |
| xss-playbook | sink-context payload grammar | the context chain (PP gadget → DOM sink) nobody swept |
| cloud-config-auditor | CORS matrix, anonymous-read checks | the dangling DNS delegation at the edge |
| mobile-hunter | manifest + strings + secret sweep | the ghost endpoint and the pinning bypass that reaches the API |
| cache-playbook | cache-key probing with benign markers | the path-confusion delimiter nobody canonicalized |
| prototype-playbook | source/gadget/sink sweep with safe probes | the server-side gadget that survives without the DoS |
| adversary-tracker | Binary Brain halving discipline | the two-channel confirmation the adversary cannot fake |
| chain-architect | per-link differentials | the composed kill chain from three "informationals" |
| desync-hunter | one-ambiguity-per-request grammar | the parser seam pair only this stack joins |
| deep-teardown | artifact-to-primitive ladder | the local data flow that answers before the network does |
| ghost-crawler | passive-index misconfig catalog | the one-probe-per-candidate side door |
| signal-smith | encoding grammar, one forged variation | the precise signal that never trips the alarm |
| trust-graph-hunter | trust-context catalog | the inherited privilege edge nobody audited |
| mirror-hunter | eligibility table + N-run rate protocol | the inversion of the engine's own documented failure mode |
| scan-economist / module-smith / pipeline-smith / feedback-fuzzer / template-scanner / packet-orchestrator | their craft doctrines unchanged | economy itself: the unorthodox move that costs the least |

## 5. Reading discipline

* **No decorative quotation.** A Sun Tzu line appears in a report or a
  plan note only when it is doing mechanical work — naming a rule the
  next action must obey. Otherwise it is noise, and noise fails audits.
* **Translation lineage.** The Giles 1910 translation is public domain
  and the phrasing this module's anchors follow; other translations
  shift wording (e.g. shih as "energy", "force", or "momentum") — the
  crosswalk's mechanism column, not the English phrasing, is the law.
* **Scholarship honesty.** *The Art of War*'s traditional attribution
  and dating are ancient-text questions; this module claims nothing
  about the historical Sun Wu. It uses the text the way A3 uses any
  source: read, attributed, re-implemented as decision logic.
* **The crosswalk is this bundle's contribution.** Sun Tzu wrote none
  of the mechanisms in the right-hand columns; the mapping — which war
  concept binds which enforced behavior — is original to this bundle
  and on record as such.

## 6. Sources

* Sun Tzu, *The Art of War*, Lionel Giles translation (1910; public
  domain), chapters I–XIII as cited per row above.
* The enforcement mechanisms cited in the crosswalk: this bundle's own
  charter (A4, A5, A8, A13, A14, A15), the spine's canon (R0, R6, R7;
  researcher-conduct §34.8), and the organ modules named in §4 — each
  carries its own sources file.
