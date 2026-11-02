"""skill-mythos tests — charter, doctrine forge, CVSS engine, VRT classifier.

Covers: the thirteen-article activation payload, the doctrine_forge
prompt-escalation engine (intent grammar, severity/quota extraction,
persona mixes, determinism), spec-exact CVSS 3.1 base scoring (including
the FIRST published example scores), VRT classification against the
shipped official taxonomy (variant selection, HackerOne crosswalk,
template shaping), and the hardened auditor gates (cvss recomputation,
vrt validation, reproduction reference, incident-handoff exemption).
"""
import importlib.util
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

from arsenal import cvss as _cvss  # noqa: E402
from arsenal.tools import mythos as _mythos  # noqa: E402

_TREE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
_AUDITOR_PATH = os.path.join(_TREE_ROOT, "auditor", "audit_report.py")


def _auditor():
    spec = importlib.util.spec_from_file_location("mythos_audit_report",
                                                  _AUDITOR_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------ CVSS v3.1

class TestCvssEngine(unittest.TestCase):
    SPEC_VECTORS = [
        # published CVSS v3.1 example scores (FIRST calculator)
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", 9.8),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H", 10.0),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N", 6.1),
        ("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N", 6.5),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N", 5.3),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N", 7.5),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N", 0.0),
        ("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H", 9.9),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N", 8.6),
    ]

    def test_spec_example_scores(self):
        for vector, expected in self.SPEC_VECTORS:
            got = _cvss.base_score(vector)
            self.assertEqual(got["score"], expected, vector)
            self.assertEqual(got["vector"],
                             vector if vector.startswith("CVSS:")
                             else "CVSS:3.1/" + vector)

    def test_bare_vector_and_prefixes(self):
        for prefix in ("CVSS:3.1/", "CVSS:3.0/", ""):
            vec = prefix + "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
            self.assertEqual(_cvss.base_score(vec)["score"], 9.8, vec)

    def test_severity_bands(self):
        cases = [(0.0, "None"), (3.9, "Low"), (4.0, "Medium"),
                 (6.9, "Medium"), (7.0, "High"), (8.9, "High"),
                 (9.0, "Critical"), (10.0, "Critical")]
        for score, band in cases:
            self.assertEqual(_cvss.severity_band(score), band, score)

    def test_pr_weight_depends_on_scope(self):
        # same PR:L and same impact metrics; only Scope changes, and the
        # PR weight relaxes (0.62 -> 0.68, spec table 7): 8.8 -> 9.9
        u = _cvss.base_score("AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H")
        c = _cvss.base_score("AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H")
        self.assertEqual(u["score"], 8.8)
        self.assertEqual(c["score"], 9.9)

    def test_rejects_broken_vectors(self):
        bad = [
            "",                                  # empty
            "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H",   # missing A
            "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:X",  # bad value
            "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/A:H",  # duplicate
            "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/XX:N",  # unknown metric
            "CVSS:2.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",  # old version
        ]
        for vector in bad:
            with self.assertRaises(ValueError, msg=vector):
                _cvss.parse_vector(vector)

    def test_error_messages_stay_instructive(self):
        with self.assertRaises(ValueError) as cm:
            _cvss.parse_vector("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H")
        self.assertIn("missing metric(s): A", str(cm.exception))


# ------------------------------------------------------------- charter

class TestMythosCharter(unittest.TestCase):
    def setUp(self):
        self.charter = _mythos.mythos_charter()

    def test_thirteen_articles(self):
        self.assertEqual(len(self.charter["articles"]), 13)
        for article in self.charter["articles"]:
            self.assertRegex(article, r"^A\d+ ")
        self.assertIn("CVSS 3.1", "".join(self.charter["articles"]))
        self.assertTrue(self.charter["articles"][-1].startswith("A13"))

    def test_charter_carries_prompt_escalation(self):
        escalation = self.charter["prompt_escalation"]
        self.assertEqual(escalation["tool"], "doctrine_forge")
        self.assertIn("A13", escalation["rule"])

    def test_tier_registry_lists_all_organs(self):
        tiers = self.charter["tiers"]
        self.assertEqual(sum(len(v) for v in tiers.values()), 27)
        self.assertEqual(tiers["0-engine"], {"glm-self-model": True})
        self.assertEqual(tiers["0-master"], {"skill-mythos": True})
        self.assertEqual(sorted(tiers["5-craft"]), [
            "feedback-fuzzer", "module-smith", "packet-orchestrator",
            "pipeline-smith", "scan-economist", "template-scanner"])
        self.assertEqual(sorted(tiers["6-legend"]), [
            "chain-architect", "deep-teardown", "desync-hunter",
            "ghost-crawler", "signal-smith", "trust-graph-hunter"])
        for tier, skills in tiers.items():
            for name, installed in skills.items():
                self.assertTrue(installed, "%s missing in tier %s"
                                % (name, tier))

    def test_reporting_tools_routing(self):
        self.assertIn("cvss3_score", self.charter["reporting_tools"])
        self.assertIn("vrt_classify", self.charter["reporting_tools"])
        self.assertIn("mythos_lineages", self.charter["reporting_tools"])

    def test_quality_gates_name_the_instruments(self):
        gates = " ".join(self.charter["quality_gates"])
        for token in ("differential triad", "CVSS 3.1", "VRT",
                      "HackerOne", "reproduction", "impact-chain"):
            self.assertIn(token, gates)


class TestMythosLineages(unittest.TestCase):
    def test_registry_lists_twenty_lineages_all_installed(self):
        registry = _mythos.mythos_lineages()
        self.assertEqual(registry["count"], 20)
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        for organ in ("adversary-tracker", "scan-economist", "module-smith",
                      "pipeline-smith", "feedback-fuzzer",
                      "template-scanner", "packet-orchestrator",
                      "chain-architect", "desync-hunter", "deep-teardown",
                      "ghost-crawler", "auth-boundary-mapper",
                      "signal-smith", "trust-graph-hunter",
                      "subdomain-hunter", "xss-playbook",
                      "oauth-flow-auditor", "content-discovery",
                      "business-logic-hunter", "cloud-config-auditor"):
            self.assertIn(organ, by_organ)
            self.assertTrue(by_organ[organ]["installed"], organ)
            for field in ("figure", "distillation", "sources"):
                self.assertTrue(by_organ[organ][field], "%s lacks %s"
                                % (organ, field))

    def test_lineage_figures_are_the_verified_names(self):
        registry = _mythos.mythos_lineages()
        joined = " ".join(e["figure"] for e in registry["lineages"])
        for name in ("Shimomura", "Gordon Lyon", "HD Moore", "Tom Hudson",
                     "Zalewski", "Sandeep Singh", "Nizamul Rana",
                     "Justin Searle", "PhonePe", "Orange Tsai",
                     "James Kettle", "George Hotz", "Adrian Lamo",
                     "Frans Rosen", "John Draper", "Kevin Mitnick",
                     "EdOverflow", "Heiderich", "Parecki", "Miessler",
                     "Dalili", "de la Fuente"):
            self.assertIn(name, joined, name)
        # the unverified attributions from the operator brief stay out
        self.assertNotIn("Skappen", joined)
        self.assertNotIn("Franz Rosen", joined)  # misspelling stays out

    def test_attribution_corrections_are_on_record(self):
        registry = _mythos.mythos_lineages()
        corrections = {e["organ"]: e["correction"] for e in
                       registry["lineages"]}
        self.assertIsNone(corrections["scan-economist"])
        self.assertIn("Nizamul Rana", corrections["template-scanner"])
        self.assertIn("PhonePe", corrections["packet-orchestrator"])
        self.assertIn("Skappen", corrections["packet-orchestrator"])
        self.assertIn("Frans Rosen", corrections["auth-boundary-mapper"])
        self.assertIn("unauthorized", corrections["ghost-crawler"])
        self.assertIn("translation", corrections["trust-graph-hunter"])

    def test_second_wave_lineage_organs_are_v2(self):
        """The six v2.0.0 organs carry the lineage in frontmatter, not
        just in the registry — the SKILL.md metadata and the registry
        entry must agree."""
        registry = _mythos.mythos_lineages()
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        skills_root = os.path.join(_TREE_ROOT, "skills")
        for organ in ("subdomain-hunter", "xss-playbook",
                      "oauth-flow-auditor", "content-discovery",
                      "business-logic-hunter", "cloud-config-auditor"):
            path = os.path.join(skills_root, organ, "SKILL.md")
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            self.assertIn("version: 2.0.0", text, organ)
            self.assertIn("lineage:", text, organ)
            figure = by_organ[organ]["figure"]
            surname = figure.split("(")[0].split("—")[0].strip()
            self.assertIn(surname, text,
                          "%s: figure %r not in SKILL.md lineage"
                          % (organ, surname))


# --------------------------------------------------------- vrt_classify

class TestVrtClassify(unittest.TestCase):
    def test_ssrf_variants(self):
        hot = _mythos.vrt_classify("ssrf", internal=True, sensitive=True)
        self.assertEqual(hot["vrt_id"],
                         "server_security_misconfiguration."
                         "server_side_request_forgery_ssrf."
                         "internal_secrets_exposure")
        self.assertEqual(hot["p"], 2)
        self.assertEqual(hot["hackerone_severity"], "High")
        cold = _mythos.vrt_classify("ssrf", internal=False)
        self.assertTrue(cold["vrt_id"].endswith("external_low_impact"))
        self.assertEqual(cold["p"], 5)
        self.assertEqual(cold["cvss_template"]["base_score"], 0.0)

    def test_idor_variants(self):
        read = _mythos.vrt_classify("idor", sensitive=True)
        self.assertTrue(read["vrt_id"].endswith(
            "view_sensitive_information_iterable_object_identifiers"))
        self.assertEqual(read["p"], 3)
        write = _mythos.vrt_classify("idor", sensitive=True,
                                     scope_changed=True)
        self.assertTrue(write["vrt_id"].endswith(
            "modify_view_sensitive_information_iterable_object_identifiers"))
        self.assertEqual(write["p"], 1)
        trivial = _mythos.vrt_classify("idor", sensitive=False)
        self.assertEqual(trivial["p"], 5)
        self.assertEqual(trivial["cvss_template"]["base_score"], 5.3)

    def test_xss_variants(self):
        refl = _mythos.vrt_classify("xss_reflected")
        self.assertEqual(refl["p"], 3)
        self.assertEqual(refl["cvss_template"]["base_score"], 6.1)
        self_xss = _mythos.vrt_classify("xss_reflected", self_only=True)
        self.assertEqual(self_xss["p"], 5)
        stored = _mythos.vrt_classify("xss_stored")
        self.assertEqual(stored["p"], 2)

    def test_fixed_priority_classes(self):
        self.assertEqual(_mythos.vrt_classify("auth_bypass")["p"], 1)
        self.assertEqual(_mythos.vrt_classify("auth_bypass")
                         ["hackerone_severity"], "Critical")
        self.assertEqual(_mythos.vrt_classify("exposed_debug_portal")["p"], 3)
        admin = _mythos.vrt_classify("exposed_debug_portal", admin=True)
        self.assertEqual(admin["p"], 1)

    def test_all_mapped_vrt_ids_resolve_in_shipped_taxonomy(self):
        for klass in _mythos.FINDING_CLASSES:
            result = _mythos.vrt_classify(klass)
            self.assertTrue(result["taxonomy_resolved"],
                            "%s -> %s not in shipped taxonomy"
                            % (klass, result["vrt_id"]))

    def test_varies_classes_flag_context(self):
        ssti = _mythos.vrt_classify("ssti")
        self.assertIsNone(ssti["p"])
        self.assertIn("Varies", ssti["priority"])
        self.assertIn("context", " ".join(ssti["notes"]))

    def test_context_flags_shape_cvss_template(self):
        authed = _mythos.vrt_classify("idor", authenticated=True)
        self.assertIn("PR:L", authed["cvss_template"]["vector"])
        self.assertEqual(authed["cvss_template"]["base_score"], 6.5)

    def test_unknown_class_raises_with_supported_list(self):
        with self.assertRaises(ValueError) as cm:
            _mythos.vrt_classify("time_travel")
        self.assertIn("supported classes", str(cm.exception))
        self.assertIn("sql_injection", str(cm.exception))

    def test_class_name_normalization(self):
        quiet = _mythos.vrt_classify("SQL Injection")
        self.assertEqual(quiet["vrt_id"],
                         _mythos.vrt_classify("sql_injection")["vrt_id"])


# ------------------------------------------------------ auditor gates

_GOOD = """# Report

### H-001 — Unauthenticated debug route (facts R-001)

- claim: unauthenticated read of diagnostic state (R-001)
- Closure: CONFIRMED (E-001: R-003; closure R-004)
- severity: low (records R-001, R-003)
- impact-chain: one bounded read of the banner (R-003)
- canary attestation: self-owned lab only (AUTH R-000)
- cvss: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N = 5.3 (records R-001)
- vrt: server_security_misconfiguration.exposed_portal.non_admin_portal [P3] (records R-001)
- reproduction: E-001 — GET /debug, n_runs 3

### E-001 — differential probe

- baseline: R-002 (401, 3/3)
- n_runs: 3
"""


class TestReportGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit_mod = _auditor()

    def _audit_text(self, text):
        fd, path = tempfile.mkstemp(suffix=".md")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        try:
            return self.audit_mod.audit(path)
        finally:
            os.unlink(path)

    def _fails(self, text):
        return [msg for status, msg in self._audit_text(text)
                if status == "FAIL"]

    def test_good_report_passes_classification_gates(self):
        results = self._audit_text(_GOOD)
        self.assertEqual([m for s, m in results if s == "FAIL"], [])
        self.assertIn("H-001 CONFIRMED finding carries the full "
                      "classification set",
                      " ".join(m for _s, m in results))

    def test_missing_cvss_line_fails(self):
        fails = self._fails(_GOOD.replace(
            "- cvss: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N = 5.3 "
            "(records R-001)\n", ""))
        self.assertTrue(any("cvss" in m and "lacks" in m or "no cvss" in m
                            for m in fails), fails)

    def test_score_mismatch_fails_with_recomputed_value(self):
        bad = _GOOD.replace("= 5.3", "= 7.5")
        fails = self._fails(bad)
        self.assertTrue(any("cvss score mismatch" in m and "5.3" in m
                            for m in fails), fails)

    def test_bogus_vrt_category_fails(self):
        bad = _GOOD.replace(
            "server_security_misconfiguration.exposed_portal."
            "non_admin_portal", "totally.made_up.category")
        fails = self._fails(bad)
        self.assertTrue(any("not found in the shipped taxonomy" in m
                            for m in fails), fails)

    def test_vrt_without_p_rating_fails(self):
        bad = _GOOD.replace("[P3]", "baseline")
        fails = self._fails(bad)
        self.assertTrue(any("no P-rating" in m for m in fails), fails)

    def test_missing_reproduction_fails(self):
        # the E-001 id in the Closure line itself counts as the
        # reproduction reference — remove BOTH to prove the gate bites
        bad = _GOOD.replace(
            "- reproduction: E-001 — GET /debug, n_runs 3\n", "")
        bad = bad.replace("Closure: CONFIRMED (E-001: R-003; closure R-004)",
                          "Closure: CONFIRMED (R-003; closure R-004)")
        fails = self._fails(bad)
        self.assertTrue(any("reproduction reference" in m for m in fails),
                        fails)

    def test_incident_handoff_risk_line_skips_classification_gates(self):
        handoff = """# Adversary handoff

### H-004 compromised container

Risk: high — unauthorized actor with valid credentials — R-009
- Closure: CONFIRMED — R-008, R-009
- impact-chain: login anomaly to confirmed access (R-001, R-008)
- canary: none during the trace — TIP-OFF discipline held (R-003)
"""
        fails = self._fails(handoff)
        self.assertEqual(fails, [], fails)

    def test_summary_sections_do_not_leak_into_blocks(self):
        # a severity line under a ## section after the finding block must
        # NOT arm the classification gates for that block (strict blocks)
        sneaky = _GOOD + """## Impact

- severity: low (records R-001) — summary restating
"""
        fails = self._fails(sneaky)
        self.assertEqual(fails, [], fails)


if __name__ == "__main__":
    unittest.main()
