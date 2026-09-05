# Node firmware

Source and build for the sensing-node firmware.

Empty at G0. No MCU platform, toolchain or build system has been selected; all are
candidates. The selection should follow from what hardware is physically available for G1,
and should be recorded as an ADR only when it becomes a commitment rather than a
convenience.

The first firmware should be the smallest thing that lets a sample rate be measured on an
instrument — not an architecture.
