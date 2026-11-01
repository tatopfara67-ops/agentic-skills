# sources.md — the lcamtuf lineage, verified

## Primary sources (consulted in full)

* **Michal Zalewski, AFL design document —
  lcamtuf.coredump.cx/afl/technical_details.txt** — read in full.
  Everything quoted in the mindset module comes from this text:
  tuple coverage and the 64KB map, bucketed hit counts (1, 2, 3,
  4-7, 8-15, 16-31, 32-127, 128+), the guided-vs-blind comparison,
  "not a greedy genetic algorithm" and 75-99% skip probabilities,
  corpus culling by latency+size ("usually 5-10x smaller"),
  deterministic-then-random stages, calibrated timeouts and tarpit
  rejection ("improve coverage by 1% while being 100x slower"),
  trimming/afl-tmin with alphabet normalization, and the closing
  "collection of hacks… simplest, most robust way" philosophy.
* **google/AFL repository README (github.com/google/AFL)** — "a
  brute-force fuzzer coupled with an exceedingly simple but
  rock-solid instrumentation-guided genetic algorithm."

## Secondary sources (consulted)

* Wikipedia (American Fuzzy Lop; Michal Zalewski) — biographical and
  release framing: Polish security researcher, AFL released 2013,
  genetic algorithms for coverage.
* AFL++ project pages — the AFL lineage and its continuation by the
  community.
* Academic layer: "Dissecting American Fuzzy Lop: A FuzzBench
  Evaluation" (ACM CCS workshop publication) and the AFL-family
  literature (FuzzBench, etc.) — consulted for the standing of AFL's
  design in the research community; the organ cites design, not the
  benchmark numbers.
* moyix's "Fuzzing with AFL is an Art" (2016) — "a powerful
  coverage-guided fuzzer developed by Michal Zalewski (lcamtuf) at
  Google."
* lcamtuf.coredump.cx (current) — his later work (books, hardware);
  confirms the author's continuing public-engineering record.

## Attribution notes

* Zalewski's exact Google title changed over the years; the public
  record (HN threads, profiles) supports "Google security
  engineering lead"-level attribution, which is how the SKILL.md
  phrases it. No finer title is claimed.
* Browser-security-era lcamtuf work (mangleme lineage, "Browser
  Security Handbook") is part of the lineage's history but is NOT
  cited as a consulted source here and informs nothing specific in
  this organ — flagged honestly.

## What this organ does NOT include

* No AFL code is redistributed; the instrumentation pseudocode is
  described at the design level only, as published in the design doc.
* No claim about AFL++ specifics beyond its existence as the
  community continuation.

## Confidence

High — the governing design document was read in full and every
translated law traces to a specific passage in it.
