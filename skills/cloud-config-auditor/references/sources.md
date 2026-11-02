# sources.md — verified lineage sources for cloud-config-auditor (v2)

The de la Fuente layer (`checks-as-code.md`) distills the public
Prowler tradition. Verified during this upgrade:

* Toni de la Fuente — Prowler's author/steward (prowler.com;
  github.com/prowler-cloud/prowler; @toniblyx). The checks-as-code
  doctrine — versioned rules with severity/rationale/remediation, open
  cloud security as a posture — is distilled from the project and his
  public writing:
  * "Why We Need the Open Cloud Security Movement" (prowler.com blog,
    Feb 2025)
  * "Prowler's State of Cloud Security Report 2025" (prowler.com blog)
* CIS Benchmarks — cisecurity.org, the benchmark families the local
  check families map onto.
* The organ's own v1 differentials (CORS matrix, bounded storage
  listing, takeover record pairs, hygiene facts) — `cors-matrix.md`,
  `takeover-checks.md` — unchanged; the lineage layer adds check IDs,
  version pinning, benchmark citation, and drift discipline on top.

Correction record: none.
