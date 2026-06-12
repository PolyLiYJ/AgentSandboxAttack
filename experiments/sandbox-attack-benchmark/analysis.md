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
