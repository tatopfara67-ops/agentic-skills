"""Vault accuracy bench tests — proving_ground.py.

The bench contract under test:
  * the labeled case set decides exactly as labeled on the current
    gate: zero false releases (the zero-miss doctrine — a labeled
    refusal that releases is the critical failure), zero false
    refusals (overblocking is a defect, not margin), accuracy 1.0
  * the refuse side covers every refusal family with the right
    REASON (instruction-override, unknown entry, the scope triad)
  * the release side spans every vault organ — the corpus wave
    coverage is exercised end-to-end through the same door
  * the banned-class dimension hits the weaponized vocabulary and
    passes the authorized-testing vocabulary, including the
    credential-bearing metadata probes and browser gadget bytes
  * the bench is deterministic and hermetic: same output twice, a
    synthetic .test fixture scope, no environment read, no host
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

from arsenal import proving_ground  # noqa: E402


class TestVaultBench(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = proving_ground.run_bench()

    def test_bench_passes_with_zero_miss(self):
        """The zero-miss doctrine: no labeled refusal ever releases,
        no labeled release is blocked, and the verdict is PASS."""
        m = self.report["metrics"]
        self.assertEqual(self.report["verdict"], "PASS")
        self.assertEqual(m["false_releases"], 0)
        self.assertEqual(m["false_refusals"], 0)
        self.assertEqual(m["accuracy"], 1.0)
        self.assertEqual(m["refuse_precision"], 1.0)
        self.assertEqual(m["refuse_recall"], 1.0)

    def test_refuse_side_covers_every_family_with_the_right_reason(self):
        """Every refusal carries its family's reason — a right verdict
        with a wrong reason still surfaces in the case rows."""
        rows = {r["case"]: r for r in self.report["cases"]}
        jailbreak_family = [c for c in rows if c.startswith("jb-")]
        self.assertGreaterEqual(len(jailbreak_family), 17)
        for case in jailbreak_family:
            self.assertEqual(rows[case]["got"], "refuse", case)
            self.assertTrue(rows[case]["reason_family_ok"], case)
        for case, fragment in (("unk-01", "no versioned corpus entry"),
                               ("unk-02", "no versioned corpus entry"),
                               ("sc-01", "deny-by-default"),
                               ("sc-02", "recon_only"),
                               ("sc-03", "authorizing artifact")):
            self.assertEqual(rows[case]["got"], "refuse", case)
            self.assertTrue(rows[case]["reason_family_ok"], case)
        confusion = self.report["metrics"]["confusion_refuse_class"]
        self.assertEqual(confusion["true_refusal"], 22)

    def test_release_side_spans_every_vault_organ(self):
        """The clean releases exercise every organ corpus through the
        same door — including the fifth-wave ssrf/prototype entries and
        the php2shell forensics organ (its detection entries are
        standard-tier but release through the vault like everything)."""
        organs = self.report["metrics"]["organs_released_through"]
        self.assertEqual(organs, [
            "cache-playbook", "desync-hunter", "injection-lab",
            "php2shell-forensics", "prototype-playbook", "ssrf-playbook",
            "xss-playbook"])
        rows = {r["case"]: r for r in self.report["cases"]}
        self.assertEqual(rows["rl-05"]["organ"], "ssrf-playbook")
        self.assertEqual(rows["rl-07"]["organ"], "prototype-playbook")
        self.assertEqual(rows["rl-09"]["organ"], "php2shell-forensics")

    def test_banned_dimension_hits_and_passes_exactly(self):
        """Weaponized vocabulary hits; authorized-testing vocabulary
        (delay oracles, mutation markers, the credential-bearing
        metadata curl, the browser gadget bytes) passes."""
        banned = self.report["metrics"]["banned_scan"]
        self.assertEqual(banned["must_hit"], banned["hits"])
        self.assertEqual(banned["false_hits"], 0)
        self.assertEqual(banned["must_pass"], banned["passes"])
        self.assertEqual(banned["false_passes"], 0)
        self.assertGreaterEqual(banned["must_pass"], 4)

    def test_bench_is_deterministic(self):
        """A measurement of a pure function: two runs, one output."""
        again = proving_ground.run_bench()
        self.assertEqual(self.report, again)

    def test_fixture_is_synthetic_and_hermetic(self):
        """The embedded scope fixture uses .test hosts only (never
        resolvable), and the case set carries no real host — the bench
        is inspect-only by construction."""
        for case in proving_ground.CASES:
            _cid, entry_id, target, _note, _expected, _frag = case
            self.assertIn(".test", target, entry_id)
            self.assertTrue(
                target.startswith("https://") or
                target.startswith("http://"), target)
        source = os.path.join(os.path.dirname(proving_ground.__file__),
                              "proving_ground.py")
        with open(source, encoding="utf-8") as fh:
            body = fh.read()
        self.assertNotIn("os.environ", body)
        self.assertNotIn("getenv", body)


if __name__ == "__main__":
    unittest.main()
