"""Tests for SglCtaBin."""

import re

import numpy as np
import pandas as pd
import pytest

from pysgl import SglError
from pysgl.cta import SglCta, SglCtaBin
from pysgl.scale import SglScaleLinear, SglScaleLog


def test_is_an_sgl_cta_bin():
    assert isinstance(SglCtaBin(), SglCtaBin)
    assert isinstance(SglCtaBin(), SglCta)


def test_sgl_func_name_returns_bin():
    assert SglCtaBin().sgl_func_name() == "bin"


def test_valid_cta_raises_error_for_star():
    col_expr = {"column": "*", "cta": SglCtaBin()}

    with pytest.raises(
        SglError,
        match=re.escape("Error: '*' can only be used inside an aggregation function"),
    ):
        SglCtaBin().valid_cta(col_expr, pd.DataFrame())


def test_valid_cta_doesnt_raise_error_for_numerical_column(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "number", "cta": SglCtaBin()}

    SglCtaBin().valid_cta(col_expr, df)


def test_valid_cta_doesnt_raise_error_for_temporal_column(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "day", "cta": SglCtaBin()}

    SglCtaBin().valid_cta(col_expr, df)


def test_valid_cta_raises_error_for_categorical_column(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "letter", "cta": SglCtaBin()}

    with pytest.raises(
        SglError,
        match=re.escape(
            "Error: cannot apply bin to a categorical column, found bin(letter)."
        ),
    ):
        SglCtaBin().valid_cta(col_expr, df)


def test_valid_cta_doesnt_raise_error_for_no_arg(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "number", "cta": SglCtaBin()}

    SglCtaBin().valid_cta(col_expr, df)


def test_valid_cta_doesnt_raise_error_for_arg_value_greater_than_zero(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "number", "cta": SglCtaBin(), "arg": 1}

    SglCtaBin().valid_cta(col_expr, df)


def test_valid_cta_raises_error_for_arg_value_of_zero(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "number", "cta": SglCtaBin(), "arg": 0}

    with pytest.raises(
        SglError,
        match=re.escape("Error: number of bins must be greater than 0."),
    ):
        SglCtaBin().valid_cta(col_expr, df)


def test_valid_cta_raises_error_for_negative_arg_value(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "number", "cta": SglCtaBin(), "arg": -1}

    with pytest.raises(
        SglError,
        match=re.escape("Error: number of bins must be greater than 0."),
    ):
        SglCtaBin().valid_cta(col_expr, df)


def test_add_transformed_column_adds_correct_values_for_linear_scale():
    df = pd.DataFrame({"col_1": np.arange(0, 11)})
    expected = [0.992, 0.992, 2.996, 2.996, 5, 5, 5, 7.004, 7.004, 9.008, 9.008]

    result = SglCtaBin().add_transformed_column(
        "col_1", df, SglScaleLinear(), num_bins=5
    )

    np.testing.assert_allclose(result["pysgl.linear.bin.5.col_1"], expected)


def test_add_transformed_column_adds_correct_values_for_log_scale():
    df = pd.DataFrame({"col_1": np.power(10.0, np.arange(0, 11))})
    expected = np.power(
        10.0, [0.992, 0.992, 2.996, 2.996, 5, 5, 5, 7.004, 7.004, 9.008, 9.008]
    )

    result = SglCtaBin().add_transformed_column("col_1", df, SglScaleLog(), num_bins=5)

    np.testing.assert_allclose(result["pysgl.log.bin.5.col_1"], expected)


def test_add_transformed_column_uses_30_bins_by_default():
    df = pd.DataFrame({"col_1": np.arange(0, 101)})

    result = SglCtaBin().add_transformed_column("col_1", df, SglScaleLinear())

    assert result["pysgl.linear.bin.30.col_1"].nunique() == 30


def test_add_transformed_column_doesnt_modify_column_if_already_exists():
    df = pd.DataFrame({"pysgl.linear.bin.30.col_1": [0]})

    result = SglCtaBin().add_transformed_column("col_1", df, SglScaleLinear())

    assert result["pysgl.linear.bin.30.col_1"].tolist() == [0]


def test_add_transformed_column_doesnt_mutate_input_df():
    df = pd.DataFrame({"col_1": np.arange(0, 11)})

    SglCtaBin().add_transformed_column("col_1", df, SglScaleLinear())

    assert list(df.columns) == ["col_1"]


def test_add_transformed_column_requires_a_scale():
    df = pd.DataFrame({"col_1": [0]})

    with pytest.raises(TypeError):
        SglCtaBin().add_transformed_column("col_1", df)


def test_is_aggregation_returns_false():
    assert SglCtaBin().is_aggregation() is False


def test_is_transformation_returns_true():
    assert SglCtaBin().is_transformation() is True


def test_expr_text_without_arg():
    col_expr = {"column": "col_1", "cta": SglCtaBin()}
    assert SglCtaBin().expr_text(col_expr) == "bin(col_1)"


def test_expr_text_with_arg():
    col_expr = {"column": "col_1", "cta": SglCtaBin(), "arg": 10}
    assert SglCtaBin().expr_text(col_expr) == "bin(col_1, 10)"
