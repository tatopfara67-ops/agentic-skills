# side-door-catalog.md — the misconfig classes and dork grammar

Load during the passive sweep (step 2b) and candidate triage. One
query per class per stage; the response — not the snippet —
confirms.

## 1. Misconfig Classes (the hunt list)

| Class | Signature (passive index) | One-probe verification | Route to |
| --- | --- | --- | --- |
| exposed admin panel | dork: login pages on odd ports/subdomains | existence probe returns panel | report exposure |
| open directory listing | dork: `intitle:"index of"` + scope terms | one GET, listing confirmed | content-discovery |
| backup archive | dork/wordlist: `.bak .zip .sql .tar.gz` shapes | one HEAD/GET | content-discovery triage |
| exposed config file | `.env http` / `config.php.bak` shapes | one GET, mask secrets | secrets policy |
| staging/dev host | hostname patterns from CT logs (`stg dev test uat qa`) | one GET, banner diff vs prod | dossier backlog |
| dangling DNS delegation | CT/DNS: NS/CNAME to expired service | one resolve + one GET | subdomain-hunter takeover |
| anonymous storage | bucket shapes on public namespace | cloud-config-auditor bounded check | its own organ |
| verbose error index | dork: error strings + scope domain | one GET to the cited path | report information disclosure |
| forgotten internal service | port fingerprints from passive indexes (where rules permit) | one GET banner | report exposure intel |
| old branding/codename | archives, press, job posts | hostname resolve | dossier backlog |

## 2. Dork Grammar (one query per class)

Shapes only — operators adapt terms to the target's nouns:

```
site:<scope> intitle:"index of" (backup|db|dump)
site:<scope> inurl:(admin|panel|dashboard) -inurl:logout
site:<scope> ext:(env|bak|sql|ini|old)
site:stg.<scope> OR site:dev.<scope> OR site:test.<scope>
"<target brand>" "internal use only" OR "confidential"
site:github.com "<scope>" (password|secret|token)   # public code hosts
```

Rules: one query per class per stage; no query pagination beyond
page one (park the rest); every hit's source URL is cited in the
backlog entry. Queries run against the search engine, not the
target — the target sees nothing.

## 3. Candidate Triage Record (template)

```
CAND-<k>: <host/path>
  class: <misconfig class>
  index source: <dork/CT/archive citation>     # the passive evidence
  scope verdict: in_scope | recon_only | out_of-scope(intel only)
  probe: R-NNN (exactly one) -> exposure class CONFIRMED | dead lead
  next: dossier_add(backlog) | takeover pair | report line
```

## 4. Attribution Hygiene (posture rules)

* Rate floors per stage; never parallel-burst index queries.
* Egress only from operator-approved addresses/proxies where program
  rules require it; the ledger records which stage ran from where.
* A WAF reset or block on the ONE verification probe is recorded as
  an engagement fact (REFUSED/blocked note) and the candidate is
  parked — volume escalation is forbidden (hard rule 2).
* The main application's request count is an exit-gate metric:
  this organ's ideal engagement shows zero main-app requests.

## 5. What this catalog deliberately omits

* Active exploitation of any discovered side door (hard rule 4).
* Default-credential testing without an explicit operator
  instruction on record.
* Any technique that touches third-party infrastructure outside
  the program's scope declaration.
