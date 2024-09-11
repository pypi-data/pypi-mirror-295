import pytest


@pytest.fixture()
def long_path():
    return "/this/is/a/very/long/path/to/a/file.txt"


def test_truncate_path(long_path: str):
    from alleima_tools.utils.strings import truncate_path

    assert len(truncate_path(long_path, 20)) == 20

    print(truncate_path(long_path, 20))

    # assert truncate_path(long_path, 20) == "/this/.../file.txt"
    # assert truncate_path(long_path, 30) == "/this/is/a/.../file.txt"
    # assert truncate_path(long_path, 40) == "/this/is/a/very/.../file.txt"
    # assert truncate_path(long_path, 50) == "/this/is/a/very/long/path/to/a/file.txt"
