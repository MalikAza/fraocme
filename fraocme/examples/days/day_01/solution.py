"""
Day 1 Example: Grid Navigation with Modern Direction System

This example demonstrates the new Grid module features:
- Parsing grids with Grid.from_chars()
- Finding positions with grid.find()
- Moving with Direction objects (NORTH, SOUTH, EAST, WEST)
- Using turn_left() and turn_right()
- Tracking visited positions
"""

from fraocme import Solver
from fraocme.grid import (
    NORTH,
    Grid,
    turn_right,
)
from fraocme.ui.colors import c


class Day1(Solver):
    def __init__(self, day: int = 1, debug: bool = False):
        super().__init__(day=day, debug=debug, copy_input=True)

    def parse(self, raw: str) -> Grid[str]:
        """Parse the input into a Grid."""
        return Grid.from_chars(raw)

    def part1(self, grid: Grid[str]) -> int:
        """
        Simulate guard movement on a grid.

        Rules:
        - Guard starts at '^' facing NORTH
        - If obstacle '#' ahead, turn right 90°
        - Otherwise, move forward
        - Count distinct positions visited
        """
        # Find starting position
        start = grid.find_first("^")
        if not start:
            return 0

        self.debug(c.cyan(f"Starting at: {start}"))
        self.debug(f"Grid dimensions: {grid.dimensions}")

        # Track state
        pos = start
        direction = NORTH
        visited = {pos}

        # Simulate movement
        steps = 0
        while True:
            steps += 1

            # Try to move forward
            next_pos = grid.neighbor(pos, direction)

            # Check if we left the grid
            if next_pos is None:
                self.debug(c.yellow(f"Left grid after {steps} steps"))
                break

            # Check what's at the next position
            next_cell = grid.at(*next_pos)

            if next_cell == "#":
                # Obstacle ahead - turn right
                direction = turn_right(direction)
                self.debug(
                    c.muted(f"Obstacle at {next_pos}, turning to {direction.name}")
                )
            else:
                # Move forward
                pos = next_pos
                visited.add(pos)

                if steps % 100 == 0:
                    self.debug(
                        c.muted(f"Step {steps}: visited {len(visited)} positions")
                    )

            # Safety check to prevent infinite loops
            if steps > 10000:
                self.debug(c.red("Safety limit reached!"))
                break

        result = len(visited)
        self.debug(c.green(f"Distinct positions visited: {result}"))
        return result

    def part2(self, grid: Grid[str]) -> int:
        """
        Find positions where adding an obstacle creates a loop.

        Strategy:
        - Try placing obstacle at each empty position
        - Simulate guard movement
        - Detect loops by tracking (position, direction) states
        - Count positions that cause loops
        """
        start = grid.find_first("^")
        if not start:
            return 0

        # Get all empty positions (excluding start)
        empty_positions = [pos for pos in grid.filter_positions(lambda p, v: v == ".")]

        self.debug(c.cyan(f"Testing {len(empty_positions)} positions for loops"))

        loop_count = 0

        for test_idx, obstacle_pos in enumerate(empty_positions):
            # Create new grid with obstacle
            test_grid = grid.set(*obstacle_pos, "#")

            # Simulate movement with loop detection
            if self._creates_loop(test_grid, start):
                loop_count += 1

            # Progress update
            if (test_idx + 1) % 100 == 0:
                self.debug(
                    c.muted(
                        f"Tested {test_idx + 1}/{len(empty_positions)}, "
                        f"found {loop_count} loops"
                    )
                )

        self.debug(c.green(f"Positions causing loops: {loop_count}"))
        return loop_count

    def _creates_loop(self, grid: Grid[str], start: tuple[int, int]) -> bool:
        """Check if guard gets stuck in a loop on this grid."""
        pos = start
        direction = NORTH

        # Track (position, direction) states to detect loops
        states = {(pos, direction)}

        steps = 0
        max_steps = 10000  # Safety limit

        while steps < max_steps:
            steps += 1

            # Try to move forward
            next_pos = grid.neighbor(pos, direction)

            # If we left the grid, no loop
            if next_pos is None:
                return False

            # Check what's ahead
            next_cell = grid.at(*next_pos)

            if next_cell == "#":
                # Turn right at obstacle
                direction = turn_right(direction)
            else:
                # Move forward
                pos = next_pos

            # Check if we've been in this state before
            state = (pos, direction)
            if state in states:
                return True  # Loop detected!

            states.add(state)

        # Safety limit reached - assume it's a loop
        return True
