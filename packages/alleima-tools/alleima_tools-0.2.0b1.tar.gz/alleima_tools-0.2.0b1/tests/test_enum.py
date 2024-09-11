from enum import auto

from alleima_tools.enum import UpperStrEnum


class UpperEnum(UpperStrEnum):
    VALUE1 = auto()
    VALUE2 = auto()
    VALUE3 = auto()


def test_upper_str_enum():
    assert UpperEnum.VALUE1.value != "value1"
    assert UpperEnum.VALUE1.value == "VALUE1"
    assert UpperEnum.VALUE2.value == "VALUE2"
    assert UpperEnum.VALUE3.value == "VALUE3"
