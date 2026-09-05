# Requirements

`product.yaml` holds the requirement set. `traceability.md` maps each requirement to the
gate, experiment and evidence that will demonstrate it.

## Identifier convention

```text
SV-<AREA>-nnn
```

`SV` is the working product family. `nnn` is a zero-padded sequence number, allocated per
area, never reused.

| Area | Scope |
|---|---|
| `SYS` | System-level behaviour spanning more than one subsystem |
| `ACQ` | Sensing and signal acquisition |
| `DSP` | Signal processing, event detection, feature extraction |
| `STO` | On-device storage and retention |
| `COM` | Device ↔ gateway communications |
| `GW`  | Edge gateway behaviour |
| `CLD` | Cloud ingestion and services |
| `HW`  | Hardware, electrical and mechanical |
| `OPS` | Deployment, installation, field operation, maintenance |

`HW` and `OPS` have no requirements yet. Writing them now would be speculation.

## Requirement fields

| Field | Meaning |
|---|---|
| `id` | `SV-<AREA>-nnn` |
| `title` | Short name |
| `statement` | What the system shall do. One requirement per statement. |
| `status` | `draft` \| `accepted` \| `superseded` \| `rejected` |
| `rationale` | Why this exists. If it cannot be justified, it should not exist. |
| `verification` | How it will be demonstrated — see below |
| `gate` | Earliest gate at which it should be demonstrated |
| `evidence` | Evidence IDs supporting it. Empty until evidence is accepted. |
| `open_questions` | What is unresolved about this requirement |

### Verification methods

These are the same levels defined in `tests/README.md`, plus two non-test methods.

| Method | Meaning |
|---|---|
| `unit` | Automated test of logic in isolation |
| `integration` | Automated test across a component boundary |
| `hil` | Automated test executing on real hardware |
| `bench` | Human-run physical experiment with instrument evidence |
| `fault` | Deliberate fault injection / degraded-condition experiment |
| `analysis` | Derivation or calculation from accepted evidence |
| `inspection` | Review of an artifact |

A requirement about physical behaviour cannot be verified by `unit` or `integration` alone
(AGENTS.md §12).

## Status discipline

Every requirement is currently `draft`. **No requirement is accepted.**

`draft` means: written down so it can be argued with. Numeric targets in draft requirements
(sample rates, durations, retention periods) are **targets to be justified**, not derived
values — most are placeholders awaiting evidence or an architecture decision. They will be
wrong. Challenge them.

A requirement moves to `accepted` only when the human engineering lead and the architect
agree its statement, target and verification method are right. Requirements are not
promoted just because code was written against them.

## Adding or changing a requirement

1. Take the next unused number in the area.
2. Write the rationale before the statement. A requirement without a rationale is a guess.
3. Add its row to `traceability.md`.
4. Run `python3 tools/validate_repo.py`.
5. Changing an accepted requirement's meaning requires a new ID and marking the old one
   `superseded` — never silently edit accepted intent.
