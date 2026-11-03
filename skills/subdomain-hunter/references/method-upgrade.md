# The executable method — M1–M5 for subdomain-hunter

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The lineage critique that
justifies each step (why these phases exist, what was weak in
EdOverflow's takeover corpus) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

### M1 — the fingerprint-registry discipline

1. Every fingerprint consulted is a FACT record: provider, service
   string class, HTTP body signature (hash, first 64 bytes), DNS
   error class, and **the date the entry was last verified against a
   live service**.
2. Freshness gate: an entry verified > 180 days ago is STALE — it may
   still be used, but the finding cites it as "registry-class,
   unverified" and the report says so (the W1 floor).
3. When a live target's response matches a stale entry, the target's
   response itself becomes the new evidence: record it verbatim, and
   the registry gains a re-verified entry (local corpus correction).

### M2 — the dangling differential (dead ≠ dangling ≠ claim-able)

Per candidate record, three classes decided by PROBE, not prose:

| Class | Probe evidence | Ledger verdict |
| ----- | -------------- | -------------- |
| dead | CNAME target NXDOMAIN from ≥ 2 resolvers, stable across TTL window | FACT: dead — hygiene, not a finding |
| dangling | dead AND target zone claimable-class per M1 fingerprint AND takeover service signature observed | FACT: dangling — finding candidate, M3 |
| claim-able | dangling AND the operator's OWN registration/test claim demonstrated end-to-end inside scope rules | CANARY-graded finding — M5 disclosure |

Rules: one class per EXPERIMENT record; claiming "takeover possible"
while sitting on a dangling class is a hypothesis, never a finding;
the claim-able class is entered ONLY with an operator-owned
demonstration (registering a name outside scope is someone else's
law to break — the operator decides, on record).

### M3 — the TTL-aware verification rule

1. Query the candidate from ≥ 2 independent resolvers (system +
   `dns_resolve` external), interleaved, n ≥ 3 rounds spaced by
   min(TTL, 60 s).
2. **Stability rule**: NXDOMAIN (or the dangling signature) must hold
   in ≥ 5 of 6 queries across resolvers AND rounds. A flip marks the
   record resolver-volatile → verdict COARSE, quoted with its error
   bar (the W3 floor).
3. TTL arithmetic rides in the record: `ttl=300 observed-3600s-ago`
   means the negative cache has long expired — the NXDOMAIN is the
   authoritative state, not a cache ghost.
4. Serial/SOA check where the zone is visible: `SOA serial` recorded
   before and after the verification window; a serial bump between
   rounds means the zone CHANGED during testing — void and re-run.

### M4 — the chain walk (deep dangling classes)

Traversal, not anecdote. Per discovered record:

```
WALK: start=<record> hop-1: CNAME -> <target> class=<A|CNAME|MX|NS>
  hop-2: ... terminal=<live|dead|dangling-class>
```

1. Follow CNAME→CNAME chains to terminal (max 8 hops, each hop a
   FACT); a mid-chain dangle point (hop 2 of 4) is recorded as the
   finding candidate — the class the per-bug stories miss.
2. MX and NS classes walked separately: dangling MX (mail exchanger
   gone) and apex NS delegation are their own EXPERIMENT records with
   severity computed from the mail/signing impact, not from the story.
3. Every hop's resolver evidence rides M3's rule — no single-read
   hops anywhere in the walk.

### M5 — the disclosure gate

Mandatory report block before any takeover finding ships:

```
DISCLOSURE: class=<dangling|claim-able> demonstration=<operator-owned
  only|none> registry-entry=<id, freshness> resolver-evidence=<M3
  summary> claim-wording: "record can be claimed by" — NOT "attacker
  can take over traffic", unless an operator-owned demonstration
  showed traffic service
```

The gate refuses overclaiming wording past the demonstrated class
(the cache-playbook ceiling habit, applied here).

## 2. Falsifiers — what would prove this method wrong

* The second resolver shows LIVE where the first showed NXDOMAIN →
  geo-DNS or split-horizon, not dangling: record BOTH, verdict
  COARSE, and the finding candidate dies.
* A "dangling" target is registered by a third party mid-test → the
  class was claim-able in the wildest sense; record the observation
  with timestamps, disclose immediately, stop testing (someone else's
  claim is now live infrastructure — touching it is out of bounds).
* The registry fingerprint matches but the live body hash differs →
  provider panel changed: registry entry stale, file the correction,
  downgrade the finding to "unverified-signature class".
* SOA serial bumps but queries stay stable → the zone is under active
  management: re-verify after the change settles before ANY class
  verdict.

## 3. Worked micro-example (numbers consistent, incident fictional)

Candidate: `vpn.old-target.com CNAME → cbn-status.netlify.com`,
TTL 300. M1: netlify-class fingerprint last verified 41 days ago
(fresh). M2 round 1: NXDOMAIN from resolver A; resolver B: NXDOMAIN;
3 rounds over 5 min → 6/6 stable. SOA serial unchanged. M2 class:
dangling, signature `404: not found` netlify-class body hash match.
M4 walk: single hop, terminal dangling. M5 disclosure: class
dangling, no registration demonstration (operator declined outside
scope), wording "record can be claimed by a registrant of the
dangling service name" — P4-class hygiene finding, evidence attached.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
EdOverflow's art is real — the can-i-take-over-xyz registry, the
dangling-record taxonomy — but it ships as a community wiki read by
eyes and takeover writeups told as single-screenshot stories. This
module extracts what is protocol-shaped, names the floors, and ships
the replacement: a versioned fingerprint discipline, a dangling
differential with TTL arithmetic, a claim ladder that separates
claim-able from vulnerable, a deep-chain walk, and a disclosure
block. An agent that has never browsed the wiki must run this at its
precision.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | The registry is a wiki — fingerprints (service strings, HTTP bodies, DNS errors) curated by community edit, consumed by memory | No version, no freshness stamp, no per-entry evidence date: a fingerprint read from the wiki today may describe a provider panel retired two years ago; the hunter "matches" against a ghost |
| W2 | Takeover told as one-shot demos — "registered the name, got the panel" | No differential: a CNAME to NXDOMAIN is a DEAD record, not a takeover, until the claim is actually tested; the writeup habit blurs dead, dangling, and claim-able into one drama |
| W3 | DNS state read once — TTL, serial, and resolver variance ignored | A resolver's negative cache can fake NXDOMAIN for minutes after the record died (or hide one); single-read claims carry error bars the writeups never quote |
| W4 | Deep chains and MX/NS classes narrated per-bug — CNAME→CNAME→dangling, dangling MX, apex NS | No walk protocol: the chain classes exist as stories, not as a traversal with per-hop records, so mid-chain dangle points get missed by anyone without the anecdote |
| W5 | Disclosure etiquette as afterthought — the responsible-discipline mentioned in prose | No disclosure block in the method: what to say, what NOT to say (no claim of compromise), what evidence to attach — the part that makes a takeover finding survive triage is folklore |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Fingerprints as versioned data with freshness stamps | **M1** — the fingerprint-registry discipline |
| U2 | Dead / dangling / claim-able as a differential ladder | **M2** — the dangling differential |
| U3 | DNS claims with TTL and resolver error bars | **M3** — the TTL-aware verification rule |
| U4 | Deep chains as a traversal protocol | **M4** — the chain walk |
| U5 | Disclosure as a report block | **M5** — the disclosure gate |
