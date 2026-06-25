"""Binning helpers for the bin transformation CTA.

Ported from rsgl's ``sgl_cta_bin_utils.R``. Binning maps each value to the
centre of the bin it falls in: the (optionally scaled) data range is padded by a
small factor, split into ``bin_num`` equal-width bins, and each value is
replaced by its bin's centre, then mapped back through the scale's inverse.
"""

from __future__ import annotations

import numpy as np

_PADDING_FACTOR = 0.001


def bin_limits(input_data, bin_num: int) -> np.ndarray:
    """The ``bin_num + 1`` evenly spaced limits spanning the padded data range."""
    values = np.asarray(input_data, dtype=float)
    min_value = np.nanmin(values)
    max_value = np.nanmax(values)
    rng = max_value - min_value
    if rng == 0:
        padding = max_value * _PADDING_FACTOR
    else:
        padding = rng * _PADDING_FACTOR
    lowest = min_value - padding
    highest = max_value + padding
    return np.linspace(lowest, highest, bin_num + 1)


def bin_indices(input_data, limits) -> np.ndarray:
    """The 1-based index of the bin each value falls in (``NaN`` stays ``NaN``)."""
    values = np.asarray(input_data, dtype=float)
    limits = np.asarray(limits, dtype=float)
    indices = (values[:, None] >= limits[None, :]).sum(axis=1).astype(float)
    indices[np.isnan(values)] = np.nan
    return indices


def bin_centers(limits) -> np.ndarray:
    """The midpoint of each consecutive pair of bin limits."""
    limits = np.asarray(limits, dtype=float)
    lowers = limits[:-1]
    uppers = limits[1:]
    return (lowers + uppers) / 2


def bin_values(input_data, bin_num: int, scale) -> np.ndarray:
    """Replace each value with its bin centre, computed in the scaled space."""
    values = np.asarray(input_data, dtype=float)
    if np.all(np.isnan(values)):
        return values
    scaled = np.asarray(scale.apply_scale(values), dtype=float)
    limits = bin_limits(scaled, bin_num)
    centers = bin_centers(limits)
    indices = bin_indices(scaled, limits)
    binned = np.full(values.shape, np.nan)
    # An index outside 1..bin_num (only reachable for degenerate constant data)
    # has no centre; like R's out-of-range indexing it yields NaN.
    in_range = (indices >= 1) & (indices <= bin_num)
    binned[in_range] = centers[indices[in_range].astype(int) - 1]
    return np.asarray(scale.apply_scale_inverse(binned), dtype=float)
