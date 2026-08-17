"""Shared deterministic style for Paper 2 figures.

One font, one colourblind-safe palette (Okabe-Ito), vector PDF output.
Every figure script asserts the SHA-256 of each data input it reads; a
figure that cannot trace its numbers to a pinned sealed output does not
get built.
"""
from __future__ import annotations
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from paths import PROJECT, REPO, require   # noqa: E402,F401

OUT = PROJECT / "figures"

# Okabe-Ito, colourblind-safe
OKABE = {
    "black":   "#000000",
    "orange":  "#E69F00",
    "skyblue": "#56B4E9",
    "green":   "#009E73",
    "yellow":  "#F0E442",
    "blue":    "#0072B2",
    "vermil":  "#D55E00",
    "purple":  "#CC79A7",
    "grey":    "#999999",
}
FAMILY_COLOR = {
    "iforest": OKABE["blue"], "lof": OKABE["orange"], "knn": OKABE["green"],
    "ocsvm": OKABE["vermil"], "mcd": OKABE["purple"],
    "autoencoder": OKABE["skyblue"],
}
PENDING_FACE = "#EDEDED"
PENDING_EDGE = OKABE["grey"]

# GRAYSCALE SAFETY. The two headlined representations are contrasted in
# most figures, and Okabe blue (#0072B2) and green (#009E73) are close in
# luminance -- they collapse to nearly the same grey when a reader prints
# the article in black and white. Hue is therefore never the only channel:
# every paired bar also carries a distinct hatch, and every reference line
# a distinct dash pattern. Added 2026-08-07 for the JAIR submission; no
# data path, no input artifact and no plotted value is touched.
REP_HATCH = {"autopsy_mix": "", "structural": "///"}
REP_COLOR = {"autopsy_mix": OKABE["blue"], "structural": OKABE["green"]}

matplotlib.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8.5,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6,
    "ytick.major.width": 0.6, "axes.spines.top": False,
    "axes.spines.right": False, "figure.dpi": 200,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})


def pending_panel(ax, key: str, note: str = "") -> None:
    """Render a grey stub carrying its \\pending key, so the figure
    environment, caption and label are real while the data is not."""
    ax.set_facecolor(PENDING_FACE)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color(PENDING_EDGE)
        s.set_linestyle((0, (4, 3)))
    txt = f"[[{key}]]"
    nkey = txt.count("\n") + 1
    ax.text(0.5, 0.62, txt, ha="center", va="center", fontsize=8.5,
            color=OKABE["vermil"], family="monospace", weight="bold",
            linespacing=1.5, transform=ax.transAxes)
    if note:
        ax.text(0.5, 0.62 - 0.075 * nkey - 0.075, note, ha="center",
                va="top", fontsize=6.8, color="#555555", linespacing=1.6,
                transform=ax.transAxes)


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"wrote {path.relative_to(PROJECT)}")
