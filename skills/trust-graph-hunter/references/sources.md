# sources.md — the Kevin Mitnick lineage (verified as a translation) + the Sean Metcalf census (v1.3.0)

What was actually consulted while distilling this organ, per the
assimilation doctrine (public sources, attributed, no fabrication).
The Mitnick record is below; the Metcalf census follows it.

## Primary sources (public record, consulted)

* **Kevin D. Mitnick with William L. Simon, *The Art of Deception*
  (Wiley, 2002).** The trust-exploitation pattern book: context
  fabrication, authority borrowing, reverse social engineering,
  the exploitation of organizational trust assumptions. Consulted
  for the TRUST-MODEL analysis (what signal, believed by whom,
  grants what) — the layer this organ translates to systems.
* **Kevin D. Mitnick with William L. Simon, *The Art of Intrusion*
  (Wiley, 2005).** The technical-companion record — attack
  narratives where context and trust assumptions, not exotic
  exploits, carried the day.
* Public obituary coverage (July 2023) — biographical facts and
  dates (1963–2023).

## Secondary sources (context only)

* *Ghost in the Wires* (2011) — memoir context only.
* Public summaries and course material referencing Mitnick's
  "trust is the weakest layer" thesis — framing confirmation.

## The honest translation (kept on record)

The operator's brief asked for exactly this: the CAPABILITY to
analyze context and trust relationships BETWEEN systems —
exploiting the trust between a third-party API/server and the main
server for elevated access (access-control bypass). This organ
therefore contains NO human-target social engineering whatsoever;
what it distills is the trust-model analysis behind Mitnick's
documented work, applied to machine-context signals. The
translation is labeled as ours, not his.

## What this organ does NOT claim

* No claim that Mitnick performed machine-context trust attacks of
  the shapes catalogued here; the catalog is this organ's own
  operationalization for authorized engagements.
* No proprietary content; the books above are cited as consulted
  sources only.
* No claim of endorsement by his estate or anyone associated.

## Confidence

High for the lineage's documented shape (three widely available
books plus extensive public record). The systems translation is
explicitly labeled as this organ's contribution, per the
assimilation doctrine's honesty rule.

---

# The Sean Metcalf census (v1.3.0 — the directory-interior layer)

The queue's own gate demanded the blog corpus read end to end
before drafting; the census below is what was actually read, with
the honesty classes stated per artifact.

## Primary sources, READ IN FULL

* **ADSecurity.org long-form posts (read in full, text-extracted,
  dates and URLs pinned):**
  * "Attack Methods for Gaining Domain Admin Rights in Active
    Directory" (2016-01-01, ?p=2362) — the attack-path ladder post:
    the assume-breach framing, the five technique families, the
    per-technique mitigations, the CredSSP/pass-the-hash family.
  * "Kerberos & KRBTGT: Active Directory's Domain Kerberos Service
    Account" (2014-11-10, ?p=483) — the KRBTGT mechanics, the KVNO
    attribute, the 2×-reset arithmetic with maintenance vs
    double-tap, the Get-PSADForestKRBTGTInfo script (his own tool,
    github.com/PyroTek3/PowerShell-AD-Recon).
  * "Kerberos Golden Tickets are Now More Golden" (2015, ?p=1640) —
    HIS SIDHistory research, the outreach to Benjamin Delpy, the
    June-28 mimikatz capability, the child-domain-to-forest path,
    "the Active Directory domain is not the security boundary; the
    AD forest is".
  * "How Attackers Use Kerberos Silver Tickets to Exploit Systems"
    (2015, ?p=2011) — the service→ticket reference table (WMI,
    PSRemoting, WinRM, scheduled tasks, CIFS, LDAP/DCSync, RSAT),
    the "more dangerous than golden" assessment with its stated
    reasons, computer-account persistence.
  * "Mimikatz DCSync Usage, Exploitation, and Detection" (2015,
    ?p=1729) — DCSync authored by Benjamin Delpy and Vincent Le
    Toux; the three delegated replication rights; the
    replication-allow-list detection; the "detect the method, not
    the artifact" rule.
  * "Detecting Forged Kerberos Ticket (Golden Ticket & Silver
    Ticket) Use in Active Directory" (2015, ?p=1515) — his ORIGINAL
    golden-ticket detection method, the domain-field anomaly, and
    the honest 2016-01-05 update noting mimikatz closed it — the
    on-record indicator-rot example.
  * "Detecting Kerberoasting Activity" (2017, ?p=3458) — the RC4
    (0x17) 4769 filter heuristic, the 10–20 TGS/user/day baseline,
    the false-positive reduction chain (millions → hundreds), the
    AES 0x12 / DES 0x1-0x3 chart provenance (Ned Pyle/AskDS).
  * "Scanning for Active Directory Privileges & Privileged
    Accounts" (2016, ?p=3658) — the EIGHT-source combined-rights
    model, the interesting-groups RID catalog (Account Operators
    548, Backup Operators 551, Print Operators 550, DnsAdmins
    1102, Hyper-V 578, Domain Admins 512, EA 519, GPCO 520), the
    GPO-creator modify-rights escalation, the PowerView and
    BloodHound credits (harmj0y, Wald0).
  * "Finding Passwords in SYSVOL & Exploiting Group Policy
    Preferences" (?p=2288), "Securing Windows Workstations:
    Developing a Secure Baseline" (?p=3299, updated 2018), and
    "Securing Domain Controllers to Improve Active Directory
    Security" (?p=3377) — the mitigation corpus: the GPO hygiene,
    the DC hardening sections, the admin-tiering reference, the
    workstation baseline (AppLocker/LAPS/NetCease/WDigest/SMBv1).
* **The Black Hat USA 2016 whitepaper** — "Beyond the MCSE: Active
  Directory for the Security Professional" (50 pp, PDF read in
  structure and security-relevant sections): the
  components-with-security-roles framing, the DC-rights group
  table, the DSRM/RID-500 section, the best-practices checklist.
* **The Troopers 2024 deck** — "A Decade of Active Directory
  Attacks: What We've Learned & What's Next" (115 pp, PDF read in
  structure and timeline sections): the attack timeline eras
  ("Baby Steps" 2000–2009 through "The Third Age" 2020–2023), the
  GPP/Responder/Invoke-Mimikatz/golden-ticket first-use dates with
  original credits (Emilien Girauld and Chris Campbell for GPP,
  Laurent Gaffie for Responder, Joe Bialek for Invoke-Mimikatz,
  Duckwall/Delpy for golden tickets), and his own
  accomplishments ledger including "stealth contributor to
  Bloodhound".
* **The Trimarc research ledger** (trimarcsecurity.com/research) —
  the dated first-person record of research firsts 2014–2025,
  including the Exchange permission paths (2019), the Bronze Bit
  CVE-2020-17049 scenarios (2020), the Azure AD Connect attack
  path (2020), and the no-false-positive Kerberoast detection
  (2017).
* **The ADSecurity.org About page** — the verified bio: Microsoft
  Certified Master (MCM)/MCSM Directory Services (~100 worldwide),
  55 talks at 27 conferences, Trimarc founder/CTO (previously
  TrustedSec), 1 of 3 thanked in the CISA Director's 2021 BlackHat
  keynote for SolarWinds help.
* **The Presentations page** (?page_id=1352) — the talk record
  inventory: Black Hat USA (2015/2016/2018/2019), DEF CON
  (2015–2020, 2024), DerbyCon (2015–2019), Troopers, BlueHat
  2017, the BSides family.

## BOUNDED, not line-read (stated honestly)

* The remaining ~30 ADSecurity.org posts outside the method-bearing
  core (the AD Fundamentals 2026 permissions series, the Entra ID
  posts, the PowerShell encoding reference) — inventoried via the
  site index and Popular Posts list, not read in full.
* The talk VIDEOS (YouTube) and the remaining slide PDFs — inventoried
  via the Presentations page, not watched.
* The Mimikatz Guide and Command Reference page — known, cited by the
  technique posts, not line-read.
* Tool source trees (mimikatz, PowerSploit/PowerView, BloodHound,
  Impacket, kerberoast) — their capabilities are cited from
  Metcalf's documentation of them, not from reading their source.

## The attribution ledger (the correction record)

Every technique in the pricing matrix is credited to its documented
author, per the corpus's own reference sections:

* Golden tickets — the method presented by Skip Duckwall & Benjamin
  Delpy (Black Hat USA 2014, "Abusing Microsoft Kerberos: Sorry You
  Guys Don't Get It"); the SIDHistory/explicit-EA expansion is
  Metcalf's research with Delpy's implementation (2015).
* Silver tickets — alluded to in the Duckwall/Delpy presentation,
  partly discussed in Tim Medin's DerbyCon 2014 talk; the service
  table and persistence treatment are Metcalf's.
* DCSync — written by Benjamin Delpy and Vincent Le Toux (mimikatz,
  2015); the rights documentation and detection guidance are
  Metcalf's.
* Kerberoast — Tim Medin (DerbyCon 2014, "Attacking Microsoft
  Kerberos: Kicking the Guard Dog of Hades"), tool released there.
* MS14-068 — first public exploit PyKEK by Sylvain Monné (@BiDOrD);
  Kekeo's improved variant by Benjamin Delpy.
* GPP cpassword — the published-key discovery credited to Emilien
  Girauld and Chris Campbell (per the Troopers 2024 timeline).
* PowerView — Will Schroeder (@harmj0y); BloodHound's ACL attack
  paths — Will Schroeder and Andy Robbins (@_wald0); Metcalf is a
  documented "stealth contributor" to BloodHound.
* The admin-tiering model — Microsoft's securing-privileged-access
  reference material (Metcalf's corpus points to it; the tier
  VALIDATION discipline is his operationalization).

## The psych-read (documented behavior, lens lines on record)

* L1 heuristics — mechanism-before-technique (the auth-flow preamble
  opens every attack post); attack+mitigation+detection as the
  record shape; name-the-preconditions before the exploit; inline
  attribution of every tool author. ≥ 4 independent artifacts each.
* L2 obsession — where privilege ACTUALLY lives (the union of
  sources), mapped across 2014–2026 (KRBTGT → tickets → DCSync →
  rights scanning → cloud identity), with detection parity as the
  second arc (every documented attack got a documented signal).
* L3 aesthetics — quoted and checked against what was built: "the
  domain is not the security boundary; the AD forest is" (backed by
  the SIDHistory demonstration); "silver tickets can be more
  dangerous than golden" (backed by the service table and the
  stated reasons: cheaper hash, no DC contact, harder detection);
  "assume breach" (backed by the technique framing).
* L4 failure handling — the 2016-01-05 update note documenting that
  mimikatz closed his 2015 golden-ticket indicator, kept visible in
  the post; the SID-filtering mitigation uncertainty stated with
  three named reasons; the "99.99% of the time" generalization
  asterisked rather than absolutized.
* L5 cadence — research → coordinated disclosure with tool release
  → conference talk → long-form post, measured in weeks (SIDHistory:
  Delpy outreach June 2015 → mimikatz June 28 → Black Hat August →
  post September); reference posts maintained across years.

## OPINION quarantine (on record, not fed to distillation)

```
OPINION figure=Sean Metcalf lens=cross reading="the 'Godfather of
  Active Directory security' framing" artifact=THIRD-PARTY press
  framing (the About page quotes it as what others call him)
  status=admitted-as-press-record-only next=his own artifacts never
  claim the title; it is cited as reception, not method
OPINION figure=Sean Metcalf lens=L5 reading="podcast co-host persona
  as teaching style" artifact=NONE status=quarantined next=no
  method-bearing artifact depends on it; the Enterprise Security
  Weekly record is context only
```

## What the v1.3.0 layer does NOT claim

* No claim that Metcalf endorses this organ or its operationalization;
  his corpus is cited as the consulted public record.
* No claim that the priced-path matrix is his artifact — his corpus
  prices techniques per-post; the ASSEMBLY into one matrix (M7) is
  this organ's upgrade, stated as such (W6).
* No technique is included beyond what his documented corpus
  describes publicly; the organ adds the census/pricing/validation
  protocol, not new attack capability.
