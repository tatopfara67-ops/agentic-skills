# The executable method — M1–M9 for trust-graph-hunter

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
the Mitnick record — and, since v1.3.0, what was weak in the
shipped FORM of the Metcalf corpus) is preserved verbatim as the
§4–§5 appendix.

## 1. The executable protocol — M1 through M9

### 1a. The context tier (v1.1.0 — the Mitnick translation)

### M1 — the edge protocol (the graph, with evidence)

Per boundary (API gateway, webhook receiver, internal service,
admin panel), the trust edge is a record with an EVIDENCE command:

```
EDGE: boundary=<webhook-receiver> trusts=<HMAC signature + source
  IP> evidence=<header set observed + signature verification
  behavior on operator-owned test calls> class=<cryptographic|
  contextual|ambient> verification-strength=<graded>
```

Rules: every `trusts=` cell cites observed behavior (what the
boundary actually checks, demonstrated with operator-owned calls),
never documentation claims alone — docs are the story the boundary
tells about itself; the probe is the story it lives (W1).

### M2 — the context differential (three conditions, not one demo)

Per edge whose trust class is contextual/ambient:

1. **Conditions, n ≥ 5, interleaved**:
   * absent-context — the bare request (no forged context);
   * forged-context — the operator-owned M4 identity carrying the
     trusted markers (internal headers, Referer/Origin class,
     ticket-format lookalikes);
   * legitimate-context — the genuinely entitled operator identity
     where constructible, else the documented legit format on
     operator-owned flows.
2. **Observation**: acceptance class per condition (accepted /
   rejected / challenged).
3. **Rules**: forged beats absent (edge is real) is WEAK evidence;
   forged matches legitimate's acceptance (edge is fully forgeable)
   is the STRONG finding; forged-but-challenged is a working guard —
   recorded as a defense that holds, data, not disappointment (W2).

### M3 — the census gate (completeness or honest gaps)

```
CENSUS: boundaries=<n enumerated> classes=<per EDGE class table>
  checked=<n with M1 evidence> gapped=<n, named, reason>
  closure: "no gapped boundary may carry a claim"
```

The audit does not close while unnamed boundaries remain: every
boundary in the dossier's asset graph gets an EDGE record or an
explicit gap row (W3).

### M4 — the identity law (operator-owned only)

1. Every forged identity is built from operator-owned accounts,
   self-registered test identities, or synthetic markers the
   operator owns (canary doctrine).
2. NEVER: real employees' names, real customer identities, third
   parties' sessions — the source material's practice, forbidden
   here as a hard rule, not a preference (W4).
3. Each forged identity is a recorded ASSET with its ownership
   basis — an unowned identity in the log is an audit failure.

### M5 — the ethics gate (mechanical, before any run)

```
ETHICS: humans-involved=<none|operator-consenting> third-party-
  contact=<0 asserted, enforced by M4> deception-of-persons=
  <forbidden; systems-context forgery only> scope-basis=<program
  covers social-context simulation? default: NO — route out>
```

A run with any gate field failing does not start. The gate's
existence is the difference between auditing trust as a SYSTEM and
reheating the source material's practice with new victims (W4, W5
together: the falsifiable version of the discipline).

### 1b. The directory tier (v1.3.0 — the Metcalf extension)

### M6 — the eight-source directory-edge census

Per identity directory in scope (Active Directory or LDAP analog),
the census enumerates ALL EIGHT right sources — membership alone
is never the census (W6, W7):

```
DIR-CENSUS: domain=<D> sources-checked=<8-bit mask, one bit per
  source> principals-with-rows=<n> gapped=<sources not readable,
  named, reason> closure: "a principal's power is the UNION of the
  eight sources; a gapped source carries no claims about that
  source's edges"
```

Rules: every DIR-EDGE row cites the LDAP read that produced it
(base, filter, attributes — the row is reproducible); the census
is seeded with the interesting-principals RID table and the
AdminCount=1 filter; nesting is resolved to EFFECTIVE membership
with the chain recorded per row; SDProp-protected groups are
marked as re-asserted hourly. Read-only reads, authorized scope
only (hard rule 6).

### M7 — the inheritance-path pricing matrix

From the census graph, every technique row is priced for the
attacker positions the census shows EXIST (W6):

```
PATH: technique=<t> precondition=<position P + required key/right>
  contact=<none | DC-TGS | DC-replication | file-read>
  signal=<the detection row this path emits, event IDs named>
  price-rank=<cheapest position that qualifies>
```

Rules: price every row the census qualifies, not only the famous
ones — the SYSVOL read prices before the ticket forgery because
its position is cheaper; a path whose precondition is an OPERATOR
position is a validation failure (route to M8), not an attack
step; the matrix ships in the report as the client's own
valuation table (which edges their adversaries would buy first).
Pricing is data; execution on live estate is forbidden (hard rule
6/7).

### M8 — the tier-boundary validation gate

Defense stated as mechanical rows — every field pass/fail with
its evidence read, never prose advice (W8):

```
TIER: domain=<D>
  admin-logon-restriction | service-pw-length | krbtgt-rotation |
  replication-rights | dc-logon-groups | exchange/virtualization-
  equivalence                                    -> pass|fail + read
```

Rules: the KRBTGT rows carry the double-reset arithmetic — one
reset after a confirmed KRBTGT-hash exposure is an INCOMPLETE
recovery and is reported as a finding; maintenance mode (reset,
converge 12–24 h, reset again) and breach "double-tap" (two rapid
resets, every live ticket invalidated, service restarts expected)
are two different rows with different blast-radius statements.

### M9 — the paired detection row with its rot caveat

Every priced path ships WITH its detection signal in the same
record (W9):

```
DETECT: for=<PATH row id> signal=<event IDs / network pattern>
  filter=<the exact filter that makes it actionable> baseline=<the
  normal rate> rot=<the honest half-life statement>
```

Rules: indicators are versioned data and the rot field is
mandatory — an indicator stated as permanent is a false guarantee
(the 2016 mimikatz domain-field fix closed the original 2015
golden-ticket indicator while the method class persisted); the
filter row carries the false-positive reduction (the documented
0x17 + exclude-`$`-accounts + service-account filter chain turning
millions of events into hundreds).

## 2. Falsifiers — what would prove this method wrong

* Forged-context matches legitimate acceptance on an edge graded
  `cryptographic` → the grading was wrong: the signature is not
  actually enforced (evidence probe missed a bypass path); re-grade
  with the observation attached — the edge table self-corrects.
* The census shows 100% checked but a later engagement finds a new
  boundary class → the asset graph was incomplete: the gap is in
  Phase-1 cartography, recorded there, census re-opened for the
  class.
* An absent-context request is accepted (no forgery needed) → the
  edge does not exist: the trust model was wrong, and THAT is the
  finding (a boundary that trusts nothing is the biggest edge of
  all).
* Two analysts' EDGE records disagree on verification-strength →
  the evidence probe was under-specified: re-run the
  operator-owned calls with the disagreement as the hypothesis.
* A principal's observed power EXCEEDS the eight-source census's
  union → a ninth source exists (or one source was read shallowly):
  the census re-opens with the observed delta as the hypothesis —
  the union model is falsifiable, not doctrine.
* A directory path priced `contact=none` is later shown to emit a DC
  event → the pricing row was wrong: re-price with the signal
  attached, and the DETECT row re-pairs (M9 self-corrects).
* A tier row marked `pass` is defeated by the technique it names →
  the validation read was stale or shallower than the technique
  (e.g. password length ≥ 25 measured on a policy the service
  account does not receive): the row re-opens with the
  discrepancy named.
* An indicator in a DETECT row survives its stated rot date → the
  rot estimate was pessimistic: fine — rot is a floor on honesty,
  not a promise of decay.

## 3. Worked micro-example (numbers consistent, incident fictional)

Boundary set: 6 (asset-graph enumerated). M1 EDGE example:
webhook-receiver trusts `X-Internal-IP` header + source-IP
allowlist; evidence on operator-owned calls: source-IP alone
rejected 5/5, header alone accepted 0/5, header + spoofed-IP-class
connection from in-scope host accepted 3/5 → class contextual,
verification-strength weak. M2: absent-context 0/5 accepted;
forged (operator test identity + header) 3/5; legitimate 5/5 →
partial forgery finding, guard partially holds, recorded both ways.
M3: census 5/6 checked, 1 gapped (vendor SSO boundary, named).
M4: forged identity = operator-registered test account, ownership
basis logged. M5: ethics gate all-zero fields, run legal. Finding:
internal-header trust partially forgeable, P3, three conditions
cited, guard-holds half recorded as defense data.

Directory tier (fictional, numbers consistent): DIR-CENSUS sources
0xff (all eight readable), 214 principals with rows, 1 gap (share
delegations unreadable — no file-server scope, named). M6 rows
show: `svc-sql01` carries AdminCount=1 + SPN `MSSQLSvc/db01` +
GenericWrite on the `Domain Admins` group object (ACL-delegation
source) — a three-source principal the membership-only view
misses entirely. M7 prices the paths the census qualifies: from
`any-authenticated`, Kerberoast (`svc-sql01`, RC4 row) and the
SYSVOL GPP read both qualify — SYSVOL ranks first (no DC contact,
no signal); from `local-admin-on-any-host`, the credential
shuffle prices next (no DC contact at all). M8 rows:
`service-pw-length` FAIL (12-char service passwords, evidence:
pwdLastSet spread + policy read), `krbtgt-rotation` FAIL
(pwdLastSet == domain creation date, 2019 — the 2×-reset law
stated in the recommendation with both modes). M9 pairs the
Kerberoast row with its DETECT row (4769 + 0x17, baseline 10–20
TGS/user/day, rot: filter depends on RC4 staying exceptional) —
the finding ships as ONE record: the priced path, the failing
tier row, and the detection signal.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
Kevin Mitnick's art is real — The Art of Deception systematized
context-based trust exploitation — but this organ's source is
vignette fiction (the book's stories) plus social narrative, and
the systems translation is OURS: that means the translation itself
must be graded, not inherited. The floors: trust edges narrated
per-story, forgery demonstrated without differentials, no
completeness accounting for the graph, impersonation practiced on
third parties in the source material, and no falsifier anywhere.
This module ships the executable replacement: edge enumeration,
the context differential, a completeness gate, an
operator-owned-identity law, and an ethics gate with teeth.

The same charge grades the v1.3.0 extension. Sean Metcalf's corpus
is real and method-bearing — the eight-source rights model, the
priced technique knowledge, the tier guidance are his documented
record — but the corpus SHIPPED as per-post reference literature:
technique pages, a separate scanning post, separate detection
posts, mitigation prose. The floors below grade the corpus's
FORM, not its knowledge; the M6–M9 extension is the executable
replacement.

## 4. Appendix — the lineage critique — mechanical weaknesses of the source method (context, not steps)

### The Mitnick translation (W1–W5, v1.1.0)

| # | What the source shows (documented) | Why it is weak as a shipped method |
| - | ---------------------------------- | --------------------------------- |
| W1 | Trust edges per-vignette — each story names one exploited edge ("the help desk trusts a caller who knows the ticket format") | The edges never assemble into a GRAPH: which boundaries exist, what each trusts, and what the whole picture admits — every reader re-derives the map from scratch, per story |
| W2 | Forgery demonstrated, not differentialed — the con works in the story; the forged context is never tested AGAINST the absent context | "They believed me" conflates two questions: does the forged context beat NO context, and does it beat the LEGITIMATE context? Different weaknesses, different fixes — the vignette cannot ask |
| W3 | No completeness accounting — the stories cherry-pick the edges that worked | A trust audit needs a census discipline: every boundary, every trust class, checked or explicitly gapped; the story-form makes survivorship bias the genre |
| W4 | Third-party humans as instruments — the source material's demonstrations run against real employees, real help desks | In this organ's lane the instruments are operator-owned identities and self-owned accounts ONLY; the source practice is exactly what the ethics gate (M5) exists to forbid |
| W5 | No falsifier anywhere — a failed con is a better con, a successful one is genius | Nothing in the source can be wrong; translated to systems, that epistemology produces unfalsifiable audits — the anti-pattern this charter's ledger exists to kill |

### The Metcalf corpus form (W6–W9, v1.3.0)

| # | What the source shows (documented) | Why it is weak as a shipped method |
| - | ---------------------------------- | --------------------------------- |
| W6 | Techniques stated per-post — golden tickets in one post, silver in another, DCSync in a third, the privilege model in a separate scanning post — each excellent, none assembled | The eight-source rights model and the technique pages never meet in ONE priced path graph: which door is cheapest for which standing position is re-derived by every reader, per post — the graph exists implicitly and is never shipped |
| W7 | "Assume breach" stated as the framing, then technique enumeration starts | The attacker's starting position is the pricing variable, but no protocol step inventories the CURRENT position's granted rights before pricing doors from it — the census that would make the ladder mechanical is implied, never step one |
| W8 | Mitigations as prose per technique; tiered administration referenced through Microsoft's link, stated as narrative guidance | Defense ships as best-practice sentences, not as pass/fail rows with evidence reads — nothing in the form distinguishes a validated tier boundary from a recommended one, and the KRBTGT double-reset arithmetic lives inside prose instead of a gate |
| W9 | Detection shipped in separate posts, sometimes years later (golden-ticket detection 2015; no-FP Kerberoast detection 2017), with the 2016 indicator-loss honestly documented as an update note | The attack row and its detection row are different artifacts in different years — an organ-grade record needs them paired at birth, with the indicator's rot stated as a field, because the on-record mimikatz update proves indicators close while method classes persist |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Trust edges enumerated as a graph, with evidence | **M1** — the edge protocol |
| U2 | Forgery as a three-condition differential | **M2** — the context differential |
| U3 | Completeness gated per boundary class | **M3** — the census gate |
| U4 | Operator-owned identities only | **M4** — the identity law |
| U5 | Ethics as a mechanical gate | **M5** — the ethics gate |
| U6 | The eight rights sources assembled into one census protocol, position inventoried first | **M6** — the eight-source directory-edge census |
| U7 | Techniques priced into one path graph — position → technique → cost → signal | **M7** — the inheritance-path pricing matrix |
| U8 | Tier boundaries and the KRBTGT double-reset law as mechanical pass/fail rows | **M8** — the tier-boundary validation gate |
| U9 | Attack and detection as one record, indicator rot stated as a field | **M9** — the paired detection row with its rot caveat |
