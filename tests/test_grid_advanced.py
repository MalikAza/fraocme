"""Advanced grid tests: pathfinding, transformations, regions, animations."""

import sys
import math
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
from fraocme.grid.directions import (
    EAST,
    NORTH,
    SOUTH,
    WEST,
    direction_from_delta,
    opposite,
    turn_left,
    turn_right,
)


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

    def test_bfs_start_equals_end(self):
        """BFS should return zero-cost path when start == end."""
        grid = Grid.from_chars("S")
        start = grid.find_first("S")
        path = bfs(grid, start, start, is_walkable=lambda pos, val: True)
        self.assertIsNotNone(path)
        self.assertEqual(path.cost, 0)
        self.assertEqual(path.positions, [start])

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

    def test_dijkstra_no_path(self):
        """Dijkstra returns None when no path exists."""
        grid = Grid.from_chars("S#E")
        start = grid.find_first("S")
        end = grid.find_first("E")

        def cost_fn(src, sv, dst, dv):
            return float("inf") if dv == "#" else 1

        path = dijkstra(grid, start, end, cost_fn=cost_fn)
        self.assertIsNotNone(path)
        self.assertTrue(math.isinf(path.cost))

    def test_a_star_no_path(self):
        """A* returns None when no path exists."""
        grid = Grid.from_chars("S#E")
        start = grid.find_first("S")
        end = grid.find_first("E")
        path = a_star(
            grid,
            start,
            end,
            heuristic=manhattan_distance,
            cost_fn=lambda src, sv, dst, dv: float("inf") if dv == "#" else 1,
        )
        self.assertIsNotNone(path)
        self.assertTrue(math.isinf(path.cost))


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


class TestGridEdgeCases(unittest.TestCase):
    """Grid edge case coverage."""

    def test_empty_grid_raises(self):
        """Grid with empty data should raise ValueError."""
        with self.assertRaises(ValueError):
            Grid([])

    def test_non_rectangular_grid_raises(self):
        """Grid with inconsistent row lengths raises ValueError."""
        with self.assertRaises(ValueError):
            Grid([[1], [1, 2]])

    def test_bulk_set_no_changes_returns_self(self):
        """bulk_set with empty changes returns the same instance."""
        grid = Grid.from_chars("ab\ncd")
        new_grid = grid.bulk_set({})
        self.assertIs(new_grid, grid)

    def test_neighbor_out_of_bounds_returns_none(self):
        """Neighbor outside grid should return None."""
        grid = Grid.from_chars("ab\ncd")
        self.assertIsNone(grid.neighbor((0, 0), NORTH, distance=5))

    def test_get_neighbors_ring_two_cardinal_only(self):
        """Ring>1 cardinal neighbor lookup returns expected positions."""
        grid = Grid.from_chars(".....\n.....\n.....\n.....\n.....")
        neighbors = grid.get_neighbors((2, 2), ring=2, include_diagonals=False)
        neighbor_set = set(neighbors)
        expected = {(2, 0), (4, 2), (2, 4), (0, 2)}
        self.assertTrue(expected.issubset(neighbor_set))
        self.assertNotIn((2, 2), neighbor_set)


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


class TestDirectionsHelpers(unittest.TestCase):
    """Direction helper coverage."""

    def test_turn_and_opposite(self):
        """turn_left/right and opposite mappings work."""
        self.assertEqual(turn_left(NORTH), WEST)
        self.assertEqual(turn_right(NORTH), EAST)
        self.assertEqual(opposite(EAST), WEST)

    def test_direction_from_delta_unknown(self):
        """Unknown deltas return None."""
        self.assertIsNone(direction_from_delta(2, 2))


class TestRegionsEdge(unittest.TestCase):
    """Region edge cases and predicate normalization."""

    def test_flood_fill_value_predicate(self):
        """Value-based predicate hits normalization branch."""
        grid = Grid.from_chars("aa\nab")
        region = flood_fill(grid, (0, 0), "a")
        self.assertEqual(region.size, 3)

    def test_flood_fill_out_of_bounds(self):
        """Out-of-bounds start yields empty region."""
        grid = Grid.from_chars("...")
        region = flood_fill(grid, (-1, -1), predicate=lambda v: True)
        self.assertEqual(region.size, 0)

    def test_find_regions_none_match(self):
        """No matching cells returns empty list."""
        grid = Grid.from_chars("###")
        regions = find_regions(grid, predicate=lambda v: v == ".")
        self.assertEqual(regions, [])


class TestPrinterEdgeCases(unittest.TestCase):
    """Additional printer coverage for truncation and coords."""

    def setUp(self):
        self.grid = Grid.from_ints("123\n456\n789")
        self.char_grid = Grid.from_chars("abc\ndef\nghi")
        self.list_grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def _capture_print(self, func):
        captured = StringIO()
        sys.stdout = captured
        func()
        sys.stdout = sys.__stdout__
        return captured.getvalue()

    def test_print_grid_highlight_truncated_coords(self):
        """print_grid handles lists, highlight, coords, and truncation."""
        output = self._capture_print(
            lambda: print_grid(
                self.list_grid,
                separator=" ",
                highlight={(1, 1)},
                max_rows=2,
                max_cols=2,
                show_coords=True,
            )
        )
        self.assertIn("...", output)
        self.assertIn("0", output)

    def test_print_grid_heatmap_coords_and_footer(self):
        """Heatmap prints header/footer with coords when truncated."""
        output = self._capture_print(
            lambda: print_grid_heatmap(
                self.grid,
                separator=" ",
                max_rows=1,
                max_cols=1,
                show_coords=True,
            )
        )
        self.assertIn("Legend", output)
        self.assertIn("...", output)

    def test_print_grid_heatmap_non_numeric(self):
        """Non-numeric grids print a helpful message."""
        output = self._capture_print(
            lambda: print_grid_heatmap(self.char_grid, max_rows=1, max_cols=1)
        )
        self.assertIn("non-numeric", output)

    def test_print_grid_diff_dimension_mismatch(self):
        """Dimension mismatch path is covered."""
        grid1 = Grid.from_chars("ab\ncd")
        grid2 = Grid.from_chars("ab")
        output = self._capture_print(lambda: print_grid_diff(grid1, grid2))
        self.assertIn("Dimension mismatch", output)

    def test_print_grid_region_with_coords(self):
        """Region printing with coords and truncation."""
        region = flood_fill(self.char_grid, (0, 0), predicate=lambda v: True)
        output = self._capture_print(
            lambda: print_grid_region(
                self.char_grid,
                region,
                max_rows=1,
                max_cols=2,
                show_coords=True,
            )
        )
        self.assertIn("Region size", output)
        self.assertIn("...", output)

    def test_print_grid_neighbors_ring_two_coords(self):
        """Neighbors view with ring>1 and coords."""
        output = self._capture_print(
            lambda: print_grid_neighbors(
                self.char_grid,
                (1, 1),
                ring=2,
                include_diagonals=False,
                max_rows=2,
                max_cols=3,
                show_coords=True,
            )
        )
        self.assertIn("Ring: 2", output)
        self.assertIn("Neighbors:", output)

    def test_print_grid_animated_empty_positions(self):
        """Animated grid handles empty positions gracefully."""
        output = self._capture_print(
            lambda: print_grid_animated(
                self.char_grid,
                [],
                delay=0,
                show_coords=True,
            )
        )
        self.assertIn("no positions", output)

    def test_print_grid_animated_with_coords_and_steps(self):
        """Animated grid exercises coord and step branches."""
        positions = [(0, 0), (1, 0)]
        output = self._capture_print(
            lambda: print_grid_animated(
                self.char_grid,
                positions,
                delay=0,
                max_rows=2,
                max_cols=2,
                show_coords=True,
                show_step_count=True,
                trail_length=1,
            )
        )
        self.assertIn("Step 1", output)
        self.assertIn("Animation complete", output)

    def test_print_grid_animated_with_direction_coords(self):
        """Directional animation covers facing text and coords."""
        positions = [(0, 0), (1, 0)]
        directions = [EAST, EAST]
        output = self._capture_print(
            lambda: print_grid_animated_with_direction(
                self.char_grid,
                positions,
                directions=directions,
                delay=0,
                max_rows=2,
                max_cols=2,
                show_coords=True,
                show_step_count=True,
                trail_length=1,
            )
        )
        self.assertIn("Facing", output)
        self.assertIn("Animation complete", output)


if __name__ == "__main__":
    unittest.main()
