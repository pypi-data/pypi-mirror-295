from pathlib import Path


def truncate_path(path: Path | str, max_length: int):
    """Truncate a path to a maximum length.

    The path is truncated to the specified length by removing characters from the
    middle of the path.

    Examples:
        >>> truncate_path("C:/Users/username/Documents/file.txt", 20)
        'C:/Us...ents/file.txt'
        >>> truncate_path("C:/Users/username/Documents/file.txt", 30)
        'C:/Users/username/Docum.../file.txt'

    Args:
        path (Path | str): The path to be truncated.
        max_length (int): The maximum length of the truncated path.

    Returns:
        str: The truncated path.
    """
    path_str = str(path)
    if len(path_str) <= max_length:
        return path_str

    tail_length = max_length // 2
    head_length = max_length - tail_length - 3

    head = path_str[:head_length]
    tail = path_str[-tail_length:]

    return f"{head}...{tail}"


if __name__ == "__main__":
    from rich import print

    long_path = "/this/is/a/very/long/path/to/a/file.txt"
    length = 20

    print(f"{length} characters: {truncate_path(long_path, length)}")
