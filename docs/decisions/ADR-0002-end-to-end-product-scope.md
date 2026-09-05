# ADR-0002 — Product scope spans node → gateway → cloud

| Field | Value |
|---|---|
| Status | accepted |
| Date | 2026-09-05 |
| Deciders | Human engineering lead |
| Supersedes | none |
| Superseded by | none |

## Context

FM-P001 could have been scoped as a sensing device alone, with data handling left to
third-party systems. The program's stated intent is an end-to-end product-development
capability: physical signal through to usable information.

## Decision

FM-P001's product scope is the full chain:

```text
vibration → sensor → acquisition hardware → firmware → DSP/event detection
  → local storage → device comms → edge gateway → local persistence
  → cloud ingestion → portal / analytics
```

This fixes the *chain*, not its implementation. Every element remains technology-neutral,
and each is built only when its gate is reached.

## Alternatives

| Alternative | Why not chosen |
|---|---|
| Sensing node only, data off-boarded to third-party platform | Avoids the integration problems that dominate real products; would not build the intended capability |
| Cloud/analytics only, using off-the-shelf sensors | Skips the physical measurement layer, which is where the program's uncertainty and value lie |
| Node + gateway, no cloud | Leaves the field-to-office path unproven, which is the point of a monitoring product |
| Decide scope later | Leaves architecture, requirements and gates ungrounded |

## Rationale

The hard problems in this class of product are at the boundaries: timing at the sensor,
integrity across the link, behaviour when connectivity fails. Scoping the whole chain is
what makes those boundaries visible. Sequencing the chain across gates keeps the scope
honest — declaring the chain is not the same as building it now.

## Consequences

- Gates G1–G6 follow the chain, each converting one segment's uncertainty into evidence.
- Broad scope raises the risk of premature breadth; controlled by gate discipline
  (AGENTS.md §5) and risk R-021.
- Interfaces between segments must be defined explicitly, since they are where the
  engineering difficulty concentrates.
- The repository is structured along the chain (`firmware/`, `gateway/`, `cloud/`,
  `portal/`) from the start, even though most of it stays empty for a long time.

## Evidence

None. Program-scope decision.

## Revisit triggers

- Evidence shows a segment is better solved by an existing product than by building it.
- Scope breadth is observed to be preventing depth at the current gate.
- The commercial target narrows in a way that makes part of the chain irrelevant.
