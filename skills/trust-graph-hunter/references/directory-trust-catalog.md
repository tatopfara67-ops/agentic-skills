# directory-trust-catalog.md — the directory-interior edges, inheritance paths, and the tier gate

Load when the trust audit runs INSIDE an identity directory (Active
Directory or an LDAP-analog estate) — the Sean Metcalf lineage layer
folded in at v1.3.0. The web-edge catalog lives in
`trust-context-catalog.md`; this one answers the directory question:
WHO effectively holds which capability, through which inherited edge,
and at what cost would an attacker standing at any one position reach
the rest. Everything here is READ-ONLY census plus pricing plus
validation: the census queries are standard LDAP reads an
authenticated, in-scope account can issue; the attack techniques
named in the pricing table are PRICED as knowledge (what the edge
costs an adversary), never executed against live targets — execution
belongs to operator-owned lab ground only (hard rule 6).

## 1. The Directory Edge Inventory (template — one FACT record per edge)

```
DIR-EDGE-<k>: <principal> --holds--> <right>
  source(1-8): membership | computer-rights | acl-delegation |
               sidhistory | gpo-rights | user-rights-assignment |
               local-group | share-delegation
  right: <capability named exactly: GenericAll | WriteDACL | WriteOwner |
         GenericWrite | DS-Replication-Get-Changes-All | ...>
  object: <where the right applies — scope named, not implied>
  evidence: <the LDAP read that returned the row (base, filter, attrs)>
  inherited-through: <the chain if the right arrives by nesting, else direct>
```

The eight-source law (from the documented corpus): a principal's
real power is the UNION of (1) group membership, (2) groups granted
rights on computers, (3) delegated AD-object ACLs direct and
indirect, (4) SIDs in SIDHistory, (5) delegated GPO rights, (6) user
rights assignments via GPO/local policy, (7) local group membership,
(8) shared-folder delegation. Membership alone is never the census —
the escalation paths live in the other seven.

## 2. Edge Classes (with the inheritance mechanism each one carries)

| Class | The edge says | Inheritance mechanism |
| --- | --- | --- |
| membership | principal is in group G | nesting; AdminSDHolder-protected admin groups re-assert hourly (SDProp) |
| acl-delegation | principal holds ACE on object | WriteDACL/WriteOwner/GenericAll re-ACL the object → new edges; owner-rights on created objects |
| sidhistory | principal carries foreign SID | cross-domain reach-back; forest-wide when the SID is Enterprise Admins (RID 519) |
| gpo-rights | principal can edit/link a GPO | code execution wherever the GPO lands; the creator keeps modify rights even after the link is re-scoped |
| credential-cache | privileged principal's secret materializes on host H | interactive/RunAs/RDP/service logons leave NTLM hash + tickets in LSASS; ntds.dit copies (backup, IFM, VM snapshot) hold all hashes |
| protocol | service trusts a key K as proof | KRBTGT hash signs any TGT (domain-wide); service-account hash signs any TGS for that service (no DC contact, no PAC validation by default) |

## 3. The Interesting-Principals Table (well-known RIDs — the census seed list)

| RID | Principal | Why it is an edge, not just a group |
| --- | --- | --- |
| 500 | Administrator (and the DC's DSRM account — same RID) | cannot be disabled out of reach; DSRM dirbase logon is a separate door to the same RID-500 power |
| 512 | Domain Admins | admin on EVERY domain-joined computer by default (automatic local-admin membership) |
| 518 / 519 | Schema Admins / Enterprise Admins | 519 exists only in the forest root; forest-wide Administrators membership in every domain |
| 548 / 550 / 551 | Account / Print / Backup Operators | default INTERACTIVE LOGON RIGHTS ON DOMAIN CONTROLLERS — a "lesser" group that still reaches the database |
| 520 | Group Policy Creator Owners | GPO edit rights on created GPOs — code execution at link scope |
| 525 | Protected Users | the mitigation group — its presence/absence is itself a validation row |
| 1102 | DnsAdmins | admin rights to AD DNS; code-load path on a DC running DNS |
| 578 | Hyper-V Administrators | full control of virtual DCs = effective Domain Admin (the clone-the-DC path) |
| krbtgt (RID 502) | the domain Kerberos service account | disabled, never logged-on, password typically never rotated; its hash IS the protocol edge |

Plus the attribute filter that seeds the census in one read:
`AdminCount=1` (every principal SDProp has flagged as privileged).
Any authenticated in-scope account may issue it.

## 4. The Inheritance Path Pricing Matrix (attack paths PRICED, not run)

Each row states what the path costs an adversary standing at
position P, and which signal it emits — priced from the documented
technique corpus (golden/silver tickets, DCSync, Kerberoast, the
credential shuffle, MS14-068, GPP cpassword):

| Path | Precondition (position P) | Contact required | Stealth (signal emitted) |
| --- | --- | --- | --- |
| GPP password read | any authenticated user | read SYSVOL share | none distinctive; `cpassword` XML rows |
| Kerberoast | any authenticated user | TGS-REQ to DC | RC4 (0x17) 4769 events; bursts of distinct SPNs per second |
| MS14-068 forged PAC | any user + an unpatched DC | AS/TGS to DC | detectable exploit packets; patched by KB3011780 (2014) |
| Credential shuffle | local admin on ANY one host | none to DC | local auth logs only (often uncentralized) |
| Silver ticket | one service/computer account hash | NO DC contact, ever | events only on the target server |
| Golden ticket | KRBTGT hash (from DC, DCSync, or any ntds.dit copy) | NO AS-REQ; TGS-REQ only | custom lifetimes; account may not exist; 20-min PAC check window |
| Golden + SIDHistory | KRBTGT hash of ANY domain in forest | as golden | forest-wide EA (RID 519) reach — the child-to-root path |
| DCSync | replication rights (admin, OR delegated Get-Changes[+All]) | DRSUAPI to DC | replication traffic from a non-DC IP — the IDS row |
| ntds.dit exfil | DC logon rights OR backup/IFM/VM access | file access | offline; no DC event at all |

Pricing rules: the cheaper position wins the row (read SYSVOL
before cracking anything; request RC4 tickets before touching
hosts); paths whose precondition is ALREADY an operator position are
reported as validation failures (M8), not attack steps; every price
column is census data, so the report states the price table for the
CLIENT's graph — which edges their adversaries would buy first.

## 5. The Tier-Boundary Validation Checklist (defense rows, mechanical)

Per boundary, pass/fail — the audit statement under assume-breach:

```
TIER: domain=<D> forest=<F>
  admin-logon-restriction : DA/EA denied interactive+RDP logon on
                            workstations/member servers?      pass|fail
  service-pw-length       : every AdminCount=1 service account
                            >= 25 chars (or MSA/gMSA)?        pass|fail
  krbtgt-rotation         : pwdLastSet within policy window?
                            2x-reset law known?               pass|fail
  replication-rights      : Get-Changes[-All] held ONLY by
                            admins + DC machine accounts?     pass|fail
  dc-logon-groups         : Backup/Account/Print Operators
                            membership empty?                 pass|fail
  krbtgt-dated            : KRBTGT pwdLastSet != domain
                            creation date?                    pass|fail
  exchange/virtualization : Exchange Trusted Subsystem, hyperv-
                            admins, vCenter admins counted as
                            tier-0 equivalents?               pass|fail
```

The KRBTGT rotation arithmetic (from the documented corpus): the
account keeps current + previous password, so a breach requires the
DOUBLE reset — maintenance mode (reset once → let replication
converge 12-24 h → reset again) versus breach "double-tap" (twice in
rapid succession; invalidates every live ticket; expect service
restarts). One reset after a compromise is a reported-incomplete
recovery, and that is a finding.

## 6. Detection Signals (the paired row — attack technique ↔ its signal)

| Technique | Signal | The rot caveat |
| --- | --- | --- |
| Kerberoast | 4769 with ticket encryption 0x17 (RC4); baseline ≈ 10-20 TGS/user/day; filter out `$`-suffixed + service accounts → millions become hundreds | NetApp-class and inter-forest RC4 is legitimate — filter, then investigate the burst pattern |
| Golden/silver ticket | event domain-field anomalies on member servers | the original 2015 domain-anomaly indicator was closed by a mimikatz update (2016-01-05) — indicators rot; the method class does not |
| DCSync | DsGetNCChanges RPC from a non-DC IP (the replication allow-list) | price the method, not the tool: Impacket and DSInternals speak the same protocol |
| Password spray | Kerberos pre-auth failures, one password across many accounts (4771/4768 rate shape) | the 2017 detection pattern; 2025 honeypot-account variant still effective |
| Forged ticket use | logon events whose account does not exist / domain field null | durable only while tooling leaves the artifact — version it |

## 7. Chain Archetypes Involving Directory Trust

* **Child-to-root forest escalation.** KRBTGT hash in a child
  domain + SIDHistory with RID 519 → forest compromise (the
  documented "the domain is not the security boundary; the forest
  is").
* **Delegation self-authorship.** GenericAll/WriteDACL on an admin
  object → grant self the membership edge → SDProp re-asserts it
  hourly (persistence).
* **GPO code-execution relay.** GPO edit right → scheduled-task/
  script at link scope → credential-cache edges on every host in
  scope.
* **Virtualization equivalence.** Hypervisor admin ≈ Domain Admin
  whenever a DC is virtual: clone DC offline → full hash set.
* **Cloud-to-on-prem relay.** Entra ID Connect / sync-service
  compromise → on-prem DA (the documented unanticipated attack
  path) — the bridge to cloud-config-auditor.
* **Backup equivalence.** Whoever reads a DC backup or IFM set is
  tier-0 for free — no DC logon required.

## 8. Anti-patterns (MISTAKE records)

* Reading group membership and calling it a privilege census —
  seven of the eight sources are missing (the documented corpus's
  own key point).
* Executing any priced path against live estate — the matrix is
  valuation data for the report; execution is operator-owned lab
  only (hard rule 6).
* A "golden ticket incident" report that recommends ONE KRBTGT
  reset — incomplete by the 2× law; the correction is the finding.
* Detection rows shipped without their rot caveat — an indicator
  named as if permanent is a false guarantee (the mimikatz 2016
  update is the on-record example).
