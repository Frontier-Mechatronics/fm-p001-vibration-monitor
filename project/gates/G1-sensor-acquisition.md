# G1 — Sensor acquisition (preliminary)

| Field | Value |
|---|---|
| Gate | G1 |
| Title | Sensor acquisition |
| Status | see [`project/status.yaml`](../status.yaml) (authoritative) |
| Definition maturity | **preliminary — pass criteria NOT agreed** |

> This file exists to establish direction, not commitment. Its criteria are **not** agreed.
> G1 is scoped properly only after G0 is accepted and the human confirms which hardware is
> physically available (`HA-002` in `project/status.yaml`).

## Intent

Demonstrate, with physical evidence, that a real accelerometer can be read by real firmware
at a known, measured sample rate, and that the resulting data is trustworthy enough to
build on.

## Questions G1 should answer

1. What sample rate does the acquisition path *actually* achieve, measured on an
   instrument — not as reported by firmware?
2. How much does the sample interval vary (jitter), and is that variation acceptable for
   later frequency-domain work?
3. Does each axis respond to a controlled, repeatable directional stimulus in the expected
   direction? (Not "known" magnitude: calling a hand-applied stimulus known implies a
   traceability G1 does not have.)
4. What is the at-rest noise floor in raw counts or explicitly provisional scaled units?
   Traceable engineering units are deferred to G2.
5. What happens when the sensor link fails mid-acquisition — is the failure detected, and
   is corrupted data distinguishable from valid data?

## Candidate pass criteria (draft, not agreed)

- Firmware acquires 3 axes continuously from a physical accelerometer.
- Sample rate is measured independently of firmware (oscilloscope / logic analyser) and the
  measured value, with tolerance, is recorded as evidence.
- Sample interval jitter is measured and recorded.
- Per-axis response to a controlled, repeatable directional stimulus is observed and
  recorded, in direction only unless a reference instrument provides magnitude.
- At-rest noise floor is measured and recorded in raw counts or explicitly provisional
  scaled units; traceable engineering-unit characterisation is deferred to G2.
- A sensor-link fault is injected and the firmware's detection behaviour recorded.
- All of the above referenced from at least one experiment record with accepted evidence.

## Architect's guidance (G0 architecture review, 2026-09-05)

- **1 kHz is an experimental target, not a product requirement.** G1 configures a nominal
  target where the hardware permits and independently measures what the system actually
  produces. It must **not** back-derive the product sampling requirement from whatever the
  convenient hardware achieves — that reverses the engineering logic. A defensible rate
  requires the chain: phenomenon of interest → required bandwidth → anti-alias strategy →
  sampling requirement.
- **Three axes is working experimental scope**, not yet a derived product requirement.
- **Prove acquisition timing before attempting any calibrated vibration claim.**
- **Isolate acquisition.** Establishing traceable magnitude first would couple sensor
  response, mechanical coupling, calibration, firmware, timing and transport into one
  unresolvable result. That is why G2 follows G1.

### Proposed first experiment

Recommended by the architecture review; **not yet drafted**, pending the inventories:

> Can the existing bench hardware produce a continuous three-axis sample stream whose actual
> sample timing can be independently measured and reconciled with the firmware record?

EXP-0001 should **not** attempt sensor suitability for construction, calibrated magnitude,
product bandwidth, final sample rate, final MCU, DSP suitability or mounting design.

> "The first experiment should be almost boring. That is desirable." — it establishes the
> evidence chain every later experiment depends on.

**Procurement rule:** procure for G1 only if hardware already owned cannot expose what G1
needs to measure. Procurement then follows from a demonstrated experiment limitation, never
from anticipated product architecture.

## Anticipated bench arrangement

Hardware is recorded in [`hardware/inventory.md`](../../hardware/inventory.md); it is not
restated here. **This arrangement is anticipated, not validated** — the measurement method
is not fixed until the sensor interface is confirmed on real hardware, and the ADXL355
boards have not been delivered.

```text
        EVAL-ADXL355-PMDZ
                │
               SPI
                │
         Nucleo F411RE
                │
                ├── UART / debug ─────────→ host
                │
                └── GPIO timing marker ───→ Siglent CH2

        ADXL355 DRDY ────────────────────→ Siglent CH1
```

The point of the arrangement is to compare three things that are usually assumed to agree:

| Source | What it tells us |
|---|---|
| Sensor-generated timing (DRDY) | When the sensor says a sample is ready |
| Firmware service timing (GPIO marker) | When firmware actually acts on it |
| Retained sample sequence | What ended up in the record |

Firmware self-reporting is not evidence for any of this (ADR-0004). The oscilloscope
observes the first two independently of the code under test, which is the entire reason the
arrangement exists.

### Orientation and stimulus — stays qualitative

EXP-0001 **must** name the sensor coordinate convention and the fixture and orientation used,
so that a directional observation can be repeated and compared.

EXP-0001 **must not** infer calibrated magnitude from that stimulus, or treat mounting as
solved. Naming an orientation makes an observation repeatable; it does not make it traceable.
Magnitude belongs to G2, and mounting design is a G2 measurement-system concern that G1 works
around rather than answers.

The distinction to hold: G1 may claim *this axis responded, in this direction, repeatably,
in this arrangement*. It may not claim *this axis responded by this much*.

### What G1 should ultimately measure

- actual data-ready / sample period
- interval variation
- sensor-ready → firmware-service latency, where observable
- missing or gapped acquisition behaviour
- reconciliation between physical timing evidence and the firmware record

**None of this is known.** No hardware has been measured by this project. These are the
quantities the experiment must produce, not expectations about what it will find.

### Known constraint

The primary oscilloscope is a two-channel instrument (manufacturer specification). DRDY plus
a GPIO marker consumes both channels, leaving none for SPI chip-select or clock — so bus
activity cannot be observed in the same capture as the timing pair. Whether EXP-0001 needs
simultaneous bus observation, or can proceed with separate captures under different probe
arrangements, is open (DQ-005). No logic analyser is available, and its absence does not
block G1.

## Requirements likely in scope

`SV-ACQ-001`, `SV-ACQ-002`, `SV-SYS-002`. To be confirmed when G1 opens.

## Known open questions blocking G1 definition

- ~~Which accelerometer and MCU platform?~~ **Resolved as an inventory** (`DQ-002`,
  2026-09-05): Nucleo F411RE as experimental host, EVAL-ADXL355-PMDZ as experimental
  acquisition platform. No ADR selects either. Whether that remains true in practice is
  tested by the **R-024 checkpoint before G2 opens**, not asserted here.
- What jitter is actually acceptable? This should be *derived* from the intended DSP, not
  guessed now.
- No reference accelerometer or shaker is available. The ERM motors provide a controlled,
  repeatable directional stimulus, **not** a magnitude reference, so G1 is limited to
  direction and repeatability with absolute magnitude deferred to G2.
- Mounting is unresolved and is not G1's to solve. How the sensor couples to the excited
  structure changes what it measures; G1 works around this by claiming timing rather than
  magnitude.
- Which units, if any, can be used before G2 without being mistaken for calibrated physical
  units? Raw counts are the safe default.
