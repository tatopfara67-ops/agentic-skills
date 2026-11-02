# Reference — Sources (lineage verification)

> Part of **mirror-hunter v1.0.0** (package architecture).
> **Load when:** the lineage claim needs its citation; a craft entry's
> research-wave source needs verification; the attribution boundary
> (what is Willison's, what is this bundle's) needs restating.
> Authoritative rules and the doctrine live in [`../SKILL.md`](../SKILL.md)
> — if anything in this module conflicts with the SKILL.md laws,
> **SKILL.md wins**.

---

## 1. The lineage, verified

**Simon Willison.** The coining essay: *"Prompt injection: What's the
worst that can happen?"* — simonwillison.net, October 2022, read in
full. The essay names the class in reaction to instruction-following
models being wired to retrieval and external tools, and credits Riley
Goodside's public prompt-exploitation explorations as the immediate
trigger. Verified: the term's coinage attribution (contemporaneous and
universally credited to this essay). The years of follow-up posts on
his site treat prompt injection as the defining security problem of
the LLM era — that sustained documentation record, not any single
exploit, is what this organ's lineage rests on. The coining post is
public writing about a vulnerability class; nothing of his is
vendored, and the mirror doctrine built on top of it (SKILL.md §3) is
this bundle's own contribution, kept on record as such in the lineage
registry entry.

## 2. The research wave the name covers

- **Greshake, Plikas, Aghakhani, Grosse, Backes, Woods — "You Can't
  See Me: Indirect Prompt Injection" (arXiv:2302.12173, 2023).** The
  foundational indirect-injection paper: instructions embedded in
  content the model *retrieves* (not the user's prompt) steer tool-
  augmented agents; multi-turn escalation documented. Consulted for
  craft entries 2.4 and the channel framing of §1.
- **Johann Rehberger (Embrace the Red, embracethered.com, 2023–2025).**
  The exfiltration-chain record: model output rendered as markdown
  images/links carrying data to attacker hosts; agent and copilot tool
  abuse chains; the "confused deputy" framing for LLM agents.
  Consulted for craft entry 2.8 and the tool-hijack shape of 2.10.
- **OWASP Top 10 for LLM Applications (2025 revision).** LLM01 Prompt
  Injection through the category set — the framework mapping the
  spine's §24 already runs; this organ uses the same mapping for the
  VRT crosswalk line.
- **Invariant Labs MCP security research (2025).** Tool poisoning
  (hostile instructions inside tool descriptions), rug pulls
  (descriptions changed after client approval), cross-server
  shadowing. Already the house citation in ai-and-supply-chain.md
  §24.5; consulted for the MCP-side of the surface inventory.
- **Cloud Security Alliance research note (May 2026), "Agent Context
  Poisoning: SKILL.md and the New AI Supply Chain Attack Surface."**
  Invisible-Unicode and hidden-payload techniques in agent context
  files; the Snyk ToxicSkills audit figures. Consulted for craft entry
  2.7 (token-level smuggling) — the technique's existence and
  detectability, cited as fact; no content copied.
- **Zou, Wang, Carlini, Chawla... — "Universal and Transferable
  Adversarial Attacks on Aligned Language Models" (arXiv:2307.15043,
  2023).** GCG-style automated adversarial suffixes. Consulted for the
  priced-out entry (injection-craft.md §3): real, documented, and
  priced out of a bounty budget.

## 3. The market's existence proof

- **Google AI Vulnerability Reward Program — rules page
  (bughunters.google.com, read 2026-11).** The qualifying table
  (S1/S2/A1–A4) and the ineligible list quoted in substance in
  eligibility-and-evidence.md §1.2; the canonical eligibility-table
  shape. Read directly, per engagement discipline — the rules page is
  the primary source and programs revise it.
- **SecurityWeek (October 8, 2025), "Google Offers Up to $20,000 in
  New AI Bug Bounty Program."** The 2025 program update combining
  abuse and security rewards into a single table; the reward ceiling
  cited as the market's existence proof.

## 4. In-house foundations (no external dependency)

- **glm-self-model v1.0.0** — the five truths, the E1–E8 failure
  geometry, the compensation gates; this organ inverts that catalog
  (SKILL.md §3.1). Liu et al. 2023 ("Lost in the Middle") is cited
  there for E2; Sharma et al. 2023 for E5; Ji et al. 2023 for E6.
- **mythos-bug-hunter v4.5.0, ai-and-supply-chain.md §24** — the
  surface map, the OWASP/ASI framework table, the four concrete test
  chains, and the nondeterministic-validation seeds (reproduction
  rates, deterministic-wrapper preference) this organ deepens into a
  full protocol.
- **ssrf-playbook** (the channel law), **chain-architect** (per-link
  and joint-proof discipline), **module-smith** (module cards) — the
  craft-layer contracts inherited in SKILL.md §1.

## 5. The attribution boundary, restated

The lineage registry entry for this organ carries a correction-shaped
note by design: **the mirror doctrine is this bundle's own
contribution** — the inversion of a self-model into a target map, the
eligibility gate as negative scope, the rate law, and the wrapper rule
are original doctrine. Willison's record — naming the class in October
2022 and documenting it relentlessly since — is credited for exactly
what it is. Conflating the two would be the same fabrication the
assimilation doctrine (skill-mythos references/assimilation-doctrine.md)
exists to prevent; the boundary stays explicit here and in the
registry.
