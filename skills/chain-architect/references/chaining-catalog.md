# chaining-catalog.md — primitives, composition questions, chain archetypes

The working vocabulary of chain-architect. Load when inventoring
primitives, asking the composition question, or designing a chain.

## 1. The Primitive Vocabulary

A primitive is a CONFIRMED finding re-described as a capability. Rate
the capability, not the finding — the standalone VRT of "verbose error"
is P5, but as the second link of an auth chain it can carry a P1
argument. Record both; argue the chain honestly.

| Primitive | Grants | Typical standalone severity |
| --- | --- | --- |
| Information disclosure (stack, versions, paths) | knowledge for the NEXT link | P5 |
| Internal hostname / endpoint leak | a seam to reach | P5 |
| Post-auth SSRF | internal network position | P3-P4 |
| Auth bypass / pre-auth access to a post-auth surface | position inside a trust zone | P2-P3 |
| Arbitrary file write (bounded path) | persistence / config poisoning position | P3 |
| Arbitrary file read | secret acquisition | P2-P4 |
| Parser confusion (URL, header, path) | validation disagreement | P4 |
| Open redirect | controlled navigation of a victim | P5 |
| Account takeover of self-registered account | a trusted identity | P2-P3 |
| Race window on a state transition | duplicated side effect | P3 |
| Debug/undocumented endpoint exposure | unguarded capability | P2-P5 |

## 2. The Composition Question (ask per primitive)

**"What does this give me a position FOR?"** Concretely, per primitive:

* knowledge → which link does it make targetable?
* reach → what internal service trusts that origin?
* write → whose code or config reads what I write, and when?
* read → which secret unlocks which trust boundary?
* identity → which role does the system grant it, where?
* timing → which invariant can be violated in the window?

If no answer, the primitive is genuinely inert this engagement — park
it in the dossier with a one-line note; do not force it.

## 3. Chain Archetypes (design patterns)

1. **Pre-auth pivot (the ProxyLogon shape).**
   post-auth SSRF → backend treat-as-trusted internal call →
   privileged action exposed without real authentication. Crosses a
   trust zone: scope S:C in the chain vector.
2. **Write-then-execute.**
   file upload/write with weak path control (P3) + a parser that
   includes/interprets files (knowledge from an info leak) → code
   execution. The chain argues why the path is reachable.
3. **Confusion chain.** Parser disagreement (URL/header semantics)
   → validation bypass at the edge → privileged route internally
   interpreted. Combines with desync-hunter's asymmetry classes.
4. **Identity ladder.** Self-registered account → object-level access
   (auth-boundary-mapper violation) → role-confusion endpoint →
   admin capability. Every rung self-owned until the last, bounded
   step.
5. **Cache/store poisoning chain.** Reflected controllable content
   (P4) + caching proxy seam (ghost/desync territory) + victim fetch
   → stored XSS with CSP bypass or open-redirect bootstrapping.
6. **2nd-order reference chain.** Object reference created in one
   feature (invite, export) → consumed in another (see
   auth-boundary-mapper's 2nd-order IDOR sweep) → cross-tenant read.
7. **SSRF bridge.** SSRF + cloud metadata / internal admin panel +
   weak internal trust (trust-graph-hunter's forged-context edges) →
   credential acquisition → account takeover.

## 4. Chain Design Record (the pre-registration template)

```
CHAIN-C<k>: <one-line claim>
  path: P1(prim) -> P2(prim) -> P3(prim) -> impact
  joints: [J1: output of P1 = input expected by P2 (record R-NNN),
           J2: ...]
  prediction: <the observable if all joints hold>
  falsifier: <what observation kills which link>
  bound: one end-to-end run; canary = <self-owned marker>
  vector: CVSS:3.1/... (PR of the FIRST link; S:C iff trust-zone
          crossing; impact = the CHAIN's observed final effect)
```

Every joint cites the record pair that shows output→input coupling.
A joint with no record is an assumed link — forbidden (hard rule 1).

## 5. Anti-patterns (recorded as MISTAKEs when caught)

* **Chain inflation.** Writing the combined severity onto each link.
* **Paper chains.** Designs never bottom-up verified; two sessions of
  design with zero link triads = park and resume-note.
* **Shotgun composition.** Trying all primitives against all others —
  this is R1 slop with a chain vocabulary on top.
* **Foreign data in proofs.** Any link touching a real user's object
  invalidates the chain proof — restart the joint with self-owned
  inputs.
