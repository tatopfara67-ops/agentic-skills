# The method upgrade — critiquing the callback-everywhere habit, shipping the executable channel hunt

The charter's A16 charge: **a lineage named is not expertise delivered.**
ssrf-playbook, like injection-lab, was forged against an industry
default rather than a single master: the Collaborator-era habit of
pasting an out-of-band URL into every parameter and calling any DNS
ping "SSRF". That default has documented floors; they are critiqued
mechanically here, and the replacement ships as executable protocol:
a per-parameter channel hypothesis table, a channel-proof ladder,
a parser-differential map, a cloud-metadata decision table, and an
impact ceiling that refuses gossip. An agent with no Collaborator
subscription must run this better than the habit it replaces.

## 1. The critique — five mechanical weaknesses of the callback-everywhere habit

| # | What the habit shows (documented) | Why it is weak as a shipped method |
| - | ---------------------------------- | --------------------------------- |
| W1 | Canary-first reflex — the interaction payload goes into every parameter before anything is known about the parameter | The hit tells you SOMETHING fetched your URL, and nothing else: which parameter, which parser, which hop — all unknown; meanwhile the reflex burned the entire surface's budget in one pass |
| W2 | Channel conflation — DNS resolve, HTTP fetch, and metadata read-back all reported as "SSRF confirmed" | They are three different strengths of evidence; conflating them makes a DNS cache miss read like cloud-metadata compromise and makes real findings un-rateable |
| W3 | Parser disagreement narrated per-bug — each public writeup re-discovers that the client, proxy, and origin normalize the URL differently | The disagreement is a MAP-able property of the chain (which hop re-parses, which normalizes, which resolves), knowable quietly per hop; per-bug re-discovery is the same floor as desync-hunter's W2, one layer up |
| W4 | Cloud metadata URLs typed from memory | Endpoint drift (IMDSv2 tokens, hop limits, header requirements, GCP/Azure header names) — hand-typed URLs produce false NEGATIVES that read as "metadata secured", the worst failure class a hunter can ship |
| W5 | Impact claimed without read-back — "we got a callback" escalated to credentials/RCE in prose | Without a second-stage read-back under operator-owned rules, impact is gossip; the escalation is exactly where reports die in triage |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Per-parameter hypotheses registered before any canary fires | **M1** — the channel hypothesis table |
| U2 | Channel strength as a ladder with separate records | **M2** — the channel-proof ladder |
| U3 | The chain's parse behavior mapped, hop by hop | **M3** — the parser-differential map |
| U4 | Metadata endpoints as versioned data with required headers | **M4** — the cloud-metadata decision table |
| U5 | Impact = read-back, never the callback | **M5** — the impact ceiling |
| U6 | Byte-exact probes with sources and failure modes | `references/corpus.json` (SSRF-001…010, SSRF-010 wired to the http_probe canary) — consumed, never re-typed |

## 3. The executable protocol — M1 through M5

### M1 — the channel hypothesis table (register before firing)

For every parameter that carries a URL-ish shape (full URLs, paths,
hostnames, redirect targets, webhook fields, import/export refs),
register one EXPERIMENT row BEFORE any request:

```
SSRF-HYP: param=<webhook_url> shape=absolute-url expected_chain=
  client[app]->validator?[?]->fetcher[backend] fetch_class=server
  candidate_hops=<validator-reject|fetcher-fetch|redirect-follow>
```

The shape class selects the corpus probe family (absolute-form,
scheme-relative, redirect-based, gopher/file oddities per corpus
entries — byte-exact). A parameter with no URL-ish shape on record is
NOT canaried: the reflex is dead, the table decides (the W1 floor).

### M2 — the channel-proof ladder

Each rung is a SEPARATE record; the ladder decides what "confirmed"
means:

| Rung | Evidence | Record class | What it proves |
| ---- | -------- | ------------ | -------------- |
| 1 | DNS query for the operator-owned label at the collector | CHANNEL-DNS | a resolver touched the label — weak fetch-side evidence |
| 2 | Full TCP/HTTP fetch observed (collector log: method, path, UA) | CHANNEL-HTTP | a full HTTP client on the target fetched attacker-influenced input — the real SSRF baseline |
| 3 | Second-stage read-back: the fetched resource's CONTENT observable (length/timing reflected in the app's response, or stored artifact) | CHANNEL-READBACK | the channel is two-way enough to matter — the impact gate opens |
| 4 | Cloud metadata content retrieved (M4 table) under operator scope | CHANNEL-METADATA | the maximal class; everything below it is capped accordingly |

Rules: rung 1 alone is a LEAD; rung 2 is the minimum a report calls
"SSRF confirmed"; rung 3+ is where severity starts. Reports citing
rung 1 as impact FAIL this organ's gate (the W2 floor, made a table).

### M3 — the parser-differential map (per hop, quietly)

Which hop re-parses or re-normalizes the URL? Two probes per hop
boundary, n ≥ 3, interleaved:

1. **Case/encoding pair**: `HTTP://EXAMPLE.com` vs
   `http://example.com` (plus `%2f` vs `/` where the corpus carries
   the entry) — divergence in what the collector SEES (case folded?
   path normalized? port defaulted?) names WHICH hop normalized.
2. **Redirect-follow pair**: a URL that redirects (operator-owned,
   302 to the collector) vs the direct collector URL — a fetch when
   only the redirect version fires marks the fetcher as the
   redirect-following hop (the chain-architect L-link habit, applied
   per hop).

The completed map is a CONTROL record the ceiling cites: "fetcher
normalized case, validator did not" is a FACT, not a story (the W3
floor).

### M4 — the cloud-metadata decision table

Metadata probing uses the versioned table — entries as corpus probes,
byte-exact, never from memory:

| Cloud | Probe class | Mandatory elements |
| ----- | ----------- | ------------------ |
| AWS IMDSv1 | `http://169.254.169.254/latest/meta-data/` | none (legacy; presence itself is a hygiene finding) |
| AWS IMDSv2 | token PUT first, `X-aws-ec2-metadata-token` header, `ttl` discipline | PUT with token request, then GET carrying it — two-step is the probe, one-shot GETs produce false negatives |
| GCP | metadata endpoint with `Metadata-Flavor: Google` | header REQUIRED — without it the probe proves nothing (the W4 floor's textbook case) |
| Azure IMDS | with `Metadata: true` | header REQUIRED + resource parameter discipline |
| Container-native | `http://127.0.0.1:<docker/k8s api ports>` per corpus entries | loopback class — network namespace decides reachability; record the namespace FACT |

Every metadata attempt records cloud class + exact probe + response
class. A 403/timeout is recorded as "endpoint guarded under THIS
probe" — never as "metadata secured" (probe discipline outranks the
conclusion; the corpus's failure modes section exists for exactly
this).

### M5 — the impact ceiling

```
CEILING: channel=<ladder rung achieved> map=<M3 FACTs cited>
  read-back=<what content class was observable, or NONE>
  metadata=<class + response class, or NOT-PROBED-because-scope>
  impact-claim: capped at <rung's permitted class>
```

Permitted claims by rung: rung 2 → "server-side fetch of
attacker-influenced URL, scope <surface>"; rung 3 → "content-bearing
SSRF, read-back of <class>"; rung 4 → "cloud metadata access of
<exact response class>". Anything above the rung — credentials
implied, RCE hinted — is REFUSED in this organ's report and handed to
chain-architect as a chain CANDIDATE with the rung as link evidence
(the W5 floor, made a gate).

## 4. Falsifiers — what would prove this method wrong

* The collector sees DNS but the map shows the label never left the
  client (pre-resolved by the browser/app) → rung 1 was client-side
  gossip: the hypothesis is re-registered as client-reach, target
  exonerated on record.
* Two hops in the map produce IDENTICAL normalization on the
  case/encoding pair → the map cannot distinguish them: record the
  ambiguity, downgrade hop-attributed claims to chain-level.
* A metadata probe with the mandatory header returns 403 but the
  corpus's IMDSv2-class entry also documents token-PUT success on
  other targets → the 403 is THIS probe's result only: "guarded under
  this probe" — the failure-mode entry is cited, the conclusion
  stays bounded.
* The read-back observation flips with collector load (n = 3 unstable)
  → rung 3 evidence is jitter: downgraded to rung 2 until re-run
  stable.

## 5. Worked micro-example (numbers consistent, incident fictional)

Parameter `webhook_url` (absolute-URL shape, registered M1). Ladder:
rung 1 DNS label seen; rung 2 collector logs full GET with the
backend's UA — SSRR baseline confirmed (rung 2). Map: case-pair
divergence shows the VALIDATOR folded case but the collector saw the
original path → fetcher normalizes late; redirect-pair fires only on
the redirect version → fetcher follows redirects (both FACTs).
Metadata: scope covers AWS target class → IMDSv2 two-step probe
performed, token PUT 403, GET 403 — recorded "guarded under this
probe", corpus IMDSv2 failure-mode entry cited. Rung 3: webhook
echo page reflects the fetched banner length class 4/5 → read-back
confirmed. Ceiling: content-bearing SSRF, read-back of length class;
credentials/RCE handed to chain-architect as candidate C-021 with
rung-3 link evidence. No gossip in the report.
