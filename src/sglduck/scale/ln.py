"""The natural-log scale."""

from __future__ import annotations

import numpy as np

from .base import SglScale
from .utils import lets_plot_continuous_scales, raise_for_non_nums, raise_for_non_pos


class SglScaleLn(SglScale):
    def sgl_func_name(self) -> str:
        return "ln"

    def lets_plot_scales(self, aes: str, pgs: dict) -> list:
        # lets-plot has no natural-log axis transform (only log10/log2), where
        # rsgl uses ggplot2's "log". A log axis is base-invariant in shape — the
        # auto-ranged coordinate absorbs the constant factor between ln and
        # log10 — so log10 renders the same plot, differing only in tick-label
        # style. The exact natural-log data scaling (apply_scale) is unaffected.
        return lets_plot_continuous_scales("log10", aes, pgs)

    def valid_scale(self, aes: str, layers: list[dict], dfs) -> None:
        super().valid_scale(aes, layers, dfs)
        raise_for_non_nums(self, aes, layers, dfs)
        raise_for_non_pos(self, aes, layers, dfs)

    def apply_scale(self, values):
        return np.log(values)

    def apply_scale_inverse(self, values):
        return np.exp(values)
