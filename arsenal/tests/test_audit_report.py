"""Auditor grounding tests — citation laundering dies here.

Covers audit checks 9 (existence) and 10 (relevance entailment proxy):
fabricated records, misdirected citations, non-evidence tags, clean and
weakly-grounded reports, standalone mode, and sibling-ledger autodetect.
"""
import importlib.util
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

from arsenal import ledger  # noqa: E402

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
_SPEC = importlib.util.spec_from_file_location(
    "audit_report_under_test", os.path.join(_ROOT, "auditor",
                                            "audit_report.py"))
AR = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(AR)


class TestGrounding(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.environ["MYTHOS_ARSENAL_ROOT"] = self.root
        self.program = "audit-test"
        self.ledger_dir = os.path.join(self.root, "engagements",
                                       self.program, "ledger")
        # seed a small engagement ledger: a /login surface and an /admin fact
        self.rid_login = ledger.append(
            self.program, "GET /login", "http://t.lab/login",
            "200 412B", "412B", "SURFACE", "login page")
        self.rid_admin = ledger.append(
            self.program, "GET /admin", "http://t.lab/admin",
            "307 loc=/login", "0B", "FACT", "redirect")
        ledger.merge(self.program)
        self.report = os.path.join(self.root, "report.md")

    def tearDown(self):
        os.environ.pop("MYTHOS_ARSENAL_ROOT", None)

    def _audit(self, text, **kw):
        with open(self.report, "w") as fh:
            fh.write(text)
        return AR.audit(self.report, **kw)

    def _fails(self, results):
        return [m for s, m in results if s == "FAIL"]

    def test_fabricated_record_fails(self):
        fails = self._fails(self._audit(
            "Reflected XSS on /login (R-999)\n",
            ledger_dir=self.ledger_dir))
        self.assertTrue(any("does not exist" in m for m in fails))

    def test_misdirected_citation_fails(self):
        # the claim names /admin; the cited record only ever touched /login
        fails = self._fails(self._audit(
            "Reflected XSS on the /admin console (%s)\n" % self.rid_login,
            ledger_dir=self.ledger_dir))
        self.assertTrue(any("never touched" in m for m in fails))

    def test_non_evidence_tag_fails(self):
        rid_c = ledger.append(
            self.program, "GET /junk123", "http://t.lab/junk123",
            "404 0B", "0B", "CONTROL", "calibration")
        fails = self._fails(self._audit(
            "IDOR on /admin exposes data (%s)\n" % rid_c,
            ledger_dir=self.ledger_dir))
        self.assertTrue(any("non-evidence" in m for m in fails))

    def test_grounded_claim_passes(self):
        results = self._audit(
            "Reflected XSS confirmed on the /login page (%s)\n"
            % self.rid_login,
            ledger_dir=self.ledger_dir)
        self.assertFalse(self._fails(results))
        self.assertTrue(any(s == "PASS" and "citation existence" in m
                            for s, m in results))

    def test_weak_grounding_flagged_not_failed(self):
        # right surface, one shared token — human review, not a hard fail
        results = self._audit(
            "XSS found on /login (%s)\n" % self.rid_login,
            ledger_dir=self.ledger_dir)
        self.assertFalse(self._fails(results))
        self.assertTrue(any("weak grounding" in m for s, m in results
                            if s == "INFO"))

    def test_standalone_mode_skips_grounding(self):
        results = self._audit("Reflected XSS on /login (R-999)\n")
        self.assertFalse(self._fails(results))
        self.assertTrue(any("no engagement context" in m
                            for s, m in results if s == "INFO"))

    def test_sibling_ledger_autodetected(self):
        ex = os.path.join(self.root, "ex")
        os.makedirs(os.path.join(ex, "ledger"))
        with open(os.path.join(ex, "ledger", "records.md"), "w") as fh:
            fh.write("R-001 | GET /x | http://t.lab/x | 200 1B | 1B | FACT "
                     "| ok\n")
        rep = os.path.join(ex, "report.md")
        with open(rep, "w") as fh:
            fh.write("XSS on /x (R-999)\n")
        results = AR.audit(rep)
        self.assertTrue(any("does not exist" in m
                            for s, m in results if s == "FAIL"))

    def test_missing_ledger_skips_gracefully(self):
        results = self._audit(
            "XSS on /login (R-001)\n",
            ledger_dir=os.path.join(self.root, "nope"))
        self.assertFalse(self._fails(results))
        self.assertTrue(any("unavailable" in m for s, m in results
                            if s == "INFO"))


if __name__ == "__main__":
    unittest.main()
