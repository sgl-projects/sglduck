"""Tests for SglCtaCount.

``agg_col_name`` and ``agg_col_expr`` require a scale and belong to the
data-pipeline milestone, so they are not ported here yet.
"""

import re

import pandas as pd
import pytest

from pysgl import SglError
from pysgl.cta import SglCta, SglCtaCount


def test_is_an_sgl_cta_count():
    assert isinstance(SglCtaCount(), SglCtaCount)
    assert isinstance(SglCtaCount(), SglCta)


def test_sgl_func_name_returns_count():
    assert SglCtaCount().sgl_func_name() == "count"


def test_valid_cta_doesnt_raise_error_for_count_star():
    col_expr = {"column": "*", "cta": SglCtaCount()}

    SglCtaCount().valid_cta(col_expr, pd.DataFrame())


def test_valid_cta_raises_error_for_non_star_column():
    col_expr = {"column": "col_1", "cta": SglCtaCount()}

    with pytest.raises(
        SglError,
        match=re.escape(
            "Error: count can only be applied to *, found count(col_1)."
        ),
    ):
        SglCtaCount().valid_cta(col_expr, pd.DataFrame())


def test_valid_cta_doesnt_raise_error_for_no_arg():
    col_expr = {"column": "*", "cta": SglCtaCount()}

    SglCtaCount().valid_cta(col_expr, pd.DataFrame())


def test_valid_cta_raises_error_for_arg():
    col_expr = {"column": "*", "cta": SglCtaCount(), "arg": 5}

    with pytest.raises(
        SglError,
        match=re.escape("Error: count function received unexpected argument."),
    ):
        SglCtaCount().valid_cta(col_expr, pd.DataFrame())


def test_is_aggregation_returns_true():
    assert SglCtaCount().is_aggregation() is True


def test_is_transformation_returns_false():
    assert SglCtaCount().is_transformation() is False


def test_needs_scaling_returns_false():
    assert SglCtaCount().needs_scaling() is False


def test_expr_text_returns_count_star():
    assert SglCtaCount().expr_text({}) == "count(*)"
