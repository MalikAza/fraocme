"""
Day 4 Example: Pathfinding Algorithms

Demonstrates BFS, Dijkstra, and A* pathfinding on grids.
"""

from fraocme import Solver
from fraocme.grid import Grid, a_star, bfs, dijkstra, manhattan_distance
from fraocme.grid.printer import print_grid_path
from fraocme.profiling.timer import timed
from fraocme.ui.colors import c


class Day4(Solver):
    def __init__(self, day: int = 4, debug: bool = False):
        super().__init__(day=day, debug=debug, copy_input=True)

    def parse(self, raw: str) -> Grid[str]:
        """Parse the input into a grid."""
        return Grid.from_chars(raw)

    @timed
    def part1(self, grid: Grid[str]) -> int:
        """
        Use BFS to find shortest path (unweighted).
        """
        self.debug(c.bold("\n=== Part 1: BFS Pathfinding ===\n"))

        # Find start and end
        start = grid.find_first("S")
        end = grid.find_first("E")

        if not start or not end:
            self.debug(c.red("Start or End not found!"))
            return 0

        self.debug(c.cyan(f"Start: {start}, End: {end}"))
        self.debug(f"Grid: {grid.dimensions}\n")

        # Run BFS
        self.debug(c.yellow("Running BFS (uniform cost)..."))
        path = bfs(
            grid,
            start=start,
            end=end,
            is_walkable=lambda pos, val: val != "#",
        )

        if path:
            self.debug(c.success("\n✓ Path found!"))
            self.debug(f"  Length: {path.length} steps")
            self.debug(f"  Cost: {path.cost}")

            # Visualize the path
            self.debug(c.cyan("\nPath visualization:"))
            self.debug(
                lambda: print_grid_path(
                    grid, path.positions, separator=" ", show_coords=True
                )
            )

            return path.length
        else:
            self.debug(c.red("\n✗ No path found!"))
            return 0

    @timed
    def part2(self, grid: Grid[str]) -> int:
        """
        Compare Dijkstra and A* with weighted costs.
        """
        self.debug(c.bold("\n=== Part 2: Dijkstra vs A* ===\n"))

        start = grid.find_first("S")
        end = grid.find_first("E")

        if not start or not end:
            return 0

        # Define cost function (different terrain costs)
        def cost_fn(from_pos, from_val, to_pos, to_val):
            """Cost function: dots cost 1, start/end cost 1."""
            if to_val in (".", "S", "E"):
                return 1
            return float("inf")  # Walls are impassable

        # Run Dijkstra
        self.debug(c.yellow("1. Running Dijkstra's algorithm..."))
        dijkstra_path = dijkstra(
            grid,
            start=start,
            end=end,
            cost_fn=cost_fn,
        )

        if dijkstra_path:
            self.debug(c.success("   ✓ Dijkstra path found!"))
            self.debug(f"     Length: {dijkstra_path.length} steps")
            self.debug(f"     Cost: {dijkstra_path.cost}")

        # Run A*
        self.debug(c.yellow("\n2. Running A* algorithm..."))
        astar_path = a_star(
            grid,
            start=start,
            end=end,
            heuristic=manhattan_distance,
            cost_fn=cost_fn,
        )

        if astar_path:
            self.debug(c.success("   ✓ A* path found!"))
            self.debug(f"     Length: {astar_path.length} steps")
            self.debug(f"     Cost: {astar_path.cost}")

        # Compare results
        if dijkstra_path and astar_path:
            self.debug(c.cyan("\n3. Comparison:"))
            self.debug(
                f"   Both found optimal path: {dijkstra_path.cost == astar_path.cost}"
            )
            self.debug(
                f"   Same path taken: {dijkstra_path.positions == astar_path.positions}"
            )

            # Visualize A* path
            self.debug(c.cyan("\nA* path visualization:"))
            self.debug(
                lambda: print_grid_path(
                    grid, astar_path.positions, separator=" ", show_coords=True
                )
            )

            return int(astar_path.cost)

        return 0
