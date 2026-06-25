"""Aesthetic and qualifier name constants."""

from __future__ import annotations

CART_AES = ("x", "y")
POLAR_AES = ("theta", "r")
POS_AES = (*CART_AES, *POLAR_AES)
NON_POS_AES = ("color", "size")
ALL_AES = (*POS_AES, *NON_POS_AES)

ALL_QUALS = ("jittered", "regression", "unstacked")
