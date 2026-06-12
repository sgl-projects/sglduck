"""Tests for SglCtaBin.

``add_transformed_column`` requires a scale and belongs to the data-pipeline
milestone, so it is not ported here yet.
"""

import re

import pandas as pd
import pytest

from pysgl import SglError
from pysgl.cta import SglCta, SglCtaBin


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
