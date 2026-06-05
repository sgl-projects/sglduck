"""Port of rsgl's tests/testthat/test-RcppExports.R.

Asserts the pgs contract produced by the C bridge + ``pgs.reconstruct_pgs``:
aes mappings, CTAs and their args, source SQL, geoms/quals, groupings,
collections, layer expansion and order, scales, facets, titles, and parser
error messages.
"""

import pytest

from pysgl.cta import SglCtaBin, SglCtaIdentity
from pysgl.geom import SglGeomBar, SglGeomBox, SglGeomLine, SglGeomPoint
from pysgl.pgs import sgl_to_pgs
from pysgl.scale import SglScaleLinear, SglScaleLog


def assert_raises_message(stmt, message):
    with pytest.raises(RuntimeError) as exc_info:
        sgl_to_pgs(stmt)
    assert str(exc_info.value) == message


def test_adds_single_aes_mapping():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using points
    """)

    aes_mappings = pgs["layers"][0]["aes_mappings"]
    actual_x_mapping = aes_mappings["x"]
    assert list(aes_mappings) == ["x"]
    assert set(actual_x_mapping) == {"column", "cta"}
    assert actual_x_mapping["column"] == "col_1"
    assert actual_x_mapping["cta"] == SglCtaIdentity()


def test_adds_multiple_aes_mappings():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
    """)

    aes_mappings = pgs["layers"][0]["aes_mappings"]
    actual_x_mapping = aes_mappings["x"]
    actual_y_mapping = aes_mappings["y"]
    assert set(aes_mappings) == {"x", "y"}
    assert actual_x_mapping["column"] == "col_1"
    assert actual_x_mapping["cta"] == SglCtaIdentity()
    assert actual_y_mapping["column"] == "col_2"
    assert actual_y_mapping["cta"] == SglCtaIdentity()


def test_adds_column_transformation():
    pgs = sgl_to_pgs("""
        visualize
            bin(col_1) as x
        from table_1
        using points
    """)

    actual_x_mapping = pgs["layers"][0]["aes_mappings"]["x"]
    assert set(actual_x_mapping) == {"column", "cta"}
    assert actual_x_mapping["column"] == "col_1"
    assert actual_x_mapping["cta"] == SglCtaBin()


def test_adds_aes_mapping_with_function_arg():
    pgs = sgl_to_pgs("""
        visualize
            bin(col_1, 5) as x
        from table_1
        using points
    """)

    actual_x_mapping = pgs["layers"][0]["aes_mappings"]["x"]
    assert set(actual_x_mapping) == {"column", "cta", "arg"}
    assert actual_x_mapping["column"] == "col_1"
    assert actual_x_mapping["cta"] == SglCtaBin()
    assert actual_x_mapping["arg"] == 5


def test_adds_source_sql_query_for_table_name():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using points
    """)

    assert pgs["layers"][0]["source_sql_query"] == "select * from table_1"


def test_adds_source_sql_query_for_subquery():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from (
            select *
            from table_1
            where col_2='a'
        )
        using points
    """)

    expected = """
            select *
            from table_1
            where col_2='a'
        """
    assert pgs["layers"][0]["source_sql_query"] == expected


def test_adds_point_geom():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using points
    """)

    geom_expr = pgs["layers"][0]["geom_expr"]
    assert geom_expr["geom"] == SglGeomPoint()
    assert geom_expr["qual"] == "default"


def test_adds_bar_geom():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using bars
    """)

    geom_expr = pgs["layers"][0]["geom_expr"]
    assert geom_expr["geom"] == SglGeomBar()
    assert geom_expr["qual"] == "default"


def test_adds_line_geom():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using line
    """)

    geom_expr = pgs["layers"][0]["geom_expr"]
    assert geom_expr["geom"] == SglGeomLine()
    assert geom_expr["qual"] == "default"


def test_adds_box_geom():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using box
    """)

    geom_expr = pgs["layers"][0]["geom_expr"]
    assert geom_expr["geom"] == SglGeomBox()
    assert geom_expr["qual"] == "default"


def test_adds_geom_with_qualifier():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using regression line
    """)

    geom_expr = pgs["layers"][0]["geom_expr"]
    assert geom_expr["geom"] == SglGeomLine()
    assert geom_expr["qual"] == "regression"


def test_doesnt_add_groupings_if_group_by_omitted():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using points
    """)

    assert "groupings" not in pgs["layers"][0]


def test_adds_grouping_for_single_column():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            count(*) as y
        from table_1
        group by
            col_1
        using points
    """)

    groupings = pgs["layers"][0]["groupings"]
    assert len(groupings) == 1
    grouping = groupings[0]
    assert set(grouping) == {"column", "cta"}
    assert grouping["column"] == "col_1"
    assert grouping["cta"] == SglCtaIdentity()


def test_adds_grouping_for_single_transformed_column():
    pgs = sgl_to_pgs("""
        visualize
            bin(col_1) as x,
            count(*) as y
        from table_1
        group by
            bin(col_1)
        using points
    """)

    groupings = pgs["layers"][0]["groupings"]
    assert len(groupings) == 1
    grouping = groupings[0]
    assert set(grouping) == {"column", "cta"}
    assert grouping["column"] == "col_1"
    assert grouping["cta"] == SglCtaBin()


def test_adds_grouping_with_function_arg():
    pgs = sgl_to_pgs("""
        visualize
            bin(col_1, 5) as x,
            count(*) as y
        from table_1
        group by
            bin(col_1, 5)
        using points
    """)

    groupings = pgs["layers"][0]["groupings"]
    assert len(groupings) == 1
    grouping = groupings[0]
    assert set(grouping) == {"column", "cta", "arg"}
    assert grouping["column"] == "col_1"
    assert grouping["cta"] == SglCtaBin()
    assert grouping["arg"] == 5


def test_adds_groupings_for_multiple_grouping_expressions():
    pgs = sgl_to_pgs("""
        visualize
            bin(col_1) as x,
            count(*) as y,
            col_2 as color
        from table_1
        group by
            bin(col_1),
            col_2
        using points
    """)

    groupings = pgs["layers"][0]["groupings"]
    assert len(groupings) == 2
    first_grouping = groupings[1]
    second_grouping = groupings[0]
    assert set(first_grouping) == {"column", "cta"}
    assert first_grouping["column"] == "col_1"
    assert first_grouping["cta"] == SglCtaBin()
    assert set(second_grouping) == {"column", "cta"}
    assert second_grouping["column"] == "col_2"
    assert second_grouping["cta"] == SglCtaIdentity()


def test_doesnt_add_collections_if_collect_by_omitted():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using points
    """)

    assert "collections" not in pgs["layers"][0]


def test_adds_collection_for_single_column():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        collect by
            col_3
        using lines
    """)

    collections = pgs["layers"][0]["collections"]
    assert len(collections) == 1
    collection = collections[0]
    assert set(collection) == {"column", "cta"}
    assert collection["column"] == "col_3"
    assert collection["cta"] == SglCtaIdentity()


def test_adds_collection_for_single_transformed_column():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        collect by
            bin(col_3)
        using lines
    """)

    collections = pgs["layers"][0]["collections"]
    assert len(collections) == 1
    collection = collections[0]
    assert set(collection) == {"column", "cta"}
    assert collection["column"] == "col_3"
    assert collection["cta"] == SglCtaBin()


def test_adds_collection_with_function_arg():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        collect by
            bin(col_3, 5)
        using lines
    """)

    collections = pgs["layers"][0]["collections"]
    assert len(collections) == 1
    collection = collections[0]
    assert set(collection) == {"column", "cta", "arg"}
    assert collection["column"] == "col_3"
    assert collection["cta"] == SglCtaBin()
    assert collection["arg"] == 5


def test_adds_collection_for_multiple_collection_expressions():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        collect by
            bin(col_3),
            col_4
        using lines
    """)

    collections = pgs["layers"][0]["collections"]
    assert len(collections) == 2
    first_collection = collections[1]
    second_collection = collections[0]
    assert set(first_collection) == {"column", "cta"}
    assert first_collection["column"] == "col_3"
    assert first_collection["cta"] == SglCtaBin()
    assert set(second_collection) == {"column", "cta"}
    assert second_collection["column"] == "col_4"
    assert second_collection["cta"] == SglCtaIdentity()


def test_adds_one_layer_for_single_layer():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using points
    """)

    assert len(pgs["layers"]) == 1


def test_adds_multiple_layers():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        group by
            col_1
        using points

        layer

        visualize
            col_2 as y
        from table_2
        collect by
            col_2
        using line
    """)

    first_layer = pgs["layers"][0]
    second_layer = pgs["layers"][1]

    assert len(pgs["layers"]) == 2
    assert first_layer["aes_mappings"]["x"]["column"] == "col_1"
    assert first_layer["source_sql_query"] == "select * from table_1"
    assert first_layer["geom_expr"]["geom"] == SglGeomPoint()
    assert first_layer["groupings"][0]["column"] == "col_1"
    assert "collections" not in first_layer
    assert second_layer["aes_mappings"]["y"]["column"] == "col_2"
    assert second_layer["source_sql_query"] == "select * from table_2"
    assert second_layer["geom_expr"]["geom"] == SglGeomLine()
    assert "groupings" not in second_layer
    assert second_layer["collections"][0]["column"] == "col_2"


def test_adds_multiple_layers_for_layered_geom_exprs():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using (
            points
            layer
            regression line
        )
    """)

    first_layer = pgs["layers"][0]
    second_layer = pgs["layers"][1]

    assert len(pgs["layers"]) == 2
    assert first_layer["aes_mappings"]["x"]["column"] == "col_1"
    assert first_layer["source_sql_query"] == "select * from table_1"
    assert first_layer["geom_expr"]["geom"] == SglGeomPoint()
    assert first_layer["geom_expr"]["qual"] == "default"
    assert second_layer["aes_mappings"]["x"]["column"] == "col_1"
    assert second_layer["source_sql_query"] == "select * from table_1"
    assert second_layer["geom_expr"]["geom"] == SglGeomLine()
    assert second_layer["geom_expr"]["qual"] == "regression"


def test_adds_multiple_layers_for_layered_geom_exprs_and_top_level_layer():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x
        from table_1
        using (
            points
            layer
            regression line
        )

        layer

        visualize
            col_2 as x
        from table_2
        using bars
    """)

    first_layer = pgs["layers"][0]
    second_layer = pgs["layers"][1]
    third_layer = pgs["layers"][2]

    assert len(pgs["layers"]) == 3
    assert first_layer["aes_mappings"]["x"]["column"] == "col_1"
    assert first_layer["source_sql_query"] == "select * from table_1"
    assert first_layer["geom_expr"]["geom"] == SglGeomPoint()
    assert first_layer["geom_expr"]["qual"] == "default"
    assert second_layer["aes_mappings"]["x"]["column"] == "col_1"
    assert second_layer["source_sql_query"] == "select * from table_1"
    assert second_layer["geom_expr"]["geom"] == SglGeomLine()
    assert second_layer["geom_expr"]["qual"] == "regression"
    assert third_layer["aes_mappings"]["x"]["column"] == "col_2"
    assert third_layer["source_sql_query"] == "select * from table_2"
    assert third_layer["geom_expr"]["geom"] == SglGeomBar()
    assert third_layer["geom_expr"]["qual"] == "default"


def test_doesnt_add_scale_if_none_provided():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
    """)

    assert "scales" not in pgs


def test_adds_single_scale():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        scale by
            log(x)
    """)

    assert list(pgs["scales"]) == ["x"]
    assert pgs["scales"]["x"] == SglScaleLog()


def test_adds_multiple_scales():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        scale by
            linear(x),
            log(y)
    """)

    assert set(pgs["scales"]) == {"x", "y"}
    assert pgs["scales"]["x"] == SglScaleLinear()
    assert pgs["scales"]["y"] == SglScaleLog()


def test_adds_scale_for_multiple_layers():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points

        layer

        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using regression line

        scale by
            log(x)
    """)

    assert list(pgs["scales"]) == ["x"]
    assert pgs["scales"]["x"] == SglScaleLog()


def test_doesnt_add_facet_if_none_provided():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
    """)

    assert "facets" not in pgs


def test_adds_facet_with_default_direction():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        facet by
            col_3
    """)

    facets = pgs["facets"]
    assert len(facets) == 1
    facet = facets[0]
    assert set(facet) == {"column", "direction"}
    assert facet["column"] == "col_3"
    assert facet["direction"] == "default"


def test_adds_facet_with_horizontal_direction():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        facet by
            col_3 horizontally
    """)

    facets = pgs["facets"]
    assert len(facets) == 1
    facet = facets[0]
    assert set(facet) == {"column", "direction"}
    assert facet["column"] == "col_3"
    assert facet["direction"] == "horizontal"


def test_adds_facet_with_vertical_direction():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        facet by
            col_3 vertically
    """)

    facets = pgs["facets"]
    assert len(facets) == 1
    facet = facets[0]
    assert set(facet) == {"column", "direction"}
    assert facet["column"] == "col_3"
    assert facet["direction"] == "vertical"


def test_adds_multiple_facets_correctly():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        facet by
            col_3,
            col_4 horizontally,
            col_5 vertically
    """)

    facets = pgs["facets"]
    assert len(facets) == 3
    first_facet = facets[2]
    second_facet = facets[1]
    third_facet = facets[0]
    assert set(first_facet) == {"column", "direction"}
    assert first_facet["column"] == "col_3"
    assert first_facet["direction"] == "default"
    assert set(second_facet) == {"column", "direction"}
    assert second_facet["column"] == "col_4"
    assert second_facet["direction"] == "horizontal"
    assert set(third_facet) == {"column", "direction"}
    assert third_facet["column"] == "col_5"
    assert third_facet["direction"] == "vertical"


def test_adds_facet_with_multiple_layers():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points

        layer

        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using regression line

        facet by
            col_3 horizontally
    """)

    facets = pgs["facets"]
    assert len(facets) == 1
    facet = facets[0]
    assert set(facet) == {"column", "direction"}
    assert facet["column"] == "col_3"
    assert facet["direction"] == "horizontal"


def test_doesnt_add_title_if_none_provided():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
    """)

    assert "titles" not in pgs


def test_adds_title():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        title
            x as 'Column 1'
    """)

    titles = pgs["titles"]
    assert list(titles) == ["x"]
    assert titles["x"] == "Column 1"


def test_adds_empty_string_as_title():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        title
            x as ''
    """)

    titles = pgs["titles"]
    assert list(titles) == ["x"]
    assert titles["x"] == ""


def test_allows_escaped_single_quote_in_title():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        title
            x as 'X\\'s Title'
    """)

    titles = pgs["titles"]
    assert list(titles) == ["x"]
    assert titles["x"] == "X's Title"


def test_adds_multiple_titles():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        title
            x as 'Column 1',
            y as 'Column 2'
    """)

    titles = pgs["titles"]
    assert set(titles) == {"x", "y"}
    assert titles["x"] == "Column 1"
    assert titles["y"] == "Column 2"


def test_adds_title_with_multiple_layers():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points

        layer

        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using regression line

        title
            x as 'Column 1'
    """)

    titles = pgs["titles"]
    assert list(titles) == ["x"]
    assert titles["x"] == "Column 1"


def test_adds_multiple_graphics_clauses():
    pgs = sgl_to_pgs("""
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        using points
        facet by
            col_3
        scale by
            log(x)
        title
            x as 'Column 1'
    """)

    facets = pgs["facets"]
    assert len(facets) == 1
    facet = facets[0]
    assert set(facet) == {"column", "direction"}
    assert facet["column"] == "col_3"
    assert facet["direction"] == "default"
    scales = pgs["scales"]
    assert list(scales) == ["x"]
    assert scales["x"] == SglScaleLog()
    titles = pgs["titles"]
    assert list(titles) == ["x"]
    assert titles["x"] == "Column 1"


def test_raises_error_for_invalid_aesthetic():
    assert_raises_message(
        """
        visualize
            col_1 as notanaes
        from table_1
        using points
        """,
        "Invalid aesthetic name: notanaes\n",
    )


def test_raises_error_for_invalid_geom():
    assert_raises_message(
        """
        visualize
            col_1 as x
        from table_1
        using notageom
        """,
        "Invalid geom name: notageom\n",
    )


def test_raises_error_for_invalid_qualifier():
    assert_raises_message(
        """
        visualize
            col_1 as x
        from table_1
        using notaqual points
        """,
        "Invalid geom qualifier: notaqual\n",
    )


def test_raises_error_for_invalid_geom_in_layered_geom_exprs():
    assert_raises_message(
        """
        visualize
            col_1 as x
        from table_1
        using (
            notageom
            layer
            points
        )
        """,
        "Invalid geom name: notageom\n",
    )


def test_raises_error_for_invalid_qualifier_in_layered_geom_exprs():
    assert_raises_message(
        """
        visualize
            col_1 as x
        from table_1
        using (
            notaqual points
            layer
            line
        )
        """,
        "Invalid geom qualifier: notaqual\n",
    )


def test_raises_error_for_invalid_cta():
    assert_raises_message(
        """
        visualize
            not_a_cta(col_1) as x
        from table_1
        using points
        """,
        "Invalid CTA: not_a_cta\n",
    )


def test_raises_error_for_invalid_cta_in_grouping_expression():
    assert_raises_message(
        """
        visualize
            col_1 as x
        from table_1
        group by
            not_a_cta(col_1)
        using points
        """,
        "Invalid CTA: not_a_cta\n",
    )


def test_raises_error_for_invalid_cta_in_collection_expression():
    assert_raises_message(
        """
        visualize
            col_1 as x,
            col_2 as y
        from table_1
        collect by
            not_a_cta(col_3)
        using points
        """,
        "Invalid CTA: not_a_cta\n",
    )


def test_raises_error_for_invalid_scale_type():
    assert_raises_message(
        """
        visualize
            col_1 as x
        from table_1
        using points
        scale by
            not_a_scale(x)
        """,
        "Invalid scale type: not_a_scale\n",
    )


def test_raises_error_for_invalid_scale_aes():
    assert_raises_message(
        """
        visualize
            col_1 as x
        from table_1
        using points
        scale by
            log(notanaes)
        """,
        "Invalid aesthetic name: notanaes\n",
    )


def test_raises_error_for_invalid_title_aes():
    assert_raises_message(
        """
        visualize
            col_1 as x
        from table_1
        using points
        title
            notanaes as 'Column 1'
        """,
        "Invalid aesthetic name: notanaes\n",
    )


def test_raises_error_for_unquoted_title():
    assert_raises_message(
        """
        visualize
            col_1 as x
        from table_1
        using points
        title
            notanaes as Column1
        """,
        "syntax error\n",
    )


def test_raises_error_for_general_syntax_error():
    assert_raises_message(
        """
        visualize
        from geom
        """,
        "syntax error\n",
    )
