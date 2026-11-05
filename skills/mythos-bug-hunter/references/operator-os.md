# The operator runtime — the onboarding-preservation layer (R1–R6, T1–T5, S1–S6)

> Part of **mythos-bug-hunter v4.8.0** (package architecture).
> **Load when:** onboarding runs, engagement start (the PIN step),
> version bumps, drift audits, newcomer first-runs. The method layer
> this runtime executes lives in
> [`method-upgrade.md`](method-upgrade.md); the provenance in
> [`sources.md`](sources.md). This is the A17 runtime of the Jason
> Haddix lineage layer — the spine's first operator-os module,
> scoped to the onboarding path.

## 1. The thinking framework — decision rules

The lineage's documented heuristics, stated as rules the operator
runs mechanically:

* **R1 — pin before first request.** The corpus state is pinned (M1)
  before any non-recon request joins the state. An unpinned engagement
  is an unverifiable engagement: no diff can name what changed
  mid-run, and no audit can name which version of the doctrine
  produced the finding.
* **R2 — curation rows are claims, not facts.** Every era-stamped
  tool row is re-verified (existence, behavior, paywall) at first use
  in an era — the corpus's own rot record (the Twitter-API workflow
  died, WPscan went paid, the eight-year-old XSS methodology aged
  out) is the evidence that curation rots on a different clock than
  doctrine.
* **R3 — scanner and AI output is hypothesis.** "You will always have
  to prove out the vulnerability that any of these scanners finds for
  you" — and the AI form: dataset cutoffs are stated, model guesses
  are verified against primary artifacts before repeating them. This
  is spine R5 extended to the onboarding path, in the lineage's own
  words.
* **R4 — route, don't re-teach.** Where a task needs foundations,
  point at the canonical source instead of re-teaching it badly
  ("Many people can teach `';alert('xss');//` — less people teach
  where to look"). Onboarding artifacts state what they are NOT —
  the honest scoping the corpus itself models.
* **R5 — templates carry a verification step.** "Nothing will get a
  bug invalidated faster than stating the wrong domain or URLs in a
  report" — mechanically: every templated report field re-derives
  target-specific values from the ledger, never from the template
  as-stored; the template ships with its re-derivation checklist.
* **R6 — tiers are opinions with a correction path.** "These are just
  my opinions based on heavy use & could be wrong. I want to learn!"
  — mechanically: tier claims (S/A/B/C and any ranking) are priors
  with named basis; corrections enter the ledger as records, never as
  silent edits; a tier flip without a ledger record is a defect.

### The opening ladder — where the onboarding questions come from

The rules above preserve the methodology once the engagement runs;
the ladder produces the questions FIRST — the lineage's own opening
act, made runnable: the corpus read as an estate before anything is
pinned (nine years, six carriers, a version chain that re-forges
fast, and a documented rot record — the onboarding surface is
already rich before a single preservation row exists). Every rung is
a reading question that writes preservation rows — no rung sends a
request, gates a newcomer, or adopts a bump; generation never spends
the engagement's state. The S1–S6 order stays behind the ladder and
consumes its rows.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | What version of every loaded artifact answers this engagement — and which carrier does each row live in? | the pin row: version + carrier + provenance channel per loaded module (what is loaded is what can betray you) | the version-pinned read table on record (v1 "How To Shot Web" DEF CON 23 2015 → TBHM Core 2024+; sources.md §1, the queue's gate honored) |
| G2 | Which rows are doctrine the house owns — and which are somebody else's tool on an era stamp? | the split row: owned method vs attributed curation, owner named per tool row | the corpus's own attribution discipline on record (the seventeen-name attribution slide at DC23; "the curation is his, the tools are theirs" — sources.md §4, the A3 ledger) |
| G3 | What rotted since the last era — which curated rows are past their stamp, changed behavior, or gone paid? | the re-verification queue: existence, behavior delta, paywall/rot per stale row | the corpus's own rot record on record (WPscan "has gone paid … I'm still looking for a viable alternative", the Twitter-API workflow "currently in trouble", the eight-year-old XSS methodology — sources.md §2 L4, the Live Day 2 rows) |
| G4 | Which checklist row claims completion without its evidence artifact? | the gate conversions: entry condition, evidence, falsifier per task row | the Fast Testing Checklist on record — task-checkboxes without gates in the shipped form (W3; sources.md §1, the checklist's own header naming its WAHH parent). The gate form is the organ's own operationalization, labeled |
| G5 | Which numbers will price effort — and what is each made of? | the basis classes: measured / stated-rule-of-thumb / heuristic, sample + revalidation trigger per claim | the quantified instinct on record (the 2x-per-subdomain / 4x-per-apex multipliers, the "+50%" efficacy of configured APIs, the "3-10% increased discoveries" — sources.md §2 L1, the Live Day 1/Day 2 rows) |
| G6 | Who is the newcomer — and what closed record separates "has read the methodology" from "can run it"? | the proof gate: the canary run's gates, the calibration priors, the live-scope refusal | the corpus's own onboarding surface on record (conference decks, a paid course, a Discord community — the newcomer's proof is never defined; W5's documented absence, method-upgrade.md §1). The gate is the organ's own operationalization, labeled |

Ranking rationale: question priority = what betrays the engagement
first × what cannot be repaired mid-run. The pin ranks first — an
unpinned state is unreconstructable, and no drift audit can name what
changed mid-run after the fact; the split ranks second because it
arms the rot queue (an unsplit tool row walks into the engagement as
evidence); the rot queue ranks third — a stale row fires as evidence
before anyone re-reads it; the gate conversions rank fourth
(checkbox theater wastes a run quietly rather than catastrophically);
the basis classes fifth (a rule-of-thumb multiplier mispriced surfaces
in the report, not mid-run); the proof gate last in reading order but
first in refusal strength — live scope stays refused behind it. Rows
out; nothing pinned, nothing adopted, no newcomer cleared.

Generation falsifier: an onboarding read that yields zero rows across
all six classes means the reading was shallow, not the corpus clean —
a corpus with a nine-year version chain, a seventeen-name attribution
ledger, a documented rot record, and a carrier drift record (the
repo chapters stalled 2016–2020 while the decks versioned; 12_IDOR "To
be continued …" to this day) always yields rows; zero rows
falsifies the reading, never the corpus. A newcomer with zero
calibration deltas means the PROOF run was not run, not that the
priors were perfect.

#### The ladder's payload kit — the preservation rows (customize before use)

Generation writes rows; these are the read classes the rows name,
every one a reading of corpus artifacts already in scope (no request
sent; the protocol mechanics live in the M-protocol and T1–T5):

| Read row | The read payload class | Writes which row |
| --- | --- | --- |
| version row | each loaded module's version + carrier (deck / repo / checklist / gist) + provenance channel | PIN row (M1) |
| attribution row | each tool row's owner + era stamp + re-verify flag | SPLIT row (M2, the curation side) |
| rot row | each era-stamped row's last-verified state vs its stamp: existence, behavior delta, paywall | reverify-queue row (M2's defects) |
| gate row | each checklist task's entry condition, evidence artifact, falsifier | TASK row with gates (M3) |
| basis row | each quantified claim's basis class, sample size, revalidation trigger | NUM row (M4) |
| proof row | the newcomer's canary gates + calibration priors vs observed | PROOF row (M5) |
| drift row | old pin vs new pin per bump: doctrine delta, curation rot | DRIFT record (M6) |

Customization knobs, stated in the plan note: the pin breadth
(loaded-organs-only vs whole-corpus — the rule is loaded-only, "what
is loaded is what can betray you"; the knob is which carriers pin:
the free chain, the stated-BOUNDED paid interiors, or both), the era
window (how many months stale before a row enters the re-verification
queue), and the proof strictness (which gates the house demands
before live scope clears: auditor exit-0, ledger discipline, closure
states — the subset is the engagement's to name).

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | The refusal doing the heavy lifting |
| --- | --- | --- |
| Engagement start, R0 record present | emit the PIN (M1) into state; state the pinned versions in the engagement's opening record | refuse to proceed past recon without the PIN — "which version of the doctrine answers is unverifiable" |
| A tool row fires for the first time this era | run the re-verification step (M2): existence, behavior delta, paywall/rot check; record the outcome | refuse the tool's output as evidence when its row is past an unverified era stamp |
| A checklist row is about to be marked done | demand the evidence artifact (M3) | refuse the tick without the artifact — "checkbox ≠ completion" |
| A quantified claim is about to price effort | read the basis class (M4); cap rule-of-thumb numbers as priors | refuse the multiplier when the basis is unstated |
| A newcomer requests live scope | check for a closed PROOF record (M5) | refuse + route to the canary proving-ground run with the exact gates named |
| A corpus version bump is proposed | run the drift audit (M6) before adoption | refuse a silent bump — "no bump lands without a DRIFT record" |
| An operator asks "which artifact is authoritative?" | answer from the PIN and the split (M1/M2) — doctrine lives in the pinned module; curation lives in its era | refuse to resolve authority by seniority or by which artifact is loudest |
| A template report is being assembled | run the re-derivation checklist per field (R5) | refuse template-stored URLs/domains/names into a live report |
| A tier/ranking claim guides a tool choice | treat as prior (R6); log the choice basis | refuse to escalate a tier opinion into a factual constraint |

## 3. The scripting arsenal — techniques as runnable craft

Read-only, operator-side; writes tables and records to stdout for the
ledger. The house form: minimal, robust, resumable, deleted when the
question is answered (§27 minimal-code doctrine).

### T1 — the pin snapshotter

```bash
python3 - <<'PY'
# T1: walk the corpus frontmatter, emit the PIN record. Read-only.
import re, pathlib, datetime
root = pathlib.Path("skills")
pins = []
for sk in sorted(root.iterdir()):
    f = sk / "SKILL.md"
    if not f.is_file():
        continue
    head = f.read_text(encoding="utf-8")[:4000]
    m = re.search(r"^version: (\S+)", head, re.M)
    if m:
        pins.append((sk.name, m.group(1)))
print("PIN: corpus-state stamp=%s" % datetime.date.today().isoformat())
print("  organs=%d" % len(pins))
for name, ver in pins:
    print("  %-24s %s" % (name, ver))
print("  drift-policy=diff-before-bump, re-verify before first use")
PY
```

Validating the output: the record names every loaded organ with an
exact version; an organ missing from the PIN that later serves a
request is the falsifier tripped.

### T2 — the curation auditor

```bash
python3 - <<'PY'
# T2: find tool rows whose era stamp is stale or absent. Read-only.
# A "tool row" here is any line citing a named third-party tool.
import re, sys
era = re.compile(r"(19|20)\d{2}")
for path in sys.argv[1:]:
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        if re.search(r"\b(tool|scanner|framework)\b", line, re.I):
            print("%s:%d %s" % (path, n, line.strip()[:90]))
PY
```

Run over the onboarding artifacts; rows without an era marker or an
owner name feed the re-verification queue (M2's defects, not style
notes).

### T3 — the checklist gate renderer

```bash
python3 - <<'PY'
# T3: emit an onboarding checklist with M3 gates. Read-only.
rows = [
    # (task, entry, evidence, falsifier)
    ("read the spine canon", "newcomer",
     "ledger record R-NNN: summary in own words",
     "summary restates section numbers wrong"),
    ("first canary engagement", "spine canon read",
     "auditor exit-0 on the canary report",
     "auditor exit-1 or missing report"),
    ("ledger discipline drill", "engagement under way",
     "3 records with closure states",
     "any record lacks its closure line"),
]
for t, e, ev, f in rows:
    print("TASK %-28s entry=%-22s" % (t, e))
    print("     evidence=%s" % ev)
    print("     falsifier=%s" % f)
PY
```

### T4 — the drift differ

```bash
python3 - <<'PY'
# T4: diff two pin records into the DRIFT table. Read-only.
import sys
def load(p):
    return dict(l.split(None, 1) for l in open(p) if ":" in l)
old, new = load(sys.argv[1]), load(sys.argv[2])
for k in sorted(set(old) | set(new)):
    if old.get(k) != new.get(k):
        print("DRIFT %-24s %s -> %s" % (k, old.get(k), new.get(k)))
PY
```

Output feeds M6: doctrine deltas adopt with notes; curation rot rows
enqueue re-verification TODOs before the first request.

### T5 — the newcomer first-run verifier

```bash
python3 - <<'PY'
# T5: orchestrate the canary first run; record calibration. Read-only
# except the ledger append the operator performs from the output.
checks = [
    ("selftest", "python3 arsenal/server.py --selftest"),
    ("auditor", "python3 scripts/audit_report.py <canary-report.md>"),
    ("closure", "every hypothesis carries a Closure: line"),
]
for name, cmd in checks:
    print("PROOF-CHECK %-10s %s" % (name, cmd))
print("live-scope=REFUSED until PROOF closes")
PY
```

## 4. The rigid run-order — step by step

S1 **PIN** (M1): emit the corpus pin at engagement start, after R0.
S2 **SPLIT** (M2): confirm the loaded onboarding artifacts carry the
method/curation split; queue the curation rows for re-verification.
S3 **GATE-CONVERT** (M3): render the onboarding checklist with gates;
no row closes without its evidence artifact.
S4 **CLASSIFY** (M4): basis-class every quantified claim the corpus
will use; cap the rule-of-thumb numbers as priors.
S5 **PROVE** (M5): the newcomer's first run closes the PROOF record on
the proving ground; live scope stays refused until it closes.
S6 **DRIFT-AUDIT** (M6): at every bump, the differ runs before
adoption; the drift record lands in the ledger.

The order is rigid because each step consumes the previous record:
re-verification needs the split; the checklist gates need the
classification; the proof gate needs the checklist; the drift audit
needs the pins to differ.

## 5. Falsifiers — what would prove this runtime wrong

1. A request in an unpinned engagement state reaches a target (R1/M1
   dead).
2. A stale-era tool row produced evidence without a re-verification
   record (R2/M2 dead).
3. A completed onboarding row has no evidence artifact (R3/M3 dead
   by checkbox theater).
4. A rule-of-thumb multiplier priced effort as fact (M4 dead).
5. A newcomer with live scope and no closed PROOF record (M5 dead).
6. A version bump with no DRIFT record anywhere in the ledger
   (M6 dead).
7. A templated report field carrying template-stored target values
   (R5 dead).

Any one of these, observed in the ledger, falsifies the claim that
the onboarding path preserves the methodology it ships — and names
the exact record missing.
