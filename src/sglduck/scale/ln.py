"""The natural-log scale."""

from __future__ import annotations

import numpy as np

from .base import SglScale
from .utils import raise_for_non_nums, raise_for_non_pos


class SglScaleLn(SglScale):
    def sgl_func_name(self) -> str:
        return "ln"

    def valid_scale(self, aes: str, layers: list[dict], dfs) -> None:
        super().valid_scale(aes, layers, dfs)
        raise_for_non_nums(self, aes, layers, dfs)
        raise_for_non_pos(self, aes, layers, dfs)

    def apply_scale(self, values):
        return np.log(values)

    def apply_scale_inverse(self, values):
        return np.exp(values)
