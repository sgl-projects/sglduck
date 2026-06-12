"""The pysgl exception type."""

from __future__ import annotations


class SglError(Exception):
    """Raised when a SGL statement fails semantic validation.

    Parser errors (invalid tokens, syntax errors) surface as exceptions from
    the compiled ``_sgl`` bridge instead.
    """
