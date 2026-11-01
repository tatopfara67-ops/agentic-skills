# mindset.md — the Tomnomnom decision logic, translated

## 1. The mind, as observed in the sources

* **The tool is a stage, not a product.** The canonical toolset
  (assetfinder → httprobe → gf → meg, plus gron and qsreplace as
  data plumbers) has almost no configuration surface. Each binary
  reads stdin or a file, writes lines to stdout, exits. The user
  composes; the tool never guesses. Daniel Miessler's primer
  captures it: "tools with the Unix philosophy of doing one specific
  thing really well."
* **Passive enumeration is the free tier.** assetfinder pulls
  together CT logs and other passive sources — names you did not
  have to ask the target for. The expensive question (is it alive?)
  is asked only about names that already survived the free tier.
* **Cheap defaults are a philosophy.** httprobe defaults: a small
  port set, one request per host, no crawling. The default IS the
  discipline: liveness is not a scan.
* **Expertise encoded as data.** gf ships pattern FILES —
  `gf xss`, `gf redirect`, `gf sqli` — curated regex packs per
  vulnerability class. The expert's pattern intuition lives in a
  versioned file, not in a script nobody else can run. This is the
  single most portable idea in the lineage: knowledge as data
  composes; knowledge as code rots.
* **Diff beats absolute.** meg fetches one path across many hosts
  and lets you compare responses. One host's response means nothing
  alone; against ninety siblings it means either "normal" or "the
  interesting one." The pipeline manufactures comparison context.
* **Reshape data, don't parse it.** gron "makes JSON greppable" —
  flatten the structure so the NEXT standard tool can consume it.
  The alternative — a bespoke parser per task — is exactly the
  unshareable script the doctrine rejects.
* **Sampling when full coverage is a lie.** In his talks and AMAs,
  Hudson repeatedly pushes back on "scan everything": when the asset
  count outgrows the budget, sample and say so, rather than pretend
  coverage that did not happen. (The arsenal's equivalent is R1 park
  notes + cap bits.)

## 2. The translation table (tools → organ behavior)

| The lineage's tool | The arsenal's stage |
| --- | --- |
| assetfinder (passive sources) | `ct_subdomains` + `dns_resolve`; records cite sources |
| sort -u (dedupe) | an explicit recorded stage: count before/after |
| httprobe (liveness, minimal) | one `http_probe` per host; defaults over tuning |
| meg (uniform path × hosts, diff) | `content_discover` calibrated walks; uniform-path probe loops |
| gf (pattern packs as data) | versioned wordlists/regex packs per VRT class |
| gron (reshape for the next tool) | compact views; artifacts reshaped on disk, not bespoke parsers |
| pipes on the CLI | the ledger as chain of custody between stages |

## 3. The stage contract (this organ's unit of thought)

```
stage: <name>
question: <the ONE question it answers>
input:  <artifact + R-NNN of the stage that produced it>
output: <records written; park note for what it drops>
budget: <probes it is allowed to spend>
```

A stage card that cannot state its ONE question is two stages or
zero stages — split it or delete it.

## 4. Failure modes this organ exists to kill

* The mega-tool that enumerates, probes, crawls, and "analyzes" in
  one call — unarguable, unreproducible, uncomposable.
* Probing a list that was never deduped (paying twice for the same
  name; inflating the exposure denominator).
* Depth before liveness: crawling hosts that never answered.
* Inline regex folklore: the "interesting pattern" that lives in one
  probe call and dies with it — instead of a versioned pack the next
  engagement reuses.
* Pretended coverage: "we swept everything" when the cap bit said
  otherwise. The lineage says sample and say so; the spine says park
  and say so. Same law.

## 5. What the engine already enforces (do not re-implement)

* Scope gating before any active stage (R0).
* Calibration before sweep claims (`content_discover`'s control
  requests).
* Cap bits and park-note discipline (R1/R7).
* Compact tool outputs — bodies on disk, views in context — which is
  gron's lesson already implemented: keep the pipeline's cargo
  greppable.
