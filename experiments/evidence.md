# Evidence conventions

Evidence is the raw output of physical reality. It is the highest form of truth in this
project (AGENTS.md §2) and is treated as an immutable engineering record.

## Evidence IDs

| Prefix | Kind |
|---|---|
| `CAP-nnnn` | Oscilloscope / logic analyser capture (screenshot, CSV, native format) |
| `DATA-nnnn` | Raw dataset (sample stream, log export, sensor recording) |
| `IMG-nnnn` | Bench photograph (setup, wiring, fixture, DUT) |
| `MEAS-nnnn` | Measurement table — values read from an instrument by hand |
| `LOG-nnnn` | Device, firmware or gateway log output |

Numbers are allocated in order across the whole project and are never reused.
`tools/validate_repo.py` checks uniqueness.

## File naming

```text
<EVIDENCE-ID>_<EXP-ID>_<short-description>.<ext>
```

Example: `CAP-0001_EXP-0001_sample-tick-1khz.csv`

Evidence lives in the owning experiment's `evidence/` directory. Evidence produced outside
an experiment (e.g. an ad-hoc bench observation) still gets an ID and must be recorded
somewhere referenced from an experiment or gate file; untethered evidence is not evidence.

## Manifest

Every `evidence/` directory has a `manifest.yaml` (template:
`templates/evidence-manifest.yaml`). Each entry records enough provenance to identify:

- the experiment it belongs to
- the hardware unit and hardware revision
- the firmware/software commit
- the measurement setup (instrument model and identity, calibration status, settings, probe
  placement, coupling, mounting)
- the operator
- when it was recorded (see below)
- what was actually being measured, in words

Provenance that is unknown is recorded as `unknown`. It is never guessed.

### `recorded_at`

Either the literal `unknown`, or a calendar-valid ISO-8601/RFC-3339 timestamp **with an
explicit UTC offset**:

```yaml
recorded_at: 2026-09-05T14:32:10Z          # UTC
recorded_at: 2026-09-05T14:32:10+10:00     # local offset, retained as written
recorded_at: unknown                       # not known -- never guessed
```

A local offset is kept, not normalised to UTC: a bench session happens at a real local time,
and when a measurement was taken relative to the working day is sometimes the thing that
explains it. What is not acceptable is a timestamp with **no** offset, because it cannot be
placed on a timeline without knowing where it was written — `14:32:10` is not a moment.

`tools/validate_repo.py` rejects a missing offset, an impossible date or time, and any value
that is neither `unknown` nor a parseable timestamp. It cannot tell whether a well-formed
timestamp is the *right* one; that remains a review responsibility.

> Note for anyone hand-editing a manifest: YAML resolves an unquoted timestamp into a real
> date object, so an impossible one such as `2026-99-99T25:61:61Z` fails while the file is
> being read, and the validator reports it as an invalid timestamp rather than as a
> `recorded_at` finding. Both are errors; the message differs.

## Rules

1. **Raw evidence is never edited.** Corrections and derived views are separate files that
   reference the original ID.
2. **Never commit a fabricated or placeholder evidence file.** An absent measurement is
   `TBD` in the experiment record; it is not a stand-in file.
3. **Evidence is not deleted**, including evidence from failed or rejected experiments.
   Mark it rejected in the manifest with the reason.
4. **An evidence ID without a manifest entry does not count** as evidence.
5. **Screenshots are weaker than data.** Where an instrument can export values, export
   values; a photograph of a screen is a supplement, not a substitute.
6. **Acceptance is a human act.** Only the human engineering lead moves evidence to
   `accepted`, and only accepted evidence may support a gate criterion.

## Storage

Evidence is committed to git for now — this is a deliberate v0.1 simplification, adequate
while captures are small. It will not survive large continuous datasets (risk R-025). When
it starts to hurt, the storage decision is made in an ADR, not improvised.

Guidance until then: prefer exported CSV/text over binary instrument formats; downsample or
excerpt long captures and keep the excerpt criterion in the manifest; do not commit
multi-megabyte captures without raising it first.

## Note on `.gitignore`

The repository `.gitignore` excludes common build-output extensions (including `*.out`,
`*.map`, `*.a`, `*.hex`). If an evidence file ever collides with one of those patterns,
force-add it and note the exception here rather than renaming the instrument's output
silently.
