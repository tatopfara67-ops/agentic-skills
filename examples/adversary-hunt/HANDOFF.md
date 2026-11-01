# Adversary handoff — case christmas-lab, engagement christmas-lab

## Summary
A 03:14 debug-console login anomaly from an unassigned in-lab address opened a Binary Brain hunt of 8 hypotheses (null auto-inserted). 3 decisive tests at the information floor of 3 localized the actor; two independent channels (netflow, host-audit) agree. compromised container in the build cluster is CONFIRMED and handed to lab IR for containment. Citations: R-001, R-008, R-009.

## Timeline (from records)
| When | Record | Event |
| ---- | ------ | ----- |
| 03:14 | R-001 | trigger: 03:14 auth log: 6 failed + 1 successful debug-console login from 10.10.4.23 (in-lab, unassigned in inventory) |
| +0h | R-002 | pre-register T-001 (netflow): 1.00 bits over 8 active |
| +0h | R-003 | T-004 tripwire REFUSED — tip-off gated while passive tests eliminate |
| +0h | R-004 | T-001 outcome=1: netflow history exists; 4 hypotheses die |
| +0h | R-005 | pre-register T-002 (netflow): 1.00 bits over 4 active |
| +1h | R-006 | T-002 outcome=1: lease renews from cluster bridge; null and colleague die |
| +1h | R-007 | pre-register T-003 (host-audit): 1.00 bits over 2 active |
| +1h | R-008 | T-003 outcome=1: container veth MAC prefix; runner dies |
| +1h | R-009 | H-004 CONFIRMED via two channels (netflow, host-audit) |

## Hypotheses

### H-004 compromised container in the build cluster
Severity: high — an unauthorized actor holds valid debug-console credentials and operates from a cluster container — R-009
- Closure: CONFIRMED — R-008, R-009
- Channels: netflow (R-004, R-006) + host-audit (R-008)
- impact-chain: stale DHCP lease on the cluster bridge → 6-fail-then-success login against the debug console (R-001) → authenticated debug-console access from 10.10.4.23, netflow- and host-audit-confirmed (R-004, R-008)
- canary: none during the trace — TIP-OFF discipline held (the tripwire attempt is the REFUSED record R-003); the credential-reset tripwire is IR's containment action at handoff, scheduled and owned by IR

### H-001 authorized or benign activity (null)
- Closure: FALSIFIED — eliminated by T-002 outcome 1 (R-006)

### H-002 colleague running an overnight build experiment
- Closure: FALSIFIED — eliminated by T-002 outcome 1 (R-006)

### H-003 decommissioned build runner with stale credentials
- Closure: FALSIFIED — eliminated by T-003 outcome 1 (R-008)

### H-005 compromised office workstation
- Closure: FALSIFIED — eliminated by T-001 outcome 1 (R-004)

### H-006 remote party using leaked VPN credentials
- Closure: FALSIFIED — eliminated by T-001 outcome 1 (R-004)

### H-007 log pipeline artifact (aggregator IP rewrite)
- Closure: FALSIFIED — eliminated by T-001 outcome 1 (R-004)

### H-008 attacker bridged onto the office WLAN
- Closure: FALSIFIED — eliminated by T-001 outcome 1 (R-004)

## Elimination table
| Hypothesis | Died on | Record |
| ---------- | ------- | ------ |
| H-005 office workstation | T-001 outcome 1 | R-004 |
| H-006 leaked VPN credentials | T-001 outcome 1 | R-004 |
| H-007 log pipeline artifact | T-001 outcome 1 | R-004 |
| H-008 WLAN-bridged attacker | T-001 outcome 1 | R-004 |
| H-001 null (authorized/benign) | T-002 outcome 1 | R-006 |
| H-002 overnight colleague | T-002 outcome 1 | R-006 |
| H-003 stale runner | T-003 outcome 1 | R-008 |

## Channel matrix
| Hypothesis survived | Channel | Test | Record |
| ------------------- | ------- | ---- | ------ |
| H-004 | netflow | T-001 | R-004 |
| H-004 | netflow | T-002 | R-006 |
| H-004 | host-audit | T-003 | R-008 |

## Uncertainty and leads
The hunt established WHAT and WHERE-within-our-perimeter: an actor operating from a build-cluster container holds valid debug-console credentials (R-009). It did not establish identity, intent beyond the observed access, or how the container was compromised — those are leads for IR with host-image forensics. The identity-channel tripwire (T-004) stays refused-and-parked (R-003): executing it is IR's containment decision, with this pack behind it.

## Handoff statement
Localization inside the authorized lab perimeter is complete: H-004, channels netflow (R-004, R-006) and host-audit (R-008). Identity, anything beyond this perimeter, and every tip-off action belong to lab IR with this pack as the evidentiary basis. Efficiency: 3 tests spent at a floor of 3.
