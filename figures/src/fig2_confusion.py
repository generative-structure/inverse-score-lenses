"""Figure 2 — confusion structure.

(a) S-ID exact-specification confusion, RESTRICTED to the 22 learned cells,
    row-normalised, family-blocked so family structure is visible. Built from
    the sealed task_E_confusion.csv (26 non-ensemble cells) by dropping the
    four rule-based cells. The restriction is stated in the caption.
(b) R-ID family confusion — NOT stored in results/rid/ (verified: the run
    directory holds aggregate CSVs only, no confusion matrix). Stubbed.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

from p2style import FAMILY_COLOR, OKABE, REPO, pending_panel, require, save

CONF = "results/sid/20260726T172824Z_c093730/task_E_confusion.csv"
CONF_SHA = "07f70149d9ec9453f9082788794f54d762ac181391c8da9f89c08305ffe89d61"
FROZEN = "config/frozen_config.yaml"
FROZEN_SHA = "29346d171ba7df6547d3c87bae3e99419e62049a555aed4e25787d993ab67050"

FAMILY_ORDER = ["iforest", "lof", "knn", "ocsvm", "mcd", "autoencoder"]
SHORT = {"iforest": "iF", "lof": "LOF", "knn": "kNN", "ocsvm": "OCSVM",
         "mcd": "MCD", "autoencoder": "AE"}
# The preprocessing path must appear: three iForest cells share a feature
# set and differ only in path, so a features-only label collides.
FEAT = {"full": "full", "full_categorical": "fullcat",
        "amount_only": "amt", "amount_cents": "cents"}
PATH = {"robust": "rob", "log": "log", "raw": "raw"}


def label(name: str, alg: dict) -> str:
    _, feats, prep = name.split("__")
    return f"{SHORT[alg[name]]}·{FEAT[feats]}·{PATH[prep]}"


def learned_order(frozen) -> tuple[list[str], dict[str, str]]:
    cells = frozen["grid"]["cells"]
    alg = {c["name"]: c["algorithm"] for c in cells}
    rule = {"benford", "round_flag", "repeat", "dup_pair"}
    learned = [c["name"] for c in cells if c["algorithm"] not in rule]
    learned.sort(key=lambda n: (FAMILY_ORDER.index(alg[n]), n))
    return learned, alg


# Spelled out in-figure and in the caption. Phase 7: no abbreviation may
# appear in a figure without its expansion somewhere the reader can see.
ALG_LONG = {"iF": "isolation forest", "LOF": "local outlier factor",
            "kNN": "k-nearest-neighbour distance",
            "OCSVM": "one-class SVM",
            "MCD": "minimum covariance determinant",
            "AE": "autoencoder"}
FEAT_LONG = {"amt": "amount only", "cents": "amount and cents residue",
             "full": "amount, cents, vendor frequency, day",
             "fullcat": "full plus one-hot vendor"}
PATH_LONG = {"rob": "robust-scaled", "log": "log-transformed", "raw": "raw"}


def main() -> None:
    cm = pd.read_csv(require(CONF, CONF_SHA), index_col=0)
    frozen = yaml.safe_load(require(FROZEN, FROZEN_SHA).read_text())
    order, alg = learned_order(frozen)
    assert len(order) == 22, f"expected 22 learned cells, got {len(order)}"

    M = cm.reindex(index=order, columns=order).to_numpy(dtype=float)
    row = M.sum(axis=1, keepdims=True)
    R = np.divide(M, np.where(row == 0, 1, row))

    # PHASE 7 LAYOUT. The panels were side by side and the 22-class matrix
    # was compressed to 4.6 pt tick labels -- unreadable on paper. Stacking
    # them gives panel (a) the full text width, so its labels can be set at a
    # size a reader can actually use. Tick labels are BLACK: family identity
    # was carried by hue, which put gold-on-white in the middle of the axis
    # and encoded a variable in a channel that fails in grayscale and for
    # colourblind readers. The family blocks are now shown by rules and by
    # bracketed group labels instead.
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 9.0),
                             gridspec_kw={"height_ratios": [1.62, 0.90],
                                          "hspace": 0.62})

    ax = axes[0]
    im = ax.imshow(R, cmap="Greys", vmin=0, vmax=1, interpolation="nearest")
    ax.set_xticks(range(22))
    ax.set_yticks(range(22))
    labels = [label(n, alg) for n in order]
    assert len(set(labels)) == len(labels), "tick labels must be unique"
    ax.set_xticklabels(labels, rotation=90, fontsize=7.4, color="#000000")
    ax.set_yticklabels(labels, fontsize=7.4, color="#000000")
    ax.tick_params(length=2, width=0.5)

    # family block boundaries and bracketed group labels
    bounds, seen, starts = [], None, []
    for i, n in enumerate(order):
        if alg[n] != seen:
            starts.append((i, alg[n]))
            if seen is not None:
                bounds.append(i)
            seen = alg[n]
    for b in bounds:
        ax.axhline(b - 0.5, color="#000000", linewidth=0.9)
        ax.axvline(b - 0.5, color="#000000", linewidth=0.9)
    # No separate family bracket: every tick label already begins with its
    # family, so a bracket would repeat it and collide with the labels. The
    # black rules alone mark the blocks.

    ax.set_xlabel("predicted specification", fontsize=8.5)
    ax.set_ylabel("true specification", fontsize=8.5)
    ax.set_title("(a) synthetic study: 22 learned specifications, "
                 "rows normalised to sum to one", fontsize=9)
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label("share of the true class's instances", fontsize=7.5)
    cb.ax.tick_params(labelsize=7)

    ax2 = axes[1]
    F = pd.read_csv(require(
        "addendum/results/fig2b_family_confusion.csv",
        "1a1996d2c4382ffd97e04a82fe329e1660448f98eaaed999af5fa23f324b7517"),
        index_col=0)
    fam = [f for f in FAMILY_ORDER if f in F.index]
    Mf = F.reindex(index=fam, columns=fam).to_numpy(dtype=float)
    Rf = Mf / np.where(Mf.sum(1, keepdims=True) == 0, 1, Mf.sum(1, keepdims=True))
    im2 = ax2.imshow(Rf, cmap="Greys", vmin=0, vmax=1, interpolation="nearest")
    ax2.set_xticks(range(len(fam))); ax2.set_yticks(range(len(fam)))
    # Panel (b) names each family in full: six labels have room for words.
    lab = [f"{SHORT.get(f, f)} — {ALG_LONG[SHORT[f]]}" for f in fam]
    # 30-degree rotation: at six upright labels OCSVM touched its
    # neighbours; rotating separates them at the same type size.
    ax2.set_xticklabels([SHORT.get(f, f) for f in fam], rotation=30,
                        ha="right", fontsize=8.5, color="#000000")
    ax2.set_yticklabels(lab, fontsize=8.5, color="#000000")
    ax2.tick_params(length=2, width=0.5)
    for i in range(len(fam)):
        for j in range(len(fam)):
            if Rf[i, j] >= 0.02:
                ax2.text(j, i, f"{Rf[i,j]:.2f}", ha="center", va="center",
                         fontsize=8.0,
                         color="white" if Rf[i, j] > 0.5 else "#000000")
    ax2.set_xlabel("predicted family", fontsize=8.5)
    ax2.set_ylabel("true family", fontsize=8.5)
    ax2.set_title("(b) real-institution study: six algorithm families, "
                  "corrected grouping", fontsize=9)
    cb2 = fig.colorbar(im2, ax=ax2, fraction=0.045, pad=0.02)
    cb2.set_label("share of the true class's instances", fontsize=7.5)
    cb2.ax.tick_params(labelsize=7)

    # Expansion key for the compact cell labels of panel (a).
    lines = [
        "Panel (a) cell label = algorithm \u00b7 feature set \u00b7 preprocessing.",
        "Feature sets: " + ";  ".join(f"{k} = {v}" for k, v in
                                      FEAT_LONG.items()) + ".",
        "Preprocessing: " + ";  ".join(f"{k} = {v}" for k, v in
                                       PATH_LONG.items()) + ".",
    ]
    for n, line in enumerate(lines):
        fig.text(0.5, 0.028 - 0.011 * n, line, ha="center", va="top",
                 fontsize=7.0, color="#000000")

    save(fig, "fig2_confusion")


if __name__ == "__main__":
    main()
