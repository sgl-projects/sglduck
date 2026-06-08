"""Tests for SglCtaCount (pure methods only).

``valid_cta``, ``agg_col_name`` and ``agg_col_expr`` are deferred to the
validation and data-pipeline milestones.
"""

from pysgl.cta import SglCta, SglCtaCount


def test_is_an_sgl_cta_count():
    assert isinstance(SglCtaCount(), SglCtaCount)
    assert isinstance(SglCtaCount(), SglCta)


def test_cta_fn_name_returns_count():
    assert SglCtaCount().cta_fn_name() == "count"


def test_is_aggregation_returns_true():
    assert SglCtaCount().is_aggregation() is True


def test_is_transformation_returns_false():
    assert SglCtaCount().is_transformation() is False


def test_needs_scaling_returns_false():
    assert SglCtaCount().needs_scaling() is False


def test_expr_text_returns_count_star():
    assert SglCtaCount().expr_text({}) == "count(*)"
