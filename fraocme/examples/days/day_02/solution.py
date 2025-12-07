"""
Day 2 Example: Grid Printer Functions

Demonstrates all the grid printer utilities for debugging and visualization.
"""

from fraocme import Solver
from fraocme.grid import Grid
from fraocme.grid.printer import (
    print_grid,
    print_grid_diff,
    print_grid_heatmap,
    print_grid_neighbors,
    print_grid_path,
    print_grid_region,
)
from fraocme.ui.colors import c


class Day2(Solver):
    def __init__(self, day: int = 2, debug: bool = False):
        super().__init__(day=day, debug=debug, copy_input=True)

    def parse(self, raw: str) -> Grid[int]:
        """Parse the input into a numeric grid."""
        return Grid.from_ints(raw)

    def part1(self, grid: Grid[int]) -> int:
        """
        Demonstrate basic grid printing functions.
        """
        self.debug(c.bold("\n=== Part 1: Basic Grid Printing ===\n"))

        # 1. Basic print with coordinates
        self.debug(c.cyan("1. Basic grid with coordinates:"))
        self.debug(lambda: print_grid(grid, separator=" ", show_coords=True))

        # 2. Heat map (color-coded by value)
        self.debug(c.cyan("\n2. Heat map (auto-colored by value):"))
        self.debug(lambda: print_grid_heatmap(grid, separator=" ", show_coords=True))

        # 3. Highlight specific positions
        self.debug(c.cyan("\n3. Highlighting specific positions:"))
        highlights = {(0, 0), (2, 2), (4, 1)}
        self.debug(
            lambda: print_grid(
                grid, separator=" ", highlight=highlights, show_coords=True
            )
        )

        # 4. Neighbor visualization
        self.debug(c.cyan("\n4. Neighbors of position (4, 1):"))
        self.debug(
            lambda: print_grid_neighbors(
                grid,
                (4, 1),
                ring=1,
                include_diagonals=True,
                separator=" ",
                show_coords=True,
            )
        )

        return len(grid.data)

    def part2(self, grid: Grid[int]) -> int:
        """
        Demonstrate advanced grid printing functions.
        """
        self.debug(c.bold("\n=== Part 2: Advanced Grid Printing ===\n"))

        # 1. Create a modified grid for diff demo
        modified = grid.set(1, 1, 0).set(3, 0, 0).set(5, 2, 0)
        self.debug(c.cyan("1. Grid diff (shows changes):"))
        self.debug(
            lambda: print_grid_diff(grid, modified, separator=" ", show_coords=True)
        )

        # 2. Path visualization
        self.debug(c.cyan("\n2. Path visualization:"))
        # Create a simple path (diagonal)
        path = [
            (0, 0),
            (1, 0),
            (2, 0),
            (2, 1),
            (3, 1),
            (4, 1),
            (5, 1),
            (6, 1),
            (7, 1),
            (8, 1),
        ]
        self.debug(lambda: print_grid_path(grid, path, separator=" ", show_coords=True))

        # 3. Region highlighting
        self.debug(c.cyan("\n3. Region highlighting (high values):"))
        # Find region of high values (>= 7)
        high_positions = grid.filter_positions(lambda pos, val: val >= 7)
        from fraocme.grid.regions import Region

        region = Region(frozenset(high_positions))
        self.debug(
            lambda: print_grid_region(grid, region, separator=" ", show_coords=True)
        )

        # 4. Large grid truncation demo
        self.debug(c.cyan("\n4. Large grid truncation (10x5 display):"))
        # Create a larger grid for demo
        large_rows = [[i * 10 + j for j in range(20)] for i in range(15)]
        large_grid = Grid(large_rows)
        self.debug(
            lambda: print_grid(
                large_grid, separator=" ", max_rows=10, max_cols=15, show_coords=True
            )
        )

        return sum(sum(row) for row in grid.data)
