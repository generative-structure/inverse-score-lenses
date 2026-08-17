"""Figure 5 — family signatures. REAL.

Mean standardised composition feature per algorithm family, from the R-ID
substrate. Answers which worklist-composition coordinates characterise each
family. Built from persisted derived features; no decoder involved.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import pandas as pd

from p2style import FAMILY_COLOR, OKABE, require, save

SRC = "addendum/results/fig5_family_signatures.csv"
SHA = "dc05e546a10d96b63b3ab0676d95ce66f9ce5e5cd8fa220f544cf6c785cb100f"
ORDER = ["iforest", "lof", "knn", "ocsvm", "mcd", "autoencoder"]
NICE = {"iforest": "iForest", "lof": "LOF", "knn": "kNN", "ocsvm": "OCSVM",
        "mcd": "MCD", "autoencoder": "autoencoder"}


def main() -> None:
    d = pd.read_csv(require(SRC, SHA), index_col=0)
    fam = [f for f in ORDER if f in d.index]
    Z = d.loc[fam].to_numpy(dtype=float)
    # Abbreviations spelled out: "pct"/"dup"/"sd" were undefined in-figure.
    EXPAND = {"pct": "percentile", "dup": "duplicate", "sd": "s.d.",
              "vocab": "vocabulary", "psych": "psychological",
              "combo": "combination"}
    def _nice(c):
        t = c.replace("mix_", "").replace("struct_", "").replace("_", " ")
        return " ".join(EXPAND.get(w, w) for w in t.split())
    feats = [_nice(c) for c in d.columns]
    n_mix = sum(1 for c in d.columns if c.startswith("mix_"))

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    v = np.nanmax(np.abs(Z))
    im = ax.imshow(Z, cmap="RdBu_r", vmin=-v, vmax=v, aspect="auto")
    # GRAYSCALE SAFETY. A diverging map is the right choice for a signed
    # quantity, but it is not monotone in luminance: printed in black and
    # white, a strong positive and a strong negative both render as dark
    # grey and the sign is lost. Negative cells therefore also carry a
    # hatch, so sign is recoverable without colour. Purely an overlay --
    # no plotted value is altered.
    for r in range(Z.shape[0]):
        for c in range(Z.shape[1]):
            if np.isfinite(Z[r, c]) and Z[r, c] < 0:
                ax.add_patch(Rectangle(
                    (c - 0.5, r - 0.5), 1, 1, fill=False, hatch="////",
                    edgecolor="#FFFFFF", linewidth=0.0, alpha=0.55))
    ax.set_xticks(range(len(feats)))
    ax.set_xticklabels(feats, rotation=90, fontsize=6.8,
                       color="#000000")
    ax.set_yticks(range(len(fam)))
    ax.set_yticklabels([NICE[f] for f in fam], fontsize=8.4,
                       color="#000000")
    ax.axvline(n_mix - 0.5, color="#000000", lw=1.2)
    ax.text((n_mix - 1) / 2, -0.70, "autopsy mix", ha="center", va="bottom",
            fontsize=7.6, color="#000000")
    ax.text(n_mix + (len(feats) - n_mix - 1) / 2, -0.70, "structural",
            ha="center", va="bottom", fontsize=7.6, color="#000000")
    cb = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.015)
    cb.set_label("standard deviations from the battery mean",
                 fontsize=7.4)
    cb.ax.tick_params(labelsize=7)
    ax.set_title("mean composition of each algorithm family's selections, "
                 "real institutions;\nhatched cells are below the battery "
                 "mean", fontsize=8.6, pad=24)
    save(fig, "fig5_signatures")


if __name__ == "__main__":
    main()
