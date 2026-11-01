"""skill-mythos backends — the charter, and the classifier pair (CVSS + VRT).

Three tools, one doctrine: a finding that leaves this arsenal must be
triage-grade — zero false positive (differential triad), fully reproducible
(n_runs), and precisely classified (CVSS 3.1 vector + recomputed base score,
Bugcrowd VRT category with P-rating, HackerOne severity crosswalk).

  mythos_charter()      the activation payload: twelve articles, the bundle
                        map with install status, the quality gates
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

from .. import cvss as _cvss
from .. import paths

# --------------------------------------------------------------- the charter

MODULE = "skill-mythos"
MODULE_VERSION = "1.0.0"

SPINE = "mythos-bug-hunter"

TIERS = {
    "0-master": [MODULE],
    "1-recon-mapping": ["surface-cartographer", "subdomain-hunter",
                        "content-discovery", "js-recon", "api-surface-mapper"],
    "2-access-logic": ["auth-boundary-mapper", "oauth-flow-auditor",
                       "business-logic-hunter"],
    "3-deep-technical": ["injection-lab", "ssrf-playbook", "xss-playbook",
                         "cloud-config-auditor"],
    "4-incident": ["adversary-tracker"],
}

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

REPORTING_TOOLS = {
    "cvss3_score": "spec-exact CVSS v3.1 base score from a vector",
    "vrt_classify": "finding-class -> Bugcrowd VRT + P-rating + H1 "
                    "severity + CVSS template",
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

    Returns the twelve charter articles, the bundle map with per-skill
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
        "charter_reference": "skills/skill-mythos/SKILL.md",
    }


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
