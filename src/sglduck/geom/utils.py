"""Helpers for the geom rendering methods (ported from rsgl's sgl_geom_utils.R).

``mapping_col_name`` resolves the DataFrame column an aesthetic's ``col_expr``
maps to: the raw column for an identity CTA, or the ``sglduck.``-prefixed
derived column that ``perform_ctas`` produces for count/avg/bin.
``collection_group_cols`` resolves the columns a layer's ``collect by`` clause
groups by.
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


def collection_group_cols(layer: dict, scales: dict) -> list[str]:
    """The df columns a layer's ``collect by`` collections group by.

    A collection that matches a mapped aesthetic uses that aesthetic's (possibly
    scaled/derived) column; an unmapped collection resolves to its raw column or
    its linear-scaled derived column. Mirrors the collections branch of rsgl's
    ``ggplot_aes.sgl_geom``.
    """
    aes_mappings = layer["aes_mappings"]
    group_cols: list[str] = []
    for collection in layer.get("collections", []):
        corresponding_aes = [
            aes for aes, mapping in aes_mappings.items() if mapping == collection
        ]
        if corresponding_aes:
            for aes in corresponding_aes:
                group_cols.append(mapping_col_name(aes, aes_mappings[aes], scales))
        elif col_expr_has_cta(collection, "identity"):
            group_cols.append(collection["column"])
        elif col_expr_has_cta(collection, "bin"):
            num_bins = collection.get("arg", DEFAULT_NUM_BINS)
            group_cols.append(f"sglduck.linear.bin.{num_bins}.{collection['column']}")
        elif col_expr_has_cta(collection, "avg"):
            group_cols.append(f"sglduck.linear.avg.{collection['column']}")
        else:
            group_cols.append("sglduck.count")
    return list(dict.fromkeys(group_cols))
