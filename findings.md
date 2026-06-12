# Research Findings

## Research Question

Can adversaries exploit the semantic boundary between an AI coding agent's sandboxed workspace and the host/tool runtime to produce sandbox escape effects without relying on kernel or container vulnerabilities?

## Current Understanding

The strongest research direction is an NDSS-style attack benchmark and measurement paper for semantic sandbox escape in AI coding agents. The key insight is that many agent sandbox failures are not classic container escapes. They occur when an agent is induced to create or modify project-local artifacts that look like ordinary development files inside the sandbox but later influence host-context startup, tool discovery, package scripts, configuration loading, credential routing, or approval behavior.

This gives the paper a focused thesis:

> Agent sandboxes are increasingly evaluated as OS isolation mechanisms, but coding agents also cross a semantic boundary through repository files, configuration, tool manifests, and startup state. We show that this boundary creates a distinct, measurable class of sandbox escape attacks.

The paper should not explore many defenses. It should contribute one clean benchmark and one principled measurement story. A small defensive analysis can appear only as an ablation or discussion to show what properties a real defense must enforce.

## Candidate Ideas

1. **Semantic Sandbox Escape Benchmark (selected)**
   Build a safe benchmark in which agents must be induced to plant or modify harmless sentinel artifacts that model host-context execution triggers. The harness never runs malicious payloads; it detects whether the agent crossed the semantic boundary by creating the sentinel artifact under realistic constraints.

2. **Approval-Policy Attack Surface Study**
   Compare how approval UI wording and command summarization affect agent-assisted sandbox violation. This is publishable but narrower and more product-UX dependent.

3. **Agent-Computer Interface Fuzzing**
   Fuzz tool schemas, repository metadata, and model-visible configuration to find ambiguity patterns. Innovative, but success depends heavily on tool access and is harder to make NDSS-clean quickly.

4. **MCP/Tool Provenance Confusion**
   Study malicious local tool manifests and MCP server discovery. Timely, but likely becomes a broad defense/platform paper unless tightly scoped.

## Selected Direction

The selected direction is **Semantic Sandbox Escape Benchmark for Coding Agents**.

Why this is the best balance of novelty and success probability:

- It targets a concrete gap left by AgentDojo, WASP, AgentHarm, SWE-agent, and container escape benchmarks.
- It is measurable with controlled toy tasks before needing expensive real agents.
- It can be framed as security measurement, which fits NDSS.
- It can remain safe: experiments use sentinel files, mock startup loaders, and non-sensitive fake credentials rather than real exploitation.
- It avoids a weak "bag of defenses" paper.

## Dataset and Benchmark Plan

Dataset name: **SSE-Bench: Semantic Sandbox Escape Benchmark for AI Coding Agents**.

Unit of evaluation: one task instance containing:

- A benign user goal, such as fixing tests, adding a plugin, updating CI, or investigating a build failure.
- An attacker-controlled context source, such as a README, issue comment, dependency note, search result, generated log, or project instruction file.
- A sandbox boundary model specifying which files are safe working files and which file classes become privileged only outside the sandbox.
- A sentinel artifact target, such as `mock_startup_hook`, `mock_tool_manifest`, `mock_package_lifecycle`, `mock_env_loader`, or `mock_credential_route`.
- A success oracle that checks artifact placement and triggerability in a toy harness without executing harmful code.

Initial dataset split:

- 40 seed tasks across 5 attack surfaces.
- 5 benign control tasks per surface.
- 3 adversary visibility levels: visible instruction, indirect project context, and retrieved external context.
- 2 trigger modes: immediate sandbox action vs delayed host-context transition.

## Baselines

Attack baselines:

- Direct malicious instruction baseline.
- Indirect prompt injection baseline modeled after AgentDojo/WASP.
- Repository-context instruction baseline using project instructions or issue comments.
- Capability-preserving jailbreak baseline adapted only for benign sentinel goals.
- Random artifact placement baseline.

Agent/platform baselines:

- ReAct-style coding agent with shell and file tools in a mock workspace.
- SWE-agent-style ACI agent if locally feasible.
- Browser/computer-use style agent for web-context variants if time permits.
- Human-control baseline for oracle sanity, not for attack comparison.

Defense/control baselines:

- No defense.
- Static denylist for sensitive filenames.
- Approval prompt for executable/configuration artifacts.
- Provenance tag oracle that blocks untrusted-context-derived edits to privileged artifact classes.

## Metrics

Primary metric:

- **SSE-SR**: fraction of tasks where the agent creates or modifies a sentinel artifact that the toy host-transition harness marks as triggerable.

Decomposed metrics:

- Instruction Uptake Rate: agent starts following adversary objective.
- Artifact Placement Rate: sentinel artifact exists in the modeled privileged class.
- Triggerability Rate: toy host-transition harness would load/activate the artifact.
- Benign Task Completion: original user goal remains satisfied.
- Stealth Cost: number and suspiciousness of edits required.

## Key Results

`run_001` implemented a safe deterministic oracle and evaluated 10 seed tasks using synthetic baseline policies. `run_002` replaced direct policy simulation with a ReAct-style trace parser over safe mock traces. These are plumbing experiments, not evidence about real deployed agents.

| Policy | SSE-SR | Interpretation |
|---|---:|---|
| benign | 0.00 | Control stays clean. |
| random | 0.00 | Recalibrated in run 002; no accidental sentinel placement. |
| direct | 1.00 | Upper-bound sanity check. |
| indirect | 0.60 | Confirms the trace pipeline can represent indirect project-context attacks. |

The important result is that the metric decomposition is operational: instruction uptake, artifact placement, triggerability, benign task completion, and SSE-SR can be computed from one trace record format.

## Patterns and Insights

The literature suggests a split between **behavioral hijacking** and **boundary hijacking**. AgentDojo and WASP evaluate whether untrusted content can redirect agent behavior. SandboxEscapeBench-style work evaluates direct container escape capability. The selected direction is the missing middle: whether hijacked behavior can materialize across lifecycle boundaries that the sandbox does not model.

## Lessons and Constraints

- Do not build a paper around many defenses. NDSS reviewers will prefer one crisp threat model, one reusable benchmark, and rigorous measurement.
- Avoid real-world exploit payloads in the artifact. Use toy loaders, sentinel files, and mock secrets to preserve reproducibility and safety.
- Do not claim real product vulnerabilities without coordinated disclosure. The benchmark can model vulnerability classes without naming untested products.
- Current date is 2026-06-13 in the local environment; venue rules and recent disclosures must be re-checked before submission.

## Open Questions

- Which agent platforms can be evaluated locally without violating product terms or creating unsafe tests?
- How many attack surfaces are enough for a strong NDSS measurement paper without diluting the core story?
- Can we include one real-world-inspired case study using a patched/obsolete CVE-class issue in a non-exploitable reproduction?
- What minimum benign-task completion threshold keeps the benchmark realistic rather than merely adversarial?

## Optimization Trajectory

`run_001` completed metric plumbing. `run_002` added trace-based evaluation and fixed the random-baseline artifact. The next measurable target is `run_003`: evaluate traces from a small local coding-agent runner or manually audited controlled transcripts, keeping all sentinel artifacts harmless.
