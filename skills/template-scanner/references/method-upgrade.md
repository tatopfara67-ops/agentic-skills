# The executable method — M1–M5 for template-scanner

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
ProjectDiscovery's template practice) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

Quickstart — matchers audited BEFORE any run (M1), noise table kept
(M4), every surviving hit a T-EXP record (M5):

```bash
# M1 review gate — read each matcher's falsifier, pin tool + pack
nuclei -version && nuclei -ut                # version + template update
nuclei -l s2-live.txt -tl | wc -l            # what WOULD run
# run the audited pack — severity re-rated at M2, rate capped
nuclei -l s2-live.txt -severity medium,high,critical \
       -rate-limit 30 -c 15 -json -o t-hits.txt
# M4 noise table — a matcher hitting EVERY host is noise, parked
jq -r '."template-id"' t-hits.txt | sort | uniq -c | sort -rn | head
# gate: a matcher with no stated falsifier is REJECTED before it runs
```

### M1 — the review gate (+ template-as-experiment)

1. Before a pack runs, its matchers are AUDITED as hypotheses:
   for each template — what observation would FALSE it? A matcher
   set with no falsifier (matches anything that returns 200) is
   REJECTED at the gate (W1).
2. Each surviving template converts to an EXPERIMENT record:
   `T-EXP: template-id, matchers summary, expected-state,
   falsifier, severity-class (pre-M2)`.
3. House packs (the curated set for this arsenal) are versioned
   like any corpus — external packs are pinned by hash (M3).

### M2 — the severity re-rating ladder

Template label → target-relative class, ALWAYS re-derived:

| Template label | Default re-rate | Escalates when | Demotes when |
| -------------- | --------------- | -------------- | ------------ |
| critical | P2-class hypothesis | exploit-public + version-pin CONFIRMED (M5 evidence) | version pin INFERRED only → P4 |
| high | P3-class hypothesis | auth-bypass class + operator confirmation | staging host in scope statement → P5 |
| info/noise classes | hygiene, P5 | — | duplicates prior finding → merge |

Rules: the OUTPUT table of a run carries both `template-severity`
and `re-rated` columns; a report citing only the former fails this
organ's gate (W2).

### M3 — the version matrix

```
RUN-PIN: engine=<version-or-house-equivalent> pack=<name@hash>
  dsl-features-used=<list> compat=<audited date>
```

Every hit cites the RUN-PIN of the run that produced it (W3). A
re-run with a changed engine or pack hash is a NEW run; hits from
different pins are never merged without re-evidence.

### M4 — the noise table

| Noise class (taxonomy) | Disposition |
| ---------------------- | ----------- |
| self-signed / basic TLS config | hygiene list, appendix, never a finding row |
| banner / Server-string disclosure | hygiene list, merged per host |
| missing header (HSTS etc.) | config-note class; finding only with auth-context argument |
| takeovers/CDN classes without dangling evidence | REFUSED — routed to subdomain-hunter M2 instead |

The filter is applied BEFORE the report draft exists; filter
counts are recorded (`noise-filtered: 41 of 67 raw hits`) — visible
selectivity, not silent burial (W4).

### M5 — the hit record

```
HIT: t-exp=<id> run-pin=<id> target=<surface> evidence=<request
  bytes + response class + matcher-observed summary> version-pin=
  <CONFIRMED|CLASS-ONLY|INFERRED> re-rated=<class> next=<verify
  EXPERIMENT id or route-to organ>
```

A hit without its evidence block is refused at the report gate
(W5); the version-pin discipline inherits scan-economist M3's
confidence classes.

## 2. Falsifiers — what would prove this method wrong

* The same template id produces different match behavior across two
  RUN-PINs → the version matrix caught drift: both hits stand
  separately, never merged; the pack audit is re-dated.
* A rejected-by-M1 template (no falsifier) fires on a target and
  "finds" something real → luck, not method: the template is STILL
  rejected; a new house template is authored with a real falsifier,
  and the finding is re-proven through it.
* The re-rate ladder demotes a critical to P4 but the version pin
  was later CONFIRMED by evidence → the ladder did its job at the
  time; the finding ESCALATES with the new evidence attached, and
  the delta is visible in the record.
* Noise-filter count exceeds 70% of raw hits → the pack mix is wrong
  for this target class: re-curate the house pack, cite the count.

## 3. Worked micro-example (numbers consistent, incident fictional)

Run 7: house pack `corp-v4@sha256:9f2c…`, 62 templates pass M1
(11 rejected: no-falsifier classes). Target: bank-front scope. Raw
hits: 67. M4 noise-filtered 41 (TLS-banner classes) → 26 signal
candidates. HIT example: template `x-redirect-open` (T-EXP 12),
evidence = request bytes + 302 Location reflecting the operator
marker, version-pin CLASS-ONLY (redirect class, product version
INFERRED), template label `medium` → re-rated P3 (auth-context:
login-flow present). RUN-PIN cited on the hit. Report draft shows
both severity columns; auditor recomputes the filter counts.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
ProjectDiscovery's art is real — subfinder and nuclei industrialized
detection-as-templates — but the published practice has floors:
templates copy-pasted and run unreviewed, severity labels baked by
the template author for a generic universe, matcher drift between
engine and template versions, and noise classes narrated as
findings. This module extracts what is protocol-shaped and ships
the replacement: a pre-run template review gate, a severity
re-rating ladder, a version-pin matrix, a noise-class filter table,
and the template-as-experiment record. An agent with no nuclei
binary must run this at its discipline.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published practice (context, not steps)

| # | What the practice shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------------- | --------------------------------- |
| W1 | Templates run as received — the default workflow is `nuclei -t ~/nuclei-templates` against a list; nobody audits the matchers before the run | The matchers ARE the experiment's acceptance criteria: running unreviewed criteria means the scanner's authors pre-registered your hypotheses for you, against a target they never saw |
| W2 | Severity baked into the template — `severity: critical` ships in YAML for a generic universe and rides the output verbatim | Severity is target-relative (a self-signed cert is hygiene on a test box, P3 on a bank front door); the label's universality is exactly what makes it wrong everywhere in particular |
| W3 | Engine × template-pack drift untracked — matcher DSL features evolve; old packs on new engines (or the reverse) match differently or silently | A finding's meaning depends on an unrecorded version pair; the same template id means different things across months, and nothing in the output says which |
| W4 | Noise classes narrated as findings — self-signed cert, missing header, `Server:` banner disclosure fill reports because the template matched | The matcher fired; the CLASS is informational by taxonomy; without a filter table the report buries signal under ceremony |
| W5 | Template hits reported without the request/response evidence the matcher saw | "CVE-2021-44228 [critical]" with no bytes is gossip with a badge — the hit is the START of evidence, and the practice treats it as the end |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Matchers reviewed as pre-registered criteria | **M1** — the review gate |
| U2 | Severity re-rated per target context | **M2** — the re-rating ladder |
| U3 | The version pair pinned per run | **M3** — the version matrix |
| U4 | Noise filtered by class table | **M4** — the noise table |
| U5 | Hits carry their evidence | **M5** — the hit record |
| U6 | Templates as EXPERIMENT records | **M1(b)** — template-as-experiment |
