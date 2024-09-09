"""Unit tests for vect.py module."""

"""Copyright (C) 2023 Edward West. All rights reserved.

This code is licensed under Apache 2.0 with Commons Clause license
(see LICENSE for details).
"""

import numpy as np
import pytest
import re
from pybroker.vect import cross, highv, lowv, returnv, sumv


@pytest.mark.parametrize(
    "array, n, expected",
    [
        ([3, 3, 4, 2, 5, 6, 1, 3], 3, [np.nan, np.nan, 3, 2, 2, 2, 1, 1]),
        ([3, 3, 4, 2, 5, 6, 1, 3], 1, [3, 3, 4, 2, 5, 6, 1, 3]),
        ([4, 3, 2, 1], 4, [np.nan, np.nan, np.nan, 1]),
        ([1], 1, [1]),
        ([], 5, []),
    ],
)
def test_lowv(array, n, expected):
    assert np.array_equal(lowv(np.array(array), n), expected, equal_nan=True)


@pytest.mark.parametrize(
    "array, n, expected",
    [
        ([3, 3, 4, 2, 5, 6, 1, 3], 3, [np.nan, np.nan, 4, 4, 5, 6, 6, 6]),
        ([3, 3, 4, 2, 5, 6, 1, 3], 1, [3, 3, 4, 2, 5, 6, 1, 3]),
        ([4, 3, 2, 1], 4, [np.nan, np.nan, np.nan, 4]),
        ([1], 1, [1]),
        ([], 5, []),
    ],
)
def test_highv(array, n, expected):
    assert np.array_equal(highv(np.array(array), n), expected, equal_nan=True)


@pytest.mark.parametrize(
    "array, n, expected",
    [
        ([3, 3, 4, 2, 5, 6, 1, 3], 3, [np.nan, np.nan, 10, 9, 11, 13, 12, 10]),
        ([3, 3, 4, 2, 5, 6, 1, 3], 1, [3, 3, 4, 2, 5, 6, 1, 3]),
        ([4, 3, 2, 1], 4, [np.nan, np.nan, np.nan, 10]),
        ([1], 1, [1]),
        ([], 5, []),
    ],
)
def test_sumv(array, n, expected):
    assert np.array_equal(sumv(np.array(array), n), expected, equal_nan=True)


@pytest.mark.parametrize(
    "array, n, expected",
    [
        (
            [1, 1.5, 1.7, 1.3, 1.2, 1.4],
            1,
            [np.nan, 0.5, 0.13333333, -0.23529412, -0.07692308, 0.16666667],
        ),
        (
            [1, 1.5, 1.7, 1.3, 1.2, 1.4],
            2,
            [np.nan, np.nan, 0.7, -0.133333, -0.294118, 0.076923],
        ),
        ([1], 1, [np.nan]),
        ([], 5, []),
    ],
)
def test_returnv(array, n, expected):
    assert np.array_equal(
        np.round(returnv(np.array(array), n), 6),
        np.round(expected, 6),
        equal_nan=True,
    )


@pytest.mark.parametrize("fnv", [lowv, highv, sumv, returnv])
@pytest.mark.parametrize(
    "array, n, expected_msg",
    [
        ([1, 2, 3], 10, "n is greater than array length."),
        ([1, 2, 3], 0, "n needs to be >= 1."),
        ([1, 2, 3], -1, "n needs to be >= 1."),
    ],
)
def test_when_n_invalid_then_error(fnv, array, n, expected_msg):
    with pytest.raises(ValueError, match=re.escape(expected_msg)):
        fnv(np.array(array), n)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (
            [3, 3, 4, 2, 5, 6, 1, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
            [0, 0, 1, 0, 1, 0, 0, 0],
        ),
        (
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 4, 2, 5, 6, 1, 3],
            [0, 0, 0, 1, 0, 0, 1, 0],
        ),
        ([1, 1], [1, 1], [0, 0]),
    ],
)
def test_cross(a, b, expected):
    assert np.array_equal(
        cross(np.array(a), np.array(b)), expected, equal_nan=True
    )


@pytest.mark.parametrize(
    "a, b, expected_msg",
    [
        ([1, 2, 3], [3, 3, 3, 3], "len(a) != len(b)"),
        ([3, 3, 3, 3], [1, 2, 3], "len(a) != len(b)"),
        ([1, 2, 3], [], "b cannot be empty."),
        ([], [1, 2, 3], "a cannot be empty."),
        ([1], [1], "a and b must have length >= 2."),
    ],
)
def test_cross_when_invalid_input_then_error(a, b, expected_msg):
    with pytest.raises(ValueError, match=re.escape(expected_msg)):
        cross(np.array(a), np.array(b))
