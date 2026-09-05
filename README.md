# FM-P001 — Construction Vibration & Edge Intelligence Monitor

Frontier Mechatronics Product 001. Working family `SV`, initial model `SV1`.

An end-to-end vibration-monitoring system for construction and engineering environments,
spanning physical sensing, embedded acquisition, on-device event detection, an edge gateway
and a cloud portal.

> **Experimental.** These are early prototypes. Nothing here is a certified, calibrated or
> commercially available instrument. No compliance, safety or regulatory claim is made or
> implied, and none should be inferred. Do not use output from this system to make
> structural, safety or legal decisions.

---

## What this is

FM-P001 is the first end-to-end Frontier Mechatronics product-development program. Its goal
is both a device and a capability: a repeatable way of taking a physical signal all the way
to usable information, with evidence at every step.

The intended signal chain:

```text
physical vibration → vibration sensor → acquisition hardware → MCU firmware
  → DSP / event detection → local waveform storage → device communications
  → Linux edge gateway → local persistence → cloud ingestion → portal / analytics
```

The current working technical direction — 3-axis sensing, continuous acquisition around
1 kHz, local DSP and event detection, pre/post-event capture, feature extraction, an edge
gateway, offline-capable operation, an eventual constrained wireless link, a cloud portal,
and eventually a custom PCB — is **direction, not commitment**. No sensor, MCU, radio,
gateway platform or cloud provider has been selected. See `docs/decisions/README.md` for
what is decided and, more importantly, what is not.

## Why vibration first

Vibration is demanding enough to be a real engineering exercise and tractable enough to
start with. It forces honest treatment of sample rate, jitter, dynamic range, event
detection, data volume and link budget; it produces more data than a constrained link can
carry, which drives edge intelligence rather than cloud processing; and it is observable
with ordinary bench instruments. It has a genuine application in construction and
engineering monitoring, which keeps requirements grounded. See `ADR-0001`.

## Development philosophy

Physical measurement is authoritative.

```text
physical evidence > repeatable experiment > instrument measurement
  > datasheet/model > software behaviour > agent assumption
```

If firmware claims a timing rate and the oscilloscope measures something different, the
oscilloscope wins. Claims about hardware behaviour require physical evidence; measurements
are never invented, and failed experiments are kept as they happened. Work proceeds in small
bounded steps:

```text
question → hypothesis → bounded experiment → implementation → bench measurement
  → evidence → review → engineering conclusion → next experiment
```

Complexity — procurement, PCB design, new subsystems — is gated by demonstrated need.

Development is human-in-the-loop with defined agent roles: a **human engineering lead**
(ultimate authority, all physical work, evidence acceptance), **Claude** (lead developer),
**Codex** (adversarial tester/reviewer) and **ChatGPT** (solution architect / technical
program lead). Full definitions in `AGENTS.md`. The repository is the shared memory: state
lives in committed artifacts, not in conversation history.

## Current stage

**Gate G0 — project definition / harness.** Agentic Harness v0.1 and the repository shell
are in place and awaiting independent review. **G0 has not been passed.**

No product implementation exists. No experiment has been run. No evidence has been
collected. Every requirement is `draft` and unproven — which is the correct state at G0.

Authoritative current state: **`project/status.yaml`**.

## Orientation — read in this order

1. **`AGENTS.md`** — rules of engagement, roles, and the evidence rule
2. **`project/status.yaml`** — the single machine-readable statement of current state
3. **the current gate file** in `project/gates/` — what "done" means right now
4. **the active experiment** in `experiments/` (none yet)
5. **requirements** referenced by that gate, in `requirements/product.yaml`
6. **recent ADRs** in `docs/decisions/`

Then run `python3 tools/validate_repo.py` to confirm the repository is self-consistent.

There is deliberately no separate "current status" summary document. A second statement of
project state would drift from the first.

## Repository layout

```text
├── AGENTS.md            operating instructions for all agents and contributors
├── project/             status.yaml (canonical state), roadmap, risks, gates/,
│                       coordination/ (append-only inter-agent ledger), reviews/
├── requirements/        product.yaml (requirement set) and traceability.md
├── docs/                architecture/, decisions/ (ADRs), protocols/, references/
├── experiments/         experiment conventions, evidence conventions, templates/
├── hardware/            node/, fixtures/, gateway/ — physical build and revision records
├── firmware/            node/ firmware and host-side tests/
├── gateway/             Linux edge gateway software
├── cloud/               cloud ingestion and services
├── portal/              user-facing inspection interface
├── analysis/            host-side analysis of captured evidence
├── tests/               unit/, integration/, hil/, fault/
└── tools/               validate_repo.py and other process tooling
```

Most of this is empty. Each directory has a README stating its purpose and what is expected
to arrive there, and at which gate. Empty directories are structure for work that is
sequenced, not work that is in progress.

## Testing

Unit, integration, hardware-in-the-loop, bench experiment and fault injection are distinct
kinds of evidence and are not interchangeable. A software test does not prove electrical
behaviour; a bench observation does not prove software correctness. See `tests/README.md`.

## Licence

AGPL-3.0. See `LICENSE`.
