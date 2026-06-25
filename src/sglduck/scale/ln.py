"""The natural-log scale."""

from __future__ import annotations

import numpy as np

from .base import SglScale
from .utils import lets_plot_continuous_scales, raise_for_non_nums, raise_for_non_pos


class SglScaleLn(SglScale):
    def sgl_func_name(self) -> str:
        return "ln"

    def lets_plot_scales(self, aes: str, pgs: dict) -> list:
        return lets_plot_continuous_scales("log", aes, pgs)

    def valid_scale(self, aes: str, layers: list[dict], dfs) -> None:
        super().valid_scale(aes, layers, dfs)
        raise_for_non_nums(self, aes, layers, dfs)
        raise_for_non_pos(self, aes, layers, dfs)

    def apply_scale(self, values):
        return np.log(values)

    def apply_scale_inverse(self, values):
        return np.exp(values)
