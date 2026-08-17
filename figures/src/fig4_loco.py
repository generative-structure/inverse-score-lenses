"""Figure 4 — leave-one-institution-out, per institution. REAL.

Built from the sealed addendum's persisted per-instance LOCO predictions
(section 0.5). Carries per-institution accuracy, the majority baseline, unit
counts, the pooled and macro figures, and the excess-over-null portability
index rho = (A_out - A0)/(A_in - A0).
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from p2style import OKABE, REP_HATCH, require, save

SRC = "addendum/results/fig4_loco_per_institution.csv"
SHA = "2cd875ef8402494e499b9f3753b55da20587ba29a8d58c2398c8f46ae1cf214b"
A_IN = {"autopsy_mix": 0.4491, "structural": 0.4337}   # section A, corrected
A0 = 1.0 / 27


def main() -> None:
    d = pd.read_csv(require(SRC, SHA))
    fig, ax = plt.subplots(figsize=(7.2, 3.15))
    reps = ["autopsy_mix", "structural"]
    order = (d[d.representation == "autopsy_mix"]
             .sort_values("rows", ascending=False).corpus.tolist())
    x = np.arange(len(order))
    w = 0.36
    for i, rep in enumerate(reps):
        sub = d[d.representation == rep].set_index("corpus").loc[order]
        col = OKABE["blue"] if i == 0 else OKABE["green"]
        # Hatch as well as hue, so the pair survives grayscale printing.
        ax.bar(x + (i - 0.5) * w, sub.accuracy, w, color=col,
               hatch=REP_HATCH[rep], edgecolor="white", linewidth=0.0,
               label=f"{rep.replace('_', ' ')}  "
                     f"(pooled {sub.pooled.iloc[0]:.3f}, "
                     f"macro {sub.macro.iloc[0]:.3f}, "
                     f"$\\rho$ {(sub.macro.iloc[0]-A0)/(A_IN[rep]-A0):.3f})")
        ax.axhline(sub.pooled.iloc[0], color=col, lw=0.9, ls=(0, (1, 1.5)))
        ax.axhline(sub.macro.iloc[0], color=col, lw=0.9, ls=(0, (5, 2)))
    base = d[d.representation == "autopsy_mix"].set_index("corpus").loc[order]
    ax.plot(x, base.majority, marker="_", ls="none", ms=11,
            color=OKABE["grey"], mew=1.4)
    ax.axhline(A0, color="#000000", lw=0.7, ls=(0, (3, 2)))
    # Left edge: the right-hand end sat on top of the last pair of bars.
    ax.text(-0.55, A0 + 0.010, "chance $=1/27$", ha="left",
            fontsize=7.2, color="#000000")
    ax.set_xticks(x)
    # "u" was an undefined abbreviation; the axis label now names the count.
    ax.set_xticklabels([f"{c}\n{int(base.loc[c,'units'])}" for c in order],
                       fontsize=7.2)
    ax.set_xlabel("institution, and the number of analysis units it "
                  "contributes", fontsize=8.2)
    ax.set_ylabel("held-out attribution accuracy", fontsize=8.2)
    ax.set_ylim(0, 0.56)
    ax.set_xlim(-0.7, len(order) - 0.3)
    ax.set_title("leave-one-institution-out, ordered by instance mass; "
                 "dotted = pooled, dashed = macro", fontsize=8.4)
    h, l = ax.get_legend_handles_labels()
    h += [Line2D([], [], color=OKABE["grey"], marker="_", ls="none", mew=1.4,
                 label="per-institution majority baseline")]
    ax.legend(handles=h, frameon=False, fontsize=7.2, loc="upper right", ncol=1)
    save(fig, "fig4_loco")


if __name__ == "__main__":
    main()
