# sources.md — the Orange Tsai lineage, verified

What was actually consulted while distilling this organ, per the
assimilation doctrine (complete public sources, attributed, no
fabrication, no proprietary content).

## Primary sources (public record, consulted)

* **DEVCORE, "ProxyLogon: The Most Exploit-worthy Vulnerability in
  Recent Exchange History" (2021), blog.devco.re.** The published
  chain anatomy: pre-auth SSRF combined with post-auth arbitrary-file
  write, composed into unauthenticated RCE; the Pwn2Own chain that
  won the full award. Consulted for the chain DESIGN pattern only —
  no exploit code reproduced or embedded.
* **Orange Tsai, "A New Era of SSRF — Exploiting URL Parser in
  Trending Programming Languages" (DEF CON 28 / DE1CTF 2020).** The
  parser-confusion primitive family: identical URLs interpreted
  differently by components — the canonical "hunt the seams" source.
* **Orange Tsai, "Confusion Attacks: Exploiting Hidden Semantic
  Ambiguity in Apache HTTP Server" (OrangeCon, 2023+).** Semantic
  ambiguity between modules as a validation-bypass primitive class.
* **Orange Tsai, "A 3-Year Tale of Hacking a Pwn2Own Target"
  (HEXACON 2023).** The multi-year, architecture-first campaign
  posture: depth over breadth on a single complex target.

## Secondary sources (context only)

* Public coverage of the DEVCORE Pwn2Own Exchange result (award
  announcement, $200,000 team award) — used to confirm the event
  facts, not methodology.
* blog.orange.tw index and DEVCORE advisory pages — publication
  facts and talk titles verified against them.

## What this organ does NOT claim

* No DEVCORE exploit code, proof-of-concept requests, or advisory
  specifics are redistributed; only the public method shape
  (compose low primitives by reading architecture) is distilled.
* No claim that Orange Tsai endorses, uses, or knows about this
  bundle. The lineage is an honest study of published methodology.
* The operator's brief described the doctrine in the operator's own
  words ("find 3-4 small harmless-seeming gaps, chain them into a
  critical"); the public record above was matched to it.

## Confidence

High. The chain-design pattern is stated explicitly and repeatedly
across the primary sources; ProxyLogon is among the most documented
public chain demonstrations in existence.
