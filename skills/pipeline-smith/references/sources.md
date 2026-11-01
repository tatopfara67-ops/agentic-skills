# sources.md — the Tomnomnom lineage, verified

## Primary sources (consulted)

* **github.com/tomnomnom** — the profile and tool repositories:
  assetfinder, httprobe, gf, meg, gron, waybackurls, qsreplace.
  Confirmed: "Open-source tool maker, trainer, talker, fixer, eater"
  profile; the tool set's single-purpose stdin/stdout design is
  directly observable in the repos.
* **"Confessions of a Toolmaker" — Tom Hudson (tomnomnom), Ekoparty
  2024 (Bug Bounty Argentina)** — talk existence, title, and framing
  confirmed ("…tools, what makes a good tool, how I make tools, how
  and why you should write your own tools too"). Content points
  (what makes a good tool) referenced at the level the public record
  shows.

## Secondary sources (consulted)

* **Daniel Miessler, "A @TomNomNom Recon Tools Primer" (2021)** —
  "tools with the Unix philosophy of doing one specific thing really
  well. gf, httprobe…" — the philosophy attribution is explicit.
* **Bishop Fox, "TomNomNom AMA"** — AMA on "the pen testing tools
  he's created over the years".
* Live recon demonstrations with Tomnomnom (NahamSec session on
  Shopify recon) — referenced as demonstration of the pipeline in
  practice, not as a text source.

## Claims and confidence

* High confidence (directly observable): the tool set, the
  single-purpose design, passive-first sourcing in assetfinder,
  minimal liveness in httprobe, pattern packs in gf, uniform-path
  diffing in meg, JSON flattening in gron.
* Medium confidence (talk-level, public record only): the
  toolmaking-craft principles ("what makes a good tool") and the
  pro-sampling stance under budget pressure. These are consistent
  across the AMA/talk record and with the tools' observable design,
  but no full transcript was consulted — flagged accordingly.
* Not claimed: any private methodology, any un-published workflow,
  or the content of paid training.

## What this organ does NOT include

* No Tomnomnom code is redistributed; the tools are described at the
  behavior level (stdin/stdout/one-job) as engineering patterns.
* The organ does not depend on Go or on the specific binaries; the
  arsenal re-expresses the pipeline discipline in ledger records.
