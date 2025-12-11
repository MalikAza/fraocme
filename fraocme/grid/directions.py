"""Direction system for grid navigation."""

from dataclasses import dataclass

from .types import Position


@dataclass(frozen=True)
class Direction:
    """Represents a direction with a delta vector and name."""

    delta: tuple[int, int]
    name: str

    def apply(self, pos: Position, steps: int = 1) -> Position:
        """Apply this direction to a position."""
        dx, dy = self.delta
        x, y = pos
        return (x + dx * steps, y + dy * steps)


# Cardinal directions (4-directional)
NORTH = Direction((0, -1), "north")
SOUTH = Direction((0, 1), "south")
EAST = Direction((1, 0), "east")
WEST = Direction((-1, 0), "west")

# Diagonal directions
NORTHEAST = Direction((1, -1), "northeast")
SOUTHEAST = Direction((1, 1), "southeast")
SOUTHWEST = Direction((-1, 1), "southwest")
NORTHWEST = Direction((-1, -1), "northwest")

# Direction groups
CARDINALS = [NORTH, EAST, SOUTH, WEST]
DIAGONALS = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
ALL_DIRECTIONS = CARDINALS + DIAGONALS


# Precomputed direction mappings for O(1) lookups
_TURN_LEFT_MAP: dict[Direction, Direction] = {
    NORTH: WEST,
    WEST: SOUTH,
    SOUTH: EAST,
    EAST: NORTH,
    NORTHEAST: NORTHWEST,
    NORTHWEST: SOUTHWEST,
    SOUTHWEST: SOUTHEAST,
    SOUTHEAST: NORTHEAST,
}

_TURN_RIGHT_MAP: dict[Direction, Direction] = {
    NORTH: EAST,
    EAST: SOUTH,
    SOUTH: WEST,
    WEST: NORTH,
    NORTHEAST: SOUTHEAST,
    SOUTHEAST: SOUTHWEST,
    SOUTHWEST: NORTHWEST,
    NORTHWEST: NORTHEAST,
}

_OPPOSITE_MAP: dict[Direction, Direction] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
    NORTHEAST: SOUTHWEST,
    SOUTHWEST: NORTHEAST,
    SOUTHEAST: NORTHWEST,
    NORTHWEST: SOUTHEAST,
}

_DELTA_TO_DIRECTION: dict[tuple[int, int], Direction] = {
    d.delta: d for d in ALL_DIRECTIONS
}


def turn_left(direction: Direction) -> Direction:
    """Turn 90 degrees counter-clockwise."""
    return _TURN_LEFT_MAP[direction]


def turn_right(direction: Direction) -> Direction:
    """Turn 90 degrees clockwise."""
    return _TURN_RIGHT_MAP[direction]


def opposite(direction: Direction) -> Direction:
    """Get the opposite direction (180 degrees)."""
    return _OPPOSITE_MAP[direction]


def direction_from_delta(dx: int, dy: int) -> Direction | None:
    """
    Get Direction from delta coordinates.

    Returns None if the delta doesn't match any known direction.
    """
    return _DELTA_TO_DIRECTION.get((dx, dy))
