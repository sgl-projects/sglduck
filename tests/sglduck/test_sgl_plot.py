"""Visual snapshot tests for SglPlot (port of test-sgl_plot.R's vdiffr suite).

Each statement renders through the full cast_columns -> perform_ctas ->
rgs_to_lets_plot pipeline to SVG, compared against a committed baseline under
``tests/baseline/`` (see the ``svg_snapshot`` fixture in conftest). Regenerate
the baselines with ``pytest --snapshot-update`` and review the diff.

These carry the ``snapshot`` marker and are a local visual-regression tool: the
baselines are platform-specific (lets-plot renders the same plot slightly
differently per OS), so CI excludes them (``pytest -m "not snapshot"``) and runs
the platform-stable suite instead. Regenerate on the platform you compare on.
"""

import pytest

from sglduck import db_get_plot

# Ported from rsgl's test-sgl_plot.R doppelganger statements.
_PLOTS = [
    ("scatterplot", "visualize hp as x, mpg as y from cars using points"),
    (
        "bar_chart",
        "visualize letter as x, number as y, boolean as color "
        "from synth using bars",
    ),
    (
        "unstacked_bar_chart",
        "visualize letter as x, number as y, boolean as color "
        "from synth using unstacked bars",
    ),
    ("line_chart", "visualize date as x, pop as y from economics using line"),
    (
        "line_chart_default_collection_on_color",
        "visualize hp as x, mpg as y, cyl as color from cars using lines",
    ),
    (
        "histogram",
        "visualize bin(mpg) as x, count(*) as y from cars "
        "group by bin(mpg) using bars",
    ),
    (
        "histogram_across_groups",
        "visualize bin(mpg) as x, count(*) as y, cyl_cat as color "
        "from (select *, cast(cyl as varchar) as cyl_cat from cars) "
        "group by bin(mpg), cyl_cat using bars",
    ),
    (
        "horizontal_bar_histogram_without_qualifier",
        "visualize bin(mpg) as y, count(*) as x from cars "
        "group by bin(mpg) using bars",
    ),
    (
        "line_plot_with_multiple_collective_lines",
        "visualize letter as x, number as y from synth "
        "collect by boolean using lines",
    ),
    ("boxplot", "visualize cut as x, price as y from diamonds using boxes"),
    (
        "boxplot_with_default_collection",
        "visualize bin(carat, 5) as x, price as y from diamonds using boxes",
    ),
    (
        "subquery_data_source",
        "visualize hp as x, mpg as y, cyl as color "
        "from (select hp, mpg, cyl::varchar as cyl from cars "
        "where cyl = 4 or cyl = 6) using points",
    ),
    ("jittered_points", "visualize boolean as x from synth using jittered points"),
    (
        "linear_regression_line_plot",
        "visualize hp as x, mpg as y, cyl as color from cars using regression lines",
    ),
    (
        "scatterplot_with_regression_line",
        "visualize hp as x, mpg as y from cars using points "
        "layer visualize hp as x, mpg as y from cars using regression line",
    ),
    (
        "plot_from_layered_geom_expressions",
        "visualize hp as x, mpg as y from cars using ( points layer regression line )",
    ),
    (
        "plot_with_date_and_timestamp_layered",
        "visualize day as x, number as y from synth using line "
        "layer visualize ts_col as x, number as y from ("
        "select cast(day + interval '10 years' as timestamp) as ts_col, number "
        "from synth) using line",
    ),
    (
        "plot_with_log_scales",
        "visualize hp as x, mpg as y from cars using ( points layer regression line ) "
        "scale by log(x), log(y)",
    ),
    (
        "plot_with_ln_scales",
        "visualize hp as x, mpg as y from cars using ( points layer regression line ) "
        "scale by ln(x), ln(y)",
    ),
    (
        "bar_chart_in_polar_coordinates",
        "visualize letter as theta, number as r, boolean as color "
        "from synth using bars",
    ),
    (
        "pie_chart",
        "visualize count(*) as theta, cut as color from diamonds "
        "group by cut using bars",
    ),
    ("one_dimensional_point_plot", "visualize mpg as x from cars using points"),
    (
        "scatterplot_with_size_aesthetic",
        "visualize hp as x, mpg as y, cyl as size from cars using points",
    ),
    (
        "histogram_with_horizontal_bars",
        "visualize bin(mpg) as y, count(*) as x from cars "
        "group by bin(mpg) using horizontal bars",
    ),
    (
        "histogram_with_non_default_num_bins",
        "visualize bin(mpg, 10) as x, count(*) as y from cars "
        "group by bin(mpg, 10) using bars",
    ),
    (
        "bar_chart_avg_log_hp_per_cyl",
        "visualize cyl as x, avg(hp) as y from cars group by cyl using bars "
        "scale by log(y)",
    ),
    (
        "faceted_scatterplot",
        "visualize hp as x, mpg as y from cars using points facet by cyl",
    ),
    (
        "plot_with_explicit_titles",
        "visualize hp as x, mpg as y, cyl as color from cars using points "
        "title x as 'Horsepower', y as 'Miles Per Gallon', color as 'Cylinders'",
    ),
    (
        "case_insensitive_plot",
        "VisualiZe Hp aS X, mPG As y FrOM cars usinG PoiNts FaCEt By CyL",
    ),
]

@pytest.mark.snapshot
@pytest.mark.parametrize("name,stmt", [pytest.param(n, s, id=n) for n, s in _PLOTS])
def test_plot_matches_snapshot(test_con, svg_snapshot, name, stmt):
    svg_snapshot.assert_match(name, db_get_plot(test_con, stmt).to_svg())


def test_renders_html(test_con):
    html = db_get_plot(
        test_con, "visualize hp as x, mpg as y from cars using points"
    ).to_html()
    assert "<html" in html.lower() or "<div" in html.lower()
