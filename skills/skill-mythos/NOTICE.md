# NOTICE — third-party data shipped in this bundle

## Bugcrowd Vulnerability Rating Taxonomy

`references/vrt-taxonomy.json` is the official Bugcrowd Vulnerability
Rating Taxonomy, redistributed unchanged from:

https://github.com/bugcrowd/vulnerability-rating-taxonomy
(raw file: vulnerability-rating-taxonomy.json, branch master)

Copyright (c) Bugcrowd, Inc. Licensed under the Apache License,
Version 2.0 (the file's upstream license; a copy of the Apache-2.0
license text is available at https://www.apache.org/licenses/LICENSE-2.0).

The JSON's own `metadata.release_date` field states the release it
carries. It is data, not code: it is read by `arsenal/tools/mythos.py`
(`vrt_classify`) and validated by `auditor/audit_report.py`, and it
may be upgraded in place — see `references/activation.md` §6.

The live taxonomy at https://bugcrowd.com/vrt remains the
submission-time authority.

Everything else in this bundle is original work under the bundle's
MIT license. The CVSS 3.1 arithmetic in `arsenal/cvss.py` implements
the public FIRST specification (equations reproduced in
`references/cvss-guide.md`); no FIRST content is redistributed.
