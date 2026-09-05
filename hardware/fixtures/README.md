# Test fixtures

Mounts, stimulus rigs and jigs used to produce repeatable physical conditions.

A fixture is part of the measurement. Its mass, stiffness, mounting and coupling change what
the sensor sees, so a fixture carries a revision (`HW-fixture-<name>-rNN`) and is recorded in
experiment setups like any other hardware.

Empty. Fixture needs are driven by an experiment that cannot run without them, never
catalogued in advance (see [`../inventory.md`](../inventory.md)).

**Stimulus source is on order** — Vybronics VC1020B111F ERM motors, which provide a
*controlled, repeatable directional physical stimulus*, not a known magnitude. They are not
calibration references.

**Mounting remains unresolved and is not G1's to solve.** How the sensor couples to the
excited structure changes what it measures, which makes mounting a G2 measurement-system
concern. G1 works around it by claiming timing rather than magnitude.
