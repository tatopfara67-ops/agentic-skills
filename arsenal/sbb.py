"""sbb — the Shimomura Binary Brain: adversary-tracking discipline engine.

Distilled from the 1994-95 hunt that ended in Raleigh (skills/
adversary-tracker/references/history-1995.md): a tracker whose entire
mind is four binary registers —

    SIGNAL    1 = the observation deviates from a calibrated baseline
    SPLIT     1 = the next test halves the active hypothesis space
    TRUTH     1 = two independent channels agree on the survivor
    TIP-OFF   1 = the action would reveal our knowledge to the adversary

— and one loop: freeze, classify, enumerate (null first), eliminate by
halves, confirm the survivor through two channels, hand off. Observe,
never react.

Mechanical rules (refused, not advised):
  * the null hypothesis (authorized/benign activity) is declared for you;
    the boring explanation is always in the space
  * a test that cannot eliminate any active hypothesis is refused while
    more than one hypothesis is alive (Rule H — wasted bits)
  * a tip-off test is refused while any passive test still eliminates
    (Rule P — the Christmas Day discipline: watch, never warn)
  * no hypothesis reaches CONFIRMED on a single channel (Rule T — the
    1995 fix needed switch records AND radio measurements; one channel
    is one story, two channels are a location)

State lives at engagements/<program>/hunt.json (statuses only ever move
ACTIVE -> ELIMINATED / CONFIRMED, never backwards); the immutable
history lives in the ledger: every bit the brain decides writes an
R-NNN record first — EXPERIMENT pre-registrations at decide time, FACT
outcomes at apply time, REFUSED for gated actions, MISTAKE for a
falsified hypothesis space.

Stdlib only, lock-guarded (fcntl + threading) like the rest of the arsenal.
"""
from __future__ import annotations

import fcntl
import json
import math
import os
import threading
from datetime import datetime, timezone

from . import ledger, paths

_LOCK = threading.Lock()

NULL_LABEL = ("authorized or benign activity — the null hypothesis "
              "(ops automation, a colleague, a sensor artifact)")


# ------------------------------------------------------------- state I/O

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _hunt_path(program: str) -> str:
    return os.path.join(paths.program_dir(program), "hunt.json")


def _load(program: str) -> dict | None:
    path = _hunt_path(program)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _save(program: str, state: dict) -> None:
    path = _hunt_path(program)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with _LOCK:
        with open(path + ".lock", "a+") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(state, fh, indent=1, ensure_ascii=False)
                fh.write("\n")
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _require(program: str) -> dict:
    state = _load(program)
    if state is None:
        raise RuntimeError("no hunt open for %r — sbb_declare first "
                           "(a hunt opens on signal, not on curiosity)" % program)
    return state


def _next_id(prefix: str, items: list[dict]) -> str:
    top = 0
    for item in items:
        try:
            top = max(top, int(item["id"].split("-")[1]))
        except (KeyError, ValueError, IndexError):
            continue
    return "%s%03d" % (prefix, top + 1)


# ------------------------------------------------------------- helpers

def _active(state: dict) -> list[dict]:
    return [h for h in state["hypotheses"] if h["status"] == "ACTIVE"]


def _channels_for(hid: str, state: dict) -> set[str]:
    """Independent channels through which `hid` has survived so far."""
    return {t["channel"] for t in state["tests"]
            if t["status"] == "RUN" and hid not in (t.get("observed_killed") or [])}


def _bits(kills_one: list[str], kills_zero: list[str],
          active_ids: set[str]) -> float:
    """Expected information gain of one test over the active space.

    Under a uniform prior, P(outcome=1) = fraction of active hypotheses
    that survive outcome 1; the gain is the Shannon entropy of that split.
    Exactly right for fully-splitting tests (the discipline's target),
    a faithful heuristic when tests overlap."""
    n = len(active_ids)
    if n == 0:
        return 0.0
    a = len(set(kills_one) & active_ids)
    p = (n - a) / n
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))


def _registers(state: dict) -> dict:
    active = _active(state)
    active_ids = {h["id"] for h in active}
    pending = [t for t in state["tests"] if t["status"] == "PENDING"]
    truth = 0
    for h in active:
        truth = max(truth, len(_channels_for(h["id"], state)))
    armed = any(
        t.get("tip_off") and
        ((set(t["kills_one"]) | set(t["kills_zero"])) & active_ids)
        for t in pending)
    split = state.get("last_bits")
    reg = {
        "signal": 1 if state.get("trigger") else 0,
        "split_bits": split,
        "truth_channels": truth,
        "tipoff": "armed" if armed else "clear",
    }
    reg["line"] = ("SIGNAL=%d SPLIT=%s TRUTH=%dch TIP-OFF=%s"
                   % (reg["signal"],
                      ("%.2f" % split) if split is not None else "-",
                      truth, reg["tipoff"]))
    return reg


def _view(state: dict) -> dict:
    """Compact, context-cheap view of the hunt (bodies stay on disk)."""
    active = _active(state)
    used = [t for t in state["tests"] if t["status"] == "RUN"]
    initial = state.get("initial_hypotheses", len(state["hypotheses"]))
    floor = math.ceil(math.log2(initial)) if initial > 1 else 0
    eliminations = [{"id": h["id"], "label": h["label"][:70],
                     "status": h["status"], "killed_by": h.get("killed_by")}
                    for h in state["hypotheses"]]
    return {
        "case": state["case"],
        "mode": state.get("mode", "hunting"),
        "registers": _registers(state),
        "active": [{"id": h["id"], "label": h["label"][:70],
                    "channels": sorted(_channels_for(h["id"], state))}
                   for h in active],
        "tests": [{"id": t["id"], "channel": t["channel"],
                   "tip_off": bool(t.get("tip_off")), "status": t["status"],
                   "outcome": t.get("outcome")}
                  for t in state["tests"]],
        "eliminations": eliminations,
        "stats": {"initial": initial, "active": len(active),
                  "tests_used": len(used), "floor": floor},
    }


# ------------------------------------------------------------- declare

def declare(program: str, case: str, trigger: str,
            hypotheses: list[str], tests: list[dict]) -> dict:
    """Open a hunt (or extend a live one): hypotheses + discriminating tests.

    Tests are declared by LABEL:
        {"label": "...", "channel": "netflow", "tip_off": false,
         "kills_one": ["label A"], "kills_zero": ["label B"]}
    Hypotheses unlisted on a side survive that outcome. A hypothesis listed
    on both sides is unsplit by this test; listed on neither, likewise.
    The null hypothesis is inserted automatically on a fresh declare —
    do not include your own.
    """
    state = _load(program)
    fresh = state is None
    if fresh:
        state = {"case": str(case or "unnamed-case").strip() or "unnamed-case",
                 "trigger": str(trigger or "").strip(),
                 "opened": _now(), "hypotheses": [], "tests": [],
                 "log": [], "last_bits": None, "mode": "hunting"}
        state["hypotheses"].append(
            {"id": _next_id("H-", state["hypotheses"]), "label": NULL_LABEL,
             "status": "ACTIVE", "killed_by": None})

    known = {h["label"]: h["id"] for h in state["hypotheses"]}
    for raw in hypotheses:
        label = str(raw).strip()
        if not label:
            continue
        if label in known:
            raise ValueError("duplicate hypothesis label %r" % label)
        hid = _next_id("H-", state["hypotheses"])
        state["hypotheses"].append({"id": hid, "label": label,
                                    "status": "ACTIVE", "killed_by": None})
        known[label] = hid

    cleaned = []
    for raw in tests:
        label = str(raw.get("label", "")).strip()
        channel = str(raw.get("channel", "")).strip()
        if not label or not channel:
            raise ValueError("each test needs a label and a channel")
        kills_one, kills_zero = [], []
        for key, sink in (("kills_one", kills_one), ("kills_zero", kills_zero)):
            for ref in raw.get(key, []):
                ref = str(ref).strip()
                if ref not in known:
                    raise ValueError("test %r references unknown hypothesis "
                                     "%r (known: %s)"
                                     % (label, ref, ", ".join(sorted(known))))
                sink.append(known[ref])
        overlap = set(kills_one) & set(kills_zero)
        if overlap:
            dead = [h["label"] for h in state["hypotheses"]
                    if h["id"] in overlap]
            raise ValueError("test %r kills the same hypothesis on BOTH "
                             "outcomes (%s) — eliminate it explicitly or fix "
                             "the partition" % (label, ", ".join(dead)))
        cleaned.append({"label": label, "channel": channel,
                        "tip_off": bool(raw.get("tip_off", False)),
                        "kills_one": kills_one, "kills_zero": kills_zero})

    for t in cleaned:
        tid = _next_id("T-", state["tests"])
        state["tests"].append({"id": tid, "label": t["label"],
                               "channel": t["channel"], "tip_off": t["tip_off"],
                               "kills_one": t["kills_one"],
                               "kills_zero": t["kills_zero"],
                               "status": "PENDING", "outcome": None,
                               "observed_killed": []})

    if fresh:
        state["initial_hypotheses"] = len(state["hypotheses"])
        state["log"].append({"event": "declare",
                             "hypotheses": len(state["hypotheses"]),
                             "tests": len(state["tests"])})
        rid = ledger.append(program, "sbb",
                            "declare: hunt opened case=%s" % state["case"],
                            "hypotheses=%d (null auto-inserted) tests=%d"
                            % (len(state["hypotheses"]), len(state["tests"])),
                            "", "FACT", "trigger=%s" % state["trigger"][:90])
    else:
        state["log"].append({"event": "extend",
                             "hypotheses": len(hypotheses),
                             "tests": len(tests)})
        rid = ledger.append(program, "sbb",
                            "declare: hunt extended case=%s" % state["case"],
                            "+%d hypotheses +%d tests"
                            % (len(hypotheses), len(tests)),
                            "", "FACT", "null hypothesis not re-inserted")
    _save(program, state)
    out = _view(state)
    out["ok"] = True
    out["rid"] = rid
    if len({t["channel"] for t in state["tests"]}) < 2:
        out["warning"] = ("single-channel hunt: Rule T makes CONFIRMED "
                          "unreachable — declare tests on a second channel")
    return out


# ------------------------------------------------------------- decide

def decide(program: str) -> dict:
    """One Binary Brain step: registers + the max-gain test, pre-registered.

    Pre-registration happens BEFORE any outcome exists — the partitions are
    frozen in an EXPERIMENT record so the ledger can prove the test was
    designed to halve, not cherry-picked after the fact."""
    state = _require(program)
    active = _active(state)
    active_ids = {h["id"] for h in active}
    pending = [t for t in state["tests"] if t["status"] == "PENDING"]

    confirmed = [h for h in state["hypotheses"] if h["status"] == "CONFIRMED"]
    if confirmed:
        h = confirmed[0]
        state["mode"] = "closed"
        _save(program, state)
        return {"ok": True, "mode": "closed",
                "registers": _registers(state),
                "confirmed": {"id": h["id"], "label": h["label"],
                              "channels": sorted(_channels_for(h["id"], state))},
                "next": "hunt closed — write the handoff pack from ledger "
                        "records (references/evidence-templates.md)"}

    if not active:
        state["mode"] = "space-empty"
        _save(program, state)
        return {"ok": True, "mode": "space-empty",
                "registers": _registers(state),
                "next": "every hypothesis is dead — the SPACE was wrong, not "
                        "the logic. Re-enumerate (P3) with what the "
                        "eliminations taught, via sbb_declare extend."}

    if len(active) == 1:
        hid = active[0]["id"]
        channels = sorted(_channels_for(hid, state))
        state["mode"] = "singleton"
        _save(program, state)
        fresh_channel = [t for t in pending
                         if t["channel"] not in channels]
        return {"ok": True, "mode": "singleton",
                "registers": _registers(state),
                "singleton": {"id": hid, "label": active[0]["label"],
                              "channels": channels},
                "next": ("Rule T: one channel (%s) is one story — declare a "
                         "test on a second channel or the localization "
                         "claim is forbidden" % ", ".join(channels))
                        if not fresh_channel else
                        ("run the second-channel test %s (%s) to confirm"
                         % (fresh_channel[0]["id"], fresh_channel[0]["channel"]))}

    state["mode"] = "hunting"
    scored = []
    for t in pending:
        k1 = sorted(set(t["kills_one"]) & active_ids)
        k0 = sorted(set(t["kills_zero"]) & active_ids)
        scored.append({"t": t, "k1": k1, "k0": k0,
                       "bits": _bits(t["kills_one"], t["kills_zero"], active_ids)})
    if not scored:
        _save(program, state)
        return {"ok": True, "mode": "stalled",
                "registers": _registers(state),
                "next": "no pending tests — declare more via sbb_declare "
                        "(extend); the hunt is only over when |H|=1 or the "
                        "budget says stop (R7)"}

    passive_useful = [s for s in scored
                      if not s["t"].get("tip_off") and (s["k1"] or s["k0"])]
    gated = [s for s in scored
             if s["t"].get("tip_off") and (s["k1"] or s["k0"])]

    def _rank(s):
        return (-round(s["bits"], 6), 1 if s["t"].get("tip_off") else 0,
                s["t"]["id"])

    allowed = [s for s in scored
               if not (passive_useful and s["t"].get("tip_off"))]
    allowed.sort(key=_rank)
    chosen = allowed[0] if allowed else None

    view = _view(state)
    view["ok"] = True
    view["menu"] = [{"id": s["t"]["id"], "channel": s["t"]["channel"],
                     "tip_off": bool(s["t"].get("tip_off")),
                     "bits": round(s["bits"], 2)}
                    for s in sorted(scored, key=_rank)[:3]]
    if passive_useful and gated:
        view["gate"] = {"refused": [s["t"]["id"] for s in gated],
                        "reason": "tip-off tests are gated while passive "
                                  "tests still eliminate (Rule P)"}
    if chosen:
        t, k1, k0, bits = chosen["t"], chosen["k1"], chosen["k0"], chosen["bits"]
        if not t.get("prereg"):
            rid = ledger.append(
                program, "sbb",
                "decide: pre-register %s (%s, %s)"
                % (t["id"], t["channel"],
                   "tip-off" if t.get("tip_off") else "passive"),
                "on 1 kills %s / on 0 kills %s; %.2f bits over %d active"
                % (",".join(k1) or "none", ",".join(k0) or "none",
                   bits, len(active_ids)),
                "", "EXPERIMENT", "partitions frozen before the outcome")
            t["prereg"] = True
            state["last_bits"] = round(bits, 2)
            state["log"].append({"event": "decide", "test": t["id"],
                                 "bits": round(bits, 2)})
            _save(program, state)
        else:
            rid = None
        view["chosen"] = {"id": t["id"], "label": t["label"],
                          "channel": t["channel"],
                          "tip_off": bool(t.get("tip_off")),
                          "bits": round(bits, 2),
                          "on_1_kills": k1, "on_0_kills": k0,
                          "pre_registered_rid": rid}
        view["next"] = "run the test passively, then sbb_apply the observed bit"
        if t.get("tip_off"):
            view["next"] = ("passive reserves exhausted — running the tip-off "
                            "test is now a deliberate choice: record why the "
                            "reveal is acceptable, then sbb_apply")
        view["registers"] = _registers(state)  # split bit is fresh now
    else:
        view["next"] = ("only tip-off tests remain — passive reserves are "
                        "exhausted; running one is now permitted but must be "
                        "a deliberate choice, recorded as such")
    return view


# ------------------------------------------------------------- apply

def apply(program: str, test_id: str, outcome, note: str = "") -> dict:
    """Apply one observed binary outcome to its pre-registered test.

    Refuses mechanically: tip-off tests while passive eliminators remain
    (Rule P), tests that cannot eliminate while the space is plural
    (Rule H). Every application writes a FACT record; a CONFIRMED
    survivor requires two independent channels (Rule T)."""
    state = _require(program)
    test_id = str(test_id).strip().upper()
    test = next((t for t in state["tests"] if t["id"] == test_id), None)
    if test is None:
        raise ValueError("no test %r in hunt %r" % (test_id, state["case"]))
    if test["status"] != "PENDING":
        raise ValueError("test %s already ran (outcome=%s) — the ledger is "
                         "append-only; declare a new test instead"
                         % (test_id, test["outcome"]))

    if isinstance(outcome, bool):
        bit = 1 if outcome else 0
    elif isinstance(outcome, int) and outcome in (0, 1):
        bit = outcome
    else:
        text = str(outcome).strip().lower()
        if text in ("1", "true", "yes", "signal"):
            bit = 1
        elif text in ("0", "false", "no", "noise"):
            bit = 0
        else:
            raise ValueError("outcome must be binary, got %r" % outcome)

    active_ids = {h["id"] for h in state["hypotheses"]
                  if h["status"] == "ACTIVE"}
    pending = [t for t in state["tests"] if t["status"] == "PENDING"]

    if test.get("tip_off"):
        passive = [t for t in pending
                   if t is not test and not t.get("tip_off")
                   and ((set(t["kills_one"]) | set(t["kills_zero"]))
                        & active_ids)]
        if passive:
            alts = ", ".join(t["id"] for t in passive)
            rid = ledger.append(program, "sbb",
                                "apply: %s refused" % test_id,
                                "tip-off gated while passive tests eliminate "
                                "(%s)" % alts,
                                "", "REFUSED",
                                "Rule P — observe, never warn")
            state["log"].append({"event": "refuse", "test": test_id,
                                 "reason": "tip-off gated"})
            _save(program, state)
            return {"ok": False, "rid": rid,
                    "error": "tip-off test %s refused while passive tests "
                             "still eliminate: run %s first — the adversary "
                             "must not learn what you know"
                             % (test_id, alts)}

    killed = sorted((set(test["kills_one"] if bit else test["kills_zero"]))
                    & active_ids)
    if not killed and len(active_ids) > 1:
        rid = ledger.append(program, "sbb",
                            "apply: %s refused" % test_id,
                            "outcome=%d eliminates no active hypothesis"
                            % bit,
                            "", "REFUSED",
                            "Rule H — a test that cannot change beliefs is "
                            "wasted budget")
        state["log"].append({"event": "refuse", "test": test_id,
                             "reason": "zero bits available"})
        _save(program, state)
        return {"ok": False, "rid": rid,
                "error": "Rule H: test %s cannot eliminate any active "
                         "hypothesis — redesign the partition (halving, "
                         "not noise)" % test_id}

    for h in state["hypotheses"]:
        if h["id"] in killed:
            h["status"] = "ELIMINATED"
            h["killed_by"] = test_id
    test["status"] = "RUN"
    test["outcome"] = bit
    test["observed_killed"] = killed

    remaining = active_ids - set(killed)
    rid = ledger.append(program, "sbb",
                        "apply: %s outcome=%d" % (test_id, bit),
                        "eliminated %s; active=%d"
                        % (",".join(killed) or "none", len(remaining)),
                        "", "FACT", note)

    out = {"ok": True, "rid": rid, "test": test_id, "outcome": bit,
           "eliminated": killed, "active_remaining": len(remaining)}

    if len(remaining) == 1:
        hid = next(iter(remaining))
        hyp = next(h for h in state["hypotheses"] if h["id"] == hid)
        channels = sorted(_channels_for(hid, state))
        if len(channels) >= 2:
            hyp["status"] = "CONFIRMED"
            used = sum(1 for t in state["tests"] if t["status"] == "RUN")
            floor = math.ceil(math.log2(state.get("initial_hypotheses", 2))) \
                if state.get("initial_hypotheses", 1) > 1 else 0
            crid = ledger.append(
                program, "sbb", "confirm: %s" % hid,
                "CONFIRMED via two channels (%s); tests used %d, floor %d"
                % (", ".join(channels), used, floor),
                "", "FACT", "%s — rule T satisfied" % hyp["label"][:80])
            state["log"].append({"event": "confirm", "hyp": hid,
                                 "channels": channels})
            state["mode"] = "closed"
            out["confirmed"] = {"id": hid, "label": hyp["label"],
                                "channels": channels, "rid": crid}
        else:
            state["mode"] = "singleton"
            state["log"].append({"event": "singleton", "hyp": hid,
                                 "channels": channels})
            out["singleton"] = {"id": hid, "label": hyp["label"],
                                "channels": channels}
            out["next"] = ("single channel (%s) — Rule T: declare a "
                           "second-channel test before any localization "
                           "claim" % ", ".join(channels))
    elif not remaining:
        state["mode"] = "space-empty"
        state["log"].append({"event": "space-empty"})
        ledger.append(program, "sbb", "apply: %s outcome=%d" % (test_id, bit),
                      "hypothesis space falsified — all eliminated",
                      "", "MISTAKE",
                      "re-enumerate (P3); the space was wrong, not the logic")
        out["next"] = ("space empty — every hypothesis is dead. This is a "
                       "recorded MISTAKE, not a failure: re-enumerate with "
                       "what the eliminations taught")
    else:
        state["mode"] = "hunting"
        state["log"].append({"event": "apply", "test": test_id,
                             "killed": killed})

    _save(program, state)
    out["registers"] = _registers(state)
    out["stats"] = _view(state)["stats"]
    return out
