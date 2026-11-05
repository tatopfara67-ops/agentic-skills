# The executable method — M1–M6 for threshold-hunter

The A16 layer of threshold-hunter (the 36th method-upgrade module
on record). The house authoring contract applies: every method is
stated as name, inputs and environment, execution logic, and
validation gates — the form the operator brief demands (absolute
technical output, no biography). The critique first, then the
replacement protocol. Where the lineage's art already ships a
gate-ready statement, it is cited as such; where the house had to
build what the corpus left implicit, the upgrade says so.

## 1. The critique — six weaknesses in the published Ollam art

* **W1 — the execution layer has no remote-executable protocol.**
  The corpus is overwhelmingly hands-on physical craft: picks,
  shims, under-door tools, freeze spray through a door crack, key
  casting. An AI agent cannot execute any of it, and a method
  module that ships unexecutable steps as if they were runtime is
  theater. The DECISION LOGIC underneath (what to try, in what
  order, why, and what the observation means) is transferable and
  must be separated from the hands that carry it.
* **W2 — the flagship methodology drifts without version pins.**
  "The Search for the Perfect Door" (ShakaCon 2016) grows a
  padlock section by BruCON 0x08 (2016), morphs into "How Threats
  Are Slipping In the Back Door" (SANS 2017), and lands as "I'll
  Let Myself In" (BSides Orlando 2017, then Wild West Hackin'
  Fest 2017 as "the best version ever"). The content improves;
  the version discipline is absent — no version numbers, no
  changelog, no statement of which iteration supersedes which.
  (Contrast the Haddix deck chain, which versioned its drift and
  thereby made it auditable — the exact lesson this house's Q6
  codified as the DRIFT audit.)
* **W3 — the taxonomy never becomes a selection rule.** "The Four
  Types of Locks" (SecTor 2010) names a classification, and
  "Distinguishing Picks" (ekoparty 2010, DerbyCon 2011) even
  proposes consistent tool naming — but neither is carried into a
  rule that SAYS when each attack class is chosen against a given
  target. The selection logic exists in practice (it is the
  checklist) but is never stated as a scored or ordered rule.
* **W4 — the 100% entry claim is interview speech, not engagement
  data.** "We've never not gotten in" (Darknet Diaries 134) is an
  unverifiable aggregate over undocumented engagements. As a fact
  it is unshippable; as a REFRAMING — stop measuring entry, start
  measuring detection and response — it is the most valuable
  sentence in the corpus. The method keeps the reframing and
  drops the claim (quarantined in sources.md).
* **W5 — the cover-identity doctrine is human-only and legally
  sensitive.** The fire-code cover ("Shit's on Fire, Yo") works
  because a human acquired real NFPA certification and can speak
  under questioning. An AI agent cannot hold certifications, and
  a runtime that coaches pretexting persons violates this house's
  refusal set. The TRANSFERABLE residue is narrower and clean:
  know the adjacent legitimate domain well enough to recognize
  its traffic, its tooling, and its challenge conventions —
  perception, not impersonation.
* **W6 — the books are paywalled under a free chain.** Both
  Syngress titles are commercial. The method must stand on the
  free chain alone (talk records and abstracts, the Darknet
  Diaries transcript, Matt Blaze's public papers, vendor format
  documentation, the OSDP standard record), with the books cited
  at synopsis level and BOUNDED — the same bound the house
  applied to paywalled corpus material before (the Kaminsky
  session's discipline).

## 2. The executable protocol — M1 through M6

### M1 — the entry-ladder enumeration

* **Inputs**: the boundary inventory (from procedure step 1);
  the engagement's ROE and rate budget; the scope_check verdict
  for each in-scope boundary.
* **Environment**: the operator's request tooling (http_probe,
  the arsenal's read-only probes); the engagement ledger
  (R-NNN rows); no physical tooling, ever.
* **Execution logic**:
  1. For each boundary, instantiate the ladder as ordered rungs,
     each with a cost class and a technique template:
     R0 open/unguarded state (cost: zero — the endpoint or
     surface that simply answers; the unlocked handle);
     R1 installation and configuration error (cost: low —
     directory listings, backup artifacts, debug flags,
     integrator shortcuts, the backwards-hinge class);
     R2 factory default and keyed-alike credential (cost: low —
     public default keys, demo tokens, shared SDK secrets, the
     "available online and easy to acquire" class);
     R3 credential-format assumption failure (cost: medium —
     run M4, then replay or re-encode what is formatted but not
     authenticated);
     R4 protocol logic attack (cost: medium-high — the boundary's
     own decision logic, including M3's OR-compositions);
     R5 cryptographic or design-level analysis (cost: high —
     last, and only on record as to why it is needed).
  2. Execute rungs in order. One rung at a time. Each rung's
     verdict goes to the ledger: technique, cost class, verdict
     (worked / failed / not-applicable), evidence artifact (the
     R-NNN row or the stored response), and — if skipped — the
     reason.
  3. If a cheap rung succeeds, RECORD IT AND KEEP THE CHEAP
     FINDING AS THE HEADLINE. The lineage's preference is
     documented: even with a workable technique in hand, keep
     looking for the simpler one that "lets just anyone walk
     right in".
* **Validation gates**:
  * Every rung has a ledger row (a missing rung is a protocol
    failure, not a style choice).
  * No rung executes while a cheaper rung is unexecuted or
    unrecorded — the ladder is an ORDER, not a menu.
  * The headline finding of the boundary is the cheapest
    successful rung; a more expensive success can never displace
    it in the report.
  * Falsifier: a boundary where R5 is genuinely the first
    successful rung (a well-installed, well-configured,
    non-default, authenticated-boundary system) — the ladder
    must still show R0-R4's failed verdicts on record, which is
    itself the resist measurement.

### M2 — the egress reversal census

* **Inputs**: the boundary inventory; the target's documented or
  discovered route list; the ROE.
* **Environment**: read-only request tooling; the ledger.
* **Execution logic**:
  1. Enumerate the exit-only surfaces — the system's "opens from
     the inside" class: pre-auth endpoints, health and status
     pages, unsubscribe and notification-suppression flows
     (single-use tokens, their token namespace), webhook
     receivers and callback handlers, error and recovery paths,
     password-reset egress, emergency and kill-switch surfaces
     (censused under M2 but NEVER actuated — hard rule 5).
  2. For each egress surface, record its TRUST MODEL: what
     stimulus it accepts, what it assumes about the stimulus
     source, what state change it performs. The REX sensor's
     model is the archetype: accepts ambiguous stimulus,
     assumes stimulus implies legitimate egress intent, performs
     unlock.
  3. Test external triggerability READ-ONLY: can an
     unauthenticated or out-of-band stimulus cause the surface
     to open a protected state or leak protected information?
     The compressed-air-through-the-crack class, translated:
     stimulus delivered through a side channel the surface's
     trust model does not price.
* **Validation gates**:
  * Every egress surface has a trust-model row (stimulus,
    assumption, effect).
  * Actuation tests against life-safety and emergency surfaces
    are REFUSED on record (refusal rows count as protocol
    compliance, not gaps).
  * A finding requires the full chain: stimulus → assumption
    violated → protected state opened — the REX sensor pattern
    restated as evidence.
  * Falsifier: a system whose egress surfaces all bind stimulus
    to authenticated, challenge-bound sources — recorded as the
    negative and the resist row.

### M3 — the OR-oracle privilege probe

* **Inputs**: a decision point observed to OR-compose
  authorization conditions (user-tier OR feature-flag OR
  partner-grant OR legacy-allowlist; any check whose pass
  condition is a disjunction); the operator's legitimate
  low-privilege credential; the rate budget.
* **Environment**: http_probe with per-request pacing; the
  ledger; scope_check verdicts for every probed endpoint.
* **Execution logic**:
  1. Decompose the decision point into its component conditions
     C1..Cn (from documentation, from observed behavior, from the
     M1/M2 evidence).
  2. For each subset of size one: issue a request holding the
     legitimate low-privilege baseline plus EXACTLY ONE component
     set true (or removed, for deny-list-shaped oracles). One
     component per request — isolation is the revealing move,
     because the oracle answers open/no-open for the OR, not for
     the components.
  3. Log each answer. Any single component that flips the oracle
     is a standing privilege grant leaking through the
     composition (the master-key pin found on the first probe).
  4. For multi-component grants, extend to pairs only if singles
     all fail, and only within the rate budget — the
     combinatorial escalation is priced like any deep rung.
  5. Attribute on every row: the attack class is Matt Blaze's
    rights-amplification (IEEE Security & Privacy, 2003), taught
    publicly by the lineage (HOPE 9) — the report cites the
    class origin, per doctrine A3.
* **Validation gates**:
  * Exactly one component varies per request (a probe varying
    two components at once is a protocol failure — it cannot be
    interpreted).
  * Every oracle answer is logged with its request's ledger
    reference.
  * A reconstructed privileged combination is a finding with the
    full evidence chain AND its fix-pair (the design-level fix:
    compose authorization with AND-logic over authenticated
    grants, or bind the disjunction to a challenge).
  * Falsifier: a decision point that AND-composes authenticated
    conditions — non-decomposable by construction; recorded as
    the negative, which is knowledge (the system is not
    master-keyed).

### M4 — the credential-format assumption audit

* **Inputs**: any credential, token, or identifier structure
  observed at the boundary (session tokens, badge-format
  identifiers, API keys, signed URLs, tenant-scoped IDs).
* **Environment**: offline analysis tooling (this organ's T1 for
  Wiegand-shaped structures); the ledger.
* **Execution logic**:
  1. Build the structure table: fields, widths, fixed markers
     (the facility-code class — tenant or issuer identifiers
     embedded in the credential), parity or checksum coverage,
     signature coverage, replay protection (nonce, timestamp,
     challenge binding).
  2. Price each assumption: what is merely FORMATTED (observable,
     cloneable, re-encodable — the Wiegand 26-bit row: 1 even
     parity bit over the leftmost 13 bits, 8-bit facility code,
     16-bit card number, 1 odd parity bit over the rightmost 13,
     no authentication, no challenge, replayable by design) versus
     what is AUTHENTICATED (signature-coverage table, what the
     signature actually covers, key rotation record) versus what
     is CHALLENGE-BOUND (session-scoped, non-replayable).
  3. State the standard's own upgrade row where one exists. The
     canonical pair, stated as the industry's public record:
     Wiegand's plaintext credential to OSDP Secure Channel
     (AES-128 encryption, device supervision, the access-control
     standard's replacement; required in U.S. federal
     applications per the SIA record).
  4. Cross-run with M1 R3: a formatted-not-authenticated
     credential found at a boundary is the R3 rung's evidence —
     replay and re-encode tests are protocol-logic attacks on
     the assumption, priced as medium cost.
* **Validation gates**:
  * Every observed credential structure has a completed table
    (fields, coverage, authenticity class).
  * Every cloneable finding carries the replay evidence chain
    AND the upgrade row naming the standard or vendor fix.
  * Parity/checksum arithmetic is verified by code (T1), never
    asserted by eye — the house's arithmetic rule.
  * Falsifier: a credential whose signature covers the full
    structure and whose replay protection is challenge-bound —
    the audit records the resist row.

### M5 — the detection-as-finding ledger

* **Inputs**: every request issued under M1-M4; the engagement's
  time window.
* **Environment**: the ledger; the report's measurement section.
* **Execution logic**:
  1. Every probe writes a detection row: timestamp, request
     class, response signature — classified into WAF block,
     rate-limit response, captcha or challenge, alert signal
     (observable IR activity), and no-response.
  2. The measurement frame is the lineage's "Three R's" stated
     at Secure360 2011 — Resist, Recognize, React — applied per
     boundary: how much did the boundary resist (the ladder's
     failed rungs), did anything recognize the operator (the
     challenge and alert classes), and how competent was the
     response (latency from first anomaly to first challenge,
     coverage of the egress surfaces).
  3. Close the ledger with the per-boundary summary: resist
     row, recognize row, react row — the same shape the lineage
     demands of any physical engagement ("the question is are we
     detected? Is there a response? How competent is that
     response?").
* **Validation gates**:
  * The engagement cannot close with an empty detection ledger
    on an in-scope boundary unless the boundary is declared
    detection-free on record (itself a finding).
  * "No response" is a finding with a severity row, not an
    absence.
  * Detection latency is computed from ledger timestamps
    (arithmetic by code, per the house rule).
  * Falsifier: a boundary whose detection responds to every
    probe class within its stated SLA — the resist measurement
    becomes the engagement's headline positive, on record.

### M6 — the fix-pair closure audit

* **Inputs**: the findings register; the vendor and standard
  layer's public remediation record.
* **Environment**: the report; the auditor's grounding gate.
* **Execution logic**:
  1. For every finding, write the fix row: the mitigation, its
     source (vendor advisory, standard requirement, integrator
     remediation class), and its position on the boundary's
     upgrade path.
  2. Canonical pairs this organ ships as the archetype rows:
     misinstalled strike to integrator remediation (the
     installation class); factory keyed-alike default to rekeying
     at procurement (the default class); Wiegand plaintext
     credential to OSDP Secure Channel AES-128 (the
     format class); OR-composed authorization to
     authenticated AND-composition (the logic class); missing
     rate limit to the proxy layer (the detection class).
  3. The report fails its own audit if any finding lacks its
     pair — the lineage's documented shape: "I also discuss
     solutions to every single one of these problems."
* **Validation gates**:
  * Every finding has a fix row with a named source.
  * Fix rows cite vendor or standard records, not invented
    best practice (the house's no-fabrication rule).
  * Falsifier: a finding with no known remediation on record —
    it ships as an open row with the remediation-gap stated,
    never as a silent missing pair.

## 3. Where the upgrades land

The A16 wiring: this module is born with the organ (the 36th of
the set the guard test locks); the spine's researcher-conduct
module rides along unchanged; the charter's tier-6 row carries
the organ; the registry's LINEAGES entry carries the distillation
that these M-rows implement. The A17 runtime (operator-os.md)
executes this protocol through its run-order S1-S6 — the two
layers cross-reference by design.

## 4. Falsifiers — what would prove this method wrong

* A boundary where the expensive rung is the only honest first
  move — the ladder's ordering would be wrong for that class.
  The protocol requires R0-R4 failure rows on record before R5,
  so the case is visible and adjudicable when it occurs.
* An OR-composition that does not leak under isolation —
  recorded as the non-decomposable negative; if a population of
  them accumulates, M3's claim weakens on record.
* An engagement whose physical-layer surfaces are all out of
  scope — the organ reports BOUNDED and stands down; its
  applicability is scoped, not assumed.
* A detection ledger that stays empty across a genuinely
  probed boundary — either the declaration "detection-free" is
  true (a finding) or the instrumentation is broken (a protocol
  failure to repair before close).
