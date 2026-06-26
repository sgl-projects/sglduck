"""Render tests for SglPlot (slice of test-sgl_plot.R).

rsgl uses vdiffr SVG snapshot baselines; choosing and wiring up an equivalent
lets-plot snapshot tool is a follow-up (plan section 14). For now these are
smoke tests: a SglPlot renders to non-empty SVG/HTML through the full
cast_columns -> perform_ctas -> rgs_to_lets_plot pipeline.
"""

import pytest

from sglduck import db_get_plot

SCATTERPLOT_STMT = """
    visualize
      hp as x,
      mpg as y
    from cars
    using points
"""


def test_renders_svg(test_con):
    svg = db_get_plot(test_con, SCATTERPLOT_STMT).to_svg()
    assert "<svg" in svg


def test_renders_html(test_con):
    html = db_get_plot(test_con, SCATTERPLOT_STMT).to_html()
    assert "<html" in html.lower() or "<div" in html.lower()


# Render the qualifier/orientation branches through the full
# cast_columns -> perform_ctas -> rgs_to_lets_plot pipeline (the post-CTA data
# path the rgs_to_lets_plot as_dict tests don't exercise).
@pytest.mark.parametrize(
    "stmt",
    [
        "visualize hp as x, mpg as y from cars using regression line",
        "visualize hp as x, mpg as y from cars using jittered points",
        "visualize bin(mpg) as y, count(*) as x from cars "
        "group by bin(mpg) using horizontal bars",
        "visualize cyl as x, mpg as y from cars collect by cyl "
        "using vertical boxes",
    ],
)
def test_qualifier_statements_render_svg(test_con, stmt):
    assert "<svg" in db_get_plot(test_con, stmt).to_svg()


@pytest.mark.parametrize(
    "stmt",
    [
        "visualize letter as x, number as y from synth using points "
        "facet by boolean",
        "visualize letter as x, number as y from synth using points "
        "facet by boolean vertically",
        "visualize day as x, number as y from synth using points "
        "facet by letter, boolean",
    ],
)
def test_faceted_statements_render_svg(test_con, stmt):
    assert "<svg" in db_get_plot(test_con, stmt).to_svg()


@pytest.mark.parametrize(
    "stmt",
    [
        "visualize hp as theta, mpg as r from cars using points",
        "visualize letter as theta, number as r, boolean as color "
        "from synth using bars",
    ],
)
def test_polar_statements_render_svg(test_con, stmt):
    assert "<svg" in db_get_plot(test_con, stmt).to_svg()


# Single-positional-aesthetic plots: the unmapped axis is pinned to a constant
# blank column (a pie chart from a theta-only mapping, a single boxplot).
@pytest.mark.parametrize(
    "stmt",
    [
        "visualize count(*) as theta, cut as color from diamonds "
        "group by cut using bars",
        "visualize mpg as x from cars using boxes",
    ],
)
def test_single_positional_aesthetic_statements_render_svg(test_con, stmt):
    assert "<svg" in db_get_plot(test_con, stmt).to_svg()


# Direction-aware geoms (bars) with binned/aggregated mappings: computing geom
# orientation must not crash on a source column that perform_ctas consumed
# (e.g. bin(mpg), avg(hp) — the column is gone from the post-CTA frame).
@pytest.mark.parametrize(
    "stmt",
    [
        "visualize bin(mpg) as x, count(*) as y from cars "
        "group by bin(mpg) using bars",
        "visualize bin(mpg) as y, count(*) as x from cars "
        "group by bin(mpg) using bars",
        "visualize bin(mpg, 10) as x, count(*) as y from cars "
        "group by bin(mpg, 10) using bars",
        "visualize cyl as x, avg(hp) as y from cars group by cyl using bars",
    ],
)
def test_binned_and_aggregated_bar_charts_render_svg(test_con, stmt):
    assert "<svg" in db_get_plot(test_con, stmt).to_svg()
