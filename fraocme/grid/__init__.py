"""
Grid module for 2D grid operations.

Provides a high-performance, immutable Grid[T] class with:
- Efficient structural sharing for mutations
- Lazy indexing for fast value lookups
- Neighbor queries with ring support
- Modern direction system
- Pathfinding algorithms (BFS, Dijkstra, A*)
- Region/connected component analysis
- Transformation operations (rotate, flip, transpose)
"""

from . import parser, transformations
from .core import Grid
from .directions import (
    ALL_DIRECTIONS,
    CARDINALS,
    DIAGONALS,
    EAST,
    NORTH,
    NORTHEAST,
    NORTHWEST,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    WEST,
    Direction,
    direction_from_delta,
    opposite,
    turn_left,
    turn_right,
)
from .pathfinding import (
    Path,
    a_star,
    bfs,
    chebyshev_distance,
    dijkstra,
    manhattan_distance,
)
from .regions import Region
from .types import Position

__all__ = [
    # Core
    "Grid",
    "Position",
    "parser",
    "transformations",
    # Directions
    "Direction",
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST",
    "NORTHEAST",
    "SOUTHEAST",
    "SOUTHWEST",
    "NORTHWEST",
    "CARDINALS",
    "DIAGONALS",
    "ALL_DIRECTIONS",
    "turn_left",
    "turn_right",
    "opposite",
    "direction_from_delta",
    # Pathfinding
    "Path",
    "bfs",
    "dijkstra",
    "a_star",
    "manhattan_distance",
    "chebyshev_distance",
    # Regions
    "Region",
]
