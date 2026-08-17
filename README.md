# Replication package

Regenerates every statistic and every figure reported in the manuscript from
the stored analysis outputs.

## Requirements

Python 3.11 or later, with `numpy`, `pandas`, `pyyaml` and `matplotlib`.

## Run

    make

Equivalently, `python3 ops/make_p2_macros.py` followed by each script in
`figures/src/`.

## Output

- `results_macros.tex` — one macro per reported statistic. Every number in the
  manuscript is one of these; none is typed by hand.
- `figures/fig1_design.pdf` … `figures/fig5_signatures.pdf`

## Contents

- `ops/make_p2_macros.py` — derives every reported statistic from the pinned
  inputs and writes `results_macros.tex`.
- `figures/src/` — one script per figure, plus the shared style module.
- `paths.py` — path resolution and the SHA-256 pin check.
- `inputs/` — the stored analysis outputs the above read, unmodified.

## Integrity

Every input carries an asserted SHA-256 at its point of use. The build reads
nothing that is not pinned, and aborts naming the file if an input is missing
or its digest does not match. A number that cannot be traced to a pinned input
does not reach the output.

One redaction: a metadata comment field in `inputs/config/frozen_corpora.yaml`
has been removed. It is read by nothing in this package and affects no
reported value; the pin for that file records the redacted digest.

## Scope

This package reproduces the reported statistics and figures from the stored
analysis outputs. It does not re-execute the upstream studies that produced
those outputs: the real-institution substrate derives from public payment
registers whose raw extracts are not redistributable.
