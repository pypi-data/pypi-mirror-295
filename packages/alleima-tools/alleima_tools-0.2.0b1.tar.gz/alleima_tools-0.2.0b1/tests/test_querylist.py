from collections.abc import Callable

import pytest

from alleima_tools.querylist import query_list


@pytest.mark.parametrize(
    ("full_list", "expression", "expected"),
    [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], lambda x: x % 2 == 0, [2, 4, 6, 8, 10]),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], lambda x: x > 10, []),  # noqa: PLR2004
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], lambda x: x < 0, []),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            lambda x: x > 0,
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ),
    ],
)
def test_query_list(full_list: list, expression: Callable, expected: list):
    # Test case 1: Empty list
    assert query_list(full_list, expression) == expected
