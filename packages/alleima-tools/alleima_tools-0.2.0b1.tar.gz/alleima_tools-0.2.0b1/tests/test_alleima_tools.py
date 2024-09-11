#!/usr/bin/env python
"""Tests for `alleima_tools` package."""

from decimal import Decimal

import pytest

from alleima_tools.alleima_tools import (
    distance,
    make_decimal,
    number_isclose,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (10.5, Decimal("10.5")),
        (Decimal("10.5"), Decimal("10.5")),
        ("10.5", Decimal("10.5")),
    ],
)
def test_make_decimal(value, expected):
    """Test the make_decimal function."""
    assert make_decimal(value) == expected


@pytest.mark.parametrize(
    ("value", "places", "expected"),
    [
        (10.555, 2, Decimal("10.56")),
        (10.555, 1, Decimal("10.6")),
        (10.555, 0, Decimal("11")),
        (10.555, None, Decimal("10.555")),
        (Decimal("10.555"), 2, Decimal("10.56")),
        (Decimal("10.555"), 1, Decimal("10.6")),
        (Decimal("10.555"), 0, Decimal("11")),
        (Decimal("10.555"), None, Decimal("10.555")),
        ("10.555", 2, Decimal("10.56")),
        ("10.555", 1, Decimal("10.6")),
        ("10.555", 0, Decimal("11")),
        ("10.555", None, Decimal("10.555")),
        (10.499, 2, Decimal("10.50")),
        (10.499, 1, Decimal("10.5")),
        (10.499, 0, Decimal("10")),
        (10.499, None, Decimal("10.499")),
    ],
)
def test_round_make_decimal(value, places, expected):
    """Test the make_decimal function with rounding."""
    assert make_decimal(value, places) == expected


@pytest.mark.parametrize(
    ("first", "second", "tolerance", "expected"),
    [
        (10.5, Decimal("10.5"), None, True),
        (Decimal("10.5"), Decimal("10.5"), None, True),
        ("10.5", Decimal("10.5"), None, True),
        ("10.5", 10.5001, 1e-3, True),
        (10.5, 10.5001, None, False),
    ],
)
def test_is_number_close(first, second, tolerance, expected):
    """Test the is_number_close function."""
    assert number_isclose(first, second, tolerance=tolerance) == expected


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ((0, 0), (3, 4), 5.0),
        ((0, 0, 0), (3, 4, 0), 5.0),
        ((0, 0, 0), (2, 3, 4), 5.385164807134504),
        ((Decimal("0"), Decimal("0")), (Decimal("3"), Decimal("4")), Decimal("5.0")),
    ],
)
def test_distance(first, second, expected):
    """Test the distance function."""
    assert distance(first, second) == expected


def test_distance_mismatched_dimensions():
    """Test the distance function with mismatched dimensions."""
    with pytest.raises(ValueError, match="dimensions"):
        distance((0, 0), (3, 4, 0))
