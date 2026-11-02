# Reference — Sources (lineage verification)

> Part of **cache-playbook v1.0.0** (package architecture).
> **Load when:** the lineage claim needs its citation; the attribution
> boundary (what is Gil's, what is Kettle's, what is this bundle's)
> needs restating. Authoritative rules live in
> [`../SKILL.md`](../SKILL.md) — **SKILL.md wins** on any conflict.

---

## 1. The lineage, verified

**Omer Gil.** *Web Cache Deception Attack* — the Black Hat USA 2017
whitepaper (`blackhat.com/docs/us-17/.../us-17-Gil-Web-Cache-Deception-Attack-wp.pdf`),
slides on record (Scribd archival copy consulted); the discovery and
industry coverage date to February 2017 (BleepingComputer, Feb 28,
2017, "Web Cache Deception attack tricks servers into caching pages
with personal data", naming Gil as the Israeli security researcher
who discovered it). At the time of the talk: PT team leader at EY. The
class: a path the cache classifies as static while the origin serves
the authenticated page beneath it. Distilled here as the
path-confusion half of this organ's doctrine.

**James Kettle — the cache corpus specifically.** *Practical Web
Cache Poisoning: Redefining "Unexploitable"* — Black Hat USA 2018
(also ekoparty 14, 2018; catalog on record via conference indexes).
*Web Cache Entanglements: Novel Pathways for Poisoning the Cache* —
PortSwigger Research, 2020 (portswigger.net/research/web-cache-
entanglement). The corpus built the unkeyed-input methodology and the
cache-key/display-key discrepancy craft. **Attribution boundary, on
record:** Kettle's *desync* corpus anchors desync-hunter (tier 6);
this organ cites his cache works only. The lineage registry carries
this as an explicit correction field — two organs, one author, two
distinct corpuses, kept distinct.

**The academic anchor.** Mirheidari, Arshad, Onarlioglu, Crispo,
Kirda, Robertson — *Cached and Confused: Web Cache Deception in the
Wild*, USENIX Security 2020 (usenix.org/system/files/sec20-
mirheidari.pdf): the large-scale measurement of the class in the
wild, and the delimiter-based path-confusion variations this organ's
sweep family builds on. Cited as measurement and delimiter source,
not as method donor.

**The research wave.** Martin Doyhenard (PortSwigger) — *Gotta Cache
'em All: Bending the Rules of Web Cache Exploitation*, DEF CON 32
(2024): the delimiter-methodology expansion (cataloged via conference
indexes; its own citations name Gil 2017, Kettle's Entanglements, and
USENIX'20 as its starting points — the same chain this organ rests
on). Real-world case literature (public write-ups of cache-deception
and poisoning bounties) is consulted per-engagement, never
vendored.

## 2. What this organ adds on top

The second-parser doctrine statement, the nonce-path victimless proof
law (SKILL.md §5.2 — poisoning proofs run only under keys containing
a fresh random nonce), the operator-as-victim deception law, the purge
ledger line, and the key-map-as-dossier-table procedure are this
bundle's own contributions. Gil, Kettle, Mirheidari et al., and
Doyhenard published none of those rules; they are the arsenal's
evidence law applied to the cache surface.

## 3. Verification record

| Claim | Source | Status |
| --- | --- | --- |
| Gil: class discovered + BH USA 2017 whitepaper | blackhat.com docs (us-17), slides archive | verified |
| Gil: Feb 2017 disclosure, EY PT team leader | BleepingComputer Feb 28 2017; talk slides | verified |
| Kettle: Practical Web Cache Poisoning BH USA 2018 | conference indexes (BH USA 2018, ekoparty 14) | verified |
| Kettle: Web Cache Entanglements 2020 | portswigger.net/research | verified |
| Mirheidari et al.: USENIX Security 2020 | usenix.org/system/files/sec20-mirheidari.pdf | verified |
| Doyhenard: DEF CON 32 (2024) delimiter methodology | conference catalog | verified |
