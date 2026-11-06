# The executable method — M1–M5 for injection-lab

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
the sqlmap-era tradition) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

### M1 — the oracle census (before any payload exists)

For each injection-surface parameter (from surface records), determine
WHICH channels exist, cheapest and quietest first. Each probe is an
EXPERIMENT with n = 3:

| Channel | Quiet probe | Evidence it exists |
| ------- | ----------- | ------------------ |
| error | one malformed grammar value (per corpus class, single request) | backend error text appears whose signature class matches a corpus entry |
| boolean | benign differential pair (`7` vs `8` against a known record) | response buckets differ (status/length bucket/first-line) on a TRUE/FALSE fact the agent controls |
| time | benign slow request + baseline timing FIRST (M3's floor) | see M3 — never probed before the baseline exists |
| out-of-band | operator-owned collector reference (M5) | callback observed on the collector |

Census output: one FACT record per parameter listing its channel set.
A parameter with an empty channel set is CLOSED on record — no
battery is fired at it (the W1 floor, inverted: classification first,
spray never).

### M2 — the parity differential (boolean claims as statistics)

1. **Alternation design**: TRUE-probe and FALSE-probe interleave,
   n ≥ 10 pairs, one fact the agent controls (e.g. a record id known
   to exist vs one known not to).
2. **Bucket observation**: each response bucketed [same / ±10% /
   >2×] plus first-line class — recorded per pair.
3. **Confirm rule (all three)**: TRUE bucket ≠ FALSE bucket in ≥ 8 of
   10 pairs AND no pair flips order when the probe order is reversed
   (run a second reversed pass, n ≥ 4) AND the parity holds across
   re-issuing the SAME fact (jitter check: identical inputs, n ≥ 3,
   stable buckets).
4. A single pair difference, however pretty, is a LEAD with
   `n_pairs=1` — the ledger records it as such, and the report gate
   refuses it (the W2 floor made mechanical).

### M3 — the jitter-gated timing oracle

1. **Baseline FIRST**: 10 benign requests to the same endpoint,
   recorded median and IQR of wall time. The baseline is a CONTROL
   record; without it, the timing channel is CLOSED.
2. **Threshold, pre-registered**: treatment delay counts only if
   treatment median − baseline median > max(3 × baseline IQR, 2 s).
3. **Confirm rule**: n ≥ 5 treatment / 5 baseline, interleaved A-B-A-B
   (never five sleeps in a row — queue warming fakes the effect);
   ≥ 4 of 5 treatment runs over threshold AND baseline stable during
   the interleave.
4. Escalation ladder inside the oracle: 2 s → 5 s payloads only AFTER
   the 2 s class confirms; the 10 s class is REFUSED unless the
   operator approves the additional dwell (it is the target's money).

### M4 — the extraction budget table

Extraction starts only after M2/M3 confirmation, under an explicit
budget row:

```
EXTRACT-BUDGET: channel=<boolean|time> rows_target=<n or "count only">
  req_per_row=<estimate incl. charset arithmetic shown> rate_floor=
  <house civility cap> resume_ledger=<id> abort=<basis: any 5xx
  streak or baseline drift> 
```

Rules: binary-search extraction arithmetic (rows × ceil(log2
charset)) is shown BEFORE the job — the W5 floor is arithmetic, not
discipline. Any 5xx streak ≥ 3 or baseline drift during extraction
ABORTS the job and parks it with a resume note; extraction is
resumable precisely because the ledger has the row cursor.

### M5 — the out-of-band canary rule

1. The collector is operator-owned and OUT-OF-SCOPE — never a
   subdomain of the target (the desync-hunter fixture lesson,
   applied here), never a shared public Collaborator pool for
   operator-attributable evidence.
2. Each callback reference is unique per EXPERIMENT (per-parameter
   subdomain/label) — a hit maps to one probe, one parameter, one
   timestamp.
3. A callback proves the CHANNEL (data left the target toward a
   controlled listener); IMPACT is a separate claim requiring the
   channel's read-back (what the backend fetched/did) — the
   ssrf-playbook ladder is the cross-reference. "We got DNS" is
   never "we have SQLi impact" in any report this organ signs.

## 2. Falsifiers — what would prove this method wrong

* The reversed-parity pass flips the buckets → order effect, not a
  boolean oracle: M2's confirm rule kills the claim; re-design the
  fact pair.
* Baseline IQR exceeds the treatment delta → the timing channel is
  the target's weather, not an oracle: CLOSED, recorded.
* Two different corpus error-signatures match the same response →
  signature family too coarse: file a corpus correction; the version
  pin rides the signature (the W4 fix).
* Extraction aborts on 5xx streak at row k, resumes clean, aborts
  again at row k+j → the abort basis is load, not defense: record
  BOTH aborts with timestamps; the operator decides whether the
  target is defending or dying.

## 3. Worked micro-example (numbers consistent, incident fictional)

Parameter `?item=` on a product endpoint. M1 census: error channel
YES (signature class matches corpus INJ-004 entry, backend family
pinned as a FACT), boolean channel UNKNOWN, time CLOSED until
baseline. M2: TRUE/FALSE fact pair `id=7` vs `id=70000`, 10 pairs →
9/10 bucket separation, reversed pass 4/4 stable, re-issue jitter 3/3
stable → boolean oracle confirmed. M3: baseline median 180 ms, IQR
20 ms → threshold max(60 ms, 2 s) = 2 s; 2 s-class treatment 5/5
over, baseline stable 5/5 → time oracle confirmed at level 1; 5 s
class not needed. M4: extraction budget = count-only first (11
requests, parity arithmetic shown), then 40 rows × ceil(log2 62) ≈ 6
req/char-column, house rate floor, resume ledger id attached. Ceiling:
data extraction demonstrated under operator scope; impact beyond the
queried table NOT claimed.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
injection-lab carries no single master's name — its "lineage" is the
industry default it was built against: the sqlmap-era payload-spray
tradition and the checklist habit of running a battery before knowing
what oracle, if any, the sink even exposes. A16 still applies: the
tradition has documented floors, they get critiqued mechanically, and
the replacement ships as executable protocol. An agent that has never
launched sqlmap must run this at a better precision than sqlmap.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the scan-first tradition (context, not steps)

| # | What the tradition shows (documented) | Why it is weak as a shipped method |
| - | -------------------------------------- | --------------------------------- |
| W1 | Battery-first — fire the payload list, then look at what came back | Oracle classification comes AFTER the noise: the target's error/boolean/time/out-of-band channels are knowable quietly first; spraying burns budget, trips WAFs, and closes sinks that a quieter probe would have kept open |
| W2 | Boolean-blind confirmed by ONE true/false pair, read by eyes | One page-length difference is jitter until proven otherwise: no n_runs, no alternation, no bucket statistics — the tradition's false-positive engine |
| W3 | Time-based oracles without a jitter baseline — `SLEEP(5)` once, delta seen, "confirmed" | A loaded shared host delays everything seconds; the tradition never measures the target's idle IQR first, so its slowest oracle is also its noisiest false source |
| W4 | Error signatures matched from memory or stale regex lists | Signature drift: backend version families change error grammar; unpinned signatures produce both misses and false families. Signatures are data (versioned corpus), not lore |
| W5 | Extraction habits without a budget — dump-the-table reflex at scanner rates | The extraction phase is where the DoS and the WAF trip actually happen; a method without explicit row/request caps and resume points is a liability wearing a badge |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Oracle channel classified FIRST, quietly, before any payload battery | **M1** — the oracle census |
| U2 | Boolean claims as alternation statistics | **M2** — the parity differential |
| U3 | Time claims above a measured jitter floor | **M3** — the jitter-gated timing oracle |
| U4 | Signatures as versioned data with sources | `references/corpus.json` (INJ-001…016; INJ-016 releases through the weapons vault) + `references/oracles.md` — consumed, never re-typed |
| U5 | Extraction as a budgeted, resumable job | **M4** — the extraction budget table |
| U6 | Out-of-band callbacks under canary doctrine | **M5** — the operator-owned collector rule |
