"""The linear (identity) scale (~ R/sgl_scale_linear.R)."""

from __future__ import annotations

from .base import SglScale


class SglScaleLinear(SglScale):
    def sgl_func_name(self) -> str:
        return "linear"

    def apply_scale(self, values):
        return values

    def apply_scale_inverse(self, values):
        return values
