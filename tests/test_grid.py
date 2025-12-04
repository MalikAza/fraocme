import unittest
from io import StringIO
import sys

from fraocme.grid.parser import lines, int_grid
from fraocme.grid.printer import print_grid
from fraocme.grid.utils import GridUtils


class TestGridParser(unittest.TestCase):
    """Test grid parser functions."""

    def test_lines_basic(self):
        """Test parsing lines."""
        raw = "hello\nworld\ntest"
        self.assertEqual(lines(raw), ["hello", "world", "test"])

    def test_lines_with_whitespace(self):
        """Test lines strips whitespace."""
        raw = "\nhello\nworld\n"
        self.assertEqual(lines(raw), ["hello", "world"])

    def test_lines_single_line(self):
        """Test lines with single line."""
        self.assertEqual(lines("hello"), ["hello"])

    def test_int_grid_basic(self):
        """Test parsing 2D integer grid."""
        raw = "123\n456"
        expected = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(int_grid(raw), expected)

    def test_int_grid_single_row(self):
        """Test int_grid with single row."""
        raw = "12345"
        expected = [[1, 2, 3, 4, 5]]
        self.assertEqual(int_grid(raw), expected)

    def test_int_grid_single_column(self):
        """Test int_grid with single column."""
        raw = "1\n2\n3"
        expected = [[1], [2], [3]]
        self.assertEqual(int_grid(raw), expected)

    def test_int_grid_with_whitespace(self):
        """Test int_grid strips whitespace."""
        raw = "\n123\n456\n"
        expected = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(int_grid(raw), expected)


class TestGridPrinter(unittest.TestCase):
    """Test grid printer functions."""

    def test_print_grid_basic(self):
        """Test printing basic grid."""
        grid = [['a', 'b'], ['c', 'd']]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        print_grid(grid)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip().split('\n')
        self.assertEqual(output[0], 'ab')
        self.assertEqual(output[1], 'cd')

    def test_print_grid_with_separator(self):
        """Test printing grid with separator."""
        grid = [['a', 'b'], ['c', 'd']]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        print_grid(grid, separator=' ')
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip().split('\n')
        self.assertEqual(output[0], 'a b')
        self.assertEqual(output[1], 'c d')

    def test_print_grid_with_numbers(self):
        """Test printing grid with numbers."""
        grid = [[1, 2], [3, 4]]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        print_grid(grid, separator=',')
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip().split('\n')
        self.assertEqual(output[0], '1,2')
        self.assertEqual(output[1], '3,4')

    def test_print_grid_with_highlight(self):
        """Test printing grid with highlighted positions."""
        grid = [['a', 'b'], ['c', 'd']]
        highlight = {(0, 0), (1, 1)}
        
        captured_output = StringIO()
        sys.stdout = captured_output
        print_grid(grid, highlight=highlight)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        # Should contain ANSI codes for highlighting
        self.assertIn('\033[', output)

    def test_print_grid_empty(self):
        """Test printing empty grid."""
        grid = []
        
        captured_output = StringIO()
        sys.stdout = captured_output
        print_grid(grid)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertEqual(output, '')


class TestGridUtils(unittest.TestCase):
    """Test GridUtils class."""

    def setUp(self):
        """Set up test fixtures."""
        self.grid_str = "abc\ndef\nghi"
        self.grid_list = ['abc', 'def', 'ghi']
        self.utils_str = GridUtils(self.grid_str)
        self.utils_list = GridUtils(self.grid_list)

    def test_initialization_from_string(self):
        """Test initializing from string."""
        self.assertEqual(self.utils_str.grid, self.grid_list)

    def test_initialization_from_list(self):
        """Test initializing from list."""
        self.assertEqual(self.utils_list.grid, self.grid_list)

    def test_is_position_out_of_bounds_valid(self):
        """Test position within bounds."""
        self.assertFalse(self.utils_str.is_position_out_of_bounds((0, 0)))
        self.assertFalse(self.utils_str.is_position_out_of_bounds((2, 2)))

    def test_is_position_out_of_bounds_invalid(self):
        """Test position out of bounds."""
        self.assertTrue(self.utils_str.is_position_out_of_bounds((-1, 0)))
        self.assertTrue(self.utils_str.is_position_out_of_bounds((0, -1)))
        self.assertTrue(self.utils_str.is_position_out_of_bounds((3, 0)))
        self.assertTrue(self.utils_str.is_position_out_of_bounds((0, 3)))

    def test_get_position_down(self):
        """Test getting position below."""
        result = self.utils_str.get_position_down((1, 1))
        self.assertEqual(result, (1, 2))

    def test_get_position_up(self):
        """Test getting position above."""
        result = self.utils_str.get_position_up((1, 1))
        self.assertEqual(result, (1, 0))

    def test_get_position_right(self):
        """Test getting position to the right."""
        result = self.utils_str.get_position_right((1, 1))
        self.assertEqual(result, (2, 1))

    def test_get_position_left(self):
        """Test getting position to the left."""
        result = self.utils_str.get_position_left((1, 1))
        self.assertEqual(result, (0, 1))

    def test_get_position_diagonal(self):
        """Test getting diagonal positions."""
        pos = (1, 1)
        self.assertEqual(self.utils_str.get_position_down_right(pos), (2, 2))
        self.assertEqual(self.utils_str.get_position_down_left(pos), (0, 2))
        self.assertEqual(self.utils_str.get_position_up_right(pos), (2, 0))
        self.assertEqual(self.utils_str.get_position_up_left(pos), (0, 0))

    def test_get_positions_in_corners(self):
        """Test getting all corner positions."""
        corners = self.utils_str.get_positions_in_corners((1, 1))
        
        self.assertEqual(corners['down_right'], (2, 2))
        self.assertEqual(corners['down_left'], (0, 2))
        self.assertEqual(corners['up_right'], (2, 0))
        self.assertEqual(corners['up_left'], (0, 0))

    def test_get_positions_in_nsew(self):
        """Test getting cardinal direction positions."""
        nsew = self.utils_str.get_positions_in_nsew((1, 1))
        
        self.assertEqual(nsew['down'], (1, 2))
        self.assertEqual(nsew['right'], (2, 1))
        self.assertEqual(nsew['up'], (1, 0))
        self.assertEqual(nsew['left'], (0, 1))

    def test_get_positions_around(self):
        """Test getting all 8 surrounding positions."""
        around = self.utils_str.get_positions_around((1, 1))
        
        self.assertEqual(around['down'], (1, 2))
        self.assertEqual(around['right'], (2, 1))
        self.assertEqual(around['up'], (1, 0))
        self.assertEqual(around['left'], (0, 1))
        self.assertEqual(around['down_right'], (2, 2))
        self.assertEqual(around['down_left'], (0, 2))
        self.assertEqual(around['up_right'], (2, 0))
        self.assertEqual(around['up_left'], (0, 0))

    def test_get_position_by_direction_up(self):
        """Test getting position by direction (up)."""
        result = self.utils_str.get_position_by_direction((1, 1), '^')
        self.assertEqual(result, (1, 0))

    def test_get_position_by_direction_down(self):
        """Test getting position by direction (down)."""
        result = self.utils_str.get_position_by_direction((1, 1), 'v')
        self.assertEqual(result, (1, 2))

    def test_get_position_by_direction_right(self):
        """Test getting position by direction (right)."""
        result = self.utils_str.get_position_by_direction((1, 1), '>')
        self.assertEqual(result, (2, 1))

    def test_get_position_by_direction_left(self):
        """Test getting position by direction (left)."""
        result = self.utils_str.get_position_by_direction((1, 1), '<')
        self.assertEqual(result, (0, 1))

    def test_search_value_single(self):
        """Test searching for a value that appears once."""
        result = self.utils_str.search_value('a')
        self.assertEqual(result, ((0, 0),))

    def test_search_value_multiple(self):
        """Test searching for a value that appears multiple times."""
        grid = GridUtils("aba\nbab\naba")
        result = grid.search_value('a')
        self.assertEqual(len(result), 5)  # a at (0,0), (2,0), (1,1), (0,2), (2,2)
        self.assertIn((0, 0), result)
        self.assertIn((2, 0), result)

    def test_search_value_not_found(self):
        """Test searching for a value not in grid."""
        result = self.utils_str.search_value('x')
        self.assertEqual(result, ())

    def test_get_cell_value_valid(self):
        """Test getting cell value at valid position."""
        self.assertEqual(self.utils_str.get_cell_value((0, 0)), 'a')
        self.assertEqual(self.utils_str.get_cell_value((1, 1)), 'e')
        self.assertEqual(self.utils_str.get_cell_value((2, 2)), 'i')

    def test_get_cell_value_out_of_bounds(self):
        """Test getting cell value at invalid position."""
        self.assertIsNone(self.utils_str.get_cell_value((-1, 0)))
        self.assertIsNone(self.utils_str.get_cell_value((0, -1)))
        self.assertIsNone(self.utils_str.get_cell_value((3, 0)))
        self.assertIsNone(self.utils_str.get_cell_value((0, 3)))

    def test_search_start_and_end_with_markers(self):
        """Test finding start and end positions."""
        grid = GridUtils("S..\n...\n..E", start_value='S', end_value='E')
        self.assertEqual(grid.start, (0, 0))
        self.assertEqual(grid.end, (2, 2))

    def test_search_start_and_end_not_found(self):
        """Test when start/end not found."""
        grid = GridUtils("abc\ndef\nghi", start_value='S', end_value='E')
        self.assertIsNone(grid.start)
        self.assertIsNone(grid.end)


if __name__ == '__main__':
    unittest.main()
