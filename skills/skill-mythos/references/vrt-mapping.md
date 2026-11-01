# vrt-mapping.md — Bugcrowd VRT and the HackerOne crosswalk

Load when classifying a finding for submission. The instrument is
`vrt_classify(finding_class, …flags)`; this module teaches you to
argue with its output — and when you must.

## 1. What the VRT is

The Bugcrowd Vulnerability Rating Taxonomy is a three-level hierarchy:

```
Category            e.g. server_security_misconfiguration
  Sub-Category      e.g. exposed_portal
    Variant         e.g. non_admin_portal   [P3]
```

* P1 Critical / P2 High / P3 Medium / P4 Low / P5 Informational.
* Some nodes are marked **Varies** — the priority legitimately depends
  on context (that is not a bug in the taxonomy; it is the taxonomy
  telling you to argue).
* IDs are stable lowercase dotted paths
  (`broken_access_control.idor.view_sensitive_information_iterable_object_identifiers`)
  — copy them exactly; a near-miss id fails the auditor.

The shipped snapshot lives at `references/vrt-taxonomy.json`
(Apache-2.0, see NOTICE.md; release date inside its metadata). The
live taxonomy at bugcrowd.com/vrt is the submission-time authority —
cross-check the node before filing, because programs override and the
taxonomy moves.

## 2. How `vrt_classify` decides

You pass a finding class plus the flags you OBSERVED:

| Flag | Effect |
| --- | --- |
| authenticated | CVSS template PR:L |
| user_interaction | CVSS template UI:R |
| scope_changed | CVSS template S:C |
| internal | SSRF/secrets variant selection |
| sensitive | IDOR/XSS/secrets/clickjacking variant selection |
| admin | stored-XSS / exposed-portal variant selection |
| self_only | self-XSS / non-sensitive-IDOR variants |

The tool resolves your class + flags to a taxonomy node, prefers the
taxonomy's own priority over the built-in default when they differ,
tells you when the node is Varies, and hands back a CVSS template for
your context. Treat its answer as a strong prior, not a verdict —
the tool never saw the response bodies; you did.

## 3. The mapping table (supported classes)

| finding_class | VRT node | Baseline |
| --- | --- | --- |
| rce / command_injection | server_side_injection.remote_code_execution_rce | P1 |
| sql_injection | server_side_injection.sql_injection | P1 |
| xxe | server_side_injection.xml_external_entity_injection_xxe | P1 |
| lfi | server_side_injection.file_inclusion.local | P1 |
| ssti | server_side_injection.ssti | Varies (basic P4 → custom chains) |
| ssrf | server_security_misconfiguration.server_side_request_forgery_ssrf.{internal_secrets_exposure P2, internal_data_exposure P3, external_low_impact P5} | variants |
| xss_reflected | cross_site_scripting_xss.reflected.{non_self P3, self P5} | variants |
| xss_stored | cross_site_scripting_xss.stored.{non_admin_to_anyone P2, privileged_user_to_privilege_elevation P3, self P5} | variants |
| idor | broken_access_control.idor.{view_sensitive P3, view+modify P1, guid P4, non_sensitive P5} | variants |
| auth_bypass | broken_authentication_and_session_management.authentication_bypass | P1 |
| session_fixation | …session_fixation.{remote P3, local P5} | variants |
| session_invalid_persist | …failure_to_invalidate_session.{on_logout P4, on_password_change P4, others P5} | variants |
| open_redirect | unvalidated_redirects_and_forwards.open_redirect.get_based | P4 |
| csrf | cross_site_request_forgery_csrf.{application_wide P2, action_specific Varies} | variants |
| exposed_debug_portal | server_security_misconfiguration.exposed_portal.{admin_portal P1, non_admin_portal P3, protected P5} | variants |
| verbose_error | sensitive_data_exposure.visible_detailed_error_page.{descriptive_stack_trace P5, detailed_server_configuration P4} | variants |
| internal_ip_disclosure | sensitive_data_exposure.internal_ip_disclosure | P5 |
| graphql_introspection | sensitive_data_exposure.graphql_introspection_enabled | P5 |
| secrets_exposure | sensitive_data_exposure.disclosure_of_secrets.{for_publicly_accessible_asset P1, for_internal_asset P3, sample_or_invalid P5} | variants |
| jwt_disclosure | …disclosure_of_secrets.sensitive_information_disclosed_jwt | P5 |
| subdomain_takeover | server_security_misconfiguration.misconfigured_dns.subdomain_takeover | P3 |
| default_credentials | server_security_misconfiguration.using_default_credentials | P1 |
| race_condition | server_security_misconfiguration.race_condition | Varies |
| path_traversal | server_security_misconfiguration.path_traversal | Varies |
| cors_misconfiguration | server_security_misconfiguration.unsafe_cross_origin_resource_sharing | Varies |
| clickjacking | server_security_misconfiguration.clickjacking.{sensitive_action P4, non_sensitive_action P5} | variants |
| rate_limit_bypass | server_security_misconfiguration.no_rate_limiting_on_form.{login P4, registration P4, change_password P5} | variants |
| oauth_account_takeover | server_security_misconfiguration.oauth_misconfiguration.account_takeover | P2 |
| two_fa_bypass | broken_authentication_and_session_management.two_fa_bypass | P3 |
| username_enumeration | broken_access_control.username_enumeration.non_brute_force | P4 |
| directory_listing | server_security_misconfiguration.directory_listing_enabled.{non_sensitive P5, sensitive Varies} | variants |
| request_smuggling | server_security_misconfiguration.request_smuggling | Varies |
| ai_prompt_injection | ai_application_security.prompt_injection.system_prompt_leakage | P2 |
| ai_output_xss | ai_application_security.improper_output_handling.cross_site_scripting_xss | P3 |
| ai_key_leak | ai_application_security.sensitive_information_disclosure.key_leak | P1 |
| xssi | sensitive_data_exposure.xssi | Varies |

(Names abbreviated with `…` where the parent repeats; the tool and
`vrt-taxonomy.json` carry the exact full paths.)

## 4. The HackerOne crosswalk

HackerOne does not grade by the VRT; its severity scale maps cleanly:

| VRT | HackerOne |
| --- | --- |
| P1 | Critical |
| P2 | High |
| P3 | Medium |
| P4 | Low |
| P5 | None / Informational |

State both in the report block — the VRT id for Bugcrowd-style
programs, the crosswalked severity for HackerOne-style programs, and
the argued program-context call on the `severity:` line either way.

## 5. Arguing a variant (the discipline)

1. Classify with the flags you observed — not the flags that pay
   better.
2. Read the sibling variants of your node; name why yours fits and
   the neighbors do not (the vrt: line carries this argument).
3. If the node is Varies, the demonstrated impact — from your ledger
   records — sets the P; say so explicitly.
4. Program briefs override taxonomies: when the program's scope page
   says "X is out of scope / rated lower here", the program wins and
   your report says that it did.
5. Cross-check the live taxonomy (bugcrowd.com/vrt) before filing.
