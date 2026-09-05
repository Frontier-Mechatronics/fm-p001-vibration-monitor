# System overview (working)

Status: **working picture, not a commitment.** Every element below is technology-neutral.
Committed decisions are in `docs/decisions/`; the "not decided" list there governs.

## Signal chain

```text
   physical vibration
          │
          ▼
   [1] vibration sensor              ── transduction, axes, range, bandwidth
          │
          ▼
   [2] acquisition hardware          ── conditioning, digitisation, timing source
          │
          ▼
   [3] MCU firmware                  ── sampling, buffering, timebase, health
          │
          ▼
   [4] DSP / event detection         ── triggering, feature extraction
          │
          ▼
   [5] local waveform storage        ── pre/post-event retention, durability
          │
          ▼
   [6] device communications         ── framing, integrity, retry, backpressure
          │
          ▼
   [7] Linux edge gateway            ── reception, buffering, site-local service
          │
          ▼
   [8] local persistence / intelligence  ── durable store, offline operation
          │
          ▼
   [9] cloud ingestion               ── authenticated intake, de-duplication
          │
          ▼
  [10] portal / analytics            ── inspection, history
```

## Boundaries — where the engineering difficulty concentrates

| Boundary | Central question | Decided at |
|---|---|---|
| [1]→[2] | Is the analogue signal digitised without losing what matters? | G1–G2 |
| [3]→[4] | Is the sample stream continuous with a known, measured timebase? | G1 |
| [4]→[5] | Is an event captured with enough context, including before the trigger? | G3–G4 |
| [5]→[6] | Can retained data leave the node within the link and power budget? | G6–G7 |
| [6]→[7] | Is a partial or corrupt transfer detected rather than silently accepted? | G5 |
| [7]→[9] | Does the system behave correctly when the cloud is absent? | G5–G6 |
| [9]→[10] | Is an event inspectable with its provenance intact? | G6 |

## Cross-cutting concerns

**Timebase.** Every stage depends on time being meaningful. The node's timebase accuracy,
its relationship to gateway and cloud time, and drift over a deployment are unresolved and
affect `SV-SYS-002`. Multi-node correlation (G9) makes this harder; do not design for it
yet.

**Provenance.** Hardware unit, hardware revision, firmware revision and configuration must
travel with the data. Data whose origin is unknown cannot be used as engineering evidence
(`SV-SYS-002`).

**Data volume.** Whether continuous 3-axis acquisition at the provisional ~1 kHz target
will exceed the eventual link and power budget is **unknown**. Local detection and feature
extraction are current product constraints (`SV-DSP-001`, `SV-DSP-002`); G3 and G7 must
measure the payload and budget that justify, alter or retire them.

**Failure behaviour.** Every boundary has a failure mode: sensor absent, buffer overrun,
storage full, link down, cloud unreachable. A field instrument is defined as much by its
degraded behaviour as its nominal behaviour, which is why fault injection is part of the
experiment method rather than an afterthought.

**Power.** Untouched. It becomes a first-order constraint at G7 and will retroactively
constrain [1]–[6]. Recorded here so it is not forgotten, not to be designed for now.

## Explicitly undecided

Sensor part, MCU/SoC, timing source, storage medium, node↔gateway transport and protocol,
gateway hardware and OS, cloud provider and services, portal technology, data format,
enclosure and mounting.

Naming a stage in the diagram does not select a technology for it.
