# interior-method.md — the census, the tables, the crosswalk

The organ's worked method: the enumeration order, the computed tables
(every number either computed in-house from documented constants or
cited to a specific public artifact — and labeled which), the boundary
crosswalk schema, and the composition rules. Load when running the hunt
end to end.

## 1. The enumeration order (M1's numbered procedure)

The census runs class by class, cheapest first, every row pinned to its
instrument and version:

1. **RPC endpoints** — local transports first (ALPC), then the
   network-exposed subset; each endpoint by interface id, with the
   protocol sequence and the security descriptor.
2. **COM/DCOM activation objects** — the activation catalog with the
   launch and access permissions per class.
3. **Services and their binary paths** — name, binary path, account,
   and whether any path component is writable by the census principal.
4. **Registry keys writable by the principal** that privileged
   components read (configuration, image paths, COM registration).
5. **Object-manager namespace** — named objects reachable for creation
   (squatting ground) and existing objects openable by the principal.
6. **Privileged DLL search orders** — directories preceding the binary's
   own directory on the search path, writable by the principal.
7. **Scheduled tasks and other execution triggers** reachable for
   creation or modification.

Order discipline: no class is attacked before every class is enumerated
— the seam table is built from the WHOLE census, and a seam argued from
a half-census is a product review wearing an interior's clothes.

## 2. The computed tables (on record this forge; recompute per engagement)

### 2.1 The access-mask budget (M2's arithmetic)

Documented constants (the Windows access-mask layout; the same constants
the 2024 book teaches chapter by chapter for humans — here they are a
decision table):

| Constant | Value (hex) | Value (dec) |
| --- | --- | --- |
| DELETE | 0x00010000 | 65,536 |
| READ_CONTROL | 0x00020000 | 131,072 |
| WRITE_DAC | 0x00040000 | 262,144 |
| WRITE_OWNER | 0x00080000 | 524,288 |
| SYNCHRONIZE | 0x00100000 | 1,048,576 |
| ACCESS_SYSTEM_SECURITY | 0x01000000 | 16,777,216 |
| GENERIC_ALL | 0x10000000 | 268,435,456 |
| GENERIC_EXECUTE | 0x20000000 | 536,870,912 |
| GENERIC_WRITE | 0x40000000 | 1,073,741,824 |
| GENERIC_READ | 0x80000000 | 2,147,483,648 |

Computed from those constants: the total mask space is 2^32 =
4,294,967,296; the per-object-type specific-rights subspace is 2^16 =
65,536; the ten named standard and generic bits combine to
0xF11F0000. Decision rule for the census: an access-check audit prices
each object type at its 65,536 specific-right combinations plus the ten
named bits — a guard cannot be argued "complete" without stating which
of that space it actually checks.

### 2.2 The enumeration-toolset growth (W3's arithmetic, computed)

From the public package pages and manifest, transcribed and counted by
code this forge (the instrument's own public record):

| Snapshot | Listed commands | Source |
| --- | --- | --- |
| v1.1.14 | 65 (56 cmdlets + 9 functions) | package page listing |
| v1.1.17 | 118 declared exports (56 + 62) | module manifest |
| v1.1.33 | 75 (66 cmdlets + 9 functions) | package page listing |

Computed: the page-listed surface grew 65 → 75 (+10, +15.4%) between
the two listed snapshots; the manifest at the intervening version
declares 118 exports — 43 more than either page listing shows. Decision
rule: the census pins the instrument by version AND by manifest count
where available; a discrepancy between the page and the manifest is
recorded, never averaged away.

### 2.3 The link-type availability matrix (M3's template row)

The documented 2015 taxonomy, held as the matrix's template:

| Primitive | Creatable by |
| --- | --- |
| Object-manager symbolic link | low-privileged user |
| Registry key symbolic link | low-privileged user |
| NTFS mount point | low-privileged user |
| NTFS symbolic link | administrator only |

Computed: 4 documented types, 3 user-creatable, 1 administrator-only.
Every new primitive row cites its precondition the same way.

### 2.4 The lineage's measured footprints (census anchors)

| Measurement | Value | Source |
| --- | --- | --- |
| MSRC 2015 credits (October–December window read) | 3 rows (MS15-115/CVE-2015-6113; MS15-111/CVE-2015-2553; MS15-111/CVE-2015-2554) | MSRC acknowledgments 2015, portion read |
| Public repositories under the lineage's account | 37 | profile page |
| Pinned reference instruments (stars) | the sandbox analysis suite at 2.3k; the COM viewer at 1.4k; the PoC packer at 1.3k | repository pages |
| First Microsoft bounty payout | $100,000 (2013, mitigation bypass) | press record, 2013 |

## 3. The boundary crosswalk (M5's schema)

The vendor's own boundary documentation is a census input: pulled fresh
at engagement time, cited by section — the organ never restates the
vendor's taxonomy from memory (the record shows the taxonomy moves:
mitigations backported across generations, dispositions argued per
issue). The crosswalk files, for every finding:

1. **chain** — the step list, one primitive per step, each with its
   census row and ledger id;
2. **taxonomy row** — the documented boundary the chain crosses, cited,
   OR the named seam where no row exists;
3. **disposition** — the vendor's verdict where one exists, quoted and
   dated;
4. **residual-risk row** — stopgap status, structural fix named, re-test
   trigger, date.

## 4. The composition rules (M4's discipline)

1. One primitive per step; one variable per step; a step that changes
   two things is two steps, each with its own control.
2. n_runs ≥ 2 on load-bearing cells (A8); a cell that flips between
   runs is re-run at n ≥ 3 and the instability is recorded as the
   cell's own data.
3. The demonstration proves the seam, not the impact: the chain's reach
   is the evidence; impact claims run the house report gates.
4. A primitive's precondition is checked against the census principal
   BEFORE the step is written — falsified primitives shrink the matrix
   on record, they do not disappear.
5. The chain stops at the first seam: composing across two seams in one
   chain is two findings, filed separately.
