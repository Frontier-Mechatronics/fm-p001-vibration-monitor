# FM-P001 roadmap

Direction, not schedule. There are no dates: this is an evidence-driven program and each
step's cost is unknown until the step before it produces evidence.

Authoritative current state is `project/status.yaml`. Gate criteria live in
`project/gates/`. This file explains *why the gates are in this order*.

## Sequencing principle

Each gate should convert one uncertainty into evidence, using the smallest system that can
produce that evidence. The order below is chosen so that later, more expensive commitments
(custom PCB, wireless, field deployment) are made only after the measurements that justify
them exist.

| Gate | Converts this uncertainty into evidence |
|---|---|
| G0 | Can these four parties (human, Claude, Codex, ChatGPT) work coherently on one hardware program? |
| G1 | Can we acquire vibration data at a known, *measured* rate from real hardware? |
| G2 | Do our numbers mean anything in physical units, and what are our error bounds? |
| G3 | Can we detect events on-device and describe them compactly and correctly? |
| G4 | Can the device retain pre/post-event waveforms reliably, including across power loss? |
| G5 | Can an edge gateway receive, persist and serve event data without the cloud? |
| G6 | Can an event travel node → gateway → cloud and be inspected end to end? |
| G7 | Does the concept survive a constrained wireless link and a field power budget? |
| G8 | Does a custom board reproduce the measured behaviour of the breadboard system? |
| G9 | Does the system hold together with multiple nodes and shared time? |
| G10 | Does it produce trustworthy results in a real, uncontrolled environment? |

## Why vibration first

Vibration is a demanding but tractable first physical signal: it is continuous, has real
bandwidth and dynamic-range constraints, forces honest treatment of sampling and timing,
produces data volumes that make storage and link budgets matter, and has an obvious
real-world context in construction monitoring. It exercises the entire chain from analogue
physics to cloud analytics without requiring exotic instrumentation to observe.

## Architecture actions deferred to later gates

From the G0 architecture review (`project/reviews/G0-chatgpt-review-2026-09-05.md`). Recorded
here rather than in the gate files so each attaches to the gate that must satisfy it, and so
none is lost between now and then. None was a G0 blocker.

| Due before | Action |
|---|---|
| G1 opens | Retain 1 kHz explicitly as an experimental target, not a derived product requirement |
| During G1 | Prove acquisition timing before attempting any calibrated vibration claim |
| G2 opens | Define mounting, sensor coupling and measurement orientation as explicit requirements — mounting is part of the measurement chain, not enclosure design |
| G2 opens | Define whatever calibration/traceability requirement is needed to make physical-unit claims |
| G5 opens | Define device identity; configuration identity and versioning; message/data integrity; node↔gateway trust and security model; behaviour under duplicate, incomplete and corrupt transfers; configuration ownership and persistence |
| G5–G7 | Derive an offline-endurance target from deployment/domain evidence — the difference between 15 minutes and 2 weeks drives storage and protocol design |
| G5 | Refine ADR-0003's rationale toward monitoring continuity as a product principle, with site connectivity evidence determining the required endurance rather than justifying the decision |
| G7 | Production power budget, before wireless/custom-node decisions bind |
| G7–G8 | Firmware update/OTA requirement, before a deployed fleet architecture binds |
| G8–G10 | Environmental operating envelope |
| After first completed experiment | Review Harness v0.1 overhead under R-022 |
| Standing | Do not select the product accelerometer or MCU until experiment evidence creates a reason to |
| Standing | Procure only against an explicit experimental limitation, recorded in the experiment before the purchase |
| When an experiment demonstrates the need | Logic analyser (Saleae-class) — deferred; its absence does not block G1 |

One architectural principle added by the review, worth carrying forward:

> Owning the end-to-end product experience does not require manufacturing or implementing
> every underlying subsystem ourselves.

That becomes material for gateways, radio infrastructure and cloud components.

Site connectivity is worth a lightweight reconnaissance before G5/G7 choices become
expensive, rather than waiting for G10 — it need not be a formal experiment unless site
access is available.

## Deliberately deferred

Not started, and not to be started, until the gate that needs them:

PCB design, enclosure and ingress protection, wireless/LoRa, cloud implementation, portal,
DSP implementation, classification or ML, vibration compliance calculations (e.g. structural
damage or human-comfort standards), certification and regulatory work, multi-node time
synchronisation, production test, manufacturing.

Naming any of these here is scope *direction*, not scope commitment.
