"""Hypothesis-rail unit tests — pre-registration refusals, three-state
closure, retrodiction guard, append-only state."""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

import arsenal.hypotheses as hyp  # noqa: E402
import arsenal.ledger as ledger  # noqa: E402


class TestHypotheses(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.environ["MYTHOS_ARSENAL_ROOT"] = self.root
        self.program = "unit-hyp"
        self.facts = [ledger.append(self.program, "curl", "GET /admin",
                                    "403 empty body", "12B", "FACT", "")]
        self.facts.append(ledger.append(self.program, "curl", "GET /x",
                                        "200", "1kB", "FACT", ""))

    def tearDown(self):
        os.environ.pop("MYTHOS_ARSENAL_ROOT", None)

    def _register(self, **kw):
        base = dict(surface="t.example/admin", obs="403 differs from WAF 403",
                    claim="path-based ACL bypassable by prefix",
                    pred="prefix /admin/../public returns 200",
                    falsifier="3 bypass variants all fail",
                    prior=0.35, prior_basis="class frequency in lab corpus",
                    facts=list(self.facts))
        base.update(kw)
        return hyp.register(self.program, **base)

    def test_register_mints_sequential_ids_and_records(self):
        r1 = self._register()
        r2 = self._register(claim="second mechanism")
        self.assertEqual((r1["id"], r2["id"]), ("H-001", "H-002"))
        self.assertEqual(r1["status"], "open")
        for rid in (r1["record"], r2["record"]):
            line = ledger.read(self.program, rid)
            self.assertIn("HYPOTHESIS", line)

    def test_register_refuses_fact_not_in_ledger(self):
        with self.assertRaises(ValueError) as ctx:
            self._register(facts=["R-999"])
        self.assertIn("not in the ledger", str(ctx.exception))

    def test_register_refutes_no_facts(self):
        with self.assertRaises(ValueError):
            self._register(facts=[])

    def test_register_refuses_bad_prior(self):
        for prior in (0, 1, 1.5, -0.2):
            with self.assertRaises(ValueError):
                self._register(prior=prior)

    def test_register_refuses_empty_slots(self):
        for field in ("surface", "obs", "claim", "pred", "falsifier",
                      "prior_basis"):
            kw = {field: "  "}
            with self.assertRaises(ValueError):
                self._register(**kw)

    def test_register_validates_cue(self):
        with self.assertRaises(ValueError):
            self._register(cue="cue-2")
        r = self._register(cue="C2")
        self.assertEqual(r["id"], "H-001")

    def test_close_confirmed_writes_closure_record(self):
        h = self._register()
        ev = ledger.append(self.program, "curl", "GET /admin/../public",
                           "200", "9B", "EXPERIMENT", "delta vs R-001, H-001")
        out = hyp.close(self.program, h["id"], "CONFIRMED", [ev])
        self.assertEqual(out["state"], "CONFIRMED")
        line = ledger.read(self.program, out["record"])
        self.assertIn("CLOSURE", line)
        self.assertIn(h["id"], line)

    def test_close_refuses_fourth_state(self):
        h = self._register()
        with self.assertRaises(ValueError) as ctx:
            hyp.close(self.program, h["id"], "SUPPORTED", self.facts)
        self.assertIn("three states", str(ctx.exception))

    def test_close_refuses_missing_evidence(self):
        h = self._register()
        with self.assertRaises(ValueError):
            hyp.close(self.program, h["id"], "FALSIFIED", ["R-499"])

    def test_close_refuses_inconclusive_without_park(self):
        h = self._register()
        with self.assertRaises(ValueError) as ctx:
            hyp.close(self.program, h["id"], "INCONCLUSIVE", self.facts)
        self.assertIn("Park", str(ctx.exception))
        park = ledger.append(self.program, "scan-economist", "budget R7",
                             "vector budget exhausted", "", "PARK", "H-001")
        out = hyp.close(self.program, h["id"], "inconclusive", [park])
        self.assertEqual(out["state"], "INCONCLUSIVE")

    def test_close_is_append_only(self):
        h = self._register()
        ev = ledger.append(self.program, "curl", "GET /admin/x", "403",
                           "0B", "CONTROL", "same delta, H-001")
        hyp.close(self.program, h["id"], "FALSIFIED", [ev])
        with self.assertRaises(ValueError) as ctx:
            hyp.close(self.program, h["id"], "CONFIRMED", self.facts)
        self.assertIn("append-only", str(ctx.exception))

    def test_close_refuses_unknown_id(self):
        with self.assertRaises(KeyError):
            hyp.close(self.program, "H-999", "FALSIFIED", self.facts)

    def test_retrodiction_guard(self):
        # an EXPERIMENT citing H-001, timestamped BEFORE registration
        with open(os.path.join(self.root, "engagements", self.program,
                               "ledger", "append.md"), "a",
                  encoding="utf-8") as fh:
            fh.write("R-098 | 2020-01-01T00:00:00Z | curl | GET /admin/../"
                     "public | 200 | 9B | EXPERIMENT | delta, H-001\n")
        h = self._register()          # registered "now" — after R-098
        with self.assertRaises(ValueError) as ctx:
            hyp.close(self.program, h["id"], "CONFIRMED", ["R-098"])
        self.assertIn("retrodiction", str(ctx.exception))
        out = hyp.close(self.program, h["id"], "FALSIFIED", ["R-098"])
        self.assertIn("retrodiction_warning", out)  # flagged, not refused

    def test_summary_folds_and_filters(self):
        h1 = self._register()
        h2 = self._register(claim="second mechanism")
        ev = ledger.append(self.program, "curl", "GET /a", "200", "1B",
                           "CONTROL", "delta zero, H-002")
        hyp.close(self.program, h2["id"], "FALSIFIED", [ev])
        view = hyp.summary(self.program)
        self.assertEqual(view["counts"],
                         {"open": 1, "confirmed": 0, "falsified": 1,
                          "inconclusive": 0})
        self.assertEqual([r["id"] for r in view["rows"]],
                         [h1["id"], h2["id"]])
        only_open = hyp.summary(self.program, status="open")
        self.assertEqual([r["id"] for r in only_open["rows"]], [h1["id"]])
        with self.assertRaises(ValueError):
            hyp.summary(self.program, status="parked")

    def test_state_is_append_only_jsonl(self):
        h = self._register()
        ev = ledger.append(self.program, "curl", "GET /b", "200", "1B",
                           "CONTROL", "delta zero, H-001")
        hyp.close(self.program, h["id"], "FALSIFIED", [ev])
        path = os.path.join(self.root, "engagements", self.program,
                            "hypotheses.jsonl")
        with open(path, encoding="utf-8") as fh:
            rows = [json.loads(ln) for ln in fh if ln.strip()]
        self.assertEqual(len(rows), 2)          # register + closure, no edits
        self.assertEqual(rows[0]["status"], "open")       # history intact
        self.assertEqual(rows[1]["status"], "falsified")  # last row wins

    def test_calibration_signal(self):
        h = self._register(prior=0.8)
        ev = ledger.append(self.program, "curl", "GET /c", "403", "0B",
                           "CONTROL", "delta zero, H-001")
        out = hyp.close(self.program, h["id"], "FALSIFIED", [ev])
        self.assertIn("mistake-ledger", out["calibration"])


if __name__ == "__main__":
    unittest.main()
