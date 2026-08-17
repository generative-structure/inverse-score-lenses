"""Figure 3 — decoder-achieved recoverable information.

Left: I-hat(S;F) and I-hat(plant;F) in bits, with the sealed bootstrap
intervals (S-ID resamples POPULATIONS), both headlined representations,
random forest primary. A reserved empty group carries the pending key for
the conditional quantities.

Right: the GOVERNING certificate. Fano lower bounds per representation
against the two plant-prior ceilings — the sealed prior and the balanced
variant — so the design-conditionality is visible and the one cell that
fails to clear a balanced prior is legible on the figure. The normalized
ratio panel is gone: the certificate is a dominance result, not a ratio,
and drawing a committed ratio floor invited exactly the reading the paper
now disclaims.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from p2style import (OKABE, PENDING_EDGE, PENDING_FACE, REP_HATCH,
                     require, save)

S = "results/sid/20260726T172824Z_c093730/"
SRC = {
    S + "task_A.csv":
        "18ef7747b08c56865e5a2e5ec292b11b2addd0c5a77ca4f280d88a198074c8a4",
    S + "task_B1.csv":
        "ce3ee1fce536ea30fbfaa412f85e21986689252ad9ce6a1d3d6cc0a7cdb6189f",
    S + "P3.csv":
        "c3a20163d9999a4c1ce4ee49ec5ada758b466285847c9206d57a35c6a21be000",
    "addendum/results/certificate_rederived.csv":
        "16cce8ac210b59fb7cc900e2322a456e0e8ccae854a23f0840b73493a81312cb",
}
import math
ANY_PRIOR = math.log2(6)   # ceiling for ANY six-class prior; analytic
REPS = [("autopsy_mix", "autopsy mix"), ("structural", "structural")]


def ci(s: str) -> tuple[float, float]:
    lo, hi = str(s).strip("[]").split(",")
    return float(lo), float(hi)


def main() -> None:
    paths = {k: require(k, v) for k, v in SRC.items()}
    A = pd.read_csv(paths[S + "task_A.csv"])
    B1 = pd.read_csv(paths[S + "task_B1.csv"])
    P3 = pd.read_csv(paths[S + "P3.csv"]).set_index("representation")

    fig, (ax, ax2) = plt.subplots(
        1, 2, figsize=(7.0, 2.85), gridspec_kw={"width_ratios": [1.28, 0.72]})

    groups = ["specification $S$", "planted mechanism"]
    xs = np.arange(len(groups))
    width = 0.34

    for j, (rep, lab) in enumerate(REPS):
        off = (j - 0.5) * width
        a = A[(A.representation == rep) & (A.model == "random_forest")].iloc[0]
        b = B1[(B1.representation == rep)
               & (B1.model == "random_forest")].iloc[0]
        vals = [a.I_bits, b.I_plant_bits]
        cis = [ci(a.CI), ci(b.CI)]
        err = np.array([[v - c[0] for v, c in zip(vals, cis)],
                        [c[1] - v for v, c in zip(vals, cis)]])
        colour = OKABE["blue"] if j == 0 else OKABE["green"]
        # Hatch as well as hue: the two representations must stay
        # distinguishable in a grayscale printing.
        ax.bar(xs[:2] + off, vals, width, label=lab, color=colour,
               hatch=REP_HATCH[rep], edgecolor="white", linewidth=0.0)
        ax.errorbar(xs[:2] + off, vals, yerr=err, fmt="none",
                    ecolor="#222222", elinewidth=0.8, capsize=2.2)

    ax.set_xticks(xs)
    ax.set_xticklabels(groups)
    ax.set_ylabel(r"$\hat{I}(\cdot\,;F)$  (bits)")
    ax.set_title("(a) decoder-achieved recoverable information, S-ID\n"
                 "intervals resample populations; bits only",
                 fontsize=7.6)
    ax.legend(frameon=False, loc="upper right")
    ax.set_ylim(0, 4.6)

    C = pd.read_csv(paths["addendum/results/certificate_rederived.csv"])
    C = C[C.M == 22].set_index("representation")
    reps = [r for r, _ in REPS]
    fano = [float(C.loc[r, "fano_emp"]) for r in reps]
    h_sealed = float(C.iloc[0]["h_plant"])
    x2 = np.arange(len(reps))

    bars = ax2.bar(x2, fano, 0.46,
                   color=[OKABE["blue"], OKABE["green"]],
                   hatch=[REP_HATCH[r] for r in reps],
                   edgecolor="white", linewidth=0.0,
                   label=r"Fano lower bound on $\hat{I}(S;F)$")
    # The two ceilings are labelled on the lines themselves rather than in a
    # legend: a legend box has nowhere to sit here without covering a bar,
    # and solid-vs-dashed already separates them without colour.
    ax2.axhline(h_sealed, color="#000000", linewidth=1.1, linestyle="-")
    ax2.axhline(ANY_PRIOR, color="#000000", linewidth=1.1,
                linestyle=(0, (3, 1.6)))
    top = max(max(fano), ANY_PRIOR) * 1.58
    ax2.set_ylim(0, top)
    # Ceiling labels go in the right-hand margin, clear of both bars; the
    # numeric values are in the caption and in Table 3, so only the short
    # names are needed here.
    ax2.set_xlim(-0.42, len(reps) - 0.22)
    for y, name in ((h_sealed, "design"), (ANY_PRIOR, "any-prior")):
        ax2.text(len(reps) - 0.25, y, f"{name}\nceiling",
                 ha="right", va="center", fontsize=5.6, color="#000000",
                 linespacing=1.15,
                 bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
    for i, r in enumerate(reps):
        d = fano[i] - ANY_PRIOR
        tag = "below" if d < 0 else "above"
        ax2.text(i, fano[i] + 0.07,
                 f"{d:+.2f} bits\n{tag} the\nany-prior ceiling",
                 ha="center", va="bottom", fontsize=6.0, weight="bold",
                 color="#000000", linespacing=1.2)
    ax2.set_xticks(x2)
    ax2.set_xticklabels([l for _, l in REPS], fontsize=7)
    ax2.set_ylabel("bits")
    ax2.set_title("(b) the governing certificate, $M=22$\n"
                  "bars are Fano lower bounds on $\\hat{I}(S;F)$",
                  fontsize=7.6)

    save(fig, "fig3_information")


if __name__ == "__main__":
    main()
