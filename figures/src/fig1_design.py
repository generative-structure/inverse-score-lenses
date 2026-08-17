"""Figure 1 — what the study observes and what it recovers. No data.

LAYOUT CONTRACT. Every length below is in inches on the canvas, so a length
here is a length on the page up to the \\includegraphics scale factor.

  * A row is as tall as the TALLER of its box and its text block, and the
    gap between rows is fixed. Row height set by box height alone is what
    let the long text blocks overrun the rows beneath them.
  * The canvas height follows from the rows. The rows are not packed into
    a canvas fixed in advance.
  * The box column is wide enough for the widest stage label, and the text
    column is narrow enough to leave the right margin clear.
  * The decoder is a side input, so it sits below the flow on its own row
    and feeds the last stage from underneath.

Text blocks are two lines each; the caption carries the full account, so
the in-figure text names each stage and its counts and stops there. Type
sizes are those of the legibility pass. The assertions in check() measure
the rendered result and are what keep the contract honest if either the
text or the sizes change.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from p2style import OKABE, save

# CANVAS WIDTH IS THE TYPE-SIZE CONTROL. savefig crops to content and
# \includegraphics scales the result to \linewidth (6.5in), so on-page type
# size is fontsize * 6.5 / canvas width. W is pinned to the width the
# legibility pass produced, which puts the 7.6pt body text on the page at
# 8.79pt exactly as before. Changing W changes every type size in the
# figure; nothing else here does.
W = 5.62
PAD = 0.06          # canvas margin
BOX_X, BOX_W = 0.06, 1.44
TEXT_X = 1.62
ROW_GAP = 0.17      # fixed gap between rows; the arrows live inside it
BOX_H = 0.42
DEC_GAP, DEC_H, DEC_W = 0.28, 0.42, 5.50

FS_STAGE, FS_SYM, FS_TEXT = 8.6, 8.2, 7.6
FS_DEC_TITLE, FS_DEC_BODY = 7.8, 6.8
LINESPACING = 1.35
BOX_INNER_PAD = 0.10

# (stage, symbol, two lines -- every count named where it appears)
ROWS = [
    ("Population", "$X$",
     ["the records a procedure was run on:",
      "12 government payment registers, 1,200 synthetic populations"],
     OKABE["grey"]),
    ("Specification", "$s$",
     ["one configured procedure: algorithm, features, preprocessing",
      "27 specifications in the battery, in 6 algorithm families"],
     OKABE["blue"]),
    ("Worklist", "$W_{s,k}(X)$",
     ["the records that procedure selected:",
      "50 records, in rank order"],
     OKABE["green"]),
    ("Representation", r"$\varphi(W;X)$",
     ["the selection as a vector, read against its population:",
      "category: 15 composition shares; structural: 7 position statistics"],
     OKABE["orange"]),
    ("Recovered", "$Y$",
     ["the label a decoder predicts: which specification of the 27,",
      "which of the 6 families, which planted mechanism, which population"],
     OKABE["vermil"]),
]

DEC_TITLE = "the decoder"
DEC_BODY = ("fitted on labelled worklists from other populations, under "
            "population-grouped folds")


def line_height(fontsize: float) -> float:
    """Height of one rendered line, in inches. Matches how matplotlib
    spaces a multi-line Text, so a block's height is known before it is
    drawn and a row can be sized to it."""
    return fontsize * LINESPACING / 72.0


def main() -> None:
    # Row heights first: the taller of the box and the text block.
    text_h = [len(lines) * line_height(FS_TEXT) for _, _, lines, _ in ROWS]
    row_h = [max(BOX_H, th) for th in text_h]
    flow_h = sum(row_h) + ROW_GAP * (len(ROWS) - 1)
    H = PAD + flow_h + DEC_GAP + DEC_H + PAD

    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    handles = []
    y = H - PAD                       # top edge of the current row
    for i, (stage, sym, lines, colour) in enumerate(ROWS):
        yc = y - row_h[i] / 2         # row centre
        ax.add_patch(FancyBboxPatch(
            (BOX_X, yc - BOX_H / 2), BOX_W, BOX_H,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            linewidth=1.1, edgecolor=colour, facecolor=colour + "20"))
        label = ax.text(BOX_X + BOX_W / 2, yc + 0.075, stage,
                        ha="center", va="center", fontsize=FS_STAGE,
                        weight="bold", color="#000000")
        ax.text(BOX_X + BOX_W / 2, yc - 0.095, sym, ha="center", va="center",
                fontsize=FS_SYM, color="#000000")
        block = ax.text(TEXT_X, yc, "\n".join(lines), ha="left", va="center",
                        fontsize=FS_TEXT, color="#000000",
                        linespacing=LINESPACING)
        handles.append((stage, label, block, yc))

        if i < len(ROWS) - 1:
            yc_next = y - row_h[i] - ROW_GAP - row_h[i + 1] / 2
            ax.add_patch(FancyArrowPatch(
                (BOX_X + BOX_W / 2, yc - BOX_H / 2 - 0.015),
                (BOX_X + BOX_W / 2, yc_next + BOX_H / 2 + 0.015),
                arrowstyle="-|>", mutation_scale=9, linewidth=1.0,
                color="#000000", shrinkA=0, shrinkB=0))
        y -= row_h[i] + ROW_GAP

    # The decoder is a side input, not a further stage: its own row below
    # the flow, dashed, feeding the last stage from underneath.
    last_yc = handles[-1][3]
    dec_top = last_yc - BOX_H / 2 - DEC_GAP
    ax.add_patch(FancyBboxPatch(
        (BOX_X, dec_top - DEC_H), DEC_W, DEC_H,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=1.0, edgecolor="#555555", facecolor="#F2F2F2",
        linestyle=(0, (4, 2))))
    dec_title = ax.text(BOX_X + BOX_INNER_PAD, dec_top - DEC_H / 2 + 0.075,
                        DEC_TITLE, ha="left", va="center",
                        fontsize=FS_DEC_TITLE, weight="bold", color="#000000")
    dec_body = ax.text(BOX_X + BOX_INNER_PAD, dec_top - DEC_H / 2 - 0.080,
                       DEC_BODY, ha="left", va="center",
                       fontsize=FS_DEC_BODY, color="#333333")
    ax.add_patch(FancyArrowPatch(
        (BOX_X + BOX_W / 2, dec_top + 0.015),
        (BOX_X + BOX_W / 2, last_yc - BOX_H / 2 - 0.015),
        arrowstyle="-|>", mutation_scale=9, linewidth=1.0,
        color="#555555", linestyle=(0, (4, 2)), shrinkA=0, shrinkB=0))

    check(fig, ax, handles, row_h, dec_title, dec_body)
    save(fig, "fig1_design")


def check(fig, ax, handles, row_h, dec_title, dec_body) -> None:
    """Measure what was drawn and refuse to write a broken layout."""
    fig.canvas.draw()
    inv = ax.transData.inverted()

    def extent(t):
        bb = t.get_window_extent(fig.canvas.get_renderer())
        (x0, y0), (x1, y1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        return x0, y0, x1, y1

    inner = BOX_W - 2 * BOX_INNER_PAD
    for (stage, label, block, yc), rh in zip(handles, row_h):
        lx0, _, lx1, _ = extent(label)
        assert lx1 - lx0 <= inner, (
            f"{stage!r}: label is {lx1 - lx0:.3f}in wide, box holds "
            f"{inner:.3f}in -- widen BOX_W or shorten the label")
        bx0, by0, bx1, by1 = extent(block)
        assert by1 - by0 <= rh + 1e-6, (
            f"{stage!r}: text block is {by1 - by0:.3f}in tall, row is "
            f"{rh:.3f}in -- the block would overrun the row below")
        assert bx1 <= W - PAD + 1e-6, (
            f"{stage!r}: text reaches {bx1:.3f}in on a {W}in canvas")
        assert bx0 >= BOX_X + BOX_W, f"{stage!r}: text overlaps the box column"

    for t, name in ((dec_title, "decoder title"), (dec_body, "decoder note")):
        x0, _, x1, _ = extent(t)
        assert x1 <= BOX_X + DEC_W - BOX_INNER_PAD + 1e-6, (
            f"{name} is {x1 - x0:.3f}in wide and crosses its border")


if __name__ == "__main__":
    main()
