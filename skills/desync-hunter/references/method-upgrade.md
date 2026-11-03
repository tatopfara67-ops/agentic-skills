# The executable method — M1–M4 for desync-hunter

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
Kettle's published desync research) is preserved verbatim as the
§3–§4 appendix.

## 1. The executable protocol — M1 through M4

### M1 — the chain map, as a record with a schema

Before any ambiguous byte exists, one FACT record per hop:

```
CHAINMAP hop-1: role=edge-proxy product=nginx evidence="Server: nginx/1.24.0
  (Via header, ordered headers: Server,Date,Content-Type)" framing=H1+H2
CHAINMAP hop-2: role=cache product=unknown evidence="X-Cache: Hit; header
  order differs from origin on MISS responses" framing=H1
CHAINMAP hop-3: role=origin product=node evidence="X-Powered-By: Express"
  framing=H1
```

Evidence commands (all quiet, all scope-gated to the seam's owner):

1. `http_probe` GET / — record response headers IN ORDER plus the
   Server / Via / X-Cache / X-Served-By / X-Powered-By set.
2. ALPN capability: `curl -sv --http2 https://<host>/ 2>&1 | grep -i
   alpn` — records whether the edge negotiates H2 while the origin
   speaks H1 (the h2 downgrade seam).
3. Absolute-form acceptance: `http_probe` with request line
   `GET https://<host>/ HTTP/1.1` — accepted-and-forwarded marks a
   proxy hop (and a candidate seam); rejected is also a recorded bit.
4. Error-page signatures per hop: one deliberately malformed request
   (bad method) — WHICH error page answers names WHICH hop terminated
   it. Two different error pages on two probe types = two parsers
   disagreeing in the wild, before any CL/TE craft.

Version granularity matters: "nginx" is not "nginx/1.24.0"; the
selection matrix keys on the PAIR of versions, and the report's
reproduction section cites them verbatim.

### M2 — the selection matrix (parser pair × ambiguity class)

Read the CHAINMAP pair for the seam under test, then select:

| Front / Back pair | Classes the pair ADMITS | First probes | Preconditions |
| ----------------- | ----------------------- | ------------ | ------------- |
| H1 / H1 | duplicate-CL · CL.TE · TE.CL · TE.TE · obs-fold · header-name oddities · absolute-form | corpus DS-001 (CL.TE differential), then per class | both hops announce H1; edge does not re-frame (test with probe #4 of M1) |
| H2 / H1 | H2.CL (CL header survives translation) · H2.TE smuggling a TE header · CRLF injection into translated fields | corpus H2.CL entry | edge negotiates H2 (ALPN evidence), origin H1 — the downgrade seam |
| H1 / H2 | connection-specific header smuggling (Upgrade/Keep-Alive reaching H2 origin) | corpus H1→H2 entry if shipped, else park with resume note | origin announces H2 directly |
| cache in chain | cache-key vs body divergence · delimiter disagreement | cache-playbook organ corpus (CACHE-*) | a cache hop exists in CHAINMAP and its key behavior is baselined |

Rules of the matrix:

1. A class selected WITHOUT a matching pair row is a pre-registered
   EXPERIMENT only if the chain map itself is uncertain (unknown
   framing) — otherwise it is a refused request (wasted bytes).
2. Each selected class names its FIRST probe by corpus ID — byte-exact
   transcription from `references/corpus.json`, never from memory or
   from this file.
3. The one-ambiguity-per-request rule is unchanged: the matrix selects
   ONE class per EXPERIMENT record.

### M3 — the differential confirmation protocol

Per hypothesis (one ambiguity class, one probe):

1. **Conditions, n ≥ 5 each, interleaved** (A,B,A,B… — order effects
   die in interleaving):
   * baseline — canonical benign request for the same endpoint;
   * treatment — the corpus probe, byte-exact;
   * control — the same probe minus ONE byte that restores framing
     agreement (already house doctrine; kept because it proves the
     AMBIGUITY caused any delta, not the connection).
2. **Observation vector per send**: response class bucket
   (status, length bucket [same/±10%/>2×], first-line, body-hash
   class) AND wall-clock time. Both are artifacts.
3. **Confirm rule (all three must hold)**:
   * treatment bucket ≠ baseline bucket in ≥ 4 of 5 runs, AND
   * control bucket == baseline bucket in ≥ 4 of 5 runs, AND
   * no baseline bucket drift across the interleave (else the run is
     void — re-baseline and restart, recording the void).
4. **Timing as escalation only**, with thresholds pre-registered:
   * timing-LEAD: treatment median − baseline median > max(3 ×
     baseline IQR, 2 s);
   * timing-CONFIRM (after response-class or echo graduation):
     treatment median − baseline median > 5 s AND control within
     baseline IQR;
   * medians and IQRs are reported, single shots never.
5. **Error-echo oracle** (the cheap first escalation): a treatment
   response that quotes the smuggled prefix (a length echo, a parse
   error naming the second request) is response-class evidence at
   zero extra delay cost — read the BODY before reaching for the
   40-second habit.

### M4 — the escalation ladder and the ceiling

Each step is entered ONLY when the previous one is inconclusive
(recorded as such):

```
1. error-echo        (body evidence, cheap, fast)
2. response-class    (bucket differential, M3 rule)
3. short timing      (2–5 s differential)
4. long timing       (30–40 s differential — the expensive habit, demoted to last)
5. poisoning demo    (ONLY with operator-owned victim session + canary marker
                      in the smuggled prefix; a second operator-owned fetch
                      reads the poisoned entry back)
```

The canary marker (a distinctive header/path unique to this
EXPERIMENT, from the canary doctrine) is what converts "something was
poisoned" into "MY smuggled bytes were served to MY fetch" — the
victimless differential at full strength.

**Ceiling statement, mandatory in the report**: proven = the parser
pair disagreed on THIS byte sequence, n_runs and deltas attached;
demonstrated impact = the escalation level actually reached. "H2.CL
reached the origin queue (level 3)" is a different finding than "cache
poisoning served to an operator-owned fetch (level 5)" and is reported
as such — never rounded up.

## 2. Falsifiers — what would prove this method wrong

* The CONTROL also shows the delta → the ambiguity was not the cause;
  the hypothesis dies (and the control caught it — that is its job).
* A delta appears in 1 of 5 treatment runs with no error echo and no
  control movement → jitter artifact: LEAD, not a finding; the n_runs
  floor exists exactly here.
* The probe fails for a documented corpus failure mode (per-request
  connections, intermediary re-framing, refusal posture) → the seam is
  UNTESTED, not disproven; the failure mode entry is cited in the
  park note.
* Two hops in CHAINMAP cannot be given product/version evidence →
  treat the seam as unknown-framing: matrix row 1 classes run as
  EXPERIMENTS with framing explicitly uncertain, and the report says
  which hop could not be pinned.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§2 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
Kettle's published art is real, but it is told through Burp Suite and
one-shot narratives. This module extracts what is tool-agnostic in it,
names the mechanical weaknesses, and ships the executable protocol:
chain map with a schema, a parser-pair × ambiguity-class selection
matrix, and a differential confirmation protocol with thresholds. An
agent that has never opened Burp must run this at the lineage's
precision.

## 3. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Delivery is Burp-centric — Repeater, Turbo Intruder, the Smuggler extension are the verbs | The method does not transfer. An agent with `http_probe` and raw sockets inherits the posture but not the procedure; "open Repeater" is not a step |
| W2 | Probe-first: the labs jump straight to sending known CL.TE / TE.CL templates | Spraying classes at a chain that cannot disagree that way burns requests, alerts WAFs, and leaves the seam untested while looking busy. The chain map (WHO parses, WHICH versions) must select the class, not habit |
| W3 | The timing oracle is the default confirmation — hold the backend 30–40 s and watch | Slow, noisy, and inconclusive on jittery edges: a cold cache or a queued worker can fake a one-off delay. Error-echo and response-class oracles confirm faster and cheaper; timing is escalation, not default |
| W4 | Single-shot narrative — "the request smuggled" reported from one send | No n_runs, no jitter baseline, no control condition. A flaky backend reads as a desync exactly once, then never again — and the writeup still says confirmed |
| W5 | Poisoning demos that borrow third-party users as the victim | The victim must be operator-owned — the rule is in our canary doctrine precisely because the published demos needed it written down |

## 4. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The method stated in bytes and steps, tool-agnostic | This module; probes come byte-exact from `references/corpus.json` (never hand-typed) |
| U2 | Map the parsers WITH versions before selecting a class | **M1** — the CHAINMAP record schema + evidence commands |
| U3 | Class selection by parser PAIR, not by habit | **M2** — the selection matrix (pair × class → probe + preconditions) |
| U4 | Confirmation as a differential with distributions | **M3** — baseline/treatment/control, n ≥ 5, medians + IQR, bucket rules |
| U5 | A written victim rule and an escalation ladder with gates | **M4** — operator-owned victims, canary markers, each escalation earned |
