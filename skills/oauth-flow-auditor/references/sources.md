# sources.md — verified lineage sources for oauth-flow-auditor (v2)

The Parecki layer (`flow-craft.md`) distills the public OAuth craft
corpus. Verified during this upgrade:

* Aaron Parecki — author of "OAuth 2.0 Simplified" (oauth.com /
  oauth2simplified.com), maintainer of oauth.net, co-editor of the
  in-progress OAuth 2.1 draft; Senior Security Architect at Okta. The
  book's client-and-server walkthroughs (redirect_uri exactness, state,
  PKCE handling, token audience) are the field-guide layer's backbone.
* RFC 6749 — "The OAuth 2.0 Authorization Framework" (§3.1.2.3 exact
  match; §3.3 scope/audience).
* RFC 7636 — "Proof Key for Code Exchange" (S256 vs plain).
* RFC 6819 — "OAuth 2.0 Threat Model and Security Considerations".
* RFC 9700 — "OAuth 2.0 Security Best Current Practice" (issuer
  identification / mix-up defense, exact redirect matching, no implicit,
  sender-constrained tokens).
* oauth.net/getting-started — the public on-ramp that names the same
  craft order this organ follows.

Correction record: none.
