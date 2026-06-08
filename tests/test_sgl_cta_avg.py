"""Tests for SglCtaAvg (pure methods only).

``valid_cta``, ``agg_col_name`` and ``agg_col_expr`` require a DataFrame/scale
and belong to the validation and data-pipeline milestones, so they are not
ported here yet.
"""

from pysgl.cta import SglCta, SglCtaAvg


def test_is_an_sgl_cta_avg():
    assert isinstance(SglCtaAvg(), SglCtaAvg)
    assert isinstance(SglCtaAvg(), SglCta)


def test_cta_fn_name_returns_avg():
    assert SglCtaAvg().cta_fn_name() == "avg"


def test_is_aggregation_returns_true():
    assert SglCtaAvg().is_aggregation() is True


def test_needs_scaling_returns_true():
    assert SglCtaAvg().needs_scaling() is True


def test_is_transformation_returns_false():
    assert SglCtaAvg().is_transformation() is False


def test_expr_text_returns_expr_for_avg_called_on_column():
    col_expr = {"column": "col_1", "cta": SglCtaAvg()}
    assert SglCtaAvg().expr_text(col_expr) == "avg(col_1)"
