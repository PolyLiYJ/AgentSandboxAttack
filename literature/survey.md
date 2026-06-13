# Literature Survey: Agent Sandbox Attacks

## Summary

Recent agent security work has matured around prompt injection, harmful agent tasks, web-agent hijacking, and coding-agent interfaces. The sandbox-specific literature is newer. The gap is a reusable academic benchmark for **semantic sandbox escape**: attacks that abuse configuration, startup, workspace, and tool-discovery boundaries rather than OS/container vulnerabilities.

## Papers and Sources

### AgentDojo

- URL: https://arxiv.org/abs/2406.13352
- Venue/status: NeurIPS 2024 Datasets and Benchmarks Track, per project page.
- Contribution: Dynamic environment for prompt injection attacks and defenses in tool-using agents, with realistic tasks and security test cases.
- Relevance: Provides benchmark design precedent. It measures hijacking of agents over untrusted tool data but not sandbox escape through agent lifecycle artifacts.

### WASP

- URL: https://arxiv.org/abs/2504.18575
- Contribution: Web Agent Security against Prompt injection attacks; introduces realistic web-agent hijacking objectives and isolated environments.
- Relevance: Strong model for realistic adversary constraints and decomposed metrics. Its finding that agents often start adversarial instructions but fail end-to-end motivates decomposed sandbox metrics.

### AgentHarm

- URL: https://arxiv.org/abs/2410.09024
- Contribution: Benchmark of harmful multi-step agent tasks across harm categories.
- Relevance: Shows agent safety evaluation must measure whether the agent remains capable across steps, not only whether it refuses the first request.

### SWE-agent

- URL: https://arxiv.org/abs/2405.15793
- Contribution: Agent-computer interfaces for software engineering agents.
- Relevance: Establishes that the interface materially changes agent behavior. Our work asks how ACI design changes sandbox attackability.

### SandboxEscapeBench

- URL: https://arxiv.org/html/2603.02277v1
- Contribution: Open benchmark for measuring LLM capability to escape container sandboxes.
- Relevance: Adjacent but centered on container/OCI escape. SSE-Bench should explicitly distinguish itself by studying agent-level semantic boundaries.
- Verification note: arXiv metadata checked on 2026-06-13; see `literature/verified_sources.md`. Final BibTeX still needs programmatic fetch before submission.

### Prompt Injection Attacks on Agentic Coding Assistants

- URL: https://arxiv.org/html/2601.17548v1
- Contribution: Catalog of attack techniques against coding assistants, including tool poisoning and protocol exploitation.
- Relevance: Useful taxonomy for threat model and attack-surface selection.
- Verification note: arXiv metadata checked on 2026-06-13; see `literature/verified_sources.md`. Final BibTeX still needs programmatic fetch before submission.

### Configuration-Based Sandbox Escape in AI Coding Tools

- URL: https://cymulate.com/blog/the-race-to-ship-ai-tools-left-security-behind-part-1-sandbox-escape/
- Contribution: Industry report identifying configuration-based sandbox escape as a recurring class in AI CLI tools.
- Relevance: Strong motivation, but must not be treated as peer-reviewed evidence. Useful for threat-model examples and responsible disclosure discussion.

### Codex CLI RCE and Prompt Injection Mitigations

- URL: https://cymulate.com/blog/codex-cli-rce-prompt-injection-mitigations/
- Contribution: Industry discussion of prompt injection plus binary/search-order style risks in an AI CLI context.
- Relevance: Motivates delayed host-context trigger patterns. Use only as a real-world motivation source, not as a benchmark payload.

### NDSS Artifact Evaluation

- URL: https://www.ndss-symposium.org/ndss2026/submissions/call-for-artifacts/
- Contribution: NDSS encourages reusable artifacts; accepted papers can submit artifact appendices and badges.
- Relevance: SSE-Bench should be packaged as a safe artifact with clear reproducibility scripts.

## Gap

No surveyed academic benchmark cleanly asks:

> When an AI coding agent is sandboxed, can adversarial context cause it to prepare artifacts that become privileged only when the sandboxed workspace is later interpreted by the host, tool runtime, or startup system?

That gap is concrete, timely, and testable.
