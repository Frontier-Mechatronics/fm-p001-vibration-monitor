# Engineering gates

A **gate** is a bounded engineering milestone with explicit, checkable pass criteria. The
project is at exactly one gate at a time; `project/status.yaml` names it.

## Rules

1. A gate file lists pass criteria. Each criterion is either satisfied or it is not — no
   partial credit, no "substantially complete".
2. Criteria that depend on physical behaviour require **accepted physical evidence**
   (`experiments/evidence.md`). A software test does not satisfy a hardware criterion.
3. Agents may move a gate to `ready_for_review`. **Only the human engineering lead may mark
   a gate `passed`** (AGENTS.md §5).
4. Gate scope is fixed when the gate opens. Work that expands it is a scope change and needs
   an ADR or explicit human approval.
5. Future gates are deliberately under-specified. Only the current gate and a preliminary
   sketch of the next one are defined. Do not build ahead of the gate.

## Gate status values

`not_started` → `in_progress` → `ready_for_review` → `passed`

A gate may also be `superseded` if the program direction changes; record why in an ADR.

## Gate map

This map lists the gates and how well each is *defined*. It deliberately does not restate
gate **status** — `project/status.yaml` is the single authoritative source for which gate is
current and what state it is in (AGENTS.md §11).

| Gate | Title | Definition | File |
|---|---|---|---|
| G0 | Project definition / harness | defined; outcome recorded | [G0-project-definition.md](G0-project-definition.md) |
| G1 | Sensor acquisition | preliminary — direction only | [G1-sensor-acquisition.md](G1-sensor-acquisition.md) |
| G2 | Instrument characterisation | title only | — |
| G3 | DSP and event engine | title only | — |
| G4 | Local storage / persistence | title only | — |
| G5 | Edge gateway | title only | — |
| G6 | Cloud end-to-end path | title only | — |
| G7 | Wireless field node | title only | — |
| G8 | Custom PCB | title only | — |
| G9 | Multi-node system | title only | — |
| G10 | Controlled field trial | title only | — |

Gates G2–G10 are titles only. They express intended direction, not commitments. Their
criteria will be written when they are approached, informed by evidence gathered before
them. The gate list itself may change.
