"""Tests for the binning helpers (port of test-sgl_cta_bin_utils.R)."""

import numpy as np

from pysgl.cta.bin_utils import bin_centers, bin_indices, bin_limits, bin_values
from pysgl.scale import SglScaleLinear, SglScaleLog


def _allclose(actual, expected):
    np.testing.assert_allclose(
        np.asarray(actual, dtype=float),
        np.asarray(expected, dtype=float),
        equal_nan=True,
    )


class TestSuite1Basic:
    input_data = np.arange(0, 11)
    bin_num = 5
    scale = SglScaleLinear()
    expected_bin_limits = [-0.010, 1.994, 3.998, 6.002, 8.006, 10.010]
    expected_bin_indices = [1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5]
    expected_bin_centers = [0.992, 2.996, 5, 7.004, 9.008]
    expected_bin_values = [
        0.992, 0.992, 2.996, 2.996, 5, 5, 5, 7.004, 7.004, 9.008, 9.008
    ]

    def test_bin_limits(self):
        _allclose(bin_limits(self.input_data, self.bin_num), self.expected_bin_limits)

    def test_bin_indices(self):
        _allclose(
            bin_indices(self.input_data, self.expected_bin_limits),
            self.expected_bin_indices,
        )

    def test_bin_centers(self):
        _allclose(bin_centers(self.expected_bin_limits), self.expected_bin_centers)

    def test_bin_values(self):
        _allclose(
            bin_values(self.input_data, self.bin_num, self.scale),
            self.expected_bin_values,
        )


class TestSuite2MinEqualsMax:
    input_data = np.array([10])
    bin_num = 5
    scale = SglScaleLinear()
    expected_bin_limits = [9.990, 9.994, 9.998, 10.002, 10.006, 10.010]
    expected_bin_indices = [3]
    expected_bin_centers = [9.992, 9.996, 10.000, 10.004, 10.008]
    expected_bin_values = [10]

    def test_bin_limits(self):
        _allclose(bin_limits(self.input_data, self.bin_num), self.expected_bin_limits)

    def test_bin_indices(self):
        _allclose(
            bin_indices(self.input_data, self.expected_bin_limits),
            self.expected_bin_indices,
        )

    def test_bin_centers(self):
        _allclose(bin_centers(self.expected_bin_limits), self.expected_bin_centers)

    def test_bin_values(self):
        _allclose(
            bin_values(self.input_data, self.bin_num, self.scale),
            self.expected_bin_values,
        )


class TestSuite3SingleBin:
    input_data = np.arange(0, 11)
    bin_num = 1
    scale = SglScaleLinear()
    expected_bin_limits = [-0.010, 10.010]
    expected_bin_indices = [1] * 11
    expected_bin_centers = [5]
    expected_bin_values = [5] * 11

    def test_bin_limits(self):
        _allclose(bin_limits(self.input_data, self.bin_num), self.expected_bin_limits)

    def test_bin_indices(self):
        _allclose(
            bin_indices(self.input_data, self.expected_bin_limits),
            self.expected_bin_indices,
        )

    def test_bin_centers(self):
        _allclose(bin_centers(self.expected_bin_limits), self.expected_bin_centers)

    def test_bin_values(self):
        _allclose(
            bin_values(self.input_data, self.bin_num, self.scale),
            self.expected_bin_values,
        )


class TestSuite4MissingValues:
    input_data = np.array([np.nan, 1, 2, 3, 4, np.nan])
    bin_num = 2
    scale = SglScaleLinear()
    expected_bin_limits = [0.997, 2.5, 4.003]
    expected_bin_indices = [np.nan, 1, 1, 2, 2, np.nan]
    expected_bin_centers = [1.7485, 3.2515]
    expected_bin_values = [np.nan, 1.7485, 1.7485, 3.2515, 3.2515, np.nan]

    def test_bin_limits(self):
        _allclose(bin_limits(self.input_data, self.bin_num), self.expected_bin_limits)

    def test_bin_indices(self):
        _allclose(
            bin_indices(self.input_data, self.expected_bin_limits),
            self.expected_bin_indices,
        )

    def test_bin_centers(self):
        _allclose(bin_centers(self.expected_bin_limits), self.expected_bin_centers)

    def test_bin_values(self):
        _allclose(
            bin_values(self.input_data, self.bin_num, self.scale),
            self.expected_bin_values,
        )


class TestSuite5AllMissing:
    input_data = np.full(5, np.nan)
    bin_num = 5
    scale = SglScaleLinear()

    def test_bin_values_returns_all_na(self):
        _allclose(
            bin_values(self.input_data, self.bin_num, self.scale), self.input_data
        )


class TestSuite6NonLinearScale:
    input_data = np.power(10.0, np.arange(0, 11))
    bin_num = 5
    scale = SglScaleLog()
    scaled_input_data = np.arange(0, 11)
    expected_bin_limits = [-0.010, 1.994, 3.998, 6.002, 8.006, 10.010]
    expected_bin_indices = [1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5]
    expected_bin_centers = [0.992, 2.996, 5, 7.004, 9.008]
    expected_bin_values = np.power(
        10.0, [0.992, 0.992, 2.996, 2.996, 5, 5, 5, 7.004, 7.004, 9.008, 9.008]
    )

    def test_bin_limits(self):
        _allclose(
            bin_limits(self.scaled_input_data, self.bin_num), self.expected_bin_limits
        )

    def test_bin_indices(self):
        _allclose(
            bin_indices(self.scaled_input_data, self.expected_bin_limits),
            self.expected_bin_indices,
        )

    def test_bin_centers(self):
        _allclose(bin_centers(self.expected_bin_limits), self.expected_bin_centers)

    def test_bin_values(self):
        _allclose(
            bin_values(self.input_data, self.bin_num, self.scale),
            self.expected_bin_values,
        )
