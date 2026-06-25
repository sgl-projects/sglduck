"""Run all semantic validations over a pgs and its layer DataFrames."""

from __future__ import annotations

import polars as pl

from .valid_aesthetics import valid_aesthetics
from .valid_collections import valid_collections
from .valid_column_classes import valid_column_classes
from .valid_column_refs import valid_column_refs
from .valid_ctas import valid_ctas
from .valid_facet import valid_facet
from .valid_groupings import valid_groupings
from .valid_layering import valid_layering
from .valid_qualifier import valid_qualifier
from .valid_scales import valid_scales
from .valid_titles import valid_titles


def validate_semantics(pgs: dict, dfs: list[pl.DataFrame]) -> None:
    """Raise SglError if the pgs fails any semantic validation."""
    for layer, df in zip(pgs["layers"], dfs):
        valid_column_refs(layer, df)
        valid_column_classes(layer, df)
        valid_ctas(layer, df)
        valid_aesthetics(layer)
        valid_groupings(layer)
        valid_collections(layer)
        valid_qualifier(layer)
    valid_layering(pgs, dfs)
    valid_scales(pgs, dfs)
    valid_facet(pgs, dfs)
    valid_titles(pgs)
