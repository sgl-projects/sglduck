"""The ``db_get_plot`` entry point (ported from rsgl's ``dbGetPlot.R``).

``db_get_plot`` takes a DuckDB connection and a SGL statement and returns the
corresponding plot. Building the plot parses the statement, runs each layer's
SQL, reconciles column casing, and validates the statement's semantics; the
returned ``SglPlot`` renders lazily.
"""

from __future__ import annotations

from .match_col_casing import match_col_casing
from .pgs import sgl_to_pgs
from .result_dfs import result_dfs
from .sgl_plot import SglPlot
from .validate import validate_semantics


def db_get_plot(con, sgl_stmt: str) -> SglPlot:
    """Return the ``SglPlot`` defined by a SGL statement.

    :param con: A DuckDB connection holding the tables the statement queries.
    :param sgl_stmt: A SGL statement (see the Get started guide for the language).
    :return: An ``SglPlot`` that renders the corresponding plot.
    """
    pgs = sgl_to_pgs(sgl_stmt)
    dfs = result_dfs(pgs, con)
    pgs = match_col_casing(pgs, dfs)
    validate_semantics(pgs, dfs)
    return SglPlot(pgs, dfs)
