# EXP-nnnn — <short title>

<!--
Copy to experiments/EXP-nnnn-<slug>/EXP-nnnn.md and fill in.
Sections 1–9 are written BEFORE the bench session and are not edited afterwards to match
the outcome. Deviations go in section 11. Measured fields stay TBD until a human measures
them — never fill them in from a datasheet, a simulation or an expectation.
-->

| Field | Value |
|---|---|
| ID | EXP-nnnn |
| Status | draft \| ready \| running \| analysed \| accepted \| rejected \| abandoned |
| Gate | Gn |
| Requirements | SV-…-nnn, … |
| Author | |
| Bench operator | |
| Date designed | YYYY-MM-DD |
| Date run | TBD |

## 1. Objective

One paragraph. What question is this experiment answering, and why does it matter now?

## 2. Hypothesis

A falsifiable statement.

**Falsified if:** the concrete result that would disprove it. If this cannot be written,
the experiment is not yet designed.

## 3. Requirements addressed

| Requirement | What this experiment contributes to it |
|---|---|
| SV-…-nnn | |

## 4. Hardware

| Item | Identity | Revision | Notes |
|---|---|---|---|
| DUT | | HW-…-rNN | |
| Sensor | | | |
| Fixture | | | |
| Instrument | make/model | | settings summary |

## 5. Firmware / software under test

| Field | Value |
|---|---|
| Repository commit | `<sha>` |
| Build command | |
| Build artifact hash | |
| Configuration | file/params, or inline |

## 6. Bench setup

Describe the physical setup precisely enough for someone else to rebuild it: wiring, probe
points and grounding, mounting and coupling, orientation, supply, environment. Reference an
`IMG-nnnn` photograph of the actual setup.

## 7. Expected result

What the hypothesis predicts, quantitatively where possible, with the tolerance considered
acceptable. State the basis: `predicted (datasheet)`, `computed`, or `assumed`.

## 8. Procedure

Numbered, repeatable steps. Include safety-relevant steps explicitly. State what is recorded
at each step and to which evidence ID.

1.
2.

## 9. Fault injection

Faults deliberately introduced, and what the system is expected to do. Omit only if the
experiment genuinely has no failure dimension — and say so if omitted.

| Fault | Method | Expected behaviour | Observed |
|---|---|---|---|
| | | | TBD |

---
<!-- Everything below is written AFTER the bench session. -->

## 10. Raw evidence

| Evidence ID | Kind | File | What it shows |
|---|---|---|---|
| | | | |

Provenance for each entry is in `evidence/manifest.yaml`.

## 11. Measured result

Measured values only. Include units, instrument, and uncertainty or resolution. Record
deviations from the planned procedure here, including anything that went wrong.

| Quantity | Measured | Units | Uncertainty / resolution | Evidence |
|---|---|---|---|---|
| | TBD | | | |

## 12. Analysis

What the numbers mean. Distinguish `measured`, `computed`, `predicted` and `assumed`
explicitly. Address the difference between expected and measured, including the possibility
that the setup or the instrument is wrong.

## 13. Conclusion

Hypothesis **supported / falsified / inconclusive**, and why. A falsified hypothesis is a
successful experiment — state what it rules out.

## 14. Design rule

Durable, testable constraints this experiment established for the product. Omit if none.

- **DR-nnnn:** …

## 15. Follow-up

Open questions, next experiments, requirement changes, ADRs needed, risks raised or retired.

## 16. Acceptance

| Field | Value |
|---|---|
| Accepted by | (human engineering lead) |
| Date | |
| Decision | accepted / rejected + reason |
