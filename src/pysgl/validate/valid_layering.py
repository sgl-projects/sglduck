"""Validate aesthetic consistency across layers."""

from __future__ import annotations

import pandas as pd

from ..constants import POS_AES
from ..errors import SglError
from ..types import (
    is_categorical_mapping,
    is_numerical_mapping,
    is_temporal_mapping,
)
from ..utils import all_aesthetics


def valid_layering_for_aes(pgs: dict, dfs: list[pd.DataFrame], aes: str) -> None:
    """Raise if the aesthetic's layering is invalid."""
    if aes in POS_AES:
        if not all(aes in layer["aes_mappings"] for layer in pgs["layers"]):
            raise SglError(
                "Error: if a positional aesthetic is present in one layer,"
                f" it must be present in all layers. '{aes}' is not present in"
                " all layers."
            )
    numerical_found = False
    categorical_found = False
    temporal_found = False
    for layer, df in zip(pgs["layers"], dfs):
        if aes in layer["aes_mappings"]:
            if is_numerical_mapping(layer, df, aes):
                numerical_found = True
            elif is_categorical_mapping(layer, df, aes):
                categorical_found = True
            elif is_temporal_mapping(layer, df, aes):
                temporal_found = True
    types_found = [
        type_name
        for type_name, found in (
            ("numerical", numerical_found),
            ("categorical", categorical_found),
            ("temporal", temporal_found),
        )
        if found
    ]
    if len(types_found) > 1:
        raise SglError(
            "Error: an aesthetic must be mapped to the same type"
            " (numerical, categorical, or temporal) across layers."
            f" Found the following types for the {aes} aesthetic:"
            f" {', '.join(types_found)}."
        )


def valid_layering(pgs: dict, dfs: list[pd.DataFrame]) -> None:
    """Raise if any aesthetic is layered inconsistently."""
    for aes in all_aesthetics(pgs):
        valid_layering_for_aes(pgs, dfs, aes)
