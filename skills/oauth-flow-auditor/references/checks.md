# OAuth Check Catalog

Each check: the transition it attacks, the treatment, the control, the
falsifier. Pre-register the hypothesis BEFORE the treatment request.

| # | Check | Transition | Treatment | Control | Falsifier |
| --- | --- | --- | --- | --- | --- |
| C1 | redirect_uri scheme swap | authorize | `redirect_uri=https://` → `http://` same host | port changed on unrelated param | request still 30x to the swapped scheme |
| C2 | redirect_uri path traversal | authorize | append `/..%2f` or `/%2e%2e/` to the registered path | append a random suffix char | callback hit under a path outside the registration |
| C3 | redirect_uri host confusion | authorize | case/unicode look-alike or subdomain of the registered host | entirely different TLD | 30x to the look-alike host survives |
| C4 | open redirect chain | callback | callback param inside the redirect_uri value echoed on | garbage callback param | post-auth bounce lands on attacker-controllable host |
| C5 | state absent or unvalidated | callback | drop the state / send another state | send same-state to wrong nonce | flow completes anyway (account-takeover enablement) |
| C6 | PKCE absent for public client | authorize | remove `code_challenge` | add invalid challenge | authorization code issued without a challenge |
| C7 | code reuse | token | redeem the SAME code twice, sequentially | redeem two DIFFERENT codes | second redemption returns tokens |
| C8 | code substitution | token | redeem operator-app-B's code with app-A's client credentials | redeem garbage string | exchange succeeds cross-client |
| C9 | token audience | resource | send app-A's token to app-B's resource (both operator-owned) | send garbage token | resource accepts the wrong-audience token |
| C10 | implicit/fragment flow live | authorize | `response_type=token` | `response_type=garbage` | tokens in the fragment without a code round-trip |
| C11 | refresh token rotation | token | use a refreshed (rotated) refresh token again | use current refresh token | the pre-rotation token still redeems |
| C12 | prompt/consent bypass | authorize | `prompt=none` for a never-consented operator app | `prompt=login` | silent issuance without prior consent |

## Interpretation discipline

* C1–C4 family: "open redirect_uri" only matters if the code/state lands
  somewhere attacker-influenced — the CONFIRMED bar needs the full chain
  (issuance → attacker-visible landing), not a permissive 30x alone.
* C5: absence of state is a hygiene finding; CONFIRMED account-takeover
  enablement needs a CSRF-able state-bearing action demonstrated with
  operator accounts.
* C7/C8: single-hypothesis each; the reuse attempt count is 2 sequential
  (n_runs floor does not multiply code redemptions — the server may
  single-use-invalidate on first redemption, which is the FALSIFIER).
* C9: audience confusion requires BOTH apps operator-owned; report the
  class even when impact is bounded to test apps — programs rate it on
  the IdP's isolation model, not your demo's blast radius.

## Report grammar for this organ

Every CONFIRMED check cites: the happy-path baseline record, the treatment
record, the control record, the catalog id (C1–C12), and the canary
attestation that only operator-owned apps/accounts were involved.
