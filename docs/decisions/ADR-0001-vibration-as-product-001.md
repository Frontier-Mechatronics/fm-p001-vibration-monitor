# ADR-0001 — Vibration monitoring as FM-P001

| Field | Value |
|---|---|
| Status | accepted |
| Date | 2026-09-05 |
| Deciders | Human engineering lead |
| Supersedes | none |
| Superseded by | none |

## Context

Frontier Mechatronics needs a first end-to-end product-development program. The program's
purpose is as much to establish a repeatable engineering capability — physical measurement,
firmware, edge, cloud, and a disciplined evidence process — as to produce a specific device.
A first physical signal had to be chosen before any engineering could begin.

## Decision

FM-P001 is a construction and engineering vibration-monitoring system, working family `SV`,
initial model `SV1`. Vibration is the first physical signal the program will measure.

This decides the *domain*. It decides nothing about sensor, hardware architecture, market
segment or commercial form.

## Alternatives

| Alternative | Why not chosen |
|---|---|
| Temperature / environmental monitoring | Signal is slow and undemanding; would not exercise sampling, timing, bandwidth or data-volume problems |
| Acoustic monitoring | Higher bandwidth and data rates raise the entry cost before basic capability exists; also carries privacy considerations |
| Electrical power/energy monitoring | Mains-connected measurement adds safety and isolation burden at the outset |
| Defer and build capability with no product target | Without a concrete physical target, engineering discipline has nothing to bite on |

## Rationale

Vibration is demanding enough to be a real engineering exercise — it forces honest treatment
of sample rate, jitter, dynamic range, event detection, storage volume and link budget —
while remaining observable with ordinary bench instruments. Construction and engineering
monitoring is a plausible real application, which keeps requirements grounded rather than
academic.

## Consequences

- Timing and sampling correctness become first-order concerns from G1 onward.
- Data volume forces early attention to event detection and compact representation, rather
  than continuous streaming.
- Requires physical stimulus for testing; some evidence will need fixtures the program does
  not yet have.
- Absolute measurement accuracy will eventually require reference instrumentation
  (deferred to G2).

## Evidence

None. This is a program-direction decision, not a technical claim about physical behaviour.

## Revisit triggers

- Bench evidence shows vibration measurement of useful quality is not achievable within a
  plausible cost and power envelope.
- The intended application is found to require compliance work disproportionate to the
  program's stage.
- A different first signal is shown to build the same engineering capability at materially
  lower cost.
