# Testing

Five distinct kinds of evidence. They are not interchangeable, and conflating them is a
review-blocking defect.

> **A software test does not prove electrical behaviour.**
> **A bench observation does not automatically prove software correctness.**

## The levels

| Level | Location | Runs on | Human required | Proves | Does **not** prove |
|---|---|---|---|---|---|
| Unit | `tests/unit/`, `firmware/tests/` | host | no | logic in isolation | anything about hardware |
| Integration | `tests/integration/` | host | no | components agree across an interface | electrical or timing reality |
| Hardware-in-the-loop | `tests/hil/` | real target, automated | setup only | software behaviour on real hardware | that the physical setup is correct |
| Bench experiment | `experiments/` | real hardware, human-run | yes | physical and electrical behaviour | that software handles it correctly |
| Fault injection | `tests/fault/`, experiments | host or target | sometimes | behaviour under failure/degradation | nominal-path correctness |

## Which to use

- A claim about **logic** → unit test.
- A claim about **an interface** → integration test.
- A claim about **timing, voltage, current, noise, or physical response** → bench
  experiment with instrument evidence. No exceptions.
- A claim that **software behaves correctly on the real target** → HIL, once it exists;
  until then a bench experiment with logged output.
- A claim about **what happens when something breaks** → fault injection, and record what
  was actually injected.

Claims spanning domains need evidence from both: "firmware samples at 1 kHz" requires a
measured tick interval (bench) *and* a test showing the sample buffer is filled correctly
(unit/integration). Either alone is a partial claim and must be stated as such.

## Current state

All four subdirectories are empty at G0 — no product code exists to test. `tests/unit/` and
`firmware/tests/` overlap deliberately: firmware-local unit tests live next to the firmware,
while `tests/unit/` is for cross-cutting host-side code (analysis, tooling, gateway).
Whichever is chosen for a given module, choose one; do not test the same unit in both.

The only executable check in the repository at G0 is `tools/validate_repo.py`, which checks
the harness itself, not the product.

## Conventions for when tests exist

- A test's name states the behaviour it asserts, not the function it calls.
- A test that has never failed has not been shown to test anything — verify new tests fail
  when the behaviour is broken.
- Tests that require hardware are never silently skipped; they fail loudly or are explicitly
  marked as requiring hardware.
- A test asserting a physical value must reference the evidence that value came from.
- Fixtures and recorded datasets used by tests reference the evidence ID they came from.

## Hardware-in-the-loop direction

Not implemented, and not to be implemented before G1 produces evidence about what is worth
automating. The eventual shape is expected to be:

```text
build → flash → reset → capture UART → collect instrument output
  → retain evidence → evaluate acceptance criteria
```

Structural expectations so this can be added later without reorganising: builds are
reproducible from a documented command; firmware emits machine-parseable output on a known
interface; evidence file naming follows `experiments/evidence.md` regardless of whether a
human or a script produced it; acceptance criteria are stated as checkable values.

**The human remains responsible for safe physical setup.** Automation may drive a rig that
is already safely built; it never makes it safe.
