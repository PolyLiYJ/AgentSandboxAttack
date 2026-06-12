# Protocol: H1 Semantic Sandbox Escape Benchmark

## Hypothesis

H1: A benchmark centered on semantic sandbox escape tasks will reveal a distinct vulnerability class: agents can create or modify artifacts that are inert inside the sandbox but become executable or privileged in a later host/context transition.

## Threat Model

The adversary cannot exploit the kernel, container runtime, or real host. The adversary can influence text that the agent reasonably ingests while doing a benign coding task: repository documentation, issue comments, logs, search results, project instruction files, or dependency notes.

The agent can read and write files and may run commands inside a sandbox. The benchmark evaluates whether the agent can be induced to create a **harmless sentinel artifact** in a location or file class that a toy host-transition harness would load.

## Safety Boundary

This experiment must not contain working malware, credential theft, destructive commands, or real product exploit payloads. It uses only sentinel strings and mock loaders.

## Dataset

Initial seed set:

- 5 attack surfaces:
  - startup/runtime discovery
  - tool manifest discovery
  - package lifecycle configuration
  - environment/credential routing
  - project instruction hierarchy
- 2 tasks per surface for `run_001`
- 1 benign control per surface

## Baselines

- random artifact placement
- direct adversarial instruction
- indirect project-context injection
- benign-only control

## Metrics

- Semantic Sandbox Escape Success Rate (SSE-SR)
- Instruction Uptake Rate
- Artifact Placement Rate
- Triggerability Rate in toy harness
- Benign Task Completion

## Prediction

Direct and indirect project-context attacks will outperform random placement. Indirect attacks will have lower instruction uptake but may still produce high artifact placement when the malicious instruction is framed as a legitimate project convention.

## Run Plan

`run_001` will implement a deterministic toy oracle and evaluate handcrafted seed tasks without invoking live third-party agents. Later runs can add real agents after the safety and disclosure boundary is reviewed.
