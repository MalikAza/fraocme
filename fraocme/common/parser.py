from typing import Callable, TypeVar

T = TypeVar("T")


def lines(raw: str) -> list[str]:
    """Parse input as list of strings (one per line)."""
    return raw.strip().split("\n")


def ints(raw: str) -> list[int]:
    """
    Parse input as list of integers (one per line).

    Example:
        "42\\n100\\n-5" -> [42, 100, -5]
    """
    return [int(line) for line in lines(raw)]


def floats(raw: str) -> list[float]:
    """
    Parse input as list of floats (one per line).

    Example:
        "3.14\\n2.71" -> [3.14, 2.71]
    """
    return [float(line) for line in lines(raw)]


def ints_per_line(raw: str, delimiter: str | None = None) -> list[list[int]]:
    """
    Parse input as lists of integers per line.

    Args:
        delimiter: Separator between numbers (default: whitespace)

    Example:
        "1 2 3\\n4 5 6" -> [[1, 2, 3], [4, 5, 6]]
    """
    return [list(map(int, line.split(delimiter))) for line in lines(raw)]


# ─────────────────────────────────────────────────────────
# Custom line parser
# ─────────────────────────────────────────────────────────
def mapped(raw: str, line_parser: Callable[[str], T]) -> list[T]:
    """
    Parse each line with a custom parser function.

    Args:
        raw: Raw input string
        line_parser: Function to parse each line

    Example:
        def parse_coords(line):
            x, y = line.split(',')
            return (int(x), int(y))

        coords = mapped(raw, parse_coords)
    """
    return [line_parser(line) for line in lines(raw)]
