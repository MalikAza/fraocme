import re
import sys
import unittest
from io import StringIO

from fraocme.grid import EAST, NORTH, SOUTH, WEST, Grid
from fraocme.grid.printer import print_grid


class TestGridParser(unittest.TestCase):
    """Test Grid factory methods."""

    def test_from_ints(self):
        """Test parsing 2D integer grid."""
        raw = "123\n456"
        grid = Grid.from_ints(raw)
        self.assertEqual(grid.at(0, 0), 1)
        self.assertEqual(grid.at(2, 1), 6)
        self.assertEqual(grid.dimensions, (3, 2))

    def test_from_chars(self):
        """Test parsing character grid."""
        raw = "abc\ndef"
        grid = Grid.from_chars(raw)
        self.assertEqual(grid.at(0, 0), "a")
        self.assertEqual(grid.at(2, 1), "f")
        self.assertEqual(grid.dimensions, (3, 2))

    def test_from_dense(self):
        """Test parsing space-separated grid."""
        raw = "10 20 30\n40 50 60"
        grid = Grid.from_dense(raw)
        self.assertEqual(grid.at(0, 0), 10)
        self.assertEqual(grid.at(2, 1), 60)

    def test_create_with_default_value(self):
        """Test creating grid with default value."""
        grid = Grid.create(3, 2, ".")
        self.assertEqual(grid.dimensions, (3, 2))
        self.assertEqual(grid.at(0, 0), ".")
        self.assertEqual(grid.at(2, 1), ".")
        # Check all cells have the default value
        for y in range(2):
            for x in range(3):
                self.assertEqual(grid.at(x, y), ".")

    def test_create_with_custom_value(self):
        """Test creating grid with custom value."""
        grid = Grid.create(2, 3, 0)
        self.assertEqual(grid.dimensions, (2, 3))
        self.assertEqual(grid.at(0, 0), 0)
        self.assertEqual(grid.at(1, 2), 0)

    def test_create_invalid_dimensions(self):
        """Test creating grid with invalid dimensions."""
        with self.assertRaises(ValueError):
            Grid.create(0, 5, ".")
        with self.assertRaises(ValueError):
            Grid.create(5, 0, ".")
        with self.assertRaises(ValueError):
            Grid.create(-1, 5, ".")


class TestGridPrinter(unittest.TestCase):
    def strip_row_header(self, s):
        parts = s.lstrip().split(None, 1)
        if len(parts) == 2 and parts[0].isdigit():
            return re.sub(r"^[^\w\d]+", "", parts[1])
        return s

    def strip_ansi(self, s):
        return re.sub(r"\x1b\[[0-9;]*m", "", s)

    """Test grid printer functions."""

    def test_print_grid_basic(self):
        """Test printing basic grid."""
        grid = [["a", "b"], ["c", "d"]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_grid(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        # First line is info, second is col header, then grid rows
        self.assertIn("Grid", self.strip_ansi(output[0]))
        self.assertEqual(self.strip_row_header(self.strip_ansi(output[2])), "ab")
        self.assertEqual(self.strip_row_header(self.strip_ansi(output[3])), "cd")

    def test_print_grid_with_separator(self):
        """Test printing grid with separator."""
        grid = [["a", "b"], ["c", "d"]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_grid(grid, separator=" ")
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertIn("Grid", self.strip_ansi(output[0]))
        self.assertEqual(self.strip_row_header(self.strip_ansi(output[2])), "a b")
        self.assertEqual(self.strip_row_header(self.strip_ansi(output[3])), "c d")

    def test_print_grid_with_numbers(self):
        """Test printing grid with numbers."""
        grid = [[1, 2], [3, 4]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_grid(grid, separator=",")
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertIn("Grid", self.strip_ansi(output[0]))
        self.assertEqual(self.strip_row_header(self.strip_ansi(output[2])), "1,2")
        self.assertEqual(self.strip_row_header(self.strip_ansi(output[3])), "3,4")

    def test_print_grid_with_highlight(self):
        """Test printing grid with highlighted positions."""
        grid = [["a", "b"], ["c", "d"]]
        highlight = {(0, 0), (1, 1)}

        captured_output = StringIO()
        sys.stdout = captured_output
        print_grid(grid, highlight=highlight)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        # Should contain ANSI codes for highlighting
        self.assertIn("\033[", output)

    def test_print_grid_empty(self):
        """Test printing empty grid."""
        grid = []

        captured_output = StringIO()
        sys.stdout = captured_output
        print_grid(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        # Should print only the info line for empty grid
        self.assertIn("Grid", output)


class TestGridCore(unittest.TestCase):
    """Test Grid core functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.grid = Grid.from_chars("abc\ndef\nghi")

    def test_in_bounds_valid(self):
        """Test position within bounds."""
        self.assertTrue(self.grid.in_bounds((0, 0)))
        self.assertTrue(self.grid.in_bounds((2, 2)))

    def test_in_bounds_invalid(self):
        """Test position out of bounds."""
        self.assertFalse(self.grid.in_bounds((-1, 0)))
        self.assertFalse(self.grid.in_bounds((0, -1)))
        self.assertFalse(self.grid.in_bounds((3, 0)))
        self.assertFalse(self.grid.in_bounds((0, 3)))

    def test_neighbor_cardinals(self):
        """Test getting neighbor positions in cardinal directions."""
        pos = (1, 1)
        self.assertEqual(self.grid.neighbor(pos, NORTH), (1, 0))
        self.assertEqual(self.grid.neighbor(pos, SOUTH), (1, 2))
        self.assertEqual(self.grid.neighbor(pos, EAST), (2, 1))
        self.assertEqual(self.grid.neighbor(pos, WEST), (0, 1))

    def test_neighbor_with_distance(self):
        """Test getting neighbor at different distances."""
        pos = (1, 1)
        self.assertEqual(self.grid.neighbor(pos, EAST, 2), None)  # Out of bounds
        self.assertEqual(self.grid.neighbor(pos, NORTH, 1), (1, 0))
        self.assertEqual(self.grid.neighbor(pos, WEST, 1), (0, 1))

    def test_get_neighbors_cardinal(self):
        """Test getting cardinal neighbors."""
        neighbors = self.grid.get_neighbors((1, 1), include_diagonals=False)
        self.assertEqual(len(neighbors), 4)
        self.assertIn((1, 0), neighbors)  # up
        self.assertIn((1, 2), neighbors)  # down
        self.assertIn((0, 1), neighbors)  # left
        self.assertIn((2, 1), neighbors)  # right

    def test_get_neighbors_all(self):
        """Test getting all 8 neighbors."""
        neighbors = self.grid.get_neighbors((1, 1), include_diagonals=True)
        self.assertEqual(len(neighbors), 8)

    def test_find_single(self):
        """Test finding a value that appears once."""
        result = self.grid.find("a")
        self.assertEqual(result, [(0, 0)])

    def test_find_multiple(self):
        """Test searching for a value that appears multiple times."""
        grid = Grid.from_chars("aba\nbab\naba")
        result = grid.find("a")
        self.assertEqual(len(result), 5)  # a at (0,0), (2,0), (1,1), (0,2), (2,2)
        self.assertIn((0, 0), result)
        self.assertIn((2, 0), result)

    def test_find_not_found(self):
        """Test searching for a value not in grid."""
        result = self.grid.find("x")
        self.assertEqual(result, [])

    def test_at_valid(self):
        """Test getting cell value at valid position."""
        self.assertEqual(self.grid.at(0, 0), "a")
        self.assertEqual(self.grid.at(1, 1), "e")
        self.assertEqual(self.grid.at(2, 2), "i")

    def test_find_first(self):
        """Test finding first occurrence of a value."""
        grid = Grid.from_chars("S..\n...\n..E")
        self.assertEqual(grid.find_first("S"), (0, 0))
        self.assertEqual(grid.find_first("E"), (2, 2))
        self.assertIsNone(grid.find_first("X"))


if __name__ == "__main__":
    unittest.main()
