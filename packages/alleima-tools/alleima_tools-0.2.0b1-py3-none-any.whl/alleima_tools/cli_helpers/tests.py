from datetime import UTC, datetime
from unittest import mock

from alleima_tools.cli_helpers import versions


@mock.patch(f"{versions.__name__}.datetime", wraps=datetime)
def test_build_number(mocker):
    mocker.now = mock.Mock(return_value=datetime(2022, 1, 31, 1, 20, tzinfo=UTC))

    build_number = versions.generate_build_number()

    assert build_number == "20220131040"
