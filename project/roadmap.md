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

## Deliberately deferred

Not started, and not to be started, until the gate that needs them:

PCB design, enclosure and ingress protection, wireless/LoRa, cloud implementation, portal,
DSP implementation, classification or ML, vibration compliance calculations (e.g. structural
damage or human-comfort standards), certification and regulatory work, multi-node time
synchronisation, production test, manufacturing.

Naming any of these here is scope *direction*, not scope commitment.
