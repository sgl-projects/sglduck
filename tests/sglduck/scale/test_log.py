"""Tests for SglScaleLog.

``lets_plot_scales`` requires the full pgs and belongs to the rendering
milestone, so it is not ported here yet.
"""

import re

import numpy as np
import pandas as pd
import pytest

from sglduck import SglError
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs
from sglduck.scale import SglScale, SglScaleLog

NON_NUMERICAL_MSG = (
    "Error: the log scale can only be applied"
    " to aesthetics with numerical mappings."
)
NON_POSITIVE_MSG = (
    "Error: the log scale can only be applied to"
    " aesthetics where all values from mappings are positive."
)


def test_is_an_sgl_scale_log():
    assert isinstance(SglScaleLog(), SglScaleLog)
    assert isinstance(SglScaleLog(), SglScale)


def test_sgl_func_name_returns_log():
    assert SglScaleLog().sgl_func_name() == "log"


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
        SglScaleLog().valid_scale("color", pgs["layers"], dfs)


def test_valid_scale_raises_error_if_mapping_for_aes_is_categorical(test_con):
    pgs = sgl_to_pgs("""
        visualize
            cut as x
        from diamonds
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError, match=re.escape(NON_NUMERICAL_MSG)):
        SglScaleLog().valid_scale("x", pgs["layers"], dfs)


def test_valid_scale_raises_error_if_mapping_for_aes_is_temporal(test_con):
    pgs = sgl_to_pgs("""
        visualize
            day as x
        from synth
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError, match=re.escape(NON_NUMERICAL_MSG)):
        SglScaleLog().valid_scale("x", pgs["layers"], dfs)


def test_valid_scale_doesnt_raise_error_if_mapping_for_aes_is_numerical(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    SglScaleLog().valid_scale("x", pgs["layers"], dfs)


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
        SglScaleLog().valid_scale("color", pgs["layers"], dfs)


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
        SglScaleLog().valid_scale("x", pgs["layers"], dfs)


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

    SglScaleLog().valid_scale("x", pgs["layers"], dfs)


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

    SglScaleLog().valid_scale("color", pgs["layers"], dfs)


def _non_pos_layers_and_dfs():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from placeholder
        using (
            points
            layer
            regression line
        )
    """)
    df_1 = pd.DataFrame(
        {"col_1": [1.2, 3.4, np.nan], "col_2": [5.6, np.nan, 7.8]}
    )
    df_2 = pd.DataFrame(
        {"col_1": [1.2, 3.4, np.nan], "col_2": [5.6, np.nan, -7.8]}
    )
    return pgs["layers"], [df_1, df_2]


def test_valid_scale_doesnt_raise_error_if_no_layer_has_non_pos_value():
    layers, dfs = _non_pos_layers_and_dfs()

    SglScaleLog().valid_scale("x", layers, dfs)


def test_valid_scale_raises_error_if_layer_has_non_pos_value():
    layers, dfs = _non_pos_layers_and_dfs()

    with pytest.raises(SglError, match=re.escape(NON_POSITIVE_MSG)):
        SglScaleLog().valid_scale("y", layers, dfs)


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
