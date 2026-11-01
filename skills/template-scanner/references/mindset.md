# mindset.md — the ProjectDiscovery decision logic, translated

## 1. The mind, as observed in the sources

* **Founded on a shared problem, not a product.** The Bishop Fox
  account: four people (Sandeep Singh, Rishiraj Sharma, Marco Rivoli,
  Nizamul Rana) collaborating on subfinder, discovering common
  interests in security automation, "decided to work on all the ideas
  we had, including Nuclei" — the company grew out of open-source
  collaboration, and the tools stayed open.
* **Templates as the unit of detection.** nuclei's grammar: a YAML
  file declares id, info (severity, tags, references), requests with
  matchers — status, word, regex, DSL conditions. The engine
  evaluates; it does not decide. The intelligence lives in data that
  anyone can read, diff, and improve.
* **The community compounds on the language.** Practitioners at scale
  (Bishop Fox's account again) describe templates as "a single
  source of knowledge" and a shared vocabulary: "we can build each
  other's understanding of vulnerabilities really quickly because we
  have the ability to communicate in the same language."
* **Adaptation speed is the payoff.** The Log4j story, as told by
  operators: basic header templates first, obfuscated-payload
  templates next, then non-HTTP protocols — "how fast we were able
  to apply updates as we discovered different avenues of attack…
  made possible by the flexibility of templates."
* **Multi-protocol on one grammar.** Raw TCP templates (craft bytes,
  parse responses) put undocumented services under the same language
  as HTTP; credential re-use against SFTP-class endpoints ships as
  templates too.
* **Speed with explicitness.** The tooling is built for millions of
  requests — but every request is a template's declared intent. Fast
  AND pre-registered is the whole trick; most ecosystems manage one.

## 2. The translation table (nuclei → arsenal)

| nuclei concept | Organ behavior |
| --- | --- |
| YAML template + matchers | template data file: id/class/target-shape/request/matcher, hash-versioned |
| template repo + PRs | packs evolve by versioned diff; ledger cites template ids |
| engine ↔ templates separation | arsenal tools (stable) ↔ template packs (moving) |
| tags/severity metadata | VRT class + severity-baseline — crosswalked via `vrt_classify` |
| multi-protocol templates | protocol-neutral template fields (request-shape + matcher) |
| workflows (template chains) | pipeline-smith stages composed of template sets |
| community template packs | shareable data files — knowledge as data, per the gf lesson too |

## 3. The template file (this organ's unit of thought)

```
template:
  id: unauth-debug-route
  class: server_security_misconfiguration.exposed_portal.non_admin_portal  # vrt_classify
  target-shape: <surface class + auth precondition>
  request: GET {base}/api/v0/debug            # the probe shape
  matcher:
    status: 200
    body-regex: ["diagnostic", "debug-console"]   # condition BEFORE run
    negative: [401 on {base}/api/v2/admin/metrics]  # the built-in control leg
  severity-baseline: P3 (VRT baseline — report still argues three layers)
  references: [R-NNN, advisory URL]
  version: sha256:<12 hex of this file>
```

The `negative` field is this lineage meeting ours: the matcher
carries its own control leg, because a template that cannot say what
would falsify it is a fortune cookie.

## 4. Failure modes this organ exists to kill

* The brilliant check that lives inside one probe call and is
  re-typed, slightly differently, every engagement — unversioned,
  unreviewable, unshareable.
* Post-hoc matchers: "we looked at the responses and noticed…" —
  which is analysis, not detection, and does not survive an audit.
* Campaign amnesia: re-running "the usual checks" whose membership
  nobody can enumerate.
* Template sprawl: packs that grow without false-positive rates
  recorded on controls — trust erodes silently until the pack is
  noise.
* Severity copy-paste: a template's P-rating pasted into a report as
  if it were the program-context call (A10 forbids; the template
  states the taxonomy layer only).

## 5. What the engine already enforces (do not re-implement)

* Pre-registration discipline (EXPERIMENT records) — the template's
  matcher IS a pre-registered partition.
* The auditor's classification gates (cvss recomputed, vrt validated)
  — severity-baseline from a template never bypasses them.
* Calibration (`content_discover` controls) — the matcher's negative
  leg, mechanically.
