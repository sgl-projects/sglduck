"""Port of rsgl's test-sgl_cta_identity.R (pure methods only).

``valid_cta`` requires a DataFrame and is part of the validation milestone, so
it is not ported here yet.
"""

from pysgl.cta import SglCta, SglCtaIdentity


def test_is_an_sgl_cta_identity():
    assert isinstance(SglCtaIdentity(), SglCtaIdentity)
    assert isinstance(SglCtaIdentity(), SglCta)


def test_is_aggregation_returns_false():
    assert SglCtaIdentity().is_aggregation() is False


def test_is_transformation_returns_false():
    assert SglCtaIdentity().is_transformation() is False


def test_expr_text_returns_the_column_name():
    col_expr = {"column": "col_1", "cta": SglCtaIdentity()}
    assert SglCtaIdentity().expr_text(col_expr) == "col_1"
