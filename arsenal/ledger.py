"""Append-only evidence ledger — the L5 chain-of-custody primitive.

One record per observation, single pipe-separated line:

    R-041 | 2026-11-01T08:12:44Z | curl | GET /admin | 307 loc=/login | 412B | EXPERIMENT | baseline run 1/3, H-001

Storage per engagement (program):
    engagements/<program>/ledger/records.md   merged, canonical
    engagements/<program>/ledger/append.md    fresh records, merged at
                                              phase boundaries

Discipline (inherited from the mythos-bug-hunter spine, §2–§3):
  * append-only: nothing ever edits or renumbers a record once written
  * interpretation never edits records — it adds new records citing old ones
  * the report is written ONLY from records; not in the ledger = not in the
    report
  * the "|" field separator is protected: pipes in field values become "/"

This module is deliberately stdlib-only and lock-guarded (fcntl) so two
concurrent tool calls cannot mint the same R-NNN.
"""
from __future__ import annotations

import fcntl
import os
import re
import threading
from datetime import datetime, timezone

from . import paths

TAGS = ("FACT", "SURFACE", "EXPERIMENT", "CONTROL", "CANARY",
        "PARK", "AUTH", "REFUSED", "MISTAKE")

_RID_RE = re.compile(r"^(R-(\d{3,}))\s*\|")
_LOCAL = threading.Lock()


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sanitize(value: str) -> str:
    value = str(value).replace("|", "/").replace("\n", " ").replace("\r", " ")
    return value.strip()


def _ledger_dir(program: str) -> str:
    d = os.path.join(paths.program_dir(program), "ledger")
    os.makedirs(d, exist_ok=True)
    for name in ("records.md", "append.md"):
        p = os.path.join(d, name)
        if not os.path.exists(p):
            open(p, "a", encoding="utf-8").close()
    return d


def _next_rid(dir_: str, lock: int) -> str:
    top = 0
    for name in ("records.md", "append.md"):
        with open(os.path.join(dir_, name), encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = _RID_RE.match(line)
                if m:
                    top = max(top, int(m.group(2)))
    return "R-%03d" % (top + 1)


def append(program: str, tool: str, action: str, result: str,
           size: str | int = "", tag: str = "FACT", note: str = "") -> str:
    """Append one record; returns its R-NNN id. Never edits history."""
    if tag not in TAGS:
        raise ValueError("tag %r not in %s" % (tag, TAGS))
    dir_ = _ledger_dir(program)
    rec_id = None
    line = None
    with _LOCAL:
        lockpath = os.path.join(dir_, ".lock")
        with open(lockpath, "a+") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            rec_id = _next_rid(dir_, lock)
            ts = _now()
            fields = [rec_id, ts, _sanitize(tool), _sanitize(action),
                      _sanitize(result), _sanitize(size), tag, _sanitize(note)]
            line = " | ".join(fields) + "\n"
            with open(os.path.join(dir_, "append.md"), "a", encoding="utf-8") as fh:
                fh.write(line)
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    return rec_id


def merge(program: str) -> int:
    """Fold append.md into records.md (call at phase boundaries). Returns
    the number of records merged."""
    dir_ = _ledger_dir(program)
    moved = 0
    with _LOCAL:
        lockpath = os.path.join(dir_, ".lock")
        with open(lockpath, "a+") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            app = os.path.join(dir_, "append.md")
            rec = os.path.join(dir_, "records.md")
            with open(app, encoding="utf-8") as fh:
                fresh = fh.read()
            if fresh.strip():
                with open(rec, "a", encoding="utf-8") as fh:
                    fh.write(fresh if fresh.endswith("\n") else fresh + "\n")
                moved = sum(1 for ln in fresh.splitlines() if ln.strip())
                open(app, "w", encoding="utf-8").close()
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    return moved


def _iter_records(program: str):
    dir_ = _ledger_dir(program)
    seen = set()
    for name in ("records.md", "append.md"):
        with open(os.path.join(dir_, name), encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                m = _RID_RE.match(line)
                if not m or m.group(1) in seen:
                    continue
                seen.add(m.group(1))
                yield m.group(1), line


def summary(program: str, limit: int = 0) -> list[dict]:
    """Compact in-context view: record id + one-line gist only (§3)."""
    out = []
    for rid, line in _iter_records(program):
        parts = [p.strip() for p in line.split("|")]
        gist = "%s %s %s" % (parts[2] if len(parts) > 2 else "",
                             parts[3] if len(parts) > 3 else "",
                             parts[4] if len(parts) > 4 else "")
        out.append({"id": rid, "tag": parts[6] if len(parts) > 6 else "",
                    "gist": gist[:110]})
    return out if not limit else out[-limit:]


def read(program: str, rid: str) -> str:
    """Full record detail, re-read from disk exactly when needed (§3)."""
    rid = rid.strip()
    for rec_id, line in _iter_records(program):
        if rec_id == rid:
            return line
    raise KeyError("no ledger record %s in engagement %r" % (rid, program))


def count(program: str) -> int:
    return sum(1 for _ in _iter_records(program))


def exists(program: str, rid: str) -> bool:
    try:
        read(program, rid)
        return True
    except KeyError:
        return False
