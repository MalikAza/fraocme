"""
Day 3 Example: Animated Grid Visualization

Demonstrates grid animation functions for visualizing movement and simulations.
"""

from fraocme import Solver
from fraocme.grid import NORTH, Grid, turn_right
from fraocme.grid.printer import (
    print_grid,
    print_grid_animated,
    print_grid_animated_with_direction,
)
from fraocme.ui.colors import c


class Day103(Solver):
    def parse(self, raw: str) -> Grid[str]:
        """Parse the input into a grid."""
        return Grid.from_chars(raw)

    def simulate_patrol(self, grid: Grid[str]) -> tuple[list[tuple[int, int]], list]:
        """
        Simulate guard patrol and return positions + directions.
        """
        start = grid.find_first("^")
        if not start:
            return [], []

        position = start
        direction = NORTH
        positions = [position]
        directions = [direction]
        visited = {(position, direction)}

        steps = 0
        max_steps = 100  # Limit for demo

        while steps < max_steps:
            steps += 1
            next_pos = grid.neighbor(position, direction)

            # Check if out of bounds
            if next_pos is None:
                break

            # Check for obstacle
            if grid.at(*next_pos) == "#":
                # Turn right at obstacle
                direction = turn_right(direction)
                directions.append(direction)
                positions.append(position)
            else:
                # Move forward
                position = next_pos
                positions.append(position)
                directions.append(direction)

            # Check for loop
            state = (position, direction)
            if state in visited:
                break
            visited.add(state)

        return positions, directions

    def part1(self, grid: Grid[str]) -> int:
        """
        Demonstrate basic animation (position only).
        """
        self.debug(lambda: print_grid(grid, separator=" ", max_cols=15, max_rows=10))
        self.debug(c.bold("\n=== Part 1: Basic Animation ===\n"))

        # Simulate patrol
        positions, _ = self.simulate_patrol(grid)
        self.debug(c.cyan(f"Simulated {len(positions)} steps"))

        # Show animation (first 30 steps for speed)
        if len(positions) > 0:
            self.debug(c.yellow("\nAnimating patrol (basic mode)..."))
            self.debug(c.dim("Press Ctrl+C to stop\n"))

            # Short delay to let user read
            import time

            time.sleep(1)

            # Animate with trail
            self.debug(
                lambda: print_grid_animated(
                    grid,
                    positions[:50],  # First 50 steps
                    delay=0.1,  # 100ms per frame
                    trail_length=5,  # Show last 5 positions
                    separator=" ",
                    show_coords=True,
                    max_cols=10,
                    max_rows=10,
                    erase_after=True,  # Erase grid after animation
                )
            )

        return len(set(positions))

    def part2(self, grid: Grid[str]) -> int:
        """
        Demonstrate directional animation (with arrows).
        """
        self.debug(c.bold("\n=== Part 2: Directional Animation ===\n"))

        # Simulate patrol
        positions, directions = self.simulate_patrol(grid)
        self.debug(c.cyan(f"Simulated {len(positions)} steps"))

        # Show animation with directional arrows
        if len(positions) > 0:
            self.debug(c.yellow("\nAnimating with directional arrows..."))
            self.debug(c.dim("Press Ctrl+C to stop\n"))

            # Short delay
            import time

            time.sleep(1)

            # Animate with directions
            self.debug(
                lambda: print_grid_animated_with_direction(
                    grid,
                    positions[:300],  # First 30 steps
                    directions[:300],
                    delay=0.1,  # 100ms per frame
                    trail_length=8,  # Longer trail
                    separator=" ",
                    max_cols=25,
                    show_coords=True,
                )
            )

        return len(set(positions))
