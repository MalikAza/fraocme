from typing import TypeVar

T = TypeVar("T")


def lines(raw: str) -> list[str]:
    """
    Parse input as list of strings (one per line).

    Example:
        "hello\nworld" -> ["hello", "world"]
    """
    return raw.strip().split("\n")


def int_grid(raw: str) -> list[list[int]]:
    """
    Parse input as 2D grid of single-digit integers.

    Example:
        "123\n456" -> [[1,2,3], [4,5,6]]
    """
    return [[int(char) for char in line] for line in lines(raw)]
