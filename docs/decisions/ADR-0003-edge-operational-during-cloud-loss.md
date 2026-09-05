# ADR-0003 — The edge must remain operational during cloud loss

| Field | Value |
|---|---|
| Status | accepted |
| Date | 2026-09-05 |
| Deciders | Human engineering lead |
| Supersedes | none |
| Superseded by | none |

## Context

The program **assumes** that the intended deployment environment — construction and
engineering sites — has poor, intermittent or sometimes absent connectivity. This premise
has not been measured. A monitoring system whose function depends on a live cloud connection
would fail if that assumption holds.

## Decision

Cloud connectivity is treated as **optional and intermittent**. Acquisition, event
detection, retention and node→gateway transfer shall continue to function while the cloud
is unreachable, and retained data shall be delivered once connectivity returns.

The cloud may be authoritative for long-term storage and analysis. It may not be required
for the device to do its job.

## Alternatives

| Alternative | Why not chosen |
|---|---|
| Cloud-dependent (stream-only) architecture | Would fail if the assumed target connectivity conditions hold; its link budget is unproven |
| Store-and-forward on the node alone, no gateway | Node storage and power limits are unknown; this alternative was not selected because it concentrates the unproven burden at the node |
| Decide later | This constraint shapes storage, buffering and protocol design, so deciding late means redesigning |

## Rationale

Offline capability is a functional requirement of the environment, not a resilience feature
added later. It constrains storage sizing, buffering, transfer protocol and acknowledgement
design, so it must be established before those are built. It also implies data must be
durable at two points — node and gateway — which is a design constraint rather than an
implementation detail.

## Consequences

- Requirement `SV-GW-002` exists and is a first-class G5 concern.
- Storage sizing at node and gateway must be driven by a defined offline endurance, still
  undefined (open question).
- Transfer must be resumable and must tolerate duplicates; exactly-once delivery cannot be
  assumed.
- Reconciliation and de-duplication become cloud-side concerns at G6.
- Fault-injection testing of connectivity loss is required, not optional.

## Evidence

None yet. The environmental premise (poor site connectivity) is currently `assumed` from
domain knowledge and has not been measured. Site connectivity measurement should form part
of G10 planning, and could retire or sharpen this assumption earlier if a site is available.

## Revisit triggers

- Site connectivity measurements show reliable connectivity is realistically available.
- Offline endurance requirements are found to demand storage that is not economically
  viable, forcing a different split of responsibility.
- The product's target application changes to a connected, permanent-infrastructure setting.
