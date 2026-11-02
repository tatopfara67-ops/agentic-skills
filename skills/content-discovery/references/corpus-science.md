# corpus-science.md — the Miessler lineage layer for content-discovery (v2)

Load when choosing or composing ANY wordlist beyond rung 0, when a
second walk is being justified, or when someone proposes a mega-list.

## 1. The Corpus Is Data, Not Vibes

The SecLists corpus (maintained by Daniel Miessler) is organized in
families that map DIRECTLY onto this organ's rungs — the mistake is
grabbing by size instead of by family:

| SecLists family | Feeds | Discipline |
| --- | --- | --- |
| Discovery/Web-Content | rungs 1–3 of the ladder | framework/technology-specific lists, one marker at a time |
| Discovery/DNS | subdomain-hunter ONLY | never fired at HTTP paths |
| Passwords / Usernames | never in this organ | authentication surfaces are a different scope row (see §5) |
| Miscellaneous (APIs, raft, common) | rung 2 convention lists | composed, not blasted whole |

Field rule: a walk is justified by which FAMILY it draws from; "the list
was big" is not a reason, it is the slop this organ exists to prevent.

## 2. Composition Law

A rung-1/2 list is ASSEMBLED, never downloaded whole:

* framework marker (evidence) → the framework's Discovery list →
  intersect with what the deployment can plausibly mount (php list on a
  JSP stack is noise with a HTTP label).
* convention derivation: resource names from JS/API specs × version
  prefixes SEEN in evidence — the spec is the corpus here, SecLists is
  the seasoning.
* cap arithmetic from `wordlists.md` applies unchanged:
  `probes = min(words × exts, max_requests)`; composition that busts the
  cap splits into a parked backlog row, not a silent truncation.

## 3. Extension Derivation From the Observed Stack

Extensions are derived, not defaults beyond the standard round:

* server/casing markers (`X-Powered-By`, file casing in observed 200s)
  decide `.php` / `.aspx` / `.jsp` rounds;
* CMS or framework marker decides plugin/theme path rounds;
* the archive round (`.zip .bak .tar.gz .sql`) runs only when a signal
  earned it — a found `backup.zip` triggers the NEIGHBORHOOD round
  (siblings of the found name), which is where the yield actually lives.

## 4. Re-Calibrate When the Base Moves

The negative-profile (three junk-path control probes) belongs to a BASE
URL. Any second walk against a different base — a vhost, a path prefix,
an API root — recalibrates first; soft-404 shapes differ per handler.
Re-using rung-0's calibration for a new base is the classic
false-positive generator this organ was built to kill.

## 5. The Scope Wall Around the Other Families

The corpus also carriesPasswords/default-credentials lists. In THIS
organ they are out of bounds: authentication-surface testing (default
logins, credential stuffing shapes) runs only under an explicit scope
row naming it, as its own hypothesis family with its own audit story.
Parking is one ledger note; crossing the wall silently is an engagement
ending.

## 6. The Craft, Stated As Five Field Rules

1. Choose by family, not by size.
2. Compose rung-1/2 lists from evidence; never blast a mega-list.
3. Extensions derive from the observed stack; archives follow signals.
4. New base URL → new calibration round, always.
5. The password families live behind their own scope wall — park, don't
   peek.
