import sys
import unittest
from io import StringIO

from fraocme.common.printer import print_max_in_rows


class TestCommonPrinter(unittest.TestCase):
    """Test common printer functions."""

    def test_print_max_in_rows_basic(self):
        """Test print_max_in_rows prints max of each row."""
        grid = [[1, 5, 3], [2, 4, 6], [7, 2, 1]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertEqual(output, ["5", "6", "7"])

    def test_print_max_in_rows_single_row(self):
        """Test print_max_in_rows with single row."""
        grid = [[1, 5, 3]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        self.assertEqual(output, "5")

    def test_print_max_in_rows_single_element(self):
        """Test print_max_in_rows with single element per row."""
        grid = [[1], [5], [3]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertEqual(output, ["1", "5", "3"])

    def test_print_max_in_rows_empty_row(self):
        """Test print_max_in_rows handles empty row."""
        grid = [[1, 2], [], [3, 4]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertEqual(output[0], "2")
        self.assertEqual(output[1], "Empty row")
        self.assertEqual(output[2], "4")

    def test_print_max_in_rows_negative_numbers(self):
        """Test print_max_in_rows with negative numbers."""
        grid = [[-1, -5, -3], [-2, -4, -6]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertEqual(output, ["-1", "-2"])

    def test_print_max_in_rows_mixed_numbers(self):
        """Test print_max_in_rows with mixed positive/negative numbers."""
        grid = [[1, -5, 3], [-2, 4, -6]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertEqual(output, ["3", "4"])


if __name__ == "__main__":
    unittest.main()
