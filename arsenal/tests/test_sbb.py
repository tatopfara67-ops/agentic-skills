"""SBB unit tests — the binary brain's mechanical rules.

Covers: null-hypothesis auto-insert, partition validation, information-
gain ranking, pre-registration discipline, tip-off gating, the two-channel
rule, falsified-space handling, mid-hunt extension, and convergence at
the information-theoretic floor.

The fixture is a perfect binary tree over 8 hypotheses (auto null + 7
operator labels l1..l7; the "truth" is l3), so every split is exactly
1.00 bit and convergence lands on the floor, log2(8) = 3.
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

import arsenal.ledger as ledger  # noqa: E402
import arsenal.sbb as sbb  # noqa: E402


def _balanced_tests():
    """Partitions over labels (null is auto-inserted as H-001):

    T-001 netflow history      : on 1 kills l4..l7        (4/4 split)
    T-002 lease origin         : on 1 kills null,l1,l4..l7 (2/2 over the 4
                                 survivors of T-001=1)
    T-003 interface fingerprint: on 1 kills l2             (1/1 final)
    T-004 credential tripwire  : tip-off gated, second channel
    """
    labels = ["l1", "l2", "l3", "l4", "l5", "l6", "l7"]
    return labels, [
        {"label": "history check", "channel": "netflow", "tip_off": False,
         "kills_one": ["l4", "l5", "l6", "l7"],
         "kills_zero": [sbb.NULL_LABEL, "l1", "l2", "l3"]},
        {"label": "lease origin", "channel": "netflow", "tip_off": False,
         "kills_one": [sbb.NULL_LABEL, "l1", "l4", "l5", "l6", "l7"],
         "kills_zero": ["l2", "l3"]},
        {"label": "interface fingerprint", "channel": "host-audit",
         "tip_off": False,
         "kills_one": ["l2"], "kills_zero": ["l3"]},
        {"label": "credential tripwire", "channel": "identity",
         "tip_off": True,
         "kills_one": [sbb.NULL_LABEL, "l1", "l2", "l6"],
         "kills_zero": ["l3", "l5", "l7"]},
    ]


class TestSBB(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.environ["MYTHOS_ARSENAL_ROOT"] = self.root
        self.program = "sbb-unit"

    def tearDown(self):
        os.environ.pop("MYTHOS_ARSENAL_ROOT", None)

    # ---------------------------------------------------------- declare

    def test_fresh_declare_inserts_null(self):
        labels, tests = _balanced_tests()
        out = sbb.declare(self.program, "case", "odd login at 03:14",
                          labels, tests)
        self.assertTrue(out["ok"])
        all_labels = [h["label"] for h in out["eliminations"]]
        self.assertTrue(any(l.startswith("authorized or benign activity")
                            for l in all_labels))
        self.assertEqual(out["stats"]["initial"], 8)
        self.assertEqual(out["stats"]["floor"], 3)

    def test_declare_rejects_bad_partitions(self):
        with self.assertRaises(ValueError):  # unknown label
            sbb.declare(self.program, "case", "trig", ["a"], [
                {"label": "t", "channel": "c",
                 "kills_one": ["nope"], "kills_zero": []}])
        with self.assertRaises(ValueError):  # kills same hyp on both sides
            sbb.declare(self.program, "case", "trig", ["a"], [
                {"label": "t", "channel": "c",
                 "kills_one": ["a"], "kills_zero": ["a"]}])
        with self.assertRaises(ValueError):  # duplicate hypothesis label
            sbb.declare(self.program, "case", "trig", ["a", "a"], [])

    def test_single_channel_warned(self):
        out = sbb.declare(self.program, "case", "trig", ["a", "b"], [
            {"label": "t", "channel": "only-one",
             "kills_one": ["a"], "kills_zero": ["b"]}])
        self.assertIn("Rule T", out["warning"])

    # ----------------------------------------------------------- decide

    def test_decide_ranks_by_information_gain(self):
        labels, tests = _balanced_tests()
        tests.append({"label": "lopsided", "channel": "netflow",
                      "tip_off": False,
                      "kills_one": ["l7"], "kills_zero": []})
        sbb.declare(self.program, "case", "trig", labels, tests)
        out = sbb.decide(self.program)
        self.assertEqual(out["chosen"]["id"], "T-001")  # 1.00 beats 0.54
        self.assertEqual(out["chosen"]["bits"], 1.0)
        self.assertEqual(out["chosen"]["on_1_kills"],
                         ["H-005", "H-006", "H-007", "H-008"])
        self.assertEqual(out["chosen"]["on_0_kills"],
                         ["H-001", "H-002", "H-003", "H-004"])

    def test_decide_pre_registers_experiment(self):
        labels, tests = _balanced_tests()
        sbb.declare(self.program, "case", "trig", labels, tests)
        before = ledger.count(self.program)
        sbb.decide(self.program)
        sbb.decide(self.program)  # idempotent: no double pre-registration
        self.assertEqual(ledger.count(self.program), before + 1)
        line = ledger.read(self.program, "R-002")
        self.assertIn("EXPERIMENT", line)
        self.assertIn("pre-register T-001", line)

    def test_decide_requires_open_hunt(self):
        with self.assertRaises(RuntimeError):
            sbb.decide(self.program)

    # ------------------------------------------------------------ apply

    def test_tipoff_refused_while_passive_remains(self):
        labels, tests = _balanced_tests()
        sbb.declare(self.program, "case", "trig", labels, tests)
        out = sbb.apply(self.program, "T-004", 1)  # the credential tripwire
        self.assertFalse(out["ok"])
        self.assertIn("refused while passive", out["error"])
        line = ledger.read(self.program, out["rid"])
        self.assertIn("REFUSED", line)

    def test_apply_eliminates_and_ledgers_fact(self):
        labels, tests = _balanced_tests()
        sbb.declare(self.program, "case", "trig", labels, tests)
        before = ledger.count(self.program)
        out = sbb.apply(self.program, "T-001", 1)
        self.assertTrue(out["ok"])
        self.assertEqual(out["eliminated"],
                         ["H-005", "H-006", "H-007", "H-008"])
        self.assertEqual(out["active_remaining"], 4)
        line = ledger.read(self.program, "R-002")
        self.assertIn("FACT", line)
        self.assertEqual(ledger.count(self.program), before + 1)

    def test_apply_rejects_rerun_and_bad_outcome(self):
        labels, tests = _balanced_tests()
        sbb.declare(self.program, "case", "trig", labels, tests)
        sbb.apply(self.program, "T-001", 1)
        with self.assertRaises(ValueError):  # already ran — history is frozen
            sbb.apply(self.program, "T-001", 0)
        with self.assertRaises(ValueError):  # not binary
            sbb.apply(self.program, "T-002", "maybe")

    def test_zero_capability_test_refused(self):
        sbb.declare(self.program, "case", "trig", ["a", "b"], [
            {"label": "useless", "channel": "c",
             "kills_one": [], "kills_zero": []},
            {"label": "real", "channel": "c",
             "kills_one": ["a"], "kills_zero": ["b"]}])
        out = sbb.apply(self.program, "T-001", 1)
        self.assertFalse(out["ok"])
        self.assertIn("Rule H", out["error"])

    def test_singleton_confirmed_via_second_channel(self):
        labels, tests = _balanced_tests()
        # drop T-003: the hunt must instead confirm through the identity
        # channel (T-004) once passive netflow reserves are exhausted
        tests = [t for t in tests if t["label"] != "interface fingerprint"]
        sbb.declare(self.program, "case", "trig", labels, tests)
        sbb.apply(self.program, "T-001", 1)   # active: null,l1,l2,l3
        sbb.apply(self.program, "T-002", 1)   # active: l2,l3
        out = sbb.apply(self.program, "T-003", 1)  # tripwire kills l2 -> l3
        self.assertTrue(out["ok"])
        self.assertIn("confirmed", out)
        self.assertEqual(out["confirmed"]["id"], "H-004")
        self.assertEqual(sorted(out["confirmed"]["channels"]),
                         ["identity", "netflow"])

    def test_one_channel_never_confirms(self):
        labels, tests = _balanced_tests()
        tests = [t for t in tests
                 if t["label"] not in ("interface fingerprint",
                                       "credential tripwire")]
        # a third netflow-only probe isolates l3 without opening a channel
        tests.append({"label": "flow-shape probe", "channel": "netflow",
                      "tip_off": False,
                      "kills_one": ["l2"], "kills_zero": ["l3"]})
        sbb.declare(self.program, "case", "trig", labels, tests)
        sbb.apply(self.program, "T-001", 1)   # active: null,l1,l2,l3
        sbb.apply(self.program, "T-002", 1)   # active: l2,l3
        out = sbb.apply(self.program, "T-003", 1)  # kills l2 -> singleton l3
        self.assertTrue(out["ok"])
        self.assertIn("singleton", out)
        self.assertNotIn("confirmed", out)
        self.assertEqual(out["singleton"]["channels"], ["netflow"])
        self.assertIn("Rule T", out["next"])

    def test_space_falsified_writes_mistake(self):
        self.program = "sbb-unit-dead"
        sbb.declare(self.program, "case2", "trig", ["only"], [
            {"label": "sensor replay check", "channel": "sensor",
             "tip_off": False,
             "kills_one": [], "kills_zero": [sbb.NULL_LABEL]},
            {"label": "lease check", "channel": "netflow",
             "tip_off": False,
             "kills_one": ["only"], "kills_zero": [sbb.NULL_LABEL]}])
        sbb.apply(self.program, "T-001", 0)   # null dies; active: only
        out = sbb.apply(self.program, "T-002", 1)  # only dies; space empty
        self.assertTrue(out["ok"])
        self.assertEqual(out["active_remaining"], 0)
        view = sbb.decide(self.program)
        self.assertEqual(view["mode"], "space-empty")
        append_path = os.path.join(self.root, "engagements", self.program,
                                   "ledger", "append.md")
        with open(append_path) as fh:
            mistakes = [ln for ln in fh.read().splitlines()
                        if "MISTAKE" in ln]
        self.assertTrue(mistakes)

    def test_declare_extends_mid_hunt(self):
        labels, tests = _balanced_tests()
        sbb.declare(self.program, "case", "trig", labels, tests)
        sbb.apply(self.program, "T-001", 1)
        out = sbb.declare(self.program, "case", "trig",
                          ["new suspect"], [
            {"label": "t-new", "channel": "identity", "tip_off": False,
             "kills_one": ["new suspect"], "kills_zero": ["l3"]}])
        self.assertTrue(out["ok"])
        ids = [h["id"] for h in out["eliminations"]]
        self.assertIn("H-009", ids)  # 8 existing + 1 new
        self.assertEqual([t["id"] for t in out["tests"]][-1], "T-005")
        self.assertEqual(out["stats"]["initial"], 8)  # floor unchanged

    def test_converges_at_informational_floor(self):
        labels, tests = _balanced_tests()
        sbb.declare(self.program, "case", "trig", labels, tests)
        d1 = sbb.decide(self.program)
        self.assertEqual(d1["chosen"]["id"], "T-001")
        self.assertEqual(d1["registers"]["split_bits"], 1.0)
        sbb.apply(self.program, "T-001", 1)
        d2 = sbb.decide(self.program)
        self.assertEqual(d2["chosen"]["id"], "T-002")
        self.assertEqual(d2["chosen"]["bits"], 1.0)
        sbb.apply(self.program, "T-002", 1)
        d3 = sbb.decide(self.program)
        self.assertEqual(d3["chosen"]["id"], "T-003")
        self.assertEqual(d3["chosen"]["bits"], 1.0)
        out = sbb.apply(self.program, "T-003", 1)
        self.assertIn("confirmed", out)
        stats = out["stats"]
        self.assertEqual(stats["tests_used"], 3)
        self.assertEqual(stats["floor"], 3)   # log2(8) = 3 exactly
        self.assertEqual(out["confirmed"]["id"], "H-004")  # l3
        self.assertEqual(sorted(out["confirmed"]["channels"]),
                         ["host-audit", "netflow"])


if __name__ == "__main__":
    unittest.main()
