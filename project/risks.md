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

## Program / process

| ID | Risk | L | I | Decidable at | Current mitigation |
|---|---|---|---|---|---|
| R-020 | Agents assert hardware behaviour without evidence, and it enters the record as fact | high | high | continuous | Physical evidence rule (AGENTS.md §2); unsupported claims are review-blocking defects |
| R-021 | Scope creep toward the "final product" before evidence justifies it | high | high | continuous | Gate discipline; scope changes require an ADR |
| R-022 | Harness overhead exceeds its value and slows engineering down | med | med | after first completed G1 experiment | Review rule below; a condition of the G0 acceptance |
| R-023 | Duplicated project state drifts between documents | med | med | continuous | Single canonical `project/status.yaml`; checked by `tools/validate_repo.py` |
| R-024 | Early component choices become de-facto irreversible through accumulated code | med | high | G2 | Components stay explicitly "candidate" until an ADR decides them |
| R-025 | Evidence volume (raw captures, datasets) outgrows git | med | med | G2 | Convention now, storage decision when it actually hurts |
| R-026 | Long gaps between sessions lose engineering context | med | med | continuous | Repository is the memory: status.yaml, gates, experiments, ADRs |

## Safety / physical

| ID | Risk | L | I | Decidable at | Current mitigation |
|---|---|---|---|---|---|
| R-040 | Bench work involves mains power, mechanical energy or moving fixtures | med | high | continuous | Human owns all physical setup and safety; agents never direct unsupervised physical action |
| R-041 | Field deployment on a real construction site introduces access and site-safety obligations | med | high | G10 | Out of scope until G10; site requirements to be defined with the site owner |

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
