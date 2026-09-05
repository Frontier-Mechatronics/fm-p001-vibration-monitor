# Experiments

An experiment is a **bounded** question put to physical reality. It must be possible to
state, before running it, what result would falsify the hypothesis. An experiment that
cannot fail is not an experiment.

```text
question → hypothesis → bounded experiment → implementation → bench measurement
  → evidence → review → engineering conclusion → next experiment
```

## Layout

```text
experiments/
├── README.md                    this file — experiment conventions
├── evidence.md                  evidence ID and provenance conventions
├── templates/
│   ├── experiment-template.md   copy this to start an experiment
│   └── evidence-manifest.yaml   copy this into an experiment's evidence/ directory
└── EXP-nnnn-<slug>/
    ├── EXP-nnnn.md              the experiment record
    └── evidence/
        ├── manifest.yaml        what each evidence file is and how it was produced
        └── <evidence files>
```

No experiments exist yet. The first will be created at G1.

## Identifiers

`EXP-nnnn`, allocated in order, never reused. The directory is
`EXP-nnnn-<short-slug>`; the record inside is `EXP-nnnn.md`.

## Lifecycle

| Status | Meaning |
|---|---|
| `draft` | Being designed. Objective, hypothesis, procedure being written. |
| `ready` | Design reviewed; awaiting a human bench session. |
| `running` | Bench work in progress. |
| `analysed` | Measured results and analysis recorded. |
| `accepted` | Human engineering lead accepts the evidence and conclusion. |
| `rejected` | Evidence unsound (bad setup, bad procedure, unrepeatable). Kept, not deleted. |
| `abandoned` | Not completed. Record why. Kept, not deleted. |

Sections up to and including **Procedure** are written *before* the bench session and are
not edited afterwards to match what happened. If the procedure changed on the bench, record
the deviation in the results section. Rewriting a plan to match the outcome destroys the
value of having planned it.

## Hard rules

1. **Never fabricate a measured result.** Fields for measured values stay `TBD` until a
   human produces them.
2. **A failed experiment is a valid engineering artifact.** Record it fully. Never rewrite a
   failure as a success, and never quietly delete one.
3. **A negative result must state what it rules out.** That is its value.
4. **Record the setup precisely enough to repeat it** — hardware revision, firmware commit,
   configuration, instrument settings, probe placement, mounting, environment.
5. **Agents do not run experiments.** Agents design them, provide tooling, and analyse
   results the human produces (AGENTS.md §7).
6. **One experiment, one question.** If it needs two hypotheses, it is two experiments.

## Design rules

An experiment that produces a durable engineering constraint records it as a **design
rule** — a short, testable statement carried forward (e.g. "the acquisition timer must not
share a timebase with X"). Design rules are the compounding output of the program; they are
why running an experiment is worth more than reading a datasheet.

## Fault injection

Where a subsystem's failure behaviour matters, the experiment includes a fault-injection
section: disconnect the sensor, brown out the supply, corrupt a frame, fill the storage,
drop the link. Nominal-path evidence alone does not describe how a field instrument
behaves.
