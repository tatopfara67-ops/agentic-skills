# mythos-proving-ground

**The examiner for AI security agents.** Not another scanner — the benchmark
that proves a security skill actually works.

## Why this exists

Every marketplace skill promises to make your agent a better hunter. None of
them can prove it. "Not generic" is claimed in every README and measured in
none of them.

This package inverts the market: instead of selling another student, it sells
the exam. An **instrumented lab** (localhost, synthetic, self-owned) records
what an agent actually does; the agent's claimed findings are scored against
server-side reality. Hallucinated findings have no server-side trace and are
exposed mechanically. Impact discipline — proving harm with canaries instead
of reading production-like data — is a score, not a vibe.

> The lab is the ground truth. Claims without server-side trace are noise.

## The pitch in one table

| Metric | What it catches |
|---|---|
| coverage / recall | what the arm actually found |
| precision | claims not backed by server-side reality |
| hallucination rate | fabricated or misclassified findings |
| harm events | decoy-data touches (impact discipline failures) |
| evidence discipline | paperwork slop |
| efficiency | brute force vs directed hunting |

Run a **naked arm** vs a **skilled arm** under the fairness doctrine
(identical prompt, budget, model; N≥3 trials; medians), and "my skill is not
generic" becomes a delta table — or becomes decoration, honestly labeled.

## Quickstart

```bash
# 1. start the lab (fresh state)
cd targets/taskboard-lite && rm -f events.jsonl
LAB_PORT=3101 LAB_EVENTS=$PWD/events.jsonl python3 lab_server.py &

# 2. run your agent (naked or skilled) with the operator prompt in SKILL.md §5

# 3. score it
python3 ../../scripts/run_benchmark.py \
    --ground-truth ground_truth.json \
    --events events.jsonl \
    --results /path/to/results.json \
    --label "skilled-arm trial 1" --out scorecard.md

# 4. see the fixtures that calibrate the examiner
python3 ../scripts/run_benchmark.py \
    --ground-truth targets/taskboard-lite/ground_truth.json \
    --events example/events-skilled-run.jsonl \
    --results example/results-skilled.json --label "fixture: skilled"
python3 ../scripts/run_benchmark.py \
    --ground-truth targets/taskboard-lite/ground_truth.json \
    --events example/events-skilled-run.jsonl \
    --results example/results-sloppy.json --label "fixture: sloppy"
```

The sloppy fixture — an agent claiming RCE, CSRF, SSRF it never triggered —
scores 67% hallucination. That is the machine working.

## What this is — and is not

- **Is**: a measurement instrument for skill authors and agent operators.
  Sibling of `mythos-bug-hunter` (the discipline layer for hunting); this
  package measures the hunter.
- **Is not**: a hunting skill, a real-world certification, or marketing
  material. Lab scores are lab-scoped; publish all arms or publish nothing.
- The lab: 6 seeded bugs across 6 classes (IDOR, open redirect, reflected
  XSS, client-trusted header bypass, information disclosure, simulated SQLi
  sink), canary + decoy separation, stdlib-only Python, binds 127.0.0.1 only.

## Legal

Self-owned synthetic lab, localhost only, zero real data. Authorization is
trivial by construction — that is the point.

## License

MIT — see the LICENSE file in the repository root if present, otherwise
treat this README's section as the grant.
