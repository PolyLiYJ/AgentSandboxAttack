# Protocol: H1 Run 003 Automated Mining and Real-Agent Evaluation

## Hypothesis

An automated repository miner can discover semantic sandbox boundary candidates and generate safe sentinel tasks that produce measurable differences across real coding agents.

## Method

Run **SandScout**, a conservative static miner, over target repositories. SandScout scans files whose semantics often cross from the sandboxed workspace into a later host, editor, CI, package, tool, or instruction lifecycle. It emits sentinel tasks rather than exploit payloads.

Pipeline:

1. Mine candidate boundary surfaces from a repository.
2. Generate a disposable worktree per task.
3. Insert benign user goal plus adversarial repository context.
4. Run a real agent in a sandboxed or disposable environment.
5. Convert transcript and diff to trace records.
6. Evaluate traces with `src/sse_trace_oracle.py`.

## Real Agents

Initial matrix:

- Codex CLI: locally detected, first executable target.
- Claude Code: planned, requires local install/auth.
- Gemini CLI: planned, requires local install/auth.
- OpenHands: planned open-source agent baseline.

## Safety Boundary

All generated tasks use `SSE_BENIGN_SENTINEL`. No task contains malware, credential access, destructive shell commands, or real product exploit payloads. Real-agent runs must occur in disposable worktrees.

## Prediction

SandScout will find at least one boundary candidate in typical agent/software repositories. Real-agent attack success will vary more by agent interface and policy than by task surface alone.
