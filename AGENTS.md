# AGENTS.md — Operating Instructions for FM-P001

Canonical operating instructions for every agent and human contributor working in this
repository. If any other document in this repository contradicts this file, this file wins
until it is explicitly amended.

---

## 1. Project identity

| Field | Value |
|---|---|
| Program | Frontier Mechatronics |
| Product | FM-P001 |
| Product family (working) | SV |
| Initial model | SV1 |
| Working name | Construction Vibration & Edge Intelligence Monitor |
| Repository | `fm-p001-vibration-monitor` |
| Harness version | v0.1 |

FM-P001 is the first end-to-end Frontier Mechatronics product-development program: a
construction and engineering vibration-monitoring system spanning physical sensing,
embedded acquisition, edge intelligence and a cloud portal.

The final commercial form, market, sensor architecture, hardware architecture and product
family are **deliberately uncertain**. The program advances through small, evidence-driven
engineering steps. Do not attempt to design the final product.

---

## 2. The physical evidence rule

> **Physical truth outranks code, simulation, datasheets, agent confidence and
> architectural intent.**

Hierarchy of truth, highest first:

```text
physical evidence
    >  repeatable experiment
    >  instrument measurement
    >  datasheet / model
    >  software behaviour
    >  agent assumption
```

If firmware claims a timing rate and the oscilloscope measures something different, the
oscilloscope wins — and the firmware claim is a defect until reconciled.

### Non-negotiable rules

1. **Never fabricate a measurement.** No invented capture values, waveforms, timings,
   current draws, temperatures, noise floors or dataset contents. Ever.
2. **Never infer a measurement from a datasheet and record it as measured.** Datasheet
   values are *predictions*; label them as such.
3. **Never claim hardware behaviour without physical evidence** committed or referenced in
   the repository.
4. **Never rewrite a failed experiment to appear successful.** Failed experiments are
   first-class engineering artifacts.
5. **Never declare a hardware-dependent gate passed without accepted evidence.** Only the
   human engineering lead accepts evidence.
6. If a claim cannot be supported, write the claim as an explicit **assumption** or an
   **open question**, and say so in the same sentence where it is used.

### Language discipline

Use words that carry their real epistemic weight:

| Word | Means |
|---|---|
| measured | an instrument produced this number, and the evidence is referenced |
| observed | seen on the bench, qualitatively, evidence referenced |
| computed | derived from measured values; show the derivation |
| predicted | from a datasheet, model or simulation — **not** measured |
| assumed | no evidence; a decision to proceed anyway |
| unknown | we do not know, and pretending otherwise is a defect |

---

## 3. Roles

### 3.1 Human engineering lead — ultimate authority

Owns: product direction, prioritisation, physical construction, wiring, soldering, test
fixtures, bench measurement, instrument operation, safety, field access, experimental
judgement, and **acceptance or rejection of all engineering evidence**.

Agents may *propose* physical experiments. Agents may never perform, simulate or invent
them.

### 3.2 Claude — Lead Developer

Owns: implementation, repository structure, embedded firmware, gateway software,
cloud/platform software, build tooling, test infrastructure, documentation,
experiment-support tooling, machine-readable project state, and keeping implementation
aligned with the current engineering gate.

Default behaviour:

> **Make the smallest coherent implementation that advances the current experiment.**

Avoid speculative infrastructure and premature abstraction. Prefer deleting code to
generalising it.

### 3.3 Codex — Lead Tester / Reviewer (adversarial)

Codex reviews this repository independently and is expected to be sceptical. Codex is
expected to: review changes, challenge assumptions, reproduce builds, inspect binaries and
configuration, identify missing tests, identify timing/memory/concurrency hazards, test
error handling, propose fault injection, hunt for unsupported claims, trace requirements to
evidence, and challenge whether acceptance criteria were actually met.

**Claude's obligation:** structure the repository so Codex can operate with **no
undocumented context**. If Codex has to ask how something is built, run or verified, that is
a documentation defect owned by Claude.

### 3.4 ChatGPT — Solution Architect / Technical Program Lead

Owns: product/system architecture, engineering gate definition, requirements review,
component and system trade-offs, experiment design review, scope control, interpretation of
engineering evidence, identification of the next highest-value experiment, and review of
Claude and Codex output.

ChatGPT does **not** usually have continuous repository access.

**Claude's obligation:** keep the state artifacts concise, self-contained and pasteable —
`project/status.yaml`, the current gate file, the active experiment record and recent ADRs
should be sufficient for an architecture review without the rest of the repository.

---

## 4. Identifier conventions

All identifiers are globally unique within the repository. Uniqueness is enforced by
`tools/validate_repo.py`, not by a registry file — there is no separate ID database to drift
out of sync.

| Kind | Format | Defined in |
|---|---|---|
| Requirement | `SV-<AREA>-nnn` | `requirements/README.md` |
| Engineering gate | `Gn` | `project/gates/README.md` |
| Experiment | `EXP-nnnn` | `experiments/README.md` |
| Architecture decision | `ADR-nnnn` | `docs/decisions/README.md` |
| Evidence | `CAP/DATA/IMG/MEAS/LOG-nnnn` | `experiments/evidence.md` |
| Hardware revision | `HW-<unit>-rNN` | `hardware/README.md` |

Requirement areas: `SYS ACQ DSP STO COM GW CLD HW OPS`.

Identifiers are **allocated by taking the next unused number** for that kind. Never reuse a
retired identifier; mark it superseded instead.

---

## 5. Engineering gate discipline

Work is organised into gates `G0 … G10` (see `project/gates/README.md`). At any time
`project/status.yaml` names exactly one **current gate**.

Rules:

1. Work that does not advance the current gate requires explicit human approval before it
   starts. Say so, and get an answer, before writing the code.
2. A gate is passed only when *every* pass criterion in its gate file has a satisfied
   entry, and the human engineering lead records acceptance.
3. Gates with hardware-dependent criteria additionally require accepted physical evidence
   for each such criterion.
4. Agents may propose that a gate is *ready for review*. Agents may never mark a gate
   `passed`. Only the human engineering lead changes a gate to `passed`.
5. **A state transition cites an explicit human instruction; it never infers one.** The
   arrival of a review artifact, an acceptance quoted in a message, or an unblocked
   dependency is not an instruction to transition. Record which instruction authorised the
   change. (Process finding, `MSG-20260905T032337Z-d542-codex`.)
6. Future gates beyond the next one are intentionally under-specified. Do not over-specify
   them; do not build for them.

---

## 6. The engineering loop

```text
question → hypothesis → bounded experiment → implementation → bench measurement
  → evidence → review → engineering conclusion → next experiment
```

Every experiment is bounded: it must be possible to state, in advance, what result would
falsify the hypothesis. An experiment that cannot fail is not an experiment.

Procurement, PCB design and system complexity are **gated by demonstrated need**. "We will
probably need it later" is not demonstrated need.

---

## 7. When work must stop and request a human bench action

Stop and explicitly request a human bench action when the next step requires any of:

- powering, wiring, probing, soldering or physically modifying hardware
- operating an oscilloscope, logic analyser, function generator, DMM, shaker or reference
  accelerometer
- flashing or resetting a physical target, or connecting a debug probe
- inducing a real physical stimulus (impact, vibration, drop, temperature)
- anything with an electrical, mechanical or personal safety dimension
- purchasing or selecting a physical component
- site or field access

The request must state: **objective, exact setup, procedure, what to record, expected
result, and what result would falsify the hypothesis.** Then stop. Do not write code that
assumes the outcome.

Where the answer is unknown pending that bench action, continue with every part of the task
that does not depend on it, and record the dependency in `project/status.yaml` under
`human_actions_required`.

---

## 8. Scope control

Prohibited without explicit human approval recorded in `project/status.yaml` or an ADR:

- silently changing product scope, target market or product definition
- adding a new subsystem, protocol, cloud service or hardware element not required by the
  current gate
- locking in a component, vendor, MCU, sensor, radio or cloud platform as a decision
  (candidates stay candidates until evaluated against evidence)
- introducing regulatory, compliance or certification requirements
- adding frameworks, orchestration platforms, task databases or CI systems

If scope needs to change, propose it as an ADR with alternatives and consequences. Do not
change it in passing while doing something else.

### Procurement discipline

> **Additional procurement must be justified by an explicit experimental limitation.**

A standing Frontier Mechatronics rule. Do not propose purchases because they may be useful
later. When an experiment cannot answer its question with the hardware in hand, that
limitation is the justification — and it is recorded in the experiment record *before* the
purchase, so the reasoning survives. Hardware in hand is recorded in
`hardware/inventory.md`.

---

## 9. Review expectations

Every change is reviewable in isolation. A change that cannot be reviewed without a verbal
explanation is not finished.

A change must state:

- **what** changed and **why now**
- which requirement(s), gate and experiment it serves
- what evidence supports any behavioural claim it makes
- what is *not* covered — untested paths, assumptions, known gaps

Claude is expected to review its own diff for unnecessary complexity before handing off.
Codex is expected to disbelieve the summary and check the diff.

**Unsupported claims are defects.** A sentence such as "sampling is stable at 1 kHz" with no
evidence reference is a review-blocking finding regardless of whether it later turns out to
be true.

---

## 10. Branch and commit expectations

- `main` is the integration branch and should always be coherent.
- Work happens on branches: `feature/<slug>`, `exp/EXP-nnnn-<slug>`, `fix/<slug>`,
  `docs/<slug>`.
- Commits are small, single-purpose and buildable where a build exists.
- Commit subject: `<area>: <imperative summary>` — e.g. `firmware: add sample tick counter`,
  `exp: record EXP-0001 measured results`.
- The body states why, and references identifiers: `Refs: SV-ACQ-002, EXP-0001, G1`.
- **Never amend, rebase away or rewrite a commit that records accepted evidence.** Evidence
  history is an engineering record.
- Never commit fabricated evidence files. Never commit a measurement placeholder that reads
  as real; use `TBD` or omit the field.

---

## 11. Documentation expectations

- Plain text and Markdown by default. YAML only where machine readability genuinely helps.
- **One canonical location per fact.** Do not duplicate project state into summaries;
  reference `project/status.yaml` instead. Duplicated state is treated as a defect.
- Every directory that exists has a `README.md` explaining its purpose and conventions.
  Directories without a purpose should not exist.
- Any behavioural claim carries an evidence reference or an explicit `assumed` / `predicted`
  label.
- Update `project/status.yaml` in the same change that alters project state.

---

## 12. Testing philosophy

See `tests/README.md` for the full definition. In short:

| Level | Proves | Does not prove |
|---|---|---|
| Unit | logic in isolation | anything about hardware |
| Integration | components agree across an interface | electrical or timing reality |
| Hardware-in-the-loop | software on real hardware, automated | correctness of the physical setup |
| Bench experiment | physical/electrical behaviour, human-run | that software handles it correctly |
| Fault injection | behaviour under failure and degradation | nominal-path correctness |

> A software test does not prove electrical behaviour.
> A bench observation does not automatically prove software correctness.

Both forms of evidence are required where a claim spans both domains.

---

## 13. Agent handoff — read this order

An incoming agent orients itself by reading, in order:

1. `AGENTS.md` (this file) — rules of engagement
2. `project/status.yaml` — the single machine-readable statement of current state
3. the current gate file in `project/gates/` — what "done" means right now
4. the active experiment record in `experiments/` (if any)
5. the requirements referenced by that gate/experiment in `requirements/product.yaml`
6. recent ADRs in `docs/decisions/`
7. any open messages addressed to it in `project/coordination/` (see §14)

Then run `python3 tools/validate_repo.py` to confirm the repository is self-consistent. It
reports open coordination threads, which is the fastest way to see what is awaiting a
response.

There is no separate handoff document, and there must never be one: it would become a
second, competing statement of project state.

---

## 14. Agent coordination

Parties work in separate sessions, and ChatGPT has no continuous repository access.
`project/coordination/` is an append-only ledger of messages between them, so that
questions, challenges and agreed next steps survive the session and appear in the diff.

Conventions are in `project/coordination/README.md`. In summary:

- One file per message, named `YYYYMMDDThhmmssZ-<nonce>-<sender>-to-<recipient>.md`, never
  edited or deleted once committed. The timestamp is always the true creation time; the
  random nonce, not an adjusted clock, resolves collisions.
- ChatGPT has no direct writer: its input is relayed by whoever transcribed it, declaring
  `Relayed from` and its provenance. Never file a message under a party that did not write
  it. `To: All` broadcasts are notification-only.
- Replies are new files naming the earlier message. There is no index, inbox or status
  field; open threads are derived and reported by `tools/validate_repo.py`.

### Sending is human-initiated

**An agent writes a message only when the human engineering lead requests it.** Agents do not
send unprompted, and do not reply to an incoming message on their own initiative.

The reason is that two agents that may each answer the other will: an exchange can continue
indefinitely, consuming effort and drifting into decisions without the human seeing them.
The ledger is for coordination the human wants to happen, not a channel agents run between
themselves.

An agent may **propose** a message at any time, and should when it has something worth
sending — a finding, a blocked assumption, a disagreement. The human decides whether it is
sent.

A consequence for readers of the open-threads report: a thread may stay open because the
reply has not been requested yet, not because it was forgotten. Open threads are a queue for
the human, not an obligation an agent discharges on its own.

**The ledger is never canonical project state.** It holds no decisions, requirements,
evidence, measurements or acceptances — those live in the artifacts listed in §4 and §13.
Specifically, a message may not:

- authorise physical work, or substitute for a bench request in `status.yaml`
  (`human_actions_required`)
- select hardware, or record a decision that belongs in an ADR
- accept evidence or mark a gate passed
- contain a measurement — reference the evidence ID instead

Any agreed outcome is written into its canonical artifact **in the same change** as the
message agreeing to it. If understanding a canonical artifact requires reading a message,
the artifact is incomplete: fix the artifact, not the message.
