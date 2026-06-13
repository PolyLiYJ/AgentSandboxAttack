# Protocol: run_018 Safety Scanner Smoke Test

## Status

OFFLINE INFRASTRUCTURE CHECK.

## Hypothesis

SandScout should not merely exclude unsafe categories from generated benchmark content. It should also detect and label real exploit payload indicators, credential/secret indicators, destructive commands, and product-specific vulnerability claims if they appear in task specifications or real-agent artifacts.

## Procedure

Run the safety scanner on:

- A benign safety-instruction string containing negated safety constraints.
- A synthetic risky string containing one example from each target category.
- Existing run artifacts from a completed no-note control.

Do not store risky raw strings in committed artifacts. Record only category-level summary.

## Expected Outcome

- Benign safety-instruction string: clean.
- Synthetic risky string: four target categories detected.
- Existing safe run artifacts: clean.

## Safety

This is an offline scanner validation. It does not run a real agent and does not execute any scanned content.

