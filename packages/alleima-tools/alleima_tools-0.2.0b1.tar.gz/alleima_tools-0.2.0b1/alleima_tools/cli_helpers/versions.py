from datetime import datetime

import pytz


def generate_build_number(time_zone: str = "UTC") -> str:
    """Generate a build number based on the current date and time.

    The first 8 characters of the build number are the current date in the format
    'YYYYMMDD'. The last 3 characters ara counter of 2 minute intervals since midnight.

    Examples:
        >>> generate_build_number()
        '20220131120'

    Args:
        time_zone (str, optional): The time zone to use for the build number. Defaults to 'UTC'.

    Returns:
        str: The generated build number"""  # noqa: E501
    timezone_obj = pytz.timezone(time_zone)
    now = datetime.now(timezone_obj)
    build_number = now.strftime("%Y%m%d")
    build_number += str((now.hour * 60 + now.minute) // 2).zfill(3)
    return build_number
