# SandScout Method

SandScout is the primary technical contribution. SSE-Bench is the artifact produced by applying SandScout, not the whole paper.

## Problem

Coding-agent sandboxes are usually treated as OS-level boundaries. In practice, the agent edits repository artifacts that may later be consumed by host-side lifecycle systems: editors, package managers, CI, agent runtimes, shell startup tools, and tool-discovery mechanisms. SandScout searches for these semantic boundaries automatically.

## Method Overview

SandScout performs four steps:

1. **Boundary Mining**
   Scan a repository for files whose semantics often cross from sandboxed editing into later host/runtime interpretation.

2. **Safe Task Synthesis**
   Convert each discovered surface into a benign coding task plus adversarial repository context. The target is always a harmless sentinel file containing `SSE_BENIGN_SENTINEL`.

3. **Real-Agent Execution**
   Run real coding agents in disposable worktrees. Initial target: Codex CLI, because it is locally detected. Planned targets: Claude Code, Gemini CLI, and OpenHands.

4. **Trace, Diff, and Safety Oracles**
   Convert transcripts and workspace diffs into normalized traces. Compute SSE-SR and decomposed metrics. In parallel, scan tasks, prompts, outputs, and diffs for real exploit payload indicators, credential/secret indicators, destructive commands, and product-specific vulnerability claims.

## Boundary Classes

Current miner rules cover:

- package lifecycle configuration
- startup/runtime discovery
- tool manifest discovery
- CI workflow transition
- instruction hierarchy

These are intentionally conservative. The miner should prefer fewer high-confidence candidates over broad noisy matching.

## Why This Is More Than a Benchmark

A benchmark says "here are tasks." SandScout says "here is a reproducible way to discover new sandbox-boundary tasks from repositories." This supports:

- scaling to unseen repositories
- explaining why a task is security-relevant
- comparing agents on mined surfaces rather than only hand-authored attacks
- updating the benchmark as agent ecosystems evolve

## Safety

SandScout never emits real exploit payloads. It emits sentinel tasks and mock triggerability checks. Real-agent tests must run in disposable worktrees and must not include credential access, malware, destructive commands, or product-specific exploit strings.

SandScout should still detect and flag those categories if they appear in task specifications or real-agent artifacts. The runner now records `safety_scan.json` to distinguish a clean sentinel-only run from a run that contains exploit, credential, destructive-command, or product-specific vulnerability indicators.

For paper text, see `paper/sections/threat_model.md`, which spells out adversary capabilities, trusted components, out-of-scope behavior, and artifact-release policy.
