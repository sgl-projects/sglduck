"""Port of rsgl's test-sgl_scale_linear.R (pure methods only).

``valid_scale`` and ``plotnine_scales`` require layers/DataFrames/the full pgs
and belong to the validation and rendering milestones, so they are not ported
here yet.
"""

import numpy as np

from pysgl.scale import SglScale, SglScaleLinear


def test_is_an_sgl_scale_linear():
    assert isinstance(SglScaleLinear(), SglScaleLinear)
    assert isinstance(SglScaleLinear(), SglScale)


def test_scale_name_returns_linear():
    assert SglScaleLinear().scale_name() == "linear"


def test_apply_scale_returns_original_values():
    values = np.array([1.2, np.nan, 3.4])
    np.testing.assert_allclose(
        SglScaleLinear().apply_scale(values), values, equal_nan=True
    )


def test_apply_scale_inverse_returns_original_values():
    values = np.array([1.2, np.nan, 3.4])
    np.testing.assert_allclose(
        SglScaleLinear().apply_scale_inverse(values), values, equal_nan=True
    )
