# FM-P001 risk register

Living register. Risks are reviewed when a gate opens or closes, and whenever evidence
changes a likelihood or impact. Each risk names the gate at which it should become
*decidable* — the point where evidence can retire or confirm it.

Levels: L = likelihood, I = impact, on `low / med / high`.

## Engineering / technical

| ID | Risk | L | I | Decidable at | Current mitigation |
|---|---|---|---|---|---|
| R-001 | Actual sample timing differs materially from firmware's claim (jitter, drift, dropped samples), invalidating frequency-domain work | high | high | G1 | Measure rate and jitter on an instrument, never trust firmware self-reporting |
| R-002 | Measurements are not traceable to physical units, so results are self-referential | high | high | G2 | Defer absolute claims to G2; label pre-G2 results as relative |
| R-003 | Sensor dynamic range / bandwidth inadequate for real construction vibration amplitudes | med | high | G2 | Treat sensor as a candidate; characterise before committing |
| R-004 | Event detection produces excessive false positives or misses real events | med | high | G3 | Detection thresholds derived from measured data, not assumed |
| R-005 | Pre/post-event buffering loses data on power interruption | med | high | G4 | Explicit power-loss fault injection at G4 |
| R-006 | Constrained wireless link cannot carry the intended event payload within the power budget | high | high | G7 | Payload size becomes a G3 design constraint; measure before committing to a radio |
| R-007 | Custom PCB fails to reproduce breadboard-measured behaviour | med | high | G8 | Retain breadboard evidence as the reference; A/B against it |
| R-008 | Time base drift across nodes prevents correlating multi-node events | med | med | G9 | Deferred; do not design for it before G5 evidence exists |
| R-009 | Field environment (temperature, mounting, coupling, noise) invalidates lab results | high | high | G10 | Mounting and coupling treated as measurement variables, recorded in every experiment |
| R-010 | Single two-channel oscilloscope cannot observe sensor timing, firmware timing and bus activity simultaneously, so a correlated fault could be missed | med | med | G1 | Multiple captures under different probe arrangements; a logic analyser only if an experiment demonstrates the limitation (DQ-005) |
| R-011 | Instrument calibration state is unknown, so timing evidence has no stated uncertainty | med | med | G1 | Record serials and calibration before evidence is taken (HA-005); state measurement uncertainty in every manifest |

## Program / process

| ID | Risk | L | I | Decidable at | Current mitigation |
|---|---|---|---|---|---|
| R-020 | Agents assert hardware behaviour without evidence, and it enters the record as fact | high | high | continuous | Physical evidence rule (AGENTS.md §2); unsupported claims are review-blocking defects |
| R-021 | Scope creep toward the "final product" before evidence justifies it | high | high | continuous | Gate discipline; scope changes require an ADR |
| R-022 | Harness overhead exceeds its value and slows engineering down | med | med | after first completed G1 experiment | Review rule below; a condition of the G0 acceptance |
| R-023 | Duplicated project state drifts between documents | med | med | continuous | Single canonical `project/status.yaml`; checked by `tools/validate_repo.py` |
| R-024 | Early component choices become de-facto irreversible through accumulated code | med | high | G1→G2 checkpoint | Components stay explicitly "candidate" until an ADR decides them. Live from 2026-09-05: F411RE and ADXL355 in use as experiment platforms with no ADR selecting either. Enforced by the checkpoint below, not by assertion |
| R-025 | Evidence volume (raw captures, datasets) outgrows git | med | med | G2 | Convention now, storage decision when it actually hurts |
| R-026 | Long gaps between sessions lose engineering context | med | med | continuous | Repository is the memory: status.yaml, gates, experiments, ADRs |

## Safety / physical

| ID | Risk | L | I | Decidable at | Current mitigation |
|---|---|---|---|---|---|
| R-040 | Bench work involves mains power, mechanical energy or moving fixtures | med | high | continuous | Human owns all physical setup and safety; agents never direct unsupervised physical action |
| R-041 | Field deployment on a real construction site introduces access and site-safety obligations | med | high | G10 | Out of scope until G10; site requirements to be defined with the site owner |

## R-024 checkpoint — before G2 opens

Required by Codex review (`MSG-20260905T032337Z-d542-codex`), which rejected the earlier
assurance that experimental use of the F411RE and ADXL355 "commits the product to nothing".
That claim was untestable: no observation could show it false, so it could never be enforced,
and repeating it in four documents made it less likely to be examined rather than more.

What *is* testable is when lock-in has **already occurred**:

> Lock-in has occurred when a G1-specific register map, HAL or peripheral model, pinout,
> record format, test fixture, or requirement has become a prerequisite for G2 work without
> being labelled disposable or reviewed as a product choice.

That is observable, and it is checked at a fixed point rather than continuously worried about.

### The checkpoint

Before G2 opens, inventory every board- or sensor-specific dependency that G1 produced, and
record each as exactly one of:

| Classification | Meaning |
|---|---|
| **Isolated / disposable** | Confined to G1 artifacts, discarded when the platform changes. No further action |
| **Retained as an explicit experiment constraint** | Carried forward knowingly, recorded as a constraint on later work, still not a product choice |
| **Needs an ADR or comparative experiment** | Has become a de-facto product decision. Decide it deliberately, or gather the evidence to decide it |

Candidate dependency classes to inventory: sensor register map and configuration sequence;
MCU HAL and peripheral model; interrupt and timing model; pinout and interconnect; sample
record and file format; fixture and mounting arrangement; any requirement whose numeric value
came from what this hardware happened to do.

**A second platform is not required to satisfy this checkpoint.** Porting to prove
portability would be exactly the speculative work the program is meant to avoid. The
checkpoint asks what was built and how it is classified, not that it be rebuilt.

Anything landing in the third column before G2 opens is the finding. That is the point.

### Event trigger — classify at the moment of spread

The before-G2 checkpoint is late if a dependency becomes shared while G1 is still open.
Perform the **same three-way classification immediately** before a board- or sensor-specific
dependency is:

- used outside EXP-0001 support;
- retained as shared firmware or tooling; or
- made a prerequisite for another G1 change.

Those are the three ways a dependency stops being confined to one experiment. Classifying at
that moment costs almost nothing, because whoever is about to spread it already has the
context; discovering it at the G1→G2 checkpoint costs whatever was built on top in between.

This is an **event trigger, not a cadence** (required by `MSG-20260905T032805Z-c949-codex`).
There is no periodic review to schedule, remember or skip — the classification is part of the
act of reuse. A time-based cadence would have been a number invented without evidence, which
is the failure mode this project exists to avoid.

**The before-G2 checkpoint remains mandatory** and catches anything the trigger missed. The
trigger prevents early capture; the checkpoint is the backstop.

## R-022 review rule

A condition attached to the human engineering lead's G0 acceptance, and specified by the
G0 architecture review. After the **first completed experiment**, ask:

1. Which artifacts were naturally useful?
2. Which required duplicate entry?
3. Which were never consulted?
4. Which omissions caused confusion?
5. How much agent effort went into maintaining process rather than doing engineering?

Delete or simplify anything that fails that test. The question is not file count; it is
whether maintaining the artifacts displaces engineering.

No compliance or regulatory risks are listed. That work has not started and inventing its
obligations now would be speculation (AGENTS.md §8).
