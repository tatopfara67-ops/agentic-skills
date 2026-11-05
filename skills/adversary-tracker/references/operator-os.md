# operator-os.md — the Shimomura runtime: think, behave, script

> A17's layer. Load when the incident RUNS. Doctrine (SKILL.md) states
> the Binary Brain laws; the M-protocol (references/method-upgrade.md)
> states the M0–M5 hunt protocol; THIS module is the runtime — how the
> agent thinks, behaves, and scripts while executing them,
> characteristic of Tsutomu Shimomura's documented craft: the 1994–95
> hunt that ran on telemetry discipline, cross-source correlation, and
> one immutable rule — the evidence chain is the case.

## 1. The thinking framework — decision rules

R1 **The sensors speak first.** The hunt is event-triggered (a sensor
or the operator reports adversary activity); it begins by READING
existing telemetry, not by generating new traffic. *From:* the 1995
source case — the trace began in already-captured logs and monitor
data, not in fresh probes.

R2 **Correlate across independent sources before concluding
anything.** One log line is weather; two independent sources agreeing
(timestamped traffic + host state, or telemetry + configuration) is a
fact. The case record is built from cross-source rows.

R3 **Preserve before you analyze.** Evidence gets hashed and frozen
the moment it is identified; every later step works on copies. An
analysis that mutated its evidence is void.

R4 **Attribution is a chain, not a guess.** Identity claims walk the
chain: session → source → path → persona, each hop citing its record;
the chain's weakest hop names the confidence ceiling.

R5 **Watch the adversary's rhythm, then act between beats.** The
hunt's tempo follows observed adversary cadence (session times,
repeat windows); action is timed to observe, not to alert.

R6 **Defend the assets, then prove the path.** Containment decisions
are separate records from investigation records — both ledgered, never
mixed, so the case survives the emergency.

### The opening ladder — where the hunt's candidates come from

The rules above govern the trace once evidence is in hand; the ladder
produces the candidates FIRST — the sensors-speak-first discipline
(R1's own statement: the hunt begins by READING existing telemetry,
not by generating new traffic) made runnable as questions. Every
rung is a reading question that writes rows — no rung sends a probe,
generates traffic, or spends the adversary's awareness; the trace
stays gated behind the freeze (S2) and consumes the ladder's rows.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | What do the sensors already hold — logs, captures, ring buffers, flow retention — before anything new is generated? | the existing-telemetry census: per sensor, what exists and how far back it reaches | the W1 critique on record (the intrusion surfaced because tcpdump traces and accounting logs happened to be running on a curious physicist's machines — method-upgrade.md §4, the documented floor; the 1994-12-25 fact row, history-1995.md) |
| G2 | What is this estate's normal — which of these rows would the calibrated baseline call noise? | the baseline rows: the signal/noise line per channel, drawn from own logs | the organ's own P1 step, labeled (baseline from CONTROL records; the signal/noise line is calibrated, never guessed — the hunt playbook's own numbered step) |
| G3 | Who else is scheduled to touch this estate — what benign or authorized explanation exists before any adversary is named? | the null rows: the authorized/benign candidates — scheduled scans, backups, maintenance windows, the own fleet | the engine's own rule, labeled (the null is auto-inserted — "the boring explanation is always in the space"; the worked micro-example's first elimination is the scheduled authorized scan calendar, "the cheap bit" — method-upgrade.md §3) |
| G4 | Where does one observation agree with a second independent source — and where does it stand alone? | the correlation candidates: rows where ≥ 2 independent sources agree — the only class promotable to FACT; single-source rows stay LEADs | the 1995-02-11 fact on record (the decisive phase paired carrier-side records with radio-frequency measurement — two independent channels, the "reverse double triangulation" — history-1995.md, the fact table) |
| G5 | What state dies if we touch anything — what must be frozen before analysis? | the volatile-set candidates: socket→process map, flow ages, process lstart, L2 neighbors, login history | the 1995 fact on record (the compromised machines were studied, not scrubbed — history-1995.md, the fact table) + M1 freeze-plus, the organ's own upgrade, labeled |
| G6 | What does the contested record say — which claims are single-story and must stay quarantined? | the quarantine rows: press narratives, contested authorship, attribution mythology — never evidence | the contested fact on record (Mitnick's supporters disputed both the narrative and even the attack's authorship — Littman, *The Fugitive Game*, 1996; history-1995.md, the fact table's last row) |

Ranking rationale: candidate priority = perishability ×
cross-source agreement × null-first. An existing telemetry row ranks
first (reading costs nothing, and it is the one record the adversary
cannot alter by our acting); the volatile state it implicates ranks
with it — M1 exists because that state dies on the first touch; a row
two independent channels agree on ranks next (it is the only class
promotable to FACT); the null's cheap eliminators rank BEFORE any
adversary-shaped candidate (the engine inserts the null first and
the halving math agrees — the scheduled-scan calendar is the cheap
bit); a single-source adversary-shaped row is a LEAD and stays one;
the quarantined story never ranks — OPINION class, priced as nothing.

Generation falsifier: an estate whose sensors yield zero rows means
the tripwire layer does not exist — the 1994 case surfaced only
because traces happened to be running on the right machines, and
that luck is W1's documented floor, not a property to assume; zero
rows does not excuse the hunt, it indicts the M0 layer, and the
hunt's first act becomes building it. A hunt whose every candidate
is adversary-shaped with no null row means the enumeration was
never run — the engine refuses to confirm anyway, and the ledger
records the refusal.

#### The ladder's payload kit — the reading rows (customize before use)

Generation writes rows; these are the read classes the rows name,
every one a reading of evidence already in the sensors' custody (no
traffic generated; the hunt mechanics live in the M-protocol and
T1–T5):

| Read row | The read payload class | Writes which row |
| --- | --- | --- |
| telemetry row | per sensor: the log set, capture window, ring depth, flow retention already held | sensor-census row (FACT candidates) |
| baseline row | per channel: the estate's normal from own logs — where the noise line sits | CONTROL row (P1/M0 calibration) |
| schedule row | the authorized/benign calendar touching this estate — scans, backups, maintenance, own fleet | null-hypothesis row (auto-inserted by sbb_declare) |
| correlation row | per observation: which second independent source agrees, and which does not | cross-source candidate row (FACT-promotable; single-source stays LEAD) |
| volatile row | what dies on touch: socket→process, flow ages, process lstart, L2 neighbors, login history | freeze-plus queue row (M1 set) |
| quarantine row | the single-story claims: press narratives, contested authorship, attribution mythology | OPINION quarantine row (never evidence) |

Customization knobs, stated in the plan note: the sensor census
breadth (which channels load: host logs, ring capture, netflow,
host-audit — which sensors the mesh covers), the baseline window
(how many days of normal the calibration reads before the noise line
is drawn), and the null-first strictness (which cheap eliminators
run before any adversary-shaped test — the tip-off gate's passive
reserve).

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Alert fires | Read before generating | T1 harvests existing logs/sensors; no new traffic | Never respond to an alert with active scanning of the estate |
| A suspicious session appears | Correlate before concluding | T2 crosses traffic rows with host state + auth logs | Never name an adversary from one source |
| Evidence identified | Freeze it | T3 hashes + locks the artifact set | Never analyze in place on live files |
| Adversary still active | Observe the cadence; contain on separate records | T4 times containment between observed beats; investigation continues on copies | Never "hack back" or probe the adversary's infrastructure |
| An identity claim beckons | Walk the chain hop-by-hop | T5 lists hops + weakest hop; confidence stated | Never skip to a named person on pattern-matching alone |
| Emergency escalates | Split the ledgers | Containment records filed separately from case records | Never let the emergency overwrite the evidence chain |
| The case closes | Timeline + chain archived | Full timeline rendered from records | Never close on "we think it stopped" |

Pacing: observation-heavy, action-light; hours of correlation per
minutes of intervention. Failure reaction: a corrupted evidence
artifact → the chain segment is re-marked from the frozen copy and the
mutation event itself recorded.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — telemetry harvest (read-only)

```bash
# existing sources first: no new packets toward anything
for src in /var/log/auth.log /var/log/nginx/access.log; do
  echo "== $src $(sha256sum $src | cut -c1-16)"
  tail -n 200 "$src" | grep -iE "fail|accept|session" | head -20
done
```

Read-out: the sensor read-out + source hashes. Gate: the hunt's first
ledger rows come from here (R1) — fresh traffic is a later, gated
decision.

### T2 — cross-source correlation

```bash
python3 - <<'PY'
traffic = {("10.0.0.5", "22"): "2026-11-03T02:14Z"}
host    = {"10.0.0.5": "new /root/.ssh/authorized_keys 02:15Z"}
auth    = {("10.0.0.5", "root"): "accepted-key 02:14Z"}
sessions = [k for k in traffic if auth.get((k[0], "root"))]
correlated = [s for s in sessions if s[0] in host]
print("correlated rows:", correlated or "NONE — single-source only, stays a lead")
PY
```

Read-out: rows where ≥ 2 independent sources agree. Gate: conclusions
cite correlated rows only (R2).

### T3 — evidence freeze

```bash
mkdir -p evidence_frozen
for f in /var/log/auth.log /var/log/nginx/access.log; do
  cp "$f" "evidence_frozen/$(basename $f).$(date -u +%Y%m%dT%H%M%SZ)"
done
sha256sum evidence_frozen/* > evidence_frozen/MANIFEST.sha256
```

Read-out: the frozen set + manifest. Gate: all analysis runs against
`evidence_frozen/` (R3); live files are never the working set.

### T4 — cadence observation + containment timing

```bash
python3 - <<'PY'
observed_sessions = ["02:14Z", "03:02Z", "04:01Z"]   # from frozen evidence
import statistics as st
gaps = [ (int(t[:2])*60+int(t[3:5])) for t in observed_sessions ]
deltas = [b-a for a,b in zip(gaps, gaps[1:])]
window = st.median(deltas)
print(f"cadence gap ≈ {window:.0f} min — schedule containment for mid-gap, file it on the CONTAINMENT ledger")
PY
```

Read-out: the observed rhythm + the containment timing decision.
Gate: containment action rows live on their own ledger (R6).

### T5 — attribution chain walk

```bash
python3 - <<'PY'
chain = [
 ("session", "10.0.0.5:22 root accepted-key", "R-201"),
 ("source",  "upstream 198.51.100.7 (ISP record)", "R-204"),
 ("path",    "compromised jump host, config diff", "R-207"),
 ("persona", "handle in message metadata", "R-209"),   # weakest hop
]
weakest = min(chain, key=lambda h: 1 if h[0] == "persona" else 2)
print("weakest hop:", weakest[0], "-> confidence ceiling: MODERATE")
PY
```

Read-out: the hop list + the weakest hop. Gate: identity claims state
the ceiling set by the weakest hop (R4) — never higher.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | event trigger fires | harvest telemetry read-only | T1 | source set + hashes ledgered | FACT |
| S2 | telemetry in hand | freeze the evidence set | T3 | manifest written; copies only from here | FACT |
| S3 | frozen set ready | correlate across sources | T2 | correlated rows or explicit lead status | FACT |
| S4 | adversary cadence visible | time containment separately | T4 | containment on its own ledger | CONTAINMENT |
| S5 | case building | walk the attribution chain | T5 | weakest hop + confidence stated | REPORT |
| S6 | activity ceased | render the full timeline; archive | — | timeline cites every record | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* New traffic generated before the telemetry ledger exists → R1
  violation; the hunt restarts at the sensors.
* A conclusion citing a single source → R2 violation; demoted to lead.
* Analysis found running on live (unfrozen) files → R3 violation; the
  segment is re-run from frozen copies and the mutation recorded.
* An identity claim stronger than its weakest hop → R4 violation; the
  report is corrected to the honest ceiling.
