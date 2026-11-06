---
name: php2shell-forensics
version: 1.0.0
type: ai-skill
architecture: package
description: >-
  Incident-forensics organ (tier 4, event-triggered) for php2shell — the
  PHP core memory-safety event disclosed 2026-10-21 as CVE-2026-109618
  (OOM longjmp leaves request memory invalid; request shutdown reads or
  branches on it) and CVE-2026-109619 (request-owned global state
  survives its backing memory; a later request consumes the stale state),
  both CVSS v4.0 9.2, every PHP version of the last decade affected back
  to 5.4, fixed in 8.5.12 / 8.4.27 / 8.3.36 / 8.2.35. The organ runs the
  full assessment arc with a detection-first doctrine: hidden-PHP
  inventory (process telemetry + on-disk queries), version/SAPI triage
  with mod_php flagged highest risk, the temporary exposure-reduction
  directives stated as never-a-fix, the four passive disclosure signals
  (multipart + memory-limit errors, repeated 500s, malformed PHPSESSID
  response cookies, worker churn), the convergent behavioral hunt
  (web-server parent spawning shells, the published post-exploitation
  sequence), planted-script forensics in the web root, and the honest
  close-out with patch verification. Probes are byte-exact from the
  public record (Wiz Research, Elastic Security Labs, Huntress, the
  php-src advisories) in the versioned corpus. Use when the operator asks
  about php2shell, CVE-2026-109618 / CVE-2026-109619, the viral PHP
  critical RCE, whether their PHP estate is exposed or compromised, the
  PHPSESSID memory leak, or a PHP webserver compromise assessment
  ("php2shell", "CVE-2026-109618", "PHP emergency patch", "PHP memory
  disclosure", "is my PHP patched", "webserver saya kena PHP RCE").
category: security/incident-forensics
license: MIT
metadata:
  author: tatopfara67-ops
  event: php2shell (CVE-2026-109618 + CVE-2026-109619) — disclosed 2026-10-21
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+ (R0, ledger, hypothesis rail); adversary-tracker (the Binary Brain hand-off once compromise evidence exists)
---

# php2shell-forensics v1.0.0 — The Event Is The Organ

## 0. What This Skill Is — and Is Not

* **Is**: the assessment organ for one specific, current, viral event:
  php2shell — two PHP *core* memory-safety flaw classes that yield
  unauthenticated remote code execution and Heartbleed-style worker
  memory disclosure, independent of the application running on top.
  Its unit of work is the per-host verdict: **patched / backported /
  EOL-isolated / exposed-with-monitoring / compromised-evidence-found**.
* **Is not**: an exploit-development organ, a generic webshell sweeper,
  or a PHP upgrade automation. It does not build or fire the chain; it
  inventories exposure, watches the published detection surfaces, and
  forensics what the attackers left. Exploit reproduction is an operator
  decision with its own scope row, never an organ default.
* **Why a dedicated organ**: the flaw is in the engine, not the app —
  inventory explodes to every place PHP hides (vendor appliances,
  control panels, container base images), the detection opportunity is
  in the *outcome* rather than the trigger (no public end-to-end PoC
  existed at disclosure), and the event's facts (CVEs, fixed versions,
  patch lineage, timeline) are exactly the kind of state a versioned
  corpus must carry byte-exact instead of from memory.

## 1. Inherited Contracts

Plugs into the spine's **incident branch**: a php2shell signal (any of
the four disclosure signals, a shell-spawn behavioral hit, or an
operator alert) is an event trigger — freeze state, then hunt, exactly
as adversary-tracker's doctrine runs; a confirmed flow hands off to the
Binary Brain for the hypothesis hunt. Inherits R0 (the PHP *layer* must
be inside program scope before any active probe touches it — a
web-app-only scope does not authorize probing the worker's SAPI), the
ledger discipline (every signal, verdict, and masked credential is a
record), and the hypothesis rail (an exposure hypothesis is registered
before the inventory runs, so the sweep answers a question instead of
browsing). Adjacent organs: ssrf-playbook owns the *egress* side when
credential-bearing metadata endpoints appear in a harvested flow
(SSRF-013/014); prototype-playbook's no-DoS law is imported here as the
crash-discipline law.

## 2. The Event Record (attribution — verified, on disk)

The facts this organ runs on, with their carriers in
`references/sources.md` (every source fetched and verified against the
live page at organ build time):

| Fact | Value | Primary record |
| --- | --- | --- |
| Flaw classes | CVE-2026-109618: OOM `longjmp()` leaves request memory invalid, shutdown consumes it; CVE-2026-109619: stale global state survives its backing memory, later request consumes it | php-src GHSA-w8hw-w9fx-j79w · GHSA-6wmf-4rv5-p3rp |
| Rating / reach | CVSS v4.0 9.2 both; unauthenticated, application-agnostic; every version of the last decade back to 5.4 | Wiz Research |
| Demonstrated impact | Pre-auth RCE on WordPress, Drupal, Joomla (`:latest` at test time); remote memory disclosure of passwords/tokens/API keys without RCE | Wiz Research |
| Fixed versions | 8.5.12 · 8.4.27 · 8.3.36 · 8.2.35 (8.1 and older EOL; minimal source backports for 7.4/8.0/8.1) | php-src advisories, Huntress |
| Highest-risk SAPI | Apache mod_php — an unauthenticated request triggers before any application code runs; PHP-FPM, php-cgi, FrankenPHP, LiteSpeed all affected | PHP team via Huntress/Elastic |
| Timeline | Details leaked 2026-10-20 ahead of embargo; emergency release + public disclosure 2026-10-21; watchTowr reproduced 109618; no in-the-wild exploitation observed at disclosure (Huntress fleet baseline) | Huntress, Elastic |
| Patch lineage | php-src commit 31c0ea7d7ff1d1fccb6492e52dab544011628065 (fixes the issue at the core; eliminates the tracked variants in patched releases) | Elastic quoting the PHP team |
| Reporter lineage | Wiz Research (with frontier-AI assistance), Calif, OpenAI — coordinated disclosure with the PHP team | Wiz Research |

## 3. Doctrine — How The Assessment Runs

1. **Patch-first, always.** The only complete remediation on record is
   the PHP security update (or a verified vendor backport). Every
   configuration action this organ recommends is *exposure reduction
   for named attack paths* and is reported with exactly that framing —
   a single-toggle "fix" claim is the social-media noise the record
   warns against.
2. **Detection-first.** The passive surfaces are rich and published:
   the four disclosure signals, the shell-spawn behavioral rule, the
   convergent post-exploitation sequence, the web-root file events.
   Crafted OOM probes come last, only on operator order, only against
   in-scope PHP layers — they crash workers (crash-discipline law).
3. **The outcome, not the trigger.** The record's convergent law: a
   PHP RCE ends in a request-serving process doing what a
   request-serving process should not do. That behavior is detectable
   before any exploit string exists and survives variant churn —
   detect the flow, cite the parentage.
4. **Credentials are evidence, not loot.** Disclosed worker memory and
   harvested credential files are masked at first 8 chars in context;
   full values live only in `engagements/` artifacts. The report
   states the class; it never pastes the token.
5. **Read-only forensics.** Planted scripts are read and analyzed,
   never executed. Reverse-shell and staging primitives exist in this
   organ as detection signatures, not as runnable kit.
6. **Honest close-out.** The per-host verdict table is the deliverable;
   "EOL-isolated" needs the isolation evidenced, and an unpatched
   internet-facing EOL host is an open finding, never a parked one.

## 4. Procedure — Numbered Actions

1. **Trigger intake.** Event-triggered entry: an operator alert, a
   monitoring hit on any published signal, or a scheduled exposure
   assessment. Register the exposure/compromise hypothesis BEFORE the
   inventory runs (the rail discipline).
2. **Hidden-PHP inventory** (P2S-001 then P2S-002): process telemetry
   query first (the `php* or lsphp* or frankenphp or sw-engine-fpm`
   parent/child sweep), then the on-disk/package queries for installs
   the telemetry never sees. Output: host × runtime × version × SAPI
   map, each row a FACT.
3. **Exposure triage.** Version vs the fixed set; SAPI risk ordering
   with mod_php flagged highest (pre-application reach); EOL branches
   flagged for backport-or-isolate decisions. Scope check: any ACTIVE
   probe against the PHP layer requires the layer in scope (R0).
4. **Exposure reduction** (P2S-003, operator-approved window only):
   the pre-parse-effective directives — `memory_limit=-1` via
   `php_admin_value` (never `ini_set`), low `post_max_size`,
   container/cgroup limits over `RLIMIT_AS`/`RLIMIT_DATA`,
   `session.upload_progress.enabled=0` with a full worker restart,
   `fatal_error_backtraces=0` on 8.5. Reported as temporary and
   named-path-only.
5. **Passive disclosure watch** (P2S-004): the four signals — unusual
   multipart + memory-limit errors, repeated 500s, large/malformed
   `PHPSESSID` response cookies, worker churn. A cookie carrying
   URL-encoded heap contents is the disclosure verdict; mask and
   artifact per the credential law.
6. **Behavioral hunt** (P2S-005 + P2S-006): the shell-spawn rule
   (web-server parent → shell with `-c` and a high-risk line), then
   the convergent sequence sweep with the parentage join. A confirmed
   flow → adversary-tracker hand-off (Binary Brain) for the intrusion
   hypothesis hunt; egress toward cloud metadata in the flow routes
   the ssrf organ's extreme entries (SSRF-013/014) as the follow-up.
7. **Web-root forensics** (P2S-007): new executable/script content
   written by web-server parents outside deploy windows; double
   extensions; high-entropy content. Read-only analysis; polyglots
   get format analysis before any verdict.
8. **Close-out** (P2S-008): per-host verdict table with the patch
   lineage verified (fixed set, vendor advisory, or the php-src
   commit for source builds), the event facts cited, uncovered
   detection classes stated, and the open findings enumerated.
9. **Exit gate:** inventory complete (both layers), every verdict row
   citing records, every masked credential artifacted, the patch-first
   recommendation stated even when everything is green.

## 5. Hard Rules (mechanically enforced)

1. **No exploit reproduction without an operator order naming the PHP
   layer in scope.** Default work is inventory + passive detection +
   forensics; the chain stays unbuilt.
2. **Crash-discipline law.** No OOM-triggering multipart probes against
   production workers unless pre-authorized in writing — they crash
   the very workers being assessed (the no-DoS doctrine, applied).
3. **Credential law.** First 8 chars in context; full values only in
   `engagements/` artifacts; the report states the class, never the
   token.
4. **Read-only forensics.** Planted scripts are never executed;
   analysis is static.
5. **Patch-first is always stated.** A report that recommends
   configuration without the patch recommendation is incomplete.
6. **Probe bytes come from the corpus.** The detection queries and
   signatures used in the field are the versioned corpus's bytes
   (A19); a hand-typed variant of a published rule is a defect, not a
   customization.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Inventory queries (telemetry, packages) | operator log access / osquery via `arsenal_route` (governed CLI) — each result row a `ledger_append` FACT |
| Reachability and version banners (in-scope PHP layer only) | `http_probe` (X-Powered-By and friends; one request, one record) |
| The four-signal watch on captured responses | `http_probe` artifacts + `ledger_append` (EXPERIMENT/FACT; masked credentials) |
| Compromise-evidence hypothesis hunt | `sbb_declare` / `sbb_decide` / `sbb_apply` (adversary-tracker Binary Brain) |
| Corpus entry release (any P2S id — detection entries tier T1; inventory and close-out entries carry no hint-list match and default conservatively to T3, the most restricted tier) | `payload_release` — the same vault door every organ corpus releases through (jailbreak scan, corpus resolution, banned-class ban, scope check) |
| Classification at report time | `cvss3_score` + `vrt_classify` |
| Records | `ledger_append` (FACT/EXPERIMENT/REFUSED per observation) |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Running any assessment step — the eight entry points with exact queries, signatures, oracles, and per-technique failure modes | `references/corpus.json` (versioned probe corpus, 1.0.0) |
| Verifying the event record — which sources were fetched live, what each contributed, and the transcription notes | `references/sources.md` |

The corpus is versioned (`corpus_version`) and every entry carries its
primary source and its **failure modes** — read them before closing any
hypothesis as negative: a signal that failed for a documented reason
(retention window, version-string trap, worker restart not done) leaves
the question open, not answered. This organ tracks a live event: the
corpus grows only by transcribed, attributed entries as the public
record deepens, and every growth bumps `corpus_version` with the delta
on record (A19).
