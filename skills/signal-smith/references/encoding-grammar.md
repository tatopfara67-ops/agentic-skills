# encoding-grammar.md — the input ladder, seam map, and variation catalog

Load when calibrating a validator or choosing the minimal variation.
The variation classes named in section 3 are carried byte-exact and
attributed in `references/corpus.json` (the versioned variation
corpus, A19) — the catalog below names the classes and the selection
rules; the corpus carries the bytes.

## 1. The Input Ladder (calibration template — CONTROL records)

| Dimension | Edge inputs | What the verdicts reveal |
| --- | --- | --- |
| length | 0, 1, max-1, max, max+1, 2×max | truncation point, enforcement point |
| charset | [a-z], [0-9], symbols, unicode, C0 controls, NUL | the accepted alphabet |
| encoding | raw, %-enc, double-%-enc, \u escapes, &#...; | decode layers |
| structure | flat, json, xml, nested, array-wrapped | parser selection |
| content-type | form, json, text/plain + charset params | charset assumption |
| frequency | 1, 2, 5, 10 requests at fixed spacing | rate filter floor |

Rule: the ladder carries NO payloads — it measures. Every verdict
pair (validator verdict, backend behavior class) is one CONTROL
record. (The corpus serves the forge in section 3 — never the
ladder; contaminating calibration with probe bytes poisons the
grammar map, house rule 3 of the corpus.)

## 2. The Seam Map (double-parse inventory)

A seam exists wherever the SAME logical input produces DIFFERENT
backend behavior classes under different encodings. Inventory:

```
SEAM-<k>: edge=<WAF/proxy> vs origin=<app/parser>
  divergence observed: input X (raw) -> class A
                        input X (%-enc) -> class B
  hypothesis: edge normalizes, origin re-decodes
  minimal variation candidate: <one byte edit>
```

Typical seam locations: WAF→origin, CDN cache key vs origin route,
client-side validator→server API, JSON parser→template/SQL layer,
URL router→file path resolver, header parser→logging sink.

## 3. The Variation Catalog (minimal edits, selection rules)

Every fixed-byte class resolves to its versioned corpus entry
(`references/corpus.json`); the engagement's own variation bytes
derive from the captured grammar (A19 derivation rows — the corpus
enumerates the classes, the grammar picks the bytes):

| Variation | Corpus | Byte delta | Select when |
| --- | --- | --- | --- |
| case flip (`s`→`S` in a keyword) | derivation row (labeled: no transcribed corpus carrier — a target-grammar-derived flip, not a fixed byte class; A19 clause b) | 1 | case-insensitive validator, case-sensitive sink |
| single %-encode (`<`→`%3C`) | SIG-001 | 2 | edge decodes once, origin decodes twice |
| double %-encode (`%253C`) | SIG-002 | 3 | proxy re-encodes on forward, or decodes-once filter over a twice-decoding origin |
| unicode homoglyph (`＜` U+FF1C) | SIG-003 | 1 char | sink renders/normalizes (NFKC/best-fit) after filter |
| overlong/malformed utf-8 (`%C0%80`) | SIG-004 | 2-3 | charset disagreement between parsers |
| NUL injection (`%00`) | SIG-005 | 3 | C-string truncation behind the filter |
| terminator smuggle (`%0d%0a`) | SIG-006 | 6 | header/log injection behind the filter |
| charset param switch (UTF-7 `+ADw-`) | SIG-007 | param | legacy charset decoder at origin |
| JSON escape layer (`\u0022`) | SIG-008 | 6 | JSON parser before SQL/template layer |
| header-name case fold (`x-forwarded-for`) | SIG-009 | 1 | case-anchored edge rules over a case-folding origin |
| duplicate-parameter pair (`par1=val1&par1=val2`) | SIG-010 | varies | precedence disagreement between two parsers (HPP) |
| header-name underscore variant (`X_Forwarded_For`) | operationalization row (labeled: no transcribed corpus carrier — default underscore-dropping behavior differs per proxy build; verify on the captured grammar before use, A19 clause b) | 1 | header rewrite rules vs origin lookup |

Rule: pick the SMALLEST delta whose divergence class is already
observed in the seam map. The catalog is ordered by typical delta
for exactly this reason.

## 4. Frequency Discipline

* Observe the target's natural rate tolerance in the ladder's
  frequency dimension; ride BELOW it for variations.
* One variation request at a time; spacing ≥ the calibration
  spacing. Parallel variation requests are forbidden.
* A 429/reset response parks the seam immediately (fact reported,
  no retry escalation — hard rule 3).

## 5. Handoff Record (to the payload organ)

```
SPLIT-<k>: seam-<k> confirmed — artifact <bytes>, records R-a/b/c
  grammar: <what the validator accepts>
  variation: <the minimal edit and its bytes>
  payload organ: <injection-lab|xss|ssrf|desync>
  next: payload differential WITH this variation as transport,
        baseline = unencoded payload, control = variation alone
        (no payload) — the triad still belongs to the payload organ
```

## 6. Anti-patterns (MISTAKE records)

* Payloads inside calibration inputs (contaminates the grammar map).
* Five variations "to be sure" — the cap is two (hard rule 1).
* Retrying a WAF-blocked variation with different encodings —
  that is a volume war with extra steps.
* Claiming impact from a split alone — the split is the seam fact;
  impact needs the payload organ's triad.
