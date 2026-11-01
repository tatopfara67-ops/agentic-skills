# The Shimomura Binary Brain — formal spec

The tracker's entire mind is **four bits**. Not a dashboard, not a
score: four registers, each readable as 1 or 0, each one a gate the
loop must pass before it may advance. Everything else — playbooks,
channels, tooling — exists to set those bits honestly.

## 1. The four registers

| # | Register | Reads 1 when | Reads 0 when | Gate it controls |
| - | -------- | ------------ | ------------ | ---------------- |
| 1 | SIGNAL   | the observation deviates from the calibrated baseline | baseline noise | no hunt may open on noise |
| 2 | SPLIT    | the candidate test halves the active space (≈1 bit) | the test discriminates weakly or not at all | a 0-SPLIT test is refused while the space is plural |
| 3 | TRUTH    | ≥2 independent channels agree on the surviving hypothesis | fewer than two channels | CONFIRMED is unreachable; localization claims are forbidden |
| 4 | TIP-OFF  | the planned action would reveal our knowledge to the adversary | the action is indistinguishable from baseline | a 1-TIP-OFF test is gated behind every passive eliminator |

Registers 1–2 are about **us** (are we seeing, are we choosing well);
registers 3–4 are about **them** (can we prove it, will they notice).
The engine (`arsenal/sbb.py`) reads them out on every call:

    SIGNAL=1 SPLIT=1.00 TRUTH=2ch TIP-OFF=clear

## 2. The loop

    FREEZE      capture before change; clocks synced; nothing scrubbed
    BASELINE    normal is measured, recorded as CONTROL records
    CLASSIFY    observation → SIGNAL bit → FACT record
    ENUMERATE   H = {hypotheses} ∪ {null}; null is auto-inserted
    loop:
      SELECT    test = argmax expected bits over active H   (SPLIT)
      GATE      if test.tip_off and passive eliminators remain: refuse
      EXECUTE   passively; observation arrives as one bit
      ELIMINATE hypotheses inconsistent with the bit        (ledgered)
      until |active H| = 1 or budget (R7) says stop
    FIX         survivor crosses a SECOND independent channel (TRUTH)
    HANDOFF     pack written from records; the last mile is not ours

Two exits are honest: `|H| = 1` with TRUTH=1 (confirmed), and
`|H| = 0` (the space was falsified — a MISTAKE record, then
re-enumeration with what the deaths taught). Everything else is
parking, and parking is recorded.

## 3. Legal states (the 4-bit table)

Only these states may occur; anything else is a bug in the tracker,
not a mystery in the case.

| SIGNAL | SPLIT | TRUTH | TIP-OFF | State | Meaning |
| ------ | ----- | ----- | ------- | ----- | ------- |
| 0 | – | – | – | dormant | no signal; hunting now would be curiosity, which is forbidden |
| 1 | 0 | 0 | 0 | alerted | signal recorded, space not yet declared — declare or park |
| 1 | 1 | 0 | 0 | armed | space declared, max-gain test pre-registered |
| 1 | 1 | 0 | 1 | armed-gated | best available test would tip the adversary; passive alternative forced |
| 1 | 1 | 1 | 0 | fixing | singleton alive on ≥2 channels: CONFIRMED, close the hunt |
| 1 | 0 | 1 | 1 | closed-armed | confirmed; a tip-off action (containment) is now IR's deliberate choice |
| 1 | 0 | 0 | 1 | hold | nothing executable without either wasting bits or tipping off — declare new tests |

Invariants:

* TRUTH=1 requires SIGNAL=1 (no confirmation without a recorded signal).
* TRUTH=1 requires a singleton (channels accumulate on survivors only).
* TIP-OFF=1 never blocks *thinking*, only *acting* — the register
  gates execution, never analysis.
* SPLIT is recomputed at every decision; it is a property of the
  frontier, not of the hunt.

## 4. The halving math (why "binary" is not a metaphor)

For a test T over n active hypotheses, let a = number of hypotheses
T kills on outcome 1. Under a uniform prior the expected information
gain is the Shannon entropy of the split:

    p   = (n − a) / n
    bits(T) = −p·log₂(p) − (1−p)·log₂(1−p)

* a = n/2 → 1.00 bit: the discipline's target.
* a = 0 (or n) → 0.00 bits: refused as wasted budget (Rule H).
* Lower bound on decisive tests: **floor = ⌈log₂(n₀)⌉** where n₀ is
  the initial space. Eight hypotheses → three perfect tests. The
  engine reports `tests_used` against `floor` on every apply; a hunt
  that keeps needing twice the floor has a partitioning problem, not
  an evidence problem.

Worked micro-example (the lab demo, `lab/christmas_lab.py`):

    n₀ = 8 (null + 7 suspects)
    T-001 netflow history      on 1 kills 4   → 1.00 bit  → 4 alive
    T-002 lease origin         on 1 kills 2   → 1.00 bit  → 2 alive
    T-003 interface fingerprint on 1 kills 1  → 1.00 bit  → 1 alive
    channels on survivor: netflow (T-001, T-002) + host-audit (T-003)
    → CONFIRMED at exactly the floor: 3 tests, log₂(8) = 3.

## 5. The two-channel rule (Rule T)

Two channels are independent when their **error sources are
uncorrelated**. Network telemetry and host audit fail differently; two
sensors of the same network feed do not — that is one story told
twice. In 1995 the fix that mattered paired carrier switch records
with radio-frequency measurements (the "reverse double
triangulation"); neither alone would have survived scrutiny.

Modern pairs that qualify:

| Channel A | Channel B | Why independent |
| --------- | --------- | --------------- |
| netflow / VPC flow logs | host audit (auth logs, EDR) | network view vs endpoint state |
| identity provider sign-in logs | passive external (CT, passive DNS) | operator-side vs third-party |
| temporal correlation (clock skew, cadence) | build/physical metadata (MAC OUI, DHCP fingerprint) | behavior vs artifact |

The engine enforces this mechanically: CONFIRMED requires that the
survivor crossed RUN tests spanning ≥2 distinct channel names. A
single-channel hunt is warned at declare time and can never close.

## 6. Why binary at all

* **Falsifiability.** A bit cannot be half-true. Every decision the
  brain makes is checkable against one ledger record — the auditor's
  whole job.
* **The asymmetry.** The adversary must eventually act in the world
  (scans, connections, taunts); the tracker only has to observe. In
  1994 the intruder left mocking voicemails — pure information
  transferred to the defender at zero cost. Our budget is bits; their
  budget is exposure. Halving spends ours at the theoretical minimum
  and forces them to keep spending theirs.
* **Pre-registration kills hindsight bias.** The partitions are frozen
  in an EXPERIMENT record before the outcome exists, so "the test was
  designed to discriminate, not to flatter" is provable from the
  ledger, not assertable from memory.
