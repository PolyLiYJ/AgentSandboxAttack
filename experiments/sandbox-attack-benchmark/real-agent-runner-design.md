# Real-Agent Runner Design

The real-agent runner is the next component after SandScout mining.

## Goals

- Run real coding agents on SandScout-generated sentinel tasks.
- Use disposable worktrees for every task.
- Capture enough evidence to evaluate SSE-SR without relying on hidden agent internals.

## Initial Target

Codex CLI is locally available. The first runner should support:

```bash
codex exec --cd <workspace> --sandbox workspace-write --ask-for-approval never <prompt>
```

The runner must provide only harmless sentinel prompts and should never ask the agent to exfiltrate secrets, execute malware, or modify host-level files.

## Evidence Collection

For each run, collect:

- prompt file
- stdout/stderr transcript
- pre/post git diff
- normalized trace JSON
- oracle metrics JSON

## Disposable Workspace Flow

1. Create temporary directory.
2. Copy or checkout target repository fixture.
3. Inject the SandScout task context.
4. Run the agent.
5. Convert diff/transcript to trace.
6. Evaluate with `sse_trace_oracle.py`.
7. Delete or archive the workspace depending on debug flag.

## Safety

The runner must reject task prompts containing:

- credential access requests
- network exfiltration requests
- destructive shell commands
- product-specific exploit payloads
- requests to disable security controls outside the disposable workspace
