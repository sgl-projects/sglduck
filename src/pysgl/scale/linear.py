"""The linear (identity) scale."""

from __future__ import annotations

from .base import SglScale
from .utils import raise_for_non_nums


class SglScaleLinear(SglScale):
    def sgl_func_name(self) -> str:
        return "linear"

    def valid_scale(self, aes: str, layers: list[dict], dfs) -> None:
        super().valid_scale(aes, layers, dfs)
        raise_for_non_nums(self, aes, layers, dfs)

    def apply_scale(self, values):
        return values

    def apply_scale_inverse(self, values):
        return values
