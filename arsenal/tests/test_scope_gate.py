"""Scope gate unit tests — the gate is the product; it gets its own tests."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

from arsenal.scope_gate import check_canary, check_target  # noqa: E402

SCOPE = """# comment line
127.0.0.1,in_scope,lab declaration,,,op,
example.com,in_scope,artifact-bbp,,,op,
*.stage.example.com,recon_only,artifact-bbp,,,op,
10.0.0.0/24,in_scope,artifact-lab,,,op,
bad.example.com,denied,artifact-x,,,op,
noart.lab,in_scope,,op-note,,,op,
expired.lab,in_scope,artifact-y,2020-01-01,2021-01-01,op,
hpcheck.lab:8443,in_scope,artifact-z,,,op,
https://prefixcheck.lab/private,in_scope,artifact-p,,,op,
https://mycollector.canary.io/collect,canary,operator-canary-server,,,op,
canaryhost.example.net,canary,operator-canary-server,,,op,
noart-canary.lab,canary,,,,op,
"""


class TestScopeGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "scope.csv")
        with open(self.path, "w") as fh:
            fh.write(SCOPE)

    def _check(self, target, active=True):
        return check_target(target, active=active, scope_path=self.path)

    def test_domain_suffix_match(self):
        self.assertTrue(self._check("https://www.example.com/x").authorized)
        self.assertTrue(self._check("example.com").authorized)

    def test_lookalike_not_matched(self):
        self.assertFalse(self._check("evil-example.com").authorized)
        self.assertFalse(self._check("notexample.com").authorized)

    def test_recon_only_blocks_active(self):
        res = self._check("foo.stage.example.com", active=True)
        self.assertFalse(res.authorized)
        self.assertIn("recon_only", res.reason)
        res = self._check("foo.stage.example.com", active=False)
        self.assertTrue(res.authorized)

    def test_cidr(self):
        self.assertTrue(self._check("10.0.0.55").authorized)
        self.assertFalse(self._check("10.0.1.55").authorized)

    def test_denied_row_wins(self):
        res = self._check("bad.example.com")
        self.assertFalse(res.authorized)
        self.assertIn("denied", res.reason)

    def test_missing_artifact_refused(self):
        res = self._check("noart.lab")
        self.assertFalse(res.authorized)
        self.assertIn("artifact", res.reason)

    def test_expired_refused(self):
        res = self._check("expired.lab")
        self.assertFalse(res.authorized)
        self.assertIn("expired", res.reason)

    def test_hostport_exact(self):
        self.assertTrue(self._check("hpcheck.lab:8443").authorized)
        self.assertFalse(self._check("hpcheck.lab:9999").authorized)

    def test_url_prefix(self):
        self.assertTrue(
            self._check("https://prefixcheck.lab/private/deep").authorized)
        self.assertFalse(
            self._check("https://prefixcheck.lab/public").authorized)

    def test_deny_by_default(self):
        res = self._check("https://unknown.target.org/")
        self.assertFalse(res.authorized)
        self.assertIn("deny-by-default", res.reason)

    def test_localhost_ip(self):
        self.assertTrue(self._check("http://127.0.0.1:8477/").authorized)

    # ------------------------------------------------ canary class (L1b)

    def _canary(self, target):
        return check_canary(target, scope_path=self.path)

    def test_canary_row_blocks_normal_probing(self):
        res = self._check("https://mycollector.canary.io/collect")
        self.assertFalse(res.authorized)
        self.assertIn("canary", res.reason)
        self.assertIn("http_probe(canary=True)", res.reason)

    def test_check_canary_authorizes_declared_collector(self):
        res = self._canary("https://mycollector.canary.io/collect/abc123")
        self.assertTrue(res.authorized)
        self.assertEqual(res.klass, "canary")
        self.assertIn("operator-canary-server", res.artifact)

    def test_check_canary_host_row(self):
        self.assertTrue(self._canary("https://canaryhost.example.net/x").
                        authorized)

    def test_check_canary_refuses_query_string(self):
        res = self._canary("https://mycollector.canary.io/collect?d=steal")
        self.assertFalse(res.authorized)
        self.assertIn("query", res.reason.lower())

    def test_check_canary_refuses_test_target_rows(self):
        # in_scope rows never authorize canary polls — a test target is
        # not the operator's callback collector
        res = self._canary("https://example.com/x")
        self.assertFalse(res.authorized)
        self.assertIn("canary-class", res.reason)

    def test_check_canary_refuses_undeclared_host(self):
        res = self._canary("https://evil.example.net/")
        self.assertFalse(res.authorized)

    def test_check_canary_path_slack(self):
        res = self._canary("https://mycollector.canary.io/collect/"
                           + "a" * 200)
        self.assertFalse(res.authorized)
        self.assertIn("exceeds", res.reason)

    def test_check_canary_missing_artifact_refused(self):
        res = self._canary("https://noart-canary.lab/cb")
        self.assertFalse(res.authorized)
        self.assertIn("artifact", res.reason)

    def test_check_canary_denied_wins(self):
        res = self._canary("http://bad.example.com/")
        self.assertFalse(res.authorized)
        self.assertIn("denied", res.reason)


if __name__ == "__main__":
    unittest.main()
