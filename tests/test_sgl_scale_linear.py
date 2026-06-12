"""Tests for SglScaleLinear.

``plotnine_scales`` requires the full pgs and belongs to the rendering
milestone, so it is not ported here yet.
"""

import re

import numpy as np
import pytest

from pysgl import SglError
from pysgl.pgs import sgl_to_pgs
from pysgl.result_dfs import result_dfs
from pysgl.scale import SglScale, SglScaleLinear

NON_NUMERICAL_MSG = (
    "Error: the linear scale can only be applied"
    " to aesthetics with numerical mappings."
)


def test_is_an_sgl_scale_linear():
    assert isinstance(SglScaleLinear(), SglScaleLinear)
    assert isinstance(SglScaleLinear(), SglScale)


def test_sgl_func_name_returns_linear():
    assert SglScaleLinear().sgl_func_name() == "linear"


def test_valid_scale_raises_error_if_no_mapping_for_aes(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(
        SglError,
        match=re.escape("Error: a scaled aesthetic must have at least one mapping"),
    ):
        SglScaleLinear().valid_scale("color", pgs["layers"], dfs)


def test_valid_scale_raises_error_if_mapping_for_aes_is_categorical(test_con):
    pgs = sgl_to_pgs("""
        visualize
            cut as x
        from diamonds
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError, match=re.escape(NON_NUMERICAL_MSG)):
        SglScaleLinear().valid_scale("x", pgs["layers"], dfs)


def test_valid_scale_raises_error_if_mapping_for_aes_is_temporal(test_con):
    pgs = sgl_to_pgs("""
        visualize
            day as x
        from synth
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError, match=re.escape(NON_NUMERICAL_MSG)):
        SglScaleLinear().valid_scale("x", pgs["layers"], dfs)


def test_valid_scale_doesnt_raise_error_if_mapping_for_aes_is_numerical(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    SglScaleLinear().valid_scale("x", pgs["layers"], dfs)


def test_valid_scale_raises_error_if_no_mapping_for_aes_in_any_layer(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y
        from cars
        using (
            points
            layer
            regression line
        )
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(
        SglError,
        match=re.escape("Error: a scaled aesthetic must have at least one mapping"),
    ):
        SglScaleLinear().valid_scale("color", pgs["layers"], dfs)


def test_valid_scale_raises_error_if_any_mapping_for_aes_is_non_numerical(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x
        from cars
        using points

        layer

        visualize
            day as x
        from synth
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError, match=re.escape(NON_NUMERICAL_MSG)):
        SglScaleLinear().valid_scale("x", pgs["layers"], dfs)


def test_valid_scale_doesnt_raise_error_if_all_mappings_for_aes_are_numerical(
    test_con,
):
    pgs = sgl_to_pgs("""
        visualize
            hp as x
        from cars
        using points

        layer

        visualize
            number as x
        from synth
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    SglScaleLinear().valid_scale("x", pgs["layers"], dfs)


def test_valid_scale_doesnt_raise_error_if_some_layers_lack_mapping_for_aes(
    test_con,
):
    pgs = sgl_to_pgs("""
        visualize
            hp as x,
            mpg as y,
            cyl as color
        from cars
        using points

        layer

        visualize
            hp as x,
            mpg as y
        from cars
        using regression line
    """)
    dfs = result_dfs(pgs, test_con)

    SglScaleLinear().valid_scale("color", pgs["layers"], dfs)


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
