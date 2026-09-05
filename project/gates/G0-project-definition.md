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
| G0-14 | Another agent can understand current state from repository artifacts alone | Cold read performed by Codex; confirmed by the architect review | met |
| G0-15 | Independent review by Codex | [`project/reviews/G0-codex-review-2026-09-05.md`](../reviews/G0-codex-review-2026-09-05.md) | met |
| G0-16 | Independent architecture review by ChatGPT | [`project/reviews/G0-chatgpt-review-2026-09-05.md`](../reviews/G0-chatgpt-review-2026-09-05.md) | met |
| G0-17 | Human engineering lead accepts G0 | recorded under *Gate outcome* below | met |

`met` for G0-01 … G0-13 originally meant *the artifact exists and Claude believes it
satisfies the criterion* — a claim submitted for review. Those claims have since been
examined by Codex and by the architect. G0-14 was deliberately not self-assessed, and is
marked met on Codex's cold read of the repository, confirmed independently in the
architecture review.

## Explicitly out of scope for G0

No sensor acquisition, DSP, storage, gateway, cloud, portal, PCB, enclosure, wireless,
classification, compliance or regulatory work. No component, vendor or platform selection.
No CI system. No HIL automation.

## Exit condition

G0 is passed when criteria G0-01 … G0-17 are all satisfied and the human engineering lead
records acceptance.

## Gate outcome

**G0 PASSED — 2026-09-05.**

Accepted by Hamish, project owner and human engineering lead:

> The Agentic Harness v0.1 is approved as the initial engineering operating framework for
> FM-P001. Acceptance does not imply approval of any product architecture, component choice,
> physical behaviour or draft product requirement. The harness will be reviewed for
> proportionality after the first completed G1 experiment.

| Field | Value |
|---|---|
| Accepted by | Hamish — project owner / human engineering lead |
| Date | 2026-09-05 |
| Codex review | [`G0-codex-review-2026-09-05.md`](../reviews/G0-codex-review-2026-09-05.md) — suitable with minor changes; corrections applied before acceptance |
| Architecture review | [`G0-chatgpt-review-2026-09-05.md`](../reviews/G0-chatgpt-review-2026-09-05.md) — ready to pass; no finding required a change before G0 |
| Conditions attached | Harness proportionality to be reviewed after the first completed G1 experiment (risk R-022) |

**What this acceptance does not mean.** It approves the engineering operating framework and
nothing else. No product architecture, component, physical behaviour or product requirement
is approved by it. All eleven requirements remain `draft`. No physical measurement exists.

The architecture review's deferred actions are recorded in
[`project/roadmap.md`](../roadmap.md), not here, so they attach to the gates that must
satisfy them.

> **Attribution note.** The acceptance statement above reached the repository quoted inside
> a Codex-authored ledger message (`MSG-20260905T021612Z-5963-codex`) that did not declare
> itself a relay under the convention in `project/coordination/README.md`. The wording is
> recorded here verbatim as transcribed. If the project owner wants a first-party record, a
> `human`-authored message would supply it; the human engineering lead has a direct writer in
> the ledger.

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
