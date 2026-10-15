#!/bin/sh
# Rebuild the paper PDF from paper/paper.md (requires pandoc + XeLaTeX with TeX Gyre Pagella).
# Run analysis.py first so that output/ holds the figures the paper includes.
cd "$(dirname "$0")/paper" && pandoc paper.md -o paper.pdf --pdf-engine=xelatex \
  --from markdown-implicit_figures -H header.tex \
  -V mainfont="TeX Gyre Pagella" -V monofont="DejaVu Sans Mono" -V fontsize=10pt \
  -V geometry:a4paper,margin=2cm -V colorlinks=true -V linkcolor=blue -V urlcolor=blue \
  && cp paper.pdf ../Track9_Protection_Gap_Paper.pdf
