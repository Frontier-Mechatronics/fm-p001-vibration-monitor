# G0 independent Codex review — 2026-09-05

| Field | Value |
|---|---|
| Reviewer | Codex — Lead Tester / Reviewer |
| Scope | Agentic Harness v0.1 |
| Result | Suitable with minor changes |

The cold handoff path in `AGENTS.md` was completed using the repository alone: it identified
G0 as current, no active experiment, the G1 hardware-availability blocker, and no accepted
evidence. `python3 tools/validate_repo.py` passes after the corrections below.

## Findings and corrections

- The validator previously allowed a requirement or `latest_accepted_evidence` entry to
  reference evidence that was merely recorded or rejected. It now requires a manifest entry
  with status `accepted`, and also checks manifest/experiment, evidence-kind and filename
  consistency.
- Evidence provenance now explicitly requests instrument identity and calibration state.
- Link-budget and connectivity statements that read as established physical facts were
  relabelled as assumptions or unknowns.
- G1's at-rest noise criterion now requires raw counts or explicitly provisional scaled
  units; traceable engineering-unit characterisation belongs at G2.

## Remaining review limits

No product implementation, bench experiment, evidence item or HIL path exists at G0, so none
can yet be reviewed. The validator establishes structural consistency only; it cannot detect
invented values, inappropriate verification methods, unsound measurement setups, or a human
accepting inadequate evidence.

## Recommendation

G0 is ready for independent architecture review and human review. This record is not a gate
acceptance; G0 remains `ready_for_review` until the human engineering lead records `passed`
in `project/status.yaml`.
