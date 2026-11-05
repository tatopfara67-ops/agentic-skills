# sources.md — the reading ledger for the Jason Haddix lineage layer

> Part of **mythos-bug-hunter v4.7.0** (package architecture).
> **Load when:** auditing the onboarding-preservation layer's provenance;
> re-screening the candidate queue; verifying a census claim about the
> Haddix corpus. This is the P2/P3 record: what was read, how fully, and
> what stayed quarantined. The lineage registry entry
> (`mythos_lineages`, organ `mythos-bug-hunter`) points here.

---

## 1. The version-pinned read table (the queue's gate, honored)

The Q6 gate demanded two things before drafting: the deck versions
PINNED (the corpus versions fast), and the figure's own method separated
from his documented curation of others' tools. Both were executed and
are on record below.

**READ IN FULL (primary artifacts, text-extracted, dates pinned):**

| Artifact | Version / year pinned | Read how |
| --- | --- | --- |
| "How To Shot Web (Better hacking in 2015)" — the TBHM v1.0 deck | DEF CON 23, Aug 2015 (the repo README pins it as version 1.0) | the repo PDF (82 slides), full text extraction; role on record in-deck: Bugcrowd Director of Technical Ops, #1 on the all-time Bugcrowd leaderboard 2014 |
| The tbhm repo chapters 01_Philosophy … 11_Auxiliary_Info | 2016–2020 by commit dates (05_XSS Mar 2018, 07_File_Upload Oct 2017, 02_Discovery Jun 2020) | every chapter read in full; 12_IDOR is a "To be continued ..." stub — the carrier itself stalled while the decks advanced |
| Fast Testing Checklist.md (tbhm repo) | last touched Jan 17 2023 | read in full; the header states the derivation on record: "a combination of my own methodology and the Web Application Hacker's Handbook task checklist" |
| TBHM Live — Day One: Recon (course deck) | the 2023-era content (BBOT, WayMore, ReconGPT, the kaeferjaeger cert datasets) | full text extraction (1160 lines) from the public mirror copy |
| TBHM Live — Day Two: Application Analysis Master (course deck) | same era | full text extraction (1175 lines) from the public mirror copy |
| TBHM Core public syllabus (arcanum-sec.com) | the 2024+ on-demand course | the 20-module syllabus read (M01 general topics … M20) |

**READ (documented via primary records, stated as such):**

| Record | What it pins |
| --- | --- |
| The v4 release record (X posts, Jun 14–15 2020) | v4 Recon edition slides released Jun 14 2020 ("Here are the slides ... Enjoy!"); the S-Tier framework additions (Jaeles, Osmedeus, HunterSuite) Jun 15; "When is v4 App Analysis coming out? ... probably 2-6 weeks. I want to encompass all the old version's ideas into this new one"; the correction path in his own words: "these are just my opinions based on heavy use & could be wrong. I want to learn! DM me!" |
| The v2 record | Bugcrowd LevelUp 0x01 (virtual conference, Jul 2017) — the Bugcrowd recap (Jul 21 2017) names "Bugcrowd's Head of Trust & Security, Jason Haddix, give his presentation 'Bug Hunter Methodology, v2'" |
| The v3 record | LevelUp 0x02, 2018 — the Bugcrowd resource page ("Bug Bounty Hunter Methodology v3, plus the announcement of Bugcrowd University") plus the complete third-party conference notes (pentester.land, Jun 19 2018; secondary, stated as such) covering the full v3 structure: IP space, brand/TLD discovery, subdomain discovery, enumeration, credential bruteforce, visual identification, wayback, platform/CVE, JS parsing, content discovery, XSS/SSRF/IDOR/infra/WAF, Xmind organization |
| The v4 Recon edition deck content | via the complete third-party notes (trickster.dev): the root/seed mind-map structure, the recon question set (ASN/acquisitions/linked discovery/reverse whois), and the four recon-framework tiers C/B/A/S |
| The career record (multi-sourced: Arcanum about-us, Recon Village speaker bio, SANS profile, LinkedIn surface) | CISO of Ubisoft and BuddoBot (plus FLARE per the older bio), Head of Trust & Security (later Trust/Security/Operations) at Bugcrowd, Director of Penetration Testing at HP, Lead Penetration Tester at Redspin, founder/CEO Arcanum Information Security; stages: DEF CON, Black Hat, RSA, OWASP, Nullcon, SANS |
| DEF CON 25 Recon Village 2017 | "Domain Discovery: Expanding your scope like a boss" (abstract read) |
| DEF CON 32 (2024) | "The Darkest Side of Bug Bounty" (talk record read) |
| The podcast record | Critical Thinking — Bug Bounty Podcast (running since 2023, ~200 episodes, host Justin): his appearances on record (ep 12, Mar 2023, "Hacker->Hacker CISO"; ep 102, Dec 19 2024, "Building Web Hacking Micro Agents with Jason Haddix") |
| The GitHub record | jhaddix/tbhm (4.4k stars, 104 commits, last Jan 17 2023), jhaddix/domain (enumall.sh, 942 stars), SubreconGPT (referenced in-deck), the public gists (bountycatch.py, the GitHub-dork collection, the SSRF metadata list, the content-discovery and subdomain-enumeration wordlist files) |

**BOUNDED (stated, not line-read):** the talk videos (v1 2015 through
"Darkest Side" 2024); the v4 Recon edition Google Drive original (the
link is truncated in the release post; content covered via the complete
notes); the .xmind mind-map binaries (Project (OD).xmind in-repo and
the xmind gallery mirror); all2.txt (16.6 MB) and the wordlist gists
(data, not method); the TBHM2 and TBHM Core paid course interiors; the
LinkedIn essay (login wall); the kris3c TBHM2 decode series beyond the
introductory article read.

The version chain as pinned: v1 "How To Shot Web" DEF CON 23 (2015) →
v2 LevelUp 0x01 (Jul 2017) → v3 LevelUp 0x02 (2018, Bugcrowd
University launch) → the Application Analysis edition (h1-702 era, per
the talk record) → v4 Recon edition (Jun 2020) + v4 App Analysis →
TBHM Live (2023/24) → TBHM Core (2024+, paid). No public v5 deck
exists in the census — the free chain ends at the v4/Live era; the
series continues as the paid Core course.

## 2. The psych-read (five lenses, documented behavior only)

| Lens | The pattern (artifact, year) |
| --- | --- |
| L1 heuristics | the road-less-traveled scope selection (DC23 2015; repo 02_Discovery 2016-2020; Live Day 1 wide-vs-narrow; Core syllabus) — hunt the less-tested asset, flagships are saturated; the quantified instinct (the 2x-per-subdomain / 4x-per-apex multipliers, the "+50% efficacy" of configured APIs, the "3-10% increased discoveries" from standalone narrow tools, the HUNT parameter lists per vuln class — Live Day 1/Day 2); the cycle-and-state kit ("recon is a cycle ... not a linear process", the mind-map color protocol green/orange/red/checkmark, bountycatch.py / BBRF tracking); the template discipline ("most found" classes get templates — with the URL/domain-change protip, DC23 + repo 01_Philosophy); the prove-it-out rule ("You will always have to prove out the vulnerability that any of these scanners finds for you" and, for the AI form, "Remember the dataset cuts off in 2021. Verify all results!" — Live Day 1/Day 2) |
| L2 obsession | methodology packaging itself: one artifact re-forged across six carriers over nine years (talk → repo → class → live course → on-demand course), each version "encompassing all the old version's ideas" (his own words, Jun 2020); the curator-teacher stance (the 17-name attribution slide at DC23; "follow these ninjas"; the resources routing to PortSwigger Academy / Rana Khalil / Nahamsec; the Bugcrowd University launch riding the v3 talk) |
| L3 aesthetics (own words) | "Find the road less traveled" (2015→2023); "Many people can teach `';alert('xss');//` — less people teach where to look for web bugs" (Live Day 2); "Recon is a cycle ... It's not a linear process" (Live Day 1); "Data Driven Assessment (diminishing return FTW)" (DC23); "the vulns formerly known as 'noise'" (repo 11_Auxiliary) |
| L4 failure mode (on record) | the honest-rot documentation: the Ashar Javed XSS methodology "at this point eight years old ... I still struggle to replicate" (Live Day 2); the Twitter-API automation workflow "currently in trouble" (Live Day 2); WPscan "has gone paid ... I'm still looking for a viable alternative" (Live Day 2); the correction path ("could be wrong. I want to learn! DM me!", Jun 2020); the commitment honesty ("I'm moving this week, so probably 2-6 weeks", Jun 2020); the carrier drift (repo chapters stalled 2016–2020 while the decks versioned; 12_IDOR "To be continued ...") |
| L5 cadence | the version release cadence IS the shipping cadence: v1 2015, v2 2017, v3 2018, the App-Analysis era 2019, v4 Jun 2020, Live 2023/24, Core 2024+ — for a methodology corpus the artifact-release event ("Here are the slides ... Enjoy!") is the disclosure equivalent |

## 3. The quarantine (OPINION class — never method evidence)

* The Bugcrowd all-time leaderboard rank (57th in the older bios, 85th
  in the current Arcanum bio) — a press-record-of-standing row; ranking
  drift is recorded as fact, priced as nothing.
* Community-reception framings around TBHM ("legendary", "the OG") —
  press/podcast reception only.
* The DEF CON 34 Hackbots / BBV masterclass record (2026) and the
  "sixteenth DEF CON" essay (Aug 2026, login wall) — career-record
  rows, not method artifacts.
* Any reading of motive behind the free-deck → paid-course transition —
  not in evidence. The census records the transition as fact and prices
  nothing about intent.

## 4. The attribution ledger (A3 — the curation is his, the tools are theirs)

The corpus's tool rows are documented curation, attributed in the
artifacts themselves: recon-ng/enumall (Tim Tomes), Amass (Jeff
Foley), Subfinder and Nuclei (ProjectDiscovery), altdns (Nathaniel
Wakelam and Shubham Shah), GoSpider (j3ssie), hakrawler (hakluke),
Autorize (Quitten), Gap and WayMore (Xnl-h4ck3r — "one of our
esteemed class members"), getrelationship.py (m4ll0k), Metasec.js
(LewisArdern), Webpack Exploder (spaceraccoon), the polyglot payloads
(rsnake, Ashar Javed, Mathias Karlsson), the upload-filter research
(Soroush Dalili), Source2URL (Daniel Miessler), the DC23 attribution
slide's seventeen names, and — stated by the artifact's own header —
the Web Application Hacker's Handbook task checklist as the Fast
Testing Checklist's other parent (Stuttard and Pinto heritage).

This ledger is also the license: the W1–W6 critique in
references/method-upgrade.md critiques the corpus's SHIPPED FORM, and
that license is granted by attribution, never by seniority.

## 5. The Q6 gate verdict (the re-score, reasons per axis)

The gate was honored before drafting: deck versions pinned (§1), the
method/curation separation executed as the A3 ledger (§4). Re-score at
retirement: **7 → 9**, the queue's second recorded RISE.

* volume 2 — nine years, six carriers, a versioned chain.
* explicitness 2 — the HOW ships: checklists, numbered protocols, a
  report template, a response-reading mnemonic, parameter lists; this
  axis was the 7-score's doubt and the reading answered it.
* verifiability 2 — the free chain is public (decks, repo, checklist,
  gists); the paid interiors are stated BOUNDED, not silently assumed.
* non-overlap 1 — the upgrade route: the methodology-preservation
  layer is new ground, but it lands ON the spine's existing onboarding
  path. The queue's own rule ("a documented upgrade of an existing
  organ counts as an assimilation too") legitimized the route; the
  ground is the organ's, not virgin corpus territory. Capped honestly.
* psych-read yield 2 — patterns repeat across 15+ artifacts on the open
  record; no pseudonym caps the read.

Total 9/10, with the per-axis reasons kept per queue discipline rule 2.
