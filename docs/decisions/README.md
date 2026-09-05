# Architecture decision records

An ADR records a decision that would be expensive or confusing to reverse silently. It
captures *why*, not just *what*, so a future reader — human or agent — can tell whether the
reasoning still holds.

## What is and is not an ADR

Record a decision when it constrains later work: scope, architecture boundaries, a
committed component or platform, a convention others must follow, or a reversal of a
previous decision.

Do not record routine implementation choices, and **do not record a preference as a
decision**. Naming a candidate part is not a decision; committing to it is.

## Status values

| Status | Meaning |
|---|---|
| `proposed` | Written, not yet agreed |
| `accepted` | Agreed and in force |
| `superseded` | Replaced by a later ADR (name it) |
| `rejected` | Considered and declined; kept for the reasoning |

## Numbering

`ADR-nnnn`, allocated in order, never reused. Filename:
`ADR-nnnn-<short-slug>.md`. Superseded ADRs are kept, never deleted.

## Required sections

`context`, `decision`, `alternatives`, `rationale`, `consequences`, `evidence`,
`revisit triggers`, `status`. `tools/validate_repo.py` checks these headings exist.

**Evidence** may legitimately be "none — this is a program decision, not a technical claim".
It may never be a claim about physical behaviour with nothing behind it.

**Revisit triggers** are what would make this decision wrong. An ADR with no revisit trigger
is either trivial or not thought through.

## Register

| ID | Title | Status |
|---|---|---|
| [ADR-0001](ADR-0001-vibration-as-product-001.md) | Vibration monitoring as FM-P001 | accepted |
| [ADR-0002](ADR-0002-end-to-end-product-scope.md) | Product scope spans node → gateway → cloud | accepted |
| [ADR-0003](ADR-0003-edge-operational-during-cloud-loss.md) | The edge must remain operational during cloud loss | accepted |
| [ADR-0004](ADR-0004-physical-evidence-is-authoritative.md) | Physical evidence is authoritative | accepted |
| [ADR-0005](ADR-0005-agentic-human-in-the-loop-model.md) | Agentic human-in-the-loop development model | accepted |

## Explicitly NOT decided

The following are **candidates only**. No ADR commits to any of them, and code must not
treat them as settled:

accelerometer/sensor part, MCU or SoC family, wireless technology (including LoRa-class),
gateway hardware and OS, cloud provider and services, portal technology, storage medium,
protocol and data format, enclosure and mounting approach, product family and model naming.

Committing to any of these requires an ADR with alternatives evaluated against evidence.
