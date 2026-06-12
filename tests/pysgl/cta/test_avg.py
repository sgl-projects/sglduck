"""Tests for SglCtaAvg.

``agg_col_name`` and ``agg_col_expr`` require a scale and belong to the
data-pipeline milestone, so they are not ported here yet.
"""

import re

import pandas as pd
import pytest

from pysgl import SglError
from pysgl.cta import SglCta, SglCtaAvg


def test_is_an_sgl_cta_avg():
    assert isinstance(SglCtaAvg(), SglCtaAvg)
    assert isinstance(SglCtaAvg(), SglCta)


def test_sgl_func_name_returns_avg():
    assert SglCtaAvg().sgl_func_name() == "avg"


def test_valid_cta_raises_error_for_star():
    col_expr = {"column": "*", "cta": SglCtaAvg()}

    with pytest.raises(
        SglError,
        match=re.escape("Error: '*' cannot be used with the avg function."),
    ):
        SglCtaAvg().valid_cta(col_expr, pd.DataFrame())


def test_valid_cta_doesnt_raise_error_for_numerical_column(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "number", "cta": SglCtaAvg()}

    SglCtaAvg().valid_cta(col_expr, df)


def test_valid_cta_raises_error_for_temporal_column(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "day", "cta": SglCtaAvg()}

    with pytest.raises(
        SglError,
        match=re.escape(
            "Error: avg function can only be applied to numerical columns."
        ),
    ):
        SglCtaAvg().valid_cta(col_expr, df)


def test_valid_cta_raises_error_for_categorical_column(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "letter", "cta": SglCtaAvg()}

    with pytest.raises(
        SglError,
        match=re.escape(
            "Error: avg function can only be applied to numerical columns."
        ),
    ):
        SglCtaAvg().valid_cta(col_expr, df)


def test_valid_cta_doesnt_raise_error_for_no_arg(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "number", "cta": SglCtaAvg()}

    SglCtaAvg().valid_cta(col_expr, df)


def test_valid_cta_raises_error_for_arg(test_con):
    df = test_con.execute("select * from synth").df()
    col_expr = {"column": "number", "cta": SglCtaAvg(), "arg": 1}

    with pytest.raises(
        SglError,
        match=re.escape("Error: avg function received unexpected argument."),
    ):
        SglCtaAvg().valid_cta(col_expr, df)


def test_is_aggregation_returns_true():
    assert SglCtaAvg().is_aggregation() is True


def test_needs_scaling_returns_true():
    assert SglCtaAvg().needs_scaling() is True


def test_is_transformation_returns_false():
    assert SglCtaAvg().is_transformation() is False


def test_expr_text_returns_expr_for_avg_called_on_column():
    col_expr = {"column": "col_1", "cta": SglCtaAvg()}
    assert SglCtaAvg().expr_text(col_expr) == "avg(col_1)"
