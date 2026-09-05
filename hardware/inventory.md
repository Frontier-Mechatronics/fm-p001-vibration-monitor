# Bench inventory

The canonical record of physical hardware available to this project. Referenced by
`project/status.yaml` and by experiment records; **not duplicated** anywhere else.

Last updated: 2026-09-05.

## Scope

This is a working inventory of equipment relevant to the current and next gate, not a
laboratory asset register. Items are added when a gate needs them, not catalogued in
advance. Mounting and fixture hardware is deliberately **not** inventoried — see
[Fixtures](#fixtures-and-mounting) below.

## How to read this

**Nothing here has been measured by this project.** Every specification is manufacturer
documentation — `predicted`, in the language of `AGENTS.md` §2. No item has produced
evidence, and no claim about any item's real behaviour exists.

| Availability | Meaning |
|---|---|
| `available` | Physically in hand and usable now |
| `on order` | Purchased, not yet delivered — **may not be relied on for experiment scheduling** |
| `not available` | Identified as potentially useful; not purchased |

Serial numbers, asset IDs and calibration state are recorded as `unknown` where they have
not been established. They are never guessed: `experiments/evidence.md` requires instrument
identity and calibration state in every evidence manifest, so these fields must be filled by
the human engineering lead before evidence is recorded, not back-filled afterwards.

### This is planning data, not evidence provenance

This inventory says what kind of equipment exists. It is **not** the provenance record for
any measurement, and referencing it from a manifest does not discharge the provenance
requirement.

An experiment record and its manifest must independently identify:

- **which** physical board and sensor unit was used, not merely the model
- the assembled hardware revision (`HW-node-rNN`)
- the interconnect as actually wired
- the probe points and ground reference used for each capture

Those belong in `experiments/EXP-nnnn/` because they change between runs while this file does
not. A model name is not an identity.

---

## Measurement instruments

| Instrument | Role | Availability | Serial / asset ID | Calibration |
|---|---|---|---|---|
| Siglent SDS1202X-E digital oscilloscope | **Primary G1 timing and electrical evidence instrument** | available | unknown | unknown |
| HDS272S handheld oscilloscope (70 MHz class) | Secondary / portable. **Not** the primary metrology instrument | available | unknown | unknown |
| Rigol DP932E bench power supply | Controlled bring-up and current-limited power work | available | unknown | unknown |
| Logic analyser (Saleae-class) | Multi-signal digital capture | **not available** — deliberately deferred | — | — |

### Constraint worth knowing before EXP-0001 is designed

Manufacturer documentation lists the SDS1202X-E as a **two-channel** instrument. The
currently anticipated G1 arrangement uses both:

```text
sensor DRDY or equivalent  → CH1
MCU GPIO timing marker     → CH2
```

That leaves **no third channel** for SPI chip-select or clock, so sensor timing, firmware
service timing and bus activity cannot all be observed in a single capture. This shapes what
one capture can prove and may require several captures with different probe arrangements.

Flagged rather than solved: the measurement methodology is not fixed until the sensor
interface is confirmed on real hardware.

### Absence of a logic analyser does not block G1

A Saleae-class analyser is planned and deliberately deferred. G1's independent timing
evidence comes from the Siglent oscilloscope. A logic analyser would be procured only if an
experiment demonstrates a limitation the oscilloscope cannot overcome — an explicit
experimental limitation, per the procurement rule below.

---

## MCU and development boards

All `available`. None is a product selection — a claim that means nothing on its own, and
is given teeth by the R-024 checkpoint rather than by assertion.

| Board | Notes |
|---|---|
| **STM32 Nucleo F411RE** | **Preferred experimental host for G1.** Already available. Headroom for acquisition work is `assumed` — inferred from the device class, not derived from a stated acquisition workload and not measured |
| Nordic nRF52840 Development Kit | |
| Arduino Nano 33 IoT | |
| STM32 Nucleo F030R8 | |
| STM32 "Blue Pill" | |
| Elegoo UNO R3 | |

> **The F411RE is an experiment platform, not the product MCU.** The experimental platform
> and the final product platform are separate questions, decided by different evidence at
> different gates. No ADR selects STM32F4, the F411RE, or any MCU family for SV1, and none
> should be written on the strength of G1 convenience.
>
> An earlier version of this note claimed experimental use "commits the product to nothing".
> That was rejected in review as untestable, and correctly: no observation could show it
> false, so it could never be enforced. What is testable is when lock-in has **already
> happened** — see the R-024 checkpoint in [`project/risks.md`](../project/risks.md), which
> runs before G2 opens.

## Debug and interface hardware

| Item | Availability | Role |
|---|---|---|
| ST-Link STM8/STM32 V2 emulator / debug probe | available | Programming and debug for STM32 targets |
| Waveshare USB-to-TTL (USB-C) | available | Host serial link for firmware diagnostic output |

## Sensor evaluation hardware

| Item | Qty | Availability | Role |
|---|---|---|---|
| Analog Devices EVAL-ADXL355-PMDZ | 3 | **on order** | G1 acquisition platform; likely G2 characterisation platform |

**Epistemic status: approved as an experimental G1/G2 platform only.** This is **not**
selection of the ADXL355 as the SV1 product sensor, and no ADR selects it.

Expected from manufacturer documentation, none verified by this project: three-axis sensing,
a documented digital interface, PMOD form factor, SPI accessibility, exposed data-ready /
interrupt signalling suitable for direct timing observation, and performance headroom
sufficient for early acquisition and characterisation work — the last of these `assumed`
rather than read from a specification.

Those are the *reasons for choosing it experimentally*. They are `predicted`, not measured,
and must not be restated as properties of the delivered hardware. Nothing about these boards
is known to this project until one is on the bench and observed.

## Stimulus hardware

| Item | Qty | Availability | Role |
|---|---|---|---|
| Vybronics VC1020B111F ERM vibration motor | 3 | **on order** | Repeatable low-complexity vibration excitation for G1/G2 bench work |

**These are not calibration references.** Their datasheet values are manufacturer-specified
and `predicted`; this project has measured nothing. Any resulting plate acceleration or
vibration amplitude is **unknown** until measured.

Their role is to provide a *controlled, repeatable directional physical stimulus* — not a
*known vibration magnitude*. G1 may claim direction and repeatability. It may not claim
magnitude, which requires the traceability deferred to G2.

## Interconnect

| Item | Qty | Availability | Role |
|---|---|---|---|
| Digilent 240-110 Pmod split cable | 2 | **on order** | Connect the ADXL355 PMOD interface to the Nucleo F411RE and bench wiring; access to SPI and timing signals |

No custom adapter PCB is justified. PCB work is gated at G8 and requires evidence that an
off-the-shelf assembly cannot provide (`AGENTS.md` §8).

## Fixtures and mounting

**Not inventoried, and deliberately so.** Fixture needs follow from an experiment that
cannot run without them:

```text
experiment question → required fixture → what already exists?
  → identify only the gap → acquire locally if justified
```

The likely G1 arrangement uses a simple rigid carrier plate or bench structure, controlled
motor excitation, the ADXL355 board mechanically attached to the test object, and
oscilloscope observation of timing signals. **Exact mounting is unresolved.**

Mounting and coupling are a **G2 measurement-system concern** and must not be treated as
solved in G1. A fixture is part of the measurement: its mass, stiffness and coupling change
what the sensor sees. G1 works around this by claiming timing, not magnitude.

## Procurement rule

> Additional procurement must be justified by an explicit experimental limitation.

A standing Frontier Mechatronics rule. Do not propose purchases because they may be useful
later; the first order is complete. When an experiment demonstrates it cannot answer its
question with what is in hand, that limitation is the justification — and it is recorded in
the experiment before the purchase, not after.

## Hardware revision identity

Once the ADXL355 boards arrive and are wired to a host, the assembly becomes a node under
`HW-node-rNN` and gets a `revisions.md` in `hardware/node/` (see `hardware/README.md`).
Nothing is assembled yet, so no revision exists.
