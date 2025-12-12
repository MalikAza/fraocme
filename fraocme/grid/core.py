"""Core Grid class with optimized immutable operations."""

from typing import Callable, Generic, Sequence, TypeVar

from .directions import Direction
from .types import Position

T = TypeVar("T")
U = TypeVar("U")


class Grid(Generic[T]):
    """
    Immutable 2D grid with performance optimizations.

    Uses tuple-based storage for immutability and structural sharing.
    Supports lazy indexing, efficient transformations, and neighbor queries.

    Position convention: (x, y) where x is column, y is row.
    Grid access: grid[y][x] or grid.at(x, y)

    Example:
        grid = Grid.from_chars("abc\ndef")    # 3x2 grid of strings
        grid.width, grid.height               # (3, 2)
        grid.at(1, 0)                         # 'b'
        grid = grid.set(0, 1, "z")            # structural sharing copy
        grid.transpose()[0]                   # first column after transpose
    """

    __slots__ = ("data", "_index", "_width", "_height")

    # Class constants for neighbor operations
    CARDINAL_DELTAS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    DIAGONAL_DELTAS = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

    def __init__(self, data: Sequence[Sequence[T]]):
        """
        Initialize grid from 2D sequence.

        Args:
            data: 2D sequence that will be converted to immutable tuples.

        Raises:
            ValueError: If data is empty or rows have inconsistent lengths.
        """
        if not data:
            raise ValueError("Grid data cannot be empty")

        # Convert to immutable tuple structure
        tuple_data = tuple(tuple(row) for row in data)

        # Validate rectangular shape
        first_len = len(tuple_data[0])
        if not all(len(row) == first_len for row in tuple_data):
            raise ValueError("All rows must have the same length")

        self.data = tuple_data
        self._index = None
        self._width = len(tuple_data[0]) if tuple_data else 0
        self._height = len(tuple_data)

    @classmethod
    def create(cls, width: int, height: int, default_value: T = ".") -> "Grid[T]":
        """
        Create a new grid with specified dimensions filled with a default value.

        Args:
            width: Number of columns
            height: Number of rows
            default_value: Value to fill the grid with (default: ".")

        Returns:
            New Grid instance filled with the default value

        Raises:
            ValueError: If width or height is less than 1

        Example:
            grid = Grid.create(3, 2, ".")
            # Creates a 3x2 grid filled with "."
            # . . .
            # . . .
        """
        if width < 1 or height < 1:
            raise ValueError("Width and height must be at least 1")

        data = tuple(tuple(default_value for _ in range(width)) for _ in range(height))
        return cls(data)

    @classmethod
    def from_positions(
        cls,
        positions: set[tuple[int, int]] | list[tuple[int, int]],
        fill: T = "#",
        default: T = ".",
    ) -> "Grid[T]":
        """
        Create a grid from a set of positions. Fill those positions with ``fill``
        and use ``default`` for other cells.

        Args:
            positions: Set or list of (x, y) positions
            fill: Value to fill at given positions (default: "#")
            default: Value for other cells (default: ".")

        Returns:
            Grid instance covering the minimal bounding box of positions

        Example:
            Grid.from_positions({(1, 1), (2, 2)}, fill="*")
        """
        if not positions:
            return cls.create(1, 1, default)
        xs = [x for x, y in positions]
        ys = [y for x, y in positions]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        # Build grid data
        data = []
        pos_set = set(positions)
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                row.append(fill if (x, y) in pos_set else default)
            data.append(row)
        return cls(data)

    @property
    def width(self) -> int:
        """Get grid width (number of columns)."""
        return self._width

    @property
    def height(self) -> int:
        """Get grid height (number of rows)."""
        return self._height

    @property
    def dimensions(self) -> tuple[int, int]:
        """Get grid dimensions as (width, height)."""
        return (self._width, self._height)

    def at(self, x: int, y: int) -> T:
        """
        Get value at position (x, y).

        Args:
            x: Column index
            y: Row index

        Returns:
            Value at the position

        Raises:
            IndexError: If position is out of bounds
        """
        return self.data[y][x]

    def __getitem__(self, key: int) -> tuple[T, ...]:
        """
        Support subscript access: grid[y] returns row tuple.

        Enables grid[y][x] syntax for cell access.
        """
        return self.data[key]

    def in_bounds(self, pos: Position) -> bool:
        """Check if position is within grid boundaries."""
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def set(self, x: int, y: int, value: T) -> "Grid[T]":
        """
        Create new Grid with updated value at (x, y).

        Uses structural sharing - only copies the affected row.

        Args:
            x: Column index
            y: Row index
            value: New value

        Returns:
            New Grid instance with the change
        """
        # Create new row with updated value
        old_row = self.data[y]
        new_row = old_row[:x] + (value,) + old_row[x + 1 :]

        # Create new data tuple reusing unchanged rows
        new_data = self.data[:y] + (new_row,) + self.data[y + 1 :]

        return Grid(new_data)

    def bulk_set(self, changes: dict[Position, T]) -> "Grid[T]":
        """
        Create new Grid with multiple changes efficiently.

        Groups changes by row to minimize copying.

        Args:
            changes: Dictionary mapping positions to new values

        Returns:
            New Grid instance with all changes applied
        """
        if not changes:
            return self

        # Group changes by row
        rows_to_update: dict[int, dict[int, T]] = {}
        for (x, y), value in changes.items():
            if y not in rows_to_update:
                rows_to_update[y] = {}
            rows_to_update[y][x] = value

        # Build new data with minimal copying
        new_data = []
        for y, row in enumerate(self.data):
            if y in rows_to_update:
                # This row has changes - rebuild it
                row_changes = rows_to_update[y]
                new_row = tuple(row_changes.get(x, row[x]) for x in range(len(row)))
                new_data.append(new_row)
            else:
                # Reuse unchanged row
                new_data.append(row)

        return Grid(new_data)

    def find(self, value: T) -> list[Position]:
        """
        Find all positions containing the given value.

        Uses lazy caching for performance on repeated calls.

        Args:
            value: Value to search for

        Returns:
            List of positions where value was found
        """
        # Build index lazily
        if self._index is None:
            self._build_index()

        return self._index.get(value, [])

    def find_first(self, value: T) -> Position | None:
        """
        Find first position containing the given value.

        Args:
            value: Value to search for

        Returns:
            First position where value was found, or None
        """
        positions = self.find(value)
        return positions[0] if positions else None

    def _build_index(self) -> None:
        """Build the value-to-positions index."""
        index: dict[T, list[Position]] = {}
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell not in index:
                    index[cell] = []
                index[cell].append((x, y))

        object.__setattr__(self, "_index", index)

    def get_neighbors(
        self, pos: Position, ring: int = 1, include_diagonals: bool = True
    ) -> list[Position]:
        """
        Get all neighbor positions at a specific ring distance.

        Uses Chebyshev distance for diagonal movement, Manhattan for cardinal only.

        Args:
            pos: Center position
            ring: Distance ring (1 = immediate neighbors, 2 = next layer, etc.)
            include_diagonals: Whether to include diagonal neighbors

        Returns:
            List of valid in-bounds neighbor positions at the specified ring

        Example:
            grid = Grid.from_chars("abc\ndef\nghi")
            grid.get_neighbors((1, 1))
            # [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
            grid.get_neighbors((1, 1), include_diagonals=False)
            # [(1, 0), (2, 1), (1, 2), (0, 1)]
        """
        x, y = pos
        neighbors = []

        if include_diagonals:
            # Chebyshev distance: max(|dx|, |dy|) == ring
            for dx in range(-ring, ring + 1):
                for dy in range(-ring, ring + 1):
                    if max(abs(dx), abs(dy)) == ring:
                        neighbor = (x + dx, y + dy)
                        if self.in_bounds(neighbor):
                            neighbors.append(neighbor)
        else:
            # Manhattan distance: |dx| + |dy| == ring (cardinal only)
            for dx in range(-ring, ring + 1):
                for dy in range(-ring, ring + 1):
                    if abs(dx) + abs(dy) == ring:
                        neighbor = (x + dx, y + dy)
                        if self.in_bounds(neighbor):
                            neighbors.append(neighbor)

        return neighbors

    def get_neighbor_values(
        self, pos: Position, ring: int = 1, include_diagonals: bool = True
    ) -> list[tuple[Position, T]]:
        """
        Get all neighbor positions with their values at a specific ring distance.

        Args:
            pos: Center position
            ring: Distance ring
            include_diagonals: Whether to include diagonal neighbors

        Example:
            grid = Grid.from_chars("abc\ndef\nghi")
            grid.get_neighbor_values((1, 1), include_diagonals=False)

        Returns:
            List of (position, value) tuples for neighbors at the specified ring
            [((1, 0), 'b'), ((2, 1), 'f'), ((1, 2), 'h'), ((0, 1), 'd')]

        """
        neighbors = self.get_neighbors(pos, ring, include_diagonals)
        return [(neighbor, self.at(*neighbor)) for neighbor in neighbors]

    def neighbor(
        self, pos: Position, direction: Direction, distance: int = 1
    ) -> Position | None:
        """
        Get neighbor position in a direction.

        Args:
            pos: Starting position
            direction: Direction to look
            distance: Distance to neighbor (default 1)

        Example:
            grid.neighbor((1, 1), NORTH)       # (1, 0)
            grid.neighbor((1, 1), EAST, 3)     # (4, 1)

        Returns:
            Neighbor position if in bounds, None otherwise
            [(1, 0), (4, 1)]
        """
        new_pos = direction.apply(pos, distance)
        return new_pos if self.in_bounds(new_pos) else None

    def map(self, fn: Callable[[T], U]) -> "Grid[U]":
        """
        Apply function to all cells, returning new Grid.

        Args:
            fn: Function to apply to each cell value

        Returns:
            New Grid with transformed values
        """
        new_data = tuple(tuple(fn(cell) for cell in row) for row in self.data)
        return Grid(new_data)

    def filter_positions(
        self, predicate: Callable[[Position, T], bool]
    ) -> list[Position]:
        """
        Find all positions matching a predicate.

        Args:
            predicate: Function that returns True for matching cells

        Returns:
            List of positions where predicate returned True
        """
        positions = []
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if predicate((x, y), cell):
                    positions.append((x, y))
        return positions

    def __hash__(self) -> int:
        """Make Grid hashable for use in sets/dicts."""
        return hash(self.data)

    def __eq__(self, other: object) -> bool:
        """Check equality based on data content."""
        if not isinstance(other, Grid):
            return False
        return self.data == other.data

    def __repr__(self) -> str:
        """Return concise representation showing type and dimensions."""
        if not self.data:
            return "Grid(empty)"

        # Get type of first element
        first_elem = self.data[0][0]
        type_name = type(first_elem).__name__

        return f"Grid[{type_name}]({self.width}x{self.height})"

    def __str__(self) -> str:
        """String representation. For detailed printing, use printer functions."""
        type_name = type(self.data[0][0]).__name__
        return (
            f"Grid[{type_name}]({self.width}x{self.height}) "
            f"(use fraocme.grid.printer for details)"
        )
