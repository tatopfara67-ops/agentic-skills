# sources.md — the Kaminsky lineage, verified

What was actually consulted while distilling this organ, per the
assimilation doctrine (complete sources, attributed, no fabrication),
including the P2 census with its read ledger and the P3 psych-read
evidence per lens. The corpus is large (~152 blog posts across
2003–2017, a 16-year talk run, and 128K social posts); the ledger
below states honestly what was read in full, what was read as
index/abstract, and what was not read.

## P2 — the corpus census (with read ledger)

### Primary artifacts, read in full this session

| Artifact | Year | Read status |
| --- | --- | --- |
| CERT Vulnerability Note VU#800113 (DNS cache poisoning; 16-bit TXID, 32,768 average attempts, +16 bits source-port entropy, 22-vendor list incl. Apple/Cisco/IBM/ISC/Juniper/Microsoft; NAT caveat; DNSSEC for complete protection) | 2008-07-08 (rev. 2014) | full text |
| Black Hat Webcast #2 page, "Dan Kaminsky's DNS Discovery: The Massive, Multi-Vendor Issue and the Massive, Multi-Vendor Fix" (with Jeff Moss, Rich Mogull, Joao Damas/ISC — "early in 2008" discovery; "combined effort of historic proportion") | 2008 | full page |
| Wikipedia "Dan Kaminsky" (career: Cisco, Avaya, IOActive director of pentest, White Ops/Human Security co-founder; Sony rootkit 568,000+ count; Earthlink DNS April 2008; Conficker detection 2009-03-27; SSL flaws 2009 with M. Patterson and L. Sassaman; Interpolique 2010-06; ICANN Trusted Community Rep 2010-06-16; the 2016 "pictures of cats / trillions of dollars" quote; djb's 1999 prior TXID report; NYT "Internet security savior") | 1979–2021 | full article |
| dankaminsky.org — the posthumous restoration of his blog (original domain lost to spammers): the complete talk-corpus list 2001–2012 with Kaminsky's own abstracts, and the blog archive counts (2003–2017, ~152 posts) | 2001–2017 | full index + all talk abstracts |
| X/Twitter @dakami profile: the bio ("We can fix it. We have the technology. OK. We need to create the technology... WE'RE ON IT.") and the pinned 2018-01-17 post ("every functioning system has two forms... You eventually unlearn its necessary lies.") | 2018–2021 | profile + pinned post |
| Internet Hall of Fame 2021 inductee page (secret meeting at Microsoft HQ; DHS involvement; patch "applied simultaneously worldwide within a few months"; Conficker scanner; Sony; age at discovery: 29) | 2021 | full page |
| paratrace man page (Paketto Keiretsu 1.0 — "Parasitic Traceroute via Established TCP Flows & IPID Hopcount", DoxPara Research) | 2002 | full man page |

### Read as listing/abstract or via documented secondary coverage

| Artifact | Year | Read status |
| --- | --- | --- |
| "It's The End Of The Cache As We Know It" — Black Hat/DEF CON 16 talk (abstract via the restored blog; slides PDF at blackhat.com not fetched in full — binary) | 2008 | abstract + coverage (CSO, ZDNet 2008-08-07) |
| Black Ops talk series — "Black Ops of DNS" (2004, incl. MD5 work), "Black Ops of TCP/IP 2005.5" (worldwide DNS scans, Sony rootkit), "Staring Into The Abyss" + "Black Ops of PKI" (2009, X.509 structural weaknesses), "Black Ops of TCP/IP 2011", "Black Ops of Fundamental Defense: Web Edition" (IOActive-era abstract carrying the "design-level fault analysis, particularly against large-scale systems" specialty line) | 2001–2011 | own abstracts via restoration |
| Paketto Keiretsu 1.10 (scanrand stateless SYN-cookie scanner, 5 tools, DoxPara) | 2002 | tool listing + scanrand/paratrace documentation |
| LWN coverage threads, July–Aug 2008 (djbdns confirmed not vulnerable via its own source-port randomization; glibc stub-resolver population discussion) | 2008 | full comment threads |
| easydns "DNS cache poisoning exploit released" (the post-leak exploit wave) | 2008-07-24 | article read |
| Network World "Kaminsky pushes DNS patching" (the DNSSEC pivot: "for years ambivalent... has become an ardent supporter") | 2009-02-19 | article read |
| Ivan Ristić, "Black Hat 2009 SSL Review: Black Ops of PKI" ("several very interesting points, but it fails on delivery") | 2009-08-04 | article read |
| Black Hat DC 09, Wouters, "Defending your DNS in a post-Kaminsky world" (0x20 encoding, birthday-attack hardening — the ecosystem response) | 2009 | slides cited as follow-up record |

### Not read (and not claimed)

* The ~152 blog post bodies (the restoration's index and talk
  abstracts were read; individual essays were not) — the census
  bounds itself accordingly.
* His social feed's bulk (128K posts) — only the bio and pinned
  post, which are self-authored artifacts.
* Private coordination records (the Microsoft HQ meeting has no
  public transcript; the Hall of Fame's account is the record used).

## P3 — the psych-read, lens by lens (documented behavior only)

* **L1 heuristics (≥3 artifacts each):**
  1. *Attack the spec at the population level* — DNS 2008 (VU#800113,
     22+ vendors), PKI 2009 (X.509 structure, not one CA), Sony 2005
     (population census of one infection) — the same move three
     times, six years apart.
  2. *Build instruments to see the population* — Paketto tools
     (2002), worldwide DNS scans (2005), the Conficker signature
     scanner (2009): the corpus ships measurement tools with its
     findings.
  3. *Compose the invariant classes* — entropy × ordering × trust
     (2008); ASN.1 confusion × null terminators (2009): single-class
     findings get composed before they are claimed.
* **L2 obsession (multi-year arc):** the DNS/trust-in-infrastructure
  class spans 2002–2017 — DNS tunneling (2004), DNS scans (2005),
  rebinding (2007), cache poisoning + the fix (2008), DNSSEC
  advocacy and zero-config DNSSEC serving (2009–2010), the root
  key-holder role (2010), web-trust realism (2010).
* **L3 aesthetics (own words, cited):** "The Internet was never
  designed to be secure. The Internet was designed to move pictures
  of cats... We didn't think you'd be moving trillions of dollars
  onto this... Some of us got to go out and fix it." (2016
  interview, via the Wikipedia record); "every functioning system
  has two forms: The abstraction that outsiders are led to believe,
  and the reality that insiders actually and carefully operate...
  You eventually unlearn its necessary lies." (X, 2018-01-17).
* **L4 failure mode (on the record):** the priority record — djb
  reported the TXID weakness in 1999 and djbdns shipped the port
  randomization years early while the industry shipped vulnerable
  (Wikipedia; LWN 2008), and Kaminsky himself confirmed djbdns
  non-vulnerable; the delivery criticism — Ristić's "fails on
  delivery" (2009) is kept as the documented cost of the humor-first
  format; the stopgap honesty — the record itself prices port
  randomization as partial and pushes DNSSEC (VU#800113;
  Network World 2009).
* **L5 cadence (public timeline):** discovered early 2008 → months
  of secret coordination (DHS; Microsoft HQ meeting) → simultaneous
  patch 2008-07-08 (VU#800113 original release date) → leak
  2008-07-21 → full reveal Black Hat 2008-08-06/07 (webcast page,
  Wikipedia, Hall of Fame). The pattern: sit on the find until the
  fix is ecosystem-ready, then disclose as a coordinated event.

OPINION figure=Dan Kaminsky lens=cross reading=the humor was a
deliberate pedagogical instrument, chosen over density
artifact=NONE status=quarantined next=a dated talk transcript with
its joke/density structure annotated would admit it; Ristić's
review is one professional's verdict, not a measured instrument.

## Boundaries argued (P1's overlap gate, on record)

* **vs desync-hunter (Kettle)**: same protocol family, different
  unit — desync-hunter proves one ambiguity on one request path
  between two specific parsers; protocol-forensics prices the
  spec's ambiguity across the whole implementation population and
  engineers the class-level fix. The 2008 record is the type case
  (the finding was never "one vendor's parser").
* **vs scan-economist (Fyodor)**: scanrand (Paketto, 2002) is
  adjacent to scan economy, but the lineage's hunting ground is the
  spec class, not the sweep; probe budgeting is INHERITED from
  scan-economist while running this organ's matrix, not re-derived
  here.

## What this organ does NOT claim

* No Kaminsky code, tools, or talk materials are redistributed or
  embedded; the arithmetic constants are cited to VU#800113 and the
  rest is computed in-house and labeled as computed.
* The blog-restoration site is a posthumous mirror (the original
  domain was lost); it is cited as the restoration it is, with that
  provenance kept visible.
* The private coordination narrative (secret meetings, DHS) is
  recorded only at the level the public record supports; nothing
  about motives or inner life is claimed — the psych-read cites
  behavior with artifacts only.

## Confidence

High for the 2008 event's mechanics and timeline (three independent
primary records agree: CERT, the Black Hat webcast page, the Hall of
Fame account); high for the talk corpus structure (his own restored
abstracts); medium for the blog-era method claims (index read, post
bodies not read — the ledger says so). Where the record and the
folklore differ ("Kaminsky bug" as a wholly novel find vs the 1999
Bernstein prior art), the priority record wins and the correction
lives in the registry entry.
