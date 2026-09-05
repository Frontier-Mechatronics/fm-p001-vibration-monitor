# Tools

Small, dependency-light scripts supporting the engineering process. Not product code.

| Tool | Purpose |
|---|---|
| `validate_repo.py` | Structural self-consistency check of the harness artifacts |

## `validate_repo.py`

```sh
python3 tools/validate_repo.py        # exit 0 = consistent, 1 = errors found
```

Requires PyYAML. Run it after any change to project state, requirements, gates, ADRs or
experiments, and as the first thing an incoming agent does after reading the handoff files
(AGENTS.md §13).

It checks:

- required harness files exist
- `project/status.yaml` parses, has its expected keys, uses a valid gate status, and points
  at a gate file that exists
- requirement IDs are well-formed and unique, with valid status, gate and verification
  methods
- every requirement appears exactly once in `traceability.md`, and no phantom requirement is
  referenced there
- gate filenames match the gate ID convention and the current gate has a file
- ADR filenames and numbers are valid and unique, each ADR has all required sections and a
  status, and each is listed in the ADR register
- experiment directories and IDs are well-formed and unique, records exist, statuses are
  valid
- evidence IDs are well-formed and unique across the whole repository, every manifest entry
  points at a file that exists, and **every file in an `evidence/` directory has a manifest
  entry** — an unmanifested file is not evidence
- evidence listed in `latest_accepted_evidence` actually exists
- each evidence item's `recorded_at` is either `unknown` or a calendar-valid ISO-8601
  timestamp with an explicit UTC offset — a missing offset or an impossible date is rejected
- every directory is documented, by its own README or by name in its parent's
- coordination messages have well-formed filenames, and their `ID` / `From` / `To` /
  `Created` headers agree with the filename; replies reference messages that exist
- messages carry a nonce, are sent by a party that actually has a writer, and use
  `Requires response: no` on broadcasts
- a relayed message carries a complete `Relay provenance` section — who supplied it, when
  (ISO-8601 UTC), whether it is verbatim or summarised, and its source — with no field left
  empty or as a placeholder. The heading alone does not satisfy the check
- **open coordination threads are reported** — messages requiring a response that no later
  message replies to. This is derived, not tracked, so nothing needs marking as resolved
- relative Markdown links resolve
- real experiment and ADR records contain no unfilled `nnnn` placeholders (warning)

### What it cannot check

It validates **structure, not truth**. It cannot tell a real measurement from an invented
one, a sound requirement from a bad one, or an honest conclusion from a convenient one.
A green run is a precondition for review, never a substitute for it (AGENTS.md §9).

## Adding tools

Keep them plain Python or shell, standard-library where possible, and documented in the
table above. Do not add a build system, task runner or CI configuration before there is
something to build (AGENTS.md §8).
