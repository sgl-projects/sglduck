"""Tests for the SGL type classification helpers in ``types``."""

import datetime

import polars as pl
from polars.testing import assert_frame_equal
import pytest

from sglduck.pgs import sgl_to_pgs
from sglduck.types import (
    is_binned_mapping,
    is_categorical_col,
    is_categorical_mapping,
    is_date_col,
    is_date_mapping,
    is_numerical_col,
    is_numerical_mapping,
    is_temporal_col,
    is_temporal_mapping,
    is_timestamp_col,
    is_timestamp_mapping,
    type_classifications,
)


def df_with_supported_polars_types():
    df = pl.DataFrame(
        {
            "float_col": [1.2],
            "bool_col": [True],
            "date_col": [datetime.date(2025, 1, 1)],
            "int_col": [1],
            "timedelta_col": [datetime.timedelta(days=1)],
            "datetime_col": [datetime.datetime(2025, 1, 1, 0, 0, 0)],
            "str_col": ["1"],
            "category_col": ["a"],
        }
    ).with_columns(pl.col("category_col").cast(pl.Categorical))

    assert df["float_col"].dtype == pl.Float64
    assert df["bool_col"].dtype == pl.Boolean
    assert df["date_col"].dtype == pl.Date
    assert df["int_col"].dtype == pl.Int64
    assert df["timedelta_col"].dtype == pl.Duration
    assert df["datetime_col"].dtype == pl.Datetime
    assert df["str_col"].dtype == pl.String
    assert df["category_col"].dtype == pl.Categorical

    return df


def test_is_numerical_col_determines_whether_column_is_numerical():
    df = df_with_supported_polars_types()

    assert is_numerical_col(df["float_col"]) is True
    assert is_numerical_col(df["bool_col"]) is False
    assert is_numerical_col(df["date_col"]) is False
    assert is_numerical_col(df["int_col"]) is True
    assert is_numerical_col(df["timedelta_col"]) is True
    assert is_numerical_col(df["datetime_col"]) is False
    assert is_numerical_col(df["str_col"]) is False
    assert is_numerical_col(df["category_col"]) is False


def test_is_categorical_col_determines_whether_column_is_categorical():
    df = df_with_supported_polars_types()

    assert is_categorical_col(df["float_col"]) is False
    assert is_categorical_col(df["bool_col"]) is True
    assert is_categorical_col(df["date_col"]) is False
    assert is_categorical_col(df["int_col"]) is False
    assert is_categorical_col(df["timedelta_col"]) is False
    assert is_categorical_col(df["datetime_col"]) is False
    assert is_categorical_col(df["str_col"]) is True
    assert is_categorical_col(df["category_col"]) is True


def test_is_date_col_determines_whether_column_is_a_date():
    df = df_with_supported_polars_types()

    assert is_date_col(df["float_col"]) is False
    assert is_date_col(df["bool_col"]) is False
    assert is_date_col(df["date_col"]) is True
    assert is_date_col(df["int_col"]) is False
    assert is_date_col(df["timedelta_col"]) is False
    assert is_date_col(df["datetime_col"]) is False
    assert is_date_col(df["str_col"]) is False
    assert is_date_col(df["category_col"]) is False


def test_is_timestamp_col_determines_whether_column_is_a_timestamp():
    df = df_with_supported_polars_types()

    assert is_timestamp_col(df["float_col"]) is False
    assert is_timestamp_col(df["bool_col"]) is False
    assert is_timestamp_col(df["date_col"]) is False
    assert is_timestamp_col(df["int_col"]) is False
    assert is_timestamp_col(df["timedelta_col"]) is False
    assert is_timestamp_col(df["datetime_col"]) is True
    assert is_timestamp_col(df["str_col"]) is False
    assert is_timestamp_col(df["category_col"]) is False


def test_is_temporal_col_determines_whether_column_is_temporal():
    df = df_with_supported_polars_types()

    assert is_temporal_col(df["float_col"]) is False
    assert is_temporal_col(df["bool_col"]) is False
    assert is_temporal_col(df["date_col"]) is True
    assert is_temporal_col(df["int_col"]) is False
    assert is_temporal_col(df["timedelta_col"]) is False
    assert is_temporal_col(df["datetime_col"]) is True
    assert is_temporal_col(df["str_col"]) is False
    assert is_temporal_col(df["category_col"]) is False


def test_is_numerical_mapping_returns_true_for_count_star():
    df = df_with_supported_polars_types()
    pgs = sgl_to_pgs("""
        visualize
            bin(float_col) as x,
            count(*) as y
        from all_classes
        group by
            bin(float_col)
        using points
    """)

    assert is_numerical_mapping(pgs["layers"][0], df, "y") is True


def test_is_numerical_mapping_determines_whether_mapping_to_column_is_numerical():
    df = df_with_supported_polars_types()
    pgs = sgl_to_pgs("""
        visualize
            float_col as x,
            bool_col as y,
            date_col as color
        from all_classes
        using points
    """)

    assert is_numerical_mapping(pgs["layers"][0], df, "x") is True
    assert is_numerical_mapping(pgs["layers"][0], df, "y") is False
    assert is_numerical_mapping(pgs["layers"][0], df, "color") is False


def test_is_categorical_mapping_returns_false_for_count_star():
    df = df_with_supported_polars_types()
    pgs = sgl_to_pgs("""
        visualize
            bin(float_col) as x,
            count(*) as y
        from all_classes
        group by
            bin(float_col)
        using points
    """)

    assert is_categorical_mapping(pgs["layers"][0], df, "y") is False


def test_is_categorical_mapping_determines_whether_mapping_to_column_is_categorical():
    df = df_with_supported_polars_types()
    pgs = sgl_to_pgs("""
        visualize
            float_col as x,
            bool_col as y,
            date_col as color
        from all_classes
        using points
    """)

    assert is_categorical_mapping(pgs["layers"][0], df, "x") is False
    assert is_categorical_mapping(pgs["layers"][0], df, "y") is True
    assert is_categorical_mapping(pgs["layers"][0], df, "color") is False


def test_is_date_mapping_returns_false_for_count_star():
    df = df_with_supported_polars_types()
    pgs = sgl_to_pgs("""
        visualize
            bin(float_col) as x,
            count(*) as y
        from all_classes
        group by
            bin(float_col)
        using points
    """)

    assert is_date_mapping(pgs["layers"][0], df, "y") is False


def test_is_date_mapping_determines_whether_mapping_to_column_is_date():
    df = df_with_supported_polars_types()
    pgs = sgl_to_pgs("""
        visualize
            float_col as x,
            bool_col as y,
            date_col as color,
            datetime_col as size
        from all_classes
        using points
    """)

    assert is_date_mapping(pgs["layers"][0], df, "x") is False
    assert is_date_mapping(pgs["layers"][0], df, "y") is False
    assert is_date_mapping(pgs["layers"][0], df, "color") is True
    assert is_date_mapping(pgs["layers"][0], df, "size") is False


def test_is_timestamp_mapping_returns_false_for_count_star():
    df = df_with_supported_polars_types()
    pgs = sgl_to_pgs("""
        visualize
            bin(float_col) as x,
            count(*) as y
        from all_classes
        group by
            bin(float_col)
        using points
    """)

    assert is_timestamp_mapping(pgs["layers"][0], df, "y") is False


def test_is_timestamp_mapping_determines_whether_mapping_to_column_is_timestamp():
    df = df_with_supported_polars_types()
    pgs = sgl_to_pgs("""
        visualize
            float_col as x,
            bool_col as y,
            date_col as color,
            datetime_col as size
        from all_classes
        using points
    """)

    assert is_timestamp_mapping(pgs["layers"][0], df, "x") is False
    assert is_timestamp_mapping(pgs["layers"][0], df, "y") is False
    assert is_timestamp_mapping(pgs["layers"][0], df, "color") is False
    assert is_timestamp_mapping(pgs["layers"][0], df, "size") is True


def test_is_temporal_mapping_returns_false_for_count_star():
    df = df_with_supported_polars_types()
    pgs = sgl_to_pgs("""
        visualize
            bin(float_col) as x,
            count(*) as y
        from all_classes
        group by
            bin(float_col)
        using points
    """)

    assert is_temporal_mapping(pgs["layers"][0], df, "y") is False


def test_is_temporal_mapping_determines_whether_mapping_to_column_is_temporal():
    df = df_with_supported_polars_types()
    pgs = sgl_to_pgs("""
        visualize
            float_col as x,
            bool_col as y,
            date_col as color,
            datetime_col as size
        from all_classes
        using points
    """)

    assert is_temporal_mapping(pgs["layers"][0], df, "x") is False
    assert is_temporal_mapping(pgs["layers"][0], df, "y") is False
    assert is_temporal_mapping(pgs["layers"][0], df, "color") is True
    assert is_temporal_mapping(pgs["layers"][0], df, "size") is True


def test_is_binned_mapping_determines_whether_mapping_is_binned():
    pgs = sgl_to_pgs("""
        visualize
            bin(float_col) as x,
            count(*) as y,
            bool_col as color
        from all_classes
        group by
            bin(float_col),
            bool_col
        using bars
    """)

    layer = pgs["layers"][0]
    assert is_binned_mapping(layer, "x") is True
    assert is_binned_mapping(layer, "y") is False
    assert is_binned_mapping(layer, "color") is False


def test_mapping_checks_tolerate_a_dropped_source_column():
    # A binned mapping's source column is consumed by perform_ctas, so the
    # post-CTA frame no longer has it. The orientation type checks run against
    # that frame and must read the missing column as "no type" rather than
    # raising (rsgl relies on R returning NULL for the absent column).
    pgs = sgl_to_pgs("""
        visualize
            bin(float_col) as x,
            count(*) as y
        from all_classes
        group by
            bin(float_col)
        using bars
    """)
    layer = pgs["layers"][0]
    post_cta_df = pl.DataFrame(
        {"sglduck.linear.bin.30.float_col": [1.0], "sglduck.count": [5]}
    )

    assert is_numerical_mapping(layer, post_cta_df, "x") is False
    assert is_categorical_mapping(layer, post_cta_df, "x") is False
    assert is_date_mapping(layer, post_cta_df, "x") is False
    assert is_timestamp_mapping(layer, post_cta_df, "x") is False
    assert is_temporal_mapping(layer, post_cta_df, "x") is False


def test_type_classifications_raises_error_if_table_doesnt_exist(test_con):
    with pytest.raises(
        Exception, match="Table with name not_a_table does not exist"
    ):
        type_classifications(test_con, "not_a_table")


def test_type_classifications_returns_correct_classes_for_table_cols(test_con):
    # Cleanup is an explicit drop of the column rather than a transaction
    # rollback, keeping the test independent of DuckDB's transaction state.
    test_con.execute("alter table synth add column blob_col BLOB")
    try:
        actual = type_classifications(test_con, "synth")
    finally:
        test_con.execute("alter table synth drop column blob_col")

    expected = pl.DataFrame(
        {
            "column_name": [
                "letter", "number", "day",
                "day_and_time", "boolean", "blob_col",
            ],
            "column_class": [
                "categorical", "numerical", "temporal",
                "temporal", "categorical", "unknown",
            ],
        }
    )
    assert_frame_equal(actual, expected)


def test_type_classifications_handles_table_names_needing_quoting(test_con):
    test_con.execute('create table "weird-name" (a INTEGER, b VARCHAR)')
    test_con.execute("insert into \"weird-name\" values (1, 'x')")
    try:
        actual = type_classifications(test_con, "weird-name")
    finally:
        test_con.execute('drop table "weird-name"')

    expected = pl.DataFrame(
        {
            "column_name": ["a", "b"],
            "column_class": ["numerical", "categorical"],
        }
    )
    assert_frame_equal(actual, expected)
