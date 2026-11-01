# asymmetry-catalog.md — the ambiguity grammar of desync-hunter

Load when designing an ambiguity hypothesis. Every entry: the two
parsers that disagree, the ambiguity shape, the predicted observable,
and the one-byte control that restores agreement.

## 1. The Parsing-Chain Map (template, a FACT record set)

```
client -> [ CDN/WAF ] -> [ HTTP/2 terminator ] -> [ LB ] -> [ origin ]
           Server: ...      :protocol h2            Via: ...   X-Powered-By: ...
```

Record per hop: product/version evidence (headers), protocol spoken
upstream/downstream, which hop rewrites URLs or headers. The SEAM
LIST is every adjacent pair. An ambiguity matters only at a seam
where the two sides parse differently.

## 2. Ambiguity Classes (HTTP/1.1 inheritance)

| Class | Shape | Frontend reads | Backend reads | Control byte |
| --- | --- | --- | --- | --- |
| CL.TE | both CL and TE headers | CL | TE | remove TE → agreement |
| TE.CL | both, opposite preference | TE | CL | remove CL |
| TE.TE | TE with obfuscated value | junk→ignore | chunked | de-obfuscate the value |
| dup-CL | two CL values, 1 apart | first | second | make values equal |
| header-name oddity | space/underscore/dot variants | forwarded as-is | dropped or re-named | canonical name |
| obs-fold | folded header value line | continued value | new header | unfold to one line |
| absolute-form | `GET http://host/path` | routed by host | path parsed oddly | origin-form `/path` |
| non-standard method | `GETS`, `\tGET` | passed | rejected/interpreted | canonical `GET` |

## 3. Ambiguity Classes (HTTP/2 era)

| Class | Shape | Divergence |
| --- | --- | --- |
| H2.CL | :content-length on a stream + framing | terminator's CL vs origin's re-serialized body |
| H2.TE | transfer-encoding smuggled through H2 | hop re-serializes into HTTP/1.1 chunked |
| name case/order | lowercase h2 names re-cased upstream | cache/WAF match rules vs origin routing |
| pseudo-header abuse | :path with odd characters | frontend normalize vs backend route |
| content-type divergence | same body parsed twice differently | validator vs business logic |

## 4. Detection Matrix (evidence oracles, weakest→strongest)

1. **Timing (LEAD only).** Response-time divergence between treatment
   and control — backend connection held open ≈ desync candidate.
   Requires ≥ 5 runs per side with medians reported; NEVER confirms
   alone.
2. **Response-class differential.** Treatment returns class A
   (e.g. 404 of the NEXT request) where baseline/control return B —
   the smuggled prefix surfaced.
3. **Echo capture.** A distinctive self-marked canary path
   (`/canary-<random>` existing nowhere) surfacing in a subsequent
   request's response — the strongest passive confirmation.
4. **Poisoned fetch.** Operator-owned victim session fetches content
   shaped by the treatment request — impact-grade proof, run once.

## 5. Hypothesis Pre-Registration Template

```
DSYNC-<k>: seam = <hopA> vs <hopB> (versions)
  ambiguity: <class> — exact bytes in artifact <path>
  frontend prediction: <parse/behavior>
  backend prediction: <parse/behavior>
  oracle: <timing|response-class|echo-capture|poisoned-fetch>
  control: <the one byte that restores agreement>
  rate: one request / 10 s; n_runs >= 2 (>=5 if timing oracle)
```

## 6. Cautions carved from the lineage

* Frontends that timeout slowly make timing oracles noisy — always
  pair with response-class evidence.
* Some seams only desync the SECOND request on the connection —
  the differential belongs to the follow-up request, recorded as
  its own EXPERIMENT.
* A WAF that resets connections on ambiguity is an engagement fact
  (report it), not an invitation to escalate volume.
* Web-cache-deception shapes (path/semantics divergence between
  cache key and origin authorization) are a sibling class: record
  as `cache-key divergence`, proof = operator-owned victim fetch
  retrieving non-cacheable personal content from the cache.
