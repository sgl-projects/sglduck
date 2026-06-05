"""Port of rsgl's test-sgl_scale_ln.R (pure methods only).

``valid_scale`` and ``plotnine_scales`` are deferred to the validation and
rendering milestones.
"""

import numpy as np

from pysgl.scale import SglScale, SglScaleLn


def test_is_an_sgl_scale_ln():
    assert isinstance(SglScaleLn(), SglScaleLn)
    assert isinstance(SglScaleLn(), SglScale)


def test_scale_name_returns_ln():
    assert SglScaleLn().scale_name() == "ln"


def test_apply_scale_returns_natural_log():
    values = np.array([10.0, np.nan, 27.5])
    expected = np.array([2.302585093, np.nan, 3.314186005])
    np.testing.assert_allclose(
        SglScaleLn().apply_scale(values), expected, equal_nan=True
    )


def test_apply_scale_inverse_returns_e_to_the_power():
    values = np.array([2.302585093, np.nan, 3.314186005])
    expected = np.array([10.0, np.nan, 27.5])
    np.testing.assert_allclose(
        SglScaleLn().apply_scale_inverse(values), expected, equal_nan=True
    )
