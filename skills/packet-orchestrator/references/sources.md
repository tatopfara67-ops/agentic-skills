# sources.md — the Searle + Mantis lineages, verified (with the attribution correction)

## The correction, stated plainly

The operator's brief listed "Justin Searle & Tim Skappen (Mantis)" as
one entry. Research findings:

* **No security practitioner named "Tim Skappen" was found.** The
  closest name match is a transactional/IP lawyer (different person,
  different field). The doctrine's admission criteria (public,
  documented, attributable) fail for this attribution — so it is not
  carried into the organ.
* **Mantis exists and is verifiable — as the PhonePe project**
  (github.com/PhonePe/mantis, Apache-2.0): "a command-line framework
  designed to automate the workflow of asset discovery,
  reconnaissance, and scanning", with MongoDB state, distributed
  scanning, dashboard integration, scheduler, alerting, and the
  "integrate new scanner in minutes" base-class recipe.
* **Justin Searle is verifiable independently**: Director of ICS
  Security at InGuardians; SANS profile; creator/maintainer of
  SamuraiWTF and SamuraiSTFU; BlackHat trainer whose course
  ("Pentesting Smart Grid and SCADA with SamuraiSTFU") is built on
  the NESCOR methodology (a US Department of Energy project) and
  sequences manual protocol dissection → entropy analysis → RE →
  fuzzing on real+simulated devices.

The organ therefore stands on two verified lineages (Searle's
manual-to-structured craft; Mantis's orchestration design) plus the
credited Scapy tool lineage — and this file keeps the correction on
record. Nothing else in the operator's brief required correction.

## Primary sources (consulted)

* **github.com/PhonePe/mantis** + **phonepe.github.io/mantis**
  (documentation: introduction, features, config, "New Scanner
  Integrations" recipe, scanner base class, DB models, distributed
  scanning) — the orchestration design points in mindset.md are from
  these pages.
* **BlackHat US 2013 training page** — "Pentesting Smart Grid and
  SCADA with SamuraiSTFU", Justin Searle: the NESCOR methodology
  basis, the "network mediums vs network protocols" distinction, the
  capture → entropy → reverse-engineering → fuzzing sequence, and
  the real-world + simulated device mix. Read in full.
* **SANS.edu profile — Justin Searle** ("Director of ICS Security at
  InGuardians; ICS security architecture design and penetration
  testing").
* **SamuraiWTF materials** (Searle's web-testing-framework lineage,
  e.g. the BH EU 2012 deck "Assessing and Exploiting Web
  Applications with Samurai-WTF") — consulted for the
  methodology-in-a-distribution pattern.

## Credited tool lineage (not a consulted source for specific claims)

* **Scapy** — Philippe Biondi, "Scapy: a powerful interactive packet
  manipulation program" (the paper and the tool). Credited as the
  packet-crafting lineage the organ's exact-bytes law descends from;
  no specific Scapy feature is claimed as consulted evidence.

## What this organ does NOT include

* No Mantis code, no SamuraiWTF/STFU distribution content — design
  lessons only, at the behavior level.
* No claim about Searle's private methodologies beyond the public
  training/course record.
* No "Tim Skappen" lineage — by the doctrine's rules, what cannot be
  verified cannot be assimilated.

## Confidence

High for both carried lineages (primary pages read directly). The
correction itself is high-confidence: multiple targeted searches
found no security-context "Tim Skappen", while Mantis's actual
provenance is documented in its own repository.
