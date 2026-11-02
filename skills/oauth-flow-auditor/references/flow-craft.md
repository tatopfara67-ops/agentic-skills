# flow-craft.md — the Parecki lineage layer for oauth-flow-auditor (v2)

Load when selecting checks for an authorization code flow, when a
redirect_uri hypothesis needs its exact-match matrix, or when closing
PKCE/state checks. The RFC citations are anchors, not decoration: each
check row below names the normative sentence it attacks.

## 1. redirect_uri Is the Load-Bearing Wall

RFC 6749 §3.1.2.3: the authorization server MUST require an exact match
of redirect URI — not prefix, not substring. The v1 check catalog treats
"exact-match" as one check; the craft treats it as a matrix:

| Variant class | Treatment | Verdict shape |
| --- | --- | --- |
| case difference | `REDIRECT.example.com` vs registered | acceptance = case-insensitive comparator bug |
| trailing slash | `/cb` vs `/cb/` | acceptance = path-prefix match |
| path traversal | `/cb/../../evil` (post-normalization) | acceptance = normalization AFTER validation |
| userinfo | `https://app.example.com@evil.com/` | acceptance = authority confusion |
| uncommon encoding | `%2F`, `%5C`, double-encoded segments | acceptance = decode-order bug |
| scheme swap | `http://` vs `https://` | acceptance = scheme ignored |

Run the matrix at BOTH ends separately: the authorization endpoint and
the token endpoint validate redirect_uri independently — they can
disagree, and the disagreement is itself a finding (one end exact, one
end prefix = code issuance to a prefixed redirect that the other end
rejects, or worse, accepts).

## 2. state Is CSRF Armor AND a Nonce

Three separate checks, never one:

1. **Presence.** Happy-path transcript without `state` → CSRF door open
   (record; impact rides the code-interception chain).
2. **Validation.** Treatment: callback with valid code + garbage state;
   the server-side session accept/reject verdict read from the app's
   behavior, not from the IdP docs.
3. **Binding/single-use.** state is bound to the browser session and
   dies on first use — replaying a captured state+code pair at the
   operator's own callback host is the bounded differential that closes
   it.

## 3. PKCE Everywhere, Including Where It Wasn't Invited

RFC 7636 exists for public clients; the modern posture (and the 2.1 line)
expects it on confidential clients too. Two checks:

* **Downgrade.** Send the authorization request WITHOUT code_challenge
  where the client normally sends one: acceptance = the server does not
  require PKCE for this client.
* **Plain-vs-S256.** A code_challenge_method=plain acceptance where S256
  was offered = downgrade bait; record, and let severity ride the chain.

## 4. The BCP Ceiling (RFC 9700)

The Security BCP names the controls this organ checks, so the report
vocabulary maps cleanly: issuer identification (mix-up defense — the
operator's second app registration is the differential instrument),
exact redirect matching (§1 above), no implicit flow (its presence is a
recorded fact feeding token-leak chains), and sender-constrained tokens
(absence bounds the code-interception impact claim). Token audience and
scope handling per RFC 6749 §3.3: the resource server's accept/reject of
an operator token outside its audience is a one-differential closure.

## 5. The Error-Path Leak Family

Authorization-server error pages are differential instruments in their
own right: differential body/latency across (unknown client_id, known
client_id + bad redirect, valid pair) maps the enumeration surface.
Error redirects that ECHO the unvalidated redirect_uri back (in Location
or in the body) convert an open-redirect finding into a code-theft
primitive — record the echo verbatim; it is chain-architect input.

## 6. The Craft, Stated As Five Field Rules

1. redirect_uri is a matrix at both ends, exact match per RFC 6749 —
   each variant its own hypothesis row.
2. state = presence + validation + binding: three checks, three closures.
3. PKCE downgrade is checked even where PKCE wasn't invited.
4. Severity vocabulary maps to the BCP (RFC 9700); cite the control, not
   the mood.
5. Error paths are instruments — echo verbatim, chain outward.
