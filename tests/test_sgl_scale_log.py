"""Port of rsgl's test-sgl_scale_log.R (pure methods only).

``valid_scale`` and ``plotnine_scales`` are deferred to the validation and
rendering milestones.
"""

import numpy as np

from pysgl.scale import SglScale, SglScaleLog


def test_is_an_sgl_scale_log():
    assert isinstance(SglScaleLog(), SglScaleLog)
    assert isinstance(SglScaleLog(), SglScale)


def test_scale_name_returns_log():
    assert SglScaleLog().scale_name() == "log"


def test_apply_scale_returns_base_10_log():
    values = np.array([10.0, np.nan, 27.5])
    expected = np.array([1.0, np.nan, 1.43933269])
    np.testing.assert_allclose(
        SglScaleLog().apply_scale(values), expected, equal_nan=True
    )


def test_apply_scale_inverse_returns_10_to_the_power():
    values = np.array([1.0, np.nan, 1.43933269])
    expected = np.array([10.0, np.nan, 27.5])
    np.testing.assert_allclose(
        SglScaleLog().apply_scale_inverse(values), expected, equal_nan=True
    )
