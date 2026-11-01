# Extraction Catalog

## Collecting bundle URLs

1. `http_probe` the HTML entry points; artifact bodies contain the markup.
2. From markup, collect: `<script src=...>`, `import` statements in inline
   modules, `<link rel=preload as=script>`, JSON-LD/`__NEXT_DATA__`/`__NUXT__`
   build manifests (they carry chunk lists).
3. SPA chunk graphs: modern bundlers emit a manifest (`buildManifest`,
   `_buildManifest.js` for Next; `webpack chunk` maps). Parse chunk names
   from the manifest instead of guessing — bounded to the manifest's own
   list.
4. Bounded cap: ~40 bundles per engagement unless the operator raises it.
   Past the cap, park the remainder (R7 budget).

## What the tool extracts (and what to do with it)

| Extraction | Meaning | Next action |
| --- | --- | --- |
| Quoted path-shaped strings | candidate endpoints | probe each once |
| Routes inside comments | deprecated endpoints | probe each once, flag class |
| `fetch/axios` call shapes with method | endpoint + verb | probe with the right verb |
| `sourceMappingURL=` | map file candidate | bounded fetch of the `.map` |
| Key-shaped strings | secret hints | masked, report-only (secrets-policy) |
| WebSocket URLs (`wss://`) | websocket surface | dossier as `websocket` |
| Third-party hosts | dependency inventory | `third-party-asset` surfaces if in scope |

## Version drift (old bundle vs new)

When an archive (wayback-style) or a renamed old bundle is available in
evidence: diff endpoint lists between versions. Endpoints that VANISHED
between versions are `deprecated-endpoint` candidates with a high-yield
variant-analysis shape — same bug class, unfixed remnant. Diff output is a
hypothesis list; each candidate still needs a fresh probe record.

## Local-analysis discipline

All regex work happens against the saved artifact, never a re-fetch.
Extraction results cite the artifact path in the ledger note. If a pattern
misses (bundle is minified beyond the pattern), record THAT as a fact and
park — do not churn requests looking for a prettier bundle.
