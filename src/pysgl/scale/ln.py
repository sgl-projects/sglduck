"""The natural-log scale."""

from __future__ import annotations

import numpy as np

from .base import SglScale


class SglScaleLn(SglScale):
    def sgl_func_name(self) -> str:
        return "ln"

    def apply_scale(self, values):
        return np.log(values)

    def apply_scale_inverse(self, values):
        return np.exp(values)
