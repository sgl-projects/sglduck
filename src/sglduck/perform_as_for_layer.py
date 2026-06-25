"""Apply a layer's aggregations (the "a" of cta).

Ported from rsgl's ``perform_as_for_layer.R``. When a layer references any
aggregation CTA (``avg``, ``count``), group its DataFrame by the group-by
columns and summarize each aggregation into its own column. Aggregations on a
non-linearly scaled aesthetic are computed in the scaled space (the values are
pre-scaled, aggregated, then mapped back through the scale's inverse), mirroring
rsgl's add-scale / summarize / back-scale sequence.
"""

from __future__ import annotations

import pandas as pd

from .scale import SglScaleLinear
from .utils import filter_agg_exprs, filter_agg_mappings


def _non_linear_scales(scales: dict | None) -> dict:
    if not scales:
        return {}
    linear = SglScaleLinear()
    return {aes: scale for aes, scale in scales.items() if scale != linear}


def _needs_scale_mappings(layer: dict, scales: dict | None) -> dict:
    """Aes->col_expr for aggregations on a non-linearly scaled, scalable aes."""
    non_lin_aes = _non_linear_scales(scales).keys()
    agg_mappings = filter_agg_mappings(layer["aes_mappings"])
    return {
        aes: col_expr
        for aes, col_expr in agg_mappings.items()
        if aes in non_lin_aes and col_expr["cta"].needs_scaling()
    }


def add_scaled_cols(
    layer: dict, scales: dict | None, df: pd.DataFrame
) -> pd.DataFrame:
    """Add a pre-scaled source column for each non-linearly scaled aggregation."""
    needs_scale_mappings = _needs_scale_mappings(layer, scales)
    if not needs_scale_mappings:
        return df
    df = df.copy()
    for aes, col_expr in needs_scale_mappings.items():
        scale = scales[aes]
        existing_col = col_expr["column"]
        new_col = f"sglduck.{scale.sgl_func_name()}.{existing_col}"
        if new_col not in df.columns:
            df[new_col] = scale.apply_scale(df[existing_col])
    return df


def summarize_args(layer: dict, scales: dict | None) -> dict:
    """Map each aggregation's output column name to its aggregation spec."""
    aes_mappings = layer["aes_mappings"]
    args: dict = {}
    for aes, col_expr in filter_agg_mappings(aes_mappings).items():
        scale = scales[aes] if (scales and aes in scales) else None
        cta = col_expr["cta"]
        name = cta.agg_col_name(col_expr, scale)
        if name not in args:
            args[name] = cta.agg_col_expr(col_expr, scale)

    aes_values = list(aes_mappings.values())
    addnl_collections = [
        col_expr
        for col_expr in layer.get("collections", [])
        if col_expr not in aes_values
    ]
    for col_expr in filter_agg_exprs(addnl_collections):
        cta = col_expr["cta"]
        name = cta.agg_col_name(col_expr, None)
        if name not in args:
            args[name] = cta.agg_col_expr(col_expr, None)
    return args


def group_by_col_names(
    col_expr: dict, aes_mappings: dict, scales: dict | None
) -> list[str]:
    """The DataFrame column name(s) to group by for one group-by expression."""
    from .utils import col_expr_has_cta

    column = col_expr["column"]
    if not col_expr_has_cta(col_expr, "bin"):
        return [column]

    num_bins = col_expr["arg"] if "arg" in col_expr else 30
    aes_values = list(aes_mappings.values())
    if col_expr not in aes_values:
        return [f"sglduck.linear.bin.{num_bins}.{column}"]

    corresponding_aes = [
        aes for aes, mapping in aes_mappings.items() if mapping == col_expr
    ]
    corresponding_scales = {
        aes: scales[aes]
        for aes in corresponding_aes
        if scales and aes in scales
    }
    names = [
        f"sglduck.{scale.sgl_func_name()}.bin.{num_bins}.{column}"
        for scale in corresponding_scales.values()
    ]
    if any(aes not in corresponding_scales for aes in corresponding_aes):
        names.append(f"sglduck.linear.bin.{num_bins}.{column}")
    return names


def backscale_cols(
    layer: dict, scales: dict | None, df: pd.DataFrame
) -> pd.DataFrame:
    """Map each non-linearly scaled aggregate back through the scale's inverse."""
    needs_scale_mappings = _needs_scale_mappings(layer, scales)
    if not needs_scale_mappings:
        return df
    df = df.copy()
    backscaled: set[str] = set()
    for aes, col_expr in needs_scale_mappings.items():
        scale = scales[aes]
        col_name = col_expr["cta"].agg_col_name(col_expr, scale)
        if col_name not in backscaled:
            df[col_name] = scale.apply_scale_inverse(df[col_name])
            backscaled.add(col_name)
    return df


def perform_as_for_layer(
    layer: dict, df: pd.DataFrame, scales: dict | None
) -> pd.DataFrame:
    """Return the layer's DataFrame aggregated per its group-by columns."""
    aes_mappings = layer["aes_mappings"]
    aes_aggs = filter_agg_mappings(aes_mappings)
    collect_aggs = filter_agg_exprs(layer.get("collections", []))
    if not aes_aggs and not collect_aggs:
        return df

    scaled_df = add_scaled_cols(layer, scales, df)
    args = summarize_args(layer, scales)

    if "groupings" not in layer:
        row = {
            name: len(scaled_df) if agg.func == "size"
            else scaled_df[agg.column].agg(agg.func)
            for name, agg in args.items()
        }
        return pd.DataFrame([row])

    group_by_cols = list(
        dict.fromkeys(
            name
            for col_expr in layer["groupings"]
            for name in group_by_col_names(col_expr, aes_mappings, scales)
        )
    )
    grouped = scaled_df.groupby(group_by_cols, dropna=False, sort=False)
    summarized = {
        name: grouped.size() if agg.func == "size"
        else grouped[agg.column].agg(agg.func)
        for name, agg in args.items()
    }
    agg_df = pd.concat(summarized, axis=1).reset_index()

    return backscale_cols(layer, scales, agg_df)
