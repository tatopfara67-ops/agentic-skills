# The executable method — M1–M5 for business-logic-hunter

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The lineage critique that
justifies each step (why these phases exist, what was weak in
Soroush Dalili's public practice) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

### M1 — the bypass matrix (rule classes before tricks)

| Rule class (observed on the target) | Trick family | First probe (corpus-pinned) |
| ------------------------------------ | ------------ | --------------------------- |
| method blocklist (403 on POST) | override family: `X-HTTP-Method-Override` / `X-Method-Override` / query `_method=` | corpus bypass-class entry, byte-exact |
| path regex (pattern blocklist) | normalization family: dot-segments, case, encoding per corpus grammar class | corpus entry; encoding variants from M2's seam evidence |
| header gate (missing header = 403) | redistribution family: content-type re-casing, header smuggling via body fields per corpus | corpus entry |
| unknown rule | REFUSED until M3's chain map names the enforcing hop | — |

Rules: a trick fired without its rule-class row is spray (W1); the
matrix grows from OBSERVED 403/redirect behavior (the rejection
classes recorded verbatim — the signal-smith M1 dialect habit).

### M2 — the reshaping differential (three conditions)

Per (rule class × trick family):

1. **Conditions, n ≥ 5, interleaved**:
   * baseline — the blocked request as-is (the 403 oracle);
   * treatment — the reshaped request, byte-exact from the corpus
     entry, same semantic intent;
   * control — a DIFFERENT reshaping of the same family that should
     NOT defeat the rule (e.g. unknown override header) — the
     placebo that catches permissive intermediaries.
2. **Observation**: response class bucket (status, length bucket,
   action-executed marker on operator-owned state).
3. **Confirm rule**: treatment reaches the backend action class in
   ≥ 4 of 5 AND baseline blocked 5/5 AND control blocked ≥ 4 of 5.
   Control passing too = the INTERMEDIARY is permissive, not the
   rule defeated — a different finding class, recorded as such.

### M3 — the chain-map linkage (which hop was defeated)

The target's parser chain is mapped per desync-hunter's CHAINMAP
discipline BEFORE tricks are graded (edge/WAF/backend with version
evidence). Each confirmed bypass cites the hop: "defeated hop-2
rule (WAF class X, version-pinned)" — the mechanism, not the
anecdote (W3). A bypass with no attributable hop is graded
UNATTRIBUTED and the chain map is re-run before it rides a report.

### M4 — the repeatability rule

A confirmed bypass re-runs n ≥ 5 MORE times across ≥ 10 minutes
(cache states, rule warmup): reproduces ≥ 4 of 5 → STABLE; flaky →
ENVIRONMENT-CONDITIONAL, recorded with its conditions (load class,
cache state) — never reported as a stable bypass (W4).

### M5 — the impact ceiling

```
CEILING: bypass=<rule class, hop cited, stable|conditional> route-
  opened=<what the backend now accepts> impact=<NONE-DEMONSTRATED
  | demonstrated on operator-owned state with marker> next: impact
  differential is auth-boundary M3's lane, cited by cell
```

"Bypassed" never grades as "accessed" in this organ's reports; the
route-opened row is the deliverable and the impact row cites the
boundary differential that closed it (W5).

## 2. Falsifiers — what would prove this method wrong

* The control passes as often as the treatment → the rule was never
  the gate: the intermediary accepts anything of that shape; the
  finding reclasses to permissive-intermediary (route to desync-
  hunter for the seam).
* A bypass stable for 10 minutes fails on re-test next day → rule
  learning/WAF updated: the record keeps both windows with
  timestamps; STABILITY is time-boxed and re-quoted with its window.
* The chain map attributes the defeat to a hop that demonstrably
  never saw the request (backend log evidence) → the map is wrong
  at that hop: re-map with the log as control; the bypass's
  citation is corrected on record.
* A trick family fires on a rule class it should not fit → the
  rule class was mis-observed (the rejection dialect was read
  wrong): re-read the verbatim 403 classes; the matrix row moves.

## 3. Worked micro-example (numbers consistent, incident fictional)

Rule observed: POST /api/admin blocked 403, rejection class
verbatim "method not allowed" (recorded). M1 row: method-blocklist
→ override family. M2: baseline blocked 5/5; treatment
(`X-HTTP-Method-Override: POST` on GET) reaches action 4/5; control
(`X-Method: POST` unknown header) blocked 5/5 → CONFIRMED. M3:
chain map names hop-2 (WAF class, version-pinned) as the enforcing
hop; citation attached. M4: re-run across 15 min → 5/5 → STABLE.
M5 ceiling: route-opened = admin action reachable; impact =
NONE-DEMONSTRATED (auth still required — boundary differential cell
cited, parked as chain candidate). Report grades bypass P4 with
hop, stability window, and the honest impact row.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
Soroush Dalili's art is real — the HTTP-reshaping bypass grammar
(irsdl's method overrides, path normalization tricks, header
redistribution) is the field's reference craft — but the published
form has floors: bypasses as curated lists, single-bug narratives,
the parser hop each trick defeats unnamed, repeatability unproven,
and bypass conflated with impact. This module extracts what is
protocol-shaped and ships the replacement: a bypass-class matrix
with preconditions, the reshaping differential, chain-map linkage
to the defeating hop, a repeatability floor, and an impact ceiling.
An agent that has never read the writeups must run this at its
grammar.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Bypasses as curated lists — the tricks ship as enumeration posts (method-override families, case tricks, dot-segments) | A list without preconditions sprays: which trick applies depends on the defender's RULE (method blocklist? path regex? header gate); without the rule class, the "method" is matching lottery tickets |
| W2 | Single-bug narratives — each bypass shown defeating ONE concrete WAF/rule in ONE writeup | The generalization (this trick family defeats rules of shape S) stays implicit; readers re-discover applicability per target by trial |
| W3 | The defeating hop unnamed — the writeup says "the WAF missed it" without the parser chain | WHICH layer parsed what is the whole mechanism (the desync-hunter CHAINMAP habit); without it the fix-side and the finding-side both stay folklore |
| W4 | Repeatability unproven — the demo fires once | Reshaping tricks interact with normalization order and caching; a 1-of-1 bypass is environment luck until re-run — the floor every organ in this charter names |
| W5 | Bypass conflated with impact — "bypassed the rule" graded as if access followed | The bypass OPENS a route; whether the route leads anywhere is a separate differential (the auth-boundary M3 discipline); the writeup form merges them into one adjective |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Each trick family bound to rule-class preconditions | **M1** — the bypass matrix |
| U2 | Reshaping as a three-condition differential | **M2** — the reshaping differential |
| U3 | The defeating hop cited from a chain map | **M3** — the chain-map linkage |
| U4 | Repeatability as a floor before claims | **M4** — the repeatability rule |
| U5 | Bypass and impact kept separate | **M5** — the impact ceiling |
