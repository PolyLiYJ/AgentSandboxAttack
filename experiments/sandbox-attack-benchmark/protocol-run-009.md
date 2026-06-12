# Protocol: H1 Run 009 Offline Ranking and Ablation Plan

## Hypothesis

SandScout confidence scores can prioritize mined tasks for real-agent evaluation and avoid spending limited agent budget on low-signal README-only candidates.

## Motivation

Run 008 hit a Codex CLI usage limit before task execution. Until live agent budget resets, progress should focus on offline ranking and ablation design.

## Method

Use `run_007_mining_corpus.json` to derive:

- high-confidence candidate queue
- surface-balanced evaluation queue
- README-only low-confidence controls
- ablation sets with and without `SANDSCOUT_NOTE.md`

## Planned Metrics

- Mining Yield: total mined candidates per repository.
- High-Confidence Yield: candidates with confidence >= 0.75.
- Surface Balance: number of surface classes covered by top-k.
- Agent Budget Efficiency: successful completed agent runs per attempted live run.

## Prediction

Ranking by confidence should select package lifecycle, tool manifest, startup, CI, and AGENTS.md candidates before README-only candidates. This should improve agent-budget efficiency in later live runs.

## Safety Boundary

No real agents are executed in this protocol. It only analyzes existing safe sentinel task metadata.
