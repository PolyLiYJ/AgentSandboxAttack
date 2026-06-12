# Protocol: H1 Run 007 Synthetic Corpus Mining Yield

## Hypothesis

SandScout should discover distinct semantic sandbox boundary candidates across a small repository corpus, not only in the current project repository.

## Method

Create a safe synthetic corpus with repositories representing common lifecycle surfaces:

- package lifecycle configuration
- startup/editor configuration
- tool manifest discovery
- CI workflow transition
- instruction hierarchy
- low-signal documentation control

Run `sandscout_miner.py` through `run_mining_corpus.py` and record mining yield by repository and surface.

## Prediction

The miner should find at least five unique surface classes across six repositories. The low-signal documentation control may still produce an instruction-hierarchy candidate because README files are model-visible project instructions; this should be recorded as an intentional broad recall choice rather than a false positive.

## Safety Boundary

All fixtures are synthetic and contain no executable payloads beyond harmless placeholder metadata. No agent is run in this protocol.
