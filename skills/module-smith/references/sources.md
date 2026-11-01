# sources.md — the HD Moore lineage, verified

## Primary sources (consulted)

* **Metasploit Framework source tree, github.com/rapid7/
  metasploit-framework** — module architecture verified directly:
  `modules/exploits/`, `modules/auxiliary/`, `modules/payloads/
  {singles,stagers,stages}/`, `modules/encoders/`, `modules/nops/`;
  stager modules read in full (e.g. `payloads/stagers/linux/x86/
  find_tag.rb`: `Msf::Payload::Stager`, `Handler`, `Stager.Offsets`,
  cached size 37 bytes) — the exploit/payload/stager/handler
  separation and per-module metadata (Name, Author, License,
  Platform, Arch, References) confirmed as shipped, not as folklore.
* **HD Moore, Project Sonar decks** — hdm.io/decks/
  UNITED_2015_Internet_of_Threats_A.pdf ("Project Sonar scans 12
  unique UDP services each week… Most should never be exposed to the
  internet… Many can lead to a direct compromise"), consulted via
  search-indexed text.
* Project Sonar announcement history (2013) and its continuation
  under Rapid7, confirmed through multiple independent write-ups
  (Dark Reading "#ScanAllTheThings" coverage; academic citations in
  theses and "Open Data: Internet Scale Telemetry").

## Secondary sources (consulted)

* Metasploit history summaries (framework first released October 2003
  by HD Moore; Perl → Ruby rewrite) — consistent across several
  introductory decks and course materials.
* Academic use of Metasploit as a study object (Masaryk University
  thesis "The use of Metasploit tool in development lifecycle") —
  consulted for the framework's module counts and role framing.

## Not consulted / not claimed

* Metasploit Pro (commercial) internals; specific exploit techniques
  shipped in modules — the organ cites architecture, not payloads.
* Moore's post-Rapid7 work (critical-intelligence/reverse) beyond
  what the Sonar record shows.

## Confidence

High for the module architecture (verified in the shipped source
tree) and for Sonar's existence/cadence/purpose (deck + multiple
independent sources). Medium for biographical details beyond the
public record. Quotes in mindset/playbook are paraphrases of the
cited deck text except where quotation marks are used.
