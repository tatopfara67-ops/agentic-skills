# The executable method — M1–M6 for interior-cartographer

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
Forshaw's published interior work) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M6

### M1 — the interior census (the map before the move)

The census header is written before any probing:

```
CENSUS: system-class=<OS class in scope>
  principal-assumed=<the unprivileged foothold, e.g. low-priv local user>
  boundary: api-surface-mapper=<why this is not an external-API spec diff>
  boundary: surface-cartographer=<why this is not the network-visible estate>
  classes: rpc-endpoints, alpc-ports, com-activation, services+paths,
           registry-writable, objmgr-namespace, tasks, dll-search-order
  instrument: <name+version of the enumeration instrument per class>
  floor: |classes| < 3 -> park as product review (recorded)
```

Rules: every row pinned by name or interface id AND by the instrument
that enumerated it (W1's floor — the census is a procedure, not a
tool's output); the boundary rows are mandatory (the class claim is
argued, not assumed); the instrument's version is part of the row (W3's
floor — the denominator must not drift silently).

### M2 — the access-model audit (the seam table)

For each census row, record the guard (security descriptor, token
requirement, privilege requirement) and the vendor-documented boundary
the crossing would traverse. Price the per-object-type access space with
the computed budget (table in references/interior-method.md): a 32-bit
access mask over 2^16 per-type specific rights plus 10 named standard
and generic bits — the census's arithmetic, recomputed per engagement,
never recalled. Then file the seam table: every row whose trust
transition has no boundary row in the vendor's taxonomy is a seam
candidate. The seam table — not any single bug — is the organ's primary
evidence artifact (W2's floor, closed: the taxonomy is a shipped
crosswalk, not per-issue prose).

### M3 — the primitive inventory (the availability matrix)

The reusable local primitives, each with precondition, observable, and
ledger row. The documented 2015 availability example, held as the
template row: four link types, three creatable by a low-privileged user
(object-manager symbolic links, registry key symbolic links, NTFS mount
points), one administrator-only (NTFS symbolic links). Squatting,
impersonation quirks, reflection and marshaling confusions join the
matrix as the census discovers them. A primitive whose precondition
fails under the census principal is falsified for this engagement and
recorded as such (W4's floor, closed: one matrix, not scattered posts).

### M4 — the composition hunt (one variable per step)

Chain primitives across ONE seam candidate at a time: one primitive per
step, one variable per step, n_runs ≥ 2 on load-bearing cells (A8). The
demonstration proves the seam exists — the chain's reach is evidence,
while impact claims run the house report gates like any other finding.
A step that changes two things is two steps, each with its own control.

### M5 — the boundary report (the taxonomy crosswalk)

```
BOUNDARY-REPORT: chain=<step list, one primitive each>
  taxonomy-row=<the vendor boundary crossed, cited by section>
  OR seam=<the uncovered trust transition, named>
  disposition=<vendor verdict if declined — quoted, dated>
  residual-risk-row=<stopgap status, re-test trigger, date>
```

The report maps the chain onto the vendor's own boundary list; where the
taxonomy has no row, the seam is named and the finding is argued as the
taxonomy's gap. A declined seam is filed as residual risk with the
disposition quoted and the date (W5's floor, closed: the register keeps
what the threads lose).

### M6 — the census regression (measurement, not anecdote)

After the fix, re-run the census: the diff — rows added, rows removed,
guards changed — is the verification artifact. A fix that changes no
census row while the chain still runs is a mitigation: labeled a
stopgap, its structural fix named, the residual-risk row dated (the
MS15-090 backport is the lineage's own type case — a mitigation shipped
as far back as Vista in response to the primitive line).

## 2. Falsifiers — what would prove this method wrong

* The census yields zero seam candidates (every row's trust transition
  is a documented boundary) → the interior-hypothesis is falsified for
  this target: record it, park the organ, route to the per-product
  organs — a uniform seam table is a negative result worth its ledger
  row.
* A primitive's precondition fails under the census principal → the
  composition is falsified before it starts; the primitive's row keeps
  the failure, and the matrix shrinks on record.
* A composition cell flips between runs (n=2) → the step was flaky, not
  the seam: re-run with n ≥ 3 and record the instability as the cell's
  own data.
* The vendor's taxonomy, read carefully, DOES cover the seam → the
  "uncovered" claim is withdrawn; severity re-runs on the documented
  boundary row — the correction is filed, not buried.
* The fix changes no census row and the chain still runs → the
  mitigation is absent, not the seam: escalate per the report gates with
  the census diff as the measured denominator.

## 3. Worked micro-example (numbers consistent, incident fictional)

An internal estate, one Windows-class build family, census principal =
standard user with logon-session. M1 census (instrument version pinned
per class): 84 RPC endpoints (11 network-exposed, 73 ALPC-only), 210
COM activation objects, 23 registry keys writable by the principal and
touched by privileged services, 17 privileged binaries with writable
search-order directories; boundary rows filed against api-surface-mapper
(no external spec assumed — the enumeration is the ground truth) and
surface-cartographer (the foothold predates the hunt; the estate map
already exists). M2: guards recorded per row; computed access budget
cited per object type; seam table yields 6 candidates — including one
service whose activation guard checks only the caller's group, not the
impersonation level, an uncovered trust transition. M3: availability
matrix rows — mount points and registry key links creatable by the
principal (the documented template row), object-directory squatting
available in one namespace subtree, one reflection primitive requiring
an authentication the principal lacks (falsified, recorded). M4: a
3-primitive chain across the service seam — squat, link, marshal — one
variable per step, n_runs = 2 on the load-bearing cells (ledger R-4xx).
M5: boundary report files the crossed taxonomy row for 3 of the 6
candidates and names the seam for the service row; the vendor declines
the seam — disposition quoted, residual-risk row dated with a re-test
trigger. M6: post-fix census diff shows the service's guard row changed
(token requirement added), chain dead at step 3, remaining 5 candidates
unchanged — one fix, one stopgap labeled, the register keeps the
declined seam. Fix window: reported → fixed 81 of the 90 disclosure
days (90% of budget consumed — computed, on record).

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise
delivered.** Forshaw's art is real — the first-ever Microsoft bounty
payout ($100,000 mitigation bypass, 2013), the #1 MSRC researcher
listing, a Project Zero corpus that repeatedly moved Microsoft to
backport mitigations (MS15-090, as far as Windows Vista), and an
instrument line (the object-manager cmdlets, the RPC tooling) that the
field itself curates as reference material — but the published form has
floors: the census lives inside the tools, the boundary argument is
re-derived in prose per issue, and the deepest knowledge ships as books
for humans. This module extracts what is replayable by an agent and
ships the replacement: an interior census with boundary rows, an
access-model audit with a computed budget and a seam table, a primitive
inventory with an availability matrix, a one-variable composition hunt,
a taxonomy-mapped boundary report with declined-seam residual risk, and
a census regression. An agent without Forshaw's decade of Windows
internals runs this at his precision.

## 4. Appendix — the lineage critique — six mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | The census embodied in tools, not procedures — the module's own pages list 65 exported commands at v1.1.14 and 75 at v1.1.33, but no published decision table orders WHICH enumeration answers WHICH question for a given target class | An agent cannot re-derive the enumeration order; it can only admire the instrument. The workshop repository teaches the domain but does not number the procedure |
| W2 | The boundary argument made per-issue in prose — "it didn't meet the bar for a security bulletin" (AppContainer firewall, 2021); "not an issue which can be exploited remotely, nor is it a privilege escalation" (lockdown policy, 2018) | The vendor's boundary taxonomy — the terrain the whole argument fights on — is never shipped as a reusable crosswalk from chain → taxonomy row → severity; every engagement re-derives it from issue threads |
| W3 | The tool surface's growth is unmeasured public record — the gallery page and the module manifest disagree at the same era (75 listed commands on the v1.1.33 page against 118 declared exports in the v1.1.17 manifest — both computed on record) | No authoritative "what became enumerable when" ledger exists; census reproducibility rests on version pinning the operator must do by hand, and a version drift silently changes the census's denominator |
| W4 | Composition knowledge scattered — the primitive taxonomy in the 2015 symbolic-link post, the chaining in the 2018 file-write series, the reflection record in the 2015 issue, the UMCI bypasses in the 2017-2018 talks and the Device Guard repository | No single primitive × seam matrix ships with the corpus; compositions are re-invented per engagement, and the field's own curations (third-party awesome-lists) partially substitute for the missing matrix |
| W5 | Declined findings living in threads — the WontFix disposition on the AppContainer firewall configuration issue is published inside the blog post, not tracked anywhere with a date and a re-test trigger | The seam landscape silently regresses: a seam the vendor declined is folklore until an engagement re-encounters it; no residual-risk register exists in the published art |
| W6 | The books teach humans, not agents — Attacking Network Protocols (336 pp, 2017) and Windows Security Internals (2024) encode the domain as chapters a person reads, with worked examples for a human hand | The lineage's deepest layer — the access-check process, token construction, security-descriptor manipulation — is the least executable: an agent cannot replay a chapter as a decision procedure without the steps extracted and numbered |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The enumeration as a numbered census procedure with boundary rows | **M1** — the interior census |
| U2 | The vendor's boundary taxonomy as a reusable crosswalk | **M2** — the access-model audit and seam table |
| U3 | The primitives as one availability matrix | **M3** — the primitive inventory |
| U4 | The compositions under a one-variable discipline | **M4** — the composition hunt |
| U5 | Declined seams as a dated residual-risk register | **M5** — the boundary report |
| U6 | The post-fix state as a measured census diff | **M6** — the census regression |
