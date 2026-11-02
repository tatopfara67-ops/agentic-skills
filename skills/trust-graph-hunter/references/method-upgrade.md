# The method upgrade — critiquing the Mitnick translation, shipping the executable trust audit

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

## 1. The critique — five mechanical weaknesses of the source method

| # | What the source shows (documented) | Why it is weak as a shipped method |
| - | ---------------------------------- | --------------------------------- |
| W1 | Trust edges per-vignette — each story names one exploited edge ("the help desk trusts a caller who knows the ticket format") | The edges never assemble into a GRAPH: which boundaries exist, what each trusts, and what the whole picture admits — every reader re-derives the map from scratch, per story |
| W2 | Forgery demonstrated, not differentialed — the con works in the story; the forged context is never tested AGAINST the absent context | "They believed me" conflates two questions: does the forged context beat NO context, and does it beat the LEGITIMATE context? Different weaknesses, different fixes — the vignette cannot ask |
| W3 | No completeness accounting — the stories cherry-pick the edges that worked | A trust audit needs a census discipline: every boundary, every trust class, checked or explicitly gapped; the story-form makes survivorship bias the genre |
| W4 | Third-party humans as instruments — the source material's demonstrations run against real employees, real help desks | In this organ's lane the instruments are operator-owned identities and self-owned accounts ONLY; the source practice is exactly what the ethics gate (M5) exists to forbid |
| W5 | No falsifier anywhere — a failed con is a better con, a successful one is genius | Nothing in the source can be wrong; translated to systems, that epistemology produces unfalsifiable audits — the anti-pattern this charter's ledger exists to kill |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Trust edges enumerated as a graph, with evidence | **M1** — the edge protocol |
| U2 | Forgery as a three-condition differential | **M2** — the context differential |
| U3 | Completeness gated per boundary class | **M3** — the census gate |
| U4 | Operator-owned identities only | **M4** — the identity law |
| U5 | Ethics as a mechanical gate | **M5** — the ethics gate |

## 3. The executable protocol — M1 through M5

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

## 4. Falsifiers — what would prove this method wrong

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

## 5. Worked micro-example (numbers consistent, incident fictional)

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
