# Reference — Case Studies

> Part of **mythos-bug-hunter v4.3.0** (package architecture).
> **Load when:** Grounded narratives: php2shell (CVE-2026-109618/109619), php.net 2021, Next.js CVE-2025-29927, MCP tool poisoning, xz-utils.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

## C. Case Studies

### C.1 php2shell — CVE-2026-109618 / CVE-2026-109619 (October 2026)

Two critical PHP-engine RCEs, CVSS v4.0 9.2 each, leaked on 2026-10-20
before the coordinated disclosure; PHP shipped emergency releases on
2026-10-21 (8.5.12 / 8.4.27 / 8.3.36 / 8.2.35). All web-serving SAPIs were
affected (PHP-FPM, Apache mod_php, php-cgi, FrankenPHP, LiteSpeed) on PHP
≥ 5.4. CVE-2026-109618: out-of-memory during request setup leaves
partially initialized request data that cleanup later treats as valid —
unauthenticated RCE as the web worker (validated against default mod_php).
CVE-2026-109619: request-specific state retained after its backing memory
is freed; worker reuse turns it into heap UAF + memory disclosure + RCE.
Public analysis showed exploitation typically needs target-specific
preconditions (e.g. an LFI or a multipart heap amplifier — the public PoC
used ~390x nested empty-filename `$_FILES` fields), so mass exploitation
was constrained even as targeted attacks emerged (first observed by
Cloudflare at 07:43 UTC on release day). EOL branches relied on mitigations
(disable `session.upload_progress` and `fatal_error_backtraces`, cap
multipart complexity, recycle workers) and detection heuristics (PHP
workers spawning shells/interpreters/download tools; `/dev/tcp/`,
`fsockopen`, `mkfifo` patterns). **Skill relevance:** sections 25.1-25.2
exposure mapping; §4 item 11 no-exploit rule; §30 TRENDFRESH trigger.

### C.2 php.net Git Server Compromise (March 2021)

Attackers compromised the official `git.php.net` server and pushed two
commits impersonating maintainers (Rasmus Lerdorf, Nikita Popov) with the
message "[skip-ci] Fix typo". The payload in `ext/zlib/zlib.c` checked for
a crafted `HTTP_USER_AGENTT` header containing "zerodium" and passed the
header's tail to `zend_eval_string` — a remote-code-execution backdoor
disguised as a typo fix. Detection was human vigilance (a maintainer
spotted and reverted it; the attacker re-pushed under another identity).
Response: the GitHub mirror became canonical and 2FA became mandatory.
**Skill relevance:** §3.8 provenance (authorship is spoofable), §25.3
integrity checks, §25.4 safety rules.

### C.3 Next.js Middleware Authorization Bypass — CVE-2025-29927 (March 2025)

Self-hosted Next.js apps using middleware for auth were bypassable by
sending the internal header `x-middleware-subrequest` with the middleware
path value; Next.js treated the request as an internal subrequest and
skipped middleware entirely. Patched in 12.3.5 / 13.5.9 / 14.2.25 /
15.2.3; Vercel/Netlify/static-export deployments unaffected; on 15.x the
`MAX_RECURSION_DEPTH` (default 5) counting logic was the bypass surface.
**Skill relevance:** §23.5 playbook and §21.4 probe catalog.

### C.4 MCP Tool Poisoning, Rug Pulls, and Shadowing (2025 research)

Invariant Labs documented: (1) tool poisoning — malicious instructions
embedded in a tool's description (an `add(a, b, sidenote)` helper whose
docstring ordered the agent to read `~/.cursor/mcp.json` and `~/.ssh/
id_rsa` and pass them via `sidenote`); (2) rug pulls — the server changes
tool descriptions after client approval; (3) cross-server shadowing — a
malicious server's descriptions manipulate agent behavior toward a
different, trusted server (authentication hijacking). **Skill relevance:**
§24.5, ASI02/ASI04 mapping.

### C.5 xz-utils Backdoor (2024) — Brief

A multi-year social-engineering campaign gained maintainer access to
xz-utils and shipped an obfuscated backdoor (versions 5.6.0/5.6.1) that
patched SSH authentication paths via the library's build system; it was
caught by a downstream user investigating subtle performance anomalies.
**Skill relevance:** §3.8, §25 — provenance of maintainers and artifacts
alike; baseline behavioral anomalies as detection signals.

### C.6 References (primary sources used for this revision)

- php2shell / CVE-2026-109618 & CVE-2026-109619:
  Huntress rapid response —
  https://www.huntress.com/blog/php2shell-leaked-critical-php-vulnerabilities ;
  Sansec threat research — https://sansec.io/research/php2shell ;
  Google Cloud responding guidance —
  https://cloud.google.com/blog/products/identity-security/responding-to-core-php-vulnerabilities-cve-2026-109618-cve-2026-109619
- php.net Git server compromise (2021):
  https://php.watch/news/2021/03/git-php-net-hack ;
  https://www.welivesecurity.com/2021/03/30/backdoor-php-source-code-git-server-breach
- Next.js CVE-2025-29927:
  https://securitylabs.datadoghq.com/articles/nextjs-middleware-auth-bypass ;
  https://nvd.nist.gov/vuln/detail/CVE-2025-29927
- Race conditions / single-packet attack (PortSwigger):
  https://portswigger.net/research/the-single-packet-attack-making-remote-race-conditions-local ;
  https://portswigger.net/web-security/race-conditions
- Web cache attacks (PortSwigger Academy):
  https://portswigger.net/web-security/web-cache-deception ;
  https://portswigger.net/web-security/web-cache-poisoning
- JWT attack classes:
  https://blogs.jsmon.sh/jwt-algorithm-confusion-to-account-takeover-rs256-hs256-jku-injection-kid-sqli ;
  https://workos.com/blog/jwt-algorithm-confusion-attacks
- MCP tool poisoning (Invariant Labs):
  https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
- OWASP frameworks:
  Top 10:2025 — https://top10.owasp.org/ ;
  LLM Top 10 2025 — https://genai.owasp.org/llm-top-10/ ;
  Agentic Top 10 2026 —
  https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026 ;
  API Security Top 10 — https://owasp.org/API-Security/editions/2023/en/0x11-t10/
  Agentic Top 10 walkthrough —
  https://auth0.com/blog/owasp-top-10-agentic-applications-lessons

---
