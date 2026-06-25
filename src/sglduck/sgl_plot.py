"""The ``SglPlot`` object (ported from rsgl's ``sgl_plot.R`` / ``print.sgl_plot``).

An ``SglPlot`` bundles the matched-casing pgs with its per-layer result frames.
Rendering is lazy and mirrors rsgl's ``print.sgl_plot``: reconcile date/timestamp
columns, run the CTA pipeline, then assemble the lets-plot figure.
"""

from __future__ import annotations

from .cast_columns import cast_columns
from .perform_ctas import perform_ctas
from .rgs_to_lets_plot import rgs_to_lets_plot


class SglPlot:
    def __init__(self, pgs: dict, result_dfs: list):
        self.pgs = pgs
        self.result_dfs = result_dfs

    def _figure(self):
        """Build the lets-plot figure (the render-time data + plot pipeline)."""
        casted_dfs = cast_columns(self.pgs, self.result_dfs)
        post_cta_dfs = perform_ctas(self.pgs, casted_dfs)
        return rgs_to_lets_plot(self.pgs, post_cta_dfs)

    def show(self) -> None:
        """Open the plot in the default browser."""
        self._figure().show()

    def to_svg(self) -> str:
        return self._figure().to_svg()

    def to_html(self) -> str:
        return self._figure().to_html()

    def save(self, filename: str, **kwargs):
        """Save the plot to ``filename`` (delegates to ``lets_plot.export.ggsave``)."""
        from lets_plot.export import ggsave

        return ggsave(self._figure(), filename, **kwargs)

    def _repr_html_(self) -> str:
        """Rich display for Jupyter (the analog of rsgl's ``print.sgl_plot``)."""
        return self._figure()._repr_html_()
