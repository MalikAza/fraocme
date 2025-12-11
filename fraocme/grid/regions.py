"""Region and connected component analysis for grids."""

from dataclasses import dataclass
from typing import Callable, TypeVar

from .core import Grid
from .directions import CARDINALS
from .types import Position

T = TypeVar("T")


@dataclass
class Region:
    """
    Represents a connected region in a grid.

    Example:
        region = Region(frozenset([(0, 0), (1, 0), (0, 1)]))
        print(region.size)    # 3
        print(region.bounds)  # ((0, 0), (1, 1))
    """

    positions: frozenset[Position]

    @property
    def size(self) -> int:
        """
        Get the number of positions in the region.

        Returns:
            Count of positions in this region
        """
        return len(self.positions)

    @property
    def bounds(self) -> tuple[Position, Position]:
        """
        Get bounding box of the region.

        Returns:
            Tuple of (top_left, bottom_right) positions as
            ((min_x, min_y), (max_x, max_y))

        Example:
            region = Region(frozenset([(1, 2), (3, 2), (2, 4)]))
            bounds = region.bounds  # ((1, 2), (3, 4))
        """
        if not self.positions:
            return ((0, 0), (0, 0))

        xs = [p[0] for p in self.positions]
        ys = [p[1] for p in self.positions]

        return ((min(xs), min(ys)), (max(xs), max(ys)))


def _normalize_predicate(predicate: Callable[[T], bool] | T) -> Callable[[T], bool]:
    """
    Convert predicate to callable form.

    If predicate is not callable, treat it as a value and check for equality.
    """
    if callable(predicate):
        return predicate
    else:
        # Value-based predicate
        target_value = predicate
        return lambda cell: cell == target_value


def flood_fill(
    grid: Grid[T], start: Position, predicate: Callable[[T], bool] | T
) -> Region:
    """
    Find all connected positions matching a predicate using flood fill.

    Uses iterative stack-based approach (4-directional connectivity).

    Args:
        grid: Grid to search
        start: Starting position
        predicate: Either a function that returns True for matching cells,
                   or a value to match for equality

    Returns:
        Region containing all connected matching positions

    Example input:
        grid = Grid.from_chars("##.\\n#..\\n...")

    Example usage:
        region = grid.flood_fill((0, 0), '#')
        # or with a function:
        region = grid.flood_fill((0, 0), lambda cell: cell == '#')

    Returns:
        Region with:
        - positions: {(0, 0), (1, 0), (0, 1)}
        - size: 3
        - bounds: ((0, 0), (1, 1))
    """
    pred_fn = _normalize_predicate(predicate)

    # Check if start position matches
    if not grid.in_bounds(start) or not pred_fn(grid.at(*start)):
        return Region(frozenset())

    visited = set()
    stack = [start]
    positions = []

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        positions.append(current)

        # Check 4-directional neighbors
        for direction in CARDINALS:
            next_pos = grid.neighbor(current, direction)

            if next_pos and next_pos not in visited:
                if pred_fn(grid.at(*next_pos)):
                    stack.append(next_pos)

    return Region(frozenset(positions))


def find_regions(grid: Grid[T], predicate: Callable[[T], bool] | T) -> list[Region]:
    """
    Find all connected regions matching a predicate.

    Args:
        grid: Grid to search
        predicate: Either a function that returns True for matching cells,
                   or a value to match for equality

    Returns:
        List of all distinct connected regions

    Example input:
        grid = Grid.from_chars("##.#\\n#...\\n..##")

    Example usage:
        regions = grid.find_regions('#')
        # or with a function:
        regions = grid.find_regions(lambda cell: cell != '.')

    Returns:
        [Region(size=3, bounds=((0,0), (1,1))),
         Region(size=1, bounds=((3,0), (3,0))),
         Region(size=2, bounds=((2,2), (3,2)))]

    Note:
        Uses 4-directional connectivity (NSEW).
        Diagonal neighbors are not considered connected.
    """
    pred_fn = _normalize_predicate(predicate)
    visited_global = set()
    regions = []

    # Scan entire grid
    for y in range(grid.height):
        for x in range(grid.width):
            pos = (x, y)

            if pos not in visited_global and pred_fn(grid.at(x, y)):
                # Found new region - flood fill from here
                region = flood_fill(grid, pos, predicate)
                regions.append(region)
                visited_global.update(region.positions)

    return regions


Grid.flood_fill = lambda self, start, predicate: flood_fill(self, start, predicate)
Grid.find_regions = lambda self, predicate: find_regions(self, predicate)
