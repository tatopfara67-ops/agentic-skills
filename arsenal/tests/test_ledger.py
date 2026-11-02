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

    # ------------------------------------------- O(1) id minting (v1.7.0)

    def test_o1_mint_beyond_record_1000(self):
        ids = [ledger.append(self.program, "t", "a", "r", "", "FACT", "")
               for _ in range(1100)]
        self.assertEqual(ids[0], "R-001")
        self.assertEqual(ids[999], "R-1000")       # 4-digit id, format intact
        self.assertEqual(ids[-1], "R-1100")
        self.assertTrue(all(int(b[2:]) - int(a[2:]) == 1
                            for a, b in zip(ids, ids[1:])))
        self.assertEqual(ledger.count(self.program), 1100)

    def test_mint_after_trailing_operator_notes(self):
        for _ in range(5):
            ledger.append(self.program, "t", "a", "r", "", "FACT", "")
        d = os.path.join(self.root, "engagements", self.program, "ledger")
        with open(os.path.join(d, "append.md"), "a") as fh:
            fh.write("# operator note: weekend pause\n" * 50)
        self.assertEqual(
            ledger.append(self.program, "t", "a", "r", "", "FACT", ""),
            "R-006")

    def test_full_scan_fallback_when_tails_unreadable(self):
        # a records.md whose 8KB tail is a wall of notes (no record lines
        # in the window) must fall back to ONE full scan — ids never
        # collide silently on a hand-mangled ledger
        d = os.path.join(self.root, "engagements", self.program, "ledger")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "records.md"), "w") as fh:
            fh.write("R-001 | t | a | r |  | FACT | hand-built\n")
            fh.write("R-002 | t | a | r |  | FACT | hand-built\n")
            fh.write("# " + "operator notes " * 700 + "\n")   # > 8KB tail
        open(os.path.join(d, "append.md"), "w").close()
        self.assertEqual(
            ledger.append(self.program, "t", "a", "r", "", "FACT", ""),
            "R-003")

    def test_portable_lock_context(self):
        # the cross-platform lock acquires and releases on this platform
        d = ledger._ledger_dir(self.program)
        with ledger._CrossFileLock(os.path.join(d, ".lock")):
            pass
        with ledger._CrossFileLock(os.path.join(d, ".lock")):
            pass                      # re-acquirable after release


if __name__ == "__main__":
    unittest.main()
