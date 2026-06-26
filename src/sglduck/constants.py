"""Aesthetic and qualifier name constants."""

from __future__ import annotations

CART_AES = ("x", "y")
POLAR_AES = ("theta", "r")
POS_AES = (*CART_AES, *POLAR_AES)
NON_POS_AES = ("color", "size")
ALL_AES = (*POS_AES, *NON_POS_AES)

ALL_QUALS = ("jittered", "regression", "unstacked")

# theta/r positional aesthetics fold onto the Cartesian x/y axes.
POLAR_TO_CART_AES = {"theta": "x", "r": "y"}

# The constant column an unmapped positional aesthetic is pinned to: lets-plot
# has no constant-aesthetic literal, so a blank axis becomes a one-value column.
BLANK_AES_COLUMN = "sglduck.blank"
