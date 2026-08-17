"""Path resolution and input pinning.

Every path in this package is relative to this file. Pinned inputs are read
from inputs/; generated output is written beside it under the package root.

require() is the only way an input is read. A missing file and an altered
file are reported differently, because they mean different things: the first
is an incomplete checkout, the second means an input no longer matches the
digest the results were produced from.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT / "inputs"


def require(rel: str, sha256: str) -> Path:
    """Return a pinned input, or abort naming it."""
    path = REPO / rel
    if not path.exists():
        raise SystemExit(
            f"pinned input MISSING: {rel}\n"
            f"  looked in : inputs/\n"
            f"  Every reported statistic must trace to a pinned input. "
            f"Refusing to build.")
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != sha256:
        raise SystemExit(
            f"pinned input CHANGED: {rel}\n"
            f"  expected : {sha256}\n"
            f"  found    : {got}\n"
            f"  Refusing to build until the pin is reviewed and updated "
            f"deliberately.")
    return path
