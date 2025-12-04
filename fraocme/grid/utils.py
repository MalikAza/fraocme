from functools import cache
from typing import Tuple

from .types import (
    AroundPositions,
    CornersPositions,
    Direction,
    Grid,
    NSEWPositions,
    Position,
)


class GridUtils:
    """Utility class for navigating and manipulating 2D grids."""

    possible_directions: list[Direction] = ["^", ">", "v", "<"]
    start: Position | None = None
    end: Position | None = None

    def __init__(
        self,
        data: str | Grid,
        start_value: str | None = None,
        end_value: str | None = None,
    ):
        """
        Initialize grid utilities.

        Args:
            data: Raw string input or pre-parsed grid
            start_value: Optional character to mark as start position
            end_value: Optional character to mark as end position
        """
        if isinstance(data, str):
            self.grid = data.split("\n")
        else:
            self.grid = data

        self._start_value = start_value
        self._end_value = end_value
        self._search_start_and_end()

    @cache
    def is_position_out_of_bounds(self, position: Position) -> bool:
        """Check if a position is outside the grid boundaries."""
        x, y = position
        return y < 0 or y >= len(self.grid) or x < 0 or x >= len(self.grid[y])

    @cache
    def get_position_down(self, position: Position) -> Position:
        """Get the position directly below."""
        return (position[0], position[1] + 1)

    @cache
    def get_position_right(self, position: Position) -> Position:
        """Get the position to the right."""
        return (position[0] + 1, position[1])

    @cache
    def get_position_up(self, position: Position) -> Position:
        """Get the position directly above."""
        return (position[0], position[1] - 1)

    @cache
    def get_position_left(self, position: Position) -> Position:
        """Get the position to the left."""
        return (position[0] - 1, position[1])

    @cache
    def get_position_down_right(self, position: Position) -> Position:
        """Get the position diagonally down-right."""
        return self.get_position_down(self.get_position_right(position))

    @cache
    def get_position_down_left(self, position: Position) -> Position:
        """Get the position diagonally down-left."""
        return self.get_position_down(self.get_position_left(position))

    @cache
    def get_position_up_right(self, position: Position) -> Position:
        """Get the position diagonally up-right."""
        return self.get_position_up(self.get_position_right(position))

    @cache
    def get_position_up_left(self, position: Position) -> Position:
        """Get the position diagonally up-left."""
        return self.get_position_up(self.get_position_left(position))

    @cache
    def get_positions_in_corners(self, position: Position) -> CornersPositions:
        """Get all four corner positions around a point."""
        return {
            "down_right": self.get_position_down_right(position),
            "down_left": self.get_position_down_left(position),
            "up_right": self.get_position_up_right(position),
            "up_left": self.get_position_up_left(position),
        }

    @cache
    def get_positions_in_nsew(self, position: Position) -> NSEWPositions:
        """Get all four cardinal direction positions (North, South, East, West)."""
        return {
            "down": self.get_position_down(position),
            "right": self.get_position_right(position),
            "up": self.get_position_up(position),
            "left": self.get_position_left(position),
        }

    @cache
    def get_positions_around(self, position: Position) -> AroundPositions:
        """Get all 8 positions around a point (cardinal + corners)."""
        return {
            **self.get_positions_in_nsew(position),
            **self.get_positions_in_corners(position),
        }

    @cache
    def get_position_by_direction(
        self, position: Position, direction: Direction
    ) -> Position:
        """
        Get the position in a specific direction.

        Args:
            position: Starting position
            direction: One of '^' (up), '>' (right), 'v' (down), '<' (left)

        Returns:
            New position after moving in the specified direction
        """
        match direction:
            case "^":
                return self.get_position_up(position)
            case ">":
                return self.get_position_right(position)
            case "v":
                return self.get_position_down(position)
            case "<":
                return self.get_position_left(position)

    def _search_start_and_end(self) -> None:
        """Internal method to find start and end positions if specified."""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if self._start_value and cell == self._start_value:
                    self.start = (x, y)

                if self._end_value and cell == self._end_value:
                    self.end = (x, y)

    def search_value(self, value: str) -> Tuple[Position, ...]:
        """
        Find all positions containing a specific value.

        Args:
            value: Character/value to search for

        Returns:
            Tuple of positions where the value was found
        """
        positions = []
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == value:
                    positions.append((x, y))

        return tuple(positions)

    def get_cell_value(self, position: Position) -> str | None:
        """
        Get the value at a specific position.

        Args:
            position: Grid position to check

        Returns:
            Cell value or None if out of bounds
        """
        if self.is_position_out_of_bounds(position):
            return None

        return self.grid[position[1]][position[0]]
