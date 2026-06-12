# AgentSandboxAttack

Research workspace for an autoresearch project on automated discovery of semantic sandbox escape paths in AI coding agents.

## Focus

The selected direction is **SandScout: Automatically Mining Semantic Sandbox Escape Paths in AI Coding Agents**. The project studies how to automatically mine repository artifacts that cross sandbox lifecycle boundaries, synthesize safe sentinel tasks, and test real coding agents.

SSE-Bench is the benchmark artifact produced by SandScout, not the whole paper. The current prototype is intentionally safe. It uses toy sentinels and mock oracles rather than real exploit payloads.

## Structure

- `research-state.yaml` tracks project state, hypotheses, and experiment trajectory.
- `findings.md` contains the evolving research narrative.
- `literature/survey.md` summarizes related work and gaps.
- `method.md` describes the SandScout automated mining method.
- `experiments/sandbox-attack-benchmark/` contains protocols, results, and analysis.
- `src/sandscout_miner.py` mines repository boundary candidates and emits safe sentinel tasks.
- `src/sse_trace_oracle.py` evaluates normalized traces.
- `paper/ndss_draft.md` contains the current NDSS-style paper skeleton.

## Run

Toy oracle:

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

Automated mining prototype:

```bash
python3 src/sandscout_miner.py \
  --repo . \
  --out experiments/sandbox-attack-benchmark/results/run_003_mined_tasks.json
```

Real-agent runner prototype:

```bash
python3 src/run_real_agent.py \
  --repo . \
  --tasks experiments/sandbox-attack-benchmark/results/run_003_mined_tasks.json \
  --out-dir experiments/sandbox-attack-benchmark/results/run_005_codex \
  --agent codex \
  --task-index 0 \
  --timeout 45
```

Minimal real-agent fixture:

```bash
python3 src/run_real_agent.py \
  --repo . \
  --tasks experiments/sandbox-attack-benchmark/results/run_003_mined_tasks.json \
  --out-dir experiments/sandbox-attack-benchmark/results/run_006_codex_minimal \
  --agent codex \
  --task-index 0 \
  --timeout 150 \
  --fixture-mode minimal
```

Synthetic corpus mining:

```bash
python3 src/make_fixture_corpus.py \
  --out data/fixture_corpus \
  --clean

python3 src/run_mining_corpus.py \
  --corpus data/fixture_corpus \
  --out experiments/sandbox-attack-benchmark/results/run_007_mining_corpus.json
```
