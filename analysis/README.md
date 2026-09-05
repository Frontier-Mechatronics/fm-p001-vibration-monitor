# Analysis

Host-side analysis of captured data: scripts and notebooks used to interpret evidence,
compute derived values, and produce the numbers quoted in experiment records.

## Rules

1. **Analysis is derived, evidence is raw.** Never modify a raw evidence file; read it and
   write derived output separately (`experiments/evidence.md`).
2. **Analysis must be re-runnable** from the raw evidence it consumes. A number in an
   experiment record should be reproducible by re-running the script that produced it.
3. **Name the evidence IDs consumed** at the top of every script, so a reviewer can trace a
   result back to the instrument that produced it.
4. Analysis output is `computed`, not `measured` (AGENTS.md §2). Label it that way where it
   is quoted.

Empty at G0 — there is no data to analyse. First content is expected at G1: rate and jitter
computation from a captured sample-tick trace.
