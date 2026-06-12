# Protocol: H1 Run 002 Trace-Based Metric Plumbing

## Hypothesis

Replacing hard-coded synthetic policies with parsed ReAct-style traces will make SSE-Bench closer to real agent evaluation while preserving the safe sentinel-only boundary.

## Change From Run 001

Run 001 simulated policy outcomes directly in the oracle. Run 002 introduces a trace schema:

- `thoughts`: model/agent reasoning summary or redacted trace notes
- `actions`: tool calls such as `write_file` and `edit_file`
- `final`: task completion marker

The oracle computes instruction uptake, artifact placement, triggerability, benign completion, and SSE-SR from trace contents.

## Prediction

The recalibrated random baseline should drop from 0.50 SSE-SR to 0.00 because random traces no longer receive deterministic sentinel placement. The indirect mock baseline should remain at 0.60 because 3 of 5 surfaces are marked susceptible in the mock traces.

## Safety Boundary

No trace contains exploit code or real product-specific payloads. The only boundary artifact is the harmless string `SSE_BENIGN_SENTINEL`.
