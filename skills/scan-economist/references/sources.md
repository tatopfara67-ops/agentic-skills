# sources.md — the Fyodor lineage, verified

What was actually consulted while distilling this organ, per the
assimilation doctrine (complete sources, attributed, no fabrication).

## Primary sources (consulted in full)

* **Fyodor, "The Art of Port Scanning", Phrack Magazine Volume 7,
  Issue 51, article 11 (September 1997).**
  http://phrack.org/issues/51/11 — the founding paper, read in full:
  technique tradeoffs, dynamic delay, retransmission, bounded
  parallelism ("more than 18 or so" hurting fast networks), dead-host
  economics, /etc/services priors, and the original nmap source.
  Every quote in the mindset module is from this text.

## Primary sources (partially consulted — free online edition)

* **Gordon Lyon, *Nmap Network Scanning* (2009), free online edition
  at nmap.org.** Reference structure confirmed (host discovery, port
  scanning, service/version detection, NSE, timing/performance);
  paywalled print chapters (firewall/IDS evasion depth) were not
  consulted and are not claimed.

## Secondary sources (consulted for context)

* nmap.org project pages and the Nmap Scripting Engine documentation
  structure (script categories, version detection feeding targeted
  scripts) — read as documentation, not as lineage claims.
* Catalog/aggregator listings of the book (Google Books, Slideshare
  summaries) — used only to confirm publication facts.

## What this organ does NOT claim

* No Nmap code, NSE scripts, or nmap-services data is redistributed
  or embedded.
* The 2009 book's paid chapters are behind a paywall; this organ does
  not cite them.
* Modern Nmap feature specifics (version detection internals, OS
  fingerprinting databases) are referenced only at the level of the
  public documentation.

## Confidence

High for the 1997 decision logic (full primary text); medium for the
book-era refinements (free-edition sections only). Where the two
differ, the 1997 paper's economics are the organ's backbone and the
modern behavior is treated as implementation detail.
