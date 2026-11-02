# mxss-and-clobber.md — the Heiderich lineage layer for xss-playbook (v2)

Load when a sink context is INSIDE a mutation-capable host (innerHTML,
insertAdjacentHTML, document.write), when a sanitizer output still
executes, or when a "safe" framework API turns out not to be.

## 1. Why Context Analysis Alone Is Not Enough

The v1 organ derives sink context (HTML body / attribute / JS string /
URL) and builds payload grammar per context. The Heiderich layer adds the
uncomfortable fact: **context is not stable**. Between the moment a
payload is sanitized (or deemed safe by a framework API) and the moment a
browser re-parses it, the serialization can MUTATE — the re-read parses
different bytes than were written. The mutation, not the payload, is the
vulnerability. Field rule: after ANY DOM mutation of attacker-relevant
data, re-derive the context before refining the payload further.

## 2. The mXSS Class Catalog

Three classes cover the published mutation vectors (the ACM WPES paper
"mXSS attacks" and the follow-up "Attacking well-secured Web-Applications
by using innerHTML" — Cure53):

| Class | Shape | Canonical hosts |
| --- | --- | --- |
| Re-serialization mutation | content read back ≠ bytes written: `noscript`, `style`, `title` bodies escape their inert context on innerHTML round-trip; attribute quoting/order normalizes | any `element.innerHTML = x; read(element.innerHTML)` pattern |
| Namespace confusion | markup that re-parses into an executing namespace: SVG `<foreignObject>`, MathML, mXSS inside `<template>` | frameworks rendering "HTML fragments" |
| Parsing-context switch | the same string parsed as markup in one insertion point and inert text in another: comments in attributes, `--!>` comment closing | template engines, rich-text editors |

For each class: ONE minimal reproduction differential (mutation-free
control vs mutated treatment), the mutated bytes recorded verbatim in the
artifact, the marker proof only after the mutation is on record.

## 3. DOM Clobbering — the Pseudo-Source

Before a sink executes anything, the markup itself can corrupt the
program: `id`/`name` attributes on injected markup collide with
`window.*` and `document.*` lookups. A clobbered validator (`if
(window.config.isAdmin)`) is a logic finding that FEEDS the XSS hunt:

* Treat `id`/`name` values harvested from the injection point as
  candidate clobber keys for the page's own scripts.
* Proof discipline is unchanged: the clobbered branch observed in a
  self-owned marker run, not a static guess.
* Clobbering alone (no execution) closes as its own hypothesis class —
  it chains with everything else (chain-architect territory).

## 4. Sanitizer and Framework Traps

* **Version-pin the sanitizer as a FACT.** Sanitizer libraries regress;
  the mXSS 2024 wave re-demonstrated that "sanitized" output re-enters
  mutation hosts and breaks. The sanitizer's name+version goes in the
  ledger; a known-stale version is itself a reportable hygiene fact.
* **"Safe" framework APIs are sink-shaped.** `element.innerHTML =`
  behind any wrapper (including framework templating that "escapes") is
  still innerHTML: the wrapper's promise is the hypothesis, the mutation
  differential is the verdict.
* **Trusted Types / CSP are recorded facts** (organ hard rule unchanged):
  when present they bound impact claims; they do not close the mutation
  hypothesis — the mutation record still ships as a finding.

## 5. The Craft, Stated As Five Field Rules

1. Re-derive context after every mutation; mutation ≠ payload.
2. One minimal differential per mutation class; mutated bytes are the
   artifact.
3. Clobber keys are harvested from evidence, not sprayed.
4. Sanitizer name+version is a ledgered FACT; regressions are expected.
5. The marker proof still decides (canary, self-owned, spine §8) — mXSS
   earns severity through the chain it enables, not its own drama.
