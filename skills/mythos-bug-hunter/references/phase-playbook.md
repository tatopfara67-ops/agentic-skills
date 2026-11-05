# Reference — The Phase Playbook (Recon to Report, Action by Action)

> Part of **mythos-bug-hunter v4.7.0** (package architecture).
> **Load when:** An engagement starts (Mode F), a phase transition lands, or
> the agent needs the *execution sequence* for the phase it is standing in:
> entry conditions, numbered actions, methods, decision rules, exit gate,
> failure modes. SKILL.md §4 holds the phase contracts; this module is the
> operating manual that walks each phase action by action.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

## 35. The Phase Playbook

### 35.0 How to Read This Playbook

Each phase block has six fixed parts: **Objective** (one sentence), **Entry**
(what must already be true), **Actions** (numbered, each with its method and
where the output lands), **Decisions** (the routing rules that choose the
next action), **Exit gate** (from SKILL.md §4, restated operationally), and
**Failure modes** (named anti-patterns with their ledger tell).

Phase numbering follows SKILL.md §4 (0–5). The older 8-step machine in
`engagement-architecture.md` §16 maps onto it as: §16.1 SETUP → Phase 0,
MAPPING → Phase 1, HYPOTHESES → Phase 2, VALIDATION → Phase 3, IMPACT →
Phase 4, REPORTABILITY + REPORTING + NEXT/STOP → Phase 5 plus the loop-back
rules in §35.4. Depth routing: when an action cites another module, load
that module *at that action*, not before — context discipline
(`research-protocol.md` §29) outranks completeness anxiety.

Throughout: the moment loop (`researcher-conduct.md` §34.2) runs on every
observation in every phase; the ledger is the only memory; R0–R7 hold.

---

### 35.1 Phase 0 — Scoping: Prove the Right to Test, Then Learn the Facts

**Objective:** authorization proven in the ledger, baseline facts recorded,
capabilities and budgets fixed — before any crafted request exists.

**Entry:** the operator names a target or program.

**Actions:**

1. **Read the scope artifact.** Program page, engagement letter, or lab
   declaration. Extract five things verbatim: in-scope assets (exact
   hostnames/wildcards), forbidden actions (e.g. "no automated scanning",
   "no DoS"), severity floor for acceptance, disclosure policy, and any
   asset exclusions. Write the `AUTH` ledger record citing the artifact URL
   or document and quoting the scope line. **No AUTH record, no requests —
   this is R0, and it has no small violations.**
2. **Resolve scope ambiguity with one blocking question.** Ambiguities worth
   a message: wildcard depth (`*.example.com` — does `a.b.example.com`
   count?), third-party SaaS on the domain, API rate expectations. Format
   per §34.4: options + costs + recommendation. Ambiguities not worth a
   message: anything answerable by reading the program page again.
3. **Build the fact table.** For each in-scope hostname, run the six-probe
   baseline, one FACT record per probe:

   ```bash
   curl -sS -D - -o /dev/null "https://app.example.com/"        # headers: Server, X-Powered-By, CSP, HSTS, Set-Cookie flags, redirect chain
   curl -sS "https://app.example.com/robots.txt"                 # disallowed paths = a free endpoint lead list
   curl -sS "https://app.example.com/sitemap.xml"                # routes the app itself advertises
   curl -sS "https://app.example.com/.well-known/security.txt"   # disclosure posture, sometimes contacts
   curl -sS "https://app.example.com/favicon.ico" | md5sum       # stable fingerprint for dedup later
   curl -sS -o /dev/null -w "%{http_code} %{size_download} %{time_total}\n" "https://app.example.com/"
   ```

   Rules: fingerprint from *behavior* (cookie names, header sets, error-page
   shapes), never from the `Server` banner alone — banners lie more often
   than they inform, and version-derived priors are capped at 60%
   (`logic-and-probability.md` §10). Each technology claim in every later
   phase must trace to one of these FACT records.
4. **Inventory your capabilities** (R5's other half). One command, one FACT
   record:

   ```bash
   for t in subfinder amass dnsx httpx gau waymore katana jsluice arjun ffuf nuclei naabu uro wafw00f interactsh-client dalfox ghauri byp4xx nomore403 gowitness; do
     command -v "$t" >/dev/null 2>&1 && echo "HAVE $t" || echo "MISSING $t"
   done
   ```

   Plus: enumerate available MCP tool servers and their security tools.
   Record which rung of the fallback ladder (MCP → CLI → curl → python3)
   this engagement actually runs on. Every plan you make from here must be
   executable at that rung.
5. **Set the budgets** (R7): defaults are 15 experiment cards per hypothesis
   cluster, 400 ledger records per engagement, and the three time-boxes from
   `recon-toolchain.md` §29.4 (5/20/45 minutes). Operator overrides are
   themselves ledger records.
6. **Secure test accounts** if authorization surfaces are in scope: ≥2
   accounts with different privilege levels, both yours. If unobtainable,
   record the blocker *and* what it disables — without account B, object-
   substitution experiments (the densest authz family) cannot run honestly;
   note that in the state so Phase 2 prices those hypotheses accordingly.

**Decisions:** in-scope asset with WAF in front → keep it, note the cost
penalty (§29.2's −1, not a skip); scope artifact silent on automated
scanning → ask once, default to manual-rate probing until answered; target
stack unknown after probes → proceed black-box, record the capability gap.

**Exit gate:** AUTH record + fact table (each probe cited) + capability
inventory + budgets + accounts-or-blocker, all in the ledger. Kickoff message
to the operator (§34.4 type 1).

**Failure modes:** *the brand tester* (testing `example.com` because it is
famous while the scope says `*.example.com` — or testing assets the scope
never listed); *the banner believer* (stack "known" from `Server:` alone);
*the silent starter* (first requests sent before the AUTH record exists).

---

### 35.2 Phase 1 — Recon: Build the Inventory Before Probing the Behavior

**Objective:** the attack-surface inventory (§14 categories 1–8 minimum),
every entry carrying evidence IDs, ordered by the triage score.

**Entry:** AUTH record exists. One hour of disciplined recon beats three
hours of spray — and recon *is* the first act of hunting, not the thing
before it.

**Actions (stages run in order; each stage's output is the next stage's
input; tool flags and rationale live in the §29.1 routing table — here it is
the sequence and the decisions that matter):**

1. **Passive subdomain enumeration** — no packets touch the target:

   ```bash
   subfinder -d example.com -silent -o subs_1.txt
   amass enum -passive -d example.com -o subs_2.txt
   curl -s "https://crt.sh/?q=%25.example.com&output=json" | jq -r '.[].name_value' | sort -u > subs_3.txt
   sort -u subs_*.txt > subs_all.txt
   ```

   Three sources minimum — sources disagree constantly, and the disagreement
   is free coverage. Decision: hosts resolving to in-scope IPs proceed;
   everything else is recorded and parked.
2. **Resolve and probe what is alive:**

   ```bash
   dnsx -l subs_all.txt -silent -a -resp -o resolved.txt
   httpx -l resolved.txt -status-code -title -tech-detect -content-length -json -o live.jsonl
   ```

   One `SURFACE` record per live host, the probe line as its result. Then
   immediately: triage score (§29.2) computes the backlog order; dedup key
   (§29.3) suppresses clones before they cost a single experiment.
3. **Port sweep only when scope permits and only as justified:** top-1000
   (`naabu`) on resolved in-scope IPs; full 65535 only on hosts whose triage
   score earned it. Each open service → `SURFACE` record.
4. **Historical URL archaeology:**

   ```bash
   gau example.com > urls_1.txt ; waymore -d example.com -o urls_2.txt
   uro <(sort -u urls_*.txt) > urls_dedup.txt
   ```

   The archive remembers endpoints the live site deleted: old API versions,
   debug routes, admin panels moved but not gone. Unique paths → `SURFACE`
   records; dead-but-archived URLs are version-gap leads (conduct rule S3),
   not trash.
5. **Active crawl for the SPA routes the archive cannot see:**

   ```bash
   katana -u https://app.example.com -d 3 -jc -kf all -o crawl.txt
   ```

   New routes → `SURFACE`; forms and their fields → category 6 entries.
6. **JS bundle analysis** — download the bundles the crawl referenced:

   ```bash
   jsluice urls bundle.js > js_urls.txt ; jsluice secrets bundle.js > js_secrets.txt
   ```

   Endpoints and params → `SURFACE`; key material → a `FACT` record and an
   immediate check against the secrets row of §29.1 (verification only
   where authorized — contacting a provider uninvited is a third-party
   effect R0 does not permit).
7. **Hidden parameter discovery** on the key endpoints:

   ```bash
   arjun -u "https://app.example.com/api/v1/users"
   ```

   Unlinked parameters are where authorization checks forget to exist —
   each discovered param attaches to its endpoint's inventory entry.
8. **Content discovery on live hosts** — the wordlist ladder escalates by
   cost, and the rate comes from the Phase 0 budget, never from impatience:

   ```bash
   ffuf -ac -t 20 -rate 30 -w raft-medium-directories.txt -u "https://target/FUZZ"
   ```

   `-ac` auto-calibrates against the target's own 404 behavior — a
   self-differential by design. Hits → `SURFACE`.
9. **Visual triage where scale justifies it** (`gowitness`): login portals,
   error-spewing debug pages, and default installs jump out of a screenshot
   grid in a way status codes never convey.

**Decisions:** stage ordering is cost-ordered — passive before active,
archive before crawl (free before paid); a stage that doubles coverage at
zero target cost (passive enum, archive) always runs in full; a stage that
spends requests (crawl, content discovery) runs to the traffic budget and
stops. Mid-engagement discoveries go to the **backlog**, never the active
queue (R1) — the active queue changes only when the current vector closes.

**Exit gate:** inventory categories 1–8 (§14.1) each have ≥1 entry with
evidence IDs, OR an explicit deferred-with-reason line; every live host has
a `SURFACE` record; triage order computed; dedup applied. "Recon complete"
is a claim with numbers: N assets, M endpoints, K parameters, per category.

**Failure modes:** *infinite recon* (recon as procrastination — the
countermeasure is the category checklist plus the time budget); *main-domain
fixation* (hundreds of hunters already harvested the famous host; the
staging box from last quarter has never been scanned); *single-source trust*
(one enum tool missing 20% of subdomains and nobody noticing).

---

### 35.3 Phase 2 — Hypotheses: Pre-Register the Attack Before Building It

**Objective:** every inventory entry has ≥1 falsifiable H-record (SKILL.md
§5 grammar) with a justified prior — or an explicit why-not.

**Entry:** Phase 1 exit gate passed. This is warzone time (§9): maximum
aggression, zero accountability for volume — accountability starts at the
gates, not at idea generation.

**Actions:**

1. **Run the surface-class × attack-class matrix.** For each populated
   inventory category, cross-reference the matching catalog and generate
   candidate mechanisms:

   | Inventory category (§14.1) | Generate hypotheses from |
   |---|---|
   | 7 Authentication, 8 authorization boundaries | §20 authorization matrix (actor→resource→action); §22 JWT catalog (`alg` confusion, `alg:none`, weak-key acceptance, claim validation order) |
   | 9 Object identifiers | ownership substitution: every ID-accepting endpoint × every foreign ID the app has ever shown you |
   | 10 Upload/download | upload validation bypass chains; served-from location (user content on the app origin → stored-XSS and content-type confusion families) |
   | 11 Redirects | open redirect on every `next`/`redirect`/`return_url` parameter, tested across auth states |
   | 12 OAuth/OIDC | §23.6: `redirect_uri` validation strictness, state/nonce presence, PKCE absence, token-in-URL flows |
   | 13 GraphQL | introspection on, field suggestions, global-ID replay across queries/mutations, depth/batching abuse only as DoS-relevant behavior within policy |
   | 14 WebSocket | origin validation on upgrade, per-message authorization, injection points in message schema |
   | 15 Exposed functionality | debug/admin endpoints: authentication on the route vs authorization on the action (BFLA shape) |
   | 16 Client-side JS | hardcoded secrets, forgotten internal endpoints, `postMessage` origin checks, DOM sinks |
   | 17 Third-party/webhooks | inbound webhook signature validation, SSO binding |
   | 18–19 AI/MCP surface | §24: prompt-injection-to-tool chains, output rendering path, agent memory scoping |
   | 20 Protocol edge | §23.1 smuggling, §23.2 cache poisoning/deception |
   | 21 Supply-chain (web tier) | §25: SRI presence, webhook signature checks, exposed CI artifacts |

2. **Run assumption enumeration on each core business flow** (checkout,
   refund, transfer, approval, signup — whatever the app's money and
   identity flows are). For each flow, write down the developer's
   assumptions, then negate each one as a hypothesis. The seven assumption
   families: **role** (only staff reach this), **ownership** (the object is
   the caller's), **state** (the object is in the state the flow expects),
   **ordering** (step N happens after step N−1), **uniqueness** (one per
   account), **idempotency** (retries are safe), **price integrity** (the
   client never sets the price). Each negation is one H-record: "if the
   ownership assumption is unenforced on POST /refund, then account A's
   token executes refund for account B's transaction id, observable as a
   200 plus B's balance change."
3. **Convert the anomaly backlog.** Every deviation classified during Phase
   1 (moment loop step 2, `researcher-conduct.md` §34.2) becomes an
   H-record by abduction: which mechanism would make this observation
   *inevitable*? Pre-register that mechanism.
4. **Convert scanner hits** (if the Phase 0 rung included nuclei/other):
   each hit → H-record with a capped prior (R5; conduct rule S6).
5. **Seed from prior sessions.** Park records, INCONCLUSIVE closures, and
   posterior-updated leads from earlier engagements on this target are
   generation input, not history: each re-enters as an H-record carrying its
   updated prior, and only new evidence (new account, new capability, new
   fact-table row) justifies the re-test — the disproven list stays hot
   (conduct habit 3).
6. **Assign priors with base rates, not vibes** (`logic-and-probability.md`
   §10): advisory coverage for the exact fingerprint, class frequency for
   the surface category, sibling-of-confirmed for seeded leads. Version-
   derived priors cap at 60% pending behavioral confirmation.
7. **Order the queue by EV/minute** (§10.7): high-impact × high-prior ×
   low-cost first. Write the why-not lines for hypothesis-less surfaces —
   an unexplained gap in coverage is a silent claim of "nothing there",
   which is a claim like any other.

**Decisions:** a hypothesis that cannot name its falsifier is returned for
rewriting, not downgraded; two hypotheses on one mechanism merge; a
hypothesis requiring out-of-scope actions is refused and recorded as
capability-limited (never silently dropped).

**Exit gate:** no hypothesis-less surface; the H-queue is ordered; P0/P1
TODOs (§15) exist for the top of the queue. Mechanical form (v4.7.0): every
hypothesis was minted through `hypothesis_register` (facts must cite ledger
records), and `hypothesis_list` shows the open set — that set emptying, via
`hypothesis_close`, is what actually opens Phase 3's exit.

**Failure modes:** *the narrative capture* (writing findings instead of
hypotheses — the tell is H-records containing severity adjectives); *the
boring-surface skip* (20 hypotheses on the admin panel, zero on the invoice
PDF export — backwards, because nobody watched the boring surface); *prior
pollution* (priors drifting upward under operator enthusiasm, §29.7).

---

### 35.4 Phase 3 — Testing: One Variable at a Time, Until Closure

**Objective:** every H-record reaches Closure (CONFIRMED / FALSIFIED /
INCONCLUSIVE) through experiment cards, or parks with a resume point.

**Entry:** ordered H-queue exists; test accounts or blockers recorded.

**Actions (the loop — this is the engagement's engine room):**

1. **Pick the next TODO** from the top of the P0/P1 queue (§15.3 factors,
   not enthusiasm).
2. **Write the E-card before any payload exists** (SKILL.md §6): baseline
   definition, treatment, control, `n_runs`, and the expected delta. A
   payload written before its card is retrodiction bait — discard it and
   write the card.
3. **Run the baseline** and record it. The baseline is the world as it is:
   same session, same endpoint, unmodified input. Expectation stated per
   §34.2.
4. **Run the treatment** — one variable changed, nothing else. One
   connection shape, one header, one ID, one byte.
5. **Run the control** — same effort, wrong knob. A valid control changes
   something the hypothesis says is *irrelevant*: for a header-bypass
   hypothesis, the control is a different irrelevant header (proving the
   target reacts to the *specific* header, not to any odd header); for an
   ID-substitution hypothesis, the control is a nonexistent ID (proving
   404-vs-403 semantics before the ownership test); for a timing claim, the
   control is the same request without the delay payload (jitter
   calibration). The control lights up → the delta was not specific →
   back to the mechanism, and the control's result goes in the ledger as a
   falsifier observation.
6. **Measure the delta** against the baseline — status, size, body hash,
   timing distribution (median of runs, never single-shot for timing).
7. **Route on the outcome:**

   | Outcome | Action |
   |---|---|
   | Delta reproduced + control clean | extend the evidence chain (§7 capture spec), check the reproduction floor (3 consecutive identical deltas deterministic; 20 attempts + two stable 10-attempt windows stochastic), then move toward Closure: CONFIRMED |
   | Delta not reproduced | hunt the confound: what differed between runs (state? cache? account? time?) — each candidate confound is itself a new H-record; the instability is a finding about the finding |
   | No delta at any rung | climb the probing ladder (§29.5: error-based → differential-content → time-based → OOB), one rung per card; ladder exhausted → Closure: FALSIFIED (bounded to the rungs tried) |
   | Partial / ambiguous delta | new H-record for the refined mechanism; the original stays open |

8. **Obey the clock:** 20-minute progress check on the active vector; rotate
   inventory categories between consecutive cards when stuck; 45-minute
   rabbit hole → mandatory Park (§29.4). A Park record stores: what was
   tried (E-card IDs), the leading untested angle, and the resume cost.
9. **On any Closure: CONFIRMED** — schedule the sibling sweep (§29.6):
   20 bounded minutes across naming/version/controller seams, siblings
   pre-registered with sibling-of-confirmed priors.
10. **Update state after every verdict change** (§18): queue, disproven
    list, blockers, counts. State is how the session survives context loss
    without becoming a goldfish (§34.6).

**Decisions:** treatment vs. control disagreement resolves toward the
control (specificity beats enthusiasm); an endpoint yielding three
consecutive no-delta cards rotates out per the anti-fixation rule (§15.3);
in-scope target switches are free, out-of-scope ones never happen (R0,
conduct S11).

**Exit gate:** all P0/P1 hypotheses at Closure or parked; the closure
vocabulary has exactly three words — "looks vulnerable" does not parse.

**Failure modes:** *payload spray* (requests without cards — the tell is
ledger EXPERIMENT records with no hypothesis ID in the note); *the
control-skiper* (most common exactly when the researcher feels most
certain, §34.7); *n=1 enthusiasm*; *the gambler* (15 cards on one knob with
no stability criterion).

---

### 35.5 Phase 4 — Impact: Prove the Bug Matters Without Doing Harm

**Objective:** for every CONFIRMED hypothesis — a canary-proven channel, a
bounded demonstration of reach, and an impact chain whose every hop cites
records.

**Entry:** at least one Closure: CONFIRMED.

**Actions:**

1. **Design the canary round-trip** (toolkit §26 library): generate a
   unique marker (`MYTHOS-CANARY-<uuid>`); inject it through the
   vulnerability's own channel; observe it cross the boundary; capture all
   three legs as ledger records. Only self-injected synthetic data ever
   demonstrates a channel — this is simultaneously the scientific standard
   and the legal posture.
2. **Demonstrate bounded reach, not maximal reach.** "Could download
   everything" is proven by retrieving exactly one canary or one
   depth-limited page and stopping. Enumeration bounds (depth, page,
   count) are stated in the report as design decisions, not accidents.
3. **Build the impact chain** primitive → hop → terminal impact, each hop
   individually evidenced. The report may claim only up to the weakest
   *verified* link: `SLEEP(5)` plus a read marker inside a blind injection
   is a specific, honest story; "RCE" without a demonstrated execution hop
   is a title with no evidence under it.
4. **Anchor severity to the demonstrated chain** — confidentiality /
   integrity / availability / authentication / authorization, at the
   actually-shown scope, with the reproduction rate stated honestly
   (stochastic findings report "12/20 attempts", because characterizing
   the variance *is* the reproduction).
5. **Run the duplicate check** before drafting: program known-issues and
   out-of-scope lists first, then a bounded external look (TRENDFRESH,
   `research-protocol.md` §30) for public writeups of the same endpoint
   and class. Likely-duplicate findings are reported as such or held,
   never laundered into "new" wording.

**Decisions:** chain hops that would require out-of-scope or destructive
actions are described, never executed; a finding whose only demonstrated
impact is "unusual behavior" fails the reportability gate (§19 criterion B)
and becomes an internal note.

**Exit gate:** every CONFIRMED finding has an impact chain citing records,
a canary reference, and a reproduction statement; report claims cite
records line by line.

**Failure modes:** *the extrapolator* ("could lead to RCE" as impact);
*the dumper* (touching real user rows to make severity look bigger — that
is not research, and the attestation in the report would be a lie);
*chain inflation* (unverified hops stated as if demonstrated).

---

### 35.6 Phase 5 — Report, Audit, Ship, and Close the Loop

**Objective:** a report written entirely from ledger records that passes the
mechanical auditor, shipped per program policy — plus the learning artifacts
that make the next engagement sharper.

**Entry:** Phase 4 exit gate passed.

**Actions:**

1. **Pass the reportability gate per finding** (§19, criteria A–G) *before*
   drafting. Any fail → obtain the missing evidence as a new TODO, keep
   the finding internal, or drop it.
2. **Draft from the ledger only** — open `ledger/records.md`, draft claim by
   cited record. Templates and JSON schemas: `report-templates.md` §28. The
   report contract (SKILL.md §13) is mechanical: severity lines cite
   R-NNN, hypothesis blocks carry Closure lines, no hedging vocabulary, no
   ungated victory language.
3. **Run the auditor and fix until green:**

   ```bash
   python3 scripts/audit_report.py report.md   # exit 0 ships; exit 1 lists violations
   ```

   Fix the *work* behind the violation when the report is right and the
   evidence is thin — never the reverse (fix the skill, not the gate).
4. **Ship via the program's channel** with the disclosure etiquette of
   §33: no public writeup before the program's disclosure window closes.
5. **Write the mistake ledger** (§31) with numbers: which priors were
   overconfident (prior vs. closure rate per source), which tools produced
   false leads, which conduct failure tells from §34.7 actually appeared in
   your ledger this session.
6. **Run the calibration audit:** recompute prior adjustments for the next
   engagement from this session's numbers. Self-awareness here is numeric
   or it is theater.
7. **Close the session:** final state summary, posterior-updated leads
   appendix (INCONCLUSIVE and parked items with their resume points),
   scratch files cleaned, `next_todo` written for whoever resumes —
   including future you after context loss.

**Exit gate:** auditor exit 0; report shipped or explicitly held with
reason; mistake ledger written; session state closed.

**Failure modes:** *memory drafting* (paragraphs with no record citations —
the auditor exists precisely for this); *the hedge* ("might allow an
attacker to…"); *the ghost close* (session ends without state summary, so
the resumed session re-tests disproven hypotheses).

---

### 35.7 The Compact Timeline — What a Full Engagement Looks Like

Illustrative two-day engagement on a mid-sized wildcard scope, shown so the
rhythm is concrete (times are T+hours from kickoff; every block's output is
ledger records, not memories):

| Clock | Phase | What happens |
|---|---|---|
| T+0.0–0.5 | 0 | Scope artifact read, AUTH recorded, fact table probes, capability inventory, budgets fixed; kickoff message sent |
| T+0.5–1.0 | 1 | Passive enum (3 sources), resolution, `httpx` probe; triage score orders the backlog; dedup parks 12 clone hosts |
| T+1.0–2.5 | 1 | Archive archaeology, crawl, JS analysis, hidden params on the top-10 endpoints |
| T+2.5–3.0 | 1 | Content discovery to traffic budget; inventory numbers stated: 34 assets, 217 endpoints, ~1.1k params; categories 1–8 gate passes |
| T+3.0–3.5 | 2 | Matrix + assumption enumeration → 38 H-records with priors; queue ordered by EV/minute |
| T+3.5–6.0 | 3 | Card loop on the top P1s: two FALSIFIED by ladder exhaustion, one 403 anomaly opens a header-routing H-record (conduct S2), one ID-substitution CONFIRMED at T+5.7 with clean control |
| T+5.7–6.1 | 3 | Sibling sweep (§29.6): naming-seam twin found, pre-registered, queued next |
| T+6.1–6.5 | 4 | Canary round-trip on the confirmed finding; bounded one-page reach proof; impact chain drafted hop by hop |
| T+6.5–7.0 | 5 | Reportability gate, draft from ledger, auditor exit 0, shipped; state summary + park records written |
| Day 2 | 3–5 | Queue drains: sibling CONFIRMED; two rabbit holes parked at 45 minutes; a scanner hit behaviorally falsified; calibration audit + mistake ledger close the session |

The shape to notice: no phase is skipped when time is short — the budgets
shrink instead. A one-hour engagement is the same machine with a 6-record
fact table, one enum source, three hypotheses, and one card; the gates are
identical, which is what makes small engagements honest and large ones
survivable.
