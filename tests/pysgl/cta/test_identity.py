"""Tests for SglCtaIdentity."""

import re

import pandas as pd
import pytest

from pysgl import SglError
from pysgl.cta import SglCta, SglCtaIdentity


@pytest.fixture
def df():
    return pd.DataFrame()


def test_is_an_sgl_cta_identity():
    assert isinstance(SglCtaIdentity(), SglCtaIdentity)
    assert isinstance(SglCtaIdentity(), SglCta)


def test_valid_cta_raises_error_for_star(df):
    col_expr = {"column": "*", "cta": SglCtaIdentity()}

    with pytest.raises(
        SglError,
        match=re.escape("Error: '*' can only be used inside an aggregation function"),
    ):
        SglCtaIdentity().valid_cta(col_expr, df)


def test_valid_cta_doesnt_raise_error_for_non_star_column(df):
    col_expr = {"column": "col", "cta": SglCtaIdentity()}

    SglCtaIdentity().valid_cta(col_expr, df)


def test_is_aggregation_returns_false():
    assert SglCtaIdentity().is_aggregation() is False


def test_is_transformation_returns_false():
    assert SglCtaIdentity().is_transformation() is False


def test_expr_text_returns_the_column_name():
    col_expr = {"column": "col_1", "cta": SglCtaIdentity()}
    assert SglCtaIdentity().expr_text(col_expr) == "col_1"
