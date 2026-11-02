# cache-method.md — the disagreement hunt, step by step

> Part of **cache-playbook v1.0.0** (package architecture).
> **Load when:** any step of the SKILL.md procedure needs its exact
> probes, its oracle, or its falsifier. Authoritative rules live in
> [`../SKILL.md`](../SKILL.md) — **SKILL.md wins** on any conflict.

---

## 1. The shape of every cache proof

Both attack families reduce to one shape:

```
request R1 (carries the trick)  -> stored by the cache   [MISS observed]
request R2 (the clean victim)   -> served R1's response  [HIT observed]
```

Deception: R1 is the operator's authenticated fetch of a confused
path; R2 is the anonymous fetch. Poisoning: R1 is the unkeyed-input
request carrying the marker; R2 is the clean retrieval. The panel
(`X-Cache`-family headers, `Age`) must show the MISS→HIT transition
for R1→R2 in both families, and the response bytes must differ from a
no-truth baseline. That is the whole instrument — everything below is
how to find where the trick and the victim diverge.

## 2. Fingerprinting (step 1), with the oracle

Repeat-fetch the same URL twice with identical requests. Oracle for
"cache present": second response shows HIT-class status or `Age` > 0
with matching `Date` deltas. Falsifier: both responses MISS with
distinct `Date` — no cache in the path (organ stops; the row records
it). Record the vendor fingerprint (header names are telling:
`CF-Cache-Status`, `X-Cache`, `X-Served-By`, `X-Varnish`) — cache
behavior is per-vendor and per-config, never assumed transferable
between targets.

## 3. Key mapping (step 2) — the differential that never ends

For the target path, vary exactly one element per request pair and
read the HIT pattern:

| Variation pair | Same HIT ⇒ | Different keys ⇒ |
| --- | --- | --- |
| query param added | param NOT in key | param keyed |
| header added | header unkeyed (poisoning candidate) | header keyed |
| path case change | case-normalized key | case-sensitive key |
| `?` vs `;` param sep | both collapse to one key | distinct keys |
| trailing delimiter | normalization seam (probe family) | — |

Every row lands in the dossier's key-map table with its request
records. The unkeyed column of this table IS the poisoning candidate
list; the normalization-seam rows feed step 4's delimiter sweep.

## 4. Delimiter sweep (step 4) — the deception engine

Candidate delimiters (the USENIX'20 set plus practice): `.`, `/`,
`%2f`, `%2e`, `%23`, `%3f`, `;`, `..;/`, `#`, `?`, `\`, and the
static-suffix family (`.css`, `.js`, `.ico`, `.png`, `.txt`, `.swf`
appended or path-embedded). For each: ONE request, operator session,
on a personalized page; compare response bytes to the unconfused
fetch. Oracle for "confusion achieved": bytes equal the personalized
body while the cache treats the variant as cacheable (its
store-decision visible in the MISS→HIT of the next fetch). Falsifier:
404/redirect body differs, or the cache refuses to store — record and
next delimiter. One per request, always; a combined probe answers
nothing (which element confused the parser?).

## 5. Deception differential (step 5) — the operator-as-victim law

```
baseline    anonymous fetch of confused path      -> MISS, public body
treatment   operator-session fetch, same path     -> MISS, PRIVATE body
control     anonymous re-fetch, same path         -> HIT, ??? 
```
CONFIRMED requires: treatment stored the private body (MISS with
private bytes), control retrieved it (HIT with private bytes). The
private body contains ONLY operator data. n_runs ≥ 2 with the same
transition. The Age header at control time bounds the exposure
window — that number rides into the report's impact line.

## 6. Unkeyed-input reflection (step 6) — mechanism probing

From the key map's unkeyed list, send one benign self-owned marker
(e.g. `znm-cacheprobe-<nonce>`) through each unkeyed input; the
oracle is the marker's reflection in the stored response body or
headers. Reflection in headers only (e.g. a reflected
`X-Forwarded-Host` into `Location`) is still reflection — the sink
family decides exploitability, and that question belongs to
xss-playbook's sink grammar once reflection is proven. Falsifier:
marker absent from the stored response — the input is unkeyed AND
unreflected; discard.

## 7. Poisoning proof on a nonce path (step 7) — the victimless law

The proof path is `<target>/<nonce-folder-znm...>/legit-asset`:
1. store: request with the unkeyed trick + marker payload → MISS,
   marked body stored;
2. retrieve: clean request, same nonce path → HIT, marked body
   served;
3. record both, attempt purge (or record no purge API exists).

The nonce guarantees no other human ever requests the key. What this
proves: unkeyed input controls a stored response served to other
requesters of that key. What it does NOT prove (and must never
"demonstrate" against real users): impact on a real person's session
— that step is the program's to credit from the mechanism proof, and
chain-architect composes escalation only through further nonce-path
links.

## 8. Classification notes

* Deception CVSS geometry: AV:N/AC:L usually, C:H with the private
  body's content class; Scope rarely changes (the cache is the same
  authority zone) — state the vector you observed, not the family's
  folklore.
* Poisoning geometry: score the payload's achieved effect (reflection
  alone: a hardening lead; stored script served to key holders: the
  XSS-family vector on the serving path).
* VRT rows: server security misconfiguration → cache deception /
  cache poisoning families; cross-reference the taxonomy file before
  writing the dotted id (it ships with skill-mythos).
* Report reproduction: the two requests verbatim, the nonce, the
  HIT/MISS records, and the purge attempt — a triager replays it
  against their own cache in minutes.

## 9. The purge ledger line

Every stored proof appends one ledger line: what was stored, under
what key, when it was purged or why it could not be. W2 in action:
the campaign ends with the cache exactly as it was found — the
finding survives, the damage does not exist.
