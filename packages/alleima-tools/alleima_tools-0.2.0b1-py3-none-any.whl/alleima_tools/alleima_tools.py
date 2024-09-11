"""Main module."""

from decimal import Decimal
from typing import TypeVar


def is_number(s):
    """Tries to make a float, returns True if it succeeds, False otherwise."""
    if s is None:
        return False
    try:
        _ = float(s)
    except ValueError:
        return False
    else:
        return True


def make_decimal(value: str | float | Decimal, places: int | None = None) -> Decimal:
    """
    Convert the input value to a Decimal object.

    Parameters:
    value (str | float | Decimal): The value to be converted to a Decimal.
    places (int | None, optional): The number of decimal places to round the converted
        Decimal object to. If None, no rounding will be performed. Default is None.

    Returns:
    Decimal: The converted Decimal object.

    Raises:
    TypeError: If the input value is not a string, float, or Decimal.

    Examples:
    >>> make_decimal('10.5')
    Decimal('10.5')

    >>> make_decimal(10.5)
    Decimal('10.5')

    >>> make_decimal(Decimal('10.5'))
    Decimal('10.5')

    >>> make_decimal(10.555, 2)
    Decimal('10.56')
    """
    decimal_value = Decimal(value) if isinstance(value, str) else Decimal(str(value))

    return (
        decimal_value
        if places is None
        else decimal_value.quantize(Decimal(10) ** -places)
    )


def number_isclose(
    first: str | float | Decimal,
    second: str | float | Decimal,
    *,
    tolerance: float | None = None,
) -> bool:
    """
    Compare two numbers for approximate equality.

    Parameters:
    first (str | float | Decimal): The first number to compare.
    second (str | float | Decimal): The second number to compare.
    tolerance (float, optional): The maximum difference between the two numbers for
        them to be considered equal. Default is 1E-9.

    Returns:
    bool: True if the two numbers are approximately equal, False otherwise.

    Raises:
    TypeError: If the input values are not strings, floats, or Decimals.

    Examples:
    >>> number_isclose(10.5, 10.500000001)
    True

    >>> number_isclose(10.5, 10.50000001)
    False

    >>> number_isclose(10.5, 10.50000001, tolerance=1E-7)
    True

    >>> number_isclose(10.5, 10.5001, tolerance=1E-3)
    False
    """
    if tolerance is None:
        tolerance = 1e-9
    first_float = float(first)
    second_float = float(second)

    return abs(second_float - first_float) <= tolerance


class MismatchedDimensionsError(ValueError):
    """Exception raised when two points have different numbers of dimensions."""


T = TypeVar("T", float, int, Decimal)


def distance(point1: tuple[T, ...], point2: tuple[T, ...]) -> T:
    """Calculate euclidean distance between two points.

    Parameters:
    point1 (tuple): The first point.
    point2 (tuple): The second point.

    Returns:
    float: The distance between the two points.

    Examples:
    >>> distance((0, 0), (3, 4))
    5.0

    >>> distance((0, 0, 0), (3, 4, 0))
    5.0
    """
    if len(point1) != len(point2):
        msg = "Points must have the same number of dimensions."
        raise MismatchedDimensionsError(msg)

    pre_sqrt = sum((x - y) ** 2 for x, y in zip(point1, point2))  # noqa: B905 we've already checked the lengths

    if isinstance(pre_sqrt, Decimal):
        return pre_sqrt.sqrt()
    return pre_sqrt**0.5
