# The source case — Christmas Day 1994 to Raleigh, February 1995 (case file)

The binary brain is distilled from one hunt. This file is the case
record in fact-table form: every documented fact carries the method
lesson it contributed, and the era, the personalities, and the
mythology stay out. The method itself lives in
references/binary-brain.md and references/hunt-playbook.md; the
executable protocol is references/method-upgrade.md §1 (M0–M5).

## Case facts → method lessons

| Date | Documented fact (sourced) | Method lesson kept |
| ---- | ------------------------- | ------------------ |
| 1994-12-25 | Intrusion into Shimomura's personal machines discovered; technique = IP source-address spoofing + TCP sequence-number prediction, abusing rsh/rlogin trust without seeing the replies | the trust decision, not the memory, is the seam — hunt the trust edge (P1/P2) |
| prior art | The technique was described by Robert Morris (1985) and Steven Bellovin (1989) but had mostly lived on paper until then | the spec-vs-population gap: a paper mitigation is not a deployed defense — audit the population |
| 1994-12-25 | Among the files taken: cellular-telephone security software (later reporting put its value at up to one million dollars); taunting messages left on the answering machine | tempting unreadable assets are instrumentation, not just loss — file canaries with unique tokens (M0) |
| 1992 | Shimomura had testified before the U.S. Congress on cellular-phone vulnerabilities — years before the same substrate became his hunting ground | domain depth under the adversary's tools beats generic incident response |
| 1995 (weeks after) | The compromised machines were studied, not scrubbed — packet captures preserved, the intrusion reconstructed from records | capture before change (P0) — volatile state first, analysis second |
| 1995 (weeks after) | The trail ran through intermediate systems and telephone networks; the intruder touched systems in San Diego, Seattle, and Colorado, and monitoring watched telephone switching centers being commandeered | multi-channel evidence with per-channel provenance (P3) — a channel that lands in the ledger is a channel that exists |
| 1995-02-11 | The decisive phase paired carrier-side records (the telephone network's own accounting) with radio-frequency measurement on the ground — the "reverse double triangulation" | two independent channels to fix a claim; single-channel conclusions are LEADs, never findings (Rule T) |
| 1995-02-15 ~01:30 | The FBI arrested Mitnick at his Raleigh apartment; the physicist had handed them the location | the handoff pack is the ending (P6) — person-level action is the consumer's lane, not the tracker's |
| 1996-04 | Plea agreement; nearly five years served; later a security consultant and author until his death in July 2023 | nothing — era, not method; kept here only to close the record |
| contested | Mitnick's supporters disputed both the narrative and even the authorship of the attack (Jonathan Littman, *The Fugitive Game*, 1996) | single-story epistemology fails: pre-registered falsifiers, n_runs floors, and append-only records (W6 → U6) |

## What the skill keeps, and what it leaves

| Keeps (method, documented) | Leaves (era, contested, or unlawful for us) |
| -------------------------- | ------------------------------------------- |
| capture before change (P0) | the 1995 X.25/modem substrate |
| baseline-then-signal (P1/P2) | attribution mythology, "most wanted" framing |
| halving the hypothesis space | vigilante pursuit of a person |
| two independent channels to fix | knocking on doors — the FBI's job, then and now |
| quiet while they spend exposure | counter-intrusion into the adversary's systems |
| handoff pack as the ending | the taunt-vs-taunt game |

## Sources consulted

* Korben — "Tsutomu Shimomura, the physicist who trapped Kevin
  Mitnick": https://korben.info/en/tsutomu-shimomura-physicist-trapped-kevin-mitnick.html
* thern.io lexicon — "Tsutomu Shimomura":
  https://wiki.thern.io/en/t/tsutomu-shimomura
* San Francisco Chronicle/ Associated Press, Feb 16, 1995 — "Elusive
  Computer Hacker Tracked Down by Another":
  https://www.sfgate.com/news/article/Elusive-Computer-Hacker-Tracked-Down-by-Another-3044586.php
* Sun-Sentinel, Feb 18, 1995 — "Civilian experts helped nab hacker":
  https://www.sun-sentinel.com/1995/02/18/civilian-experts-helped-nab-hacker-authorities-say
* EBSCO Research Starters — "Arrest of Hacker Kevin Mitnick":
  https://www.ebsco.com/research-starters/history/arrest-hacker-kevin-mitnick
* Christian Science Monitor, Oct 3, 2002:
  https://www.csmonitor.com/2002/1003/p15s02-bogn.html
* New York Times, Apr 24, 1996 — "Leading Computer Hacker Strikes a
  Plea Agreement":
  https://www.nytimes.com/1996/04/24/us/leading-computer-hacker-strikes-a-plea-agreement.html
* Shimomura & Markoff, *Takedown: The Pursuit and Capture of America's
  Most Wanted Computer Outlaw* (Hyperion, 1996).
