from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class QueryList(list[T]):
    def query(self, expression):
        return QueryList([item for item in self if expression(item)])

    @property
    def first(self):
        return self[0] if self else None


def query_list(full_list: list[T], expression: Callable):
    return [item for item in full_list if expression(item)]
