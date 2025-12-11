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
        from fraocme.ui.colors import c

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

        # Calculate offset for grid display
        xs = [x for x, y in red_tiles]
        ys = [y for x, y in red_tiles]
        min_x, min_y = min(xs), min(ys)
        self.debug(f"Coordinate offset: ({c.yellow(min_x)}, {c.yellow(min_y)})")

        # Display red tiles grid
        grid = Grid.from_positions(red_tiles, fill="#", default=".")

        # Translate highlight positions to grid coordinates
        highlight_translated = {(x - min_x, y - min_y) for x, y in red_tiles}
        self.debug(c.bold("Red tile grid:"))
        self.debug(
            lambda: print_grid(
                grid, separator=" ", highlight=highlight_translated, show_coords=True
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
                f"Best corners: {c.yellow(best_corners[0])} to {c.yellow(best_corners[1])}"
            )

            # Show the winning rectangle
            from fraocme.common.coordinate_utils import rectangle_points

            rect_points = rectangle_points(best_corners[0], best_corners[1])
            rect_grid = Grid.from_positions(rect_points, fill="O", default=".")

            # Calculate offset for rectangle grid
            rect_xs = [x for x, y in rect_points]
            rect_ys = [y for x, y in rect_points]
            rect_offset_x, rect_offset_y = min(rect_xs), min(rect_ys)

            # Highlight the corners in the rectangle
            corners_translated = {
                (x - rect_offset_x, y - rect_offset_y) for x, y in best_corners
            }
            self.debug(c.bold("\nWinning rectangle (corners highlighted):"))
            self.debug(
                lambda: print_grid(
                    rect_grid,
                    separator=" ",
                    highlight=corners_translated,
                    show_coords=True,
                )
            )

        return max_area

    def part2(self, red_tiles: list[tuple[int, int]]) -> int:
        """
        Find largest rectangle using two red tiles as opposite corners,
        where all interior tiles must be red or green.

        Green tiles = outline connecting consecutive red tiles + interior of that outline
        """
        self.debug(
            c.bold("\n=== Part 2: Largest Rectangle (Interior Must Be Red/Green) ===")
        )

        # Calculate bounds for offset
        xs = [x for x, y in red_tiles]
        ys = [y for x, y in red_tiles]
        min_x, min_y = min(xs), min(ys)
        self.debug(f"Coordinate offset: ({c.yellow(min_x)}, {c.yellow(min_y)})")

        # Build outline and fill
        outline = build_outline_from_vertices(red_tiles, closed=True)
        self.debug(f"Outline has {c.magenta(len(outline))} points")

        green_region = fill_outline_floodfill(outline)
        self.debug(f"Green region has {c.green(len(green_region))} tiles")

        red_set = set(red_tiles)
        allowed = red_set | green_region
        self.debug(f"Total allowed tiles: {c.cyan(len(allowed))}")

        # Display the allowed region
        self.debug(c.bold("\nAllowed region (highlighted = red tiles):"))
        grid = Grid.from_positions(allowed, fill="·", default=" ")

        # Get offset from the allowed set (same as grid uses internally)
        allowed_xs = [x for x, y in allowed]
        allowed_ys = [y for x, y in allowed]
        offset_x, offset_y = min(allowed_xs), min(allowed_ys)

        # Mark red tiles using bulk_set (Grid is immutable!)
        red_changes = {}
        for rx, ry in red_tiles:
            gx = rx - offset_x
            gy = ry - offset_y
            if 0 <= gy < grid.height and 0 <= gx < grid.width:
                red_changes[(gx, gy)] = "#"

        grid = grid.bulk_set(red_changes)

        # Translate highlight positions to grid coordinates
        highlight_translated = {(x - offset_x, y - offset_y) for x, y in red_set}
        self.debug(
            lambda: print_grid(
                grid, separator=" ", highlight=highlight_translated, show_coords=True
            )
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
            rect_grid = Grid.from_positions(rect_points, fill="O", default=".")
            self.debug(c.bold("\nWinning rectangle:"))
            self.debug(lambda: print_grid(rect_grid, separator=" ", show_coords=True))

        return max_area
