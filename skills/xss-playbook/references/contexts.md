# Sink Contexts & Payload Grammar

## Context classification (recorded BEFORE any payload)

| Context | Recognition | Minimal grammar | Neutralized control |
| --- | --- | --- | --- |
| Element text | reflection between tags, no encoding | `<` + marker element (e.g. `<b id=MARKER>`), then context's execution primitive | same length with `<` URL-encoded |
| Attribute value (generic) | reflection inside `attr="..."` | breakout quote + new marker attribute | quote escaped/doubled |
| `href`/`src` attribute | URL-shaped sink | scheme the page permits + marker fragment; javascript: only as the recorded hypothesis it is | scheme stripped by the app |
| Event attribute (`onerror=` etc.) | reflection lands in an existing handler value | handler body = marker assignment (`this.id='MARKER'`) | body punctuation stripped |
| JS string literal | reflection inside quotes in a script block | breakout quote + `;` + marker assignment + `//` to close | quote backslash-escaped by the app |
| JS code position | reflection unquoted in script | marker assignment statement | parens/semicolons filtered |
| HTML comment | inside `<!-- -->` | breakout `-->` + marker element | comment not closed |
| URL parameter (page-level) | value lands in `location`-derived sinks | encode the marker; grammar belongs to the DOM sink below | encoding rejected |

## DOM sinks (from bundle artifacts)

`innerHTML`/`outerHTML` · `document.write(ln)` · `insertAdjacentHTML` ·
`eval`/`Function`/`setTimeout(string)` · script-element `src` assignment ·
`location` assignment/`location.href`/`location.replace` ·
`jQuery(html)`/`$(...)` with html strings · `setAttribute('href'|'src', ...)`
· `postMessage` handlers writing into any of the above.

DOM sources (trace from): `location.hash/search/pathname/name` ·
`document.referrer` · `postMessage` data · `window.name` · storage keys.
The hypothesis cites the source line and sink line from the artifact.

## CSP interpretation (fact, then verdict)

| Policy shape | Verdict to record |
| --- | --- |
| No CSP header | recorded absence; standard impact story |
| CSP with `unsafe-inline` in script-src | inline execution survives; grammar unaffected |
| script-src nonce/strict-dynamic only | inline payloads dead; HTML-injection impact capping unless a bypass hypothesis (trusted-types gaps, DOM sinks that parse regardless) is CONFIRMED |
| `trusted-types` enforced | sink list shrinks to non-TT sinks; DOM XSS hypotheses re-rate |
| default-src strong, object-src weak | object/plugin vectors get their own hypothesis, not a blanket claim |

## Marker discipline

The marker appears in the payload AND in the observed outcome: element id,
attribute value, assigned variable, or fragment — one observable artifact,
one record. Screenshots/DOM snippets are operator-captured evidence files
cited by the CANARY record; the report reproduces the marker pair
(payload-marker ↔ observed-marker), never a bare screenshot of an alert.
