# Hardware-in-the-loop tests

Automated tests executing against real hardware: build → flash → reset → capture → evaluate.

**Not implemented.** Do not build HIL automation before G1 shows what is worth automating
(`tests/README.md`, "Hardware-in-the-loop direction").

A HIL run produces evidence and follows `experiments/evidence.md` naming and provenance
rules exactly as a human bench session does — the fact that a script collected it does not
make it a different class of evidence. The human remains responsible for the physical rig.
