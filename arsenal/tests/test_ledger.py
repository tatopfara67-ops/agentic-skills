"""Ledger unit tests — append-only discipline, ids, merge, sanitization."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

import arsenal.ledger as ledger  # noqa: E402


class TestLedger(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.environ["MYTHOS_ARSENAL_ROOT"] = self.root
        self.program = "unit-test"

    def tearDown(self):
        os.environ.pop("MYTHOS_ARSENAL_ROOT", None)

    def test_sequential_ids(self):
        r1 = ledger.append(self.program, "curl", "GET /", "200", "1kB",
                           "FACT", "first")
        r2 = ledger.append(self.program, "curl", "GET /a", "404", "12B",
                           "SURFACE", "second")
        self.assertEqual((r1, r2), ("R-001", "R-002"))

    def test_append_only(self):
        ledger.append(self.program, "t", "a", "r", "", "FACT", "")
        before = ledger.count(self.program)
        # appending never rewrites; the only writer is append()
        ledger.append(self.program, "t", "a2", "r2", "", "FACT", "")
        self.assertEqual(ledger.count(self.program), before + 1)
        records = os.path.join(self.root, "engagements", self.program,
                               "ledger", "records.md")
        with open(records) as fh:
            self.assertEqual(len(fh.read().splitlines()), 0)  # merge pending

    def test_merge(self):
        for i in range(3):
            ledger.append(self.program, "t", "a%d" % i, "r", "", "FACT", "")
        moved = ledger.merge(self.program)
        self.assertEqual(moved, 3)
        self.assertEqual(ledger.count(self.program), 3)
        self.assertEqual(ledger.merge(self.program), 0)  # idempotent

    def test_read_and_summary(self):
        rid = ledger.append(self.program, "curl", "GET /x", "307", "0B",
                            "EXPERIMENT", "baseline run 1/3, H-001")
        line = ledger.read(self.program, rid)
        self.assertIn(rid, line)
        self.assertIn("EXPERIMENT", line)
        summary = ledger.summary(self.program)
        self.assertEqual(summary[0]["id"], rid)
        self.assertEqual(summary[0]["tag"], "EXPERIMENT")

    def test_pipe_sanitized(self):
        rid = ledger.append(self.program, "t", "a|b|c", "r|d", "", "FACT", "")
        line = ledger.read(self.program, rid)
        self.assertNotIn("a|b", line)  # pipes replaced, format intact
        self.assertEqual(line.count(" | "), 7)  # 8 fields, 7 separators

    def test_bad_tag_rejected(self):
        with self.assertRaises(ValueError):
            ledger.append(self.program, "t", "a", "r", "", "BOGUS", "")

    def test_read_missing(self):
        with self.assertRaises(KeyError):
            ledger.read(self.program, "R-999")


if __name__ == "__main__":
    unittest.main()
