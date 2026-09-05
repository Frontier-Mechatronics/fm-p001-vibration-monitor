# Firmware

Embedded firmware for the sensing node.

| Directory | Contents |
|---|---|
| `node/` | Node firmware source and build |
| `tests/` | Host-side unit tests of firmware logic |

Empty at G0. Firmware work begins at G1, against whatever hardware the human confirms is
physically available.

## Expectations when code arrives

- **Reproducible build from a single documented command.** Codex must be able to reproduce
  a build without asking how (AGENTS.md §3.3), and HIL automation later depends on it.
- **The build records its identity** — commit and configuration — in a form that ends up in
  data provenance (`SV-SYS-002`).
- **Logic separable from hardware access**, so it can be unit-tested on the host. Not an
  abstraction layer built in advance; just don't weld computation to register access.
- **Machine-parseable diagnostic output** on a known interface, so evidence collection can
  later be automated.
- **Firmware never self-certifies timing.** A firmware-reported rate is a claim to be
  checked against an instrument, not evidence (ADR-0004).
