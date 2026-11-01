# The source case — Christmas Day 1994 to Raleigh, February 1995

The binary brain is distilled from one hunt. This file records what is
documented, with sources; the skill keeps the method and leaves the era.

## The event

On **December 25, 1994**, Tsutomu Shimomura — a computational physicist
at the San Diego Supercomputer Center — discovered that someone had
broken into his personal machines, kept at his beach cottage near San
Diego. The intrusion used **IP source-address spoofing combined with
TCP sequence-number prediction**: the attacker posed as a trusted host
and abused rsh/rlogin trust without ever seeing the replies. The
technique was not new — Robert Morris had described it in 1985 and
Steven Bellovin in 1989 — but it had mostly lived on paper until then.
Among the files taken was cellular-telephone security software; later
reporting put its value at up to one million dollars. The intruder
reportedly also left taunting messages on Shimomura's answering
machine.

## The man

The counterparty was not a generic incident responder. Shimomura had
studied at Caltech under Richard Feynman, worked on lattice-gas
computation at Los Alamos, joined SDSC in 1989, and had testified
before the U.S. Congress in **1992 on vulnerabilities in cellular
phone systems** — years before the same substrate became his hunting
ground. He is the son of Osamu Shimomura, who received the 2008 Nobel
Prize in Chemistry for green fluorescent protein. The hunt worked
because the defender understood the physics underneath the adversary's
tools: sequence-number mathematics, telephone switching, radio.

## The hunt

Contemporary reporting and the book account (*Takedown*, 1996, with
journalist John Markoff) describe the shape:

* The compromised machines were **studied, not scrubbed** — packet
  captures preserved, the intrusion reconstructed from records.
* The trail ran through intermediate systems and telephone networks;
  the intruder had touched systems in **San Diego, Seattle, and
  Colorado**, and monitoring let investigators watch him "commandeer
  telephone company switching centers" while using cellular phones for
  access.
* The decisive phase paired **carrier-side records** (the telephone
  network's own accounting of where the calls were) with
  **radio-frequency measurement** on the ground — triangulating the
  handset's signal from the street. Retellings popularized the phrase
  "reverse double triangulation" for this two-channel fix. On
  **Saturday, February 11, 1995**, Shimomura concluded the intruder
  was Kevin Mitnick and that he was in Raleigh, North Carolina.
* On **February 15, 1995, at about 1:30 in the morning**, the FBI
  arrested Mitnick at his Raleigh apartment. The physicist had handed
  them the location; the door was theirs to knock on.

## The aftermath

Mitnick — by then the FBI's most wanted computer outlaw — was indicted
on multiple counts of computer and wire fraud and, after a 1996 plea
agreement, ultimately served nearly five years in prison. He later
worked as a security consultant and author until his death in July
2023. The telling itself stayed contested: Mitnick's supporters
disputed both the narrative and even the authorship of the attack
itself; Jonathan Littman's *The Fugitive Game* (1996) is the rival
account. The discipline in this skill takes no side in that argument —
it keeps the method, which is documented, not the mythology.

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
