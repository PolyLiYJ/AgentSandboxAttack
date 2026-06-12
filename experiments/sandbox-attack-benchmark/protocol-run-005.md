# Protocol: H1 Run 005 Hardened Real-Agent Runner

## Hypothesis

A hardened real-agent runner with disposable git workspaces, timeout control, transcript capture, diff capture, and trace conversion will make SandScout real-agent evaluation reproducible enough to run on Codex CLI and later agents.

## Change From Run 004

Run 004 used a hand-written shell smoke test. It confirmed Codex CLI could launch and inspect files, but the run was interrupted after repeated stream reconnects and no structured trace was produced.

Run 005 introduces `src/run_real_agent.py`, which:

- creates a disposable git repository fixture
- writes the exact prompt to disk
- runs Codex CLI with a configurable timeout
- captures stdout, stderr, git diff, and summary JSON
- converts the diff into a normalized trace for `sse_trace_oracle.py`
- rejects prompts/tasks with unsafe terms

## Prediction

Even if Codex CLI times out again, the output will be structured enough to distinguish runner failure, model refusal, no-op completion, and sentinel creation.

## Safety Boundary

The task contains only the harmless `SSE_BENIGN_SENTINEL` marker. The runner rejects tasks containing credential access, exfiltration, malware, destructive shell commands, or non-benign sentinel values.
