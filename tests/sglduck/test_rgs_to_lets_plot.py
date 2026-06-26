"""Tests for rgs_to_lets_plot (port of test-rgs_to_ggplot2.R, Cartesian slice).

Covers the Cartesian default-qualifier, scale, and qualifier/orientation cases;
the facet, polar, and labs cases arrive with the follow-up rendering PRs that
implement those branches.
"""

import pytest

from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs
from sglduck.rgs_to_lets_plot import rgs_to_lets_plot

POINTS_STMT = """
    visualize
      hp as x,
      mpg as y
    from cars
    using points
"""


@pytest.fixture
def points_plot(test_con):
    pgs = sgl_to_pgs(POINTS_STMT)
    dfs = result_dfs(pgs, test_con)
    return rgs_to_lets_plot(pgs, dfs), dfs


def test_single_layer(points_plot):
    spec, _ = points_plot
    assert len(spec.as_dict()["layers"]) == 1


def test_top_level_mapping_is_empty(points_plot):
    spec, _ = points_plot
    assert spec.as_dict()["mapping"] == {}


def test_layer_aes_mapping(points_plot):
    spec, _ = points_plot
    layer = spec.as_dict()["layers"][0]
    assert layer["mapping"] == {"x": "hp", "y": "mpg"}


def test_layer_geom_is_point(points_plot):
    spec, _ = points_plot
    assert spec.as_dict()["layers"][0]["geom"] == "point"


def test_layer_has_identity_stat(points_plot):
    spec, _ = points_plot
    assert spec.as_dict()["layers"][0]["stat"] == "identity"


def test_layer_carries_its_dataframe(points_plot):
    spec, dfs = points_plot
    layer_data = spec.as_dict()["layers"][0]["data"]
    assert list(layer_data.columns) == list(dfs[0].columns)


def test_no_scales_without_a_scale_by_clause(points_plot):
    spec, _ = points_plot
    assert spec.as_dict()["scales"] == []


def test_scales_from_scale_by_clause(test_con):
    pgs = sgl_to_pgs(
        """
        visualize hp as x, mpg as y, cyl as color from cars using points
        scale by log(x), linear(color)
        """
    )
    dfs = result_dfs(pgs, test_con)
    scales = rgs_to_lets_plot(pgs, dfs).as_dict()["scales"]
    by_aes = {scale["aesthetic"]: scale for scale in scales}
    assert by_aes["x"]["trans"] == "log10"
    assert by_aes["color"]["trans"] == "identity"


def _first_layer_dict(con, sgl):
    pgs = sgl_to_pgs(sgl)
    dfs = result_dfs(pgs, con)
    return rgs_to_lets_plot(pgs, dfs).as_dict()["layers"][0]


def test_regression_qualifier_uses_smooth_lm_stat(test_con):
    layer = _first_layer_dict(
        test_con, "visualize hp as x, mpg as y from cars using regression line"
    )
    assert layer["stat"] == "smooth"
    assert layer["method"] == "lm"


def test_jittered_qualifier_uses_jitter_position(test_con):
    layer = _first_layer_dict(
        test_con, "visualize hp as x, mpg as y from cars using jittered points"
    )
    assert layer["position"] == "jitter"


def test_unstacked_qualifier_uses_identity_position(test_con):
    layer = _first_layer_dict(
        test_con,
        "visualize letter as x, number as y, boolean as color "
        "from synth using unstacked bars",
    )
    assert layer["position"] == "identity"


def test_box_geom_keeps_default_boxplot_stat(test_con):
    # lets-plot leaves the default boxplot stat implicit (no "stat" key); the
    # box geom must not be given a forced identity/smooth stat that overrides it.
    layer = _first_layer_dict(
        test_con, "visualize cut as x, price as y from diamonds using boxes"
    )
    assert "stat" not in layer


def test_no_orientation_when_geom_lacks_direction(test_con):
    layer = _first_layer_dict(
        test_con, "visualize hp as x, mpg as y from cars using points"
    )
    assert "orientation" not in layer


def test_orientation_present_when_geom_has_direction(test_con):
    layer = _first_layer_dict(
        test_con,
        "visualize bin(mpg) as y, count(*) as x from cars using horizontal bars",
    )
    assert layer["orientation"] == "y"
