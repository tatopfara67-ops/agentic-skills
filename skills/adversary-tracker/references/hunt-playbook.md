# Hunt playbook — P0 through P6, with channels and test design

The phases map onto the 1994–95 hunt's shape (see
references/history-1995.md): everything before the first hypothesis is
about NOT destroying evidence; everything after is about spending bits
at the floor; the end is a handoff, never a confrontation.

## P0 — FREEZE (the Christmas Day discipline)

The scene is evidence; touching it is spending evidence. Before any
sbb call:

1. Start full packet capture on every sensor you control. Disk is
   cheaper than a second chance.
2. Do NOT power off or reboot the affected host — memory (connection
   tables, process state) dies with it. Isolate at the network layer
   only if containment is explicitly authorized, and record the moment
   of isolation.
3. Sync and record clock state of every sensor (NTP offset per host).
   Cross-sensor correlation is only as good as timestamp comparability.
4. Hash and snapshot what can be snapshotted without altering it
   (read-only mounts, `dd` of disks you can take offline).
5. Ledger every action of your own as a FACT record — including the
   freeze itself. The 1994 machines were studied, not scrubbed; that
   is why the attack could be reconstructed packet by packet.

## P1 — BASELINE

Signal is defined ONLY as deviation from measured normal (the spine's
calibration doctrine, applied defensively):

* Pull a representative window of your own logs: login cadence per
  account, source-address ranges per service, scheduled-job times.
* Record 3 CONTROL records that establish what normal looks like for
  the specific sensor that fired (the same three-observation pattern
  the content-discovery organ uses for its 404 baseline).
* If you cannot state what normal is, you cannot state what anomalous
  is — park the hunt and build the baseline first.

## P2 — CLASSIFY

Each incoming observation becomes exactly one FACT record, then one
bit: signal or noise. Rules:

* Classification is against P1's baseline, and the verdict names the
  baseline record it used.
* Noise is still recorded (a negative is an observation — spine
  doctrine).
* Do not batch-edit classifications later; if a verdict changes, that
  is a new record citing the old one.

## P3 — ENUMERATE

Hypotheses across five axes (declare as plain labels; the engine
numbers them and inserts the null):

| Axis | Question | Example labels |
| ---- | -------- | --------------- |
| identity | who is acting | "authorized ops automation", "compromised build container", "contractor with leaked creds" |
| location | where they sit | "office LAN", "cluster bridge network", "remote via VPN pool" |
| capability | what they can do | "valid credentials only", "root on one host", "subnet presence" |
| intent | what they want | "credential harvesting", "persistence", "recon of our sensors" |
| path | how they arrived | "phished session token", "stale DHCP lease reuse", "exposed debug console" |

Budget (R7): declare the space at a size you can actually halve —
8–16 hypotheses is a hunt; 200 is a census. Extend mid-hunt via
`sbb_declare` when eliminations teach you new suspects; eliminated
hypotheses stay dead (history is append-only).

## P4 — HALVE (test design)

A test is a question whose answer is one bit AND whose two answers
eliminate disjoint, roughly equal, halves. Design procedure:

1. List the active hypotheses in two columns: "would survive answer
   1" / "would survive answer 0". Unlisted hypotheses survive both
   (unsplit — allowed, but they lower the test's bits).
2. Compute the split; if it is worse than ~70/30, redesign the
   question before spending it.
3. Prefer channels you can read passively (see catalog below).
4. Pre-register via `sbb_decide` — the EXPERIMENT record freezes the
   partition before the world answers.

Channel catalog (declare at least two, from different rows):

| Channel | Passive sources | Typical questions |
| ------- | --------------- | ----------------- |
| netflow | VPC flow logs, router/switch counters, firewall logs | "did this source talk to X in the window?" |
| host-audit | auth logs, EDR telemetry, DHCP leases, process lineage | "what interface held this address?" |
| identity | IdP sign-in logs, credential age, MFA events | "when was this credential last legitimately used?" |
| external-passive | CT logs, passive DNS, WHOIS history | "what infrastructure does the relay domain have?" |
| temporal | clock skew, session cadence, job schedules | "does the actor keep our working hours?" |
| build/physical | MAC OUI, image manifests, badge/access data | "which image generates this fingerprint?" |

Tip-off taxonomy (Rule P). An action is TIP-OFF=1 if it changes any
state the adversary can observe: credential resets or lockouts,
blocking/allow-listing their source, "investigative" logins into
infrastructure they control, scanning their relay hosts. Reading logs,
flow records, and passive databases is quiet. The engine refuses
tip-off tests while passive eliminators remain; when passive reserves
are exhausted, running one is a deliberate, recorded choice — and in
this skill's doctrine it is IR's choice at containment time, not the
tracker's during the trace.

## P5 — FIX (two channels)

* The survivor must cross a second channel whose errors are
  uncorrelated with the first (pairs table in
  references/binary-brain.md §5).
* Build the channel matrix as you go: every RUN test contributes its
  channel to every hypothesis that survived it. The engine tracks
  this; your job is to DECLARE the second-channel test rather than
  accept a single-channel singleton.
* If the two channels ever disagree, the hypothesis space was wrong —
  that is the space-empty exit, a MISTAKE record, and re-enumeration.
  Disagreement is information, not failure.

## P6 — HANDOFF

* Write the pack from ledger records only (template:
  references/evidence-templates.md), audit it until exit 0.
* The pack states localization (which of YOUR assets, which channel
  pair) and explicitly does NOT pursue identity, physical location, or
  retaliation. Upstream providers, foreign infrastructure, and persons
  are law enforcement's lane — the 1995 hunt ended with the location
  handed to the FBI, not a knock by the tracker.
* Containment (the tip-off actions gated all hunt long) is executed by
  IR at this point, on their authority, with the hunt's evidence
  behind it.

## 1995 → now, the translation table

| 1995 artifact | Modern analogue in this playbook |
| ------------- | -------------------------------- |
| multi-site packet capture, tcpdump | P0 full capture; netflow channel |
| telephone switch / toll records | identity + temporal channels (operator-side records) |
| RF drive-test measurement | build/physical channel (artifact-level truth) |
| cloned-cell (ESN) expertise | knowing the substrate you defend (P1 baseline depth) |
| the patience of weeks | tip-off gate: passive bits first |
| FBI at the door | P6 handoff: the last mile is not ours |
