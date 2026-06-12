# Draft Paper Skeleton: SSE-Bench

Working title: **SSE-Bench: Measuring Semantic Sandbox Escape in AI Coding Agents**

## One-Sentence Contribution

We introduce SSE-Bench, a safe benchmark for measuring whether AI coding agents can be induced to cross sandbox boundaries by creating host-triggerable configuration and lifecycle artifacts, and we use it to show that semantic sandbox escape is distinct from both prompt-injection hijacking and classical container escape.

## Abstract Draft

AI coding agents increasingly run inside sandboxes, yet those sandboxes are often evaluated as operating-system isolation mechanisms rather than as part of an agent lifecycle. This misses a growing class of attacks in which adversarial context causes an agent to create or modify repository-local artifacts that are harmless inside the sandbox but meaningful when later interpreted by host startup logic, tool discovery, package lifecycle hooks, or configuration loaders. We present SSE-Bench, a safe benchmark for semantic sandbox escape in coding agents. SSE-Bench uses benign coding tasks, adversarial context sources, harmless sentinel artifacts, and a toy host-transition oracle to measure whether an agent crosses this semantic boundary without executing real exploit payloads. The benchmark decomposes attack success into instruction uptake, artifact placement, triggerability, and benign task completion, enabling comparisons across agents, interfaces, and policies. SSE-Bench aims to make sandbox-boundary failures reproducible, measurable, and suitable for artifact evaluation.

## Introduction Plan

1. Coding agents are moving from suggestion to action: reading repos, editing files, running commands, and invoking tools.
2. Sandboxes are the natural response, but sandboxing is commonly framed as OS isolation.
3. Gap: OS isolation does not cover lifecycle artifacts that cross from sandbox to host/tool runtime.
4. Key insight: a sandbox escape can be semantic rather than kernel-level.
5. Contributions:
   - Define semantic sandbox escape for AI coding agents.
   - Build SSE-Bench with safe sentinel artifacts and realistic adversarial contexts.
   - Provide decomposed metrics and baselines.
   - Evaluate defenses/policies only as controlled ablations, not as the main contribution.

## Design

SSE-Bench should have four modules:

- Task generator: creates benign coding tasks and adversarial context.
- Agent adapter: normalizes file/shell/tool interfaces.
- Sentinel oracle: checks whether sandbox-to-host semantic boundary would be crossed.
- Metrics reporter: computes SSE-SR and decomposition metrics.

## Evaluation Questions

RQ1: Do indirect project-context attacks produce semantic sandbox escape more often than random or benign controls?

RQ2: Which attack surfaces are most susceptible: startup/runtime discovery, tool manifests, package lifecycle config, environment routing, or instruction hierarchy?

RQ3: Does stronger agent capability increase end-to-end semantic escape, or do interface affordances dominate?

RQ4: Which single policy family most reduces escape while preserving benign task completion?

## Related Work Buckets

- Prompt injection and agent hijacking: AgentDojo, WASP.
- Harmful agent task benchmarks: AgentHarm.
- Coding-agent interfaces: SWE-agent and follow-up software-engineering agents.
- Container/sandbox escape: SandboxEscapeBench and classic container isolation work.
- Industry vulnerability reports: configuration-based sandbox escape and coding-agent command injection reports, used as motivation only.

## Citation Verification Notes

Do not generate BibTeX from memory. Before LaTeX submission, fetch citation metadata using Semantic Scholar, arXiv, CrossRef, or DBLP. Unverified 2026 arXiv results are marked in `literature/survey.md`.
