"""Validate a layer's group by clause."""

from __future__ import annotations

from ..errors import SglError
from ..utils import filter_agg_exprs


def valid_groupings(layer: dict) -> None:
    """Raise if the layer's groupings are inconsistent with its aggregations."""
    viz_collect_exprs = [
        *layer["aes_mappings"].values(),
        *layer.get("collections", []),
    ]
    viz_collect_aggs = filter_agg_exprs(viz_collect_exprs)
    viz_collect_unaggs = [
        col_expr
        for col_expr in viz_collect_exprs
        if col_expr not in viz_collect_aggs
    ]

    if "groupings" in layer:
        groupings = layer["groupings"]

        group_agg_exprs = filter_agg_exprs(groupings)
        if group_agg_exprs:
            raise SglError(
                "Error: group by clause cannot contain aggregation expressions."
            )

        ungrouped_aggs = [
            col_expr for col_expr in viz_collect_unaggs if col_expr not in groupings
        ]
        if ungrouped_aggs:
            raise SglError(
                "Error: unaggregated expressions in the visualize"
                " and collect by clauses must also be present in the"
                " group by clause."
            )
    else:
        if viz_collect_aggs and viz_collect_unaggs:
            raise SglError(
                "Error: given that aggregations are present,"
                " all unaggregated expressions in the visualize"
                " and collect by clause must also be included"
                " in the group by clause."
                " However, no group by clause was provided."
            )
