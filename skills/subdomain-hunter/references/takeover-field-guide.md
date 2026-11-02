# takeover-field-guide.md — the EdOverflow lineage layer for subdomain-hunter (v2)

Load when verifying ANY takeover candidate, building a dangling-class
verdict, or deciding whether a provider fingerprint is claimable.

## 1. The Dangling Classes (CNAME is only the first rung)

A "subdomain takeover" claim starts with a resource record pointing at
infrastructure nobody currently owns. The record TYPE decides the class,
and the class decides the blast radius:

| Class | Record | Claim path | Blast radius argument |
| --- | --- | --- | --- |
| NXDOMAIN-CNAME | CNAME → host that no longer resolves | register the name at the provider | full content control on the name |
| Fingerprint-CNAME | CNAME → resolving host whose body carries the provider's "not found / unclaimed" marker | claim the resource in an existing account | full content control, but the marker must match the registry, not a vibe |
| Dangling MX | MX → mail provider tenant gone | re-register the mail route | email reception on the zone — phishing-grade trust, NOT web content |
| Dangling NS | NS → expired/delegated zone | re-register the zone at the registrar/reseller | the whole subtree, including records the parent still sets |
| Deep chain | CNAME → CNAME → … → terminal | fix the TERMINAL in the analysis; intermediates are noise | verdict is about the terminal, intermediates only route |

Record the class as a FACT in the candidate's record pair. A takeover
report that does not state its class has not stated its impact.

## 2. The Verification Protocol (three records, TTL-aware)

The organ's hard rule — CNAME chain FACT + provider marker FACT — gets its
full shape here:

1. **DNS leg.** The full chain from the parent zone to the terminal, one
   `dns_resolve` record per hop, terminal included. A chain truncated at
   the first hop is an unverified hypothesis, not evidence.
2. **Marker leg.** The terminal host probed once over HTTP(S): the body,
   status, and the specific fingerprint line. Match it against the
   signature table (`references/takeover-signatures.md`) and against the
   upstream registry's `fingerprint` field — a 404 alone is not a
   fingerprint; many healthy services 404 on `/`.
3. **Cache leg.** DNS answers and provider markers are cached. A negative
   marker read at TTL `t` must say so in the record note, and a verdict
   that matters is re-read after the TTL window expires. The classic
   false CONFIRMED is a stale NXDOMAIN surviving from before the provider
   reclaimed the resource.

## 3. The Fingerprint Registry Discipline

The upstream community registry (`can-i-take-over-xyz`) is machine-readable
by design — `fingerprints.json` carries, per service: the CNAME targets,
the exact fingerprint string, whether NXDOMAIN is expected, a
`vulnerable` boolean, and a link to the discussion issue where the verdict
was earned. Fold that discipline in:

* **Fingerprint strings are quoted, not paraphrased.** "The specified
  bucket does not exist." is evidence; "some S3 error" is slop.
* **The registry's verdict is dated.** Providers flip from vulnerable to
  hardened (and back) as they add domain-ownership verification. Pin the
  date the table was synced in the reference; a takeover table that has
  not changed in a year is dead doctrine, not stability.
* **`http_status: null` entries exist** — some fingerprints live in bodies
  served with unexpected statuses. Read the body, not the code alone.

## 4. The Claim-Path Test (the "not vulnerable" that bites)

Before any CONFIRMED, answer one question with evidence from the provider's
public behavior or documentation: **does claiming this resource require
proving ownership of the victim domain?**

* If yes (DNS TXT verification, ownership challenge on first claim), the
  dangling record is a hygiene finding, not a takeover — record it as
  such and close the hypothesis REFUTED-for-claimability.
* If no (create account → add custom domain → publish), the candidate is
  CONFIRMED-pending-operator-action. The operator decides whether the
  bounded proof claims anything at all; this organ never registers
  resources (hard rule 3 of the organ).
* Provider policy evolves: re-cite the upstream discussion issue for the
  service in question when the verdict is load-bearing for the report.

## 5. The Correction Tradition (entries retire)

The upstream registry's issue history is itself doctrine: entries are
argued, demoted to `not vulnerable`, and retired as providers harden —
the Unbounce false-positive debate and the Google Sites
ownership-verification retirement are the canonical examples. Mirror that
honesty locally:

* Every takeover CONFIRMED cites the signature-table row AND its sync
  date; every retirement of a once-vulnerable provider noted in the
  engagement gets a ledger record too.
* A takeover-signature table in this repo that contradicts the upstream
  registry on a load-bearing verdict is a bug in this repo — the
  discrepancy is recorded and resolved before the report ships.
