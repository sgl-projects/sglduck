"""Tests for the case-insensitive column reference matching pass."""

import polars as pl

from sglduck.cta import SglCtaIdentity
from sglduck.match_col_casing import (
    col_has_match_in_df,
    facet_has_match_in_df,
    match_col_casing,
    match_col_casing_for_facet,
    match_col_casing_for_facets,
    match_col_casing_for_layer,
    match_col_casing_for_layers,
    match_col_to_df,
    match_cols_to_df,
    match_facet_to_df,
)
from sglduck.pgs import sgl_to_pgs


def _empty_df(*columns):
    return pl.DataFrame(schema=list(columns))


class TestColHasMatchInDf:
    df = _empty_df("CoL_1", "col_2")

    def test_returns_true_for_case_insensitive_match(self):
        col_expr = {"column": "col_1", "cta": SglCtaIdentity()}
        assert col_has_match_in_df(col_expr, self.df)

    def test_returns_false_for_no_case_insensitive_match(self):
        col_expr = {"column": "col_3", "cta": SglCtaIdentity()}
        assert not col_has_match_in_df(col_expr, self.df)


class TestFacetHasMatchInDf:
    df = _empty_df("CoL_1", "col_2")

    def test_returns_true_for_case_insensitive_match(self):
        facet_expr = {"column": "col_1", "direction": "default"}
        assert facet_has_match_in_df(facet_expr, self.df)

    def test_returns_false_for_no_case_insensitive_match(self):
        facet_expr = {"column": "col_3", "direction": "default"}
        assert not facet_has_match_in_df(facet_expr, self.df)


class TestMatchColToDf:
    df = _empty_df("CoL_1", "col_2")

    def test_matches_df_column_if_case_insensitive_match_found(self):
        col_expr = {"column": "col_1", "cta": SglCtaIdentity()}

        actual = match_col_to_df(col_expr, self.df)

        assert actual == {"column": "CoL_1", "cta": SglCtaIdentity()}

    def test_matches_first_column_for_multiple_matches(self):
        col_expr = {"column": "col_1", "cta": SglCtaIdentity()}
        test_df = _empty_df("CoL_1", "col_2", "col_1")

        actual = match_col_to_df(col_expr, test_df)

        assert actual == {"column": "CoL_1", "cta": SglCtaIdentity()}

    def test_returns_original_column_if_no_case_insensitive_match_found(self):
        col_expr = {"column": "col_3", "cta": SglCtaIdentity()}

        actual = match_col_to_df(col_expr, self.df)

        assert actual == col_expr


class TestMatchFacetToDf:
    def test_matches_first_df_column_match_found(self):
        df = _empty_df("CoL_1", "col_2", "col_1")
        facet_expr = {"column": "col_1", "direction": "default"}

        actual = match_facet_to_df(facet_expr, df)

        assert actual == {"column": "CoL_1", "direction": "default"}


class TestMatchColCasingForFacet:
    df_1 = _empty_df("col_1")
    df_2 = _empty_df("col_1", "CoL_2")
    df_3 = _empty_df("col_2", "col_3")
    dfs = [df_1, df_2, df_3]

    def test_matches_col_to_first_df_with_a_match(self):
        facet_expr = {"column": "col_2", "direction": "default"}

        actual = match_col_casing_for_facet(facet_expr, self.dfs)

        assert actual == {"column": "CoL_2", "direction": "default"}

    def test_returns_column_as_is_when_no_match(self):
        facet_expr = {"column": "not_a_match", "direction": "default"}

        actual = match_col_casing_for_facet(facet_expr, self.dfs)

        assert actual == facet_expr


class TestMatchColsToDf:
    df = _empty_df("CoL_1", "CoL_2", "col_3", "col_1")
    col_exprs = [
        {"column": "col_1", "cta": SglCtaIdentity()},
        {"column": "col_2", "cta": SglCtaIdentity()},
        {"column": "not_a_match", "cta": SglCtaIdentity()},
    ]
    matched_col_exprs = [
        {"column": "CoL_1", "cta": SglCtaIdentity()},
        {"column": "CoL_2", "cta": SglCtaIdentity()},
        {"column": "not_a_match", "cta": SglCtaIdentity()},
    ]

    def test_matches_df_casing_for_unnamed_col_exprs(self):
        actual = match_cols_to_df(self.col_exprs, self.df)

        assert actual == self.matched_col_exprs

    def test_matches_df_casing_for_named_col_exprs_and_preserves_keys(self):
        named_col_exprs = dict(zip(("x", "y", "color"), self.col_exprs))

        actual = match_cols_to_df(named_col_exprs, self.df)

        expected = dict(zip(("x", "y", "color"), self.matched_col_exprs))
        assert actual == expected


class TestMatchColCasingForLayer:
    df = _empty_df("CoL_1", "CoL_2", "col_3", "col_1")

    def test_matches_column_casing_for_each_clause(self):
        pgs = sgl_to_pgs("""
            visualize
                col_1 as x,
                col_2 as y,
                not_a_match as color
            from placeholder
            group by
                col_1,
                col_2,
                not_a_match
            collect by
                col_1,
                col_2,
                not_a_match
            using points
        """)
        layer = pgs["layers"][0]

        actual = match_col_casing_for_layer(layer, self.df)

        expected = sgl_to_pgs("""
            visualize
                CoL_1 as x,
                CoL_2 as y,
                not_a_match as color
            from placeholder
            group by
                CoL_1,
                CoL_2,
                not_a_match
            collect by
                CoL_1,
                CoL_2,
                not_a_match
            using points
        """)["layers"][0]

        assert actual == expected

    def test_ignores_grouping_and_collection_clauses_if_omitted(self):
        pgs = sgl_to_pgs("""
            visualize
                col_1 as x,
                col_2 as y,
                not_a_match as color
            from placeholder
            using points
        """)
        layer = pgs["layers"][0]

        actual = match_col_casing_for_layer(layer, self.df)

        expected = sgl_to_pgs("""
            visualize
                CoL_1 as x,
                CoL_2 as y,
                not_a_match as color
            from placeholder
            using points
        """)["layers"][0]

        assert actual == expected


class TestMatchColCasingForLayers:
    df_1 = _empty_df("CoL_1", "col_2")
    df_2 = _empty_df("CoL_3", "col_4")
    dfs = [df_1, df_2]

    def test_matches_column_casing_for_each_layer(self):
        pgs = sgl_to_pgs("""
            visualize
                col_1 as x,
                not_a_match as y
            from placeholder
            group by
                col_1,
                not_a_match
            collect by
                col_1,
                not_a_match
            using points

            layer

            visualize
                col_3 as x,
                not_a_match as y
            from placeholder
            group by
                col_3,
                not_a_match
            collect by
                col_3,
                not_a_match
            using points
        """)
        layers = pgs["layers"]

        actual = match_col_casing_for_layers(layers, self.dfs)

        expected = sgl_to_pgs("""
            visualize
                CoL_1 as x,
                not_a_match as y
            from placeholder
            group by
                CoL_1,
                not_a_match
            collect by
                CoL_1,
                not_a_match
            using points

            layer

            visualize
                CoL_3 as x,
                not_a_match as y
            from placeholder
            group by
                CoL_3,
                not_a_match
            collect by
                CoL_3,
                not_a_match
            using points
        """)["layers"]

        assert actual == expected


class TestMatchColCasingForFacets:
    df_1 = _empty_df("CoL_1", "col_2")
    df_2 = _empty_df("CoL_3", "col_4")
    dfs = [df_1, df_2]

    def test_matches_column_casing_for_each_facet(self):
        pgs = sgl_to_pgs("""
            visualize
                placeholder as x
            from placeholder
            using points
            facet by
                col_3 horizontally,
                not_a_match
        """)
        facets = pgs["facets"]

        actual = match_col_casing_for_facets(facets, self.dfs)

        expected = sgl_to_pgs("""
            visualize
                placeholder as x
            from placeholder
            using points
            facet by
                CoL_3 horizontally,
                not_a_match
        """)["facets"]

        assert actual == expected


class TestMatchColCasing:
    df_1 = _empty_df("CoL_1", "col_2")
    df_2 = _empty_df("CoL_3", "col_4")
    dfs = [df_1, df_2]

    def test_matches_column_casing_for_layers_and_facets(self):
        pgs = sgl_to_pgs("""
            visualize
                col_1 as x,
                not_a_match as y
            from placeholder
            group by
                col_1,
                not_a_match
            collect by
                col_1,
                not_a_match
            using points

            layer

            visualize
                col_3 as x,
                not_a_match as y
            from placeholder
            group by
                col_3,
                not_a_match
            collect by
                col_3,
                not_a_match
            using points

            facet by
                col_1 horizontally,
                not_a_match
        """)

        actual = match_col_casing(pgs, self.dfs)

        expected = sgl_to_pgs("""
            visualize
                CoL_1 as x,
                not_a_match as y
            from placeholder
            group by
                CoL_1,
                not_a_match
            collect by
                CoL_1,
                not_a_match
            using points

            layer

            visualize
                CoL_3 as x,
                not_a_match as y
            from placeholder
            group by
                CoL_3,
                not_a_match
            collect by
                CoL_3,
                not_a_match
            using points

            facet by
                CoL_1 horizontally,
                not_a_match
        """)

        assert actual == expected

    def test_ignores_facets_if_no_facet_by_clause(self):
        pgs = sgl_to_pgs("""
            visualize
                col_1 as x,
                not_a_match as y
            from placeholder
            using points
        """)
        test_dfs = [self.df_1]

        actual = match_col_casing(pgs, test_dfs)

        expected = sgl_to_pgs("""
            visualize
                CoL_1 as x,
                not_a_match as y
            from placeholder
            using points
        """)

        assert actual == expected
