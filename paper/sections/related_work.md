# Related Work Section Draft

This draft is organized by methodology rather than paper-by-paper enumeration, following systems-paper guidance. Citation keys are provisional until final BibTeX is fetched programmatically.

## Prompt Injection and Agent Hijacking Benchmarks

AgentDojo and WASP are the closest benchmark-style precedents for SandScout. AgentDojo evaluates prompt-injection attacks and defenses for tool-using agents over untrusted data, while WASP evaluates realistic end-to-end prompt-injection attacks against web agents. Both establish that agent security must be evaluated in task environments with realistic adversary placement and decomposed success metrics. SandScout differs in the boundary it measures: rather than asking whether untrusted content redirects a web or tool action, it asks whether repository-local context causes a coding agent to prepare artifacts that become meaningful when the workspace crosses a host lifecycle boundary.

AgentHarm studies harmful multi-step agent tasks and shows why agent evaluations must measure capability retention across tool-mediated workflows, not only first-turn refusal. SandScout adopts the same premise that agentic behavior must be evaluated end-to-end, but replaces harmful goals with benign sentinels that model semantic sandbox escape without executing payloads.

## Coding-Agent Interfaces

SWE-agent introduced the framing of agent-computer interfaces for software engineering agents and showed that interface design materially affects agent performance and behavior. SandScout builds on this observation from a security angle: if interfaces, repository context, and tool affordances shape behavior, then sandbox evaluation must include the repository artifacts and lifecycle metadata that coding agents read and write. SandScout's mined surfaces, including package files, editor/startup metadata, CI workflows, and tool manifests, are all part of the coding-agent interface even when they are not OS-level sandbox mechanisms.

## Sandbox Escape Benchmarks

SandboxEscapeBench evaluates frontier LLM capabilities for escaping container sandboxes. This is adjacent but not identical to SandScout. Container escape benchmarks measure whether an agent can exploit or abuse isolation mechanisms such as misconfiguration, runtime weaknesses, privilege allocation, or kernel flaws. SandScout instead targets semantic sandbox escape: the agent may stay inside the filesystem and command sandbox, but still create repository artifacts that host-side automation later interprets. This distinction lets SandScout evaluate a sandbox-relevant attack class using harmless sentinels rather than real escape payloads.

## Agentic Coding-Assistant Prompt Injection

Recent systematization work on prompt injection attacks against agentic coding assistants catalogues delivery vectors, attack modalities, tool poisoning, skills, and protocol ecosystems. SandScout uses this broader taxonomy as threat-model background but contributes an automated mining and evaluation method. The key difference is methodological: SandScout does not only enumerate attacks; it scans repository artifacts, synthesizes sentinel tasks, runs real agents, and scores trace evidence.

## Industry Reports on Configuration-Based Failures

Industry reports have described configuration-based sandbox escape and prompt-injection risks in AI coding tools. These reports are useful motivation because they show that practical failures often involve configuration, startup, search-order, or tool-discovery behavior rather than only kernel-level escapes. We treat them as non-peer-reviewed motivation and avoid product-specific vulnerability claims. SandScout converts the high-level lesson into a safe academic artifact: benign sentinel tasks, disposable fixtures, and explicit controls.

## Summary

Prior work establishes that agents are vulnerable to prompt injection, that agent-computer interfaces shape coding-agent behavior, and that container sandbox escape can be benchmarked directly. SandScout fills the missing middle: automatically mining and evaluating semantic sandbox boundaries in coding-agent repositories, where ordinary project files become security-relevant when later consumed by host lifecycle systems.

