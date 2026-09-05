# ADR-0005 — Agentic human-in-the-loop development model

| Field | Value |
|---|---|
| Status | accepted |
| Date | 2026-09-05 |
| Deciders | Human engineering lead |
| Supersedes | none |
| Superseded by | none |

## Context

FM-P001 is developed by one human engineering lead working with several agents that have
different strengths and no shared memory between sessions. Agents cannot touch hardware.
Any development model must place the human where physical reality is, keep the agents'
outputs checkable, and survive discontinuous sessions.

## Decision

Development uses four defined roles with separated responsibilities:

| Role | Responsibility |
|---|---|
| Human engineering lead | Ultimate authority; all physical work; evidence acceptance |
| Claude | Lead developer — implementation, repository, tooling, documentation |
| Codex | Lead tester/reviewer — deliberately adversarial |
| ChatGPT | Solution architect / technical program lead |

The **repository is the shared memory**. State lives in version-controlled artifacts, not in
conversation history. `project/status.yaml` is the single canonical statement of current
state.

Roles are separated deliberately: the agent that writes the implementation does not
adjudicate whether it works.

## Alternatives

| Alternative | Why not chosen |
|---|---|
| Single agent doing everything | No independent check; an agent reviewing its own work reproduces its own blind spots |
| Agent orchestration framework | Automation before the workflow is understood; adds a system to maintain that produces no engineering evidence |
| Conversation-based state | Lost between sessions and invisible to agents without repository access; cannot be reviewed or diffed |
| Human-only development | Not the program's intent, and does not scale to the breadth of the chain |

## Rationale

The separation puts an adversarial reviewer between implementation and acceptance, and an
architect above both to control scope. Making the repository the memory means any party —
including one with no continuous access, like ChatGPT — can reconstruct current state from
committed artifacts. Keeping the harness to plain files and one validation script means the
process itself needs almost no maintenance.

## Consequences

- Artifacts must be self-sufficient: Codex must be able to work with no undocumented
  context, and ChatGPT with a small pasteable set of files.
- Duplicated state is a defect; a single canonical status file must be kept current.
- Agents must explicitly stop and request human bench action rather than assuming outcomes.
- Some ceremony overhead is accepted, tracked as risk R-022 and to be revised after first
  real use.
- The harness itself is versioned (`harness_version` in `project/status.yaml`) and is
  expected to change through use.

## Evidence

None. Process decision.

## Revisit triggers

- Harness overhead is observed to exceed its value at G1 (risk R-022).
- The role separation produces contradictory direction that the human spends more time
  reconciling than the reviews are worth.
- Team composition changes (additional humans, different agents, or agents gaining
  continuous repository access).
