"""doctrine_forge tests — the A13 prompt-escalation engine.

Covers: the operator's own example phrasings (Indonesian continue and
quota orders), intent detection for every grammar class, severity and
quota extraction, persona-mix integrity (every referenced organ really
ships), the gates riding along on every forged order, quota discipline
(never a severity mandate), verbatim preservation of the original
request, and determinism (A4: same request, same order, character for
character).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

from arsenal.tools import mythos as _mythos  # noqa: E402


class TestIntentDetection(unittest.TestCase):
    def test_operator_example_continue(self):
        forged = _mythos.doctrine_forge(
            "tolong lanjutkan pekerjaan bug bounty yang tertunda")
        self.assertEqual(forged["detected_intent"], "continue_pending")

    def test_operator_example_quota(self):
        forged = _mythos.doctrine_forge(
            "tolong kerjakan dengan methode dan skill yang sudah tertanam, "
            "dapatkan minimal 3 bug high-medium")
        self.assertEqual(forged["detected_intent"], "bug_quota")
        self.assertEqual(forged["quota"], 3)
        self.assertEqual(forged["severity_goal"], "high-medium")

    def test_quota_english(self):
        forged = _mythos.doctrine_forge(
            "get me at least 5 bugs, critical or high")
        self.assertEqual(forged["detected_intent"], "bug_quota")
        self.assertEqual(forged["quota"], 5)
        self.assertEqual(forged["severity_goal"], "critical-high")

    def test_quota_count_after_noun(self):
        forged = _mythos.doctrine_forge("cari 2 temuan bug")
        self.assertEqual(forged["quota"], 2)

    def test_continue_beats_quota_keywords(self):
        # 'bug bounty' present, but the continuation verb wins
        forged = _mythos.doctrine_forge(
            "please continue the bug bounty work, it is pending")
        self.assertEqual(forged["detected_intent"], "continue_pending")

    def test_incident(self):
        forged = _mythos.doctrine_forge(
            "we might be breached — adversary activity detected tonight")
        self.assertEqual(forged["detected_intent"], "incident_response")

    def test_classify(self):
        forged = _mythos.doctrine_forge(
            "classify the findings and write the report with CVSS")
        self.assertEqual(forged["detected_intent"], "classify_report")

    def test_surface_recon(self):
        forged = _mythos.doctrine_forge(
            "map the target surface and enumerate subdomains")
        self.assertEqual(forged["detected_intent"], "surface_recon")

    def test_ai_surface(self):
        forged = _mythos.doctrine_forge(
            "uji prompt injection di target AI ini sampai dapat 1 celah high")
        self.assertEqual(forged["detected_intent"], "ai_surface")
        self.assertEqual(forged["quota"], 1)
        self.assertEqual(forged["severity_goal"], "high")

    def test_ai_surface_english(self):
        forged = _mythos.doctrine_forge(
            "test the chatbot for prompt injection until data leaves")
        self.assertEqual(forged["detected_intent"], "ai_surface")

    def test_default_fallback(self):
        forged = _mythos.doctrine_forge("hello there, good morning")
        self.assertEqual(forged["detected_intent"], "default")
        # the fallback is still a full professional order
        self.assertIn("mythos_charter", forged["doctrine_prompt"])

    def test_empty_request_is_safe(self):
        forged = _mythos.doctrine_forge("   ")
        self.assertEqual(forged["detected_intent"], "default")
        self.assertEqual(forged["operator_request"], "")


class TestForgedOrderContent(unittest.TestCase):
    def setUp(self):
        self.quota_order = _mythos.doctrine_forge(
            "dapatkan minimal 3 bug high-medium")

    def test_quota_order_names_all_seven_legends(self):
        prompt = self.quota_order["doctrine_prompt"]
        for name in ("Orange Tsai", "James Kettle", "Adrian Lamo",
                     "Frans Rosen", "Kevin Mitnick", "John Draper",
                     "George Hotz"):
            self.assertIn(name, prompt, name)

    def test_quota_order_carries_quota_discipline(self):
        prompt = self.quota_order["doctrine_prompt"]
        self.assertIn("EFFORT BUDGET", prompt)
        self.assertIn("never", " ".join(prompt.split()) )
        self.assertIn("severity inflation", prompt)
        self.assertIn("differential triad", prompt)

    def test_quota_order_carries_mission_horizon(self):
        prompt = self.quota_order["doctrine_prompt"]
        self.assertIn("continuation mandate", prompt)
        self.assertIn("exhaustion proof", prompt)
        self.assertIn("operator release", prompt)
        self.assertIn("stop-condition violation", prompt)

    def test_ai_surface_order_carries_the_mirror_laws(self):
        """An AI-target instruction forges the mirror order: eligibility
        gate first, jailbreak-vs-impact, labeled projections, the rate
        law, and the wrapper rule (mirror-hunter SKILL.md sections 3-5)."""
        forged = _mythos.doctrine_forge(
            "uji prompt injection di target AI ini sampai dapat 1 celah high")
        prompt = forged["doctrine_prompt"]
        self.assertEqual(forged["detected_intent"], "ai_surface")
        # eligibility gate before the first payload
        self.assertIn("Eligibility gate BEFORE the first payload", prompt)
        self.assertIn("ineligible", prompt)
        self.assertIn("jailbreak", prompt)
        # mirror hazard: projections are labeled
        self.assertIn("PROJECTION", prompt)
        # rate law
        self.assertIn("N >= 10", prompt)
        self.assertIn("rate", prompt)
        # wrapper rule
        self.assertIn("deterministic stage", prompt)
        self.assertIn("'the wrapper executed X' is the finding", prompt)
        # persona mix carries the class namer + the chain/boundary crafts
        keys = [p["key"] for p in forged["persona_mix"]]
        self.assertIn("simon-willison", keys)
        self.assertIn("orange-tsai", keys)
        self.assertIn("frans-rosen", keys)
        # the spine's long-horizon discipline rides along unchanged
        self.assertIn("continuation mandate", prompt)

    def test_gates_ride_along_on_every_order(self):
        for request in ("tolong lanjutkan pekerjaan yang tertunda",
                        "get me 3 bugs",
                        "map the surface",
                        "classify the report",
                        "we are breached",
                        "hello"):
            forged = _mythos.doctrine_forge(request)
            self.assertEqual(forged["gates"], _mythos.QUALITY_GATES)
            self.assertIn("differential triad", " ".join(forged["gates"]))

    def test_original_request_rides_along_verbatim(self):
        request = "tolong lanjutkan pekerjaan bug bounty yang tertunda"
        forged = _mythos.doctrine_forge(request)
        self.assertEqual(forged["operator_request"], request)
        self.assertIn("verbatim", forged["escalation_rule"])

    def test_context_passthrough(self):
        forged = _mythos.doctrine_forge(
            "continue the work", context="phase 2 parked, budget half spent")
        self.assertEqual(forged["context"], "phase 2 parked, budget half spent")

    def test_persona_organs_all_ship(self):
        installed = set(_mythos._installed_skills())
        for persona in _mythos.LEGEND_REGISTRY:
            self.assertIn(persona["organ"], installed,
                          "%s organ missing" % persona["organ"])

    def test_quota_persona_mix_covers_seven_legends(self):
        keys = [p["key"] for p in self.quota_order["persona_mix"]]
        self.assertEqual(sorted(keys), sorted([
            "adrian-lamo", "orange-tsai", "james-kettle", "frans-rosen",
            "kevin-mitnick", "john-draper", "george-hotz"]))

    def test_continue_order_recovers_park_state(self):
        forged = _mythos.doctrine_forge(
            "tolong lanjutkan pekerjaan bug bounty yang tertunda")
        prompt = forged["doctrine_prompt"]
        self.assertIn("PARK", prompt)
        self.assertIn("ledger_summary", prompt)
        self.assertIn("resume, never restart", prompt)

    def test_phase_plan_and_tools_present(self):
        for forged in (self.quota_order,
                       _mythos.doctrine_forge("map the surface")):
            self.assertTrue(forged["phase_plan"])
            self.assertTrue(forged["tools"])
            self.assertTrue(all(t for t in forged["tools"]))

    def test_forged_order_carries_execution_doctrine(self):
        for request in ("dapatkan minimal 3 bug high-medium",
                        "map the target surface",
                        "tolong lanjutkan pekerjaan bug bounty yang tertunda"):
            forged = _mythos.doctrine_forge(request)
            doctrine = forged.get("execution_doctrine")
            self.assertTrue(doctrine, request)
            joined = " ".join(doctrine)
            self.assertIn("OODA-hygiene", joined)
            self.assertIn("observation note", joined)
            self.assertIn("differential triad", joined)
            self.assertIn("lesson", joined)
            prompt = forged["doctrine_prompt"]
            self.assertIn("EXECUTION DOCTRINE", prompt)
            self.assertIn("OODA-hygiene", prompt)
            self.assertIn("autonomous-operation.md", prompt)


class TestDeterminism(unittest.TestCase):
    REQUESTS = [
        "tolong lanjutkan pekerjaan bug bounty yang tertunda",
        "dapatkan minimal 3 bug high-medium",
        "map the target surface",
        "classify findings with cvss and vrt",
        "random gibberish zzz",
    ]

    def test_same_request_forges_identical_order(self):
        for request in self.REQUESTS:
            first = _mythos.doctrine_forge(request)
            second = _mythos.doctrine_forge(request)
            self.assertEqual(first, second, request)
            self.assertTrue(first["deterministic"])

    def test_different_severity_different_order(self):
        a = _mythos.doctrine_forge("dapatkan minimal 3 bug high")
        b = _mythos.doctrine_forge("dapatkan minimal 3 bug critical")
        self.assertNotEqual(a["severity_goal"], b["severity_goal"])
        self.assertNotEqual(a["doctrine_prompt"], b["doctrine_prompt"])


if __name__ == "__main__":
    unittest.main()
