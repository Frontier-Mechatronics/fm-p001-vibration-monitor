# Edge gateway

Software for the Linux edge gateway: receives events and waveforms from nodes, persists them
locally, and forwards to the cloud when connectivity allows.

Empty at G0. Gateway work begins at G5.

Requirements in scope when it does: `SV-COM-001` (reception with corruption detection),
`SV-GW-001` (persistence across restart), `SV-GW-002` (operation during cloud outage).

The defining constraint is ADR-0003: the gateway must be fully functional with no cloud
present. That is an architectural property, not a fallback mode to add later.
