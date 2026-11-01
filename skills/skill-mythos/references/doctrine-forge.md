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
  quota discipline paragraph.

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
  quota is the one unforgivable failure (A7/A8).

## 4. Extending the grammar

The keyword tables live in `arsenal/tools/mythos.py`
(`_INTENT_GRAMMAR`, `_SEVERITY_RE`, `_QUOTA_RE`) and the persona
registry in `LEGEND_REGISTRY`. To add an intent or a legend, extend
those tables plus the matching `_forge_*` builder — and add the
paired test cases in `arsenal/tests/test_doctrine_forge.py`. Keep
the function pure (no clocks, no randomness, no environment reads
beyond the static tables): determinism is the contract that makes
the forged order auditable.

## 5. Why this exists (the operator's brief, on record)

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
