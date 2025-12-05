from typing import Callable, TypeVar

T = TypeVar("T")


# ─────────────────────────────────────────────────────────
# Basic parsers
# ─────────────────────────────────────────────────────────
def sections(raw: str) -> list[str]:
    """Parse input as list of blocks (separated by blank lines).

    Example input:
        block 1, 0
        block 1, 1

        block 2, 0
        block 2, 1

    Returns: ["block 1, 0\nblock 1, 1", "block 2, 0\nblock 2, 1"]
    """
    return [block.strip() for block in raw.strip().split("\n\n")]


def lines(raw: str) -> list[str]:
    """Parse input as list of strings (one per line)."""
    return raw.strip().split("\n")


def ints(raw: str) -> list[int]:
    """
    Parse input as list of integers (one per line).

    Example input:
        42
        100
        -5
    Returns: [42, 100, -5]
    """
    return [int(line) for line in lines(raw)]


def ints_per_line(raw: str, delimiter: str | None = None) -> list[list[int]]:
    """
    Parse input as lists of integers per line.
    (2D grid of single digits.)

    Args:
        delimiter: Separator between numbers (default: whitespace)

    Example input:
        123
        456
    Returns: [[1,2,3], [4,5,6]]
    """
    return [list(map(int, line.split(delimiter))) for line in lines(raw)]


def key_ints(raw: str, key_delimiter: str = ": ") -> dict[int, list[int]]:
    """
    Parse input where each line has a key followed by space-separated integers.

    Args:
        key_delimiter: Separator between key and values (default: ": ")

    Example input:
        190: 10 19
        3267: 81 40 27
        83: 17 5
    Returns: {190: [10, 19], 3267: [81, 40, 27], 83: [17, 5]}

    Usage:
        data = key_ints(raw)
        data[190]  # → [10, 19]
    """
    result = {}
    for line in lines(raw):
        key, values = line.split(key_delimiter)
        result[int(key)] = list(map(int, values.split()))
    return result


# ─────────────────────────────────────────────────────────
# Range parser
# ─────────────────────────────────────────────────────────


def ranges(
    raw: str,
    range_delimiter: str = "-",
    entry_delimiter: str = ",",
) -> list[tuple[int, int]]:
    """
    Parse input as list of integer ranges.
    Args:
        range_delimiter: Separator between start and end of range (default: "-")
        entry_delimiter: Separator between different ranges (default: ",")
    Example input:
        1-5,10-15,20-25
    Returns: [(1,5), (10,15), (20,25)]
    """
    return [
        tuple(map(int, entry.strip().split(range_delimiter)))
        for entry in raw.strip().split(entry_delimiter)
    ]


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
