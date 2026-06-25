"""Validate the CTAs in a layer's column expressions."""

from __future__ import annotations

import polars as pl


def valid_col_expr_ctas(col_exprs, df: pl.DataFrame) -> None:
    """Run each col_expr's cta-specific validation."""
    for col_expr in col_exprs:
        col_expr["cta"].valid_cta(col_expr, df)


def valid_ctas(layer: dict, df: pl.DataFrame) -> None:
    """Raise if any clause of the layer applies a CTA invalidly."""
    valid_col_expr_ctas(layer["aes_mappings"].values(), df)
    valid_col_expr_ctas(layer.get("groupings", []), df)
    valid_col_expr_ctas(layer.get("collections", []), df)
