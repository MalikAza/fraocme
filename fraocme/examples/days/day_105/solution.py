"""
Day 5 Example: Region Analysis & Connected Components

Demonstrates flood fill and region finding algorithms.
"""

from fraocme import Solver
from fraocme.grid import Grid
from fraocme.grid.printer import print_grid_region
from fraocme.ui.colors import c


class Day105(Solver):
    def parse(self, raw: str) -> Grid[str]:
        """Parse the input into a grid."""
        return Grid.from_chars(raw)

    def part1(self, grid: Grid[str]) -> int:
        """
        Use flood_fill to analyze a single connected region.
        """
        self.debug(c.bold("\n=== Part 1: Flood Fill ===\n"))

        # Find first '#' to start flood fill
        start = grid.find_first("#")
        if not start:
            self.debug(c.red("No '#' found!"))
            return 0

        self.debug(c.cyan(f"Starting flood fill from: {start}"))
        self.debug(f"Grid: {grid.dimensions}\n")

        # Flood fill from start position
        region = grid.flood_fill(start, "#")

        # Show region info
        self.debug(c.success("✓ Region found!"))
        self.debug(f"  Size: {region.size} cells")
        self.debug(f"  Bounds: {region.bounds}")

        # Get bounding box dimensions
        (min_x, min_y), (max_x, max_y) = region.bounds
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        self.debug(f"  Dimensions: {width}x{height}")

        # Calculate density
        bounding_area = width * height
        density = region.size / bounding_area if bounding_area > 0 else 0
        self.debug(f"  Density: {density:.1%} of bounding box\n")

        # Visualize the region
        self.debug(c.cyan("Region visualization:"))
        self.debug(
            lambda: print_grid_region(grid, region, separator=" ", show_coords=True)
        )

        return region.size

    def part2(self, grid: Grid[str]) -> int:
        """
        Use find_regions to find all connected components.
        """
        self.debug(c.bold("\n=== Part 2: Find All Regions ===\n"))

        # Find all '#' regions
        self.debug(c.yellow("Finding all connected '#' regions...\n"))
        regions = grid.find_regions("#")

        # Sort by size (largest first)
        sorted_regions = sorted(regions, key=lambda r: r.size, reverse=True)

        self.debug(c.success(f"✓ Found {len(sorted_regions)} regions!\n"))

        # Show details for each region
        total_cells = 0
        for i, region in enumerate(sorted_regions, 1):
            self.debug(c.cyan(f"Region {i}:"))
            self.debug(f"  Size: {region.size} cells")
            self.debug(f"  Bounds: {region.bounds}")

            (min_x, min_y), (max_x, max_y) = region.bounds
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            self.debug(f"  Dimensions: {width}x{height}\n")

            total_cells += region.size

        # Summary
        self.debug(c.yellow("Summary:"))
        self.debug(f"  Total regions: {len(sorted_regions)}")
        self.debug(f"  Total cells: {total_cells}")
        self.debug(f"  Average size: {total_cells / len(sorted_regions):.1f} cells")
        self.debug(f"  Largest: {sorted_regions[0].size if sorted_regions else 0}")
        self.debug(f"  Smallest: {sorted_regions[-1].size if sorted_regions else 0}\n")

        # Visualize largest region
        if sorted_regions:
            self.debug(c.cyan("Largest region visualization:"))
            self.debug(
                lambda: print_grid_region(
                    grid, sorted_regions[0], separator=" ", show_coords=True
                )
            )

        return len(sorted_regions)
