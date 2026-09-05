# Firmware unit tests

Host-side tests of firmware logic in isolation — buffer management, framing, feature
computation, state machines. No target hardware.

These tests prove logic. They prove nothing about timing, electrical behaviour or the real
device (`tests/README.md`). Claims about the target require bench or HIL evidence.

Empty at G0.
