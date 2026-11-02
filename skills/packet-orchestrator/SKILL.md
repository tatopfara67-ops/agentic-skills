---
name: packet-orchestrator
version: 1.1.0
type: ai-skill
architecture: package
description: Craft-lineage organ built from two verified lineages — Justin Searle's manual-to-structured craft (SamuraiWTF/STFU distributions, NESCOR-methodology ICS testing, protocol dissection teaching) and the Mantis framework (PhonePe) school of workflow orchestration (state-backed pipelines, scanner base classes, schedulers, alerting), with Scapy's layered packet-crafting as the underlying tool lineage. Doctrine: automate only what you have first done manually and understood; translate the manual trace into a structured, state-backed automation one layer at a time; every automation stage keeps the manual path re-runnable beside it; packet-level work means crafting the exact bytes and obSince v1.1.0 the organ carries the executable method layer (A16) — a mechanical critique of the three source lineages' floors (manual craft as performed wizardry with the intent→fields translation unwritten, orchestration demonstrated without mechanical abort gates, packet libraries invoked without send discipline, dissection told as single-shot narration with implicit expectations) shipped as protocol M1–M5: the translation table with enumerated response classes, the state gates that can stop a pipeline, the send rule with its burst ban and per-send ledger, the dissection differential with a written expectation table, and the orchestrator record that makes runs re-walkable. Use when converting manual test logic into repeatable automation, when orchestrating multi-stage workflows with persistent state, when doing raw-protocol differentials, or when an automation must stay debuggable ("automate this manual check", "workflow with state", "packet-level differential", "wire this into the pipeline", "why did the automation diverge").
category: security/craft-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Justin Searle (InGuardians ICS security; SamuraiWTF/SamuraiSTFU; SANS instructor) + Mantis framework (PhonePe, Apache-2.0) + the Scapy packet-crafting lineage (Philippe Biondi)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# packet-orchestrator v1.1.0 — The Searle + Mantis Lineage

## 0. What This Skill Is — and Is Not

* **Is**: the organ for *translation and orchestration*: manual logic
  → structured modules → state-backed workflows, with packet-level
  differentials as the hardest case it must keep honest.
* **Is not**: a framework rewrite. The arsenal already IS the
  orchestration layer (tools as scanner classes, ledger as state,
  scope.csv as config); this organ governs how new manual knowledge
  enters that machine without losing its soul.

## 1. The Lineage (attribution — with one correction)

Two verified lineages, honestly labeled:

* **Justin Searle** — Director of ICS Security at InGuardians, SANS
  instructor, creator of the SamuraiWTF / SamuraiSTFU testing
  distributions. His BlackHat training lineage (NESCOR pentest
  methodology; "pentesting smart grid and SCADA") teaches exactly
  this organ's craft: dissection → entropy analysis → fuzzing, at
  "different levels of network communication", with manual exercises
  on real and simulated devices before any automation.
* **Mantis (PhonePe)** — the open-source (Apache-2.0) Python
  framework for automated asset discovery, recon, and scanning:
  MongoDB-backed state, config-driven workflows, scheduler, alerting,
  distributed scanning, and a scanner base class designed so a new
  scanner integrates "in minutes".
* **Correction on record**: the operator's brief attributed Mantis
  to "Justin Searle & Tim Skappen". Research found no security
  practitioner named "Tim Skappen"; Mantis is the PhonePe project.
  The organ is built on the two verified lineages above. Details:
  references/sources.md — the verification record

## 2. The Five Laws of Translation & Orchestration

1. **Manual first.** Searle's courses teach the manual path on real
   devices BEFORE automation exists. Modern form: any logic worth
   automating is first walked by hand — the manual trace (requests,
   expected responses, decision points) IS the specification the
   automation will be judged against.
2. **Translate layer by layer.** Manual trace → one structured module
   (inputs/observable/falsifier — module-smith's card) → one workflow
   stage (pipeline-smith's contract) → orchestrated campaign
   (template-scanner's set). Each layer keeps the layer below
   re-runnable; you can always drop to the manual path to debug.
3. **State is first-class.** Mantis's design lesson: results live in
   a database, not in shell history — workflows resume, dashboards
   read the same truth the scanners write. Modern form: the ledger IS
   the state; an automation that keeps its own private truth (a
   variable, a temp file not in artifacts/) is a defect.
4. **Extensibility is a base-class contract.** Mantis's "new scanner
   in minutes" is the property that made the framework compound.
   Modern form: every new check enters through the same shape (tool
   or template), never as a bespoke script bolted to the side.
5. **Packet-level means exact bytes.** The Scapy-lineage discipline:
   craft the precise packet (layers as explicit fields), predict the
   precise response, observe the precise delta. A packet differential
   that cannot show its bytes is a summary, not a proof.

## 2.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the three source lineages where they were mechanically weak —
craft performed live with the translation in the demonstrator's hands,
pipelines that cannot state when they stop, `sr1()` loops without count,
rate, or response classing, one weird capture read by one observer against
an expectation nobody wrote down — and ships the executable replacement:
**M1** the translation table (intent → flags/fields/count/rate/response-
classes BEFORE any packet; no response-classes cell = refused probe),
**M2** the state gates (baseline-quiet, error-rate < 5%, state-token
checks; a stage entered without its gate record voids the run), **M3** the
send rule (count + rate floor 1/2 s + timeout 2 × RTT; burst ban on the
5-tuple; stateful sequences walked one reply at a time), **M4** the
dissection differential (per-layer expectation table; anomaly class
reproduces ≥ 2/3 with a compliant control in-window), **M5** the
orchestrator record (gates, sends, pcaps, verdicts, resume cursor — the
record IS the method).

## 3. Procedure — Numbered Actions

1. Walk the logic manually; record every request/response pair and
   decision point (the manual trace = a chain of FACT records).
2. Write the module card for the smallest automatable unit; its
   observable cites the manual trace's records.
3. Implement as ONE stage/tool-shaped unit; run it beside the manual
   path and diff outcomes — the automation must reproduce the manual
   trace's decisions exactly, or be fixed, not trusted.
4. Wire into the workflow with declared state: which records in,
   which records out, where the park note goes.
5. For raw-protocol targets: craft the exact packet (layers, fields,
   checksums as needed); pre-register the expected response class;
   the differential is bytes-in/bytes-out, captured as artifacts.
6. Orchestrate: scheduler/cadence needs are operator decisions;
   alerting is a report-path concern — the automation's outputs are
   records, and only records.
7. Divergence protocol: when automation and manual trace disagree,
   the manual trace wins pending investigation; the divergence is a
   MISTAKE record, and the fix lands in the automation, never in the
   trace.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Manual traces | `http_probe` (one record per request/response) |
| Module cards from traces | `ledger_append` (EXPERIMENT) |
| Automating a stage | arsenal tool or template (template-scanner) |
| Raw-protocol differentials | `arsenal_route` (allowed CLIs) + artifacts for exact bytes |
| Workflow state | ledger + dossier (never private state) |
| Divergence handling | MISTAKE records + re-run |

## 5. Hard Rules

1. No automation of logic that was never walked manually (no
   exceptions; "it looked simple" is where pipelines rot).
2. The manual path stays re-runnable beside every automated stage.
3. State lives in the ledger — private automation state is a defect,
   not a convenience.
4. Packet differentials show their bytes (artifacts) or they did not
   happen.
5. Automation diverging from the trace is a MISTAKE record and an
   automation fix — the trace is never "updated to match".

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Translating manual logic into modules | references/mindset.md |
| Orchestrating workflows with state | references/playbook.md |
| Lineage verification, incl. the Mantis attribution correction | references/sources.md |
| Grading the source lineages, translating intent, holding the gates | references/method-upgrade.md |
