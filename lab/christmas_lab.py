#!/usr/bin/env python3
"""The Christmas Lab — a self-owned synthetic adversary trace, end to end.

Scenario (everything synthetic and self-owned — this file is the
authorizing artifact, exactly like lab/target_app.py):

    03:14 local. The lab's auth log shows six failed logins and one
    success against the debug console, from 10.10.4.23 — an address
    inside the lab net but unassigned in the inventory. The sensor
    fired. The Binary Brain opens the hunt.

The run drives the engine through its whole discipline:
  declare (null auto-inserted) → a deliberate attempt at the tip-off
  test (watch the gate bite) → three halving tests at exactly the
  information-theoretic floor (log2(8) = 3) → CONFIRMED through two
  independent channels → an auditor-compatible handoff pack written
  from the real ledger records.

Run from the repo root:
    MYTHOS_ARSENAL_ROOT=/tmp/christmas-lab python3 lab/christmas_lab.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arsenal import ledger, sbb  # noqa: E402

PROGRAM = "christmas-lab"
TRIGGER = ("03:14 auth log: 6 failed + 1 successful debug-console login "
           "from 10.10.4.23 (in-lab, unassigned in inventory)")

HYPOTHESES = [
    "colleague running an overnight build experiment from the office LAN",
    "decommissioned build runner still powered on with stale credentials",
    "compromised container in the build cluster",          # the truth
    "compromised office workstation",
    "remote party using leaked VPN credentials",
    "log pipeline artifact — source IP rewritten by the aggregator",
    "attacker bridged onto the office WLAN",
]

TESTS = [
    {"label": "netflow history: source talked to build control plane "
              "in the last 7 days",
     "channel": "netflow", "tip_off": False,
     "kills_one": ["compromised office workstation",
                   "remote party using leaked VPN credentials",
                   "log pipeline artifact — source IP rewritten by the aggregator",
                   "attacker bridged onto the office WLAN"],
     "kills_zero": [sbb.NULL_LABEL,
                    "colleague running an overnight build experiment from the office LAN",
                    "decommissioned build runner still powered on with stale credentials",
                    "compromised container in the build cluster"]},
    {"label": "DHCP lease origin: cluster bridge, not the office router",
     "channel": "netflow", "tip_off": False,
     "kills_one": [sbb.NULL_LABEL,
                   "colleague running an overnight build experiment from the office LAN",
                   "compromised office workstation",
                   "remote party using leaked VPN credentials",
                   "log pipeline artifact — source IP rewritten by the aggregator",
                   "attacker bridged onto the office WLAN"],
     "kills_zero": ["decommissioned build runner still powered on with stale credentials",
                    "compromised container in the build cluster"]},
    {"label": "lease client-id carries container veth MAC prefix (02:xx)",
     "channel": "host-audit", "tip_off": False,
     "kills_one": ["decommissioned build runner still powered on with stale credentials",
                   "compromised office workstation",
                   "attacker bridged onto the office WLAN"],
     "kills_zero": ["compromised container in the build cluster",
                    "colleague running an overnight build experiment from the office LAN"]},
    {"label": "credential tripwire: disable the debug-console credential, "
              "watch for re-auth",
     "channel": "identity", "tip_off": True,
     "kills_one": [sbb.NULL_LABEL,
                   "colleague running an overnight build experiment from the office LAN",
                   "decommissioned build runner still powered on with stale credentials",
                   "log pipeline artifact — source IP rewritten by the aggregator"],
     "kills_zero": ["compromised container in the build cluster",
                    "compromised office workstation",
                    "remote party using leaked VPN credentials",
                    "attacker bridged onto the office WLAN"]},
]

rids = {}


def rule(title: str) -> None:
    print("\n── %s %s" % (title, "─" * max(0, 58 - len(title))))


def main() -> int:
    print("THE CHRISTMAS LAB — a Shimomura Binary Brain run (synthetic, "
          "self-owned)")
    print("trigger: %s" % TRIGGER)

    rule("declare")
    out = sbb.declare(PROGRAM, "christmas-lab", TRIGGER, HYPOTHESES, TESTS)
    rids["declare"] = out["rid"]
    st = out["stats"]
    print("hunt opened (%s) — %d hypotheses (null auto-inserted), "
          "%d tests, floor %d"
          % (out["rid"], st["initial"], len(out["tests"]), st["floor"]))
    print("warning: %s" % out.get("warning", "none"))

    rule("decide #1")
    d = sbb.decide(PROGRAM)
    rids["prereg1"] = d["chosen"]["pre_registered_rid"]
    print("registers: %s" % d["registers"]["line"])
    print("chosen: %s (%s, %s) — %.2f bits"
          % (d["chosen"]["id"], d["chosen"]["channel"],
             "tip-off" if d["chosen"]["tip_off"] else "passive",
             d["chosen"]["bits"]))
    print("  on 1 kills: %s" % " ".join(d["chosen"]["on_1_kills"]))
    print("  on 0 kills: %s" % " ".join(d["chosen"]["on_0_kills"]))
    print("pre-registered: %s (partitions frozen before the outcome)"
          % rids["prereg1"])

    rule("the impatient move — apply the tripwire first")
    trip = sbb.apply(PROGRAM, "T-004", 1)
    rids["refused"] = trip["rid"]
    print("REFUSED (%s): %s" % (trip["rid"], trip["error"]))
    print("the adversary must not learn what we know — Rule P holds")

    rule("apply T-001 outcome=1 (netflow history exists)")
    a1 = sbb.apply(PROGRAM, "T-001", 1,
                   "netflow: 7 days of control-plane sessions from 10.10.4.23")
    rids["apply1"] = a1["rid"]
    print("eliminated: %s → active=%d (%s)"
          % (" ".join(a1["eliminated"]), a1["active_remaining"], a1["rid"]))

    rule("decide #2")
    d2 = sbb.decide(PROGRAM)
    rids["prereg2"] = d2["chosen"]["pre_registered_rid"]
    print("registers: %s" % d2["registers"]["line"])
    print("chosen: %s (%s) — %.2f bits over %d active"
          % (d2["chosen"]["id"], d2["chosen"]["channel"],
             d2["chosen"]["bits"], d2["stats"]["active"]))

    rule("apply T-002 outcome=1 (lease from the cluster bridge)")
    a2 = sbb.apply(PROGRAM, "T-002", 1,
                   "dhcpd: 10.10.4.23 renews from br-cluster (00:16:3e:aa:04:d2)")
    rids["apply2"] = a2["rid"]
    print("eliminated: %s → active=%d (%s)"
          % (" ".join(a2["eliminated"]), a2["active_remaining"], a2["rid"]))

    rule("decide #3")
    d3 = sbb.decide(PROGRAM)
    rids["prereg3"] = d3["chosen"]["pre_registered_rid"]
    print("registers: %s" % d3["registers"]["line"])
    print("chosen: %s (%s — a SECOND channel) — %.2f bits"
          % (d3["chosen"]["id"], d3["chosen"]["channel"], d3["chosen"]["bits"]))

    rule("apply T-003 outcome=1 (veth MAC prefix observed)")
    a3 = sbb.apply(PROGRAM, "T-003", 1,
                   "dhcpd client-id 02:42:ac:11:00:04 — container veth prefix")
    rids["apply3"] = a3["rid"]
    rids["confirm"] = a3["confirmed"]["rid"]
    print("eliminated: %s → active=%d (%s)"
          % (" ".join(a3["eliminated"]), a3["active_remaining"], a3["rid"]))
    print("CONFIRMED: %s — %s (%s)"
          % (a3["confirmed"]["id"], a3["confirmed"]["label"],
             a3["confirmed"]["rid"]))
    print("channels: %s (two independent channels — Rule T satisfied)"
          % ", ".join(a3["confirmed"]["channels"]))
    print("efficiency: %d tests used, floor %d — log2(8) = 3 exactly"
          % (a3["stats"]["tests_used"], a3["stats"]["floor"]))

    rule("close")
    closed = sbb.decide(PROGRAM)
    print("mode: %s — %s" % (closed["mode"], closed["next"]))

    ledger.merge(PROGRAM)
    _write_handoff(a3)
    print("\noutputs: %s/{hunt.json, HANDOFF.md, ledger/records.md}"
          % os.path.join(os.environ.get("MYTHOS_ARSENAL_ROOT", "."),
                        "engagements", PROGRAM))
    print("audit it: python3 auditor/audit_report.py <that>/HANDOFF.md")
    return 0


def _write_handoff(final: dict) -> None:
    """Write the handoff pack from the real records of this run."""
    root = os.environ.get("MYTHOS_ARSENAL_ROOT", ".")
    eng = os.path.join(root, "engagements", PROGRAM)
    survivor = final["confirmed"]
    stats = final["stats"]
    lines = []
    add = lines.append
    add("# Adversary handoff — case christmas-lab, engagement %s" % PROGRAM)
    add("")
    add("## Summary")
    add("A 03:14 debug-console login anomaly from an unassigned in-lab "
        "address opened a Binary Brain hunt of %d hypotheses "
        "(null auto-inserted). %d decisive tests at the information "
        "floor of %d localized the actor; two independent channels "
        "(netflow, host-audit) agree. %s is CONFIRMED and handed to "
        "lab IR for containment. Citations: %s, %s, %s."
        % (stats["initial"], stats["tests_used"], stats["floor"],
           survivor["label"], rids["declare"], rids["apply3"],
           rids["confirm"]))
    add("")
    add("## Timeline (from records)")
    add("| When | Record | Event |")
    add("| ---- | ------ | ----- |")
    add("| 03:14 | %s | trigger: %s |" % (rids["declare"], TRIGGER))
    add("| +0h | %s | pre-register T-001 (netflow): 1.00 bits over 8 "
        "active |" % rids["prereg1"])
    add("| +0h | %s | T-004 tripwire REFUSED — tip-off gated while "
        "passive tests eliminate |" % rids["refused"])
    add("| +0h | %s | T-001 outcome=1: netflow history exists; 4 "
        "hypotheses die |" % rids["apply1"])
    add("| +0h | %s | pre-register T-002 (netflow): 1.00 bits over 4 "
        "active |" % rids["prereg2"])
    add("| +1h | %s | T-002 outcome=1: lease renews from cluster bridge; "
        "null and colleague die |" % rids["apply2"])
    add("| +1h | %s | pre-register T-003 (host-audit): 1.00 bits over 2 "
        "active |" % rids["prereg3"])
    add("| +1h | %s | T-003 outcome=1: container veth MAC prefix; runner "
        "dies |" % rids["apply3"])
    add("| +1h | %s | %s CONFIRMED via two channels (netflow, "
        "host-audit) |" % (rids["confirm"], survivor["id"]))
    add("")
    add("## Hypotheses")
    add("")
    add("### %s %s" % (survivor["id"], survivor["label"]))
    add("Severity: high — an unauthorized actor holds valid debug-console "
        "credentials and operates from a cluster container — %s"
        % rids["confirm"])
    add("- Closure: CONFIRMED — %s, %s" % (rids["apply3"], rids["confirm"]))
    add("- Channels: netflow (%s, %s) + host-audit (%s)"
        % (rids["apply1"], rids["apply2"], rids["apply3"]))
    add("- impact-chain: stale DHCP lease on the cluster bridge → "
        "6-fail-then-success login against the debug console (%s) → "
        "authenticated debug-console access from 10.10.4.23, "
        "netflow- and host-audit-confirmed (%s, %s)"
        % (rids["declare"], rids["apply1"], rids["apply3"]))
    add("- canary: none during the trace — TIP-OFF discipline held "
        "(the tripwire attempt is the REFUSED record %s); the "
        "credential-reset tripwire is IR's containment action at "
        "handoff, scheduled and owned by IR" % rids["refused"])
    add("")
    for hid, label, killer, rec in (
            ("H-001", "authorized or benign activity (null)", "T-002", rids["apply2"]),
            ("H-002", "colleague running an overnight build experiment", "T-002", rids["apply2"]),
            ("H-003", "decommissioned build runner with stale credentials", "T-003", rids["apply3"]),
            ("H-005", "compromised office workstation", "T-001", rids["apply1"]),
            ("H-006", "remote party using leaked VPN credentials", "T-001", rids["apply1"]),
            ("H-007", "log pipeline artifact (aggregator IP rewrite)", "T-001", rids["apply1"]),
            ("H-008", "attacker bridged onto the office WLAN", "T-001", rids["apply1"])):
        add("### %s %s" % (hid, label))
        add("- Closure: FALSIFIED — eliminated by %s outcome %s (%s)"
            % (killer, "1", rec))
        add("")
    add("## Elimination table")
    add("| Hypothesis | Died on | Record |")
    add("| ---------- | ------- | ------ |")
    for hid, label, killer, rec in (
            ("H-005", "office workstation", "T-001", rids["apply1"]),
            ("H-006", "leaked VPN credentials", "T-001", rids["apply1"]),
            ("H-007", "log pipeline artifact", "T-001", rids["apply1"]),
            ("H-008", "WLAN-bridged attacker", "T-001", rids["apply1"]),
            ("H-001", "null (authorized/benign)", "T-002", rids["apply2"]),
            ("H-002", "overnight colleague", "T-002", rids["apply2"]),
            ("H-003", "stale runner", "T-003", rids["apply3"])):
        add("| %s %s | %s outcome 1 | %s |" % (hid, label, killer, rec))
    add("")
    add("## Channel matrix")
    add("| Hypothesis survived | Channel | Test | Record |")
    add("| ------------------- | ------- | ---- | ------ |")
    add("| %s | netflow | T-001 | %s |" % (survivor["id"], rids["apply1"]))
    add("| %s | netflow | T-002 | %s |" % (survivor["id"], rids["apply2"]))
    add("| %s | host-audit | T-003 | %s |" % (survivor["id"], rids["apply3"]))
    add("")
    add("## Uncertainty and leads")
    add("The hunt established WHAT and WHERE-within-our-perimeter: an "
        "actor operating from a build-cluster container holds valid "
        "debug-console credentials (%s). It did not establish identity, "
        "intent beyond the observed access, or how the container was "
        "compromised — those are leads for IR with host-image "
        "forensics. The identity-channel tripwire (T-004) stays "
        "refused-and-parked (%s): executing it is IR's containment "
        "decision, with this pack behind it." % (rids["confirm"],
                                                 rids["refused"]))
    add("")
    add("## Handoff statement")
    add("Localization inside the authorized lab perimeter is complete: "
        "%s, channels netflow (%s, %s) and host-audit (%s). Identity, "
        "anything beyond this perimeter, and every tip-off action "
        "belong to lab IR with this pack as the evidentiary basis. "
        "Efficiency: %d tests spent at a floor of %d."
        % (survivor["id"], rids["apply1"], rids["apply2"], rids["apply3"],
           stats["tests_used"], stats["floor"]))
    add("")
    path = os.path.join(eng, "HANDOFF.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("handoff pack written: %s" % path)


if __name__ == "__main__":
    sys.exit(main())
