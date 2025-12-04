import unittest
from io import StringIO
import sys

from fraocme.ui import Colors, c
from fraocme.ui.printer import print_header, print_section, print_grid, print_max_in_rows


class TestColors(unittest.TestCase):
    """Test Colors class ANSI codes."""

    def test_colors_exist(self):
        """Test that color constants exist."""
        self.assertIsNotNone(Colors.RED)
        self.assertIsNotNone(Colors.GREEN)
        self.assertIsNotNone(Colors.BLUE)
        self.assertIsNotNone(Colors.RESET)

    def test_colors_are_strings(self):
        """Test that colors are strings."""
        self.assertIsInstance(Colors.RED, str)
        self.assertIsInstance(Colors.GREEN, str)

    def test_bright_colors_exist(self):
        """Test bright color codes exist."""
        self.assertIsNotNone(Colors.BRIGHT_RED)
        self.assertIsNotNone(Colors.BRIGHT_GREEN)

    def test_background_colors_exist(self):
        """Test background color codes exist."""
        self.assertIsNotNone(Colors.BG_RED)
        self.assertIsNotNone(Colors.BG_GREEN)

    def test_styles_exist(self):
        """Test style codes exist."""
        self.assertIsNotNone(Colors.BOLD)
        self.assertIsNotNone(Colors.UNDERLINE)
        self.assertIsNotNone(Colors.ITALIC)


class TestColorHelper(unittest.TestCase):
    """Test c color helper class."""

    def test_red_wraps_text(self):
        """Test red color wraps text."""
        result = c.red("error")
        self.assertIn("error", result)
        self.assertIn(Colors.RED, result)
        self.assertIn(Colors.RESET, result)

    def test_green_wraps_text(self):
        """Test green color wraps text."""
        result = c.green("success")
        self.assertIn("success", result)
        self.assertIn(Colors.GREEN, result)

    def test_blue_wraps_text(self):
        """Test blue color wraps text."""
        result = c.blue("info")
        self.assertIn("info", result)
        self.assertIn(Colors.BLUE, result)

    def test_cyan_wraps_text(self):
        """Test cyan color wraps text."""
        result = c.cyan("test")
        self.assertIn("test", result)
        self.assertIn(Colors.CYAN, result)

    def test_bright_red_wraps_text(self):
        """Test bright red color."""
        result = c.bright_red("warning")
        self.assertIn("warning", result)
        self.assertIn(Colors.BRIGHT_RED, result)

    def test_yellow_wraps_text(self):
        """Test yellow color."""
        result = c.yellow("caution")
        self.assertIn("caution", result)
        self.assertIn(Colors.YELLOW, result)

    def test_bold_wraps_text(self):
        """Test bold style."""
        result = c.bold("important")
        self.assertIn("important", result)
        self.assertIn(Colors.BOLD, result)

    def test_wrap_format(self):
        """Test wrap format is correct."""
        result = c.red("text")
        # Should be color + text + reset
        expected = f"{Colors.RED}text{Colors.RESET}"
        self.assertEqual(result, expected)

    def test_nested_wrapping(self):
        """Test that multiple wraps work."""
        result = c.bold(c.green("text"))
        self.assertIn("text", result)
        # Contains both codes
        self.assertIn(Colors.BOLD, result)
        self.assertIn(Colors.GREEN, result)


class TestPrintHeader(unittest.TestCase):
    """Test print_header function."""

    def test_print_header_output(self):
        """Test header prints correctly."""
        captured = StringIO()
        sys.stdout = captured
        
        print_header("Test Header")
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("Test Header", output)
        self.assertIn("═", output)

    def test_print_header_width(self):
        """Test header respects width parameter."""
        captured = StringIO()
        sys.stdout = captured
        
        print_header("Test", width=20)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        # Line should be approximately 20 chars wide
        lines = output.strip().split("\n")
        header_line = lines[0]
        self.assertEqual(len(header_line), 20)

    def test_print_header_default_width(self):
        """Test header has default width."""
        captured = StringIO()
        sys.stdout = captured
        
        print_header("X")
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        lines = output.strip().split("\n")
        header_line = lines[0]
        self.assertEqual(len(header_line), 40)


class TestPrintSection(unittest.TestCase):
    """Test print_section function."""

    def test_print_section_output(self):
        """Test section prints correctly."""
        captured = StringIO()
        sys.stdout = captured
        
        print_section("Test Section")
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("Test Section", output)
        self.assertIn("─", output)

    def test_print_section_width(self):
        """Test section respects width parameter."""
        captured = StringIO()
        sys.stdout = captured
        
        print_section("Test", width=30)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        lines = output.strip().split("\n")
        section_line = lines[0]
        self.assertEqual(len(section_line), 30)

    def test_print_section_default_width(self):
        """Test section has default width."""
        captured = StringIO()
        sys.stdout = captured
        
        print_section("X")
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        lines = output.strip().split("\n")
        section_line = lines[0]
        self.assertEqual(len(section_line), 40)


class TestPrintGrid(unittest.TestCase):
    """Test print_grid function."""

    def test_print_grid_basic(self):
        """Test grid prints correctly."""
        captured = StringIO()
        sys.stdout = captured
        
        grid = [["a", "b"], ["c", "d"]]
        print_grid(grid)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("ab", output)
        self.assertIn("cd", output)

    def test_print_grid_with_separator(self):
        """Test grid with custom separator."""
        captured = StringIO()
        sys.stdout = captured
        
        grid = [["a", "b"], ["c", "d"]]
        print_grid(grid, sep=",")
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("a,b", output)
        self.assertIn("c,d", output)

    def test_print_grid_numbers(self):
        """Test grid with numbers."""
        captured = StringIO()
        sys.stdout = captured
        
        grid = [[1, 2, 3], [4, 5, 6]]
        print_grid(grid)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("123", output)
        self.assertIn("456", output)

    def test_print_grid_empty(self):
        """Test empty grid."""
        captured = StringIO()
        sys.stdout = captured
        
        grid = []
        print_grid(grid)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertEqual(output.strip(), "")

    def test_print_grid_single_row(self):
        """Test grid with single row."""
        captured = StringIO()
        sys.stdout = captured
        
        grid = [["x", "y", "z"]]
        print_grid(grid, sep="-")
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("x-y-z", output)


class TestPrintMaxInRows(unittest.TestCase):
    """Test print_max_in_rows function."""

    def test_print_max_in_rows_basic(self):
        """Test finding max in rows."""
        captured = StringIO()
        sys.stdout = captured
        
        grid = [[1, 2, 3], [4, 5, 6]]
        print_max_in_rows(grid)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("3", output)
        self.assertIn("6", output)

    def test_print_max_in_rows_unequal_lengths(self):
        """Test max with unequal row lengths."""
        captured = StringIO()
        sys.stdout = captured
        
        grid = [[1, 5], [2, 3, 8], [10]]
        print_max_in_rows(grid)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("5", output)
        self.assertIn("8", output)
        self.assertIn("10", output)

    def test_print_max_in_rows_single_row(self):
        """Test max with single row."""
        captured = StringIO()
        sys.stdout = captured
        
        grid = [[1, 5, 3]]
        print_max_in_rows(grid)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("5", output)

    def test_print_max_in_rows_with_negatives(self):
        """Test max with negative numbers."""
        captured = StringIO()
        sys.stdout = captured
        
        grid = [[-5, -1, -10], [2, -3, 5]]
        print_max_in_rows(grid)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("-1", output)
        self.assertIn("5", output)

    def test_print_max_in_rows_empty_row(self):
        """Test max with empty row."""
        captured = StringIO()
        sys.stdout = captured
        
        grid = [[1, 2], [], [3, 4]]
        print_max_in_rows(grid)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("2", output)
        self.assertIn("Empty row", output)
        self.assertIn("4", output)


if __name__ == "__main__":
    unittest.main()
