# Traceability

Maps every requirement to the gate that should demonstrate it, the experiment(s) that
address it, and the evidence accepted for it.

This table is maintained by hand and its structure is checked by
`python3 tools/validate_repo.py` (every requirement in `product.yaml` must appear here
exactly once, with a matching gate). The script cannot check whether the *content* is
honest — that is a review responsibility (Codex).

## Reading the table

- **Gate** — earliest gate at which the requirement should be demonstrated.
- **Experiments** — experiment IDs addressing it. `—` means none yet.
- **Evidence** — accepted evidence IDs. `—` means **unproven**.
- **State** — `unproven` until evidence is accepted by the human engineering lead.

A requirement with code written against it but no evidence is still `unproven`. Writing the
implementation is not demonstration.

## Requirement → gate → experiment → evidence

| Requirement | Title | Gate | Verification | Experiments | Evidence | State |
|---|---|---|---|---|---|---|
| SV-SYS-001 | End-to-end measurement path | G6 | integration, bench | — | — | unproven |
| SV-SYS-002 | Measurement provenance | G1 | unit, bench, inspection | — | — | unproven |
| SV-ACQ-001 | Continuous 3-axis acquisition | G1 | bench, hil | — | — | unproven |
| SV-ACQ-002 | Nominal sample rate | G1 | bench | — | — | unproven |
| SV-DSP-001 | Local event detection | G3 | unit, bench | — | — | unproven |
| SV-DSP-002 | Event feature generation | G3 | unit, bench | — | — | unproven |
| SV-STO-001 | Pre/post-event waveform retention | G4 | unit, bench, hil | — | — | unproven |
| SV-COM-001 | Gateway event reception | G5 | integration, bench, hil | — | — | unproven |
| SV-GW-001 | Gateway local persistence | G5 | integration, fault | — | — | unproven |
| SV-GW-002 | Operation during cloud outage | G5 | integration, bench, fault | — | — | unproven |
| SV-CLD-001 | Cloud event inspection | G6 | integration, inspection | — | — | unproven |

**Every requirement is currently unproven.** No experiment has been run and no evidence
exists. This is the correct state at G0.

## Coverage gaps (known), with the gate each must be closed by

Deadlines set by the G0 architecture review
(`project/reviews/G0-chatgpt-review-2026-09-05.md`), which ruled the gaps acceptable at G0
but **not equally deferrable**. Full list in `project/roadmap.md`.

| Gap | Must exist before |
|---|---|
| Mounting, sensor coupling, measurement orientation | G2 |
| Calibration / traceability needed for physical-unit claims | G2 |
| Device identity; configuration identity and versioning | G5 |
| Message and data integrity; node↔gateway trust model | G5 |
| Behaviour under duplicate, incomplete and corrupt transfers | G5 |
| Configuration ownership and persistence | G5 |
| Offline endurance target | G5–G7 |
| Production power budget | G7 |
| Firmware update / OTA | G7–G8 |
| Environmental operating envelope | G8–G10 |
| Regulatory / certification | deferred until product maturity justifies it |

## Coverage gaps (known)

- `HW` and `OPS` areas have no requirements. Deliberate: hardware and field-operation
  requirements should be derived from evidence, not invented at bootstrap.
- No requirement covers power, environmental range, mounting or mechanical coupling. These
  are real and currently unaddressed; they are expected to arrive by G2–G7.
- No requirement covers security, authentication or data integrity in transit. Deliberate
  at this stage, and a known gap to raise before G5.
- No requirement covers device configuration or update. Expected around G5.

Gaps are listed rather than filled so reviewers can judge whether the omission is
acceptable.
