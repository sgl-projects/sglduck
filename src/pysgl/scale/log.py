"""The base-10 log scale (~ R/sgl_scale_log.R)."""

from __future__ import annotations

import numpy as np

from .base import SglScale


class SglScaleLog(SglScale):
    def scale_name(self) -> str:
        return "log"

    def apply_scale(self, values):
        return np.log10(values)

    def apply_scale_inverse(self, values):
        return np.power(10.0, values)
