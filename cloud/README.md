# Cloud

Cloud-side ingestion and services: authenticated intake of events from gateways,
de-duplication, storage and retrieval.

Empty at G0. Cloud work begins at G6. **No cloud provider or service has been selected**;
all are candidates (`docs/decisions/README.md`).

Requirements in scope when it does: `SV-SYS-001` (end-to-end path), `SV-CLD-001` (event
inspection), and `SV-SYS-002` (provenance preserved end to end).

Because the gateway forwards on reconnection and transfers may be retried, ingestion must
assume duplicates and out-of-order arrival (ADR-0003).
