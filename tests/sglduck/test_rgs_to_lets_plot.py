"""Tests for rgs_to_lets_plot (port of test-rgs_to_ggplot2.R).

Covers the default-qualifier, scale, qualifier/orientation, facet, and polar
coordinate cases; the labs cases arrive with a follow-up rendering PR.
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
    # the jitter is seeded so the plot renders reproducibly
    assert layer["position"] == {"name": "jitter", "seed": 0}


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


def _facet(con, sgl):
    pgs = sgl_to_pgs(sgl)
    dfs = result_dfs(pgs, con)
    return rgs_to_lets_plot(pgs, dfs).as_dict().get("facet")


_FACET_BASE = "visualize letter as x, number as y from synth using points facet by "


def test_no_facet_without_facet_by_clause(test_con):
    stmt = "visualize letter as x, number as y from synth using points"
    assert _facet(test_con, stmt) is None


def test_single_default_facet_is_a_column(test_con):
    facet = _facet(test_con, _FACET_BASE + "boolean")
    assert facet["x"] == "boolean"
    assert "y" not in facet


def test_single_horizontal_facet_is_a_column(test_con):
    facet = _facet(test_con, _FACET_BASE + "boolean horizontally")
    assert facet["x"] == "boolean"
    assert "y" not in facet


def test_single_vertical_facet_is_a_row(test_con):
    facet = _facet(test_con, _FACET_BASE + "boolean vertically")
    assert facet["y"] == "boolean"
    assert "x" not in facet


# For two facets, "x" holds the horizontal (column) facet and "y" the vertical
# (row) facet. The cases mirror test-rgs_to_ggplot2.R.
@pytest.mark.parametrize(
    "facet_clause,expected_x,expected_y",
    [
        ("letter, boolean", "letter", "boolean"),
        ("letter, boolean horizontally", "boolean", "letter"),
        ("letter, boolean vertically", "letter", "boolean"),
        ("letter horizontally, boolean vertically", "letter", "boolean"),
        ("letter vertically, boolean horizontally", "boolean", "letter"),
    ],
)
def test_two_facets_fill_columns_and_rows(
    test_con, facet_clause, expected_x, expected_y
):
    facet = _facet(test_con, _FACET_BASE + facet_clause)
    assert facet["x"] == expected_x
    assert facet["y"] == expected_y


def test_bar_color_aesthetic_maps_to_fill(test_con):
    # bars colour their interior, so color maps onto fill, not the stroke
    layer = _first_layer_dict(
        test_con,
        "visualize letter as x, number as y, boolean as color "
        "from synth using bars",
    )
    assert layer["mapping"].get("fill") == "boolean"
    assert "color" not in layer["mapping"]


def test_non_bar_color_aesthetic_maps_to_color(test_con):
    layer = _first_layer_dict(
        test_con,
        "visualize hp as x, mpg as y, cyl as color from cars using points",
    )
    assert layer["mapping"].get("color") == "cyl"
    assert "fill" not in layer["mapping"]


def test_line_collects_by_its_color(test_con):
    layer = _first_layer_dict(
        test_con, "visualize hp as x, mpg as y, cyl as color from cars using lines"
    )
    assert layer["mapping"]["group"] == ["cyl"]


def test_collect_by_clause_sets_the_group(test_con):
    layer = _first_layer_dict(
        test_con,
        "visualize letter as x, number as y from synth "
        "collect by boolean using lines",
    )
    assert layer["mapping"]["group"] == ["boolean"]


def test_box_collects_by_its_category(test_con):
    layer = _first_layer_dict(
        test_con, "visualize cut as x, price as y from diamonds using boxes"
    )
    assert layer["mapping"]["group"] == ["cut"]


def test_plain_line_has_no_group(test_con):
    layer = _first_layer_dict(
        test_con, "visualize date as x, pop as y from economics using line"
    )
    assert "group" not in layer["mapping"]


def test_multi_column_collection_groups_by_all_columns(test_con):
    # lets-plot's group aesthetic takes a list and groups by the combination
    layer = _first_layer_dict(
        test_con,
        "visualize letter as x, number as y from synth "
        "collect by boolean, day using lines",
    )
    assert set(layer["mapping"]["group"]) == {"boolean", "day"}


POLAR_STMT = "visualize hp as theta, mpg as r from cars using points"


def _spec(con, sgl):
    pgs = sgl_to_pgs(sgl)
    dfs = result_dfs(pgs, con)
    return rgs_to_lets_plot(pgs, dfs).as_dict()


def test_no_polar_coordinates_without_theta(test_con):
    assert _spec(test_con, POINTS_STMT).get("coord") is None


def test_polar_coordinates_for_theta_and_r(test_con):
    assert _spec(test_con, POLAR_STMT)["coord"]["name"] == "polar"


def test_theta_and_r_map_to_x_and_y_in_polar_coordinates(test_con):
    spec = _spec(test_con, POLAR_STMT)
    assert spec["coord"]["theta"] == "x"
    assert spec["layers"][0]["mapping"] == {"x": "hp", "y": "mpg"}


def test_polar_coordinates_with_multiple_layers(test_con):
    spec = _spec(
        test_con,
        "visualize hp as theta, mpg as r from cars using points "
        "layer "
        "visualize hp as theta, mpg as r from cars using regression line",
    )
    assert spec["coord"]["name"] == "polar"
    assert spec["coord"]["theta"] == "x"
    for layer in spec["layers"]:
        assert layer["mapping"]["x"] == "hp"
        assert layer["mapping"]["y"] == "mpg"


@pytest.mark.parametrize(
    "stmt,blank_axis,mapped_axis",
    [
        ("visualize mpg as x from cars using boxes", "y", "x"),
        ("visualize mpg as y from cars using boxes", "x", "y"),
    ],
)
def test_unmapped_positional_axis_is_blanked(test_con, stmt, blank_axis, mapped_axis):
    spec = _spec(test_con, stmt)
    layer = spec["layers"][0]
    assert layer["mapping"][blank_axis] == "sglduck.blank"
    assert layer["mapping"][mapped_axis] == "mpg"
    assert spec["theme"][f"axis_ticks_{blank_axis}"] == {"blank": True}


def test_two_aes_plot_has_no_blank_axis(test_con):
    spec = _spec(test_con, POINTS_STMT)
    assert "sglduck.blank" not in spec["layers"][0]["mapping"].values()
    assert spec.get("theme") is None
