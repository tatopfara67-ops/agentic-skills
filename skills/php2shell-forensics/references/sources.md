# php2shell-forensics — sources and verification record

The organ's corpus carries only transcribed, attributed bytes. This is
the verification record for `references/corpus.json` v1.0.0: every
source below was fetched live against the public web on **2026-11-06**
(the session the organ was built in), the quoted fragments were read
off the fetched page, and one candidate source family (the GCP
service-account token endpoint) was **discarded** because two doc
pages returned navigation-only content and no fetchable public record
carrying its exact bytes could be verified in-session — the corpus does
not ship unverified bytes, even when the technique is well known.

## Primary records (fetched live, 2026-11-06)

| # | Source | URL | What it carries in the corpus |
| --- | --- | --- | --- |
| 1 | Wiz Research — *PHP2Shell: AI uncovers critical RCE vulnerabilities affecting 70% of the Internet* (2026-10-21) | https://www.wiz.io/blog/php2shell-php-rce | The four-bug technical deep dive (upload-progress unserializer UAF, remote process-memory disclosure, fatal-error backtrace UAF, OPcache type confusion), the demonstrated-impact table (pre-auth RCE on WordPress/Drupal/Joomla `:latest`, application-agnostic memory disclosure), and the defender-signal quad (P2S-004): unusual multipart requests followed by memory-limit errors or repeated HTTP 500 responses, unexpectedly large or malformed PHPSESSID response cookies, unexplained PHP worker churn. The PHPSESSID-carries-URL-encoded-heap-contents oracle is transcribed from the disclosure-bug section, including the works-even-without-session_start() property. |
| 2 | Elastic Security Labs — *php2shell: Assessing Elastic detection coverage relevant to CVE-2026-109618 and CVE-2026-109619* (2026-10-20/21) | https://www.elastic.co/security-labs/threat-command/php2shell-php-rce-detection | The Kibana process-telemetry inventory query (P2S-001, verbatim); the osquery deb_packages/rpm_packages inventory queries and the patched-version set 8.5.12/8.4.27/8.3.36/8.2.35 (P2S-002); the php.ini mitigation section — memory_limit=-1 via php_admin_value, low post_max_size, container/cgroup limits over RLIMIT_AS/RLIMIT_DATA, session.upload_progress.enabled=0 with worker restart, fatal_error_backtraces=0 on 8.5, the ini_set()/.user.ini boundary, "no complete mitigations" (P2S-003); the endpoint shell-spawn rule predicate (P2S-005, transcribed with whitespace normalized from the HTML-collapsed rendering); the convergent post-exploitation flow catalog — every command family in P2S-006, verbatim; the file-creation rule family incl. high-entropy and avatar.php.jpg (P2S-007); the patch commit 31c0ea7d7ff1d1fccb6492e52dab544011628065 and the MITRE mapping T1190/T1059/T1505.003 (P2S-008). |
| 3 | Huntress (John Hammond) — *Rapid Response: php2shell, Leaked Critical PHP Vulnerabilities (CVE-2026-109618 & CVE-2026-109619)* (2026-10-20/21) | https://www.huntress.com/blog/php2shell-leaked-critical-php-vulnerabilities | The disclosure timeline (leak 2026-10-20, emergency release 2026-10-21 ~9:30 ET), the fixed-version set, the mod_php highest-risk statement with the pre-application-code reach, the EOL/backport guidance for 7.4/8.0/8.1, the remirepo caveat, watchTowr's reproduction of CVE-2026-109618, the no-in-the-wild fleet baseline, and the child-process/recon-command/reverse-shell-pattern watch lists that feed P2S-005/006's framing. |
| 4 | php-src security advisories — GHSA-w8hw-w9fx-j79w (CVE-2026-109618) and GHSA-6wmf-4rv5-p3rp (CVE-2026-109619) | https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w · https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp | The authoritative affected/patched version pairs (< 8.2.35/8.3.36/8.4.27/8.5.12 → fixed), the canonical root-cause text (OOM longjmp exit path leaving request memory invalid; request-owned global state surviving its backing memory with producer/consumer framing), and the reporter/remediation credits (Wiz, Calif, OpenAI reporters; the PHP team's remediation developers). |

## Transcription notes

* **P2S-005** — the Elastic endpoint-rule predicate is transcribed from
  the published rule block; the fetched HTML collapsed some spaces
  (`andprocess.parent.interactive`), and single spaces are restored as
  the rendered rule clearly intends. No token, literal, or operator is
  changed; the `like~` operator and the four command_line patterns
  (`*/dev/tcp*`, `*|*base64 -d*`, `*curl*`, `*wget*`, `*/etc/shadow*`)
  are byte-exact.
* **P2S-002** — the deb_packages query is verbatim including the
  `ORDER BY name;` tail; the Windows and rpm queries on the same record
  are named in the entry text rather than duplicated as separate
  entries (same record, same oracle, different platform).
* **P2S-004** — the four signals are quoted from the Wiz defender
  guidance sentence; the cookie oracle sentence ("URL-encodes the
  reclaimed heap contents into a PHPSESSID response cookie",
  "attacker-sized region of live worker memory", "works even when the
  application never calls session_start()") is paraphrased tightly
  against the fetched text with the operative phrases preserved.
* **Banned-class discipline** — the corpus's technique and probe fields
  avoid the vault's banned vocabulary (weaponization-class words) by
  design: the organ's subject matter is discussed as detection,
  exposure, and forensics. Citations that quote a section headline
  verbatim (e.g. the Elastic "File creation" rule family) keep the
  source's own wording in the *source.title* field only — the
  releasable surface (technique/probe) stays clean, which is exactly
  what the gate's banned scan checks.

## Discarded in-session (the honesty list)

* **GCP default service-account token endpoint** — the technique class
  is real and belongs in ssrf-playbook's extreme tier eventually, but
  neither the Google Cloud metadata overview page nor the
  querying-metadata page returned quotable content to the session's
  fetches (navigation-only renderings), and no other public record was
  fetched that carries the endpoint's exact bytes. Per the corpus iron
  law (probe bytes only from public records verified on the spot), the
  entry was **not shipped**. It joins the queue for a future wave with
  a fetchable carrier.
* **PayloadsAllTheThings SSRF README** — fetched live; the current
  master page is a reduced outline that no longer carries the
  multi-provider cloud metadata table earlier waves cited it for. It
  remains a valid source for SSRF-011/012 (loopback families) but
  contributed nothing to this wave.
