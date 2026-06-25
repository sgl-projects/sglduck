"""Validate the pgs scales against the layer mappings."""

from __future__ import annotations

import polars as pl


def valid_scales(pgs: dict, dfs: list[pl.DataFrame]) -> None:
    """Run each scale's scale-specific validation."""
    if "scales" not in pgs:
        return
    for aes, scale in pgs["scales"].items():
        scale.valid_scale(aes, pgs["layers"], dfs)
