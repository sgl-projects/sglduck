"""Helpers shared across the pgs pipeline modules.

``filter_agg_exprs`` is deferred until the ``is_aggregation`` generic lands on
the CTA classes.
"""

from __future__ import annotations

import pandas as pd

from .cta import SglCtaAvg, SglCtaBin, SglCtaCount, SglCtaIdentity

_CTA_NAME_TO_OBJECT = {
    "identity": SglCtaIdentity(),
    "bin": SglCtaBin(),
    "count": SglCtaCount(),
    "avg": SglCtaAvg(),
}


def col_expr_has_cta(col_expr: dict, cta_name: str) -> bool:
    """Whether the col_expr's cta is the named one."""
    if cta_name not in _CTA_NAME_TO_OBJECT:
        raise ValueError(
            f"cta_name must be one of {list(_CTA_NAME_TO_OBJECT)}, got {cta_name!r}"
        )
    return _CTA_NAME_TO_OBJECT[cta_name] == col_expr["cta"]


def filter_col_exprs_by_cta(col_exprs: list[dict], cta_name: str) -> list[dict]:
    """The col_exprs whose cta is the named one."""
    if cta_name not in _CTA_NAME_TO_OBJECT:
        raise ValueError(
            f"cta_name must be one of {list(_CTA_NAME_TO_OBJECT)}, got {cta_name!r}"
        )
    return [col_expr for col_expr in col_exprs if col_expr_has_cta(col_expr, cta_name)]


def all_aesthetics(pgs: dict) -> list[str]:
    """The unique aesthetics mapped across all layers, in first-seen order."""
    return list(
        dict.fromkeys(
            aes for layer in pgs["layers"] for aes in layer["aes_mappings"]
        )
    )


def column_from_aes(layer: dict, df: pd.DataFrame, aes: str) -> pd.Series:
    """The df column the layer maps to the given aesthetic."""
    return df[layer["aes_mappings"][aes]["column"]]
