"""hypotheses — the Hypothesis Contract (spine §5) as executable discipline.

Pre-registration is the spine's most distinctive mechanism and, until
v4.7.0, its least enforced: the report auditor checked Closure lines at
Phase 5, but nothing at hunt time refused a hypothesis written after its
own confirming response. House rule: a rule nobody verifies is decoration.
This module is the decoration removed.

State lives at engagements/<program>/hypotheses.jsonl — append-only
rows, one JSON object per line, last row per id wins (the documented L8
format). Canonical row (the §5 five slots + the L3 operational fields):

    {"id": "H-014", "surface": "...", "obs": "...", "claim": "...",
     "pred": "...", "falsifier": "...", "prior": 0.35,
     "prior_basis": "...", "facts": ["R-041", "R-042"], "cue": "C2",
     "status": "open", "registered": "<iso>", "record": "R-015"}

Closure appends a new row for the same id — history is never edited,
statuses never move backwards. Reviving a falsified hypothesis with new
evidence is a NEW id citing the dead one (the L3 revival rule, kept
append-only).

Mechanical refusals (doctrine, not advice):
  * register refuses motivating facts that are not existing R-NNN
    ledger records — registration without evidence is structurally
    impossible (R4)
  * register refuses a prior outside (0,1) — priors are starting
    points, not verdicts — and a missing base-rate justification
  * register refuses a malformed cue id (C<int>, the §32.10 catalog)
  * close accepts CONFIRMED / FALSIFIED / INCONCLUSIVE only (§7)
  * close requires the closure to cite existing evidence R-NNN records
  * close refuses INCONCLUSIVE without a cited Park record (§7)
  * close refuses CONFIRMED when EXPERIMENT records citing the
    hypothesis predate its registration — retrodiction is discarded
    (§5 rule 1). The guard matches EXPERIMENT-tagged records that cite
    the H-id; experiments that never cited the hypothesis are the
    report auditor's problem at Phase 5.
  * close refuses a second closure — revival is a new hypothesis

Every state change writes a ledger record first (audit trail, sbb
precedent): tag HYPOTHESIS at registration, tag CLOSURE at verdict.
Stdlib only, lock-guarded (fcntl + threading) like the rest of the
arsenal. Id minting is O(n) over the jsonl — engagements carry dozens
of hypotheses, not thousands; the ledger's tail-window craft is not
needed here.
"""
from __future__ import annotations

import fcntl
import json
import os
import re
import threading

from . import ledger, paths

_LOCK = threading.Lock()

STATES = ("CONFIRMED", "FALSIFIED", "INCONCLUSIVE")
_OPEN = "open"
_CLOSED = {s.lower(): s for s in STATES}

_RID_RE = re.compile(r"^R-\d{3,}$")
_HID_RE = re.compile(r"^H-(\d{3,})$")
_CUE_RE = re.compile(r"^C\d+$")
_HREF_RE = re.compile(r"\bH-\d{3,}\b")
_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _path(program: str) -> str:
    return os.path.join(paths.program_dir(program), "hypotheses.jsonl")


def _fold(program: str) -> dict[str, dict]:
    """All rows folded by id — the last row per id wins. Malformed lines
    are skipped (hand-edited notes tolerated, never trusted)."""
    path = _path(program)
    rows: dict[str, dict] = {}
    if not os.path.isfile(path):
        return rows
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            hid = row.get("id", "")
            if _HID_RE.match(str(hid)):
                rows[str(hid)] = row
    return rows


def _next_id(rows: dict[str, dict]) -> str:
    top = 0
    for hid in rows:
        m = _HID_RE.match(hid)
        if m:
            top = max(top, int(m.group(1)))
    return "H-%03d" % (top + 1)


def _append_row(program: str, row: dict) -> None:
    path = _path(program)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _check_text(field: str, value: str) -> str:
    value = str(value).strip()
    if not value:
        raise ValueError("%s is required — the contract has no empty slots" % field)
    return value


def register(program: str, surface: str, obs: str, claim: str, pred: str,
             falsifier: str, prior: float, prior_basis: str,
             facts: list[str], cue: str = "") -> dict:
    """Register one hypothesis (the §5 block, before the first crafted
    payload). Returns {"id", "record", "status": "open"}."""
    surface = _check_text("surface", surface)
    obs = _check_text("obs", obs)
    claim = _check_text("claim", claim)
    pred = _check_text("pred", pred)
    falsifier = _check_text("falsifier", falsifier)
    prior_basis = _check_text("prior_basis", prior_basis)
    try:
        prior = float(prior)
    except (TypeError, ValueError):
        raise ValueError("prior must be a number in (0,1)")
    if not 0.0 < prior < 1.0:
        raise ValueError("prior %r outside (0,1) — priors are starting "
                         "points, not verdicts" % prior)
    if not facts:
        raise ValueError("facts is required — a hypothesis must cite the "
                         "R-NNN records that motivate it (R4)")
    seen: list[str] = []
    for rid in facts:
        rid = str(rid).strip()
        if not _RID_RE.match(rid):
            raise ValueError("fact %r is not an R-NNN id" % rid)
        if rid not in seen:
            seen.append(rid)
        if not ledger.exists(program, rid):
            raise ValueError("fact %s is not in the ledger — registration "
                             "without evidence is structurally impossible" % rid)
    cue = (cue or "").strip()
    if cue and not _CUE_RE.match(cue):
        raise ValueError("cue %r is not a C-id (§32.10 catalog, e.g. C2)" % cue)

    with _LOCK:
        path = _path(program)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path + ".lock", "a+") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            try:
                rows = _fold(program)
                hid = _next_id(rows)
                ts = _now()
                rec = ledger.append(
                    program, "hypothesis_register", "%s %s" % (hid, surface),
                    claim[:110], "", "HYPOTHESIS",
                    "facts %s · prior %d%% — %s · falsifier %s · pred %s · "
                    "obs %s%s" % (",".join(seen), round(prior * 100),
                                  prior_basis, falsifier, pred, obs,
                                  " · cue " + cue if cue else ""))
                row = {"id": hid, "surface": surface, "obs": obs,
                       "claim": claim, "pred": pred, "falsifier": falsifier,
                       "prior": prior, "prior_basis": prior_basis,
                       "facts": seen, "cue": cue, "status": _OPEN,
                       "registered": ts, "record": rec}
                _append_row(program, row)
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    return {"id": hid, "record": rec, "status": _OPEN}


def _retrodictions(program: str, hid: str, registered: str) -> list[str]:
    """EXPERIMENT-tagged ledger records citing this H-id whose timestamp
    predates the hypothesis registration — the retrodiction smell."""
    if not _TS_RE.match(registered):
        return []
    found = []
    for rid, line in ledger._iter_records(program):
        parts = [p.strip() for p in line.split(" | ")]
        if len(parts) < 7 or parts[6] != "EXPERIMENT":
            continue
        if hid in _HREF_RE.findall(line) and parts[1] < registered:
            found.append(rid)
    return found


def close(program: str, hid: str, state: str, evidence: list[str],
          note: str = "") -> dict:
    """Close one hypothesis (§7 three states only). Refusals: see module
    docstring. Returns {"id", "state", "record", "prior", "calibration"}."""
    hid = str(hid).strip()
    if not _HID_RE.match(hid):
        raise ValueError("hypothesis id %r is not an H-NNN id" % hid)
    state = str(state).strip().upper()
    if state not in STATES:
        raise ValueError("state %r is not one of %s — the closure vocabulary "
                         "has three states only" % (state, "/".join(STATES)))
    if not evidence:
        raise ValueError("evidence is required — a closure cites the R-NNN "
                         "records that decided it")
    cited: list[str] = []
    for rid in evidence:
        rid = str(rid).strip()
        if not _RID_RE.match(rid):
            raise ValueError("evidence %r is not an R-NNN id" % rid)
        if rid not in cited:
            cited.append(rid)
        if not ledger.exists(program, rid):
            raise ValueError("evidence %s is not in the ledger" % rid)

    with _LOCK:
        path = _path(program)
        with open(path + ".lock", "a+") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            try:
                rows = _fold(program)
                if hid not in rows:
                    raise KeyError("no hypothesis %s in engagement %r"
                                   % (hid, program))
                row = rows[hid]
                if row.get("status") != _OPEN:
                    raise ValueError("%s is already %s — closure is "
                                     "append-only; revival is a new "
                                     "hypothesis citing the dead one"
                                     % (hid, row.get("status")))
                if state == "INCONCLUSIVE":
                    parked = False
                    for rid in cited:
                        line = ledger.read(program, rid)
                        parts = [p.strip() for p in line.split(" | ")]
                        if len(parts) > 6 and parts[6] == "PARK":
                            parked = True
                            break
                    if not parked:
                        raise ValueError("INCONCLUSIVE requires a cited Park "
                                         "record — the resume point is the "
                                         "closure, not a shrug")
                suspect = _retrodictions(program, hid,
                                         str(row.get("registered", "")))
                if state == "CONFIRMED" and suspect:
                    raise ValueError(
                        "retrodiction discarded: EXPERIMENT record(s) %s cite "
                        "%s before its registration — re-register the "
                        "hypothesis and re-run" % (",".join(suspect), hid))
                rec = ledger.append(
                    program, "hypothesis_close", hid, state, "", "CLOSURE",
                    "evidence %s%s" % (",".join(cited),
                                       " · " + note.strip() if note.strip()
                                       else ""))
                prior = row.get("prior", 0.5)
                if state == "FALSIFIED" and prior >= 0.5:
                    calib = "overconfident prior — mistake-ledger candidate (§12)"
                elif state == "CONFIRMED" and prior <= 0.3:
                    calib = "surprise confirm — re-derive the base rate " \
                            "before the next hypothesis on this class"
                else:
                    calib = "as expected"
                closed = dict(row)
                closed["status"] = state.lower()
                closed["closure"] = {"state": state, "evidence": cited,
                                     "note": note.strip(), "record": rec,
                                     "closed": _now()}
                _append_row(program, closed)
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    out = {"id": hid, "state": state, "record": rec, "prior": prior,
           "calibration": calib}
    if suspect and state != "CONFIRMED":
        out["retrodiction_warning"] = (
            "EXPERIMENT record(s) %s cite %s before its registration — "
            "closure allowed, but the run order was not clean"
            % (",".join(suspect), hid))
    return out


def summary(program: str, status: str = "") -> dict:
    """Folded view: counts per state + compact rows. status filters
    (open / confirmed / falsified / inconclusive). The open set is the
    Phase-4 entry gate — it must be empty before impact proofs."""
    rows = _fold(program)
    counts = {"open": 0, "confirmed": 0, "falsified": 0, "inconclusive": 0}
    for row in rows.values():
        st = str(row.get("status", _OPEN))
        counts[st if st in counts else "open"] += 1
    want = (status or "").strip().lower()
    if want and want not in counts:
        raise ValueError("status filter %r is not one of %s"
                         % (status, "/".join(sorted(counts))))
    out = []
    for hid in sorted(rows, key=lambda h: int(_HID_RE.match(h).group(1))):
        row = rows[hid]
        st = str(row.get("status", _OPEN))
        if want and st != want:
            continue
        out.append({"id": hid, "surface": str(row.get("surface", ""))[:60],
                    "claim": str(row.get("claim", ""))[:80],
                    "prior": row.get("prior"), "status": st})
    return {"counts": counts, "rows": out}
