"""The identity CTA."""

from __future__ import annotations

import polars as pl

from ..errors import SglError
from .base import SglCta


class SglCtaIdentity(SglCta):
    def valid_cta(self, col_expr: dict, df: pl.DataFrame) -> None:
        if col_expr["column"] == "*":
            raise SglError(
                "Error: '*' can only be used inside an aggregation function"
            )

    def is_aggregation(self) -> bool:
        return False

    def is_transformation(self) -> bool:
        return False

    def expr_text(self, col_expr: dict) -> str:
        return col_expr["column"]
