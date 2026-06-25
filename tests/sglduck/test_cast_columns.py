"""Tests for the date/timestamp reconciliation helpers in ``cast_columns``."""

import pandas as pd

from sglduck.cast_columns import (
    aes_has_dt_and_ts,
    aes_with_dt_and_ts,
    cast_columns,
    cast_for_aes,
)
from sglduck.pgs import sgl_to_pgs
from sglduck.result_dfs import result_dfs


class TestAesHasDtAndTs:
    def test_single_layer_returns_false(self, test_con):
        pgs = sgl_to_pgs(
            """
            visualize day as x
            from synth
            using points
            """
        )
        dfs = result_dfs(pgs, test_con)

        assert aes_has_dt_and_ts("x", pgs["layers"], dfs) is False

    def test_aes_in_only_one_layer_returns_false(self, test_con):
        pgs = sgl_to_pgs(
            """
            visualize letter as x, number as y, day as color
            from synth
            using points

            layer

            visualize letter as x, number as y
            from synth
            using line
            """
        )
        dfs = result_dfs(pgs, test_con)

        assert aes_has_dt_and_ts("color", pgs["layers"], dfs) is False

    def test_non_temporal_mappings_return_false(self, test_con):
        pgs = sgl_to_pgs(
            """
            visualize letter as x
            from synth
            using points

            layer

            visualize boolean as x
            from synth
            using points
            """
        )
        dfs = result_dfs(pgs, test_con)

        assert aes_has_dt_and_ts("x", pgs["layers"], dfs) is False

    def test_both_dates_returns_false(self, test_con):
        pgs = sgl_to_pgs(
            """
            visualize day as x
            from synth
            using points

            layer

            visualize day as x
            from synth
            using points
            """
        )
        dfs = result_dfs(pgs, test_con)

        assert aes_has_dt_and_ts("x", pgs["layers"], dfs) is False

    def test_both_timestamps_returns_false(self, test_con):
        pgs = sgl_to_pgs(
            """
            visualize day_and_time as x
            from synth
            using points

            layer

            visualize day_and_time as x
            from synth
            using points
            """
        )
        dfs = result_dfs(pgs, test_con)

        assert aes_has_dt_and_ts("x", pgs["layers"], dfs) is False

    def test_date_and_timestamp_returns_true(self, test_con):
        pgs = sgl_to_pgs(
            """
            visualize day_and_time as x
            from synth
            using points

            layer

            visualize day as x
            from synth
            using points
            """
        )
        dfs = result_dfs(pgs, test_con)

        assert aes_has_dt_and_ts("x", pgs["layers"], dfs) is True


class TestAesWithDtAndTs:
    def test_no_aes_has_date_and_timestamp_returns_empty(self, test_con):
        pgs = sgl_to_pgs(
            """
            visualize letter as x, number as y
            from synth
            using points
            """
        )
        dfs = result_dfs(pgs, test_con)

        assert aes_with_dt_and_ts(pgs, dfs) == []

    def test_returns_aes_with_date_and_timestamp(self, test_con):
        pgs = sgl_to_pgs(
            """
            visualize
                letter as x,
                number as y,
                day as color,
                day_and_time as size
            from synth
            using points

            layer

            visualize
                letter as x,
                number as y,
                day_and_time as color,
                day as size
            from synth
            using points
            """
        )
        dfs = result_dfs(pgs, test_con)

        assert sorted(aes_with_dt_and_ts(pgs, dfs)) == ["color", "size"]


class TestCastForAes:
    THREE_LAYER_STMT = """
        visualize letter as x, number as y
        from synth
        using points

        layer

        visualize letter as x, number as y, day as color
        from synth
        using points

        layer

        visualize letter as x, number as y, day_and_time as color
        from synth
        using points
    """

    def test_returns_correct_number_of_dfs(self, test_con):
        pgs = sgl_to_pgs(self.THREE_LAYER_STMT)
        dfs = result_dfs(pgs, test_con)

        assert len(cast_for_aes("color", pgs["layers"], dfs)) == 3

    def test_layer_without_aes_unchanged(self, test_con):
        pgs = sgl_to_pgs(self.THREE_LAYER_STMT)
        dfs = result_dfs(pgs, test_con)

        actual = cast_for_aes("color", pgs["layers"], dfs)[0]

        pd.testing.assert_frame_equal(actual, dfs[0])

    def test_layer_with_date_is_cast(self, test_con):
        pgs = sgl_to_pgs(self.THREE_LAYER_STMT)
        dfs = result_dfs(pgs, test_con)

        actual = cast_for_aes("color", pgs["layers"], dfs)[1]

        expected = dfs[1].copy()
        expected["day"] = pd.to_datetime(expected["day"])
        pd.testing.assert_frame_equal(actual, expected)

    def test_layer_with_timestamp_unchanged(self, test_con):
        pgs = sgl_to_pgs(self.THREE_LAYER_STMT)
        dfs = result_dfs(pgs, test_con)

        actual = cast_for_aes("color", pgs["layers"], dfs)[2]

        pd.testing.assert_frame_equal(actual, dfs[2])


class TestCastColumns:
    def test_casts_dates_for_aes_with_date_and_timestamp(self, test_con):
        pgs = sgl_to_pgs(
            """
            visualize letter as x, number as y
            from synth
            using points

            layer

            visualize
                letter as x,
                number as y,
                day as color,
                day_and_time as size
            from synth
            using points

            layer

            visualize
                letter as x,
                number as y,
                day_and_time as color,
                day as size
            from synth
            using points
            """
        )
        dfs = result_dfs(pgs, test_con)

        actual = cast_columns(pgs, dfs)

        expected_2 = dfs[1].copy()
        expected_2["day"] = pd.to_datetime(expected_2["day"])
        expected_3 = dfs[2].copy()
        expected_3["day"] = pd.to_datetime(expected_3["day"])

        assert len(actual) == 3
        pd.testing.assert_frame_equal(actual[0], dfs[0])
        pd.testing.assert_frame_equal(actual[1], expected_2)
        pd.testing.assert_frame_equal(actual[2], expected_3)
