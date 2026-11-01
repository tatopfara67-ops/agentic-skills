# encoding-grammar.md — the input ladder, seam map, and variation catalog

Load when calibrating a validator or choosing the minimal variation.

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
record.

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

| Variation | Byte delta | Select when |
| --- | --- | --- |
| case flip (`s`→`S` in a keyword) | 1 | case-insensitive validator, case-sensitive sink |
| single %-encode (`<`→`%3C`) | 2 | edge decodes once, origin decodes twice |
| double %-encode | 3 | proxy re-encodes on forward |
| unicode homoglyph | 1 char | sink renders/normalizes (NFKC) after filter |
| overlong/malformed utf-8 | 2-3 | charset disagreement between parsers |
| NUL injection (`%00`) | 3 | C-string truncation behind the filter |
| terminator smuggle (`%0d%0a`) | 6 | header/log injection behind the filter |
| charset param switch (`?utf-7`) | param | legacy charset decoder at origin |
| case/underscore header name | 1 | header rewrite rules vs origin lookup |
| JSON escape layer (`\u0022`) | 6 | JSON parser before SQL/template layer |

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
