# mindset.md — the HD Moore decision logic, translated

## 1. The mind, as observed in the sources

* **Composition over monoliths.** Metasploit's revolution was not any
  single exploit — it was the shape: `exploits/`, `payloads/`
  (`singles`, `stagers`, `stages`), `auxiliary/`, `encoders/`, `nops/`
  — separate trees that combine at run time. The framework tree (as
  shipped today) still shows it: a stager module is 40 lines that
  carries `Handler`, `Stager.Offsets`, and a payload blob — everything
  else is composition. An exploit module's job ends where the payload
  module's job begins.
* **Auxiliary is a first-class citizen.** Scanners and fuzzers live in
  the same module system as exploits — reconnaissance written with
  the same rigor as exploitation. In the arsenal, that is the entire
  thesis: `content_discover` and `http_probe` are modules of the same
  standing as any "exploit" hypothesis.
* **Metadata is load-bearing.** Every module declares Name,
  Description, Author, License, Platform, Arch, References, Rank,
  DisclosureDate. The framework can therefore *reason* about modules
  (prefer reliable, avoid noisy) without reading their code — the
  1990s script pile could not.
* **Reuse across targets is the point.** A module written once for a
  CVE runs against every vulnerable instance the internet offers.
  The unit of work is the *class*, not the instance.
* **Then, Sonar (2013+): measure the world.** Weekly scans of twelve
  UDP services, full-responsibility open data publication, and decks
  like "Internet of Threats" that say which exposed services "can
  lead to a direct compromise". The claim "X is dangerously common"
  became a dataset with a denominator and a cadence.

## 2. The translation table (2003/2013 → arsenal)

| Then | Now (organ behavior) |
| --- | --- |
| exploit / payload / stager / handler split | access proof / impact proof (canary) / delivery (probe spec) / capture (ledger record) as separate artifacts |
| module rank (manual…low) | hypothesis prior + n_runs reproduction rate |
| module References (CVE, advisory) | R-NNN citations + advisory URLs on the H-card |
| auxiliary = scanners as modules | recon tools are modules of equal standing |
| payload staging (small first) | bounded proofs: one cheap differential before any deep payload |
| Sonar weekly cadence, open data | CONTROL baselines with denominators; prevalence claims cite the probe set |
| "most should never be exposed" | exposure verdicts phrased against the baseline, recorded |

## 3. The module card (this organ's unit of thought)

```
module: <name>                    e.g. unauth-debug-route
class:    <surface class> / <VRT class>   debug-interface / exposed_portal
inputs:   <target>, <preconditions>
observable: <the response delta that counts>
falsifier:  <the neighbor that must NOT move>
rank:     <prior %> — from <base rate source>
refs:     R-NNN, R-NNN; <advisory URLs>
runs:     <n_runs> / stable delta? <y/n>
status:   LEAD | MODULE (reusable) | DEPRECATED (why)
```

A module card that cannot fill every field is not ready to run —
that is the discipline, and it is cheap.

## 4. Failure modes this organ exists to kill

* The one-off script that "worked once" and gets re-run from memory
  on the next target with new parameters and old assumptions.
* Impact theater: "I got a 200" presented as impact. Access and
  impact are different proofs; Moore's payload tree exists because
  the distinction is real.
* Unranked confidence: "this is very reliable" from a single run.
* Prevalence vibes: "everyone has this bug" with no denominator —
  Sonar's whole contribution was the denominator.

## 5. What the engine already enforces (do not re-implement)

* The auditor requires the differential triad + canary + impact-chain
  before a CONFIRMED finding ships — the access/impact split, made
  mechanical.
* EXPERIMENT pre-registration (partitions before outcomes) is exactly
  module metadata-before-execution.
* `arsenal_route`'s sqlmap `--batch` rule keeps CLI oracles as
  measurable oracles, not adventures.
