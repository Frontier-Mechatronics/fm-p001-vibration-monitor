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

## Requirements likely in scope

`SV-ACQ-001`, `SV-ACQ-002`, `SV-SYS-002`. To be confirmed when G1 opens.

## Known open questions blocking G1 definition

- Which accelerometer and MCU platform? No decision has been made; candidates only
  (`DQ-002`). Whatever is already on the bench should be preferred for the first
  experiment — the point of G1 is to learn the measurement method, not to choose a part.
- What jitter is actually acceptable? This should be *derived* from the intended DSP, not
  guessed now.
- Is a reference accelerometer or shaker available for absolute magnitude comparison, or is
  G1 limited to relative/qualitative response with absolute accuracy deferred to G2?
- Which units, if any, can be used before G2 without being mistaken for calibrated physical
  units? Raw counts are the safe default.
