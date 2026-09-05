# Hardware

Physical hardware: schematics, wiring records, bench setups, fixtures and bring-up notes.

| Directory | Contents |
|---|---|
| `node/` | The sensing node — sensor, acquisition, MCU carrier, wiring |
| `fixtures/` | Test fixtures, mounts, stimulus rigs, instrument jigs |
| `gateway/` | Edge gateway hardware and its physical setup |

**No PCB or enclosure design.** Both are gated (G8) and require evidence that a breadboard
or off-the-shelf assembly cannot provide (AGENTS.md §8). Early hardware is expected to be
development boards, breakouts and hand wiring — and those still need revision identity,
because evidence is worthless without knowing what produced it.

## Hardware revision identity

```text
HW-<unit>-rNN
```

`<unit>` is a short unit name (e.g. `node`, `fixture-shaker`). `rNN` increments on **any
physical change that could affect measurement** — a rewired connection, a changed sensor
part, a different mounting, an added decoupling capacitor, a different cable length.

If you cannot say which revision produced a measurement, that measurement is not evidence.

Each unit directory keeps a `revisions.md` recording, per revision: what changed, why, the
date, and any evidence that motivated the change.

## What belongs here

- Wiring records and connection tables — what is actually connected, not what was intended
- Photographs of as-built setups (as `IMG-nnnn` evidence, referenced from experiments)
- Bring-up notes, including what did not work
- Bill of materials for a specific revision
- Mechanical mounting and coupling details — how a sensor is attached materially affects
  what it measures

## Safety

All physical construction, wiring, powering and probing is performed by the human
engineering lead. Agents may specify and document; agents never direct unsupervised physical
work (AGENTS.md §7).
