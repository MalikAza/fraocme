from typing import Callable, TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


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


def char_lines(raw: str, as_int: bool = True) -> list[list[int]] | list[list[str]]:
    """
    Parse input where each line is converted to a list of individual digits.
    Use if all rows haven't the same length.
    Prefer Grid.from_digits() if all rows have the same length.

    Args:
        as_int: If True, returns integers; if False, returns strings (default: True)

    Example input:
        1234521
        67890
        11111
    Returns (as_int=True): [[1, 2, 3, 4, 5, 2, 1], [6, 7, 8, 9, 0],
        [1, 1, 1, 1, 1]]
    Returns (as_int=False):
        [['1', '2', '3', '4', '5', '2', '1',],
        ['6', '7', '8', '9', '0'], ['1', '1', '1', '1', '1']]
    """
    if as_int:
        return [[int(digit) for digit in line] for line in lines(raw)]
    return [[digit for digit in line] for line in lines(raw)]


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
# Coordinate parsers
# ─────────────────────────────────────────────────────────
def coordinates(
    raw: str,
    delimiter: str = ",",
    value_type: Callable[[str], T] = int,
    coord_delimiter: str | None = None,
) -> list[tuple[T, ...]]:
    """
    Parse input as list of coordinate tuples (supports n-dimensional coordinates).

    Args:
        raw: Raw input string with coordinates
        delimiter: Separator between coordinate values within
            a coordinate (default: ",")
        value_type: Function to parse coordinate values (default: int)
        coord_delimiter: Separator between coordinates. If None,
            each line is a coordinate. Use " " or other separator
            for inline coordinates like "x-y x-y x-y"

    Example input (2D, one per line):
        10,20
        30,40
        50,60

    Returns: [(10, 20), (30, 40), (50, 60)]

    Example input (3D):
        1,2,3
        4,5,6

    Returns: [(1, 2, 3), (4, 5, 6)]

    Example input :
        1-2 3-4 5-6
        1-2,3-4,5-6

    Usage:
        Integer coordinates, one per line (default)
        coords = coordinates(raw)

        Float coordinates
        coords = coordinates(raw, value_type=float)

        Space-separated inline: "1,2 3,4 5,6"
        coords = coordinates(raw, coord_delimiter=" ")

        Dash notation inline: "1-2 3-4 5-6"
        coords = coordinates(raw, delimiter="-", coord_delimiter=" ")
    """
    result: list[tuple[T, ...]] = []

    if coord_delimiter is None:
        # Each line is a coordinate
        for line in lines(raw):
            values = tuple(value_type(v.strip()) for v in line.split(delimiter))
            result.append(values)
    else:
        # Coordinates are inline, separated by coord_delimiter
        all_coords = raw.strip().split(coord_delimiter)
        for coord_str in all_coords:
            coord_str = coord_str.strip()
            if coord_str:  # Skip empty strings
                values = tuple(
                    value_type(v.strip()) for v in coord_str.split(delimiter)
                )
                result.append(values)

    return result


# ─────────────────────────────────────────────────────────
# Custom line parser
# ─────────────────────────────────────────────────────────
def mapped(raw: str, line_parser: Callable[[str], T]) -> list[T]:
    r"""
    Parse each line with a custom parser function.

    Args:
        raw: Raw input string
        line_parser: Function to parse each line

    Example:
        def parse_coords(line):
            x, y = line.split(',')
            return (int(x), int(y))

        coords = mapped(raw, parse_coords)

    Example input (named coordinates - use regex or custom parsing):
        x=10, y=20, z=30
        x=40, y=50, z=60

    For complex formats like "x=10, y=20", use the mapped() function:
        import re
        def parse_named(line):
            nums = [int(x) for x in re.findall(r'-?\d+', line)]
            return tuple(nums)
        coords = mapped(raw, parse_named)
    """
    return [line_parser(line) for line in lines(raw)]
