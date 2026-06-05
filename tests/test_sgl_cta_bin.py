"""Port of rsgl's test-sgl_cta_bin.R (pure methods only).

``valid_cta`` and ``add_transformed_column`` require a DataFrame/scale and
belong to the validation and data-pipeline milestones, so they are not ported
here yet.
"""

from pysgl.cta import SglCta, SglCtaBin


def test_is_an_sgl_cta_bin():
    assert isinstance(SglCtaBin(), SglCtaBin)
    assert isinstance(SglCtaBin(), SglCta)


def test_cta_fn_name_returns_bin():
    assert SglCtaBin().cta_fn_name() == "bin"


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
