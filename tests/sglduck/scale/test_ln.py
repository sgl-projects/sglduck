"""Tests for SglScaleLn."""

import re

import lets_plot
import numpy as np
import polars as pl
import pytest

from sglduck import SglError
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs
from sglduck.scale import SglScale, SglScaleLn

NON_NUMERICAL_MSG = (
    "Error: the ln scale can only be applied"
    " to aesthetics with numerical mappings."
)
NON_POSITIVE_MSG = (
    "Error: the ln scale can only be applied to"
    " aesthetics where all values from mappings are positive."
)


def test_is_an_sgl_scale_ln():
    assert isinstance(SglScaleLn(), SglScaleLn)
    assert isinstance(SglScaleLn(), SglScale)


def test_sgl_func_name_returns_ln():
    assert SglScaleLn().sgl_func_name() == "ln"


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
        SglScaleLn().valid_scale("color", pgs["layers"], dfs)


def test_valid_scale_raises_error_if_mapping_for_aes_is_categorical(test_con):
    pgs = sgl_to_pgs("""
        visualize
            cut as x
        from diamonds
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError, match=re.escape(NON_NUMERICAL_MSG)):
        SglScaleLn().valid_scale("x", pgs["layers"], dfs)


def test_valid_scale_raises_error_if_mapping_for_aes_is_temporal(test_con):
    pgs = sgl_to_pgs("""
        visualize
            day as x
        from synth
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    with pytest.raises(SglError, match=re.escape(NON_NUMERICAL_MSG)):
        SglScaleLn().valid_scale("x", pgs["layers"], dfs)


def test_valid_scale_doesnt_raise_error_if_mapping_for_aes_is_numerical(test_con):
    pgs = sgl_to_pgs("""
        visualize
            hp as x
        from cars
        using points
    """)
    dfs = result_dfs(pgs, test_con)

    SglScaleLn().valid_scale("x", pgs["layers"], dfs)


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
        SglScaleLn().valid_scale("color", pgs["layers"], dfs)


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
        SglScaleLn().valid_scale("x", pgs["layers"], dfs)


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

    SglScaleLn().valid_scale("x", pgs["layers"], dfs)


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

    SglScaleLn().valid_scale("color", pgs["layers"], dfs)


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
    df_1 = pl.DataFrame(
        {"col_1": [1.2, 3.4, np.nan], "col_2": [5.6, np.nan, 7.8]}
    )
    df_2 = pl.DataFrame(
        {"col_1": [1.2, 3.4, np.nan], "col_2": [5.6, np.nan, -7.8]}
    )
    return pgs["layers"], [df_1, df_2]


def test_valid_scale_doesnt_raise_error_if_no_layer_has_non_pos_value():
    layers, dfs = _non_pos_layers_and_dfs()

    SglScaleLn().valid_scale("x", layers, dfs)


def test_valid_scale_raises_error_if_layer_has_non_pos_value():
    layers, dfs = _non_pos_layers_and_dfs()

    with pytest.raises(SglError, match=re.escape(NON_POSITIVE_MSG)):
        SglScaleLn().valid_scale("y", layers, dfs)


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


def _as_dicts(scales):
    return [scale.as_dict() for scale in scales]


@pytest.mark.parametrize(
    "aes,scale_ctor",
    [
        ("x", lets_plot.scale_x_continuous),
        ("y", lets_plot.scale_y_continuous),
        ("theta", lets_plot.scale_x_continuous),
        ("r", lets_plot.scale_y_continuous),
        ("size", lets_plot.scale_size),
    ],
)
# lets-plot has no natural-log axis transform, so the ln scale renders with the
# (base-invariant in shape) log10 transform; see SglScaleLn.lets_plot_scales.
def test_lets_plot_scales_for_non_color_aes(aes, scale_ctor):
    pgs = sgl_to_pgs(f"visualize hp as {aes} from cars using points")
    assert _as_dicts(SglScaleLn().lets_plot_scales(aes, pgs)) == _as_dicts(
        [scale_ctor(trans="log10")]
    )


def test_lets_plot_scales_returns_color_scale_for_non_bar():
    pgs = sgl_to_pgs("visualize hp as x, mpg as y, cyl as color from cars using points")
    assert _as_dicts(SglScaleLn().lets_plot_scales("color", pgs)) == _as_dicts(
        [lets_plot.scale_color_continuous(trans="log10")]
    )


def test_lets_plot_scales_returns_fill_scale_for_bar():
    pgs = sgl_to_pgs("visualize hp as x, mpg as y, cyl as color from cars using bars")
    assert _as_dicts(SglScaleLn().lets_plot_scales("color", pgs)) == _as_dicts(
        [lets_plot.scale_fill_continuous(trans="log10")]
    )


def test_ln_scaled_plot_renders_svg(test_con):
    # lets-plot rejects an unknown transform name at render time, so exercise the
    # full pipeline to guard against a transform the backend doesn't support.
    from sglduck import db_get_plot

    svg = db_get_plot(
        test_con,
        "visualize hp as x, mpg as y from cars using points "
        "scale by ln(x), ln(y)",
    ).to_svg()
    assert "<svg" in svg
