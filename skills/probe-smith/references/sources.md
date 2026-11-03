# sources.md — the census, read ledger, and psych-read evidence

The verification record for the probe-smith forge (the fourth
candidate-queue execution). What was actually read, in what depth,
and what every psych-read line cites. The queue's Q3 gate demanded
the scattered corpus be consolidated BEFORE any psych-read line
landed — this table is that consolidation.

## 1. The census and the reading bound

The Goodspeed corpus is scattered across fifteen-plus years and
venues — a personal blog, 25+ conference talks (DEF CON, CCC, REcon,
ShmooCon, ToorCon, HOPE, TROOPERS, Summercon, Hacktivity), five
PoC||GTFO essays inside a 17-issue journal, open-source tools, and
one 408-page book. The honest bound: the method-bearing long-form
artifacts and records are read and dated below; the journal issues,
the book's full text, the talk videos, and the tool source trees
are stated as BOUNDED — not line-read — and no distillation line
cites them beyond what their public records state.

| Artifact | Class | Year | Read status |
| --- | --- | --- | --- |
| "Promiscuity is the nRF24L01+'s Duty" — travisgoodspeed.blogspot.com | long-form blog (own) | 2011 | READ-FULL |
| "Emulating USB Devices with Python" (the Facedancer method) — travisgoodspeed.blogspot.com | long-form blog (own) | 2012 | READ-FULL |
| GoodFET repository README — github.com/travisgoodspeed/GoodFET | tool record (own) | — | READ-FULL |
| Trainer profile (bio naming packet-in-packet, the MYK82 Clipper dump, Facedancer, GoodWatch, the book) — hardwear.io | professional record (own, third-party hosted) | current | READ-FULL |
| Microcontroller Exploits — Penguin Random House / No Starch book page (synopsis; Sept 10, 2024; 408 pp; ISBN 9781718503885) | book record (own) | 2024 | READ-FULL (publisher synopsis; the book itself bounded below) |
| Presenter page with the full talk list 2008–2023 and the REcon 2023 bio — infocondb.org/presenter/travis-goodspeed | consolidated talk record | 2008–2023 | READ-FULL |
| 26C3 speaker page (bio + "Building a Debugger") — fahrplan.events.ccc.de | conference record | 2009 | READ-FULL |
| PoC||GTFO contents (his five essays identified: "iPod Antiforensics", "Serena Butler's TV Typewriter", "Shellcode for MSP430", "Packet-in-Packet Mitigation Bypass", "Intro to Chip Decapsulation") — nostarch.com/gtfo | journal contents record | 2013– | READ-FULL (contents) |
| "Recent Experiments with Mask ROMs" (REcon 2023) — the Class Central course-overview rendering of the talk ("a photographic method for extracting mask ROM data... when the debugging protocol is undocumented") | talk abstract (rendered) | 2023 | READ (rendered abstract) |
| "Practical Attacks against the MSP430 BSL" (25C3) — the fahrplan attachment record: "a side-channel timing attack against the MSP430... voltage glitching to attack a disabled BSL" | paper (own) | 2008 | READ (title + abstract record; PDF binary bounded) |
| Blog index — titles 2012–2013 ("Wardriving for Zigbee", "Emulating USB DFU to Capture Firmware", "Hillbilly Tracking of Low Earth Orbit Satellites") | blog index | 2012–2013 | READ (index) |
| MSP430fet project page — sourceforge (open-source MSP430 flash protocol implementation, begun by Goodspeed) | tool record | 2008 | READ (about page) |
| IM-ME records — Hackaday 2010 post + tag pages ("authored the IM-ME flashing guide"; the toy's TI CC1110 sub-GHz radio; spectrum analyzer conversion; GoodFET-based flashing) | press/project record | 2010 | READ (press, multi-source: Hackaday, RS DesignSpark, arduino.cc forum) |
| "A Keynote in Praise of Junk Hacking" (Hacktivity 2013) — venue record; the Hackaday-recorded gloss: "hacking on junk lets us focus on the process — the hack itself — rather than getting distracted by the outcome" | keynote record + press gloss | 2013 | READ (record + press) |
| Fight to Repair EP 12 "Hillbilly hacker Travis Goodspeed on junk hacking" — episode teaser (the IM-ME re-flashing story) | podcast record | current | READ (teaser only — transcript bounded) |
| Documented X post @travisgoodspeed — mask-ROM row/column marking, "positions of 1024 bits" in the green color channel | documented post | 2022–2023 window | READ (captured) |
| Wardriving for Zigbee — Dangerous Prototypes record | press record | 2012 | READ (press) |
| The PoC||GTFO journal issues (17 issues; his five essays are individually attributed in the No Starch contents) | journal corpus | 2013– | BOUNDED: not line-read; his essays cited via the contents record |
| Microcontroller Exploits (the full 408-page text) | book (own) | 2024 | BOUNDED: the synopsis read; its techniques enter the organ at synopsis level only (STM32F0 one-word-per-reset; STM32F1 hour-long exception leak; MSP430 camera-flash extraction; the indexed survey) |
| The 25C3/26C3 PDF binaries; the talk videos (REcon 2023 et al.); the GoodFET/Facedancer/GreatFET source trees; the Qt mask-ROM tool and the web-API repos | primary artifacts | 2008–2023 | BOUNDED: README/abstract/record level; cited only at that level |

## 2. The psych-read — documented behavior, per lens

* **L1 heuristics** (repeating shortcuts, ≥ 3 independent artifacts
  each):
  * Debug-port-first entry — MSP430fet (2008), "An Open JTAG
    Debugger" (DEF CON 17, 2009), "Building a Debugger" (26C3,
    2009), "Building hardware for exploring deeply embedded systems"
    (REcon 2010).
  * Build the missing instrument — MSP430static (2008), GoodFET
    (2009), Facedancer (2012), GoodWatch (2018), the Qt mask-ROM
    tool (ShmooCon 2023): five tools across fifteen years.
  * Cheap-rig junk hardware — the IM-ME guide (2010), the Next HOPE
    badge as the sniffer rig ("My target hardware is the conference
    badge that I designed for the Next Hope", 2011), the Hacktivity
    2013 keynote doctrine.
  * Bus-to-userland-Python — the GoodFET README ("quickly exposing
    embedded system buses to userland Python code"), the Facedancer
    post ("all of the complicated software is in Python on one
    workstation", 2012), the nRF24 client commands ("goodfet.nrf
    autotune", 2011).
  * Datasheet-as-hypothesis — the 25C3 attacks against the
    documented BSL protection (2008); the 2011 register move ("The
    datasheet claims... the only valid lengths are 3, 4, or 5
    bytes. Setting this value to 00b gives a 2 byte match"); the
    2024 book's per-chip protection discrepancies (synopsis level).
* **L2 obsession** (the multi-year arc): reading firmware out of
  chips configured not to allow it — the BSL timing and glitch
  attacks (2008), quantitative glitch measurements (2009), chip
  decapsulation taught in PoC||GTFO ("Intro to Chip Decapsulation"),
  the MYK82 Clipper chip firmware dump (trainer-profile record),
  mask-ROM photographic extraction (REcon 2023; ShmooCon 2023 tool;
  RE-basics 2024), and the consolidating book (2024) whose own
  synopsis is the arc's thesis: "how to read the software out of
  single chip computers, especially when they are configured not to
  allow the firmware to be extracted". Alongside it, the radio
  thread: CC2430/EM2xx exploits (2009 bio), nRF24L01+ promiscuity
  (2011), packet-in-packet (ToorCon 13, 2011, with Bratus), ZigBee
  exploitation and wardriving (HOPE 2012; blog 2012), digital
  two-way radio teardowns (TROOPERS16; Summercon 2016 "Mad Dog
  380"), polyglot radio modes (REcon 2015, with Bratus).
* **L3 aesthetics** (his own words/titles, cited): "Promiscuity is
  the nRF24L01+'s Duty" (2011 title); "Real Men Carry Pink Pagers"
  (ToorCon 12, 2010, with Ossmann); "Hillbilly Tracking of Low
  Earth Orbit" (30C3 2013 / blog); "a nifty little tool" (GoodFET
  README); the REcon 2023 bio — "driving a fleet of Studebakers and
  knowing all the best dogs by name at his corner bar"; the
  junk-hacking doctrine — "hacking on junk lets us focus on the
  process — the hack itself — rather than getting distracted by the
  outcome" (Hacktivity 2013, via the Hackaday gloss); "A Keynote in
  Praise of Junk Hacking" (the title itself).
* **L4 failure mode** (how being wrong or superseded is handled):
  reproducibility as the standard — the book's promise ("you'll
  learn how to reproduce the results, dumping a chip in your own
  lab") and the PoC||GTFO title's own falsifier demand
  (proof-of-concept or get out); tool succession honesty on record
  — the GoodFET README pointing experimenters to the maintained
  Facedancer fork ("you probably want Kate Temkin's fork") rather
  than to his own stale tree. No public retraction record was
  opened in this census; the correction culture is documented at
  the tool-succession and reproducibility level.
* **L5 cadence** (when the hunt stops and the artifact ships): the
  arc ships as public artifacts on a steady rhythm — blog posts
  (2008–2013), tools released open-source alongside the research,
  one-to-three talks per year 2008–2023, journal essays (PoC||GTFO),
  then the consolidating book (2024). For hardware the artifact IS
  the disclosure: the flashing guide written so the next operator
  follows (IM-ME, 2010), the tool released with the technique
  (GoodFET, Facedancer), the method-bearing writeup at talk time.
  No vendor-deadline cadence is documented in this census; the
  house disclosure policy rides where a vendor is involved.

## 3. Cross-lens rows (the assembly crosswalk inputs)

* **Risk appetite**: targets that refuse to yield — the
  BSL-locked MSP430 (2008), the readout-locked STM32 records (the
  2024 book), the MYK82 Clipper chip (trainer profile), the
  undocumented-debug-protocol mask ROMs (REcon 2023). The lineage
  chooses the target that says no.
* **Evidence standard**: the silicon's measured behavior as
  evidence — claim-vs-measurement discrepancies recorded verbatim
  (the 2011 register claim quoted against the measured 2-byte
  match); reproducibility from a priced parts list as the report's
  bar.
* **Composition habit**: tools built on tools — GoodFET →
  Facedancer → GoodWatch, the Qt tool atop the decap flow; the
  bypass techniques stacked as one escalation — timing, glitching,
  erasure, decap — each priced against the same lock.

## 4. Quarantined opinions (the OPINION gate — never feed distillation)

```
OPINION figure=Travis Goodspeed lens=L3 reading="the 'hillbilly
  hacker' persona and the Studebaker-fleet biography color the
  method" artifact=HIS-OWN-PUBLIC-PERSONA status=admissible-as-
  aesthetic-only (the persona names the aesthetic on record —
  junk hacking, pink pagers, hillbilly tracking, the dogs-by-name
  bio — it is never evidence about method mechanics)
OPINION figure=Travis Goodspeed lens=L1 reading="the
  high-school-teacher framing of the podcast era" artifact=
  PRESS-RECORD-TEASER status=quarantined (the Fight to Repair
  episode teaser names the toy hacking, not the teaching record;
  the documented teaching evidence is the hardwear.io trainer
  profile only; next: an episode transcript or a primary artifact
  would admit the pedagogy claim)
OPINION figure=Travis Goodspeed lens=L4 reading="the MyriaB/
  founding-editor framing around PoC||GTFO's editorial board"
  artifact=JOURNAL-PSEUDONYM-RECORD status=quarantined (the
  journal is edited under the Manul Laphroaig pseudonym; his five
  essays are individually attributed in the No Starch contents —
  the editorial-board specifics were not opened in this census)
```

## 5. The attribution note

Nothing here is his code or his words beyond quoted fragments; the
organ ships his DECISION LOGIC re-expressed as engagement rules
(the charter's A3 assimilation doctrine). Corrections belong in
the registry entry: on record at forge time — the persona and the
teaching framing stay aesthetic-only/quarantined per §4, and the
book's techniques enter the organ at synopsis level only, bounded.
