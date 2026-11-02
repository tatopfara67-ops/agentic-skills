# doctrine-forge.md — the A13 prompt-escalation reference

Load when expanding an operator request, when the operator asks how
their terse instruction becomes a full order, or when extending the
intent grammar.

## 1. The Rule (charter A13)

Every operator instruction — however terse, informal, or informal-
Indonesian — is passed through the `doctrine_forge` MCP tool BEFORE
any organ acts. The agent executes the expanded order, never the bare
words; the original request rides along verbatim into the plan note
(so the audit trail always shows both what was asked and what was
ordered). Deterministic by A4: the same request forges the same
order, character for character.

Worked example (the operator's own phrasings):

* "tolong lanjutkan pekerjaan bug bounty yang tertunda"
  → intent `continue_pending` → the resume order: re-ground with
  `auth_status` + the newest PARK record, reconcile the dossier,
  resume at the parked phase with organ routing, re-price the
  remainder, gates unchanged.
* "tolong kerjakan dengan methode dan skill yang sudah tertanam,
  dapatkan minimal 3 bug high-medium"
  → intent `bug_quota`, severity goal `high-medium`, quota 3 → the
  full legend hunting order: Lamo's stealth recon → Tsai's chaining
  mindset → Kettle's protocol asymmetry → Rosen's IDOR discipline →
  Mitnick's trust audit → Draper's signal craft (when validators
  block) → Hotz's teardown (when artifacts are in scope) — plus the
  quota discipline + mission horizon paragraphs.

## 2. The Intent Grammar (as implemented)

Scored keyword match (distinct keyword hits; ties broken by list
order; no hits → `default`). Keywords cover English and the
operator's Indonesian phrasings:

| Intent | Triggers (examples) | Forged order's core |
| --- | --- | --- |
| `continue_pending` | lanjutkan, tertunda, continue, resume, pending | resume from the PARK record, never restart |
| `incident_response` | adversary, intrusion, serangan, breach, dibobol | Binary Brain engagement, freeze-first, handoff |
| `classify_report` | cvss, vrt, classify, laporan, report, audit, rating | classification + report gates until exit 0 |
| `bug_quota` | bug, temuan, finding, celah, dapatkan, minimal, hunt, get me, at least, target | the full legend mix + quota discipline |
| `surface_recon` | recon, enumerat, subdomain, mapping, peta, surface | passive-first mapping, one probe per candidate |
| `default` | anything else | full-discipline professional expansion |

Severity goals extract from the words `critical|high|medium|low`
(order preserved, deduplicated); quota from `minimal/minimum/at
least N` or `N bug(s)/temuan/finding`.

## 3. What the forged order always carries

* the **persona mix** — which legend lineages apply, with each
  figure's contribution stated in one line;
* the **phase plan** — the ordered steps of the engagement arc;
* the **tools** — the scope-gated instruments the order will use;
* the **gates** — the full quality-gate list, verbatim, because
  escalation NEVER relaxes discipline;
* the **quota discipline** (when a quota was detected): an effort
  budget, not a severity mandate — severity inflation to satisfy a
  quota is the one unforgivable failure (A7/A8);
* the **mission horizon** (same trigger): the quota is also a
  continuation mandate — before it is met, the engagement ends only
  by exhaustion proof or operator release (§5);
* the **execution doctrine** (v1.5): every forged order carries the
  OODA-hygiene loop + the D1–D7 summary — the behavior contract the
  selected organ runs under (references/autonomous-operation.md);
  lineage intuition proposes, the differential triad concludes.

## 4. Extending the grammar

The keyword tables live in `arsenal/tools/mythos.py`
(`_INTENT_GRAMMAR`, `_SEVERITY_RE`, `_QUOTA_RE`) and the persona
registry in `LEGEND_REGISTRY`. To add an intent or a legend, extend
those tables plus the matching `_forge_*` builder — and add the
paired test cases in `arsenal/tests/test_doctrine_forge.py`. Keep
the function pure (no clocks, no randomness, no environment reads
beyond the static tables): determinism is the contract that makes
the forged order auditable.

## 5. Mission horizon (the quota's other half)

Quota discipline guards one flank: inventing findings to fill a count
(the people-pleaser). The other flank is the most common long-horizon
agent failure — **surrendering before the count is filled**: a few
dead ends, then a polished "summary + recommendations" over an
unresolved TODO queue. The forged quota order therefore carries both
clauses, and they are symmetrical:

* never MORE severity than the evidence supports (A7/A8);
* never LESS WORK than the mission demands — stopping before the
  quota is met requires one of three legal stops: quota met,
  exhaustion proof (every inventoried surface closed or why-not'd,
  backlog empty, budget spent), or explicit operator release
  (mythos-bug-hunter researcher-conduct.md §34.8 — mission contract,
  dead-end redirect rule, reframe ban, stamina floor).

"kerjakan bug bounty sampai menemukan 1 celah keamanan high" is not
satisfied by a summary that recommends future work; it is satisfied
by 1 CONFIRMED high, an exhaustion proof, or the operator saying
stop. Context exhaustion is a pause, not a stop — the MISSION block
survives in engagement state and `continue_pending` resumes toward
the unmet quota.

## 6. The three registers (charter A14 — what every organ states)

Since v1.6.0 the charter binds every organ's expertise to the WWH
registers, and the forge's phase plans inherit the duty:

* **WHAT** — the class of thing, anatomized: precise definitions and
  the surface inventory, not vibes. An organ that cannot say what the
  thing IS cannot claim to hunt it.
* **WHY** — the root cause, mechanically: the reason the bug lives
  where it lives (why the parser disagrees, why the merge trusts the
  key, why the cache misclassifies). The WHY is what transfers to a
  target the catalog never listed — it is the difference between
  replaying a technique and reasoning with a cause.
* **HOW** — the procedure, numbered, with oracles and falsifiers:
  which request answers which question, what result falsifies the
  hypothesis, and in what order the steps run. A step without its
  oracle is a hope, not a step.

The forge checks the registers by construction: a phase-plan step that
cannot name its observable, its cause-hypothesis, and its order
position is rewritten until it can. New organs are born
register-complete (mobile-hunter, cache-playbook, prototype-playbook
carry WHAT/WHY/HOW sections from v1.0.0); existing organs adopt the
registers on their next content revision, and the tier-3 attack organs
(injection-lab, ssrf-playbook, xss-playbook) already demonstrate the
pattern.

## 7. War logic on every order (charter A15)

Since v1.6.0 every forged order's prompt tail carries the WAR LOGIC
block (the `war_logic` field) — the seven rules W1–W7 distilled from
the Art of War crosswalk (references/war-doctrine.md): spies before
armies, win without fighting, avoid strength and strike weakness,
cheng paired with ch'i, shih stored in the ledger, the sovereign sets
intent while the general commands, and no nation profits from a
prolonged war. The forged campaign is a campaign: it names its fronts
(the surfaces), its sequencing (the phases), its supply lines (R7
budgets), and its unorthodox bet (the plan note's ch'i line). A
request that would produce a patrol — one technique, one surface, no
bet — is forged into a campaign instead; that is what A13 plus A15
buy together.

## 8. Why this exists (the operator's brief, on record)

The operator asked that even a sleepy one-line instruction —
"please continue the pending bug bounty work" — be enough for the
agent to operate like it had received the full professional prompt:
"When testing the target without a scanner, adopt Orange Tsai's
mindset to find chainable small gaps; combine James Kettle's
methodology for manual HTTP header/protocol manipulation; apply
Adrian Lamo's stealth principle — only passively-exposed internal
architecture misconfigurations." The forge is that request, made
mechanical, versioned, and test-covered — and it can never be used
to smuggle discipline OUT, only doctrine IN.
