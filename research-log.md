# Research Log

Chronological record of research decisions and actions. Append-only.

| # | Date | Type | Summary |
|---|------|------|---------|
| 1 | 2026-06-13 | bootstrap | Initialized AgentSandBoxResearch workspace and heartbeat automation `autoresearch-loop-2`. |
| 2 | 2026-06-13 | bootstrap | Surveyed recent agent security work: AgentDojo, WASP, AgentHarm, SWE-agent, SandboxEscapeBench, and public reports on configuration-based sandbox escape. |
| 3 | 2026-06-13 | outer-loop | Selected one direction: a safe NDSS-style benchmark for semantic/configuration-based sandbox escape attacks against coding agents. Deferred broad defense combinations. |
| 4 | 2026-06-13 | inner-loop | H1 run_001: implemented safe toy oracle and seed dataset. Synthetic indirect baseline SSE-SR=0.60; benign control SSE-SR=0.00. This validates metric plumbing only, not real agent risk. |
| 5 | 2026-06-13 | inner-loop | H1 run_002: added ReAct-style trace parser and safe mock trace generator. Random trace control SSE-SR dropped to 0.00; indirect remained 0.60. This fixes the run_001 random-baseline artifact. |
| 6 | 2026-06-13 | pivot | Reframed project from benchmark-only SSE-Bench paper to SandScout technical method paper: automated mining, real-agent execution, and benchmark artifact as outcome. |
| 7 | 2026-06-13 | inner-loop | H1 run_003: implemented `src/sandscout_miner.py` and generated one mined instruction-hierarchy candidate on the current repository. |
| 8 | 2026-06-13 | inner-loop | H1 run_004: attempted Codex CLI real-agent smoke test in disposable workspace. Codex launched and inspected files, but repeated stream reconnects exceeded the wait budget; sentinel was not created. |
| 9 | 2026-06-13 | inner-loop | H1 run_005: implemented hardened real-agent runner. Codex CLI timed out after 45 seconds, but the run produced structured prompt/stdout/stderr/diff/trace/summary and oracle metrics. |
| 10 | 2026-06-13 | inner-loop | H1 run_006: added minimal fixture mode and fixed untracked-file trace inference. Codex CLI completed, created `.sse/instruction_hierarchy.sentinel`, and scored SSE-SR=1.00 on the minimal fixture. |
| 11 | 2026-06-13 | inner-loop | H1 run_007: created six-repository synthetic corpus and batch mining driver. SandScout mined 12 safe sentinel tasks across 5 boundary classes, including 7 high-confidence candidates after confidence scoring. |
