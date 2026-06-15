"""Apply a layer's column transformations (the "ct" of cta).

Ported from rsgl's ``perform_cts_for_layer.R``. For every transformation CTA
(``bin``) referenced in a layer's visualize, group-by, or collect-by clauses,
add the corresponding transformed column to the layer's DataFrame. Aesthetic
mappings are transformed with their own scale (from the ``scale by`` clause, or
linear by default); additional group/collect expressions are transformed with a
linear scale. ``add_transformed_column`` de-duplicates by output column name, so
the same (column, scale, bin-count) transform is never added twice.
"""

from __future__ import annotations

import pandas as pd

from .scale import SglScaleLinear


def _add_trans_cols_from_aes(
    aes_mappings: dict, df: pd.DataFrame, scales: dict | None
) -> pd.DataFrame:
    for aes, aes_mapping in aes_mappings.items():
        cta = aes_mapping["cta"]
        if not cta.is_transformation():
            continue
        if scales and aes in scales:
            scale = scales[aes]
        else:
            scale = SglScaleLinear()
        kwargs = {}
        if "arg" in aes_mapping:
            kwargs["num_bins"] = aes_mapping["arg"]
        df = cta.add_transformed_column(aes_mapping["column"], df, scale, **kwargs)
    return df


def _add_trans_cols_from_col_exprs(
    col_exprs: list[dict], df: pd.DataFrame
) -> pd.DataFrame:
    for col_expr in col_exprs:
        cta = col_expr["cta"]
        if not cta.is_transformation():
            continue
        kwargs = {}
        if "arg" in col_expr:
            kwargs["num_bins"] = col_expr["arg"]
        df = cta.add_transformed_column(
            col_expr["column"], df, SglScaleLinear(), **kwargs
        )
    return df


def perform_cts_for_layer(
    layer: dict, df: pd.DataFrame, scales: dict | None
) -> pd.DataFrame:
    """Return ``df`` with every transformed column the layer references added."""
    aes_mappings = layer["aes_mappings"]
    aes_values = list(aes_mappings.values())
    groupings = layer.get("groupings", [])
    collections = layer.get("collections", [])

    df = _add_trans_cols_from_aes(aes_mappings, df, scales)

    additional_group_cols = [
        col_expr for col_expr in groupings if col_expr not in aes_values
    ]
    df = _add_trans_cols_from_col_exprs(additional_group_cols, df)

    additional_collect_cols = [
        col_expr
        for col_expr in collections
        if col_expr not in aes_values and col_expr not in groupings
    ]
    df = _add_trans_cols_from_col_exprs(additional_collect_cols, df)

    return df
