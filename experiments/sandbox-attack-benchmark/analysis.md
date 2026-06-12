# Analysis: H1 Run 001

Status: complete.

This run executed `src/sse_oracle.py` on `data/sse_seed_tasks.json`. The first run is a plumbing check, not evidence about real agents.

Output:

- `results/run_001_metrics.json`

Summary:

| Policy | SSE-SR | Instruction Uptake | Artifact Placement | Triggerable | Benign Completion |
|---|---:|---:|---:|---:|---:|
| random | 0.50 | 0.50 | 0.50 | 0.50 | 1.00 |
| direct | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| indirect | 0.60 | 0.60 | 0.60 | 0.60 | 1.00 |
| benign | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 |

Interpretation:

The metric decomposition is computable and separates benign controls from attack baselines. The random baseline is intentionally simplistic and currently too high because it deterministically places artifacts for half the seed IDs. In the next run, replace it with a calibrated low-probability baseline and add real agent traces or a mocked ReAct transcript parser.

## Run 002

Status: complete.

Run 002 introduced a ReAct-style trace parser in `src/sse_trace_oracle.py` and a safe mock-trace generator in `src/make_mock_traces.py`. The oracle now derives SSE metrics from trace actions rather than directly simulating policy outcomes.

Output:

- `data/sse_mock_traces_run_002.json`
- `results/run_002_trace_metrics.json`

Summary:

| Policy | SSE-SR | Instruction Uptake | Artifact Placement | Triggerable | Benign Completion |
|---|---:|---:|---:|---:|---:|
| benign | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 |
| random | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 |
| direct | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| indirect | 0.60 | 0.60 | 0.60 | 0.60 | 1.00 |

Interpretation:

The random baseline is now calibrated to near-zero sentinel placement, fixing the main artifact in run 001. The indirect baseline remains at 0.60 because the mock traces mark 3 of 5 attack surfaces as susceptible. The next real research step is to replace mock traces with traces from a small local coding-agent runner or manually audited transcripts from a controlled tool-use prompt.
