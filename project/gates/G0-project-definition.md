# G0 — Project definition / harness

| Field | Value |
|---|---|
| Gate | G0 |
| Title | Project definition / harness |
| Status | see [`project/status.yaml`](../status.yaml) (authoritative) |
| Opened | 2026-09-05 |
| Objective | Establish Agentic Harness v0.1 and the initial repository shell |
| Hardware dependency | None — G0 is entirely a documentation and convention gate |

## Purpose

Establish the minimum high-quality engineering environment required to begin G1. G0 makes
no claim about any physical or software behaviour of the product.

## Pass criteria

| # | Criterion | Satisfied by | State |
|---|---|---|---|
| G0-01 | Repository shell exists with a documented purpose per directory | repository tree; per-directory `README.md` | met |
| G0-02 | `AGENTS.md` defines identity, philosophy, roles and rules | `AGENTS.md` | met |
| G0-03 | Machine-readable project status exists | `project/status.yaml` | met |
| G0-04 | Requirement ID convention exists, with a small initial set | `requirements/README.md`, `requirements/product.yaml` | met |
| G0-05 | Experiment convention and template exist | `experiments/README.md`, `experiments/templates/` | met |
| G0-06 | Evidence convention exists | `experiments/evidence.md` | met |
| G0-07 | ADR convention and template exist, with founding ADRs recorded | `docs/decisions/` | met |
| G0-08 | Gate convention exists; G0 defined, G1 sketched | `project/gates/` | met |
| G0-09 | `README.md` introduces FM-P001 and orients a new reader | `README.md` | met |
| G0-10 | Claude / Codex / ChatGPT / human roles are documented | `AGENTS.md` §3 | met |
| G0-11 | Testing levels are distinguished and documented | `tests/README.md` | met |
| G0-12 | Traceability mechanism exists from requirement → gate → experiment → evidence | `requirements/traceability.md` | met |
| G0-13 | Repository self-consistency is checkable mechanically | `tools/validate_repo.py` passes | met |
| G0-14 | Another agent can understand current state from repository artifacts alone | AGENTS.md §13 handoff order; verified by independent Codex review | **pending review** |
| G0-15 | Independent review by Codex | [`project/reviews/G0-codex-review-2026-09-05.md`](../reviews/G0-codex-review-2026-09-05.md) | met |
| G0-16 | Independent architecture review by ChatGPT | architect review record | **pending** |
| G0-17 | Human engineering lead accepts G0 | human decision recorded in `project/status.yaml` | **pending** |

`met` above means *the artifact exists and Claude believes it satisfies the criterion*. It
is a claim submitted for review, not an accepted result. G0-14 is deliberately not
self-assessed: only a reviewer who did not build the harness can judge it.

## Explicitly out of scope for G0

No sensor acquisition, DSP, storage, gateway, cloud, portal, PCB, enclosure, wireless,
classification, compliance or regulatory work. No component, vendor or platform selection.
No CI system. No HIL automation.

## Exit condition

G0 is passed when criteria G0-01 … G0-17 are all satisfied and the human engineering lead
records acceptance in `project/status.yaml`.

## Amendments made during review

Changes to the harness after G0 entered `ready_for_review`. Recorded here rather than folded
into the criteria above, so reviewers can see what moved underneath them.

| Date | Amendment | Rationale |
|---|---|---|
| 2026-09-05 | Corrections arising from the Codex review — stricter evidence-acceptance checks in the validator, instrument identity and calibration in evidence provenance, unsupported link-budget and connectivity claims relabelled as assumptions, G1 noise-floor units made provisional | Findings recorded in [`project/reviews/G0-codex-review-2026-09-05.md`](../reviews/G0-codex-review-2026-09-05.md) |
| 2026-09-05 | Added `project/coordination/` — an append-only inter-agent message ledger (AGENTS.md §14), proposed by Codex and adopted with four amendments | The G0 review itself needs a durable channel; conducting it through an undocumented one would leave no reviewable record |

Both are covered by existing criteria G0-01 and G0-13 rather than adding new criteria — they
are repository structure with a documented purpose, checked by `tools/validate_repo.py`. A
reviewer who thinks a harness change mid-review should instead have waited for G0 acceptance
should say so.

## Known weaknesses of Harness v0.1

Recorded honestly so reviewers can attack them:

- The convention set is unproven — it has never been exercised by a real experiment. Expect
  it to be wrong in ways only use will reveal.
- Evidence handling is filesystem conventions plus a manifest. It has no integrity
  guarantees and will not scale to large binary captures without a decision on storage.
- The initial requirement set is a first draft with placeholder numeric targets (e.g.
  1 kHz). Those numbers are *targets to be justified*, not derived requirements.
- Traceability is maintained by hand and checked by a script; it can still be semantically
  wrong while being structurally valid.
