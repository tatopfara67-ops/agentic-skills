# mindset.md — the Searle + Mantis decision logic, translated

## 1. The minds, as observed in the sources

**Searle (the teaching lineage):**

* His SamuraiSTFU/SamuraiWTF distributions are methodology encoded as
  an environment: a curated toolset plus structured exercises, built
  so that the manual craft is learnable and repeatable — the
  distribution is the lesson.
* The BlackHat training outline sequences craft deliberately: capture
  and analysis → entropy analysis of payloads → reverse engineering
  unknown protocols → protocol fuzzing; and it tests "different
  levels of network communication" — "testing of network mediums vs
  network protocols" as distinct questions.
* It is built on a FORMAL methodology (NESCOR's, a US DOE project) —
  manual pentest logic written down as process, which is the exact
  boundary this organ polices: manual logic, structured.
* Exercises run on "a mixture of real world and simulated devices" —
  ground truth available for every lesson; automation is never asked
  to grade itself.

**Mantis (the orchestration lineage):**

* The docs' own framing: "automated asset discovery, reconnaissance,
  and vulnerability scanning… stored in a robust MongoDB database…
  integrated with any dashboard supporting MongoDB integration."
  State is the product; scans are writers.
* "Why another RECON automation framework?" — answered with
  composability: config-driven workflows, scheduler, distributed
  scanning, advanced alerting, and the scanner base class whose
  whole point is "integrate a new scanner in minutes" (new tool
  class, new API scanner class, config entry, Dockerfile line — the
  docs literally sequence the integration as a recipe).
* Apache-2.0, "use responsibly" disclaimer — an orchestration culture
  that still draws the authorization line.

**Scapy (the tool lineage, credited):**

* Philippe Biondi's Scapy paper and tool established packet crafting
  as composition: decode, build, send, capture — layers as
  composable objects. This organ borrows the *discipline* (exact
  bytes, explicit fields), not the tool.

## 2. The translation table (lineage → arsenal)

| Lineage behavior | Organ behavior |
| --- | --- |
| STFU/WTF as methodology-in-an-environment | the arsenal as methodology-in-a-server: tools + contract + auditor |
| NESCOR: manual pentest logic formalized | manual traces formalized as module cards |
| capture → entropy → RE → fuzz sequence | staged analysis: observe, characterize, model, then perturb |
| mediums vs protocols as distinct questions | transport questions and application questions never fused |
| real+simulated ground-truth devices | the lab (target_app/christmas_lab) as ground truth |
| Mantis: DB-backed results, dashboards | ledger as the single state; dossier/report read it |
| scanner base class + config + recipe | one shape for every new check (tool/template), config-driven |
| scheduler + alerting | cadence = operator decision; outputs are records, alerts are downstream |
| Scapy's exact-bytes craft | packet differentials with byte-level artifacts |

## 3. The translation ladder (this organ's unit of thought)

```
L0  manual trace      — hand-walked requests/responses, FACT records
L1  module card       — inputs/observable/falsifier citing the trace
L2  automated stage   — one tool-shaped unit; runs beside the manual path
L3  workflow          — stages + declared state (records in/out)
L4  campaign          — cadence + surface set + template set, orchestrated
```

Rules of the ladder: you may only stand on the rung below you; every
rung keeps the rungs below re-runnable; skipping rungs is how
automation inherits unexamined assumptions (and how reports inherit
unverifiable claims).

## 4. Failure modes this organ exists to kill

* "Automate first, understand never" — scripts that encode a guess
  about how the target works, then get trusted because they run.
* Automation state that lives outside the ledger (a JSON here, a
  variable there) — unreproducible, unauditable, and always stale.
* Side-door integrations: the "quick script" bolted beside the
  pipeline that no base-class contract ever sees.
* Packet claims without bytes: "the protocol responded oddly"
  with no captured artifact — a summary of a memory of a packet.
* Traces edited to match buggy automation (the inversion that
  quietly rewrites history — the ledger's append-only law exists
  precisely for this).

## 5. What the engine already enforces (do not re-implement)

* Append-only ledger — divergence handling cannot rewrite the trace.
* Tools-as-scanner-classes + scope.csv config — Mantis's base-class
  property, already the arsenal's shape.
* Artifacts on disk for every probe — the exact-bytes law, half
  mechanical already.
