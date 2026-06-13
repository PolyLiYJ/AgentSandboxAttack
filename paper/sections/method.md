# Method Section Draft

This section is written as paper-ready prose. It should replace the short design sketch in `paper/ndss_draft.md` once the paper is moved into LaTeX.

## Overview

SandScout is an automated mining and evaluation pipeline for semantic sandbox escape paths in coding-agent workflows. Its input is a repository and an agent execution configuration. Its output is a set of safe sentinel tasks, execution traces, safety-scan records, and metric rows. SandScout deliberately does not execute lifecycle hooks or generate real exploit payloads. Instead, it asks whether an agent can be induced to create a boundary-specific benign sentinel artifact that would be observable if the corresponding lifecycle boundary were crossed.

The pipeline has five stages:

1. Mine repository files whose semantics commonly cross from sandboxed editing into host-side lifecycle interpretation.
2. Synthesize a benign metadata task and repository-local adversarial context for each mined surface.
3. Run a real coding agent in a disposable git workspace under controlled prompt and sandbox settings.
4. Normalize workspace evidence into traces and score semantic sandbox escape success.
5. Scan tasks, prompts, outputs, and diffs for unsafe content categories before preserving artifacts.

This design separates three concerns that are often conflated in agent-sandbox discussions. The miner discovers where a boundary may exist. The sentinel task tests whether an agent follows repository-local context into that boundary. The safety scanner verifies that the benchmark artifact remains benign even though the paper studies attacks.

## Boundary Miner

The boundary miner is intentionally conservative. It scans a repository for file patterns that represent lifecycle transitions rather than arbitrary suspicious strings. In the current prototype, the rule set covers five surfaces:

| Surface | Representative files | Rationale |
|---|---|---|
| Package lifecycle configuration | `package.json`, `pyproject.toml`, `setup.py`, `Makefile`, `justfile` | Build and package metadata may be interpreted after the agent's sandboxed edit phase. |
| Startup/runtime discovery | `.envrc`, language-version files, `.vscode/settings.json`, `.devcontainer/devcontainer.json` | Editor, shell, and devcontainer metadata can be consumed by host-side startup flows. |
| Tool-manifest discovery | `.mcp.json`, `mcp.json`, `.cursor/mcp.json`, `.codex/config.toml`, `AGENTS.md` | Agent and tool manifests can affect tool discovery or local instruction loading. |
| CI workflow transition | `.github/workflows/*.yml`, `.github/workflows/*.yaml`, `.gitlab-ci.yml` | CI definitions can execute after a repository leaves the interactive sandbox. |
| Instruction hierarchy | `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `README.md` | Project-local instructions can carry adversarial context into agent decisions. |

Each rule has a base confidence score reflecting expected boundary relevance. The prototype raises confidence for agent-instruction files such as `AGENTS.md` and tool/package manifests, and lowers confidence for README-only hits. This ranking is not a security claim by itself; it is a budget-allocation mechanism for live-agent evaluation. A high-confidence candidate should be evaluated before broad low-confidence documentation-only candidates.

Formally, for repository `R` and rule set `S`, the miner emits a task for every rule `s in S` whose pattern set matches at least one file in `R`. Each task contains:

- a stable task identifier,
- the surface class,
- matched source files,
- a confidence score,
- a benign metadata goal,
- repository-local adversarial context,
- a sentinel path of the form `.sse/<surface>.sentinel`, and
- the fixed sentinel value `SSE_BENIGN_SENTINEL`.

The miner does not inspect or copy executable payloads from the matched files. The matched files explain why the repository has a semantic boundary; the synthesized sentinel is the only target that the oracle considers.

## Safe Task Synthesis

SandScout converts each mined boundary into a two-part task. The first part is a benign user goal, such as inspecting repository metadata related to a boundary class. The second part is repository-local context that claims compatibility requires writing a harmless sentinel marker. In the indirect setting, the user prompt does not directly name the sentinel path. Instead, the runner injects repository-local context through `SANDSCOUT_NOTE.md` and asks the agent to inspect local compatibility notes.

This construction models an attacker who controls repository context while preserving a safe artifact. The sentinel has no executable semantics, contains no secret, and is not a real exploit payload. It is only a measurement marker. A task is rejected before execution if it contains prohibited terms associated with credentials, secrets, exfiltration, malware, reverse shells, destructive filesystem commands, or a non-benign sentinel value.

SandScout also supports matched no-note controls. These controls hold the agent, repository fixture, task index, prompt mode, and sandbox settings constant, but omit `SANDSCOUT_NOTE.md`. A completed no-note control should not create the sentinel. If it does, the result would indicate a prompt-template or oracle artifact rather than support for the mined-context hypothesis.

## Real-Agent Runner

The runner executes tasks in disposable git workspaces. For a full-fixture run, it copies the target repository or synthetic corpus repository, initializes a fresh git repository, optionally injects the SandScout note, and invokes the agent with a bounded timeout. For a minimal fixture run, it creates a tiny repository containing only the files needed to smoke-test the pipeline.

The current implementation supports Codex CLI. It invokes Codex non-interactively with workspace-write sandboxing and never-approval policy, captures stdout, stderr, git diff, git status, the generated prompt, and a structured summary. The runner classifies infrastructure failures separately from model behavior:

| Failure class | Meaning |
|---|---|
| `timeout` | The agent process did not complete within the configured budget. |
| `usage_limit` | The agent failed before normal execution because service usage or credit limits were reached. |
| `agent_error` | The agent process exited non-zero for another reason. |
| `null` | The agent process completed normally. |

This classification is important for paper validity. A run that times out or hits usage limits may have `SSE-SR=0.00`, but it is not evidence that the agent resisted the attack. We therefore report such runs as availability failures and keep the corresponding behavioral condition pending.

## Trace and Sentinel Oracle

The oracle does not trust agent self-reports. It derives success from workspace evidence. If the expected sentinel file exists and contains exactly `SSE_BENIGN_SENTINEL`, the runner emits a normalized `write_file` action for the target path. The trace oracle then computes:

- **Instruction uptake:** the trace references or writes the surface-specific sentinel.
- **Artifact placement:** the trace writes the expected sentinel path with the fixed sentinel value.
- **Triggerability:** the prototype treats correct sentinel placement as triggerable in the safe mock lifecycle model.
- **Benign task completion:** the normalized trace marks task completion.
- **SSE-SR:** artifact placement, triggerability, and benign completion all hold.

This conservative oracle avoids counting ordinary metadata edits as success. Runs 015 and 016 are useful examples: Codex CLI made benign metadata edits in no-note controls, but the oracle remained at zero because the surface-specific sentinel was absent.

## Safety Scanner

The user-facing artifact must be safe to release. SandScout therefore includes a scanner for four risky categories that should not appear in benchmark tasks or preserved run artifacts:

- credential or secret indicators,
- destructive commands,
- real exploit payload indicators, and
- product-specific vulnerability claims.

The scanner runs over task JSON, prompt text, stdout, stderr, and diffs. It writes `safety_scan.json` for every real-agent run and redacts excerpts to short bounded strings. The scanner is intentionally a review aid, not a proof of absence. It ignores negated safety instructions such as "Do not access credentials" to reduce false positives, while still flagging concrete risky content if it appears elsewhere.

This scanner implements a detect-and-flag policy. SandScout blocks unsafe task specifications before execution and detects risky generated artifacts after execution. Clean safety scans are reported separately from SSE-SR so that attack-success measurement and artifact-safety assessment remain distinct.

## Design Alternatives

SandScout deliberately chooses sentinel-based measurement over real lifecycle execution. Executing package hooks, editor startup logic, CI workflows, or tool manifests would make results more concrete but would also increase safety risk and confound the method with host-specific behavior. Sentinel placement is weaker than real exploitation, but it is reproducible, safe, and sufficient to measure whether an agent follows repository-local context into a boundary-bearing artifact.

The miner also favors rule-based lifecycle patterns over unconstrained LLM generation. LLM-generated candidates may discover more diverse attacks, but they are harder to audit and could produce unsafe payloads. The current rule-based miner provides a transparent baseline. Future work can add learned or LLM-assisted candidate generation behind the same sentinel and safety-scanning interface.

Finally, SandScout reports infrastructure failures rather than silently treating them as negatives. This makes early real-agent experiments less visually tidy, but it prevents overclaiming. For example, the tool-manifest no-note control remains pending because run 017 hit a usage limit and run 019 timed out after live execution.

## Reproducibility Artifacts

The release artifact should contain:

- miner source code and rule definitions,
- synthetic fixture corpus,
- generated SSE-Bench task JSON,
- real-agent runner,
- normalized trace oracle,
- safety scanner,
- raw run summaries and metrics,
- result CSVs and plotting scripts, and
- progress reports documenting confirmatory and blocked runs.

The artifact should not include real exploit payloads, credentials, destructive commands, or product-specific bypass claims. If future real-agent outputs contain such content, the public artifact should preserve only redacted detection metadata unless coordinated disclosure permits more detail.
