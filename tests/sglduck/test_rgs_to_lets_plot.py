"""Tests for rgs_to_lets_plot (port of test-rgs_to_ggplot2.R, Cartesian slice).

Only the default-qualifier Cartesian cases are ported here; the scale, facet,
polar, labs, and qualifier/orientation cases arrive with the follow-up rendering
PRs that implement those branches.
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
