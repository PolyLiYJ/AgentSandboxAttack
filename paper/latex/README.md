# SandScout NDSS LaTeX Draft

This directory contains a working NDSS 2026-style LaTeX draft.

- `bare_conf_NDSS2026.tex` and `IEEEtran.cls` are the official downloaded template files.
- `sandscout_ndss2026.tex` is the SandScout paper draft using the template style.
- `sections/` contains the paper body.
- `references.bib` contains DOI-fetched arXiv BibTeX entries with stable project keys.

Build:

```bash
cd /Users/liyanjie/Documents/AgentSandBoxResearch/paper/latex
latexmk -pdf sandscout_ndss2026.tex
```

Clean:

```bash
latexmk -C sandscout_ndss2026.tex
```

Notes:

- Author names and affiliations are placeholders.
- The DOI in the NDSS copyright block is still the official template placeholder.
- The draft uses only verified academic references from `literature/verified_sources.md`.
- Industry motivation sources are intentionally not cited until their metadata is verified.
