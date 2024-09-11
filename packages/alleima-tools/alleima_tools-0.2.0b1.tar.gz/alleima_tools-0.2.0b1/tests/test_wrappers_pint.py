import math
from contextlib import nullcontext
from decimal import Decimal

import pytest

from alleima_tools.alleima_tools import number_isclose
from alleima_tools.wrappers import Q_
from alleima_tools.wrappers.pint import pint_acos, pint_asin, pint_cos

VALUE_ERROR_MSG_PATTERN = r"strict=True"


@pytest.mark.parametrize(
    ("value", "func", "expected"),
    [
        (Q_("0 degree"), pint_cos, nullcontext(1)),
        (
            math.pi,
            pint_cos,
            pytest.raises(ValueError, match=VALUE_ERROR_MSG_PATTERN),
        ),
        (Q_(math.pi / 2, "radian"), pint_cos, nullcontext(0)),
        (Decimal(".5"), pint_acos, nullcontext(Q_(math.pi / 3, "radian"))),
        ("1", pint_asin, pytest.raises(TypeError, match="not str")),
    ],
)
def test_pint_cos(value, func, expected):
    """Test the pint_cos function."""
    with expected as e:
        assert number_isclose(func(value), e)


@pytest.mark.skip(reason="Useless test of a math function.")
def test_math_sin_str():
    from math import sin

    with pytest.raises(TypeError, match="not str") as e:
        assert sin("1") == e
