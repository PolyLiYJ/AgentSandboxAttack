# Research Log

Chronological record of research decisions and actions. Append-only.

| # | Date | Type | Summary |
|---|------|------|---------|
| 1 | 2026-06-13 | bootstrap | Initialized AgentSandBoxResearch workspace and heartbeat automation `autoresearch-loop-2`. |
| 2 | 2026-06-13 | bootstrap | Surveyed recent agent security work: AgentDojo, WASP, AgentHarm, SWE-agent, SandboxEscapeBench, and public reports on configuration-based sandbox escape. |
| 3 | 2026-06-13 | outer-loop | Selected one direction: a safe NDSS-style benchmark for semantic/configuration-based sandbox escape attacks against coding agents. Deferred broad defense combinations. |
| 4 | 2026-06-13 | inner-loop | H1 run_001: implemented safe toy oracle and seed dataset. Synthetic indirect baseline SSE-SR=0.60; benign control SSE-SR=0.00. This validates metric plumbing only, not real agent risk. |
