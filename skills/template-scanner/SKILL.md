---
name: template-scanner
version: 1.1.0
type: ai-skill
architecture: package
description: Craft-lineage organ distilled from the ProjectDiscovery team (Sandeep Singh, Rishiraj Sharma, Marco Rivoli, Nizamul Rana — creators of subfinder and nuclei) — detection knowledge as declarative, versioned templates. A template is a pre-registered experiment: matchers (status/word/regex/DSL conditions) written before the run; severity and metadata baked in; engine and template packs evolve separately so the community compounds; multi-protocol reach (HTTP, raw TCP, DNS) keeps one language across surfaces; and a whole Since v1.1.0 the organ carries the executable method layer (A16) — a mechanical critique of the template-scanning practice's floors (matchers run as received without review, severity baked into YAML for a generic universe, engine×pack drift untracked, noise classes narrated as findings, hits reported without the bytes the matcher saw) shipped as protocol M1–M5: the pre-run review gate that converts templates into pre-registered experiments, the severity re-rating ladder with both columns in every output, the RUN-PIN version matrix, the noise filter table with visible counts, and the hit record with evidence blocks and confidence-class version pins. Use when turning a repeatable check into a reusable artifact, when running scan campaigns that must be reproducible, when aligning detection packs with VRT classes, or when sharing a detection with others ("make this a template", "rerun last week's scan", "template pack", "same check everywhere", "reproducible campaign").
category: security/craft-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: ProjectDiscovery (founded 2019 by Sandeep Singh, Rishiraj Sharma, Marco Rivoli, Nizamul Rana) — subfinder, nuclei, naabu; template-driven scanning
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# template-scanner v1.1.0 — The ProjectDiscovery Lineage

## 0. What This Skill Is — and Is Not

* **Is**: the organ for *detection knowledge as data*: checks written
  as declarative templates (condition before run, metadata baked in,
  versioned and citable), campaigns expressed as template sets, and
  reproducibility measured by whether the same template set on the
  same surface yields the same records.
* **Is not**: a scanner engine. The arsenal's tools are the engine;
  this organ governs the *template discipline* layered on them —
  the declarative half the engine deliberately leaves to data.

## 1. The Lineage (attribution)

ProjectDiscovery was founded in 2019 (per the Bishop Fox account) by
Sandeep Singh, Rishiraj Sharma, Marco Rivoli, and Nizamul Rana,
growing from collaboration on subfinder into the nuclei template
ecosystem — thousands of community templates, one detection
language. Sources: references/sources.md — the verification record

## 2. The Six Laws of Template Craft

1. **A template is a pre-registered experiment.** The matcher
   conditions (status, word, regex, DSL) exist BEFORE the run —
   exactly the spine's EXPERIMENT discipline. Post-hoc "it matched
   when I looked at it" is not a template; it is a story.
2. **Detection knowledge is data, versioned.** Templates live in a
   repo, evolve by PR, and are cited by version/hash. Modern form:
   every reusable check in this pipeline is a data file with an id;
   the ledger cites the template id it ran. Ad-hoc inline checks are
   single-use by construction — and treated as such.
3. **Engine and knowledge evolve separately.** nuclei's engine is
   stable while template packs move daily. Modern form: arsenal
   tools change rarely; the template packs (paths, matchers, VRT
   class) change per engagement — and never silently.
4. **One language across protocols.** The same template grammar
   covers HTTP, raw TCP, DNS — so a finding class speaks one
   language regardless of surface. Modern form: template fields are
   protocol-neutral (target, request-shape, matcher, class); the VRT
   class is the shared vocabulary (see vrt_classify).
5. **Severity is metadata with an argument.** Templates carry
   severity, but the arsenal's law stands: severity is three layers
   (CVSS recomputed, VRT baseline, program-context call) — the
   template states the taxonomy layer; the report argues all three.
6. **Campaigns cite their template set.** A scan campaign is only
   reproducible if the template set is named: which ids, which
   version. "We ran our checks" is not a campaign record.

## 2.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published template practice where it was mechanically weak —
`nuclei -t ~/nuclei-templates` as the workflow (the authors of the pack
pre-registered your hypotheses against a target they never saw),
`severity: critical` riding verbatim into every report, matcher DSL drift
across unrecorded version pairs, self-signed-cert classes filling finding
rows, hits without evidence — and ships the executable replacement:
**M1** the review gate (no-falsifier matchers REJECTED; survivors convert
to T-EXP records), **M2** the severity re-rating ladder (template label →
target-relative class; both columns in the output; label-only reports
refused), **M3** the RUN-PIN matrix (engine + pack hash cited per hit;
changed pin = new run, never merged), **M4** the noise table (TLS/banner
/header classes filtered BEFORE the draft; filter counts recorded), **M5**
the hit record (request bytes + response class + matcher summary + version
pin confidence class + next route).

## 3. Procedure — Numbered Actions

1. When a check is worth running twice, template it: write the data
   file — `id`, `class` (VRT id from `vrt_classify`), `target-shape`,
   `request`, `matcher` (the exact conditions), `severity-baseline`,
   `references` (the records/advisories that motivated it).
2. Register the template (ledger EXPERIMENT; the file's hash is the
   version).
3. Run it through the engine's tool for its protocol (`http_probe`
   for HTTP-shaped, `content_discover` for sweeps) — the template
   supplies the pre-registered matcher; the tool supplies the
   record.
4. Matcher fires ⇒ the triad still applies: template hits are
   candidates; baseline/control legs convert them to findings
   (module-smith handles the card).
5. Campaign = template set + surface set + run date; the campaign
   record cites all three. Re-runs cite the same set (or diff it,
   loudly).
6. Template hygiene: false-positive rate observed on controls is
   recorded on the template; templates that fire on controls get
   tightened or retired — the pack earns trust per template.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Classifying a new template | `vrt_classify` (the class field) |
| Running HTTP-shaped templates | `http_probe`, `content_discover` |
| Sweeping surfaces for a template set | pipeline-smith stages 4-5 |
| Confirming template hits | module-smith's triad |
| Campaign records | `ledger_append` (EXPERIMENT/FACT with template ids) |
| Community-style sharing | template files are the shareable artifact (data, not code) |

## 5. Hard Rules

1. No template without a matcher written before the run.
2. No campaign record without its template set cited.
3. Inline one-off checks are allowed — but they never graduate to
   "we always check this" status as folklore; they graduate by
   becoming files.
4. A template's severity-baseline never overrides the report's
   three-layer severity discipline (A10).
5. Template packs change by versioned diff, never by silent edit.

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Designing templates and packs | references/mindset.md |
| Running template campaigns | references/playbook.md |
| Checking lineage claims and reading list | references/sources.md |
| Grading the published practice, auditing matchers, re-rating severity | references/method-upgrade.md |
