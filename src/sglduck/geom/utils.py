"""Helpers for the geom rendering methods (ported from rsgl's sgl_geom_utils.R).

``mapping_col_name`` resolves the DataFrame column an aesthetic's ``col_expr``
maps to: the raw column for an identity CTA, or the ``sglduck.``-prefixed
derived column that ``perform_ctas`` produces for count/avg/bin.
"""

from __future__ import annotations

from ..utils import col_expr_has_cta

# rsgl's default bin count when bin() is used without an explicit argument.
DEFAULT_NUM_BINS = 30


def _scale_name(aes: str, scales: dict) -> str:
    """The scale applied to the aesthetic, or ``"linear"`` when none is."""
    if aes in scales:
        return scales[aes].sgl_func_name()
    return "linear"


def mapping_col_name(aes: str, col_expr: dict, scales: dict) -> str:
    """The df column a col_expr maps to (a raw or ``sglduck.``-derived column)."""
    if col_expr_has_cta(col_expr, "identity"):
        return col_expr["column"]
    if col_expr_has_cta(col_expr, "count"):
        return "sglduck.count"
    if col_expr_has_cta(col_expr, "avg"):
        return f"sglduck.{_scale_name(aes, scales)}.avg.{col_expr['column']}"
    if col_expr_has_cta(col_expr, "bin"):
        num_bins = col_expr.get("arg", DEFAULT_NUM_BINS)
        return f"sglduck.{_scale_name(aes, scales)}.bin.{num_bins}.{col_expr['column']}"
