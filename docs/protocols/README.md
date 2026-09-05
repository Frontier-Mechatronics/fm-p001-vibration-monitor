# Protocols

Wire formats and interface definitions between system elements: node ↔ gateway, gateway ↔
cloud, and any host/debug interfaces used for evidence collection.

**Empty by design.** No protocol has been defined, and none should be defined before the
data it carries is understood. Protocol design without measured event sizes, rates and
failure behaviour produces a format that must be redesigned.

Expected first occupant: the node → gateway framing at G5, after G3/G4 establish what an
event record actually contains.

When a protocol is added it should specify: framing, field definitions with units and
ranges, byte order, versioning, integrity checking, error and retry behaviour, and what a
receiver does with a message it cannot parse.
