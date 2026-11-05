# operator-os.md — the Kettle runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS, not when it is planned. The
> doctrine (SKILL.md §3) states the posture; the M-protocol
> (references/method-upgrade.md) states the procedure; THIS module is
> the runtime — how the agent notices, thinks, behaves, and scripts
> while executing them, characteristic of James Kettle's documented
> craft:
> re-read the spec as a hypothesis, map the parsers before the
> payloads, one ambiguity per request, and never mistake a slow
> response for a finding.

## 1. The thinking framework — decision rules

R1 **Spec disagreement is the hypothesis, not the bug.** If the
documentation says the chain behaves way A, the first thought is not
"what payload breaks it" but "which two components read these bytes
differently?" — write the predicted frontend verdict and the predicted
backend verdict BEFORE the request exists. *From:* the lineage's
research posture, "The Sequel Is Always Worse" (Black Hat USA 2021):
the desync class renews with every protocol generation because the
division of interpretive labor never disappears.

R2 **Versions select the class.** Never choose a technique by habit;
choose it by the parser-pair row in the M2 matrix. "nginx" is not
"nginx/1.24.0" — the pair of pinned versions decides which ambiguity
classes are even admissible.

R3 **One ambiguity, one request, one ledger row.** If a request
carries two deviations, the agent cannot attribute the delta. Split
into two hypotheses, two EXPERIMENT records.

R4 **Timing is a lead; the body is the evidence.** Before reaching for
a 40-second timeout oracle, READ THE RESPONSE BODY — an error echo
that quotes the smuggled prefix is response-class evidence at zero
delay cost. *From:* the M3 error-echo oracle — the cheap first
escalation.

R5 **Bytes are the artifact.** A finding is the exact request bytes and
both divergent responses, hashed and ledgered. "It hung a bit" is not
a thought worth keeping.

R6 **The victim is always you.** Any poisoning demonstration runs on
operator-owned sessions with a canary marker; production traffic as
victim is not a finding, it is an incident.

R7 **A negative with a documented failure mode is UNTESTED, not
disproven.** Check the corpus entry's failure modes before closing any
hypothesis — per-request connections and intermediary re-framing leave
the seam untested.

### The opening ladder — where Kettle's candidates come from

The rules above govern the differential once a seam is suspected;
the ladder produces the seam candidates themselves — the parsing-chain
first perception (the 2019 research posture: map the chain and its
verdicts BEFORE any ambiguity craft; the class renews every protocol
generation because interpretive labor never disappears) made runnable
as questions. Rungs one to three are quiet reads and malformed-input
verdicts — no CL/TE ambiguity bytes; rungs four and five select and
gate. Rows out; the anomaly budget unspent until S4's matrix selection.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | Which hops stand between client and origin — and what does each ADMIT it is? | the chain census: ordered headers, Server/Via/X-Cache, per-hop versions — every hop pinned or framing=unknown | T1's hop-fingerprint discipline; the parsing-chain-first posture (BH USA 2019, sources.md) |
| G2 | Where does the chain change protocol or framing? | framing seams: h2-negotiated edges over H1 origins, H2-only paths, protocol translations — where the interpretive labor splits | "HTTP/2: The Sequel Is Always Worse" (BH USA 2021 — H2.CL/H2.TE/name-case; sources.md) + T2's ALPN check |
| G3 | Which parser pairs already DISAGREE on malformed input? | verdict divergence: error-page ownership per hop — two different answers to the same malformed request = the seam exists before any CL/TE craft | T3's error-page ownership + R1's spec-disagreement rule |
| G4 | Which ambiguity classes does the pinned pair make admissible? | matrix selection: CL.TE / TE.CL / TE.TE / H2.CL / H2.TE / name-case × the pair of pinned versions — admissibility read from the census, not from habit | R2 + the M2 selection matrix (method-upgrade.md) |
| G5 | Whose edge is it — and who else stands on it? | scope-boundary rows: shared CDN/edge ownership, other-tenant exposure — the seam priced by blast and gated by ownership | the scope-law row (R0 on the SEAM's owner — behavioral protocol row 1) |

Ranking rationale: candidate priority = observed disagreement ×
admissibility × blast. A pair already disagreeing on malformed input
outranks a merely-versioned pair — an observed verdict divergence beats
an inferred matrix row; an h2-downgrade seam outranks an H1-only chain
for class breadth (H2.CL + name-case ride the same seam); duplicate-CL
and CL.0 rows rank by intermediary prevalence; a shared edge ranks by
other-tenant exposure but is gated FIRST by ownership — an unowned seam
parks, it never probes (R0). Rows out; no ambiguity bytes sent.

Generation falsifier: an in-scope chain where the ladder yields zero
admissible seam classes means the chain census is missing a rung for
that framing — a QUIC/H3 fronting, a non-HTTP intermediary, a
translation the CHAINMAP cannot type; the census is re-read, the rung
is written with its grounding row. The chain is never excused as
"desync-proof" at generation time: that verdict belongs to the S5
three-part differential, never to the ladder.

#### The ladder's payload kit — the ambiguity-class probe rows (customize before use)

Generation writes rows; these are the probe classes the differential
later loads — byte-exact bytes stay versioned in corpus.json (R5;
every corpus entry carries probe, oracle, failure modes, and source):

| Kit row | The ambiguity it names | Corpus entry |
| --- | --- | --- |
| CL.TE differential row | Content-Length read by the front, Transfer-Encoding by the back — non-blind verdict pair | DS-001 |
| CL.TE timeout row | the blind lead: CL kept, TE body held open — wall-clock oracle only | DS-002 |
| TE.CL differential row | the inverted disagreement — non-blind | DS-003 |
| TE.CL timeout row | the inverted blind lead | DS-004 |
| TE.TE obfuscation row | disagreement induction — obfuscated framing both must still agree on | DS-005 |
| duplicate-CL row | two Content-Length values where intermediaries differ in precedence | DS-006 |
| CL.0 row | browser-powered desync — the request that ends where the parser thinks it doesn't | DS-007 |
| H2 downgrade row | H2.CL / H2.TE — the framing seam the downgrade creates | DS-008 |
| poisoning proof row | response-queue poisoning, canary-marked, operator-owned — impact only | DS-009 (R6 ceiling) |
| differential harness row | treatment vs control (same bytes minus ONE restoring byte), interleaved A,B,A,B ×5 — the three-part confirm rule | T4 + M3 |

Customization knobs, stated in the plan note: the chain slice (which
hops the census pins — front/origin only vs every intermediary), the
framing profile (H1-only / h2-downgrade / H2-only — which kit rows are
admissible per the M2 matrix), and the pacing budget (one request per
10 s on WAF-hostile targets, the interleave count per hypothesis —
fixed before S5). The matrix mechanics and per-class preconditions
live in method-upgrade.md; the byte-exact probes live in corpus.json.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Scope names only the web app | Verify the seam's owner is in scope (R0 on the SEAM's owner) | Read program scope; if the edge/CDN is shared or unnamed, park with a resume note | Never probe a shared edge on app-only scope |
| Chain unmapped, temptation to send a known CL.TE template | Map first, probe second | Run T1–T4 (below) until every hop is pinned; CHAINMAP rows are FACT records | Refuse the probe-first habit — spraying classes at an unpinned chain burns requests and alerts the WAF |
| A differential appears once in five runs | Jitter until proven otherwise | Record as LEAD; re-run interleaved; check the control condition | Never promote a 1-of-5 delta to CONFIRMED |
| The response is slow but class-identical | Timing is escalation only | Note the wall-clock; escalate per M4 ladder ONLY after error-echo and response-class run inconclusive | Never write "confirmed by timeout" |
| WAF-looking 403/blocked patterns appear | Slow down, do not route around | Drop to one request per 10 s; ghost-crawler posture; note the block as an environment FACT | Never burst, never rotate IPs to force volume through |
| Poisoning possible on operator-owned session | Prove with canary, then STOP | Smuggle a canary-marked prefix; read it back with a second operator-owned fetch; file CANARY record | Never touch, read, or report another user's queued request |
| Two hops cannot be version-pinned | Unknown-framing protocol | Mark framing=unknown in CHAINMAP; run matrix row 1 classes as pre-registered EXPERIMENTS with uncertainty stated | Never guess a version into the record |

Pacing: one ambiguity per 10 seconds on WAF-hostile targets; a full
M3 differential (15 sends, interleaved A/B) is one working unit — do
not start a second hypothesis mid-interleave. Failure reaction: a void
run (baseline drift) is RECORDED as void and re-baselined — the agent
does not quietly discard it.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — hop fingerprint by ordered headers

```bash
# one quiet probe; record headers IN ORDER (header order is a hop signature)
curl -sv "https://<host>/" -o /dev/null 2>&1 | sed -n '/^< /p' | head -20
```

Read-out: the `<` lines in arrival order + Server/Via/X-Cache set →
CHAINMAP hop rows. Gate: every hop in the chain has one row with
product+version evidence or framing=unknown.

### T2 — ALPN / H2-downgrade seam check

```bash
curl -sv --http2 "https://<host>/" -o /dev/null 2>&1 | grep -i alpn
```

Read-out: edge negotiates h2 while origin answers H1 → the H2/H1
downgrade seam exists; matrix row 2 (H2.CL) becomes admissible. Gate:
recorded as a CHAINMAP framing bit, not as a finding.

### T3 — error-page ownership per hop

```bash
# malformed method: WHICH error page answers names WHICH hop terminated it
printf 'GARBAGE / HTTP/1.1\r\nHost: <host>\r\n\r\n' | \
  openssl s_client -quiet -connect <host>:443 -servername <host> 2>/dev/null | head -15
```

Read-out: two different error pages across two probe types = two
parsers disagreeing before any CL/TE craft. Gate: error-page text
hashes go into the hop's evidence field.

### T4 — byte-exact differential runner (treatment vs control)

```bash
# corpus DS-001 as treatment; control = same bytes minus ONE restoring byte
python3 - <<'PY'
import socket, ssl, hashlib, statistics
def send(raw, host, port=443):
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=10) as s:
        with ctx.wrap_socket(s, server_hostname=host) as tls:
            tls.sendall(raw)
            buf = b""
            while True:
                try: chunk = tls.recv(4096)
                except socket.timeout: break
                if not chunk: break
                buf += chunk
    return {"len": len(buf), "hash": hashlib.sha256(buf).hexdigest(),
            "first": buf.split(b"\r\n", 1)[0].decode("latin1")}
# treatment/control byte sequences are transcribed from references/corpus.json
# NEVER hand-typed; interleave A,B,A,B x5 and record every observation vector.
PY
```

Read-out: per-send observation vector (status/first-line, length
bucket, body hash, wall-clock). Gate: the M3 three-part confirm rule —
treatment ≠ baseline in ≥4/5, control == baseline in ≥4/5, no baseline
drift. Single shots never reported.

### T5 — timing harness with pre-registered thresholds

```bash
# medians and IQR only; thresholds decided BEFORE the run
python3 - <<'PY'
import statistics as st
base, treat = [], []   # wall-clock seconds from T4 records
m_b, m_t = st.median(base), st.median(treat)
iqr_b = st.quantiles(base, n=4)[2] - st.quantiles(base, n=4)[0] if len(base) >= 4 else 0
lead = m_t - m_b > max(3 * iqr_b, 2.0)
confirm = m_t - m_b > 5.0
print(f"median_delta={m_t-m_b:.2f}s iqr_base={iqr_b:.2f} lead={lead} confirm={confirm}")
PY
```

Read-out: LEAD vs CONFIRM against the pre-registered thresholds.
Gate: timing alone never CONFIRMs (R4); it escalates only after
response-class or echo evidence.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | scope covers the seam | R0 re-check on the seam's owner | — | owner named in plan note | PLAN |
| S2 | chain unmapped | fingerprint every hop (R2) | T1, T2, T3 | every hop pinned or framing=unknown | FACT (CHAINMAP) |
| S3 | chain mapped | baseline normal behavior: GET /, HEAD /, POST | T4 (canonical forms) | 3 baselines recorded with timing | FACT |
| S4 | baselines stable | select ONE class by matrix row; pre-register hypothesis (R1, R3) | — | predicted verdicts + observable written | EXPERIMENT |
| S5 | hypothesis registered | run interleaved differential (n≥5 each) | T4 | three-part confirm rule evaluated | EXPERIMENT/CONTROL |
| S6 | delta confirmed | read body FIRST; classify seam; state pinning parser versions (R4, R5) | T1 evidence reuse | seam class + versions stated | FACT |
| S7 | confirmation holds | escalate per ladder ONLY if inconclusive; canary demo last (R6) | T5; canary prefix | ceiling statement written | CANARY |
| S8 | impact proven or ceiling reached | exit gate: classes tested, unexplored parked with failure-mode citations (R7) | — | resume note filed | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* The control condition shows the same delta as the treatment → the
  ambiguity was not the cause; the hypothesis dies and the record says
  so (the control's job is to die in your place).
* A confirmed seam whose CHAINMAP rows were written AFTER the probe →
  the run order was violated; the finding is downgraded to LEAD and
  re-run from S2.
* A timing-only "confirmation" found in the report → R4 was violated;
  the auditor gate rejects it.
* Any victim session that is not operator-owned → R6 violation; the
  engagement halts and the record is written to the failure ledger.
