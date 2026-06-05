"""The natural-log scale (~ R/sgl_scale_ln.R)."""

from __future__ import annotations

import numpy as np

from .base import SglScale


class SglScaleLn(SglScale):
    def scale_name(self) -> str:
        return "ln"

    def apply_scale(self, values):
        return np.log(values)

    def apply_scale_inverse(self, values):
        return np.exp(values)
