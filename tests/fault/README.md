# Fault-injection tests

Deliberate failure and degradation: sensor disconnected, supply brown-out, buffer overrun,
storage full, link dropped mid-transfer, corrupted frame, cloud unreachable, clock stepped.

A field instrument is defined as much by its degraded behaviour as its nominal behaviour.
The question is never only "does it fail?" but "does it *detect* the failure, and is bad
data distinguishable from good data?".

Faults that can only be induced physically belong in an experiment record's fault-injection
section (`experiments/templates/experiment-template.md` §9); software-inducible faults belong
here.

Empty at G0.
