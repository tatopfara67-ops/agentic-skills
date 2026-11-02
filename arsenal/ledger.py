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

This module is deliberately stdlib-only and lock-guarded so two
concurrent tool calls cannot mint the same R-NNN. The lock is portable:
fcntl on POSIX, msvcrt.locking on Windows, in-process-guarded elsewhere.

Id minting is O(1): record ids are strictly increasing and only ever
appended, so the maximum id always sits in the file TAIL — `_next_rid()`
reads the last few KB of each file instead of rescanning history. A
full-scan fallback fires only when the tails hold no record lines at all
(hand-written notes / corruption), and a per-process cache defeats
duplication even if a file was hand-edited mid-file. Appending record N
costs the same whether the ledger holds 50 or 50,000 records.
"""
from __future__ import annotations

import os
import re
import threading
from datetime import datetime, timezone

from . import paths

try:  # POSIX
    import fcntl
except ImportError:  # pragma: no cover — Windows / exotic
    fcntl = None
    try:
        import msvcrt
    except ImportError:  # pragma: no cover — exotic, in-process only
        msvcrt = None
else:
    msvcrt = None

TAGS = ("FACT", "SURFACE", "EXPERIMENT", "CONTROL", "CANARY",
        "PARK", "AUTH", "REFUSED", "MISTAKE")

_RID_RE = re.compile(r"^(R-(\d{3,}))\s*\|")
_LOCAL = threading.Lock()
_TAIL_WINDOW = 8192          # bytes of file tail scanned per id mint
_last_minted: dict[str, int] = {}   # dir -> highest id minted this process


class _CrossFileLock:
    """Advisory cross-process lock: fcntl (POSIX) -> msvcrt (Windows) ->
    in-process only. The threading lock is always held on top, so
    same-process concurrency is covered on every platform."""

    def __init__(self, path: str):
        self.path = path
        self.fh = None

    def __enter__(self):
        self.fh = open(self.path, "a+")
        self.fh.seek(0)
        if fcntl is not None:
            fcntl.flock(self.fh.fileno(), fcntl.LOCK_EX)
        elif msvcrt is not None:
            import time as _time
            while True:
                try:
                    msvcrt.locking(self.fh.fileno(), msvcrt.LK_LOCK, 1)
                    break
                except OSError:
                    _time.sleep(0.05)
        return self

    def __exit__(self, *exc):
        try:
            if fcntl is not None:
                fcntl.flock(self.fh.fileno(), fcntl.LOCK_UN)
            elif msvcrt is not None:
                self.fh.seek(0)
                msvcrt.locking(self.fh.fileno(), msvcrt.LK_UNLCK, 1)
        finally:
            self.fh.close()
        return False


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


def _tail_max_rid(path: str) -> int | None:
    """Highest R-NNN found in the last _TAIL_WINDOW bytes of one ledger
    file, scanning backwards — the newest record line in the window IS
    the maximum, because ids only ever increase and are only ever
    appended. O(1) regardless of ledger size. None when the tail window
    contains no record line (empty file, or a wall of hand-written
    notes sitting after the last record)."""
    try:
        size = os.path.getsize(path)
    except OSError:
        return None
    if size == 0:
        return None
    with open(path, "rb") as fh:
        if size > _TAIL_WINDOW:
            fh.seek(size - _TAIL_WINDOW)
        chunk = fh.read()
    for raw in reversed(chunk.split(b"\n")):
        m = _RID_RE.match(raw.decode("utf-8", "replace").strip())
        if m:
            return int(m.group(2))
    return None


def _next_rid(dir_: str) -> str:
    """Mint the next R-NNN in O(1): tail-scan both files (ids are
    append-monotonic), fall back to ONE full scan only when neither tail
    yields a record line, and consult the per-process cache so a mid-file
    hand edit cannot mint a duplicate within this process."""
    top = _last_minted.get(dir_, 0)
    saw_record = False
    for name in ("records.md", "append.md"):
        t = _tail_max_rid(os.path.join(dir_, name))
        if t is not None:
            saw_record = True
            top = max(top, t)
    if not saw_record:
        # tails unreadable as records — one full scan so ids can never
        # collide silently (this path never runs on a healthy ledger)
        for name in ("records.md", "append.md"):
            with open(os.path.join(dir_, name), encoding="utf-8",
                      errors="replace") as fh:
                for line in fh:
                    m = _RID_RE.match(line)
                    if m:
                        top = max(top, int(m.group(2)))
    nxt = top + 1
    _last_minted[dir_] = nxt
    return "R-%03d" % nxt


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
        with _CrossFileLock(lockpath):
            rec_id = _next_rid(dir_)
            ts = _now()
            fields = [rec_id, ts, _sanitize(tool), _sanitize(action),
                      _sanitize(result), _sanitize(size), tag, _sanitize(note)]
            line = " | ".join(fields) + "\n"
            with open(os.path.join(dir_, "append.md"), "a", encoding="utf-8") as fh:
                fh.write(line)
    return rec_id


def merge(program: str) -> int:
    """Fold append.md into records.md (call at phase boundaries). Returns
    the number of records merged."""
    dir_ = _ledger_dir(program)
    moved = 0
    with _LOCAL:
        lockpath = os.path.join(dir_, ".lock")
        with _CrossFileLock(lockpath):
            app = os.path.join(dir_, "append.md")
            rec = os.path.join(dir_, "records.md")
            with open(app, encoding="utf-8") as fh:
                fresh = fh.read()
            if fresh.strip():
                with open(rec, "a", encoding="utf-8") as fh:
                    fh.write(fresh if fresh.endswith("\n") else fresh + "\n")
                moved = sum(1 for ln in fresh.splitlines() if ln.strip())
                open(app, "w", encoding="utf-8").close()
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
