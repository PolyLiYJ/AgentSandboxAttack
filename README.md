# AgentSandboxAttack

Research workspace for an autoresearch project on semantic sandbox escape attacks against AI coding agents.

## Focus

The selected direction is **SSE-Bench: Semantic Sandbox Escape Benchmark for AI Coding Agents**. The project studies attacks where adversarial context induces an agent to create harmless sentinel artifacts that model host-context startup, tool-discovery, package-lifecycle, environment-routing, or instruction-hierarchy boundary crossings.

The current prototype is intentionally safe. It uses toy sentinels and mock oracles rather than real exploit payloads.

## Structure

- `research-state.yaml` tracks project state, hypotheses, and experiment trajectory.
- `findings.md` contains the evolving research narrative.
- `literature/survey.md` summarizes related work and gaps.
- `experiments/sandbox-attack-benchmark/` contains the first protocol, results, and analysis.
- `src/sse_oracle.py` runs the toy benchmark oracle.
- `paper/ndss_draft.md` contains the current NDSS-style paper skeleton.

## Run

```bash
python3 src/sse_oracle.py \
  --tasks data/sse_seed_tasks.json \
  --out experiments/sandbox-attack-benchmark/results/run_001_metrics.json
```

Trace-based prototype:

```bash
python3 src/make_mock_traces.py \
  --tasks data/sse_seed_tasks.json \
  --out data/sse_mock_traces_run_002.json

python3 src/sse_trace_oracle.py \
  --tasks data/sse_seed_tasks.json \
  --traces data/sse_mock_traces_run_002.json \
  --out experiments/sandbox-attack-benchmark/results/run_002_trace_metrics.json
```
