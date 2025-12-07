"""Advanced grid tests: pathfinding, transformations, regions, animations."""

import sys
import unittest
from io import StringIO

from fraocme.grid import (
    CARDINALS,
    DIAGONALS,
    Grid,
)
from fraocme.grid.pathfinding import (
    a_star,
    bfs,
    chebyshev_distance,
    dijkstra,
    manhattan_distance,
)
from fraocme.grid.printer import (
    print_grid,
    print_grid_animated,
    print_grid_animated_with_direction,
    print_grid_diff,
    print_grid_heatmap,
    print_grid_neighbors,
    print_grid_path,
    print_grid_region,
)
from fraocme.grid.regions import find_regions, flood_fill


class TestPathfinding(unittest.TestCase):
    """Test pathfinding algorithms."""

    def setUp(self):
        """Create test grids."""
        # Simple 5x5 maze (all rows same length)
        self.maze = Grid.from_chars("S....\n#.###\n.....\n###..\n...#E")

    def test_manhattan_distance(self):
        """Test Manhattan distance calculation."""
        self.assertEqual(manhattan_distance((0, 0), (3, 4)), 7)
        self.assertEqual(manhattan_distance((1, 1), (1, 1)), 0)
        self.assertEqual(manhattan_distance((5, 0), (0, 5)), 10)

    def test_chebyshev_distance(self):
        """Test Chebyshev distance calculation."""
        self.assertEqual(chebyshev_distance((0, 0), (3, 4)), 4)
        self.assertEqual(chebyshev_distance((1, 1), (1, 1)), 0)
        self.assertEqual(chebyshev_distance((5, 0), (0, 5)), 5)

    def test_bfs_path_found(self):
        """Test BFS finds a path."""
        start = self.maze.find_first("S")
        end = self.maze.find_first("E")
        path = bfs(
            self.maze,
            start,
            end,
            is_walkable=lambda pos, val: val != "#",
            directions=CARDINALS,
        )
        self.assertIsNotNone(path)
        self.assertEqual(path.positions[0], start)
        self.assertEqual(path.positions[-1], end)

    def test_bfs_no_path(self):
        """Test BFS when no path exists."""
        grid = Grid.from_chars("S#E")
        start = grid.find_first("S")
        end = grid.find_first("E")
        path = bfs(
            grid,
            start,
            end,
            is_walkable=lambda pos, val: val != "#",
            directions=CARDINALS,
        )
        self.assertIsNone(path)

    def test_dijkstra_weighted(self):
        """Test Dijkstra with varying costs."""
        grid = Grid.from_chars("S.~E")
        start = grid.find_first("S")
        end = grid.find_first("E")

        def cost_fn(src, sv, dst, dv):
            if dv == "#":
                return float("inf")
            return 5 if dv == "~" else 1

        path = dijkstra(grid, start, end, cost_fn=cost_fn, directions=CARDINALS)
        self.assertIsNotNone(path)
        # Path should avoid ~ if possible
        self.assertGreater(path.cost, 2)  # More than straight line due to costs

    def test_a_star_finds_path(self):
        """Test A* algorithm."""
        start = self.maze.find_first("S")
        end = self.maze.find_first("E")
        path = a_star(
            self.maze,
            start,
            end,
            heuristic=manhattan_distance,
            cost_fn=lambda src, sv, dst, dv: float("inf") if dv == "#" else 1,
            directions=CARDINALS,
        )
        self.assertIsNotNone(path)
        self.assertEqual(path.positions[0], start)
        self.assertEqual(path.positions[-1], end)

    def test_a_star_with_diagonal(self):
        """Test A* with diagonal movement."""
        grid = Grid.from_chars("S...\n....\n...E")
        start = grid.find_first("S")
        end = grid.find_first("E")
        path = a_star(
            grid,
            start,
            end,
            heuristic=chebyshev_distance,
            cost_fn=lambda src, sv, dst, dv: 1,
            directions=CARDINALS + DIAGONALS,
        )
        self.assertIsNotNone(path)
        # With diagonals, path should be shorter
        self.assertLess(path.length, 8)


class TestTransformations(unittest.TestCase):
    """Test grid transformations."""

    def setUp(self):
        """Create test grid."""
        self.grid = Grid.from_chars("abc\ndef\nghi")

    def test_rotate_90(self):
        """Test 90-degree clockwise rotation."""
        rotated = self.grid.rotate_90()
        self.assertEqual(rotated.at(0, 0), "g")
        self.assertEqual(rotated.at(2, 2), "c")

    def test_rotate_180(self):
        """Test 180-degree rotation."""
        rotated = self.grid.rotate_180()
        self.assertEqual(rotated.at(0, 0), "i")
        self.assertEqual(rotated.at(2, 2), "a")

    def test_rotate_270(self):
        """Test 270-degree rotation."""
        rotated = self.grid.rotate_270()
        self.assertEqual(rotated.at(0, 0), "c")
        self.assertEqual(rotated.at(2, 2), "g")

    def test_flip_horizontal(self):
        """Test horizontal flip."""
        flipped = self.grid.flip_horizontal()
        self.assertEqual(flipped.at(0, 0), "c")
        self.assertEqual(flipped.at(2, 0), "a")

    def test_flip_vertical(self):
        """Test vertical flip."""
        flipped = self.grid.flip_vertical()
        self.assertEqual(flipped.at(0, 0), "g")
        self.assertEqual(flipped.at(0, 2), "a")

    def test_transpose(self):
        """Test matrix transpose."""
        transposed = self.grid.transpose()
        self.assertEqual(transposed.at(0, 0), "a")
        self.assertEqual(transposed.at(1, 0), "d")
        self.assertEqual(transposed.at(0, 1), "b")
        self.assertEqual(transposed.dimensions, (3, 3))


class TestRegions(unittest.TestCase):
    """Test region analysis."""

    def test_flood_fill_basic(self):
        """Test basic flood fill."""
        grid = Grid.from_chars("...\n.#.\n...")
        region = flood_fill(grid, (0, 0), predicate=lambda val: val != "#")
        self.assertEqual(region.size, 8)  # All cells except #

    def test_flood_fill_enclosed(self):
        """Test flood fill doesn't cross boundaries."""
        grid = Grid.from_chars("###\n#.#\n###")
        region = flood_fill(grid, (1, 1), predicate=lambda val: val != "#")
        self.assertEqual(region.size, 1)  # Only center cell

    def test_flood_fill_by_value(self):
        """Test flood fill targeting specific values."""
        grid = Grid.from_chars("aaa\naab\naaa")
        region = flood_fill(grid, (0, 0), predicate=lambda val: val == "a")
        self.assertEqual(region.size, 8)

    def test_find_regions_multiple(self):
        """Test finding multiple disconnected regions."""
        grid = Grid.from_chars(".#.\n###\n.#.")
        regions = find_regions(grid, predicate=lambda val: val == ".")
        self.assertEqual(len(regions), 4)  # 4 corner regions


class TestPrinterFunctions(unittest.TestCase):
    """Test printer functions."""

    def setUp(self):
        """Create test grids."""
        self.grid = Grid.from_ints("123\n456\n789")
        self.char_grid = Grid.from_chars("abc\ndef\nghi")

    def _capture_print(self, func):
        """Helper to capture printed output."""
        captured = StringIO()
        sys.stdout = captured
        func()
        sys.stdout = sys.__stdout__
        return captured.getvalue()

    def test_print_grid_basic(self):
        """Test basic grid printing."""
        output = self._capture_print(lambda: print_grid(self.char_grid))
        self.assertIn("abc", output)
        self.assertIn("def", output)

    def test_print_grid_heatmap(self):
        """Test heatmap printing."""
        output = self._capture_print(
            lambda: print_grid_heatmap(self.grid, separator=" ")
        )
        self.assertIn("1", output)
        self.assertIn("9", output)

    def test_print_grid_path(self):
        """Test path printing."""
        path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        output = self._capture_print(lambda: print_grid_path(self.char_grid, path))
        self.assertIn("S", output)  # Start marker
        self.assertIn("E", output)  # End marker

    def test_print_grid_diff(self):
        """Test diff printing."""
        grid1 = Grid.from_chars("abc\ndef\nghi")
        grid2 = grid1.set(1, 1, "X")
        output = self._capture_print(lambda: print_grid_diff(grid1, grid2))
        self.assertIn("X", output)

    def test_print_grid_region(self):
        """Test region printing."""
        region = flood_fill(self.char_grid, (0, 0), predicate=lambda v: v != "#")
        output = self._capture_print(lambda: print_grid_region(self.char_grid, region))
        self.assertIn("Region size", output)

    def test_print_grid_neighbors(self):
        """Test neighbors printing."""
        output = self._capture_print(
            lambda: print_grid_neighbors(self.char_grid, (1, 1))
        )
        self.assertIn("Center:", output)
        self.assertIn("Neighbors:", output)

    def test_print_grid_animated_basic(self):
        """Test animated grid printing."""
        positions = [(0, 0), (1, 0), (2, 0)]
        output = self._capture_print(
            lambda: print_grid_animated(
                self.char_grid,
                positions,
                delay=0.01,
                show_coords=False,
                show_step_count=False,
            )
        )
        self.assertIn("Animation complete", output)

    def test_print_grid_animated_with_direction(self):
        """Test animated grid with direction."""
        from fraocme.grid.directions import EAST

        positions = [(0, 0), (1, 0), (2, 0)]
        directions = [EAST, EAST, EAST]
        output = self._capture_print(
            lambda: print_grid_animated_with_direction(
                self.char_grid,
                positions,
                directions=directions,
                delay=0.01,
                show_coords=False,
                show_step_count=False,
            )
        )
        self.assertIn("Animation complete", output)

    def test_animated_with_frame_skipping(self):
        """Test animation respects max_iterations."""
        # Create many positions
        positions = [(i % 3, i // 3) for i in range(100)]
        output = self._capture_print(
            lambda: print_grid_animated(
                self.char_grid,
                positions,
                delay=0.01,
                max_iterations=10,
                show_coords=False,
                show_step_count=False,
            )
        )
        # Should mention frame skipping
        self.assertIn("Showing", output)


class TestGridSetOperations(unittest.TestCase):
    """Test Grid set/update operations."""

    def setUp(self):
        """Create test grid."""
        self.grid = Grid.from_ints("123\n456\n789")

    def test_set_updates_value(self):
        """Test single cell update."""
        new_grid = self.grid.set(1, 1, 99)
        self.assertEqual(new_grid.at(1, 1), 99)
        self.assertEqual(self.grid.at(1, 1), 5)  # Original unchanged

    def test_bulk_set(self):
        """Test multiple cell updates."""
        changes = {(0, 0): 0, (2, 2): 0, (1, 1): 0}
        new_grid = self.grid.bulk_set(changes)
        self.assertEqual(new_grid.at(0, 0), 0)
        self.assertEqual(new_grid.at(2, 2), 0)
        self.assertEqual(new_grid.at(1, 1), 0)
        self.assertEqual(new_grid.at(0, 1), 4)  # Unchanged

    def test_map_transform(self):
        """Test map function."""
        doubled = self.grid.map(lambda x: x * 2)
        self.assertEqual(doubled.at(0, 0), 2)
        self.assertEqual(doubled.at(1, 1), 10)


class TestGridMisc(unittest.TestCase):
    """Miscellaneous Grid tests."""

    def test_grid_equality(self):
        """Test grid equality comparison."""
        grid1 = Grid.from_chars("abc\ndef")
        grid2 = Grid.from_chars("abc\ndef")
        grid3 = Grid.from_chars("xyz\nuvw")
        self.assertEqual(grid1, grid2)
        self.assertNotEqual(grid1, grid3)

    def test_grid_hash(self):
        """Test grid hashing."""
        grid1 = Grid.from_chars("abc\ndef")
        grid2 = Grid.from_chars("abc\ndef")
        # Same content should have same hash
        self.assertEqual(hash(grid1), hash(grid2))
        # Can be used in sets
        s = {grid1, grid2}
        self.assertEqual(len(s), 1)

    def test_grid_repr(self):
        """Test grid representation."""
        grid = Grid.from_chars("abc\ndef")
        repr_str = repr(grid)
        self.assertIn("Grid[str]", repr_str)
        self.assertIn("3x2", repr_str)

    def test_grid_str(self):
        """Test grid string representation."""
        grid = Grid.from_chars("abc\ndef")
        str_repr = str(grid)
        self.assertIn("Grid[str]", str_repr)
        self.assertIn("3x2", str_repr)

    def test_in_bounds(self):
        """Test boundary checking."""
        grid = Grid.from_chars("abc\ndef")
        self.assertTrue(grid.in_bounds((0, 0)))
        self.assertTrue(grid.in_bounds((2, 1)))
        self.assertFalse(grid.in_bounds((3, 1)))
        self.assertFalse(grid.in_bounds((0, 2)))

    def test_filter_positions(self):
        """Test filtering positions."""
        grid = Grid.from_ints("123\n456\n789")
        # Find all positions with value >= 6
        positions = grid.filter_positions(lambda pos, val: val >= 6)
        self.assertEqual(len(positions), 4)
        self.assertIn((2, 1), positions)  # value 6
        self.assertIn((0, 2), positions)  # value 7


if __name__ == "__main__":
    unittest.main()
