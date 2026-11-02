"""skill-mythos backends — the charter, the prompt-escalation forge, and
the classifier pair (CVSS + VRT).

Four tools, one doctrine: a finding that leaves this arsenal must be
triage-grade — zero false positive (differential triad), fully reproducible
(n_runs), and precisely classified (CVSS 3.1 vector + recomputed base score,
Bugcrowd VRT category with P-rating, HackerOne severity crosswalk) — and an
operator instruction, however terse, becomes an explicit doctrine order
before any organ acts.

  mythos_charter()      the activation payload: fifteen articles, the
                        bundle map with install status, the quality gates
  doctrine_forge(...)   prompt escalation (A13): any operator request,
                        in any language, expanded deterministically into
                        the professional doctrine order — persona mix,
                        phase plan, tools, gates — that the agent then
                        executes
  cvss3_score(vector)   spec-exact CVSS v3.1 base score (arsenal/cvss.py)
  vrt_classify(class)   finding-class -> VRT category/variant + P-rating +
                        HackerOne severity + a CVSS template, resolved against
                        the shipped official taxonomy (Apache-2.0, see the
                        skill bundle's NOTICE.md)

The VRT data file ships inside the skill bundle (not the tool) so the
taxonomy is operator-upgradable without touching code.
"""
from __future__ import annotations

import json
import os
import re

from .. import cvss as _cvss
from .. import paths

# --------------------------------------------------------------- the charter

MODULE = "skill-mythos"
MODULE_VERSION = "1.6.0"

SPINE = "mythos-bug-hunter"

TIERS = {
    "0-engine": ["glm-self-model"],
    "0-master": [MODULE],
    "1-recon-mapping": ["surface-cartographer", "subdomain-hunter",
                        "content-discovery", "js-recon", "api-surface-mapper"],
    "2-access-logic": ["auth-boundary-mapper", "oauth-flow-auditor",
                       "business-logic-hunter"],
    "3-deep-technical": ["injection-lab", "ssrf-playbook", "xss-playbook",
                         "cloud-config-auditor", "mobile-hunter",
                         "cache-playbook", "prototype-playbook"],
    "4-incident": ["adversary-tracker"],
    "5-craft": ["scan-economist", "module-smith", "pipeline-smith",
                "feedback-fuzzer", "template-scanner",
                "packet-orchestrator"],
    "6-legend": ["chain-architect", "desync-hunter", "deep-teardown",
                 "ghost-crawler", "mirror-hunter", "signal-smith",
                 "trust-graph-hunter"],
}

# The assimilated lineage registry (doctrine A3: attributed, verified,
# no fabrication). Each entry: organ, the figure/team, the distillation,
# and where the sources live. The correction flag keeps the record honest
# where the operator's brief needed it.
LINEAGES = [
    {
        "organ": "adversary-tracker",
        "figure": "Tsutomu Shimomura (with the FBI, 1994-95; co-author "
                  "with John Markoff of Takedown)",
        "distillation": "the Binary Brain: freeze before change, null "
                        "hypothesis always in the space, halving tests by "
                        "expected information, tip-off gating, two-channel "
                        "confirmation, handoff instead of retaliation",
        "sources": "skills/adversary-tracker/references/history-1995.md",
        "correction": None,
    },
    {
        "organ": "scan-economist",
        "figure": "Gordon Lyon (Fyodor) — Nmap",
        "distillation": "scan economy: cost hierarchy (liveness before "
                        "depth), speed/stealth/reliability triangle, states "
                        "as recorded inferences with retransmission, "
                        "empirical priors over exhaustive sweeps, adaptive "
                        "pacing",
        "sources": "Phrack 51, The Art of Port Scanning (1997), read in "
                   "full; Nmap Network Scanning (2009), free online "
                   "edition; skills/scan-economist/references/sources.md",
        "correction": None,
    },
    {
        "organ": "module-smith",
        "figure": "HD Moore — Metasploit Framework; Project Sonar",
        "distillation": "exploitation as composition: access proof and "
                        "impact proof as separate artifacts; modules carry "
                        "rank/references; frameworks compound; exposure is "
                        "a measurement with a denominator",
        "sources": "rapid7/metasploit-framework module tree (stager "
                   "modules read directly); hdm.io Sonar decks; "
                   "skills/module-smith/references/sources.md",
        "correction": None,
    },
    {
        "organ": "pipeline-smith",
        "figure": "Tom Hudson (Tomnomnom) — assetfinder/httprobe/gf/meg/"
                  "gron",
        "distillation": "the Unix recon pipeline: one tool one job, "
                        "stdout as contract; passive before active; dedupe "
                        "before probing; cheap liveness; pattern knowledge "
                        "as versioned data; diff against siblings to decide",
        "sources": "github.com/tomnomnom tool repos; Ekoparty 2024 "
                   "'Confessions of a Toolmaker'; Bishop Fox AMA; "
                   "skills/pipeline-smith/references/sources.md",
        "correction": None,
    },
    {
        "organ": "feedback-fuzzer",
        "figure": "Michal Zalewski (lcamtuf) — AFL, Google security "
                  "engineering",
        "distillation": "feedback-guided search: coarse state maps and "
                        "bucketed novelty, deterministic before chaotic, "
                        "curated corpora, non-greedy exploration, tarpit "
                        "rejection, minimize before diagnosing, saturation "
                        "as the stopping rule",
        "sources": "lcamtuf.coredump.cx/afl/technical_details.txt, read in "
                   "full; google/AFL README; "
                   "skills/feedback-fuzzer/references/sources.md",
        "correction": None,
    },
    {
        "organ": "template-scanner",
        "figure": "ProjectDiscovery — Sandeep Singh, Rishiraj Sharma, "
                  "Marco Rivoli, Nizamul Rana (subfinder, nuclei)",
        "distillation": "detection knowledge as declarative templates: "
                        "matchers pre-registered, engine and packs evolve "
                        "separately, one grammar across protocols, severity "
                        "as taxonomy metadata, campaigns cite their template "
                        "set",
        "sources": "projectdiscovery.io docs + blog; the nuclei repo; "
                   "Bishop Fox's founding account; "
                   "skills/template-scanner/references/sources.md",
        "correction": "operator brief said 'Nizam & Team' — verified as "
                      "Nizamul Rana among four documented co-founders; "
                      "all four credited",
    },
    {
        "organ": "packet-orchestrator",
        "figure": "Justin Searle (InGuardians; SamuraiWTF/STFU) + the "
                  "Mantis framework (PhonePe) + the Scapy lineage credited",
        "distillation": "manual first, then translate layer by layer into "
                        "structured, state-backed automation; the manual "
                        "path stays re-runnable; packet differentials show "
                        "their bytes; state lives in records, not private "
                        "variables",
        "sources": "PhonePe/mantis docs; BlackHat US 2013 SamuraiSTFU "
                   "training page (NESCOR methodology); SANS profile; "
                   "skills/packet-orchestrator/references/sources.md",
        "correction": "operator brief attributed Mantis to 'Justin Searle & "
                      "Tim Skappen' — no security practitioner named Tim "
                      "Skappen could be verified; Mantis is the PhonePe "
                      "project (Apache-2.0). Organ built on the two "
                      "verified lineages, correction kept on record",
    },
    {
        "organ": "chain-architect",
        "figure": "Orange Tsai (DEVCORE) — Tier S, the Logic Architect",
        "distillation": "the compound kill chain: no single giant bug — "
                        "map the component architecture, hunt the seams, "
                        "treat low/informational findings as chainable "
                        "primitives, and compose 3-4 of them into one "
                        "critical impact with every link proven by its "
                        "own differential (the ProxyLogon pattern)",
        "sources": "DEVCORE 'ProxyLogon' writeup (2021); 'A New Era of "
                   "SSRF' (DEF CON 28); 'Confusion Attacks' (Apache); "
                   "HEXACON 2023 'A 3-Year Tale'; "
                   "skills/chain-architect/references/sources.md",
        "correction": None,
    },
    {
        "organ": "desync-hunter",
        "figure": "James Kettle (albinowax, PortSwigger Web Security "
                  "Research) — Tier S, the Logic Architect",
        "distillation": "protocol & specification asymmetry: the spec is a "
                        "hypothesis — map the parsing chain, craft one "
                        "ambiguity per request (CL/TE, header-name, "
                        "absolute-form, H2 classes), confirm by "
                        "response-class differential with exact bytes as "
                        "artifacts; timing is a lead, never a proof",
        "sources": "'HTTP Desync Attacks' (Black Hat US 2019) + the "
                   "PortSwigger research series; 'Browser-Powered Desync' "
                   "(2022); 'HTTP/2: The Sequel Is Always Worse' (Black "
                   "Hat US 2021); Web Security Academy smuggling modules; "
                   "skills/desync-hunter/references/sources.md",
        "correction": None,
    },
    {
        "organ": "deep-teardown",
        "figure": "George Hotz (geohot) — Tier S, the Reverse Engineer",
        "distillation": "dismantle to primitives: the shipped artifact is "
                        "the honest spec — one acquisition, then local "
                        "dissection down the teardown ladder (JS/APK/"
                        "binary), mapping local data handling of tokens, "
                        "keys, and PII before network flow; client logic "
                        "is a hypothesis until the server differential "
                        "confirms",
        "sources": "public record of the 2007 iPhone SIM unlock, the "
                   "PS3 reverse-engineering era (2010-11) and blackra1n "
                   "(2009); skills/deep-teardown/references/sources.md",
        "correction": None,
    },
    {
        "organ": "ghost-crawler",
        "figure": "Adrian Lamo (1981-2018) — Tier A, the Silent "
                  "Infiltrator",
        "distillation": "enter without knocking: the guarded main app is "
                        "the last thing you touch — passive public indexes "
                        "first (CT logs, dork grammar, archives), hunting "
                        "forgotten side doors and misconfigurations; one "
                        "bounded verification probe per candidate; "
                        "exposures reported, not looted (authorized "
                        "translation of the method shape, kept on record)",
        "sources": "United States v. Lamo (DOJ, 2003); Wired 'The "
                   "Homeless Hacker v. The New York Times' (2004); "
                   "obituary coverage (2018); "
                   "skills/ghost-crawler/references/sources.md",
        "correction": "Lamo's entries were unauthorized — this organ "
                      "distills the method shape (where forgotten exposure "
                      "lives, attribution discipline) into an R0-bounded "
                      "authorized posture; the distance is deliberate and "
                      "documented in the organ's sources.md",
    },
    {
        "organ": "mirror-hunter",
        "figure": "Simon Willison (coined the term 'prompt injection', "
                  "October 2022) — Tier S, the Class Namer",
        "distillation": "the mirror doctrine: the target runs the same "
                        "engine class as the hunter — invert the "
                        "self-model's failure geometry into attack "
                        "surface, never project your own obedience "
                        "boundary onto the target, gate on the program's "
                        "eligibility table before the first payload, and "
                        "land CONFIRMED only on the deterministic wrapper "
                        "the model feeds",
        "sources": "simonwillison.net 'Prompt injection: What's the worst "
                   "that can happen?' (October 2022) plus the years of "
                   "follow-up; the research wave it named (Greshake et "
                   "al. 2023; Rehberger's exfil chains; OWASP LLM Top 10) "
                   "— skills/mirror-hunter/references/sources.md",
        "correction": "the mirror doctrine itself (self-model inversion, "
                      "eligibility gating, the wrapper rule) is this "
                      "bundle's own contribution — Willison's record is "
                      "naming and documenting the class, credited exactly "
                      "for that",
    },
    {
        "organ": "auth-boundary-mapper",
        "figure": "Frans Rosen (Detectify co-founder; top-ranked bug "
                  "bounty hunter) — Tier A, folded into the organ at v2.0.0",
        "distillation": "IDOR as methodology: analyze identifier "
                        "construction before any swap; swap in every "
                        "parameter position; hunt 2nd-order references "
                        "across features; diff full response bodies, not "
                        "status codes; in multi-tenant SaaS the tenant "
                        "context is a matrix dimension",
        "sources": "'Attacking Modern Web Technologies' talk material; "
                   "2nd-order IDOR keynote material (Intigriti Bug Bytes "
                   "#55 coverage); the public IDOR writeup series; "
                   "skills/auth-boundary-mapper/references/"
                   "idor-field-guide.md",
        "correction": "operator brief spelled the name 'Franz Rosen' — "
                      "verified spelling is Frans Rosen; organ and "
                      "registry carry the verified spelling",
    },
    {
        "organ": "signal-smith",
        "figure": "John Draper (Captain Crunch) — Tier B, the Signal "
                  "Manipulator",
        "distillation": "one precise tone: learn the validator's expected "
                        "grammar (type, length, charset, encoding, "
                        "frequency), map the double-parse seams, then forge "
                        "ONE minimal variation that passes the filter while "
                        "the deeper parser reads different bytes — two "
                        "variations per seam, then park; never trip the "
                        "alarm",
        "sources": "the 1971-72 blue-box public record (2600 Hz in-band "
                   "signaling); Ron Rosenbaum, 'Secrets of the Little Blue "
                   "Box', Esquire (1971); "
                   "skills/signal-smith/references/sources.md",
        "correction": None,
    },
    {
        "organ": "trust-graph-hunter",
        "figure": "Kevin Mitnick (1963-2023, author of The Art of "
                  "Deception) — Tier B, translated to systems",
        "distillation": "context deception, systems edition: enumerate the "
                        "trust edges (what each boundary trusts — IPs, "
                        "Referer, internal headers, webhook signatures, "
                        "server-to-server tokens), draw the trust graph, "
                        "then pre-register deception hypotheses and prove "
                        "inherited privilege with differentials on "
                        "operator-owned ends; no human-target deception",
        "sources": "The Art of Deception (2002); The Art of Intrusion "
                   "(2005); obituary coverage (2023); "
                   "skills/trust-graph-hunter/references/sources.md",
        "correction": "the systems translation is labeled as this "
                      "bundle's own contribution, not Mitnick's practice — "
                      "no human-target social engineering is contained or "
                      "used anywhere in the organ",
    },
    {
        "organ": "subdomain-hunter",
        "figure": "EdOverflow — creator and maintainer of the "
                  "can-i-take-over-xyz community registry; folded into the "
                  "organ at v2.0.0",
        "distillation": "takeover as a registry discipline: class the "
                        "dangling record (NXDOMAIN-CNAME, fingerprint-"
                        "CNAME, dangling MX/NS, deep chains) because the "
                        "class IS the blast-radius argument; verify on "
                        "three legs (DNS chain to the terminal, quoted "
                        "provider fingerprint, TTL-aware re-reads); run "
                        "the claim-path test before CONFIRMED; date the "
                        "signature table and let upstream retirements "
                        "flow through",
        "sources": "github.com/EdOverflow/can-i-take-over-xyz — README "
                   "verdict table + fingerprints.json structure; the "
                   "issue history as the correction tradition (Unbounce "
                   "#11, Google Sites #277 retirements); "
                   "skills/subdomain-hunter/references/sources.md + "
                   "takeover-field-guide.md",
        "correction": None,
    },
    {
        "organ": "xss-playbook",
        "figure": "Mario Heiderich (Cure53 founder) — the mXSS research "
                  "line; folded into the organ at v2.0.0",
        "distillation": "context is not stable: mutation between "
                        "sanitization and re-parse is the vulnerability — "
                        "re-derive the sink context after every DOM "
                        "mutation; one minimal differential per mutation "
                        "class (re-serialization, namespace confusion, "
                        "parsing-context switch) with the mutated bytes as "
                        "the artifact; DOM clobbering harvested, not "
                        "sprayed; sanitizer name+version is a ledgered "
                        "FACT because sanitizers regress",
        "sources": "'mXSS attacks: attacking well-secured web-"
                   "applications by using innerHTML mutations' (ACM WPES "
                   "2013, DOI 10.1145/2508859.2516723); 'Attacking "
                   "well-secured Web-Applications by using innerHTML' "
                   "(cure53.de/fp170.pdf); the 2024 mXSS revival talks "
                   "(BSides Berlin 2024 showcase); "
                   "skills/xss-playbook/references/sources.md + "
                   "mxss-and-clobber.md",
        "correction": None,
    },
    {
        "organ": "oauth-flow-auditor",
        "figure": "Aaron Parecki — author of OAuth 2.0 Simplified, "
                  "maintainer of oauth.net, co-editor of the OAuth 2.1 "
                  "draft; folded into the organ at v2.0.0",
        "distillation": "redirect_uri is the load-bearing wall: exact "
                        "match per RFC 6749 tested as a matrix at BOTH "
                        "endpoints; state is three checks (presence, "
                        "validation, binding); PKCE is checked where it "
                        "wasn't invited (downgrade, plain-vs-S256); "
                        "severity vocabulary maps to the BCP (RFC 9700); "
                        "error paths are differential instruments and "
                        "echoed redirect_uri is chain input",
        "sources": "OAuth 2.0 Simplified (oauth.com / "
                   "oauth2simplified.com); oauth.net/getting-started; "
                   "RFC 6749 §3.1.2.3, RFC 7636, RFC 6819, RFC 9700; "
                   "skills/oauth-flow-auditor/references/sources.md + "
                   "flow-craft.md",
        "correction": None,
    },
    {
        "organ": "content-discovery",
        "figure": "Daniel Miessler — maintainer of SecLists; folded into "
                  "the organ at v2.0.0",
        "distillation": "corpus science: wordlists are chosen by FAMILY "
                        "and composed from evidence, never grabbed by "
                        "size; extensions derive from the observed stack; "
                        "a new base URL always recalibrates its negative "
                        "profile; the password families live behind their "
                        "own scope wall and never run in this organ",
        "sources": "github.com/danielmiessler/SecLists — the family "
                   "structure (Discovery/Web-Content, Discovery/DNS, "
                   "Passwords, Miscellaneous) that the composition law "
                   "mirrors; danielmiessler.com; "
                   "skills/content-discovery/references/sources.md + "
                   "corpus-science.md",
        "correction": None,
    },
    {
        "organ": "business-logic-hunter",
        "figure": "Soroush Dalili (@irsdl, NCC Group line) — the "
                  "HTTP-reshaping bypass grammar; folded into the organ "
                  "at v2.0.0",
        "distillation": "bypass craft: reshape once, canonically, before "
                        "closing any blocked hypothesis (case, path "
                        "params, segment padding, encoding, header/verb); "
                        "seams are read at the executor's verdict, not the "
                        "guard's status; invert every check — displaced, "
                        "what does it become; comparison functions are "
                        "testable units with both identifiers' bytes "
                        "recorded; two variants per seam, then park",
        "sources": "'WAF Bypass Techniques Using HTTP Standard and Web "
                   "Servers' Behavior' (public talk); the NCC Group "
                   "research posts (Flash upload-bypass advisory line); "
                   "soroush.me/blog (HackPra 'File in the hole!' "
                   "material); @irsdl on X; "
                   "skills/business-logic-hunter/references/sources.md + "
                   "bypass-craft.md",
        "correction": None,
    },
    {
        "organ": "cloud-config-auditor",
        "figure": "Toni de la Fuente — Prowler's author and steward; "
                  "folded into the organ at v2.0.0",
        "distillation": "checks as code: every check carries a stable ID, "
                        "a version, and a benchmark paragraph — severity "
                        "words cite the mapped CIS paragraph, never a "
                        "mood; verdicts carry timestamps and load-bearing "
                        "ones re-verify inside the engagement window; "
                        "name the posture shape, then the provider "
                        "instance; matrix tables over magic scores",
        "sources": "prowler.com (the platform + blog: 'Why We Need the "
                   "Open Cloud Security Movement', Feb 2025; the State of "
                   "Cloud Security Report 2025); github.com/prowler-"
                   "cloud/prowler; CIS Benchmarks (cisecurity.org); "
                   "skills/cloud-config-auditor/references/sources.md + "
                   "checks-as-code.md",
        "correction": None,
    },
    {
        "organ": "mobile-hunter",
        "figure": "Charlie Miller (with Collin Mulliner on the 2009 "
                  "iPhone SMS compromise)",
        "distillation": "the mobile teardown discipline: the shipped "
                        "binary is a confession (manifest, strings, "
                        "bundled secrets, ghost endpoints read before "
                        "the device is ever touched); store review and "
                        "code-signing are hypotheses about attacker "
                        "effort, not walls; and the app is a client to "
                        "the same web API the program already pays "
                        "for — mobile findings land at the API boundary",
        "sources": "Wikipedia 'Charlie Miller (security researcher)' "
                   "(Pwn2Own 2008 MacBook Air and 2009 Safari wins, "
                   "five years at the NSA, the 2011 Instastock "
                   "code-signing demonstration that got him expelled "
                   "from the App Store, the 2015 remote Jeep exploit "
                   "with Chris Valasek, and the 2009 SMS compromise "
                   "of the iPhone demonstrated with Collin Mulliner); "
                   "iOS Hacker's Handbook (Miller, Dai Zovi, Portnoy, "
                   "Weinstein — Wiley, 2012); skills/mobile-hunter/"
                   "references/sources.md",
        "correction": None,
    },
    {
        "organ": "cache-playbook",
        "figure": "Omer Gil (web cache deception, Black Hat USA 2017) "
                  "with James Kettle's cache-poisoning corpus (Black "
                  "Hat USA 2018; Web Cache Entanglements, 2020)",
        "distillation": "the cache is a second, silent parser: it "
                        "decides what to store and whom to serve by "
                        "its own key rules, and every disagreement "
                        "between origin and cache — path confusion, "
                        "unkeyed inputs, cache-key versus display-key "
                        "gaps — becomes either stored secrets "
                        "(deception) or stored payloads (poisoning)",
        "sources": "Omer Gil, 'Web Cache Deception Attack' (Black Hat "
                   "USA 2017 whitepaper, blackhat.com/docs); James "
                   "Kettle, 'Practical Web Cache Poisoning: Redefining "
                   "\"Unexploitable\"' (Black Hat USA 2018) and 'Web "
                   "Cache Entanglements' (portswigger.net/research, "
                   "2020); Mirheidari, Arshad, Onarlioglu, Crispo, "
                   "Kirda, Robertson, 'Cached and Confused: Web Cache "
                   "Deception in the Wild' (USENIX Security 2020); "
                   "skills/cache-playbook/references/sources.md",
        "correction": "James Kettle anchors desync-hunter; this entry "
                      "cites his cache-poisoning corpus specifically — "
                      "different works, different organ, kept distinct "
                      "on record.",
    },
    {
        "organ": "prototype-playbook",
        "figure": "Gareth Heyes (PortSwigger Research)",
        "distillation": "the object world is trust-bearing state: "
                        "prototypes hand every object inherited "
                        "defaults an attacker can overwrite (pollution "
                        "to a gadget, then a sink), the DOM binds "
                        "named elements into global scope (clobbering), "
                        "and windows trust message origins — hunt "
                        "source, gadget, sink in that order, and detect "
                        "server-side pollution without the DoS",
        "sources": "Gareth Heyes, 'Server-side prototype pollution: "
                   "Black-box detection without the DoS' "
                   "(portswigger.net/research, Feb 2023; presented at "
                   "NullCon Berlin 2023 and OWASP Global AppSec Dublin "
                   "2023); 'Widespread prototype pollution gadgets' "
                   "(PortSwigger Research); DOM Invader, the Burp "
                   "browser extension that finds XSS, prototype "
                   "pollution, and postMessage issues (his); the "
                   "research wave: 'DOM Clobbering strikes back' "
                   "(PortSwigger Research, Feb 2020); PortSwigger Web "
                   "Security Academy prototype-pollution module; skills/"
                   "prototype-playbook/references/sources.md",
        "correction": "'DOM Clobbering strikes back' is cited as "
                      "PortSwigger Research without an individual "
                      "author attribution — the organ's figure entry "
                      "rests on Heyes' verified prototype-pollution "
                      "and DOM Invader record only.",
    },
]

ARTICLES = [
    "A1 identity — Skill Mythos is the master activation module of an "
    "extreme-expertise bundle for pentest, bug bounty, and security "
    "research; not general-purpose skills.",
    "A2 research-grounded — methods are synthesized from complete public "
    "sources (books, papers, advisories, post-mortems) read in full "
    "context, never snippet-mined; claims still live or die by the ledger.",
    "A3 legitimate assimilation — public methodologies of named "
    "researchers are studied, attributed, and re-implemented as decision "
    "logic; no proprietary code, no IP theft, no unattributed borrowing.",
    "A4 stability, sustainability, consistency — deterministic, auditable "
    "behavior over cleverness; the same input produces the same record.",
    "A5 autonomy with accountability — once activated, the agent "
    "self-selects and combines organs to fit state, situation, "
    "environment, and target architecture; autonomy is bounded by R0 "
    "scope and the append-only ledger.",
    "A6 selection by phase and event, not curiosity — organs are routed "
    "by engagement phase, or by incident trigger for the Binary Brain.",
    "A7 quality over bounty — the end goal is superior report quality, "
    "not reward-chasing; profitability follows reproducibility.",
    "A8 zero false positives — a claim ships only after the differential "
    "triad (baseline / treatment / control); single-channel observations "
    "stay leads.",
    "A9 full reproducibility — any third party can replay every step from "
    "the report; n_runs / attempts+success_rate are mandatory fields.",
    "A10 measured severity — every CONFIRMED finding carries a CVSS 3.1 "
    "vector with recomputed base score and a Bugcrowd VRT mapping with "
    "the HackerOne severity crosswalk.",
    "A11 triage viability — reports are written for the triage desk: "
    "precise, hedging-free, evidence-cited, impact-chained.",
    "A12 philosophy per organ — each organ carries its methodology's "
    "essence and documents its lineage; the charter is the convergence "
    "point.",
    "A13 prompt escalation — every operator instruction, however terse "
    "or informal, is expanded through doctrine_forge into an explicit "
    "doctrine order (persona mix, phase plan, tools, gates) before any "
    "organ acts; the agent executes the expanded order, never the bare "
    "words — deterministic, and the original request rides along verbatim.",
    "A14 three registers (what/why/how) — every organ's expertise is "
    "stated in three registers: WHAT the class of thing is (anatomy, "
    "precise definitions), WHY it exists (the root cause, the "
    "mechanical reason the bug lives where it lives), and HOW it is "
    "hunted (numbered procedure with oracles and falsifiers); a "
    "technique missing any register is not shipped knowledge.",
    "A15 war logic — the bundle fights under the Art of War crosswalk: "
    "spies before armies (passive before active), supreme excellence "
    "wins without fighting (the differential triad proves, damage is "
    "not evidence), avoid strength and strike weakness (seam density "
    "over target size), cheng and ch'i (every plan pairs the orthodox "
    "sweep with the unorthodox bet), shih accumulation (the ledger is "
    "stored position), and the sovereign sets intent while the general "
    "commands (A13 orders are campaigns, not errands); full mapping in "
    "references/war-doctrine.md (W1-W7).",
]

QUALITY_GATES = [
    "differential triad on every claim (baseline + treatment + control)",
    "n_runs >= 2 with stable deltas, or attempts + success_rate",
    "CVSS 3.1 vector + recomputed base score on every CONFIRMED finding "
    "(cvss3_score; the auditor recomputes it)",
    "VRT category + P-rating on every CONFIRMED finding (vrt_classify; "
    "validated against the shipped official taxonomy)",
    "HackerOne severity crosswalk stated alongside the VRT rating",
    "impact-chain: and canary attestation lines in the finding block",
    "reproduction steps a third party can replay verbatim",
    "no hedging language; no claims without R-NNN citations",
]

EXECUTION_DOCTRINE = [
    "OODA-hygiene loop: write the observation note from fresh tool "
    "output BEFORE the next thought; one pre-registered hypothesis "
    "per step; a step without an observation note is not done.",
    "D1 intuition (Kahneman & Klein 2009): lineage intuition "
    "proposes hypotheses; only the differential triad concludes — a "
    "lineage is a method license, never an authority license.",
    "D5 calibration (Xiong et al. 2024): confidence derives from "
    "evidence class, never felt certainty; stochastic surfaces run "
    "as rates over N runs.",
    "D3 exploration (March 1991): while a quota is unmet, at least 1 "
    "in 5 steps targets a surface class never probed this "
    "engagement.",
    "Reflexion (Shinn et al. 2023): every refuted hypothesis leaves "
    "a one-line lesson, re-read before the next hypothesis on that "
    "surface class.",
    "Full doctrine: skill-mythos references/autonomous-operation.md "
    "(D1-D7, behavior contracts, per-organ execution anchors).",
]

# The war-logic layer (charter A15): the Sun Tzu crosswalk, distilled
# into the seven operational rules every forged order carries. The full
# concept-by-concept mapping lives in references/war-doctrine.md; these
# are the clauses the agent re-reads in every doctrine prompt.
WAR_DOCTRINE = [
    "W1 spies before armies: no active byte leaves the machine before "
    "the passive record exists (CT logs, archives, shipped code, store "
    "listings); the ghost-crawler posture is the default march.",
    "W2 win without fighting: the differential triad proves and the "
    "canary demonstrates — damage is not evidence, and a destroyed "
    "target ends the campaign for everyone.",
    "W3 avoid strength, strike weakness: the priority queue ranks by "
    "seam density and neglect, never by target size or fame; the "
    "well-guarded front is recorded and bypassed, not stormed.",
    "W4 cheng and ch'i: every engagement plan names its orthodox sweep "
    "(known classes, calibrated oracles) AND its unorthodox bet (the "
    "white-space move nobody submitted before); a plan without a ch'i "
    "is a patrol, not a campaign.",
    "W5 shih before battle: the ledger is stored position — every "
    "proven primitive is a captured hill; chains (chain-architect) "
    "convert accumulated low-severity links into decisive impact, and "
    "no proven primitive is ever discarded unrecorded.",
    "W6 the sovereign sets intent, the general commands: doctrine "
    "orders (A13) are campaigns with fronts, sequencing, and supply "
    "lines (R7 budgets); the general executes autonomously and never "
    "re-asks mid-march what the order already answers.",
    "W7 no nation ever profited from a prolonged war: quotas bound the "
    "campaign; before a quota is met it ends only by exhaustion proof "
    "or operator release, and context exhaustion is a pause, not a "
    "surrender (mission horizon, researcher-conduct 34.8).",
    "Full doctrine: skill-mythos references/war-doctrine.md (the Art of "
    "War crosswalk, W1-W7 in depth, per-organ war notes, sources).",
]

REPORTING_TOOLS = {
    "cvss3_score": "spec-exact CVSS v3.1 base score from a vector",
    "vrt_classify": "finding-class -> Bugcrowd VRT + P-rating + H1 "
                    "severity + CVSS template",
    "mythos_lineages": "the assimilated-lineage registry: organ, figure, "
                       "distillation, sources, corrections on record",
    "auditor/audit_report.py": "PASS/FAIL gate — exit 0 or the report "
                               "does not ship",
}


def _installed_skills() -> list[str]:
    root = paths.skills_dir()
    if not os.path.isdir(root):
        return []
    return sorted(entry for entry in os.listdir(root)
                  if os.path.isfile(os.path.join(root, entry, "SKILL.md")))


def mythos_charter() -> dict:
    """The Skill Mythos activation payload, in one call.

    Returns the fifteen charter articles, the bundle map with per-skill
    install status, the quality gates every report must pass, and the
    reporting-stage tool routing. Call this at session start (or whenever
    the operator says 'activate Skill Mythos') before list_skills."""
    installed = _installed_skills()
    registry = {name for names in TIERS.values() for name in names}
    tiers_out = {}
    for tier, names in TIERS.items():
        tiers_out[tier] = {name: name in installed for name in names}
    others = [s for s in installed if s not in registry and s != SPINE]
    return {
        "module": MODULE,
        "version": MODULE_VERSION,
        "spine": SPINE,
        "articles": ARTICLES,
        "tiers": tiers_out,
        "spine_installed": SPINE in installed,
        "other_installed": others,
        "quality_gates": QUALITY_GATES,
        "reporting_tools": REPORTING_TOOLS,
        "prompt_escalation": {
            "tool": "doctrine_forge",
            "rule": "every operator instruction, however terse, is expanded "
                    "into an explicit doctrine order before any organ acts "
                    "(A13); the original words ride along verbatim",
        },
        "lineage_registry_tool": "mythos_lineages",
        "execution_doctrine":
            "skills/skill-mythos/references/autonomous-operation.md",
        "war_doctrine":
            "skills/skill-mythos/references/war-doctrine.md",
        "charter_reference": "skills/skill-mythos/SKILL.md",
    }


def mythos_lineages() -> dict:
    """The assimilated-lineage registry (doctrine A3, verbatim).

    Every organ built from a named public figure or team, what was
    distilled from them, which sources were actually consulted, and any
    attribution corrections kept on record. Assimilation is legitimate
    only when it is documented exactly like this — the registry IS the
    compliance artifact."""
    installed = set(_installed_skills())
    entries = []
    for entry in LINEAGES:
        out = dict(entry)
        out["installed"] = entry["organ"] in installed
        entries.append(out)
    return {
        "count": len(entries),
        "doctrine": "skills/skill-mythos/references/assimilation-doctrine.md",
        "lineages": entries,
    }


# --------------------------------------------- prompt escalation (A13)
#
# doctrine_forge — the operator's terse instruction becomes an explicit
# doctrine order before any organ acts. Deterministic by A4: the same
# request produces the same order, character for character.

LEGEND_REGISTRY = [
    {
        "key": "orange-tsai",
        "legend": "Orange Tsai (Tier S — the Logic Architect)",
        "organ": "chain-architect",
        "contribution": "adopt the chaining mindset — hunt the small, "
                        "chainable gaps and design the compound kill chain "
                        "that composes 3-4 low-severity links into one "
                        "critical impact",
    },
    {
        "key": "james-kettle",
        "legend": "James Kettle (Tier S — the Logic Architect)",
        "organ": "desync-hunter",
        "contribution": "treat the specification as a hypothesis — manipulate "
                        "HTTP headers and protocol framing manually at the "
                        "parser seams, one ambiguity per request, bytes as "
                        "evidence",
    },
    {
        "key": "george-hotz",
        "legend": "George Hotz (Tier S — the Reverse Engineer)",
        "organ": "deep-teardown",
        "contribution": "dismantle the client artifact to primitives — read "
                        "the actual code, map local data handling before "
                        "network flow",
    },
    {
        "key": "adrian-lamo",
        "legend": "Adrian Lamo (Tier A — the Silent Infiltrator)",
        "organ": "ghost-crawler",
        "contribution": "enter without knocking — only passively-exposed "
                        "architecture misconfigurations and forgotten side "
                        "doors, one bounded probe per candidate, the guarded "
                        "main application untouched",
    },
    {
        "key": "frans-rosen",
        "legend": "Frans Rosen (Tier A — the Silent Infiltrator)",
        "organ": "auth-boundary-mapper",
        "contribution": "IDOR as methodology — identifier construction "
                        "before any swap, every parameter position, "
                        "2nd-order flows, cloud tenant slices, full response "
                        "diffs",
    },
    {
        "key": "john-draper",
        "legend": "John Draper (Tier B — the Signal Manipulator)",
        "organ": "signal-smith",
        "contribution": "one precise forged variation beats a thousand noisy "
                        "ones — calibrate the validator's grammar and "
                        "frequency, then the minimal byte edit; never trip "
                        "the alarm",
    },
    {
        "key": "kevin-mitnick",
        "legend": "Kevin Mitnick (Tier B — the Context Deceiver)",
        "organ": "trust-graph-hunter",
        "contribution": "map the trust relationships between systems and "
                        "audit every trust edge for forgeable context — "
                        "inherited privilege proven on operator-owned ends",
    },
    {
        "key": "simon-willison",
        "legend": "Simon Willison (Tier S — the Class Namer)",
        "organ": "mirror-hunter",
        "contribution": "the mirror doctrine — the target runs the same "
                        "engine class as the hunter: invert the "
                        "self-model's failure geometry into attack "
                        "surface, gate on the program's eligibility table "
                        "before the first payload, and land CONFIRMED only "
                        "on the deterministic wrapper the model feeds",
    },
]

# (intent, keywords) — scored by distinct keyword hits; ties broken by
# list order. Keywords cover English and the operator's Indonesian
# phrasings, matching the charter's activation triggers.
_INTENT_GRAMMAR = [
    ("continue_pending", (
        "lanjutkan", "lanjut", "tersambung", "continue", "resume",
        "pending", "tertunda", "sambungkan")),
    ("incident_response", (
        "adversary", "incident", "intrusion", "compromis", "serangan",
        "dibobol", "anomalous", "breach")),
    ("classify_report", (
        "cvss", "vrt", "classify", "klasifikasi", "rating", "laporan",
        "report", "audit", "severity assessment")),
    ("ai_surface", (
        "prompt injection", "prompt-injection", "injeksi prompt",
        "injection ke model", "llm", "chatbot", "copilot", "genai",
        "chatgpt", "gemini", "model ai", "ai agent", "ai target",
        "target ai", "aplikasi ai", "fitur ai", "celah ai", "bug ai",
        "uji ai", "ai surface", "mcp server", "mcp", "agent ai")),
    ("bug_quota", (
        "bug", "temuan", "finding", "vulnerabilit", "celah", "dapatkan",
        "hunt", "carikan", "cari bug", "get me", "minimum", "minimal",
        "at least", "target")),
    ("surface_recon", (
        "recon", "enumerat", "subdomain", "mapping", "peta", "asset",
        "surface", "perimeter", "inventory")),
]

_SEVERITY_RE = re.compile(r"\b(critical|high|medium|low)\b", re.IGNORECASE)
_QUOTA_RE = re.compile(
    r"(?:minimal|minimum|at least|sedikitnya|sekurang|target)\s+(\d+)"
    r"|(\d+)\s*(?:bug|temuan|finding|vulnerabilit|celah)",
    re.IGNORECASE)


def _detect_intent(request: str) -> str:
    """Scored keyword match, deterministic; 'default' when nothing hits."""
    lowered = request.lower()
    best, best_hits = "default", 0
    for intent, keywords in _INTENT_GRAMMAR:
        hits = sum(1 for kw in keywords if kw in lowered)
        if hits > best_hits:
            best, best_hits = intent, hits
    return best


def _extract_severity(request: str) -> list[str]:
    found = []
    for match in _SEVERITY_RE.findall(request):
        token = match.lower()
        if token not in found:
            found.append(token)
    return found


def _extract_quota(request: str):
    match = _QUOTA_RE.search(request)
    if not match:
        return None
    return int(match.group(1) or match.group(2))


def _personas(keys: list[str]) -> list[dict]:
    by_key = {p["key"]: p for p in LEGEND_REGISTRY}
    return [dict(by_key[k]) for k in keys if k in by_key]


def _forge_bug_quota(request: str, severity: list[str],
                     quota: int | None) -> dict:
    severity_goal = "-".join(severity) if severity else "unspecified"
    quota_line = ("at least %d" % quota) if quota else "unspecified count"
    prompt = (
        "PROFESSIONAL ORDER (auto-forged from the operator's request):\n\n"
        "Hunt the authorized targets WITHOUT scanners, under the embedded "
        "Skill Mythos methods, with a severity goal of %s and a quota of "
        "%s.\n\n"
        "1. Posture first: auth_status() — R0 scope and the authorization "
        "artifact decide which targets are touchable this session; a refusal "
        "is a ledgered audit fact, not an obstacle.\n"
        "2. Stealth principle (Adrian Lamo): enter without knocking — "
        "passive public indexes first (CT logs, dork grammar, archives), "
        "hunting forgotten side doors and exposed architecture "
        "misconfigurations; ONE bounded verification probe per candidate; "
        "the guarded main application stays untouched while side doors "
        "remain unexplored.\n"
        "3. Chaining mindset (Orange Tsai): map the component architecture "
        "and hunt the seams; treat every informational/low finding as a "
        "chainable primitive — design the compound kill chain that composes "
        "3-4 small gaps into one critical impact, each link proven by its "
        "own differential triad.\n"
        "4. Protocol asymmetry (James Kettle): treat the specification as a "
        "hypothesis — where documentation says the system works way A, "
        "craft the manual way-B input at the parser seams (header and "
        "protocol manipulation, one ambiguity per request) and prove the "
        "disagreement with exact bytes in artifacts.\n"
        "5. Authorization discipline (Frans Rosen): every object reference "
        "gets identifier-construction analysis BEFORE any swap; swap in "
        "every parameter position; sweep 2nd-order flows and cloud tenant "
        "slices; diff full response bodies, never just status codes.\n"
        "6. Trust audit (Kevin Mitnick, systems edition): draw the trust "
        "graph between components; pre-register a deception hypothesis per "
        "trust edge; prove inherited privilege on operator-owned ends only.\n"
        "7. Signal craft (John Draper) when a validator blocks honest "
        "payloads: calibrate the filter's expected grammar and frequency, "
        "then ONE precise minimal variation per seam — never a spray, "
        "never an alarm.\n"
        "8. Client teardown (George Hotz) where artifacts are in scope: one "
        "acquisition, local dissection to primitives, local data flow "
        "mapped before network flow.\n\n"
        "Quota discipline (A7/A8): the quota is an EFFORT BUDGET, not a "
        "severity mandate. Every CONFIRMED finding still clears the "
        "differential triad (baseline/treatment/control), n_runs >= 2, "
        "cvss3_score + vrt_classify on every report line, and "
        "auditor/audit_report.py exit 0. If the evidence supports fewer or "
        "milder findings than the quota, the report says exactly that, with "
        "the state that produced it — severity inflation to satisfy a quota "
        "is the one unforgivable failure. State the exit numbers (R6). "
        "Mission horizon (researcher-conduct.md 34.8): the quota is ALSO a "
        "continuation mandate. Before it is met, the engagement ends only "
        "by exhaustion proof (every inventoried surface has a closed "
        "hypothesis or a why-not; the TODO queue is empty because the "
        "backlog is empty) or explicit operator release — a summary "
        "written over an unresolved TODO queue is a stop-condition "
        "violation, not a report. Every dead end redirects: FALSIFIED or "
        "parked, then the next TODO in the same session. Context exhaustion "
        "is a pause — the MISSION block survives in state and the next "
        "session resumes toward the unmet quota."
        % (severity_goal, quota_line))
    return {
        "detected_intent": "bug_quota",
        "severity_goal": severity_goal,
        "quota": quota,
        "persona_mix": _personas(["adrian-lamo", "orange-tsai",
                                  "james-kettle", "frans-rosen",
                                  "kevin-mitnick", "john-draper",
                                  "george-hotz"]),
        "phase_plan": [
            "auth_status — R0 posture",
            "Phase 1 passive-first (ghost-crawler posture drives)",
            "Phase 2 matrix + architecture + trust graph + chain design",
            "Phase 3 differentials with craft/legend overlays",
            "Phase 4 bounded impact proofs (canary ladder)",
            "Phase 5 classification + audit until exit 0",
        ],
        "tools": ["auth_status", "ct_subdomains", "dns_resolve",
                  "http_probe", "js_analyze", "api_introspect",
                  "content_discover", "dossier_add", "ledger_append",
                  "cvss3_score", "vrt_classify",
                  "auditor/audit_report.py"],
        "doctrine_prompt": prompt,
    }


def _forge_ai_surface(request: str, severity: list[str],
                      quota: int | None) -> dict:
    severity_goal = "-".join(severity) if severity else "unspecified"
    quota_line = ("at least %d" % quota) if quota else "unspecified count"
    prompt = (
        "PROFESSIONAL ORDER (auto-forged from the operator's request):\n\n"
        "Hunt the authorized LLM/agent surface (mirror-hunter organ, "
        "Willison lineage) with a severity goal of %s and a quota of %s.\n\n"
        "1. Eligibility gate BEFORE the first payload: read the program's "
        "AI rules and write the eligibility table into state — qualifying "
        "categories with their required impact, ineligible list verbatim. "
        "A jailbreak confined to your own session is content, not a "
        "finding; a hypothesis that can only land in an ineligible class "
        "is parked before a token is spent.\n"
        "2. Surface inventory (spine section 24): which endpoints send text "
        "to a model, what the model can DO (tools, fetch, render), whose "
        "rows RAG sees, what memory persists; one dossier entry per "
        "channel with record citations.\n"
        "3. Mirror priors, labeled: every belief about what the target "
        "model will obey is a PROJECTION — it encodes your engine, not "
        "the target's — until its own record exists; write the base rate "
        "before the runs (glm-self-model G3).\n"
        "4. Craft selection (mirror-hunter injection-craft): the seam is "
        "attention, not a parser — edge-loaded imperatives, salience "
        "capture, authority forgery, commitment ladders; pre-register the "
        "differential with the benign-twin payload as the control BEFORE "
        "any run.\n"
        "5. Rate law: stochastic claims run N >= 10 with successes "
        "recorded as a rate and the model identifier recorded verbatim; "
        "1/10 is a weak signal — hunt the conditions or downgrade.\n"
        "6. Wrapper rule: CONFIRMED lands on the deterministic stage the "
        "model feeds (tool-call handler, renderer, sink) — 'the model "
        "emitted X' is a lead, 'the wrapper executed X' is the finding.\n"
        "7. Impact proof ONCE: canary at the end (self-owned account, "
        "self-owned artifact); one exfiltration hit then stop (the "
        "channel law); tool-hijack chains run per-link differentials plus "
        "a single joint proof (chain-architect law).\n"
        "8. Classification and exit: cvss3_score on the observed path, "
        "vrt_classify with the LLM01-family crosswalk, the rate line and "
        "the version line in every finding block, auditor exit 0 before "
        "shipping. State the exit numbers (R6): channels, hypotheses by "
        "state, runs, rates, wrapper crossings, canary proofs.\n\n"
        "Quota discipline (A7/A8) and mission horizon (researcher-conduct "
        "34.8) apply unchanged: the quota is an effort budget and a "
        "continuation mandate — before it is met the engagement ends only "
        "by exhaustion proof or explicit operator release; context "
        "exhaustion is a pause. Severity inflation — a jailbreak dressed "
        "as impact — is the one unforgivable failure on this surface."
        % (severity_goal, quota_line))
    return {
        "detected_intent": "ai_surface",
        "severity_goal": severity_goal,
        "quota": quota,
        "persona_mix": _personas(["simon-willison", "orange-tsai",
                                  "frans-rosen"]),
        "phase_plan": [
            "eligibility table from the program's AI rules (before payload)",
            "AI surface inventory (spine section 24) into the dossier",
            "labeled mirror priors + pre-registered differentials",
            "N-run rate protocol with benign-twin controls",
            "wrapper differentials -> bounded impact proof once",
            "classification + audit until exit 0",
        ],
        "tools": ["auth_status", "http_probe", "js_analyze",
                  "api_introspect", "dossier_add", "ledger_append",
                  "cvss3_score", "vrt_classify",
                  "auditor/audit_report.py"],
        "doctrine_prompt": prompt,
    }


def _forge_continue(request: str) -> dict:
    prompt = (
        "PROFESSIONAL ORDER (auto-forged from the operator's request):\n\n"
        "Continue the pending authorized engagement from its recorded "
        "state — resume, never restart.\n\n"
        "1. Re-ground: auth_status() (is the R0 posture unchanged?), then "
        "ledger_summary() and ledger_read() on the newest PARK record — "
        "the resume note states the phase, the parked remainder, and the "
        "next action that was declared.\n"
        "2. dossier_summary() for the surface state; reconcile against the "
        "priority queue and the backlog.\n"
        "3. Resume at the parked phase with its organ routing (charter "
        "phase table): recon organs if recon was parked; the "
        "authorization matrix if Phase 2 was parked; payload organs with "
        "the craft and legend overlays if Phase 3 was parked; "
        "classification tools if Phase 5 was parked.\n"
        "4. Effort discipline (scan-economist): re-price the parked "
        "remainder before executing; if the budget is spent, say so with "
        "numbers instead of grinding.\n"
        "5. Quality gates unchanged: differential triad on every new claim, "
        "n_runs >= 2, CVSS 3.1 + VRT on every CONFIRMED line, auditor "
        "exit 0 before shipping.\n"
        "6. State the exit numbers (R6): surfaces, hypotheses, closures by "
        "state, records appended this session.")
    return {
        "detected_intent": "continue_pending",
        "severity_goal": "-",
        "quota": None,
        "persona_mix": _personas(["orange-tsai", "adrian-lamo",
                                  "frans-rosen"]),
        "phase_plan": [
            "auth_status + ledger PARK recovery",
            "dossier reconciliation",
            "resume at the parked phase (organ routing)",
            "exit numbers at the boundary",
        ],
        "tools": ["auth_status", "ledger_summary", "ledger_read",
                  "dossier_summary", "http_probe", "ledger_append",
                  "cvss3_score", "vrt_classify"],
        "doctrine_prompt": prompt,
    }


def _forge_surface_recon(request: str) -> dict:
    prompt = (
        "PROFESSIONAL ORDER (auto-forged from the operator's request):\n\n"
        "Map the authorized target's surface — passive first, "
        "evidence-cited, alarm-free.\n\n"
        "1. auth_status() — the R0 posture and which classes of source are "
        "permitted this engagement.\n"
        "2. Passive superset (subdomain-hunter, pipeline-smith-shaped "
        "stages, scan-economist pricing): ct_subdomains + dns_resolve; "
        "wildcard verdicts; dangling delegations flagged as takeover "
        "pairs.\n"
        "3. Stealth layer (Adrian Lamo): dork grammar and public-archive "
        "sweep for forgotten side doors — one query per misconfiguration "
        "class; every candidate into the dossier backlog, nothing probed "
        "yet.\n"
        "4. Bounded verification: exactly ONE http_probe per candidate; "
        "confirmed exposures classified and reported; the main "
        "application stays untouched.\n"
        "5. Surface registration (surface-cartographer): dossier_add for "
        "every live surface with probe-record citations; dossier_render "
        "at exit with the numbers (hosts, surfaces, classes, probes "
        "spent).\n"
        "6. JS and spec inventory where in scope: js_analyze per bundle "
        "(one fetch), api_introspect for spec surfaces — extraction is "
        "hypothesis until probed (R5).")
    return {
        "detected_intent": "surface_recon",
        "severity_goal": "-",
        "quota": None,
        "persona_mix": _personas(["adrian-lamo", "george-hotz"]),
        "phase_plan": [
            "auth_status — posture and permitted sources",
            "passive superset + takeover pairs",
            "dork/archive sweep -> backlog",
            "one-probe verification per candidate",
            "dossier registration + render with numbers",
        ],
        "tools": ["auth_status", "ct_subdomains", "dns_resolve",
                  "http_probe", "js_analyze", "api_introspect",
                  "dossier_add", "dossier_render", "ledger_append"],
        "doctrine_prompt": prompt,
    }


def _forge_classify(request: str) -> dict:
    prompt = (
        "PROFESSIONAL ORDER (auto-forged from the operator's request):\n\n"
        "Classify and gate the findings for the triage desk.\n\n"
        "1. For every CONFIRMED finding: cvss3_score() on the vector of "
        "the OBSERVED attack path — write exactly what it returns; the "
        "auditor recomputes it and a mismatch fails the report.\n"
        "2. vrt_classify() with the observed context flags — Bugcrowd VRT "
        "dotted id + P-rating + the HackerOne crosswalk; divergences "
        "between the three severity layers (technical, taxonomy, "
        "program-context) are stated and argued, never silently merged.\n"
        "3. Reproduction: every finding block cites its differential triad "
        "records (baseline/treatment/control) and carries replayable "
        "steps with n_runs >= 2 or attempts + success_rate.\n"
        "4. ledger_merge(program) before writing; the report is written "
        "ONLY from ledger_read outputs — no claim without its R-NNN.\n"
        "5. auditor/audit_report.py <report> — exit 0 or it does not "
        "ship; fix the work behind the report, not the auditor.")
    return {
        "detected_intent": "classify_report",
        "severity_goal": "-",
        "quota": None,
        "persona_mix": [],
        "phase_plan": [
            "cvss3_score per CONFIRMED finding",
            "vrt_classify per CONFIRMED finding",
            "triad + reproduction lines per block",
            "ledger_merge + write from records",
            "auditor until exit 0",
        ],
        "tools": ["cvss3_score", "vrt_classify", "ledger_merge",
                  "ledger_read", "auditor/audit_report.py"],
        "doctrine_prompt": prompt,
    }


def _forge_incident(request: str) -> dict:
    prompt = (
        "PROFESSIONAL ORDER (auto-forged from the operator's request):\n\n"
        "An adversary signal fired on assets this engagement is authorized "
        "to defend — pause the phase loop and engage the Binary Brain "
        "(adversary-tracker, the Shimomura lineage):\n\n"
        "1. Freeze before change: capture the current state before ANY "
        "response action; baseline the affected asset.\n"
        "2. sbb_declare() with the observed trigger; the null hypothesis "
        "(authorized/benign activity) is auto-inserted — never add your "
        "own.\n"
        "3. sbb_decide() / sbb_apply() loop: pre-registered halving tests, "
        "one bit, one record; tip-off actions stay gated while passive "
        "eliminators remain; no CONFIRMED on a single channel (Rule T).\n"
        "4. Identity and the last mile belong to the client's IR or law "
        "enforcement — the hunt ends in the audited handoff pack, never "
        "in retaliation.\n"
        "5. Then the phase loop resumes where it paused.")
    return {
        "detected_intent": "incident_response",
        "severity_goal": "-",
        "quota": None,
        "persona_mix": [],
        "phase_plan": [
            "freeze + baseline (no change first)",
            "sbb_declare with the observed trigger",
            "decide/apply loop to convergence",
            "audited handoff pack",
            "resume the paused phase loop",
        ],
        "tools": ["sbb_declare", "sbb_decide", "sbb_apply",
                  "ledger_append", "ledger_merge"],
        "doctrine_prompt": prompt,
    }


def _forge_default(request: str) -> dict:
    prompt = (
        "PROFESSIONAL ORDER (auto-forged from the operator's request):\n\n"
        "Execute the operator's request under the full Skill Mythos "
        "discipline.\n\n"
        "1. mythos_charter() — the routing contract; auth_status() — the "
        "R0 posture; both before any tool that touches a target.\n"
        "2. Interpret the request into the phase loop: recon and mapping "
        "organs for surface questions; the authorization matrix for access "
        "questions; payload organs with the craft layer for technical "
        "questions; classification tools at report time.\n"
        "3. Legend overlays by situation: tight scope or a WAF-hostile "
        "target -> the stealth principle (ghost-crawler); low-severity "
        "findings accumulating -> chain design (chain-architect); parser "
        "seams in scope -> protocol asymmetry (desync-hunter); client "
        "artifacts in scope -> teardown (deep-teardown); validators "
        "blocking honest payloads -> signal craft (signal-smith); "
        "inter-system trust questions -> the trust-graph audit "
        "(trust-graph-hunter); object-reference questions -> the Rosen "
        "IDOR discipline (auth-boundary-mapper v2).\n"
        "4. Every claim cites records; every CONFIRMED finding clears the "
        "differential triad, n_runs >= 2, CVSS 3.1 + VRT, auditor exit 0.\n"
        "5. State the exit numbers (R6): surfaces, hypotheses, closures by "
        "state, records appended.")
    return {
        "detected_intent": "default",
        "severity_goal": "-",
        "quota": None,
        "persona_mix": _personas(["orange-tsai", "adrian-lamo",
                                  "frans-rosen", "kevin-mitnick"]),
        "phase_plan": [
            "mythos_charter + auth_status",
            "phase interpretation of the request",
            "organ + legend-overlay selection",
            "gated execution with records",
            "exit numbers",
        ],
        "tools": ["mythos_charter", "auth_status", "list_skills",
                  "http_probe", "ledger_append", "cvss3_score",
                  "vrt_classify"],
        "doctrine_prompt": prompt,
    }


def doctrine_forge(request: str, context: str = "") -> dict:
    """Prompt escalation (charter A13): the operator's instruction,
    however terse or informal, expanded deterministically into the
    professional doctrine order the agent will actually execute.

    Feed it ANY operator request — one line of Indonesian, a sleepy
    'tolong lanjutkan pekerjaan bug bounty yang tertunda', a quota
    order like 'get me at least 3 high-medium bugs'. It returns the
    detected intent, the severity/quota goals it could extract, the
    persona mix (which legend lineages apply), the phase plan, the
    tools, and the full doctrine prompt — which always carries the
    quality gates, because escalation never relaxes discipline.
    Pure function: the same request forges the same order, character
    for character (A4)."""
    request = (request or "").strip()
    context = (context or "").strip()
    severity = _extract_severity(request)
    quota = _extract_quota(request)
    intent = _detect_intent(request)
    if intent == "bug_quota":
        forged = _forge_bug_quota(request, severity, quota)
    elif intent == "ai_surface":
        forged = _forge_ai_surface(request, severity, quota)
    elif intent == "continue_pending":
        forged = _forge_continue(request)
    elif intent == "surface_recon":
        forged = _forge_surface_recon(request)
    elif intent == "classify_report":
        forged = _forge_classify(request)
    elif intent == "incident_response":
        forged = _forge_incident(request)
    else:
        forged = _forge_default(request)
    forged["doctrine_prompt"] += (
        "\n\nEXECUTION DOCTRINE (skill-mythos "
        "references/autonomous-operation.md):\n"
        + "\n".join("- " + clause for clause in EXECUTION_DOCTRINE)
        + "\n\nWAR LOGIC (skill-mythos references/war-doctrine.md):\n"
        + "\n".join("- " + clause for clause in WAR_DOCTRINE))
    forged.update({
        "operator_request": request,
        "context": context,
        "gates": QUALITY_GATES,
        "execution_doctrine": EXECUTION_DOCTRINE,
        "war_logic": WAR_DOCTRINE,
        "escalation_rule":
            "execute the expanded order, not the bare words; the original "
            "request rides along verbatim and lands in the plan note",
        "deterministic": True,
    })
    return forged


# ---------------------------------------------------------------- CVSS tool

def cvss3_score(vector: str) -> dict:
    """Score a CVSS v3.1 base vector with the spec-exact arithmetic.

    Feed it the vector that describes the OBSERVED attack path; the score,
    severity band, and intermediate quantities come back computed once —
    the same arithmetic the report auditor uses to recheck your line."""
    return _cvss.base_score(vector)


# ----------------------------------------------------------------- VRT data

_TAXONOMY: list | None = None
_TAXONOMY_TRIED = False

PRIORITY_NAME = {1: "P1 (Critical)", 2: "P2 (High)", 3: "P3 (Medium)",
                 4: "P4 (Low)", 5: "P5 (Informational)"}
H1_SEVERITY = {1: "Critical", 2: "High", 3: "Medium", 4: "Low",
               5: "Informational"}


def _taxonomy_path() -> str:
    return os.path.join(paths.skills_dir(), MODULE, "references",
                        "vrt-taxonomy.json")


def _load_taxonomy() -> list | None:
    """Load the shipped official Bugcrowd VRT taxonomy (VRT 1.19 lineage,
    Apache-2.0). Returns None when the data file is absent — the classifier
    then answers from its built-in map and says so, loudly."""
    global _TAXONOMY, _TAXONOMY_TRIED
    if _TAXONOMY_TRIED:
        return _TAXONOMY
    _TAXONOMY_TRIED = True
    path = _taxonomy_path()
    if not os.path.isfile(path):
        _TAXONOMY = None
        return _TAXONOMY
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        _TAXONOMY = data.get("content") or data
    except (OSError, ValueError):
        _TAXONOMY = None
    return _TAXONOMY


def _resolve_vrt(dotted: str):
    """Walk `cat.sub.variant` through the shipped taxonomy; return the node
    (dict) or None. The live taxonomy at bugcrowd.com/vrt stays authoritative
    for submission — this file makes offline classification honest."""
    tax = _load_taxonomy()
    if tax is None:
        return None
    node = {"children": tax}
    for part in dotted.split("."):
        node = next((ch for ch in node.get("children", []) or []
                     if ch.get("id") == part), None)
        if node is None:
            return None
    return node


# --------------------------------------------------------- finding classes
# Each entry: vrt (dotted id path), p (contextual priority 1..5 or None when
# the taxonomy itself says Varies), canonical CVSS vector for the common
# case, and a short note. Variant selection per class happens in
# _variant(); flags come straight from the caller's observed context.

FINDING_CLASSES: dict[str, dict] = {
    "rce": {
        "vrt": "server_side_injection.remote_code_execution_rce", "p": 1,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "note": "full system compromise on the observed path"},
    "command_injection": {
        "vrt": "server_side_injection.remote_code_execution_rce", "p": 1,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "note": "the VRT carries OS command injection under the RCE node"},
    "sql_injection": {
        "vrt": "server_side_injection.sql_injection", "p": 1,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "note": "blind and union variants share the P1 node"},
    "xxe": {
        "vrt": "server_side_injection.xml_external_entity_injection_xxe",
        "p": 1,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "note": "raise A when the parser can be wedged"},
    "ssti": {
        "vrt": "server_side_injection.ssti", "p": None,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "note": "Varies in the taxonomy: basic payloads P4, custom payload "
                "chains reach P1 — set the P from demonstrated impact"},
    "lfi": {
        "vrt": "server_side_injection.file_inclusion.local", "p": 1,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "note": "LFI reads server files: P1 node in the taxonomy"},
    "ssrf": {
        "vrt": "server_security_misconfiguration."
               "server_side_request_forgery_ssrf", "p": 2,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N",
        "note": "variant set by internal/sensitive flags; the bounded-proof "
                "doctrine (one canary) maps to the external low-impact nodes"},
    "xss_reflected": {
        "vrt": "cross_site_scripting_xss.reflected", "p": 3,
        "cvss": "AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
        "note": "self_only=True is the self-XSS P5 variant"},
    "xss_stored": {
        "vrt": "cross_site_scripting_xss.stored", "p": 2,
        "cvss": "AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
        "note": "victim-interaction-free delivery raises impact: raise UI to "
                "N and C/I to the observed blast radius"},
    "idor": {
        "vrt": "broken_access_control.idor", "p": 3,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "note": "variant set by sensitive/modify context: view-sensitive P3, "
                "view+modify P1, GUID objects P4, non-sensitive P5"},
    "auth_bypass": {
        "vrt": "broken_authentication_and_session_management."
               "authentication_bypass", "p": 1,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "note": "unauthenticated access to an authenticated plane"},
    "session_fixation": {
        "vrt": "broken_authentication_and_session_management."
               "session_fixation", "p": 3,
        "cvss": "AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N",
        "note": "remote attack vector P3; local-only P5"},
    "session_invalid_persist": {
        "vrt": "broken_authentication_and_session_management."
               "failure_to_invalidate_session", "p": 4,
        "cvss": "AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N",
        "note": "logout/password-change invalidation P4; other lifecycle "
                "events P5"},
    "open_redirect": {
        "vrt": "unvalidated_redirects_and_forwards.open_redirect.get_based",
        "p": 4,
        "cvss": "AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N",
        "note": "GET-based P4; pair with oauth_misconfiguration when it "
                "feeds a redirect_uri weakness"},
    "csrf": {
        "vrt": "cross_site_request_forgery_csrf.action_specific."
               "authenticated_action", "p": 3,
        "cvss": "AV:N/AC:L/PR:L/UI:R/S:U/C:L/I:L/A:N",
        "note": "application-wide token absence is the P2 "
                "application_wide node — say so when you proved it"},
    "exposed_debug_portal": {
        "vrt": "server_security_misconfiguration.exposed_portal."
               "non_admin_portal", "p": 3,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
        "note": "admin portals are the P1 admin_portal node; "
                "auth-protected ones P5"},
    "verbose_error": {
        "vrt": "sensitive_data_exposure.visible_detailed_error_page."
               "descriptive_stack_trace", "p": 5,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
        "note": "detailed server configuration disclosed is the P4 "
                "detailed_server_configuration variant"},
    "internal_ip_disclosure": {
        "vrt": "sensitive_data_exposure.internal_ip_disclosure", "p": 5,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
        "note": "drop C to N when nothing actionable leaks — the taxonomy "
                "baseline is P5 informational"},
    "graphql_introspection": {
        "vrt": "sensitive_data_exposure.graphql_introspection_enabled",
        "p": 5,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
        "note": "introspection alone is P5; the schema-guided IDOR/BAC "
                "findings that follow it are rated on their own nodes"},
    "secrets_exposure": {
        "vrt": "sensitive_data_exposure.disclosure_of_secrets."
               "for_publicly_accessible_asset", "p": 1,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
        "note": "internal-asset placement is the P3 for_internal_asset "
                "variant; sample/invalid credentials the P5 variant"},
    "jwt_disclosure": {
        "vrt": "sensitive_data_exposure.disclosure_of_secrets."
               "sensitive_information_disclosed_jwt", "p": 5,
        "cvss": "AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N",
        "note": "claims-readable JWTs are the taxonomy's P5 node"},
    "subdomain_takeover": {
        "vrt": "server_security_misconfiguration.misconfigured_dns."
               "subdomain_takeover", "p": 3,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N",
        "note": "dangling DNS + claimable service; prove the claim with a "
                "bounded marker, then stop"},
    "default_credentials": {
        "vrt": "server_security_misconfiguration.using_default_credentials",
        "p": 1,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "note": "factory credentials on a reachable plane"},
    "race_condition": {
        "vrt": "server_security_misconfiguration.race_condition", "p": None,
        "cvss": "AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N",
        "note": "Varies in the taxonomy: set P from the demonstrated "
                "double-spend / mass-assignment impact"},
    "path_traversal": {
        "vrt": "server_security_misconfiguration.path_traversal", "p": None,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
        "note": "Varies in the taxonomy: file-read vs file-write decides "
                "the band"},
    "cors_misconfiguration": {
        "vrt": "server_security_misconfiguration."
               "unsafe_cross_origin_resource_sharing", "p": None,
        "cvss": "AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
        "note": "Varies in the taxonomy: credentialed reflection to an "
                "attacker origin reads as account-data exposure"},
    "clickjacking": {
        "vrt": "server_security_misconfiguration.clickjacking."
               "sensitive_action", "p": 4,
        "cvss": "AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N",
        "note": "non-sensitive actions are the P5 variant"},
    "rate_limit_bypass": {
        "vrt": "server_security_misconfiguration.no_rate_limiting_on_form."
               "login", "p": 4,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
        "note": "login/registration/sms nodes are P4; change-password P5"},
    "oauth_account_takeover": {
        "vrt": "server_security_misconfiguration.oauth_misconfiguration."
               "account_takeover", "p": 2,
        "cvss": "AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N",
        "note": "redirect_uri weaknesses sit on the adjacent "
                "insecure_redirect_uri node and Vary"},
    "two_fa_bypass": {
        "vrt": "broken_authentication_and_session_management.two_fa_bypass",
        "p": 3,
        "cvss": "AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:N/A:N",
        "note": "second-factor bypass on an otherwise sound login"},
    "username_enumeration": {
        "vrt": "broken_access_control.username_enumeration."
               "non_brute_force", "p": 4,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
        "note": "brute-force-flavored enumeration is the P5 node under "
                "server_security_misconfiguration"},
    "directory_listing": {
        "vrt": "server_security_misconfiguration."
               "directory_listing_enabled.non_sensitive_data_exposure",
        "p": 5,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
        "note": "sensitive data in the listing Varies (P1-P4) — rate what "
                "the listing actually exposed"},
    "request_smuggling": {
        "vrt": "server_security_misconfiguration.request_smuggling", "p": None,
        "cvss": "AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N",
        "note": "Varies in the taxonomy: set P from the demonstrated "
                "front/back-end desync impact"},
    "ai_prompt_injection": {
        "vrt": "ai_application_security.prompt_injection."
               "system_prompt_leakage", "p": 2,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
        "note": "system-prompt leakage is the taxonomy's P2 variant under "
                "prompt_injection"},
    "ai_output_xss": {
        "vrt": "ai_application_security.improper_output_handling."
               "cross_site_scripting_xss", "p": 3,
        "cvss": "AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
        "note": "model output rendered as HTML/MD without sinking it "
                "safely"},
    "ai_key_leak": {
        "vrt": "ai_application_security.sensitive_information_disclosure."
               "key_leak", "p": 1,
        "cvss": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
        "note": "provider/API keys reachable through the AI surface"},
    "xssi": {
        "vrt": "sensitive_data_exposure.xssi", "p": None,
        "cvss": "AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:N/A:N",
        "note": "Varies in the taxonomy: script-include theft of "
                "authenticated JSON"},
}

_MODIFIER_FLAG_DOC = (
    "flags: authenticated (PR:L), user_interaction (UI:R), scope_changed "
    "(S:C), internal / sensitive / admin / self_only (variant selection)")


def _variant(klass: str, entry: dict, flags: dict) -> tuple[str, int | None, str]:
    """Per-class variant selection from observed context flags.

    Returns (dotted_vrt_path, contextual_priority, note). Falls back to the
    class defaults whenever the flags do not discriminate."""
    f = flags
    if klass == "ssrf":
        if f["internal"] and f["sensitive"]:
            return (entry["vrt"] + ".internal_secrets_exposure", 2,
                    "internal service reached, secrets returned")
        if f["internal"]:
            return (entry["vrt"] + ".internal_data_exposure", 3,
                    "internal service reached, data returned")
        return (entry["vrt"] + ".external_low_impact", 5,
                "external-only with bounded proof — the canary doctrine")
    if klass == "xss_reflected":
        if f["self_only"]:
            return (entry["vrt"] + ".self", 5, "self-XSS: attacker and "
                    "victim are the same session")
        return (entry["vrt"] + ".non_self", 3, "reflected into another "
                "session's page")
    if klass == "xss_stored":
        if f["self_only"]:
            return (entry["vrt"] + ".self", 5, "stored but self-only")
        if f["admin"]:
            return (entry["vrt"] + ".privileged_user_to_privilege_"
                    "elevation", 3, "privileged context, privileged target")
        return (entry["vrt"] + ".non_admin_to_anyone", 2,
                "stored payload served to arbitrary victims")
    if klass == "idor":
        if f["self_only"] or not f["sensitive"]:
            return (entry["vrt"] + ".view_non_sensitive_information", 5,
                    "non-sensitive object data visible across tenants")
        if f["admin"]:
            return (entry["vrt"] + ".modify_view_sensitive_information_"
                    "guid", 4, "GUID objects slow but not stop enumeration")
        if f["scope_changed"]:
            return (entry["vrt"] + ".modify_view_sensitive_information_"
                    "iterable_object_identifiers", 1,
                    "view AND modify across the trust boundary")
        return (entry["vrt"] + ".view_sensitive_information_iterable_"
                "object_identifiers", 3, "sensitive object data readable "
                "cross-tenant")
    if klass == "secrets_exposure":
        if not f["sensitive"]:
            return (entry["vrt"].rsplit(".", 1)[0] +
                    ".intentionally_public_sample_or_invalid", 5,
                    "sample or invalid credentials")
        if f["internal"]:
            return (entry["vrt"].rsplit(".", 1)[0] + ".for_internal_asset",
                    3, "live secrets on an internal asset")
        return (entry["vrt"], 1, "live secrets on a public asset")
    if klass == "session_fixation":
        if not f["internal"]:
            return (entry["vrt"] + ".remote_attack_vector", 3,
                    "remote fixation through attacker-controlled session id")
        return (entry["vrt"] + ".local_attack_vector", 5,
                "local-only fixation")
    if klass == "exposed_debug_portal":
        if f["admin"]:
            return (entry["vrt"].rsplit(".", 1)[0] + ".admin_portal", 1,
                    "administrative plane exposed without auth")
        return (entry["vrt"], 3, "non-admin portal plane exposed without "
                "auth")
    if klass == "clickjacking":
        if not f["sensitive"]:
            return (entry["vrt"].rsplit(".", 1)[0] + ".non_sensitive_action",
                    5, "click-shielded action is non-sensitive")
        return (entry["vrt"], 4, "click-shielded action is sensitive")
    return entry["vrt"], entry["p"], entry["note"]


def vrt_classify(finding_class: str, authenticated: bool = False,
                 user_interaction: bool = False, scope_changed: bool = False,
                 internal: bool = False, sensitive: bool = True,
                 admin: bool = False, self_only: bool = False) -> dict:
    """Classify one finding class into Bugcrowd VRT + P-rating + HackerOne
    severity, with a CVSS 3.1 template for the observed context.

    Pass the flags you OBSERVED (not the ones that flatter the score):
    %s. The answer is resolved against the shipped official taxonomy
    (vrt-taxonomy.json in the skill-mythos bundle) and says so when that
    resolution was unavailable. The live taxonomy at bugcrowd.com/vrt stays
    the submission-time authority — cross-check before you file.""" % _MODIFIER_FLAG_DOC
    key = (finding_class or "").strip().lower().replace(" ", "_").replace("-", "_")
    if key not in FINDING_CLASSES:
        raise ValueError(
            "finding_class %r not supported — supported classes: %s"
            % (finding_class, ", ".join(sorted(FINDING_CLASSES))))
    entry = FINDING_CLASSES[key]
    flags = {"authenticated": authenticated,
             "user_interaction": user_interaction,
             "scope_changed": scope_changed, "internal": internal,
             "sensitive": sensitive, "admin": admin, "self_only": self_only}
    dotted, prio, note = _variant(key, entry, flags)

    notes = [note, entry["note"]] if note != entry["note"] else [note]

    # resolve against the shipped official taxonomy
    node = _resolve_vrt(dotted)
    resolved = False
    if node is not None:
        resolved = True
        tax_prio = node.get("priority")
        if tax_prio is None:
            notes.append("taxonomy marks this node Varies — P set from the "
                         "context you passed; triage may adjust")
        elif prio is not None and tax_prio != prio:
            notes.append("contextual P%d overridden by taxonomy baseline "
                         "%s" % (prio, PRIORITY_NAME[tax_prio]))
            prio = tax_prio
        elif prio is None:
            prio = tax_prio
        name = node.get("name", "")
    else:
        name = dotted
        notes.append("shipped taxonomy data unavailable at %s — mapping "
                     "answered from the built-in table; cross-check the "
                     "live VRT" % os.path.relpath(
                         _taxonomy_path(), paths.root()))
    if prio is None:
        notes.append("priority stays context-dependent (Varies) — state "
                     "the demonstrated impact in the report")

    # CVSS template: canonical vector of the class, mutated by observed flags
    metrics = _cvss.parse_vector(entry["cvss"])
    applied = []
    if authenticated and metrics.get("PR") == "N":
        metrics["PR"] = "L"
        applied.append("PR:L (authenticated)")
    if user_interaction and metrics.get("UI") == "N":
        metrics["UI"] = "R"
        applied.append("UI:R (user interaction)")
    if scope_changed and metrics.get("S") == "U":
        metrics["S"] = "C"
        applied.append("S:C (scope changed)")
    # variant shaping: the discriminating variants carry their own impact
    # shape so the template never flatters a weaker variant with the
    # canonical (high-impact) metrics
    if key == "ssrf" and not flags["internal"]:
        metrics.update(C="N", I="N", A="N", S="U")
        applied.append("C/I/A:N, S:U (external-only, bounded canary proof)")
    elif key == "idor" and not flags["sensitive"]:
        metrics.update(C="L")
        applied.append("C:L (non-sensitive object data)")
    elif key == "secrets_exposure" and not flags["sensitive"]:
        metrics.update(C="L", I="L")
        applied.append("C/I:L (sample or invalid credentials)")
    vector = "/".join("%s:%s" % (k, metrics[k]) for k in _cvss.REQUIRED)
    score = _cvss.base_score(vector)
    notes.append("cvss template reflects the flags you passed (%s) — "
                 "adjust metrics to the observed attack path, then rescore"
                 % ("; ".join(applied) if applied else "canonical case"))
    notes.append("verify the category against the live VRT "
                 "(bugcrowd.com/vrt) before submission")

    return {
        "finding_class": key,
        "vrt_id": dotted,
        "vrt_name": name,
        "priority": PRIORITY_NAME.get(prio, "Varies (P1-P5)") if prio else
                    "Varies (P1-P5)",
        "p": prio,
        "hackerone_severity": H1_SEVERITY.get(prio, "set with context"),
        "taxonomy_resolved": resolved,
        "context": flags,
        "cvss_template": {
            "vector": score["vector"],
            "base_score": score["score"],
            "severity_band": score["severity"],
        },
        "notes": notes,
    }
