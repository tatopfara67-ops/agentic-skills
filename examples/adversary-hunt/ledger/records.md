R-001 | 2026-11-01T12:55:21Z | sbb | declare: hunt opened case=christmas-lab | hypotheses=8 (null auto-inserted) tests=4 |  | FACT | trigger=03:14 auth log: 6 failed + 1 successful debug-console login from 10.10.4.23 (in-lab, unass
R-002 | 2026-11-01T12:55:21Z | sbb | decide: pre-register T-001 (netflow, passive) | on 1 kills H-005,H-006,H-007,H-008 / on 0 kills H-001,H-002,H-003,H-004; 1.00 bits over 8 active |  | EXPERIMENT | partitions frozen before the outcome
R-003 | 2026-11-01T12:55:21Z | sbb | apply: T-004 refused | tip-off gated while passive tests eliminate (T-001, T-002, T-003) |  | REFUSED | Rule P — observe, never warn
R-004 | 2026-11-01T12:55:21Z | sbb | apply: T-001 outcome=1 | eliminated H-005,H-006,H-007,H-008; active=4 |  | FACT | netflow: 7 days of control-plane sessions from 10.10.4.23
R-005 | 2026-11-01T12:55:21Z | sbb | decide: pre-register T-002 (netflow, passive) | on 1 kills H-001,H-002 / on 0 kills H-003,H-004; 1.00 bits over 4 active |  | EXPERIMENT | partitions frozen before the outcome
R-006 | 2026-11-01T12:55:21Z | sbb | apply: T-002 outcome=1 | eliminated H-001,H-002; active=2 |  | FACT | dhcpd: 10.10.4.23 renews from br-cluster (00:16:3e:aa:04:d2)
R-007 | 2026-11-01T12:55:21Z | sbb | decide: pre-register T-003 (host-audit, passive) | on 1 kills H-003 / on 0 kills H-004; 1.00 bits over 2 active |  | EXPERIMENT | partitions frozen before the outcome
R-008 | 2026-11-01T12:55:21Z | sbb | apply: T-003 outcome=1 | eliminated H-003; active=1 |  | FACT | dhcpd client-id 02:42:ac:11:00:04 — container veth prefix
R-009 | 2026-11-01T12:55:21Z | sbb | confirm: H-004 | CONFIRMED via two channels (host-audit, netflow); tests used 3, floor 3 |  | FACT | compromised container in the build cluster — rule T satisfied
