# FM-P001 G0 Solution Architecture Review — 2026-09-05

**Reviewer:** ChatGPT — Solution Architect / Technical Program Lead  
**Scope:** Gate G0 — Project definition / Agentic Harness v0.1  
**Result:** **READY WITH MINOR CHANGES / DEFERRED ACTIONS**

## Overall assessment

Harness v0.1 is suitable to begin FM-P001.

The repository clearly separates physical evidence from software assertion, has a single canonical project state, keeps future gates deliberately under-specified, prevents agents from self-certifying hardware gates, and provides a credible handoff path for Claude, Codex and the Solution Architect. G0 correctly makes no claim about physical or software product behaviour.  

Codex independently demonstrated that a cold reader could recover the current gate, absence of experiments/evidence and the G1 blocker from the repository alone. Its review also correctly notes that structural validation cannot establish measurement quality or truth. 

I find **no architectural defect that should block G0 acceptance**.

The findings below should be incorporated as G1/G2/G5 preparation rather than expanding G0.

---

## 1. Requirement-set shape

### Finding

The current draft set is appropriately small for G0. All eleven requirements are explicitly `draft`; implementation technologies remain undecided; open questions are carried alongside the requirements rather than being hidden. 

The absence at G0 of requirements covering power, environment, mounting/coupling, security, configuration and updates is **acceptable**.

Adding all of them now would create false precision before the product has produced its first measurement.

### Required timing

They should not all be deferred equally.

**Before G2 opens:**

- mounting / sensor coupling must become explicit;
- measurement orientation must become explicit;
- any calibration/traceability requirement necessary for physical-unit claims must exist.

Mounting is part of the measurement chain, not merely enclosure design. G2 cannot meaningfully characterise an instrument without defining how mechanical energy reaches the sensor.

**Before G5 opens:**

At minimum establish requirements or explicit architectural constraints for:

- device identity;
- configuration identity/versioning;
- message/data integrity;
- node↔gateway trust/security model;
- behaviour under duplicate, incomplete and corrupt transfers;
- configuration ownership and persistence.

`SV-SYS-002` already provides an excellent foundation by requiring hardware, firmware, configuration and time provenance. 

**May remain later than G5:**

- production power budget — before wireless/custom-node decisions become binding, likely G7;
- environmental operating envelope — before rugged PCB/enclosure/field deployment, G8–G10;
- firmware update/OTA requirement — before remote/deployed fleet architecture becomes binding, likely G7/G8;
- detailed cybersecurity implementation — derived from the earlier G5 trust model;
- regulatory/certification requirements — continue to defer until product maturity justifies them.

### G0 disposition

**DEFER. No G0 change required.**

---

## 2. 1 kHz / three-axis targets

### Finding

Three axes is a reasonable **working experimental scope**, but is not yet a derived product requirement.

The 1 kHz figure should not be treated as a defensible product sampling requirement yet. The repository already acknowledges this correctly: `SV-ACQ-002` labels 1 kHz as an assumed starting point not derived from a bandwidth requirement. 

G1 should therefore do both:

1. configure a nominal experimental target where the available hardware permits it; and
2. independently measure what the acquisition system actually produces.

G1 should **not derive the final sampling requirement from what convenient hardware happens to achieve**.

That would reverse the engineering logic.

### Recommended model

Treat:

**1 kHz = experiment target**

not:

**1 kHz = established product need**

G1 answers:

> Can we build and independently measure a deterministic acquisition path around this useful starting region?

Later domain/signal investigation answers:

> What sampling rate and bandwidth does the product actually require?

### What would make 1 kHz defensible?

I would require evidence supporting at least:

- the highest vibration-frequency content that materially matters to the chosen construction use cases;
- required anti-alias transition band;
- sensor bandwidth/filter characteristics;
- DSP operations to be performed;
- allowable timing jitter for those operations;
- desired engineering margin above Nyquist;
- evidence from representative captured vibration signals.

Only after this chain exists:

```text
physical phenomenon of interest
    → required measurement bandwidth
    → anti-alias strategy
    → sampling-rate requirement
```

should 1 kHz become an accepted product requirement.

### G0 disposition

**DEFER. Before G1 opens, clarify that 1 kHz is an experimental target and not a product-derived requirement.**

The current wording already substantially does this, so this is not a G0 blocker.

---

## 3. G1 acquisition before G2 characterisation

### Finding

The current ordering is correct.

G1 establishes that a physical sensor can be acquired continuously at a **known measured rate**, with measurable jitter, observable axis response and detectable communication failure. G2 then establishes what those samples mean as an engineering instrument. 

Absolute traceability does **not** need to precede G1.

Trying to establish traceable magnitude before proving the digital acquisition path would couple too many uncertainties:

```text
sensor response
+ mechanical coupling
+ calibration
+ firmware
+ timing
+ transport
```

G1 should isolate acquisition.

The decision to keep pre-G2 noise results in raw counts or explicitly provisional units is correct. Codex's change here materially improved the gate. 

### One refinement

G1 should avoid describing a manually applied stimulus as a **known physical stimulus** unless its magnitude is actually known.

Prefer:

> controlled/repeatable directional stimulus

unless a reference instrument or controlled excitation provides magnitude traceability.

### G0 disposition

**NO CHANGE REQUIRED.**

---

## 4. ADR-0002 — node → gateway → cloud scope

### Finding

I support ADR-0002.

The decision explicitly distinguishes:

> declaring the whole product chain

from:

> building the whole product chain now.

That distinction is architecturally sound. 

The end-to-end scope is important because interface problems are part of the capability FM-P001 is deliberately intended to develop. Restricting Product 001 to the sensor would remove a major part of the intended learning and product value.

R-021 correctly identifies premature breadth as a risk and gate discipline is currently sufficient mitigation. 

### Revisit ADR-0002 if

Use its existing revisit triggers, particularly:

- evidence shows one segment is substantially better provided externally;
- scope breadth demonstrably slows depth at the current gate;
- actual market learning narrows the useful product boundary.

I would add one conceptual rule:

> Owning the end-to-end product experience does not require manufacturing or implementing every underlying subsystem ourselves.

That will become important later for gateways, radio infrastructure and cloud components.

### G0 disposition

**ADR-0002 ACCEPTED AS WRITTEN.**

---

## 5. ADR-0003 — cloud-loss operation

### Finding

I support the **decision**, but would eventually weaken the dependence of its rationale on the unmeasured claim that construction sites have poor/intermittent connectivity.

ADR-0003 correctly labels this environmental premise as assumed rather than measured. 

However, I think the architecture can be justified more strongly without it:

> A monitoring instrument should preserve its primary measurement function during temporary loss of an upstream service.

That is a resilience/product-integrity principle even on sites that normally have excellent connectivity.

Therefore:

```text
cloud outage resilience
```

need not depend completely on proving:

```text
construction sites usually have bad internet
```

### What does require evidence?

The **offline endurance** absolutely requires evidence and domain input.

There is an enormous design difference between requiring:

- 15 minutes;
- 8 hours;
- 3 days;
- 2 weeks

of offline retention.

That number drives storage and protocol decisions.

### Recommendation

Do **not** wait until G10 to learn about connectivity if site access becomes conveniently available.

Perform a lightweight site-connectivity reconnaissance before G5/G7 design choices become expensive.

This does not need to become an early formal product experiment unless access is available. It can initially be domain evidence supporting requirements.

### ADR-0003 proposed refinement

Keep the decision.

At or before G5, revise the rationale toward:

> Monitoring continuity during upstream loss is a product requirement. Actual site connectivity evidence determines the required offline endurance and therefore storage/transfer sizing.

### Revisit trigger

Revisit the required **degree** of offline capability if:

- measured site connectivity is highly reliable;
- required local retention materially damages cost/power complexity;
- the deployment model changes.

I would not currently revisit the basic principle that cloud availability should not determine whether vibration is measured.

### G0 disposition

**DEFER refinement to pre-G5. Not a G0 blocker.**

---

## 6. Harness proportionality

### Finding

Harness v0.1 is on the **heavy side for one human**, but appropriate for this specific program because three independent agents will operate asynchronously across hardware, firmware, gateway and cloud work.

The important question is not file count; it is whether maintaining the artifacts displaces engineering.

The current harness has several good anti-bureaucracy properties:

- one canonical status file;
- no duplicate handoff document;
- future gates intentionally under-specified;
- no task database;
- no orchestration framework;
- no CI/HIL system yet;
- evidence conventions rather than an evidence platform;
- explicit instruction to delete unnecessary abstraction. 

R-022 correctly makes harness overhead something to evaluate through actual G1 use rather than debate theoretically. 

### Review rule after G1

After the first complete experiment, ask:

1. Which artifacts were naturally useful?
2. Which required duplicate entry?
3. Which were never consulted?
4. Which omissions caused confusion?
5. How much agent effort went into maintaining process rather than engineering?

Delete or simplify anything that fails that test.

### G0 disposition

**NO CHANGE REQUIRED.**

---

## 7. Next highest-value experiment / DQ-002

### Finding

I agree with the current working position:

> **Do not procure a product candidate merely to start G1 if suitable accelerometer/MCU hardware is already available.**

G1's purpose is to establish the **measurement and evidence method**, not select the final sensor.

Using known hardware in hand reduces simultaneous uncertainty and gets the physical engineering loop running earlier.

The current G1 file expresses this correctly. 

### EXP-0001 should answer one narrow question

I recommend:

> **Can the existing bench hardware produce a continuous three-axis sample stream whose actual sample timing can be independently measured and reconciled with the firmware record?**

That is enough for the first experiment.

Do not attempt in EXP-0001 to establish:

- sensor suitability for construction;
- calibrated vibration magnitude;
- product bandwidth;
- final sample rate;
- final MCU;
- DSP suitability;
- mounting design.

### Initial acceptance concept

EXP-0001 should produce:

- identifiable physical sensor and MCU hardware;
- firmware revision;
- sensor configuration;
- continuous XYZ stream;
- independent timing capture;
- measured average sample interval;
- measured interval variation appropriate to available instrumentation;
- explicit accounting for gaps/errors;
- retained raw dataset;
- enough provenance to reproduce the run.

The first experiment should be almost boring.

That is desirable.

It establishes the evidence chain on which every more interesting vibration experiment will depend.

### Procurement rule

Only procure for G1 if hardware already owned cannot expose the phenomena G1 needs to measure.

Procurement then follows from an explicit experiment limitation, not from anticipated product architecture.

### G0 disposition

**Resolve DQ-002 by inventory first. No component selection ADR is warranted yet.**

---

# Findings requiring action before G0 pass

**None.**

I found no architecture or harness issue requiring repository modification before human acceptance of G0.

G0 correctly establishes process and conventions without claiming product behaviour, and Codex has independently demonstrated the cold-handoff path.  

---

# Deferred architecture actions

Record these for the relevant future gates rather than expanding G0:

1. **Before G1:** retain 1 kHz explicitly as an experimental target, not a derived product requirement.
2. **During G1:** prove acquisition timing before attempting calibrated vibration claims.
3. **Before G2:** define mounting/coupling/orientation and physical-unit traceability requirements.
4. **Before G5:** define minimum device identity, configuration, trust/security and transfer-integrity requirements.
5. **Before G5/G7:** derive an offline-endurance target using available deployment/domain evidence.
6. **After first completed experiment:** explicitly review Harness v0.1 overhead under R-022.
7. **Do not select the product accelerometer or MCU until experiment evidence creates a reason to do so.**

---

# Recommendation

## **G0 READY TO PASS**

From the Solution Architect perspective, **G0-16 is satisfied**.

The harness is suitable for beginning physical engineering and is appropriately explicit about what it does **not** prove.

The only remaining G0 decision should be **G0-17 — human engineering lead acceptance**.

If the human accepts G0, the next action should be:

> **Close G0, open G1, inventory the sensor/MCU hardware already physically available, and draft EXP-0001 around the narrow acquisition-timing question above.**

No product-component procurement should occur before that inventory and experiment definition.