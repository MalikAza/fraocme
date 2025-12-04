from typing import Literal, Tuple, TypedDict


class CornersPositions(TypedDict):
    """Positions at the four corners relative to a center point."""
    down_right: Tuple[int, int]
    down_left: Tuple[int, int]
    up_right: Tuple[int, int]
    up_left: Tuple[int, int]


class NSEWPositions(TypedDict):
    """Positions in the four cardinal directions (North, South, East, West)."""
    down: Tuple[int, int]
    right: Tuple[int, int]
    up: Tuple[int, int]
    left: Tuple[int, int]


class AroundPositions(CornersPositions, NSEWPositions):
    """All 8 positions around a center point (cardinal + corners)."""
    pass


Direction = Literal['^', '>', 'v', '<']
"""Cardinal direction symbols: ^ (up), > (right), v (down), < (left)."""

Position = Tuple[int, int]
"""Grid position as (x, y) coordinate."""

Grid = list[list[str]]
"""2D grid represented as list of rows."""
