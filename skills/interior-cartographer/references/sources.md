# sources.md — the Forshaw lineage, verified

What was actually consulted while distilling this organ, per the
assimilation doctrine (complete sources, attributed, no fabrication),
including the P2 census with its read ledger and the P3 psych-read
evidence per lens. The corpus is wide (a decade of posts, issues, talks,
two books, an instrument line); the ledger below states honestly what
was read in full, what was read as captured rendering or abstract, and
what was not read.

## P2 — the corpus census (with read ledger)

### Primary artifacts, read this forge

| Artifact | Year | Read status |
| --- | --- | --- |
| Project Zero post "Windows 10^H^H Symbolic Link Mitigations" (the four link types and their availability; MS15-090 backport to Vista; CVE examples CVE-2015-0055, CVE-2014-6322, CVE-2014-0568; the Infiltrate 2015 presentation reference; the byline "abusing symbolic links like it's 1999") | 2015-08-25 | full post body (captured rendering) |
| Project Zero post "Understanding Network Access in Windows AppContainers" (WFP architecture, layers/sublayers/filters, MPSSVC and BFE, the AppContainer restriction mechanism, the WontFix configuration issue with the disposition stated) | 2021-08 | full post body (captured rendering) |
| PoC 2023 talk page "Building More Windows RPC Tooling for Security Research" (abstract + speaker bio: local RPC extraction tooling; TCP/SMB/Hyper-V protocol sequences; cross-platform NTLM/Kerberos; Zerologon and PetitPotam named as the network-RPC class; the bio's #1 MSRC, Pwn2Own, Mitigation Bypass list) | 2023 | full abstract + bio |
| OffensiveCon 2018 speaker page (bio: #1 MSRC, Pwn2Own, Mitigation Bypass bounty winner, logical-vulnerability interest; talk abstract "New and Improved UMCI, Same Old Bugs" — UMCI history from Windows RT 2012 to Windows 10 S 2017) | 2018 | full page |
| GitHub profile tyranid (37 public repositories; pinned: the sandbox attack-surface analysis suite 2.3k stars, the COM viewer 1.4k, the PoC packer 1.3k, the Windows logical EoP workshop 233, the network proxy library line) | current | profile + pinned list |
| PowerShell Gallery pages for NtObjectManager 1.1.14 and 1.1.33 (full exported-command listings; author James Forshaw; copyright Google; the 1.1.14→1.1.33 growth measured on record) | 2017–2020 | both pages in full |
| NtObjectManager module manifest 1.1.17 (FunctionsToExport + CmdletsToExport, verbatim — 118 declared exports; the RPC/NDR tooling inside the function list) | 2018 | manifest read |
| MSRC Acknowledgments 2015 (the October–December portion of the table: three Forshaw-credited rows — MS15-115/CVE-2015-6113 kernel security feature bypass; MS15-111/CVE-2015-2553 mount point EoP; MS15-111/CVE-2015-2554 object reference EoP) | 2015 | portion read (stated) |
| Tyranid's Lair blog index at tiraniddo.dev (focus: Windows security research, ACLs, Kerberos, DCOM, Active Directory; recent posts "Working your way Around an ACL" 2024-06, "Relaying Kerberos Authentication from DCOM OXID Resolving" 2024-04, "Sudo On Windows" 2024-02, "Access Checking Active Directory" 2022-07) | 2022–2024 | index + post summaries |

### Read as captured rendering, coverage, or listing

| Artifact | Year | Read status |
| --- | --- | --- |
| Project Zero post "Windows Exploitation Tricks: Exploiting Arbitrary File Writes" (the chaining line; the reference to the earlier arbitrary directory creation technique) | 2018-04 | opening + structure |
| Project Zero issue tracker entries: the DCOM DCE/RPC local NTLM reflection issue (2015-04); the hardened VirtualBox COM interface EoP issue (2019-03); the DosDevices impersonation EoP issue | 2015–2019 | summaries |
| Press record of the first Microsoft bounty payout ($100,000; Windows 8.1-era preview mitigation bypass; program unveiled ~4 months earlier; "a computer vulnerability researcher"; employer not named in the articles read) | 2013-10 | two articles read |
| Press record of the Windows lockdown-policy disclosure (reported 2018-01; 90-day deadline enforced 2018-04; PoC via the lineage's own packing tool; the vendor's "not remotely exploitable, nor a privilege escalation" severity argument on record) | 2018 | three articles read |
| Windows 8.1 unpatched-issue disclosure with PoC (the January 2015 record) | 2015-01 | coverage read |
| TROOPERS speaker page (talks "The Joy of Sandbox Mitigations" 2016; "Demystifying COM" 2017) | 2016–2017 | page read |
| RECON 2016 speaker page (bio corroborating the #1 MSRC / Pwn2Own / bounty record) | 2016 | page read |
| Book records: Attacking Network Protocols (No Starch, December 2017, 336 pp) and Windows Security Internals (No Starch, 2024) — publisher pages, library records, and the 2024 book's table of contents (the access-check chapters: tokens, security descriptors, the access check process) | 2017–2024 | records + 2024 TOC |
| DeviceGuardBypasses repository (Windows 10 Device Guard bypasses; 7 commits through 2017-08) | 2017 | repository page |
| ZDI techniques article (the junction/hard-link/symlink following line, as ecosystem follow-on of the primitive tradition) | 2024-07 | article read |

### Not read (and not claimed)

* The two books' bodies — the census read the records and the 2024
  table of contents; no chapter's content is claimed, and the organ's
  knowledge of the access model comes from the documented constants it
  computes, not from the books.
* The blog's older archive below the index's recent window — the
  census records the focus areas and the dated recent posts; pre-2022
  post bodies are not claimed.
* The P0 bug tracker's full issue bodies beyond the summaries above —
  the organ cites them as records that exist, with ids and dates, not
  as read transcripts.
* The X/Mastodon profile beyond the bio line ("Security researcher in
  Google Project Zero. Author of Attacking Network Protocols.").

## P3 — the psych-read, lens by lens (documented behavior only)

* **L1 heuristics (≥ 3 independent artifacts each):**
  1. *Enumerate before you attack* — the accessible-object cmdlet
     family (package pages), the sandbox attack-surface suite
     (repository, 2.3k stars), the RPC extraction tooling talk (PoC
     2023): the corpus ships the census before the exploit, three
     times, years apart.
     *Extracted as*: M1 interior census with boundary rows — no class
     is attacked before every class is enumerated.
  2. *Hunt the trust decision, not the memory* — the logical-
     vulnerability interest stated in two independent conference bios
     (OffensiveCon 2018, RECON 2016) and demonstrated by the corpus's
     shape (the primitive line, the UMCI and Device Guard bypasses,
     the boundary arguments).
     *Extracted as*: the hunting ground is the access-check trust
     decision (M2 ACCESS_MASK audit), never memory corruption.
  3. *Ship the instrument with the finding* — the object-manager
     module (gallery), the PoC packing tool used in the 2018
     disclosure's PoC (press record), the network proxy library line
     (repository): findings arrive with their tools attached.
     *Extracted as*: counts and inventories are computed and cited
     (the command-count census); findings ship with reproduction
     attached.
  4. *Teach as a first-class output* — two books (2017, 2024), the
     Windows logical EoP workshop repository (233 stars), conference
     talks across a decade: the corpus doubles as curriculum.
     *Extracted as*: the boundary report with declined-seam residual
     risk (M5) — the organ doubles as curriculum.
* **L2 obsession (multi-year arc):** the Windows trust architecture —
  access control from the 2015 primitive taxonomy to the 2024 book's
  token/descriptor/access-check chapters; authentication relay from
  the 2015 NTLM reflection issue to the 2024 Kerberos-relay-from-DCOM
  post; sandbox and code-integrity from the Device Guard repository
  (2017) to the UMCI talk (2018); the RPC line from the local
  reimplementation era to the PoC 2023 tooling. Eleven-plus years on
  one problem class: how the OS decides whom to trust.
  *Extracted as*: scope discipline — one problem class, enforced by
  the census regression (M6).
* **L3 aesthetics (own words, cited):** "Symbolic links in themselves
  are not vulnerabilities, instead they're useful primitives for
  exploiting different classes of vulnerabilities" (2015 post) — the
  primitive as the unit of art; the byline "abusing symbolic links
  like it's 1999" (2015) carries the tonal register.
  *Extracted as*: the primitive, not the exploit, is the unit of
  record — M3's primitive inventory with the availability matrix.
* **L4 failure mode (on the record):** the WontFix case — the
  AppContainer firewall configuration issue published WITH the
  vendor's disposition and the full mechanism explanation (2021); the
  deadline discipline — the lockdown-policy bug disclosed at the
  90-day mark despite extension requests (2018, multi-article
  record); the counter-move documentation — the 2015 post records
  Microsoft's mitigation response (backported to Vista) to the
  lineage's own primitive line. Rejections, deadlines, and
  counter-moves are kept, not hidden.
  *Extracted as*: vendor dispositions, deadlines, and counter-moves
  land as rows in the boundary report (M5), never silently dropped.
* **L5 cadence (public timeline):** report → vendor window → publish
  with tooling → teach. The 2018 case is fully dated (reported
  January, deadline April, PoC public); the 2013 bounty (program
  unveiled mid-year, payout announced October); the 2015
  disclosure-with-PoC (January). The pattern: the finding ships with
  its reproduction attached, on a stated clock.
  *Extracted as*: the report clock — findings ship with reproduction
  attached; M6 re-runs the census on the stated schedule.

OPINION figure=James Forshaw lens=cross reading=the long game on one
vendor is deliberate platform positioning — depth chosen over breadth
artifact=NONE status=quarantined next=a stated career-strategy
statement in a primary artifact would admit it; the eleven-year arc is
a fact, the motive for it is not.

## Boundaries argued (P1's overlap gate, on record)

* **vs api-surface-mapper**: that organ maps EXTERNAL API surfaces —
  specs diffed against live behavior over HTTP; this organ enumerates
  the OS interior from the running system itself, where the
  enumeration IS the ground truth and no spec is assumed.
* **vs surface-cartographer**: that organ maps the network-visible
  estate BEFORE a foothold exists; this organ's precondition is the
  foothold — one unprivileged process — and its hunting ground is
  everything that process can reach locally.

## Corrections kept on record

* **The Registry Adventure is not Forshaw's.** The 8-part "Windows
  Registry Adventure" series (2024–2025) is Mateusz Jurczyk's work;
  an aggregator title rendered as "Project Zero: The Windows Registry
  Adventure" initially suggested otherwise. The verified shared
  record: Jurczyk documents having fuzzed the registry "together with
  James Forshaw" in 2016. The registry-entry correction keeps this
  attribution honest — the organ claims the 2016 co-fuzz thread, not
  the audit series.

## What this organ does NOT claim

* No Forshaw code, tools, module manifests, or book text are
  redistributed or embedded; the command counts are cited to the
  public package pages and manifest, and every other number in the
  organ is computed in-house and labeled as computed.
* The employer at bounty time (2013) is not claimed — the articles
  read name a London-based researcher without the employer; the
  record is stated at exactly that resolution.
* The Pwn2Own win's year and category are not claimed beyond the two
  speaker bios' own wording ("Pwn2Own ... winner").
* Nothing about motives or inner life is claimed — the psych-read
  cites behavior with artifacts only; the quarantined opinion stays
  quarantined.

## Confidence

High for the bio facts (three independent conference bios agree on the
#1 MSRC listing, the Pwn2Own and bounty record, the logical-vulnerability
interest); high for the three load-bearing Project Zero artifacts (the
2015 and 2021 posts in captured renderings, the 2023 abstract, the
2018 press record multi-sourced); high for the instrument census (two
package pages and the manifest, transcribed and counted by code);
medium for the MSRC window count (a stated portion of the table was
read — three rows in the window, not a full-year count); high for the
books' existence and shape (publisher and library records, the 2024
table of contents). Where the record and the folklore differ (the
Registry Adventure attribution), the correction above wins and lives
in the registry entry.
