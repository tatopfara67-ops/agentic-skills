"""Tool smoke tests against a live mythos-lab instance (ephemeral port).

Covers: gating + REFUSED records, http_probe artifacts, calibrated content
discovery, js_analyze extraction/masking, api_introspect spec parsing,
dossier evidence discipline, arsenal_route governance (fake binary,
blocked flags, allowlist).
"""
import json
import os
import stat
import subprocess
import sys
import tempfile
import threading
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

from arsenal import ledger  # noqa: E402
from arsenal.tools import dossier as _dossier  # noqa: E402
from arsenal.tools import jsrecon, passive, probe  # noqa: E402
from arsenal.tools import arsenal_route as _route  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from lab.target_app import Handler  # noqa: E402

from http.server import ThreadingHTTPServer  # noqa: E402

SCOPE = "127.0.0.1,in_scope,lab declaration,,,op,\n"


class LabFixture:
    def __init__(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.server.server_address[1]
        self.base = "http://127.0.0.1:%d" % self.port
        self.thread = threading.Thread(target=self.server.serve_forever,
                                       daemon=True)
        self.thread.start()

    def stop(self):
        self.server.shutdown()


class TestTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = LabFixture()
        cls.root = tempfile.mkdtemp()
        os.environ["MYTHOS_ARSENAL_ROOT"] = cls.root
        with open(os.path.join(cls.root, "scope.csv"), "w") as fh:
            fh.write(SCOPE)
        cls.program = "tool-test"

    @classmethod
    def tearDownClass(cls):
        cls.lab.stop()
        os.environ.pop("MYTHOS_ARSENAL_ROOT", None)

    # ------------------------------------------------------------ gating

    def test_01_refusal_creates_refused_record(self):
        with self.assertRaises(RuntimeError):
            probe.http_probe(self.program, "http://192.0.2.55/")
        tags = [s["tag"] for s in ledger.summary(self.program)]
        self.assertIn("REFUSED", tags)

    def test_02_passive_tool_offline_graceful(self):
        res = passive.ct_subdomains(self.program, "127.0.0.1")
        self.assertIn("ok", res)  # no crash either way

    # --------------------------------------------------------- http_probe

    def test_03_http_probe_records_and_saves_artifact(self):
        out = probe.http_probe(self.program, self.lab.base + "/")
        self.assertEqual(out["status"], 200)
        self.assertTrue(out["rid"].startswith("R-"))
        self.assertTrue(os.path.isfile(out["artifact"]))
        self.assertNotIn("body", out)  # bodies stay out of context

    def test_04_redirect_observed_not_followed(self):
        out = probe.http_probe(self.program, self.lab.base + "/admin")
        self.assertEqual(out["status"], 307)
        self.assertEqual(out.get("location"), "/login")

    # --------------------------------------------------- content_discover

    def test_05_content_discover_calibrated_findings(self):
        wl = os.path.join(self.root, "mini.txt")
        with open(wl, "w") as fh:
            fh.write("admin\nlogin\nbackup\n.env\napi/v0/debug\n"
                     "api/v1/users\nopenapi.json\ndump\n")
        out = probe.content_discover(
            self.program, self.lab.base, wordlist=wl,
            extensions=["", ".zip", ".example"],
            max_requests=60, rate_per_s=50.0)
        self.assertEqual(out["calibration"]["status"], 404)
        paths = {f["path"] for f in out["findings"]}
        self.assertIn("/backup.zip", paths)
        self.assertIn("/login", paths)
        self.assertIn("/admin", paths)
        self.assertIn("/.env.example", paths)
        self.assertIn("/api/v0/debug", paths)
        self.assertIn("/api/v1/users", paths)
        self.assertNotIn("/dump", paths)  # plain 404 = no finding

    # ----------------------------------------------------------- js_analyze

    def test_06_js_analyze_extraction_and_masking(self):
        out = jsrecon.js_analyze(self.program, self.lab.base + "/app.js")
        self.assertTrue(out["ok"])
        self.assertIn("/api/v2/admin/metrics", out["endpoints"])
        self.assertIn("/api/v1/users", out["endpoints"])
        self.assertIn("/api/v0/debug", out["commented_routes"])
        joined = json.dumps(out["secret_hints"])
        self.assertIn("MYTHOS", joined)  # masked head visible
        self.assertNotIn("MYTHOS-CANARY-lab-013", json.dumps(out))

    # ------------------------------------------------------- api_introspect

    def test_07_api_introspect_finds_openapi(self):
        out = probe.api_introspect(self.program, self.lab.base)
        spec = [f for f in out["found"] if f["endpoint"] == "/openapi.json"]
        self.assertEqual(len(spec), 1)
        self.assertEqual(spec[0]["path_count"], 4)
        self.assertIn("/api/v2/admin/export", spec[0]["paths"])

    # -------------------------------------------------------------- dossier

    def test_08_dossier_evidence_discipline(self):
        rid = ledger.append(self.program, "t", "a", "r", "", "SURFACE", "")
        with self.assertRaises(ValueError):  # unknown class
            _dossier.dossier_add(self.program, "http://x/", "bogus-class", rid)
        with self.assertRaises(ValueError):  # evidence not in ledger
            _dossier.dossier_add(self.program, "http://x/", "web-app",
                                 "R-999")
        ok = _dossier.dossier_add(self.program, "http://127.0.0.1:1/x",
                                  "web-app", rid, priority=60,
                                  note="unit surface")
        self.assertEqual(ok["id"], "S-001")

    def test_09_dossier_render(self):
        rendered = _dossier.dossier_render(self.program)
        self.assertTrue(rendered["ok"])
        with open(rendered["path"]) as fh:
            text = fh.read()
        self.assertIn("## Asset graph", text)
        self.assertIn("## Priority queue", text)

    # --------------------------------------------------------- arsenal_route

    def test_10_route_not_installed(self):
        out = _route.arsenal_route(self.program, "subfinder",
                                   "127.0.0.1", "-silent")
        self.assertFalse(out["ok"])
        self.assertFalse(out.get("installed", True))

    def test_11_route_fake_binary_executes(self):
        bindir = tempfile.mkdtemp()
        fake = os.path.join(bindir, "subfinder")
        with open(fake, "w") as fh:
            fh.write("#!/bin/sh\necho 'FAKE-SUBFINDER-OUTPUT'\n")
        os.chmod(fake, os.stat(fake).st_mode | stat.S_IEXEC)
        old_path = os.environ.get("PATH")
        os.environ["PATH"] = bindir + os.pathsep + (old_path or "")
        try:
            out = _route.arsenal_route(self.program, "subfinder",
                                       "127.0.0.1", "-silent")
        finally:
            os.environ["PATH"] = old_path or ""
        self.assertTrue(out["ok"])
        self.assertIn("FAKE-SUBFINDER-OUTPUT", out["output_head"])
        self.assertTrue(out["rid"].startswith("R-"))

    def test_12_route_flag_blacklist(self):
        out = _route.arsenal_route(self.program, "nmap", "127.0.0.1",
                                   "-sV --script vuln")
        self.assertFalse(out["ok"])
        self.assertIn("blocked", out["error"])

    def test_13_route_sqlmap_requires_batch(self):
        out = _route.arsenal_route(self.program, "sqlmap", "127.0.0.1",
                                   "-u http://127.0.0.1/")
        self.assertFalse(out["ok"])
        self.assertIn("--batch", out["error"])

    def test_14_route_allowlist(self):
        out = _route.arsenal_route(self.program, "metasploit", "127.0.0.1", "")
        self.assertFalse(out["ok"])
        self.assertIn("allowlist", out["error"])

    def test_15_route_scope_refused(self):
        with self.assertRaises(RuntimeError):
            _route.arsenal_route(self.program, "nmap", "192.0.2.99", "-sV")


if __name__ == "__main__":
    unittest.main()
