"""
Day 09: Movie Theater - Finding largest rectangles
"""

from fraocme import Solver
from fraocme.common.coordinate_utils import (
    build_outline_from_vertices,
    fill_outline_floodfill,
    largest_valid_rectangle,
    rectangle_area,
)
from fraocme.common.parser import coordinates
from fraocme.grid.core import Grid
from fraocme.grid.printer import print_grid
from fraocme.ui.colors import c


class Day5(Solver):
    def parse(self, raw: str) -> list[tuple[int, int]]:
        """Parse red tile coordinates."""
        coords = coordinates(raw)
        self.debug(f"Parsed {c.cyan(len(coords))} red tile coordinates")
        self.debug(f"First 3: {c.yellow(coords[:3])}")
        return coords

    def part1(self, red_tiles: list[tuple[int, int]]) -> int:
        """
        Find largest rectangle using any two red tiles as opposite corners.
        No constraint on interior tiles.
        """
        self.debug(
            c.bold("\n=== Part 1: Largest Rectangle (No Interior Constraint) ===")
        )
        max_area = 0
        best_corners = None
        n = len(red_tiles)
        self.debug(f"Total red tiles: {c.cyan(n)}")

        # Display red tiles grid
        grid = Grid.from_positions(red_tiles, fill="#", default=".")
        self.debug(c.bold("Red tile grid:"))
        self.debug(
            lambda: print_grid(
                grid, separator=" ", highlight=set(red_tiles), show_coords=True
            )
        )

        for i in range(n):
            for j in range(i + 1, n):
                area = rectangle_area(red_tiles[i], red_tiles[j])
                if area > max_area:
                    self.debug(
                        f"New max area {c.green(area)} from corners "
                        f"{c.yellow(red_tiles[i])} and {c.yellow(red_tiles[j])}"
                    )
                    max_area = area
                    best_corners = (red_tiles[i], red_tiles[j])

        self.debug(f"\nFinal max area: {c.bold(c.green(max_area))}")
        if best_corners:
            self.debug(
                f"Best corners: {c.yellow(best_corners[0])} "
                f"to {c.yellow(best_corners[1])}"
            )
        return max_area

    def part2(self, red_tiles: list[tuple[int, int]]) -> int:
        """
        Find largest rectangle using two red tiles as opposite corners,
        where all interior tiles must be red or green.

        Green tiles = outline connecting consecutive red tiles
        + interior of that outline
        """
        self.debug(
            c.bold("\n=== Part 2: Largest Rectangle (Interior Must Be Red/Green) ===")
        )

        # Build outline connecting consecutive red tiles
        self.debug("Building outline from red tiles...")
        outline = build_outline_from_vertices(red_tiles, closed=True)
        self.debug(f"Outline has {c.magenta(len(outline))} points")

        # Fill interior to get green region
        self.debug("Filling interior to get green region...")
        green_region = fill_outline_floodfill(outline)
        self.debug(f"Green region has {c.green(len(green_region))} tiles")

        # Combine red and green for allowed tiles
        red_set = set(red_tiles)
        allowed = red_set | green_region
        self.debug(f"Total allowed tiles: {c.cyan(len(allowed))}")

        # Display the allowed region with red tiles highlighted
        self.debug(c.bold("\nAllowed region (highlighted = red tiles):"))
        grid = Grid.from_positions(allowed, fill="·", default=" ")
        # Mark red tiles with different character
        for rx, ry in red_tiles:
            if 0 <= ry < grid.height and 0 <= rx < grid.width:
                grid.data[ry][rx] = "#"
        self.debug(
            lambda: print_grid(grid, separator=" ", highlight=red_set, show_coords=True)
        )

        # Find largest valid rectangle
        self.debug("\nSearching for largest valid rectangle...")
        max_area, corners = largest_valid_rectangle(red_tiles, allowed)

        self.debug(f"\nMax area: {c.bold(c.green(max_area))}")
        if corners:
            self.debug(
                f"Rectangle corners: {c.yellow(corners[0])} to {c.yellow(corners[1])}"
            )

            # Show the winning rectangle
            from fraocme.common.coordinate_utils import rectangle_points

            rect_points = rectangle_points(corners[0], corners[1])
            self.debug(c.bold("\nWinning rectangle:"))
            rect_grid = Grid.from_positions(rect_points, fill="O", default=".")
            self.debug(lambda: print_grid(rect_grid, separator=" ", show_coords=True))

        return max_area
