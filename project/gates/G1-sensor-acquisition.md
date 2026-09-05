# G1 — Sensor acquisition (preliminary)

| Field | Value |
|---|---|
| Gate | G1 |
| Title | Sensor acquisition |
| Status | see [`project/status.yaml`](../status.yaml) (authoritative) |
| Definition maturity | **preliminary — direction only** |

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
3. Does each axis respond to a known physical stimulus in the expected direction and
   approximate magnitude?
4. What is the at-rest noise floor in raw counts or explicitly provisional scaled units?
   Traceable engineering units are deferred to G2.
5. What happens when the sensor link fails mid-acquisition — is the failure detected, and
   is corrupted data distinguishable from valid data?

## Candidate pass criteria (draft, not agreed)

- Firmware acquires 3 axes continuously from a physical accelerometer.
- Sample rate is measured independently of firmware (oscilloscope / logic analyser) and the
  measured value, with tolerance, is recorded as evidence.
- Sample interval jitter is measured and recorded.
- Per-axis response to a known physical stimulus is observed and recorded.
- At-rest noise floor is measured and recorded in raw counts or explicitly provisional
  scaled units; traceable engineering-unit characterisation is deferred to G2.
- A sensor-link fault is injected and the firmware's detection behaviour recorded.
- All of the above referenced from at least one experiment record with accepted evidence.

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
