# Test fixtures

Mounts, stimulus rigs and jigs used to produce repeatable physical conditions.

A fixture is part of the measurement. Its mass, stiffness, mounting and coupling change what
the sensor sees, so a fixture carries a revision (`HW-fixture-<name>-rNN`) and is recorded in
experiment setups like any other hardware.

Empty at G0. Fixture needs should be driven by an experiment that cannot be run without one
— starting with G1's requirement for a repeatable physical stimulus.
