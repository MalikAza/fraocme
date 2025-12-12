"""Grid parsing utilities and factory methods."""

import re
from typing import Callable, TypeVar

from .core import Grid

T = TypeVar("T")


def from_string(raw: str, cell_parser: Callable[[str], T] = str) -> Grid[T]:
    """
    Create Grid from string with custom cell parser.

    Args:
        raw: Raw string input
        cell_parser: Function to parse each character (default: str)

    Returns:
        Grid with parsed values

    Example input:
        "123\\n456"

    Example usage:
        grid = Grid.from_string("123\\n456", int)

    Returns:
        Grid[int](3x2) containing:
        1 2 3
        4 5 6
    """
    lines = raw.strip().split("\n")
    data = tuple(tuple(cell_parser(c) for c in line) for line in lines)
    return Grid(data)


def from_ints(raw: str) -> Grid[int]:
    """
    Create Grid from string of single-digit integers.

    Args:
        raw: String with single-digit integers (no spaces)

    Returns:
        Grid[int] with parsed integers

    Example input:
        "123\\n456\\n789"

    Example usage:
        grid = Grid.from_ints("123\\n456\\n789")

    Returns:
        Grid[int](3x3) containing:
        1 2 3
        4 5 6
        7 8 9
    """
    return from_string(raw, int)


def from_chars(raw: str) -> Grid[str]:
    """
    Create Grid from string of characters.

    Args:
        raw: String with characters

    Returns:
        Grid[str] with individual characters

    Example input:
        "abc\\ndef\\nghi"

    Example usage:
        grid = Grid.from_chars("abc\\ndef\\nghi")

    Returns:
        Grid[str](3x3) containing:
        a b c
        d e f
        g h i
    """
    return from_string(raw, str)


def from_dense(
    raw: str, delimiter: str = " ", cell_parser: Callable[[str], T] = int
) -> Grid[T]:
    """
    Create Grid from delimiter-separated values.

    Args:
        raw: String with delimited values
        delimiter: Separator between values (default: space)
        cell_parser: Function to parse each value (default: int)

    Returns:
        Grid with parsed values

    Example input:
        "10 20 30\\n40 50 60"

    Example usage:
        grid = Grid.from_dense("10 20 30\\n40 50 60")

    Returns:
        Grid[int](3x2) containing:
        10 20 30
        40 50 60

    With custom delimiter:
        grid = Grid.from_dense("a,b,c\\nd,e,f", delimiter=",", cell_parser=str)

    Returns:
        Grid[str](3x2) containing:
        a b c
        d e f
    """
    lines = raw.strip().split("\n")
    data = tuple(
        tuple(cell_parser(cell) for cell in re.split(delimiter, line)) for line in lines
    )
    return Grid(data)


Grid.from_string = staticmethod(from_string)
Grid.from_ints = staticmethod(from_ints)
Grid.from_chars = staticmethod(from_chars)
Grid.from_dense = staticmethod(from_dense)
