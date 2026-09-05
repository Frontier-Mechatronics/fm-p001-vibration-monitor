# ADR-0004 — Physical evidence is authoritative

| Field | Value |
|---|---|
| Status | accepted |
| Date | 2026-09-05 |
| Deciders | Human engineering lead |
| Supersedes | none |
| Superseded by | none |

## Context

This program mixes human engineering judgement with agents that generate code and prose
fluently and confidently. Fluency is not correctness. In a hardware program, a confident but
unverified claim about physical behaviour — a sample rate, a noise floor, a current draw —
propagates into requirements, design and other decisions and is expensive to unwind once it
has been built upon.

## Decision

Physical evidence is the authoritative source of truth for all claims about physical
behaviour, above code, simulation, datasheets, agent confidence and architectural intent.

The hierarchy is:

```text
physical evidence > repeatable experiment > instrument measurement
  > datasheet/model > software behaviour > agent assumption
```

An unsupported claim about physical behaviour is a **defect**, whether or not it later turns
out to be true.

## Alternatives

| Alternative | Why not chosen |
|---|---|
| Trust datasheets and simulation, verify selectively at the end | Late discovery of a timing or noise problem invalidates work built on top of it |
| Trust firmware self-reporting for timing | Firmware measures itself with the same clock it may be getting wrong; it cannot detect its own systematic error |
| Informal verification without records | Unrepeatable and unreviewable; provides no basis for later comparison across revisions |

## Rationale

The failure mode this guards against is specific and likely: a plausible number entering the
record without measurement. Making evidence a structural requirement — of experiments, gate
criteria and review — is cheaper than detecting contaminated conclusions later. It also
gives Codex an objective basis for adversarial review: claims can be checked against
referenced evidence rather than argued about.

## Consequences

- Gate criteria depending on physical behaviour cannot pass on software tests alone.
- Progress is bounded by human bench availability; agents must stop and request bench
  actions (AGENTS.md §7).
- Every physical claim carries an evidence reference or an explicit `predicted` / `assumed`
  label.
- Experiment and evidence conventions must exist before hardware work begins — hence G0.
- Some throughput is traded for trustworthiness. This is intended.

## Evidence

None. This is a process decision.

## Revisit triggers

- The evidence discipline is observed to block progress without preventing real errors
  (i.e. the cost is real and the benefit is not).
- Automation (HIL) makes evidence collection cheap enough to change how it is gathered —
  which changes the mechanism, not the principle.
