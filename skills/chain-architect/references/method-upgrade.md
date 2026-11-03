# The executable method — M1–M5 for chain-architect

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
Orange Tsai's published chains) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

### M1 — the chain candidate schema (register before you hunt)

A chain candidate is a LEDGER record the moment it is conceived, not
when it succeeds:

```
CHAIN-CAND: id=C-014 links=[L1 primitive=SSRF-class surface=/auth/img
  precond=open-redirect; L2 primitive=auth-bypass surface=/ecp
  precond=internal-reach; L3 primitive=file-write surface=/export
  precond=NTLM-leak] status=registered conf=<per-link 0..1 with
  basis> goal=<end-state class>
```

Rules: candidates are registered in the session they are conceived
(A13 order discipline); each link names its primitive CLASS (from the
chaining-catalog), its surface, and its precondition — a link with an
empty precondition cell is not registered, it is daydreaming. The
pre-hunt register is what turns W1's narrative into method: the final
writeup must be able to cite the registered candidates, including the
ones that died.

### M2 — the surface-diff protocol (the eureka, mechanized)

1. **Component inventory**: enumerate the deployed component set and
   pin each version as a FACT record (error pages, version banners,
   build paths in static assets, `server`/`x-powered-by` sets — the
   desync-hunter CHAINMAP evidence habit, applied to app components).
2. **Cross-reference graph walk**: every reference one component makes
   to another (URL referrals, redirects, embedded links, proxy
   prefixes) is an EDGE record — scriptable over the crawled surface,
   re-runnable by a second analyst. The `/ecp`-refers-to-OWA class of
   insight becomes a queryable artifact (the W3 floor).
3. **Version-diff surface**: for each pinned component, the public
   diff surface between deployed and adjacent versions (patch notes,
   security advisories, with sources) is harvested as FACT records —
   the attack-surface delta is data, not memory.
4. Gate: chain candidates whose L1 surface does not appear in the
   inventory are REFUSED (not "tried later"): a link cannot stand on
   a surface that was never observed.

### M3 — the chain tree with prunes

The hunt explores a TREE, not a path. Every branch decision is
recorded:

```
TREE: C-014
  L1->L2: tried, FAILED (auth-bypass requires session; SSRF lacks
    cookies) — pruned, ref=<EXPERIMENT id>
  L1->L2': internal-reach via /ecp proxy-prefix — pruned, prefix
    stripped <EXPERIMENT id>
  L1->L2'': internal-reach via open-redirect + NTLM relay — LIVE,
    conf=0.8 basis=<n=5/5 differential, M4>
```

Prune records carry the EXPERIMENT id that killed them — a branch
pruned without evidence is not pruned, it is abandoned, and the
auditor treats it as such. The final report shows the tree: how many
candidates, how many prunes, why the surviving chain won (the W4
floor — alternates stop being invisible).

### M4 — the weakest-link differential gate

Every LIVE link passes its own organ's confirm rule — n ≥ 5,
interleaved, with the control condition — BEFORE the chain is claimed
end-to-end:

| Link evidence class | Gate | Chain confidence contribution |
| ------------------- | ---- | ----------------------------- |
| n = 5/5 + control clean | full | 1.0 for that link |
| n = 4/5 or control noisy | conditional | 0.6, precondition recorded |
| single-shot only | NOT A LINK | 0 — the chain may not include it |

**Weakest-link rule**: chain confidence = the MINIMUM over live
links, and the report states which link is the floor. A chain with one
0.6 link is a 0.6 chain, no matter how pretty the end-to-end demo
(the W2 floor made arithmetic).

### M5 — the ceiling statement

```
CEILING: registered=<count> pruned=<count with records> live=<count>
  weakest-link=<id, conf, basis> END-TO-END: demonstrated n=<runs
  with bucket distribution> or NOT-DEMONSTRATED
  CLAIMED-IMPACT: <class> — capped at <proven-link set>, fleet/
  org-wide claims ONLY with fleet evidence (mobile-hunter M5 habit)
```

"ProxyLogon-class RCE demonstrated once, weakest link 0.6" and "RCE
proven chain, 5/5 every link, demonstrated 10/10" are DIFFERENT
findings and are reported differently. The end-to-end run is itself an
EXPERIMENT with n_runs — one run is one run.

## 2. Falsifiers — what would prove this method wrong

* A link confirmed 5/5 in isolation fails ≥ 50% inside the chain →
  hidden precondition: the link's gate was incomplete; downgrade the
  chain and re-register the precondition as a new link.
* Two analysts' surface-diff inventories differ by a component → the
  inventory protocol missed a banner class: re-census, record the
  correction CONTROL.
* The tree has zero prune records and one live chain → the hunt
  pruned by narrative, not by experiment: the audit FAILS the chain
  report until prunes are evidenced or honestly marked unexplored.
* A pruned branch is later shown live → the prune's EXPERIMENT was
  wrong: re-open via `sbb_declare`; a prune stands only while its
  evidence stands.

## 3. Worked micro-example (numbers consistent, incident fictional)

Mail-front appliance, pinned version (M2: banner + build-path in
static asset, diff surface harvested from two public advisories).
Registered candidates: 3 (C-011..C-013) before any testing. C-012:
SSRF-class L1 → auth-bypass L2 → export file-write L3. Tree: 6
branches, 4 prunes with EXPERIMENT ids (two prefix-strips, a
cookie-lack, a dead redirect), 2 live. Link gates: L1 5/5 + control
clean → 1.0; L2 4/5 (control noisy) → 0.6 with precondition recorded.
Weakest-link: chain conf 0.6, L2 named as floor. End-to-end: 7/10
full, 3/10 crash-only — demonstrated with distribution, not a
screenshot. Ceiling block complete; org-wide impact NOT claimed
(fleet evidence absent).

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
Orange Tsai's art is real — ProxyLogon, the SSRF-era talks, the
confusion-attack line — but it is told as after-the-fact narrative: a
winning path presented as a story, endpoint lineages narrated as
insight, one chain shown among the many that died silently. This
module extracts what is tool-agnostic, names the floors, and ships the
replacement: a chain candidate schema registered BEFORE the hunt, a
surface-diff protocol, a chain tree with prunes on record, per-link
differential gates, and an honest ceiling. An agent that has never
keynoted must run this at his precision.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | The chain as after-the-fact narrative — the writeups walk the winning path end-to-end, discovered incrementally, presented as if architected | The METHOD (how candidates were generated, what was tried and discarded) is invisible; readers learn the bug, not the craft, and cannot re-run the discovery on a new target |
| W2 | Per-link confidence never tracked — every hop in the story reads equally solid | A chain is as good as its weakest link; a narrative can bury a "worked twice, flaky" hop inside confident prose. Nothing in the published form records link confidence or reproducibility per hop |
| W3 | Endpoint-lineage discovery narrated as insight — "I noticed /ecp refers to OWA" told as a eureka | No reproducible surface-diff protocol: component inventory, version pinning, and cross-reference graph walks are replaced by one analyst's noticing (the floor adversary-tracker calls W3: the method lives in the man) |
| W4 | Single-path demos — one chain is shown; alternate chains through the same primitives are unexplored or unreported | The reader cannot tell whether the shown chain was the only one, the best one, or just the first one; the attack-surface's real combinatorics stay unknown |
| W5 | Impact ceiling conflated — RCE demo theater blended with "full chain" claims | What is PROVEN (each primitive, each link, reproducibility) versus DEMONSTRATED (one end-to-end run) versus CLAIMED (fleet impact) collapse into one number-less sentence |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Chain candidates registered BEFORE the hunt, as records | **M1** — the chain candidate schema |
| U2 | Surface lineage by protocol, not insight | **M2** — the surface-diff protocol |
| U3 | Dead branches on record | **M3** — the chain tree with prunes |
| U4 | Every link earns its own differential gate | **M4** — the weakest-link rule |
| U5 | Proven / demonstrated / claimed kept apart | **M5** — the ceiling statement |
