"""Helpers shared across the CTA classes."""

from __future__ import annotations

from ..errors import SglError


def raise_if_arg_present(col_expr: dict) -> None:
    """Raise if the col_expr carries an argument its CTA doesn't accept."""
    if "arg" in col_expr:
        raise SglError(
            f"Error: {col_expr['cta'].sgl_func_name()} function received"
            " unexpected argument."
        )
